# Datasets
There are not many datasets around that focus on classification of ships.
By the time of choosing this project, I could only find two.

If you are going to train a model using notebooks from this repo, extract the DeepShip dataset here, so that its path is `dataset/DeepShip/` 

## ShipsEar
We have ShipsEar[[1]](#1) from the coast of Spain.
This dataset consisting of about 1.5 hours of recordings, distributed on 11 vessel types and noise. ShipsEar is freely aviable for educational purposeses upon request to the papres corresponding author.  

## DeepShip
Fairly recently DeepShip[[2]](#2) emerged. 
It consits of about 45 hours of recordings from the coast of Canada, distributed on 4 classes.  
The paper states they achieve 77.53% accuracy score using CQT features.   
DeepShip is freely aviable upon request to the papres corresponding author.


## Comparison 
Generally ShipsEar recordings seems to be closer to the recorder, or clipped so that they are shorter. This makes the hydrophone catches more noise, and to some extent makes the problem of detection, and asumeably classification too easy.

DeepShip is a lot bigger, and is fairly (at least in terms of time) dirstibuted across classes. This makes it more ideal for training a neural network. Generally, DeepShips recording distances seem to vary, which theoretically makes it a better candidate to train. 

In this project I have trained models on the DeepShip dataset, and included noise from ShipsEar dataset when training with noise.

# Referances
<a id="1">[1]</a>
Santos-Domínguez, D., Torres-Guijarro, S., Cardenal-López, A., Pena-Gimenez, A. (2016).  
ShipsEar: An underwater vessel noise database  
Appl. Acoust. 2016, 113, 64–69.  
https://doi.org/10.1016/j.apacoust.2016.06.008

<a id="2">[2]</a>
Irfan, M., Jiangbin, Z., Ali, S., Iqbal, M., Masood, Z., Hamid, U. (2021)    
DeepShip: An Underwater Acoustic Benchmark Dataset and a Separable Convolution Based Autoencoder for Classification  
Expert Syst. Appl. 2021, 183, 115270  
https://doi.org/10.1016/j.eswa.2021.115270  
