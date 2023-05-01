import os
from concurrent.futures import ThreadPoolExecutor

import pytesseract
from PIL import Image
from rich import print
from rich.progress import track

"""
This script scans all the images in the leaderboard_images folder and validates them using tesseract ocr.
This script will lock your CPU to 100% and can cause crashed/unresponsive behavior. 
Use with caution, and set max_workers to a reasonable number for your system. 
"""


def scale(img: Image, factor: int) -> Image:
    """Scales an image by a given factor

    Args:
        img (Image): pil image
        factor (int): multiplier

    Returns:
        Image: pil image
    """
    width, height = img.size
    return img.resize((width * factor, height * factor))


def parse_file_name(file_name: str) -> tuple:
    """converts file name to tuple

    Args:
        file_name (str): filename

    Returns:
        tuple: role region and page
    """
    role, region, page = file_name.replace(".png", "").split("-")
    return (role, region, page)


def process_file(file):
    """Worker to process a file

    Args:
        file (_type_): path to file
    """
    role, region, page = parse_file_name(file)  # unpack data

    # open the image with pillow
    img = Image.open(os.path.join("assets\leaderboard_images", file))
    # crop the image to the selection and page
    # convert to grayscale
    # scale by scale_factor
    # predict string
    role_and_region_predictions = pytesseract.image_to_string(
        scale(img.crop(selection_bounding_box).convert("L"), scale_factor)
    )
    # uses config to filter out non valid characters
    page_predictions = pytesseract.image_to_string(
        scale(img.crop(page_bounding_box).convert("L"), scale_factor), config=config
    ).replace(
        "/50", ""
    )  # replace /50 so page 50 does not match with this.

    # prompts
    if role not in role_and_region_predictions:
        print(f"[red]ERROR: {file} is not valid for role")
        return file  # return to main thread if failed; this will be printed in an array

    if region not in role_and_region_predictions:
        print(f"[red]ERROR: {file} is not valid for region")
        return file  # return to main thread if failed; this will be printed in an array

    if page not in page_predictions:
        print(f"[red]ERROR: {file} is not valid for page")
        return file  # return to main thread if failed; this will be printed in an array

    print(f"[green]SUCCESS: {file}")


def main():
    pytesseract.pytesseract.tesseract_cmd = (
        r"bin\tesseractocr\tesseract.exe"  # set tesseract path
    )

    # sorry for the global variables
    global selection_bounding_box, page_bounding_box, config, scale_factor
    selection_bounding_box = (453, 255, 1472, 295)
    page_bounding_box = (766, 857, 1158, 900)
    config = r"-c tessedit_char_whitelist=0123456789/"
    scale_factor = 15

    files = os.listdir("assets\leaderboard_images")  # get all files

    check = []  # array to hold failed files
    with ThreadPoolExecutor(max_workers=4) as executor:  # adjust max workers as needed
        # use tpe to process files in parallel
        futures = [executor.submit(process_file, file) for file in files]
        for future in track(futures, description="scanning files"):
            result = future.result()
            if result:
                check.append(result)  # store failed results

    print(check)  # print failed results


if __name__ == "__main__":
    main()
