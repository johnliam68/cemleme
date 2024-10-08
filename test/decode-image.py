import json
import base64


def decode_and_save_image(json_file_path, output_image_path):
    try:
        # Reading the JSON file
        with open(json_file_path, "r") as file:
            data = json.load(file)

        # Extracting the base64 encoded image data
        base64_image = data["output"][0]["image"]

        # Decode the Base64 string
        decoded_image_data = base64.b64decode(base64_image)

        # Writing the decoded data to an image file
        with open(output_image_path, "wb") as image_file:
            image_file.write(decoded_image_data)

        print(f"Image successfully decoded and saved as '{output_image_path}'.")

    except FileNotFoundError:
        print(
            "File not found. Please ensure the JSON file exists in the specified path."
        )
    except KeyError as e:
        print(f"Error in JSON structure: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Usage
json_file_path = "output.json"  # Path to your JSON file
output_image_path = "decoded_image.png"  # Desired path for the output image

decode_and_save_image(json_file_path, output_image_path)