"""
License
-------
    The MIT License (MIT)
    Copyright (c) 2017 Tashkel Project
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

Created on Sep 12 2020
@author: Ahmad Barqawi
"""
import utility.Config as Config
from utility.TwitterUtil import TwitterUtil
import utility.ErrorResponse as ErrorResponse
from fastapi import FastAPI, HTTPException
import uvicorn
import argparse
import tweepy

# ## Initials ##
parser = argparse.ArgumentParser()
parser.add_argument("-host", "--host",  help="REST service hostname", default=Config.CONNECT.HOST)
parser.add_argument("-port", "--port",  help="REST service port", default=Config.CONNECT.PORT, type=int)

args = parser.parse_args()
app = FastAPI(title="Twitter API", version="1.0.0")
twitter = TwitterUtil(Config.KEYS.TW_API_KEY, Config.KEYS.TW_API_SEC)


@app.get("/")
async def main_page():
    return "Social API helper fot Twitter login"


# ## Twitter API Functions ##
@app.get('/request_token')
def request_token(oauth_callback: str):
    """
    1- Get initial twitter configurations.
       The callback URL should be defined in the Twitter developer app
    :param oauth_callback:
    :return: config dict.
    """
    try:
        return twitter.request_token(oauth_callback)
    except tweepy.TweepError as e:
        print('Twitter Exception: ', e)
        raise ErrorResponse.tw_request_invalid
    except Exception:
        raise ErrorResponse.tw_request_invalid


@app.get('/access_token')
def access_token(oauth_token: str, oauth_verifier: str):
    """
    2- Access twitter token and return login tokens
    :param oauth_token:
    :param oauth_verifier:
    :return:
    """
    try:
        return twitter.access_token(oauth_token, oauth_verifier)
    except tweepy.TweepError as e:
        print('Twitter Exception: ', e)
        raise ErrorResponse.tw_access_invalid


if __name__ == "__main__":
    uvicorn.run(app, host=args.host, port=args.port)