"""
 I'm so fucking tired of resizing wallpapers I find on the internet to my laptop rare screen resolution.
 So this program is intended to help me with it.
"""
from PIL import Image, ImageOps
import argparse


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


def parse_arguments():
    """
    Parse command line arguments for the image resizing program.
    """
    parser = argparse.ArgumentParser(
        description="Resize an image without stretching it (either with letterboxing or cropping).")

    # Input image file path
    parser.add_argument("input_image", type=str, help="Path to the input image file")

    # Output image file path
    parser.add_argument("output_image", type=str, help="Path to save the resized image")

    # Desired width and height
    parser.add_argument("width", type=int, help="Desired width of the resized image")
    parser.add_argument("height", type=int, help="Desired height of the resized image")

    # Choose between letterboxing or cropping
    parser.add_argument("--method", type=str, choices=["letterbox", "crop"], default="letterbox",
                        help="Method to use for resizing (default: letterbox)")

    # Optional fill color for letterboxing
    parser.add_argument("--fill_color", type=str,
                        help="Fill color for letterbox borders (default: black). Format: '#RRGGBB'")

    return parser.parse_args()


if __name__ == "__main__":
    # Parse the arguments from the command line
    args = parse_arguments()

    # Convert fill color string (if provided) to an RGB tuple
    if args.fill_color:
        fill_color = tuple(int(args.fill_color[i:i + 2], 16) for i in (1, 3, 5))  # Convert from hex string to RGB tuple
    else:
        fill_color = (0, 0, 0)  # Default black fill

    # Call the appropriate resize function
    if args.method == "letterbox":
        resize_image_letterbox(args.input_image, args.output_image, args.width, args.height, fill_color)
    else:
        resize_image_crop(args.input_image, args.output_image, args.width, args.height)
