from PIL import Image


def resize_image(
        image_path: str,
        min_size: int = 448
) -> Image.Image:
    """
    Resize an image while preserving aspect ratio so that its smallest side 
    equals a minimum size.

    Args:
        image_path (str): The file path to the image to resize.
        min_size (int, optional): The desired minimum size (in pixels) for the 
            shorter side of the image. Defaults to 448.

    Returns:
        Image: A resized PIL Image object with preserved aspect ratio.
    """
    image = Image.open(image_path).convert("RGB")
    width, height = image.size
    if width < height:
        new_width = min_size
        new_height = int(height * (min_size / width))
    else:
        new_height = min_size
        new_width = int(width * (min_size / height))
    return image.resize((new_width, new_height), Image.LANCZOS)
