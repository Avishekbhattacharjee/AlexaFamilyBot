FROM alpine:edge

RUN sed -e 's;^#http\(.*\)/edge/community;http\1/edge/community;g' -i /etc/apk/repositories
RUN echo 'http://dl-cdn.alpinelinux.org/alpine/edge/testing' >> /etc/apk/repositories
ENV CPUCOUNT 1
RUN CPUCOUNT=$(cat /proc/cpuinfo | grep '^processor.*:' | wc -l)

ENV OPENCV_VERSION 3.1.0

ADD aiwplain1.jpg /opt/aiwplain1.jpg
ADD ocr1.py /opt/ocr1.py

# update the repositories mirrors to workaround unsatisfiable constraints issue
RUN echo "http://dl-1.alpinelinux.org/alpine/v3.3/main" >> /etc/apk/repositories && \
	echo "http://dl-2.alpinelinux.org/alpine/v3.3/main" >> /etc/apk/repositories && \
	echo "http://dl-3.alpinelinux.org/alpine/v3.3/main" >> /etc/apk/repositories && \
	echo "http://dl-4.alpinelinux.org/alpine/v3.3/main" >> /etc/apk/repositories && \
	echo "http://dl-5.alpinelinux.org/alpine/v3.3/main" >> /etc/apk/repositories && \
	echo "http://dl-1.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories && \
	echo "http://dl-2.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories && \
	echo "http://dl-3.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories && \
	echo "http://dl-4.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories

RUN apk update && \
	apk upgrade && \
	apk add \
		build-base \
		clang \
		cmake \
		git \
		libssl1.0 \
		linux-headers \
		openssl \
		py-pip \
		py-numpy \
		py-numpy-dev \
		py-scipy \
		py-scipy-dev \
		python3 \
		python3-dev \
		wget \
		libjpeg-turbo-dev tiff-dev libjasper jasper-dev libpng-dev \
		# instead of libavcodec we'll cobble together the contents as best we can...
		ffmpeg-libs ffmpeg-dev ffmpeg \
		gtk+2.0-dev \
		openblas-dev openblas gfortran \
		tesseract-ocr tesseract-ocr-dev leptonica leptonica-dev

# using CLang for build 
# https://github.com/Itseez/opencv/issues/5004
ENV CC /usr/bin/clang
ENV CXX /usr/bin/clang++


RUN cd /opt/ && \
	git clone -b ${OPENCV_VERSION} --depth 1 https://github.com/Itseez/opencv.git && \
	git clone -b ${OPENCV_VERSION} --depth 1 https://github.com/Itseez/opencv_contrib.git

RUN mkdir -p /opt/opencv/build && \
	cd /opt/opencv/build && \
	cmake -D CMAKE_BUILD_TYPE=RELEASE \
		-D CMAKE_INSTALL_PREFIX=/usr/local \
		# -D INSTALL_C_EXAMPLES=ON \
		# -D INSTALL_PYTHON_EXAMPLES=ON \
		-D OPENCV_EXTRA_MODULES_PATH=/opt/opencv_contrib/modules \
		# -D BUILD_EXAMPLES=ON \
		.. && \
	make -j${CPUCOUNT} && \
	make install

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
