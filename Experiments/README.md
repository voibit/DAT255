# Experiments and exploration
This folder contains notebooks where i have experimentented with different libraries and signal processing parameteres.  
Some may not work as is. at least paths pointing to datasets should be checked.  

 - [1. Audio processing](./1.%20Audio%20processing.ipynb)
    - Contains experimentations dealing with reading audio, normalizing it, and making spectrograms
 - [2. DeepShip](./2.%20DeepShip.ipynb)
    - Exploring the deepShip Dataset
 - [3. DeepShip 3ch cqt](./3.%20DeepShip%203ch%20cqt.ipynb)
    - Training a resnet50 model using constant q transforms.
 - [4. DeepShip 6ch](./4.%20DeepShip%206ch.ipynb)
    - Training a 6 channel resnet50 model with pretrained weights, using constant q transform
    - based/ inspired upon https://dpird-dma.github.io/blog/Multispectral-image-classification-Transfer-Learning/
 - [5. ShipsEar](./5.%20ShipsEar.ipynb)
    - Exploring the ShipsEar Dataset
 - [6. Resample noise](./6.%20Resample%20noise.ipynb)
    - Resample noise from the ShipsEar dataset so it can be trained with the DeepShip dataset
 - [7. Tensorflow](./7.%20Tensorflow.ipynb)
    - Tried to train on different models in tensorflow 
 - [8. deepship_3ch_qct_polar](./8.%20deepship_3ch_qct_polar.ipynb)
    - Experimenting with polar representation of QCT Spectrograms