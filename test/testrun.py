import requests
import json
import base64
import time
from pathlib import Path

# Your RunPod API key and endpoint ID
API_KEY = "IUOCCCBSF439C7Z6WTK58MZ7FZZCA9K82C92L5L7"
ENDPOINT_ID = "ik6194588rn8pj"

# Base URL for the API
BASE_URL = f"https://api.runpod.ai/v2/{ENDPOINT_ID}"

# Headers for the API requests
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}'
}

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
IMAGE_PATH = Path(r"67027377d927d521fa6e080e_photo_rotated.webp")

# Encode the image
base64_image = encode_image(IMAGE_PATH)

# Prepare the input for the job
input_data = {
        "input": {
            "workflow": {
  "3": {
    "inputs": {
      "seed": 601860059563177,
      "steps": 6,
      "cfg": 2,
      "sampler_name": "dpmpp_sde",
      "scheduler": "karras",
      "denoise": 1,
      "model": [
        "11",
        0
      ],
      "positive": [
        "11",
        1
      ],
      "negative": [
        "11",
        2
      ],
      "latent_image": [
        "5",
        0
      ]
    },
    "class_type": "KSampler",
    "_meta": {
      "title": "KSampler"
    }
  },
  "4": {
    "inputs": {
      "ckpt_name": "juggernautXL_v9Rdphoto2Lightning.safetensors"
    },
    "class_type": "CheckpointLoaderSimple",
    "_meta": {
      "title": "Load Checkpoint"
    }
  },
  "5": {
    "inputs": {
      "width": 1016,
      "height": 1016,
      "batch_size": 1
    },
    "class_type": "EmptyLatentImage",
    "_meta": {
      "title": "Empty Latent Image"
    }
  },
  "6": {
    "inputs": {
      "text": "Portrait of male looking at camera with a gentle smile and warm expression. Wearing white tshirt. White Background. Mouth closed, natural pose. ral-illustration",
      "clip": [
        "16",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "7": {
    "inputs": {
      "text": "nude, nudity, naked, duplicate character, duplicate, 2 heads, 2 faces, 3 feet, 4 feet, cropped image, out of frame, deformed hands, twisted fingers, cross eyes, weird eyes, dead eyes, double image, malformed hands, multiple heads, extra limb, ugly, poorly drawn hands, missing limb, disfigured, cut off, ugly, grain, low res, deformed, blurry, bad anatomy, disfigured, poorly drawn face, mutation, mutated, floating limbs, disconnected limbs, disgusting, poorly drawn, mutilated, mangled, extra fingers, duplicate artifacts, missing arms, mutated hands, mutilated hands, cloned face, malformed, text, fonts, letters, symbols, logo, wordmark, writing, heading, signature, watermark, stamp",
      "clip": [
        "16",
        1
      ]
    },
    "class_type": "CLIPTextEncode",
    "_meta": {
      "title": "CLIP Text Encode (Prompt)"
    }
  },
  "8": {
    "inputs": {
      "samples": [
        "3",
        0
      ],
      "vae": [
        "4",
        2
      ]
    },
    "class_type": "VAEDecode",
    "_meta": {
      "title": "VAE Decode"
    }
  },
  "11": {
    "inputs": {
      "weight": 1,
      "start_at": 0,
      "end_at": 1,
      "instantid": [
        "12",
        0
      ],
      "insightface": [
        "13",
        0
      ],
      "control_net": [
        "14",
        0
      ],
      "image": [
        "15",
        0
      ],
      "model": [
        "16",
        0
      ],
      "positive": [
        "6",
        0
      ],
      "negative": [
        "7",
        0
      ],
      "image_kps": [
        "15",
        0
      ]
    },
    "class_type": "ApplyInstantID",
    "_meta": {
      "title": "Apply InstantID"
    }
  },
  "12": {
    "inputs": {
      "instantid_file": "SDXL/ip-adapter.bin"
    },
    "class_type": "InstantIDModelLoader",
    "_meta": {
      "title": "Load InstantID Model"
    }
  },
  "13": {
    "inputs": {
      "provider": "CPU"
    },
    "class_type": "InstantIDFaceAnalysis",
    "_meta": {
      "title": "InstantID Face Analysis"
    }
  },
  "14": {
    "inputs": {
      "control_net_name": "instantid/diffusion_pytorch_model.safetensors"
    },
    "class_type": "ControlNetLoader",
    "_meta": {
      "title": "Load ControlNet Model"
    }
  },
  "15": {
    "inputs": {
      "image": "67027377d927d521fa6e080e_photo_rotated.webp",
      "upload": "image"
    },
    "class_type": "LoadImage",
    "_meta": {
      "title": "Load Image"
    }
  },
  "16": {
    "inputs": {
      "lora_name": "character.safetensors",
      "strength_model": 1.3,
      "strength_clip": 1,
      "model": [
        "4",
        0
      ],
      "clip": [
        "4",
        1
      ]
    },
    "class_type": "LoraLoader",
    "_meta": {
      "title": "Load LoRA"
    }
  },
  "17": {
    "inputs": {
      "filename_prefix": "ComfyUI",
      "images": [
        "8",
        0
      ]
    },
    "class_type": "SaveImage",
    "_meta": {
      "title": "Save Image"
    }
  }
},
            "images": [
                {
                    "name": "67027377d927d521fa6e080e_photo_rotated.webp",
                    "image": base64_image  # The base64 encoded image will be inserted here dynamically
                }
            ]
        }
    }

# Start the job
response = requests.post(f"{BASE_URL}/runsync", headers=headers, json=input_data)
if response.status_code == 200:
    job_id = response.json()['id']
    print(f"Job started with ID: {job_id}")
else:
    print(f"Failed to start job. Status code: {response.status_code}")
    print(f"Response: {response.text}")
    exit(1)

# Check job status
while True:
    status_response = requests.get(f"{BASE_URL}/status/{job_id}", headers=headers)
    if status_response.status_code == 200:
        status_data = status_response.json()
        if status_data['status'] == 'COMPLETED':
            print("Job completed!")
            break
        elif status_data['status'] in ['FAILED', 'CANCELLED']:
            print(f"Job failed or was cancelled. Status: {status_data['status']}")
            exit(1)
        else:
            print(f"Job status: {status_data['status']}. Waiting...")
            time.sleep(10)  # Wait for 10 seconds before checking again
    else:
        print(f"Failed to get job status. Status code: {status_response.status_code}")
        print(f"Response: {status_response.text}")
        exit(1)

# Get the results
output_response = requests.get(f"{BASE_URL}/status/{job_id}", headers=headers)
if output_response.status_code == 200:
    output_data = output_response.json()       

    if 'output' in output_data and output_data['output']:
        output_image_base64 = output_data['output']['message']
        
        # Decode and save the image
        output_image_data = base64.b64decode(output_image_base64)
        output_path = Path(r"output_image.jpg")
        with open(output_path, 'wb') as f:
            f.write(output_image_data)
        print(f"Image saved successfully to {output_path}")
    else:
        print("No output data found in the response")
else:
    print(f"Failed to get job output. Status code: {output_response.status_code}")
    # print(f"Response: {output_response.text}")