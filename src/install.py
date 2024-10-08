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
            with open('/comfyui/lib/custom-nodes.txt', 'r') as file:
                return file.read().splitlines()
        except FileNotFoundError:
            print("custom-nodes.txt not found")
            return []

def main():
    os.chdir('/comfyui/custom_nodes')    
    commands = get_commands()    
    for command in commands:
        if command.strip():
            command = command.lstrip('!')           
            print(f"Executing command: {command}")
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            print(f"Command executed successfully")
            print(result.stdout)
if __name__ == "__main__":
    main()