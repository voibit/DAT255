
# syntax = docker/dockerfile:experimental
#
# NOTE: To build this you will need a docker version > 18.06 with
#       experimental enabled and DOCKER_BUILDKIT=1
#
#       If you do not use buildkit you are not going to have a good time
#
#       For reference:
#           https://docs.docker.com/develop/develop-images/build_enhancements/
ARG BASE_IMAGE=ubuntu:22.04
ARG PYTHON_VERSION=3.9

FROM ${BASE_IMAGE} as dev-base
RUN --mount=type=cache,id=apt-dev,target=/var/cache/apt \
    apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        ccache \
        cmake \
        curl \
        git \
        libjpeg-dev \
        libpng-dev && \
    rm -rf /var/lib/apt/lists/*
RUN /usr/sbin/update-ccache-symlinks
RUN mkdir /opt/ccache && ccache --set-config=cache_dir=/opt/ccache
ENV PATH /opt/conda/bin:$PATH

FROM dev-base as conda
ARG PYTHON_VERSION=3.9
RUN curl -fsSL -v -o ~/miniconda.sh -O  https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh  && \
    chmod +x ~/miniconda.sh && \
    ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda install -y python=${PYTHON_VERSION} conda-build pyyaml numpy ipython && \
    /opt/conda/bin/conda clean -ya

FROM conda as conda-installs
ARG PYTHON_VERSION=3.9
ARG CUDA_VERSION=11.3
ARG CUDA_CHANNEL=nvidia
ARG INSTALL_CHANNEL=pytorch
ENV CONDA_OVERRIDE_CUDA=${CUDA_VERSION}
RUN /opt/conda/bin/conda install -c "${INSTALL_CHANNEL}" -c "${CUDA_CHANNEL}" -y python=${PYTHON_VERSION} pytorch torchvision torchaudio torchtext "cudatoolkit=${CUDA_VERSION}" 
RUN /opt/conda/bin/conda install -c conda-forge -y libsndfile jupyter_contrib_nbextensions jupyterlab

RUN /opt/conda/bin/conda clean -ya
RUN /opt/conda/bin/pip install torchelastic \
    albumentations \
    catalyst \
    captum \
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

# install tensorflow and xgboost
RUN /opt/conda/bin/pip install xgboost tensorflow-gpu #tfx 

FROM ${BASE_IMAGE} as official

ARG PYTORCH_VERSION
LABEL com.nvidia.volumes.needed="nvidia_driver"

RUN --mount=type=cache,id=apt-final,target=/var/cache/apt \
    apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        libjpeg-dev \
        libpng-dev \
        sudo \
        libnvidia-compute-510 nvidia-opencl-dev opencl-headers \
        #nvidia-cuda-toolkit \
        git cmake build-essential libboost-dev libboost-system-dev libboost-filesystem-dev && \
    rm -rf /var/lib/apt/lists/*

# Create a working directory
RUN mkdir /app
WORKDIR /app
# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos '' --shell /bin/bash user \
 && chown -R user:user /app
RUN echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-user
USER user
# All users can use /home/user as their home directory
ENV HOME=/home/user
RUN mkdir $HOME/.cache $HOME/.config && chmod -R 777 $HOME

COPY --from=conda-installs /opt/conda /opt/conda
ENV PATH /opt/conda/bin:$PATH
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64
ENV PYTORCH_VERSION ${PYTORCH_VERSION}

FROM official as dev

# Install fastai and fastcore
RUN git clone https://github.com/fastai/fastai.git --depth 1 \
    && git clone https://github.com/fastai/fastcore.git --depth 1 \
    && cd fastai && pip install . && cd ../fastcore && pip install . \
    && cd /app && rm -rf ./*

# Install nnAudio
RUN sudo /opt/conda/bin/pip install -Uqq fastbook git+https://github.com/KinWaiCheuk/nnAudio.git#subdirectory=Installation

# Install lightgbm
RUN git clone --recursive https://github.com/microsoft/LightGBM --depth 1 \
&& cd LightGBM && mkdir build && cd build \
&& cmake -DUSE_GPU=1 -DOpenCL_LIBRARY=/usr/lib/x86_64-linux-gnu/libOpenCL.so .. \
&& make -j$(nproc) && sudo make install \
&& cd /app/LightGBM/python-package && sudo /opt/conda/bin/python setup.py install --gpu \
&& cd /app && sudo rm -rf LightGBM

ENTRYPOINT ["/bin/bash"]
COPY run_jupyterlab.sh /app/
