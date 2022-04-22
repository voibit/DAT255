FROM anibali/pytorch:latest
ARG BUILD=prod

# Set up time zone.
ENV TZ=UTC
RUN sudo ln -snf /usr/share/zoneinfo/$TZ /etc/localtime


RUN sudo apt-get update && sudo apt-get upgrade -y \
# Install libraries required by LightGBM
&& sudo apt-get install -y --no-install-recommends \
libnvidia-compute-510 nvidia-opencl-dev opencl-headers git cmake build-essential libboost-dev libboost-system-dev libboost-filesystem-dev \
&& sudo rm -rf /var/lib/apt/lists/*


# Install system libraries required by OpenCV.
# && sudo apt-get install -y software-properties-common rsync git libglib2.0-dev graphviz nano ffmpeg libsm6 libxext6 \


RUN conda update -n base -c defaults conda 
RUN conda install -y pytorch::torchaudio
RUN conda install -c conda-forge -y libsndfile jupyter_contrib_nbextensions jupyterlab xgboost
RUN pip install --upgrade pip
RUN pip install albumentations \
    catalyst \
    captum \
    "fastprogress>=0.1.22" \
    graphviz \
    jupyter \
    kornia \
    matplotlib \
    nbconvert \
    nbdev \
    neptune-client \
    opencv-python-headless \
    pandas \
    pillow \
    pyarrow \
    pydicom \
    pyyaml \
    scikit-learn \
    scikit-image \
    scipy \
    sentencepiece \
    spacy \
    tensorboard \
    wandb \
    opendatasets \
    xlrd \
    openpyxl \
    timm \
    seaborn \
    timesformer-pytorch \
    torchsummary \
    flask

RUN git clone https://github.com/fastai/fastai.git --depth 1  && git clone https://github.com/fastai/fastcore.git --depth 1
RUN /bin/bash -c "if [[ $BUILD == 'prod' ]] ; then echo \"Production Build\" && cd fastai && pip install . && cd ../fastcore && pip install . && cd ../; fi"
RUN /bin/bash -c "if [[ $BUILD == 'dev' ]] ; then echo \"Development Build\" && cd fastai && pip install -e \".[dev]\" && cd ../fastcore && pip install -e \".[dev]\" && cd ../; fi"


# Install lightgbm
RUN git clone --recursive https://github.com/microsoft/LightGBM --depth 1 \
&& cd LightGBM && mkdir build && cd build \
&& cmake -DUSE_GPU=1 -DOpenCL_LIBRARY=/usr/lib/x86_64-linux-gnu/libOpenCL.so -DOpenCL_INCLUDE_DIR=/usr/local/cuda/include/ .. \
&& make -j$(nproc) && sudo make install && cd ../python-package \
&& python setup.py install --precompile \
&& cd ../

ENTRYPOINT ["/bin/bash"]

RUN pip install -Uqq fastbook && \
pip install git+https://github.com/KinWaiCheuk/nnAudio.git#subdirectory=Installation

COPY run_jupyterlab.sh /app/
COPY run_rest.sh /app/
