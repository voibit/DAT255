# docker
This folder contains scirpts responsible for building the docker images, and running jupyterlab and rest server. 

## fastai 
`Dockerfile` contains the my custom fastai image. It is based on [anibali's](https://github.com/anibali/docker-pytorch)
pytorch image.  
The reason I did not use the official pytorch or fastai images is because they *were* not up to date, and did not contain torchaudio, nor cuda libraries for building lightGBM.  
Fastai is added by cherrypicking code from [here](https://github.com/fastai/docker-containers)

LightGBM is build from source for gpu acceleration to work. It is not used by this project, but is useful in machine learing experimentation. 


## tf
`Dockerfile.tf` contains the custom tensorflow image.
It is based on the official, just adding jupyterlab, tensorflow extended, and other useful python modules. 
This image is not used by the final notebooks or inference for this project, it extists for experimentation. 


## Startup scripts

`run_jupyterlab.sh` is a simple bash script to run jupyterlab on port 80. 
it is used by docker-compose. 

`run_rest.sh` is a simple bash script to run the inference rest server. it points to `DeepShip/rest.py`
and is used by docker-compose. 


## Other stuff 
`Dockerfile.audio` is an experiment setting up fastaudio. It is not compatible with the latest version of fastai, and is therefore broken. 

