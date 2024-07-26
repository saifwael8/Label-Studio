import os
from PIL import Image

def resize_images(input_folder, output_folder, size=(640, 640)):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img_path = os.path.join(input_folder, filename)
            with Image.open(img_path) as img:
                # Resize the image
                img_resized = img.resize(size, Image.LANCZOS)
                # Convert image mode to RGB if necessary
                if img_resized.mode in ("RGBA", "P"):
                    img_resized = img_resized.convert("RGB")
                # Save the resized image to the output folder
                output_path = os.path.join(output_folder, filename)
                img_resized.save(output_path)
                print(f"Resized and saved {filename} to {output_folder}")

# Example usage
input_folder = r'C:\Users\sdarwish\potholes_and_snow'  # Replace with the path to your images folder
output_folder = os.path.join(input_folder, 'resized_images')
resize_images(input_folder, output_folder)







