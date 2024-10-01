from PIL import Image, ImageOps
import argparse
import os

def resize_image_letterbox(input_image_path, output_image_path, new_width, new_height, fill_color=(0, 0, 0)):
    """
    Resize an image using letterboxing (add borders to avoid stretching).

    :param input_image_path: str, path to the input image file
    :param output_image_path: str, path to save the resized image
    :param new_width: int, desired width of the resized image
    :param new_height: int, desired height of the resized image
    :param fill_color: tuple, color for the letterbox borders (default: black)
    """
    # Open the image
    with Image.open(input_image_path) as img:
        # Resize while maintaining aspect ratio, then pad to the final size
        img = ImageOps.fit(img, (new_width, new_height), method=Image.LANCZOS, bleed=0.0, centering=(0.5, 0.5))
        img_with_border = ImageOps.pad(img, (new_width, new_height), method=Image.LANCZOS, color=fill_color)

        # Save the resized image
        img_with_border.save(output_image_path, quality=95)
        print(f"Letterboxed image saved to {output_image_path}")

def resize_image_crop(input_image_path, output_image_path, new_width, new_height):
    """
    Resize an image by cropping it to fit the new dimensions without stretching.

    :param input_image_path: str, path to the input image file
    :param output_image_path: str, path to save the resized image
    :param new_width: int, desired width of the resized image
    :param new_height: int, desired height of the resized image
    """
    # Open the image
    with Image.open(input_image_path) as img:
        # Resize and crop to fill the exact dimensions
        img_cropped = ImageOps.fit(img, (new_width, new_height), method=Image.LANCZOS)

        # Save the cropped image
        img_cropped.save(output_image_path, quality=95)
        print(f"Cropped image saved to {output_image_path}")

def divide_image(input_image_path, output_directory, direction="vertical"):
    """
    Divide an image into two halves either vertically or horizontally.

    :param input_image_path: str, path to the input image file
    :param output_directory: str, directory to save the two halves
    :param direction: str, how to divide the image ("vertical" or "horizontal")
    """
    # Load the image using Pillow
    with Image.open(input_image_path) as img:
        width, height = img.size

        if direction == "vertical":
            # Divide the image into left and right halves
            left_half = img.crop((0, 0, width // 2, height))
            right_half = img.crop((width // 2, 0, width, height))

            # Save both halves
            left_half.save(os.path.join(output_directory, "left_half.jpg"))
            right_half.save(os.path.join(output_directory, "right_half.jpg"))

            print(f"Image divided vertically into left_half.jpg and right_half.jpg in {output_directory}")

        elif direction == "horizontal":
            # Divide the image into top and bottom halves
            top_half = img.crop((0, 0, width, height // 2))
            bottom_half = img.crop((0, height // 2, width, height))

            # Save both halves
            top_half.save(os.path.join(output_directory, "top_half.jpg"))
            bottom_half.save(os.path.join(output_directory, "bottom_half.jpg"))

            print(f"Image divided horizontally into top_half.jpg and bottom_half.jpg in {output_directory}")
        else:
            raise ValueError("Invalid direction. Choose 'vertical' or 'horizontal'.")

def parse_arguments():
    """
    Parse command line arguments for the image resizing and dividing program.
    """
    parser = argparse.ArgumentParser(description="Resize, divide, or manipulate an image without stretching it.")

    # Input image file path
    parser.add_argument("input_image", type=str, help="Path to the input image file")

    # Output image file path or directory
    parser.add_argument("output_path", type=str, help="Path to save the resized image or directory to save divided images")

    # Desired width and height for resizing (optional)
    parser.add_argument("--width", type=int, help="Desired width of the resized image")
    parser.add_argument("--height", type=int, help="Desired height of the resized image")

    # Choose between letterboxing or cropping
    parser.add_argument("--method", type=str, choices=["letterbox", "crop"], help="Method to use for resizing (letterbox or crop)")

    # Optional fill color for letterboxing
    parser.add_argument("--fill_color", type=str, help="Fill color for letterbox borders (default: black). Format: '#RRGGBB'")

    # Option to divide the image
    parser.add_argument("--divide", action="store_true", help="Divide the image into two halves")
    parser.add_argument("--direction", type=str, choices=["vertical", "horizontal"], default="vertical", help="Direction to divide the image (vertical or horizontal)")

    return parser.parse_args()

if __name__ == "__main__":
    # Parse the arguments from the command line
    args = parse_arguments()

    # Convert fill color string (if provided) to an RGB tuple
    if args.fill_color:
        fill_color = tuple(int(args.fill_color[i:i+2], 16) for i in (1, 3, 5))  # Convert from hex string to RGB tuple
    else:
        fill_color = (0, 0, 0)  # Default black fill

    # Call the appropriate function based on the user's choice
    if args.divide:
        # Divide the image into halves
        divide_image(args.input_image, args.output_path, args.direction)
    else:
        # Resize the image if width and height are provided
        if args.width and args.height:
            if args.method == "letterbox":
                resize_image_letterbox(args.input_image, args.output_path, args.width, args.height, fill_color)
            elif args.method == "crop":
                resize_image_crop(args.input_image, args.output_path, args.width, args.height)
        else:
            raise ValueError("Width and height must be provided for resizing.")
