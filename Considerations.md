# Considerations
There are a lot of choises using a library, framework so on and so forth.
Here are some of my considerations, which may be wrong or outdated. 

## Datasets
- DeepShip (22gb, 4 classes)
- ShipEar (awaiting replay)

## Audio processing libaries
- librosa https://librosa.org/doc/latest/index.html
    - No GPU support, this makes it too slow. |
    
- nnAudio https://kinwaicheuk.github.io/nnAudio/index.html
    - GPU support, it even has trainable FFT kernels. 
    - compatible with pytorch
    - clones some paret of librosa functionallity (eg. mel spec)
    - has CQT support
    
- fastaudio https://fastaudio.github.io/
    - Builds ontop of librosa
    - Implements augementation
    - Requires older versions of pytorch, fastaudo, fastcore (I did not manage to get it running)

- torchaudio https://pytorch.org/audio/stable/index.html
    - GPU support
    - handels IO
    - lacks CQT

During this project i have used nnAudio and torchaudio. I prefare torchaudio because it handles the io, supports read offsets as argument, and even normaizes audio by default. with that said nnAudio is also a great, and is a powerfull library.


## Signalprocessing 
### Mel Spectrograms
In audio classification with neural networks it is common to use mel spectrograms.  
Mel are designed for speech. That may not be ideal for ship classification.
For instance, in speech, there are no useful spectral information below our pitch. As a result the firtst mel filterbank "removes" that information. That is not ideal for classifying ships that can radiate noise at those frequencies. 

### STFTs
With [Short time Fourier transform](https://en.wikipedia.org/wiki/Short-time_Fourier_transform) (STFTs) you need to know what kind of temporal or spectral resolution you need. 

### CQTs
[Constant Q Transforms](https://en.wikipedia.org/wiki/Constant-Q_transform) (QCTs) are more flexible than FTFTs. The balance time/ spectral resolution, but are heavier to compute.

## DNN Library
fastai & pytorch was for me a littlebit faster when training models compared to tensorflow, even with almost identical model. 
