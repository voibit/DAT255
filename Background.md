# Background
Audio classification has been around for a long time.  
Above water, before RADAR was a thing, it was used as [early waring systems for incoming airplanes](https://rarehistoricalphotos.com/aircraft-detection-radar-1917-1940/).  
Below water, submarines and abover water warships alike, have tried to find each other for as far as they have existed.

For submerged vehicles it is important to know what is above them, for example in order to avoid crashing in them when surfacing. With the increase of autonomous underwater vehicles (AUVs), the demand for automatic detection and classfication systems is also increasing. The reaction pattern is very different knowing there is a unpredictable fishing vessel somewhere above your AUV, and knowing theres a mercent vessel. Merchent vessels are known to go straight courses as fast, or cheap as possible. 

At the core level, sound is just preasure differeces. When things move, they tend to generate several kinds of vibrations(frequencies). Those vibrations can propogate and generate preasure differences in different mediums. Almoast every ship has some kind of propuiltion system, consisting of a propeller, shaft and one or more engines. These makes noise, or rather a collection of noises, which will propogate through the ocean, and can be picked up from a distance. 

Classification of ships by sound is a hard problem. Similar noises can be learned. One should expext that two ships of the same category, consists of the same type of noises, and sounds more or less similar. If this holds true, it implies that to learn ship classes (classification), it is really down to exposure to enough noises within those different classes. 

This means that neural networks (NNs) can be used to slove ship classification by sound. The problem is that most NNs are not designed for sound classificastion. However, there are a lot of NNs that ca do image classification, and do it really well.

## Using images to represent sound
A convinient way to view a sound is using some singal processing, more spesifically; the fourier transform (FT).
If we have a frame of sound samples, and apply a fourier transform, we get the magnitudes of the different frequencies in that frame of samples. That is easier to work with rather than descrete samples, but that dont give us how the freqiencies change over time.
If we take the FT of several frames, with some overlap, it is called a short time fourier transform (STFT).
Now we can see how frequencies change over time. Another name for STFT i a spectrogram.

Things get more complicated when you have to choose different signal processing parameters such as framelengths, overlap, and so on. You can read about more of my parameter considerations in [this](./DeepShip/1.%20deepship_3ch.ipynb#%20Signal%20processing) notebook.  
Some general considerations can be found [here](./Considerations.md).
