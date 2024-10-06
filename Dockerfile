# Stage 1: Base image with common dependencies
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04 as base
# FROM runpod/pytorch:2.2.0-py3.10-cuda12.1.1-devel-ubuntu22.04 as base

# Prevents prompts from packages asking for user input during installation
ENV DEBIAN_FRONTEND=noninteractive
# Prefer binary wheels over source distributions for faster pip installations
ENV PIP_PREFER_BINARY=1
# Ensures output from python is printed immediately to the terminal without buffering
ENV PYTHONUNBUFFERED=1 

RUN apt-get update && apt-get install -y git && apt-get clean && apt-get install git-lfs && git lfs install

# Install Python, git and other necessary tools
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    wget \
    unzip

#Install for dlib
RUN pip install easydict matplotlib opencv-python scikit-image scipy && pip install cmake && pip install dlib==19.24.1

#Install jupyterlab
RUN pip install jupyterlab
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

RUN cd ${ROOT}/custom_nodes && git clone https://github.com/ltdrdata/ComfyUI-Manager
RUN pip install -r ${ROOT}/custom_nodes/ComfyUI-Manager/requirements.txt

RUN cd ${ROOT}/custom_nodes && \
git clone https://github.com/ltdrdata/ComfyUI-Impact-Pack && pip install -r ComfyUI-Impact-Pack/requirements.txt && python3 ComfyUI-Impact-Pack/install.py && \
git clone https://github.com/cdb-boop/ComfyUI-Bringing-Old-Photos-Back-to-Life && pip install -r ComfyUI-Bringing-Old-Photos-Back-to-Life/requirements.txt &&\
git clone https://github.com/Gourieff/comfyui-reactor-node && pip install -r comfyui-reactor-node/requirements.txt &&\
git clone https://github.com/cubiq/ComfyUI_InstantID && pip install -r ComfyUI_InstantID/requirements.txt &&\
git clone https://github.com/WASasquatch/was-node-suite-comfyui && pip install -r was-node-suite-comfyui/requirements.txt &&\
pip install ultralytics

#Download custom files
# RUN wget -O ${ROOT}/models/checkpoints/realvisxlV40_v40LightningBakedvae.safetensors https://huggingface.co/alexgenovese/reica_models/resolve/021e192bd744c48a85f8ae1832662e77beb9aac7/realvisxlV40_v40LightningBakedvae.safetensors
# RUN wget -O ${ROOT}/models/insightface/inswapper_128.onnx https://huggingface.co/ezioruan/inswapper_128.onnx/resolve/main/inswapper_128.onnx
# RUN wget -O ${ROOT}/models/upscale_models/RealESRGAN_x2.pth https://huggingface.co/ai-forever/Real-ESRGAN/resolve/a86fc6182b4650b4459cb1ddcb0a0d1ec86bf3b0/RealESRGAN_x2.pth
# RUN wget -O ${ROOT}/models/instantid/SDXL/ip-adapter.bin https://huggingface.co/InstantX/InstantID/resolve/main/ip-adapter.bin
# RUN wget -O ${ROOT}/models/controlnet/instantid/diffusion_pytorch_model.safetensors https://huggingface.co/InstantX/InstantID/resolve/main/ControlNetModel/diffusion_pytorch_model.safetensors
# RUN wget -O ${ROOT}/models/insightface/models/antelopev2.zip https://github.com/deepinsight/insightface/releases/download/v0.7/antelopev2.zip && unzip ${ROOT}/models/insightface/models/antelopev2.zip
# Support for the network volume
ADD src/extra_model_paths.yaml ./
ADD data/models/. ${ROOT}/models

# Go back to the root
WORKDIR /

# Add the start and the handler
ADD src/start.sh src/rp_handler.py ./
RUN chmod +x /start.sh

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