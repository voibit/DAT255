FROM tensorflow/tensorflow:latest-gpu


RUN apt-get update && apt-get upgrade -y \
&& apt-get install -y --no-install-recommends graphviz libsndfile-dev git \
&& rm -rf /var/lib/apt/lists/*


RUN pip3 install --upgrade pip
RUN pip3 --no-cache-dir install jupyterlab jupyterlab_widgets \
    graphviz \
    matplotlib \
    pandas \
    tensorboard \
    opendatasets \
    xlrd \
    openpyxl \
    seaborn \
    tensorflow-datasets \
    tfx \
    tensorflow_io \
    kapre

COPY run_jupyterlab.sh /tf/

ENTRYPOINT ["/bin/bash"]
WORKDIR /tf
