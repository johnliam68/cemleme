#!/bin/bash

# Use libtcmalloc for better memory management
TCMALLOC="$(ldconfig -p | grep -Po "libtcmalloc.so.\d" | head -n 1)"
export LD_PRELOAD="${TCMALLOC}"

# echo ">> Download model >>"
# wget -O /comfyui/models/checkpoints/realvisxlV40_v40LightningBakedvae.safetensors https://huggingface.co/alexgenovese/reica_models/resolve/021e192bd744c48a85f8ae1832662e77beb9aac7/realvisxlV40_v40LightningBakedvae.safetensors
# mkdir -p /comfyui/models/insightface/models/
# wget -O /comfyui/models/insightface/inswapper_128.onnx https://huggingface.co/ezioruan/inswapper_128.onnx/resolve/main/inswapper_128.onnx
# wget -O /comfyui/models/insightface/models/antelopev2.zip https://github.com/deepinsight/insightface/releases/download/v0.7/antelopev2.zip && unzip /comfyui//models/insightface/models/antelopev2.zip
# wget -O /comfyui/models/upscale_models/RealESRGAN_x2.pth https://huggingface.co/ai-forever/Real-ESRGAN/resolve/a86fc6182b4650b4459cb1ddcb0a0d1ec86bf3b0/RealESRGAN_x2.pth
# mkdir -p /comfyui/models/instantid/SDXL/
# wget -O /comfyui/models/instantid/SDXL/ip-adapter.bin https://huggingface.co/InstantX/InstantID/resolve/main/ip-adapter.bin
# mkdir -p /comfyui/models/controlnet/instantid 
# wget -O /comfyui/models/controlnet/instantid/diffusion_pytorch_model.safetensors https://huggingface.co/InstantX/InstantID/resolve/main/ControlNetModel/diffusion_pytorch_model.safetensors


echo ">> Starting Jupyter Lab... >>"
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password='' --NotebookApp.notebook_dir='/' --NotebookApp.disable_check_xsrf=True --NotebookApp.allow_origin='*' &


# Serve the API and don't shutdown the container
if [ "$SERVE_API_LOCALLY" == "true" ]; then
    echo "runpod-worker-comfy: Starting ComfyUI"
    python3 /comfyui/main.py --disable-auto-launch --disable-metadata --listen &

    echo "runpod-worker-comfy: Starting RunPod Handler"
    python3 -u /rp_handler.py --rp_serve_api --rp_api_host=0.0.0.0
else
    echo "runpod-worker-comfy: Starting ComfyUI"
    python3 /comfyui/main.py --disable-auto-launch --disable-metadata &

    echo "runpod-worker-comfy: Starting RunPod Handler"
    python3 -u /rp_handler.py
fi