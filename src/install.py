# import requests
# import subprocess
# import os
# import string

# os.chdir('/comfyui')

# url = "https://raw.githubusercontent.com/johnliam68/cemleme/refs/heads/main/src/custom-nodes.txt"
# response = requests.get(url)
# commands = response.text.split('\n')
# command = string.replace("pip install -r ", "pip install -r custom_nodes/")
# for command in commands:
#     if command.strip():        
#         command = command.lstrip('!')
#         try:            
#             result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
#             print(f"Command executed successfully: {command}")
#             print(result.stdout)
#         except subprocess.CalledProcessError as e:
#             print(f"Error executing command: {command}")
#             print(f"Error message: {e.stderr}")


import requests
import subprocess
import os

def get_commands():
    git_custom_nodes = os.getenv('GIT_CUSTOM_NODES')
    
    if git_custom_nodes:
        # Sử dụng URL từ biến môi trường
        url = git_custom_nodes
        try:
            response = requests.get(url)
            return response.text.split('\n')
        except requests.RequestException as e:
            print(f"Error fetching from URL: {e}")
            return []
    else:
        # Đọc từ file local
        try:
            with open('custom-nodes.txt', 'r') as file:
                return file.read().splitlines()
        except FileNotFoundError:
            print("custom-nodes.txt not found")
            return []

def main():
    os.chdir('/comfyui')
    
    commands = get_commands()
    
    for command in commands:
        if command.strip():
            # Loại bỏ '!' ở đầu nếu có
            command = command.lstrip('!')
            
            # Thay thế 'pip install -r ' thành 'pip install -r custom_nodes/'
            if 'pip install -r ' in command:
                command = command.replace('pip install -r ', 'pip install -r custom_nodes/')
            
            try:
                print(f"Executing command: {command}")
                result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
                print(f"Command executed successfully")
                print(result.stdout)
            except subprocess.CalledProcessError as e:
                print(f"Error executing command")
                print(f"Error message: {e.stderr}")

if __name__ == "__main__":
    main()