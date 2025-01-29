FROM mcr.microsoft.com/devcontainers/base:jammy

# Rust Requirements
RUN apt-get update \
  && DEBIAN_FRONTEND="noninteractive" \
  apt-get install -y --no-install-recommends \
  g++ \
  make \
  file \
  curl \
  ca-certificates \
  python3 \
  git \
  cmake \
  sudo \
  gdb \
  libedit-dev \
  libssl-dev \
  pkg-config \
  zlib1g-dev \
  xz-utils \
  ninja-build \
  libz3-dev \
  less \
  nano \
  vim \
  llvm-13