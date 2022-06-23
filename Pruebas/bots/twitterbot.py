import glob
import os

import tweepy

from modules.imageProcessing import data_processing
from modules.var_c import TWT_consumer_key, TWT_consumer_secret, TWT_access_token, TWT_access_token_secret, \
    ROUTE_IMAGE_DIRECTORY
import wget



def get_username_from_txt(txt):
    f = open(txt, 'r')
    usernames = []
    while (True):
        linea = f.readline()
        print(linea)
        usernames.append(linea)
        if not linea:
            break
    f.close()
    return usernames

def download_twt_images(usernames):
    # login en twitter
    auth = tweepy.OAuthHandler(TWT_consumer_key, TWT_consumer_secret)
    auth.set_access_token(TWT_access_token, TWT_access_token_secret)

    # Api
    api = tweepy.API(auth)

    for user in usernames:

        tweets = api.user_timeline(screen_name=user,
                                   count=200, include_rts=False,
                                   exclude_replies=True)
        last_id = tweets[-1].id
        while (True):
            more_tweets = api.user_timeline(screen_name=user,
                                            count=200,
                                            include_rts=False,
                                            exclude_replies=True,
                                            max_id=last_id - 1)
        # There are no more tweets
            if (len(more_tweets) == 0):
                break
            else:
                last_id = more_tweets[-1].id - 1
            tweets = tweets + more_tweets

        media_files = set()

        for status in tweets:
            media = status.entities.get('media', [])
            if (len(media) > 0):
                media_files.add(media[0]['media_url'])

        for media_file in media_files:
            wget.download(media_file,ROUTE_IMAGE_DIRECTORY)

        remove_image = glob.glob(ROUTE_IMAGE_DIRECTORY + '*.jpg')
        for image in remove_image:
            data_processing(f"https://twitter.com/{user}", image)
            os.remove(user)

            wget.download(media_file)

def download_from_hastags(hastagList):
    # login en twitter
    auth = tweepy.OAuthHandler(TWT_consumer_key, TWT_consumer_secret)
    auth.set_access_token(TWT_access_token, TWT_access_token_secret)

    # Api
    api = tweepy.API(auth)

    for hastag in hastagList:

        tweets = api.user_timeline(screen_name="#"+hastag,
                               count=200, include_rts=False,
                               exclude_replies=True)
        last_id = tweets[-1].id

        while (True):
            more_tweets = api.user_timeline(screen_name=hastag,
                                            count=200,
                                            include_rts=False,
                                            exclude_replies=True,
                                            max_id=last_id - 1)
            # There are no more tweets
            if (len(more_tweets) == 0):
                break
            else:
                last_id = more_tweets[-1].id - 1
            tweets = tweets + more_tweets

        media_files = set()

        for status in tweets:
            media = status.entities.get('media', [])
            if (len(media) > 0):
                media_files.add(media[0]['media_url'])

        for media_file in media_files:
            wget.download(media_file, ROUTE_IMAGE_DIRECTORY)

        remove_image = glob.glob(ROUTE_IMAGE_DIRECTORY + '*.jpg')
        for image in remove_image:
            data_processing(f"https://twitter.com/{hastag}", image)
            os.remove(hastag)

            wget.download(media_file)


def start_twitter_bot():

    usernames = get_username_from_txt("cuentasmemetwt.txt")
    hastagList = get_username_from_txt("hastagListtwt.txt")
    download_twt_images(usernames)
    download_from_hastags(hastagList)


