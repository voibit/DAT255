#!/usr/bin/env python
# coding: utf-8
import os
from pathlib import Path, PurePath
import math
from fastai.vision.all import *
import torchaudio
import tempfile
from flask import Flask, request,jsonify

# Weights, edit this. 
weights_path = Path('/app/local/models/')
weights = 'resnet50-93'

sr = 32000
imgsize = 460
Fmax = sr / 2 # Nyquist. 

# STFT LF
Nfft_lf = 32768 # 32768 is the cloeset power of 2 above the sample rate.  
Fbin_lf = Fmax / Nfft_lf
Nskip_lf = Nfft_lf //5  # 80% overlap  
rng_lf = Nskip_lf * (imgsize-1)
stft_lf = torchaudio.transforms.Spectrogram(Nfft_lf,hop_length=Nskip_lf, power=2,return_complex=False ).cuda()

# STFT HF
Nfft_hf = 1024
Fbin_hf = Fmax / Nfft_hf
Nskip_hf =(1024 * 3)//4 # 25% overlap
rng_hf = Nskip_hf * imgsize + Nfft_hf
stft_hf = torchaudio.transforms.Spectrogram(Nfft_hf,hop_length=Nskip_hf, power=2,return_complex=False ).cuda()

# Patch learner for batch predictions
def predict_batch(self, item, rm_type_tfms=None, with_input=False):
    dl = self.dls.test_dl(item, rm_type_tfms=rm_type_tfms, num_workers=0)
    ret, _,mask = self.get_preds(dl=dl, with_decoded=True)
    return ret, mask
Learner.predict_batch = predict_batch


def readWav(p: Path, rand=True):
    frames = torchaudio.info(p).num_frames
    last = frames-rng_lf
    wav = torch.Tensor()  
    # Repeat wav if not long enough
    while last < 0:
        wav = torch.cat((wav,torchaudio.load(p)[0]),1)
        last += frames
    # Random start point
    start = random.randint(0,last) if rand else int(last/2)
    
    # If enough frames
    if frames-rng_lf > 0:
        return torchaudio.load(p, num_frames=rng_lf, frame_offset=start)[0]
    else: 
        wav = torch.cat((wav,torchaudio.load(p)[0]),1)
        return wav[:,start:start+rng_lf]

def normSpec(spec):
    # take the logarithm of the values
    ret = torch.log10(spec+1e-20)
    mean = torch.mean(ret)
    std = torch.std(ret)    
    ret =  (ret - mean) / (std*4) + 0.5
    return torch.clamp(ret, min=0, max=1)  


def wavToSpecs(wavs : torch.Tensor, hf_idx=0):
    lf = stft_lf(wavs)[0]
    lf0 = normSpec(lf[:imgsize,:imgsize])
    lf1 = normSpec(lf[imgsize:imgsize*2,:imgsize])
    hf = stft_hf(wavs[:,hf_idx:hf_idx+rng_hf])[0]
    hf = normSpec(hf[12:imgsize+12,:imgsize])
    return torch.stack((lf0,lf1,hf),0)



class Spectrogram(TensorImageBase):
    """Type to represent a spectogram which knows show itself"""
    @classmethod
    def create(cls, o: Tensor):
        return cls(o)
    
    def show(self, figsize=None, ctx=None, **kwargs): 
        channels = self.shape[0]
        t = self
        if not isinstance(t, Tensor): return ctx
        if figsize is None: figsize=(10,10)   
        return show_images(t, nrows=1, ncols=channels)

# Make a fastai Transform
class SpectrogramTransform(RandTransform):
    "A transform handler for multiple `spect` transforms"
    split_idx,order=None,0  # 0 = HIGH prio
    #def __init__(self, train_aug, valid_aug): store_attr()
    def __init__(self): 
        store_attr()
    
    def before_call(self, b, split_idx):
        self.idx = split_idx
    
    def encodes(self, p : Path):
        
        if self.idx == 0: #Train transform
            hf_idx = random.randint(0,rng_lf-rng_hf)
            wav = readWav(p, True)
        else: #Valid transform
            hf_idx = (rng_lf-rng_hf) //2
            wav = readWav(p, False)
        return wavToSpecs(wav.cuda(), hf_idx)
    
    #def decodes(self, x): return TitledImage(x,'test')
def get_wavs(p : Path) :
    return get_files(p,'.wav')

def label_func(p : Path):
    if PurePath(p).parent.name == "AmbientSE": return []
    return [PurePath(p).parent.parent.name]

def predTensor(p, overlap=0.5):
    frames = torchaudio.info(p).num_frames
    wav,sr = torchaudio.load(p)
    
    # Resample audio if different samplerate
    if(sr != 32000): 
        print('resampling to 32000..')
        wav = torchaudio.functional.resample(wav, sr, 32000)
        sr = 32000
        frames = wav.shape[1]
        print('resampling done..')
    # Repeat wav if not long enough
    
    while wav.shape[1]-rng_lf < 0 :
        wav = torch.cat((wav,wav),1)    
    spec = wavToSpecs(wav[:,0:rng_lf].cuda())[None,:,:,:]
    # cat rest of the frames
    hf_idx = (rng_lf-rng_hf) //2
    start = int(Nskip_lf *(1-overlap) * (imgsize))
    runs = int((frames-Nfft_lf)/(Nskip_lf*(1-overlap))/imgsize) +1 
    for i in range(1,runs):
        idx = start*i
        if idx+rng_lf > frames: # add last frame 
            spec = torch.cat((spec,wavToSpecs(wav[:,-rng_lf:].cuda(),hf_idx)[None,:,:,:]),0)
            break
        # Add frame according to index
        spec = torch.cat((spec,wavToSpecs(wav[:,idx:idx+rng_lf].cuda(),hf_idx)[None,:,:,:]),0)
    return Spectrogram.create(spec)

learn = load_learner(weights_path / weights)

def prettyPred(pbatch):
    p = torch.mean(pbatch[0]*(pbatch[1]+ 0.0* ~pbatch[1]) ,0).tolist()
    return {k: v for k,v in zip(learn.dls.vocab, p)}  

app = Flask(__name__)
#@app.route('/')
#def idx():
#    return jsonify(test)

@app.route('/', methods=['POST'])
def classify():
    
    if 'file' not in request.files:
        return jsonify({'error':'no file element uploaded'})
    file = request.files['file']
    ext = Path(file.filename).suffix
    with tempfile.NamedTemporaryFile(suffix='.'+ext) as tmp:
        file.save(tmp)
        fname = Path(tmp.name)
        try: 
            p = prettyPred(learn.predict_batch(predTensor(fname)))
        except:
            return jsonify({'error':'Something failed..'})
        else:
            return jsonify(p)

app.run(port=8088,host='0.0.0.0')