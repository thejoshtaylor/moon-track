# Moon Tracker
# Joshua Taylor - 2024

from generate import generate_photo
from helper import resize

import cv2
import os
import argparse

# default values
directory = os.getcwd()
crop = "original"
every = 1

parser = argparse.ArgumentParser(
    description="Generate a combined photo from a directory of moon photos"
)
parser.add_argument("directory", nargs="?", help="The directory to use")
parser.add_argument("every", nargs="?", help="Use every nth photo", type=int)
parser.add_argument(
    "crop",
    nargs="?",
    help="How to crop the photos",
    choices=["original", "fit", "square"],
)
args = parser.parse_args()

if args.directory:
    # make sure it's a directory
    if os.path.isdir(args.directory):
        directory = args.directory
    # if it's not a directory, check if it's a file
    else:
        if os.path.isfile(args.directory):
            # if it's a file, get the directory
            directory = os.path.dirname(directory)
if args.every:
    every = args.every
if args.crop:
    crop = args.crop

img = None
changed = True

# # if arguments were provided, generate a photo
# if args.directory or args.every or args.crop:
#     img = generate_photo(directory, every, crop)

def title():
    print(r"""
    __  __                     _______             _             
   |  \/  |                   |__   __|           | |            
   | \  / | ___   ___  _ __      | |_ __ __ _  ___| | _____ _ __ 
   | |\/| |/ _ \ / _ \| '_ \     | | '__/ _` |/ __| |/ / _ \ '__|
   | |  | | (_) | (_) | | | |    | | | | (_| | (__|   <  __/ |   
   |_|  |_|\___/ \___/|_| |_|    |_|_|  \__,_|\___|_|\_\___|_|   
                                                                 
    """)
    print("Joshua Taylor - 2024")

def menu():
    global directory, every, crop, img, changed
    print()
    print("Directory: ", directory, " (", len([f for f in os.listdir(directory) if f.lower().endswith(".jpg")]), " images)", sep="")
    print()
    print("[e] Every:", every)
    print("[c] Crop:", crop)
    print("[g] Generate")
    if not changed:
        print("[p] Preview")
        print("[s] Save")
    print("[q] Quit")

    res = input("> ").lower()
    if len(res) == 0:
        # generate
        res = "g"
    
    if len(res) > 1:
        print("One letter only")
        return menu()
    
    if res in ["e", "c", "g", "q"] or ((res == "p" or res == "s") and not changed):
        return res
    else:
        print("Invalid option")
        return menu()

def main():
    global directory, every, crop, img, changed
    title()
    while True:
        res = menu()
        if res == "e":
            e = input("Every: ")
            try:
                e = int(e)
            except ValueError:
                print("Must be a number")
            if e > 0:
                every = e
                changed = True
            else:
                print("Must be greater than 0")
        elif res == "c":
            c = input("Crop [(o)riginal, (f)it, (s)quare]: ").lower()
            if c in ["original", "fit", "square"]:
                crop = c
                changed = True
            elif c == "o":
                crop = "original"
                changed = True
            elif c == "f":
                crop = "fit"
                changed = True
            elif c == "s":
                crop = "square"
                changed = True
            else:
                print("Invalid crop option")
        elif res == "g":
            img = generate_photo(directory, every, crop)
            if img is None:
                print("No photos found")
                continue

            changed = False
        elif res == "p":
            cv2.imshow("Moon Track", resize(img)[0])
            # Bring the window to the front
            cv2.setWindowProperty("Moon Track", cv2.WND_PROP_TOPMOST, 1)
            cv2.waitKey(1)
            input("Press [ENTER] to close")
            cv2.destroyAllWindows()
        elif res == "s":
            def make_name(index):
                filename = f"moon-track"
                if every != 1:
                    filename += f"-every-{every}"
                if crop != "original":
                    filename += f"-{crop}"
                if index > 0:
                    filename += f" ({index})"
                filename += ".jpg"
                return filename

            # check if moon-track directory
            if not os.path.isdir(os.path.join(directory, "moon-track")):
                os.mkdir(os.path.join(directory, "moon-track"))
            index = 0
            p = os.path.join(directory, "moon-track", make_name(index))
            while os.path.isfile(p):
                index += 1
                p = os.path.join(directory, "moon-track", make_name(index))
            cv2.imwrite(p, img)
            print("Saved to", p)
        elif res == "q":
            print()
            break

if __name__ == "__main__":
    main()