FROM alpine:edge

RUN sed -e 's;^#http\(.*\)/edge/community;http\1/edge/community;g' -i /etc/apk/repositories
RUN echo 'http://dl-cdn.alpinelinux.org/alpine/edge/testing' >> /etc/apk/repositories

ENV OPENCV_VER 3.3.0
ENV OPENCV https://github.com/opencv/opencv/archive/${OPENCV_VER}.tar.gz

# build dependencies
RUN apk add -U --no-cache --virtual=build-dependencies \
    build-base \
    clang \
    clang-dev ninja \
    cmake \
    freetype-dev \
    g++ \
    jpeg-dev \
    lcms2-dev \
    libffi-dev \
    libgcc \
    libxml2-dev \
    libxslt-dev \
    linux-headers \
    make \
    musl \
    musl-dev \
    openjpeg-dev \
    openssl-dev \
    python3-dev \
    zlib-dev \
    && apk add --no-cache \
    curl \
    freetype \
    gcc \
    jpeg \
    libjpeg \
    openjpeg \
    python3 \
    tesseract-ocr \
    zlib

# build opencv from source
RUN mkdir /opt && cd /opt && \
    curl -L $OPENCV | tar zx && \
    cd opencv-$OPENCV_VER && \
    mkdir build && cd build && \
    cmake -G Ninja \
          -D CMAKE_BUILD_TYPE=RELEASE \
          -D CMAKE_INSTALL_PREFIX=/usr/local \
          -D WITH_FFMPEG=NO \
          -D WITH_IPP=NO \
          -D PYTHON_EXECUTABLE=/usr/bin/python3.8 \
          -D WITH_OPENEXR=NO .. && \
    ninja && ninja install && \
    cp -p $(find /usr/local/lib/python3.8/site-packages -name cv2.*) /usr/lib/python3.8/site-packages/cv2.so


RUN apk add --no-cache --update \
    coreutils \
    bash \
    nodejs \
    build-base \
    bzip2-dev \
    curl \
    figlet \
    gcc \
    g++ \
    git \
    aria2 \
    util-linux \
    libevent \
    jpeg-dev \
    libffi-dev \
    libpq \
    libwebp-dev \
    libxml2 \
    libxml2-dev \
    libxslt-dev \
    linux-headers \
    musl \
    openssl-dev \
    postgresql \
    postgresql-client \
    postgresql-dev \
    openssl \
    jq \
    wget \
    python3 \
    python3-dev \
    readline-dev \
    sqlite \
    ffmpeg \
    sqlite-dev \
    chromium \
    chromium-chromedriver \
    zlib-dev \
    jpeg \
    megatools \
    freetype-dev \
    redis \
    imagemagick

RUN python3 -m ensurepip \
    && pip3 install --upgrade pip setuptools \
    && rm -r /usr/lib/python*/ensurepip && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

RUN git clone https://6c90e9fc05bb18518038e167c3d362ed34f83a06@github.com/Ayush1311/newbot.git /root/haruka
RUN mkdir /root/haruka/bin/
WORKDIR /root/haruka

RUN pip3 install -r requirements.txt

CMD ["bash","init/start.sh"]
