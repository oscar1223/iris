import glob

import praw
import requests
import cv2
import numpy as np
import os

from modules.imageProcessing import data_processing
from modules.var_c import REDDIT_CLIENT_ID, REDDIT_SECRET, REDDIT_USER_AGENT, ROUTE_IMAGE_DIRECTORY

POST_SEARCH_AMOUNT = 10

# Temp folder to save images.
def save_folder(image_path):
    CHECK_FOLDER = os.path.isdir(image_path)

    if not CHECK_FOLDER:
        os.makedirs(image_path)

def download_images():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    image_path = ROUTE_IMAGE_DIRECTORY
    ignore_path = os.path.join(dir_path, "ignore_images/")
    save_folder(image_path)

    reddit = praw.Reddit(
                client_id=REDDIT_CLIENT_ID,
                client_secret=REDDIT_SECRET,
                user_agent=REDDIT_USER_AGENT
                #username=creds['username'],
                #password=creds['password']
    )

    f_final = open('subreddits.csv', 'r')
    img_notfound = cv2.imread('imageNF.png')
    for line in f_final:
        sub = line.strip()
        subreddit = reddit.subreddit(sub)

        print(f"Starting {sub}")
        count = 0
        for submission in subreddit.new(limit=POST_SEARCH_AMOUNT):
            if "jpg" in submission.url.lower() or "png" in submission.url.lower():
                try:
                    resp = requests.get(submission.url.lower(), stream=True).raw
                    image = np.asarray(bytearray(resp.read()), dtype="uint8")
                    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

                    # Could do transforms on images like resize!
                    compare_image = cv2.resize(image, (224, 224))

                    # Get all images to ignore
                    for (dirpath, dirnames, filenames) in os.walk(ignore_path):
                        ignore_paths = [os.path.join(dirpath, file) for file in filenames]
                    ignore_flag = False

                    for ignore in ignore_paths:
                        ignore = cv2.imread(ignore)
                        difference = cv2.subtract(ignore, compare_image)
                        b, g, r = cv2.split(difference)
                        total_difference = cv2.countNonZero(b) + cv2.countNonZero(g) + cv2.countNonZero(r)
                        if total_difference == 0:
                            ignore_flag = True

                    if not ignore_flag:
                        cv2.imwrite(f"{image_path}{sub}-{submission.id}.png", image)
                        count += 1


                except Exception as e:
                    print(f"Image failed. {submission.url.lower()}")
                    print(e)
        remove_image = glob.glob(ROUTE_IMAGE_DIRECTORY + '*.png')
        for i in remove_image:
            data_processing(f"http://reddit.com/r/{sub}", i)
            os.remove(i)
        print(f"{sub} acabado")


def start_reddit_bot():
    download_images()

if __name__ == "__main__":
    start_reddit_bot()
