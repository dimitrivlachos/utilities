import sys
import os
import re
from PIL import Image

def generate_grayscale_image(file_path, output_path, width, height):
    # Check if the input file exists
    if not os.path.isfile(file_path):
        print(f"File {file_path} does not exist.")
        return

    # Create a new black image with the given dimensions
    image = Image.new('L', (width, height), 0)  # 'L' mode means grayscale, 0 = black

    # Load the pixel data
    pixels = image.load()

    # Define a regex pattern to match x, y coordinates and a grayscale value separated by comma, space, or both
    pattern = re.compile(r"(\d+)\s*,?\s*(\d+)\s*,?\s*(\d+)")

    # Read the coordinates and grayscale values from the file
    with open(file_path, 'r') as file:
        for line in file:
            match = pattern.match(line.strip())
            if match:
                try:
                    # Extract x, y, and value from the regex groups and convert to integers
                    x, y, value = int(match.group(1)), int(match.group(2)), int(match.group(3))

                    # Check if coordinates are within image bounds
                    if 0 <= x < width and 0 <= y < height:
                        # Clamp the grayscale value between 0 and 255 to ensure it's a valid value
                        grayscale_value = max(0, min(255, value))
                        pixels[x, y] = grayscale_value  # Set the pixel to the specified grayscale value
                    else:
                        print(f"Warning: Coordinates ({x}, {y}) are out of bounds for the image size ({width}, {height}).")
                except ValueError:
                    print(f"Warning: Invalid data in line: {line.strip()}")
            else:
                print(f"Warning: Could not parse line: {line.strip()}")
    
    # Save the image as PNG
    image.save(output_path)
    print(f"Image saved as {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <path_to_txt_file> <output_path> <width> <height>")
    else:
        txt_file_path = sys.argv[1]
        output_file_path = sys.argv[2]
        img_width = int(sys.argv[3])
        img_height = int(sys.argv[4])

        generate_grayscale_image(txt_file_path, output_file_path, img_width, img_height)
