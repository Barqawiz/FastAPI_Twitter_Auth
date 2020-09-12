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

@author: Github.com/Barqawiz
"""

import tweepy


class TwitterUtil:

    def __init__(self, api_key, api_sec):
        self.consumer_key = api_key
        self.consumer_secret = api_sec

    def request_token(self, oauth_callback: str):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret, oauth_callback)
        auth_url = auth.get_authorization_url()

        return auth.request_token

    def access_token(self, oauth_token: str, oauth_verifier: str):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.request_token = {'oauth_token': oauth_token,
                              'oauth_token_secret': oauth_verifier}

        access_token, access_token_secret = auth.get_access_token(oauth_verifier)
        user_dict = self.__get_user_details(api=tweepy.API(auth))

        return {
            "access_token": access_token,
            "access_token_secret": access_token_secret,
            "screen_name": user_dict['screen_name'],
            "user_id": user_dict['user_id']
        }

    def __get_user_details(self, api):
        user = api.verify_credentials()

        if user:
            return {'screen_name': user.screen_name,
                    'user_id': user.id_str}
        else:
            raise tweepy.TweepError('Unable to get the user details, invalid oauth token!')
