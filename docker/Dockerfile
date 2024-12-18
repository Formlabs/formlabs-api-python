FROM scottyhardy/docker-wine:latest

ARG WINDOWS_PREFORM_SERVER_URL=https://downloads.formlabs.com/PreFormServer/Release/3.43.1/PreForm_Server_win_3.43.1_release_releaser_462_70877.zip
ARG FORMLABS_LOCAL_API_PATH=local-api/minimal-lib/

ENV DISPLAY=:99
ENV USE_XVFB=yes
ENV XVFB_SERVER=:99
ENV XVFB_SCREEN=0
ENV XVFB_RESOLUTION=1920x1080x24

RUN export DEBIAN_FRONTEND=noninteractive && \
  apt-get -y update && \
  apt-get -y --no-install-recommends install ca-certificates libfreetype6-dev libjpeg-dev libpng-dev \
  libpq-dev libcurl4-openssl-dev libssl-dev fontconfig software-properties-common curl wget && \
  add-apt-repository ppa:deadsnakes/ppa && \
  apt-get -y --no-install-recommends install python3.10 python3.10-dev python3.10-distutils && \
  rm -rf /var/lib/apt/lists/*

RUN wget https://bootstrap.pypa.io/get-pip.py \
  && python3.10 get-pip.py \
  && rm get-pip.py

RUN mkdir -p /workspace
WORKDIR /workspace

RUN wget $WINDOWS_PREFORM_SERVER_URL -O /tmp/file.zip && \
  unzip /tmp/file.zip && \
  rm -rf /tmp/file.zip

RUN mkdir -p /workspace/local-api/minimal-lib
COPY $FORMLABS_LOCAL_API_PATH /workspace/local-api/minimal-lib

RUN /usr/bin/python3.10 -m pip install -e /workspace/local-api/minimal-lib
ENV PYTHONUNBUFFERED=TRUE

# Copy in an example Python application from within the formlabs-api-python repo
COPY docker/example-app.py /workspace/

CMD ["/usr/bin/python3.10", "/workspace/example-app.py"]
