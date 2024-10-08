# Stage 1: Base image with common dependencies
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04 as base
# FROM runpod/pytorch:2.2.0-py3.10-cuda12.1.1-devel-ubuntu22.04 as base

# Prevents prompts from packages asking for user input during installation
ENV DEBIAN_FRONTEND=noninteractive
# Prefer binary wheels over source distributions for faster pip installations
ENV PIP_PREFER_BINARY=1
# Ensures output from python is printed immediately to the terminal without buffering
ENV PYTHONUNBUFFERED=1 
# ENV GIT_CUSTOM_NODES="https://raw.githubusercontent.com/johnliam68/cemleme/refs/heads/main/src/custom-nodes.txt"
ENV GIT_CUSTOM_NODES=""
ENV GIT_MODELS=""

RUN apt-get update && apt-get install -y git && apt-get clean && apt-get install git-lfs && git lfs install

# Install Python, git and other necessary tools
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    wget \
    unzip

# Install runpod
RUN pip3 install runpod requests

# Clean up to reduce image size
RUN apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

ENV ROOT=/comfyui

RUN --mount=type=cache,target=/root/.cache/pip \
  git clone https://github.com/comfyanonymous/ComfyUI.git ${ROOT} && \
  cd ${ROOT} && \
  # git checkout master && \
  # git reset --hard 276f8fce9f5a80b500947fb5745a4dde9e84622d && \
  pip install -r requirements.txt

# Support for the network volume
ADD src/extra_model_paths.yaml ${ROOT}/
ADD data/models/. ${ROOT}/models

# Go back to the root
WORKDIR /

# Add the start and the handler
ADD src/start.sh src/rp_handler.py src/install.py ./
ADD lib/custom-nodes.txt lib/models.txt ${ROOT}/lib/
RUN chmod +x /start.sh

# RUN cd /content/comfyui/custom_nodes
RUN python3 /install.py 

# Stage 2: Download models
FROM base as downloader

ARG HUGGINGFACE_ACCESS_TOKEN
ARG MODEL_TYPE

# Change working directory to ComfyUI
WORKDIR /comfyui

# Stage 3: Final image
FROM base as final

# Copy models from stage 2 to the final image
COPY --from=downloader /comfyui/models /comfyui/models

# Start the container
CMD ["/start.sh"]