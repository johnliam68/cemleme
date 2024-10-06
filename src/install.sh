#!/bin/bash

import requests
import subprocess
# Cài đặt custom nodes
%cd /content/ComfyUI/custom_nodes

# Lấy nội dung của file từ GitHub
url = "https://raw.githubusercontent.com/tuyenhm68/sd-resources/refs/heads/main/lib/changebg-tln/custom-nodes.txt"
response = requests.get(url)
commands = response.text.split('\n')

# Thực thi từng lệnh
for command in commands:
    if command.strip():  # Bỏ qua các dòng trống
        # Loại bỏ ký tự '!' ở đầu lệnh nếu có
        command = command.lstrip('!')
        try:
            # Sử dụng subprocess để chạy lệnh
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            print(f"Command executed successfully: {command}")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {command}")
            print(f"Error message: {e.stderr}")