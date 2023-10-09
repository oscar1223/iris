###
# Instagram bot that downloads images from user's profiles
# ###

import glob
import os
import instaloader
from instaloader import Profile
from modules.imageProcessing import data_processing
from modules.var_c import TXT_INSTAGRAM_USERS, ROUTE_IMAGE_DIRECTORY, INSTA_USER, INSTA_PASSWD


# Method that returns the username from the txt file
def get_username_from_txt(txt):
    f = open(txt, 'r')
    while (True):
        linea = f.readline()
        print(linea)
        download_images(linea.replace("\n",""))
        if not linea:
            break
    f.close()

# Method that downloads the images
def download_images(nick):
    L = instaloader.Instaloader()
    L.dirname_pattern = ROUTE_IMAGE_DIRECTORY
    L.filename_pattern = "temp_Instagram_image"
    L.login(user=INSTA_USER, passwd=INSTA_PASSWD)

    PROFILE = nick
    profile = Profile.from_username(L.context, PROFILE)

    posts = sorted(profile.get_posts(), key=lambda post: post.likes, reverse=True)

    source = 'https://www.instagram.com/'+nick+'/'

    for post in posts:
        L.download_post(post, PROFILE)
    remove_image = glob.glob(ROUTE_IMAGE_DIRECTORY + '*.jpg')
    for i in remove_image:
        data_processing(source, i)
        os.remove(i)
    L.close()

if __name__ == "__main__":
    get_username_from_txt(TXT_INSTAGRAM_USERS)
