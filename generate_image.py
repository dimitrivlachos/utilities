import sys
import os
import re
from PIL import Image

def generate_image_from_coordinates(file_path, width, height):
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        return

    # Create a new black image with the given dimensions
    image = Image.new('L', (width, height), 0)  # 'L' mode means grayscale, 0 = black

    # Load the pixel data
    pixels = image.load()

    # Define a regex pattern to match x and y coordinates separated by comma, space, or both
    pattern = re.compile(r"(\d+)\s*,?\s*(\d+)")

    # Read the coordinates from the file
    with open(file_path, 'r') as file:
        for line in file:
            match = pattern.match(line.strip())
            if match:
                try:
                    # Extract x and y from the regex groups and convert to integers
                    x, y = int(match.group(1)), int(match.group(2))
                    
                    # Check if coordinates are within image bounds
                    if 0 <= x < width and 0 <= y < height:
                        pixels[x, y] = 255  # Set the pixel to white (255)
                    else:
                        print(f"Warning: Coordinates ({x}, {y}) are out of bounds for the image size ({width}, {height}).")
                except ValueError:
                    print(f"Warning: Invalid coordinates in line: {line.strip()}")
            else:
                print(f"Warning: Could not parse line: {line.strip()}")
    
    # Save the image as PNG
    output_path = os.path.splitext(file_path)[0] + "_output.png"
    image.save(output_path)
    print(f"Image saved as {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <path_to_txt_file> <width> <height>")
    else:
        txt_file_path = sys.argv[1]
        img_width = int(sys.argv[2])
        img_height = int(sys.argv[3])

        generate_image_from_coordinates(txt_file_path, img_width, img_height)
