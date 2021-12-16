import yfinance as yf
import numpy as np
import pandas as pd

from datetime import datetime, timedelta
from textwrap import dedent
import time

import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import Stream
# from tweepy.streaming import StreamListener
import socket 
import json

from django.conf import settings
from django.http import request, response
from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests


class TweetsListener(Stream):
    """
    tweets listener object
    """
    def __init__(self, csocket):
        self.client_socket = csocket
    def on_data(self, data):
        try:
            msg = json.loads( data )
            print('TEXT:{}\n'.format(msg['text']))
            self.client_socket.send( msg['text'].encode('utf-8') )
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            return False
        # return True
    def on_error(self, status):
        print(status)
        return False

def sendData(c_socket, tags):
    """
    send data to socket
    """
    auth = OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)
    twitter_stream = Stream(auth, TweetsListener(c_socket))
    twitter_stream.filter(track=tags,languages=['en'])


class twitter_client:
    def __init__(self, TCP_IP, TCP_PORT):
      self.s = s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.s.bind((TCP_IP, TCP_PORT))

    def run_client(self, tags):
      try:
        self.s.listen(1)
        while True:
          print("Waiting for TCP connection...")
          conn, addr = self.s.accept()
          print("Connected... Starting getting tweets.")
          sendData(conn,tags)
          conn.close()
      except KeyboardInterrupt:
        exit





def welcome(request):
    context = {}
    context['content1'] = 'Welcome to Personalized Company Research Dashboard!'
    context['content2'] = 'EECS E6893 Project: '
    context['content3'] = 'Created by Shambhavi Roy, Saravanan Govindarajan, and Rahul Lokesh'
    context['content4'] = """This is a personalized company research dashboard to help you understand the company of your choice in the US stock market. 
                            For your selection of company, our tool will help you see the current stock market price, current trending videos, and real-time sentiment through tweets."""
    
    context['content5'] = 'You have selected company:'

    
    if request.method == 'POST':
        stock_wanted = request.POST.get('stock')
        context['content6'] = stock_wanted
        return render(request, 'welcome.html', context)


    else:
        stock_ticker_dict = {'Alphabet Inc. (GOOG)' : 'GOOG', 
                            'Amazon.com Inc. (AMZN)' : 'AMZN', 
                            'Apple Inc. (AAPL)': 'AAPL',
                            'Meta Platforms, Inc. (FB)' : 'FB',
                            'Microsoft Corporation (MSFT)': 'MSFT',
                            'Netflix, Inc. (NFLX)': 'NFLX',
                            None: 'AAPL'}

        # get ticker from form - tried AAPL as example
        ticker = 'AAPL'
        tick = yf.Ticker(ticker)
        tick_hist = tick.history(period = '1d', interval = '1m')

        # get open, high, low, close, volume
        context['date'] = tick_hist.index[-1]
        context['open'] = tick_hist['Open'].iloc[-1]
        context['high'] = tick_hist['High'].iloc[-1]
        context['low'] = tick_hist['Low'].iloc[-1]
        context['close'] = tick_hist['Close'].iloc[-1]
        context['volume'] = tick_hist['Volume'].iloc[-1]

        return render(request, 'welcome.html', context)



    

    



def youtube(request):
    # function to retrieve youtube videos from API call
    context = {}
    context['content1'] = 'Relevant YouTube Videos'
    context['content2'] = 'Look up on YouTube:'
    context['content3'] = 'Videos are attached one-by-one in embedding. Keep watching...'
    
    # how to get response from form to a different page?
    # print(request.POST.get('stock'))
    stock_wanted = request.POST.get('stock', None)
    context['company'] = str(stock_wanted)

    import argparse

    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError


    # Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
    # tab of
    #   https://cloud.google.com/console
    # Please ensure that you have enabled the YouTube Data API for your project.

    DEVELOPER_KEY = 'AIzaSyAovYYRq5qG_caQTp9lzQQWTsxLyFSAufY'
    YOUTUBE_API_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'

    # def youtube_search(company):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term q.
    search_response = youtube.search().list(
        q='Apple+news+(AAPL)',
        part='id, snippet',
        relevanceLanguage = 'en',
        maxResults=10
        # maxResults=options.max_results
    ).execute()

    videos = []
    channels = []
    playlists = []
    video_urls = []
    video_ids = []
    url = ''
    # embed_url = ''

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append('%s (%s)' % (search_result['snippet']['title'],
                                    search_result['id']['videoId']))
            url = 'https://www.youtube.com/watch?v=' + str(search_result['id']['videoId'])
            print('URL:', url)
            print(video_urls)
            video_urls.append(url)

            video_ids.append(str(search_result['id']['videoId']))
        
        elif search_result['id']['kind'] == 'youtube#channel':
            channels.append('%s (%s)' % (search_result['snippet']['title'],
                                    search_result['id']['channelId']))
        
        elif search_result['id']['kind'] == 'youtube#playlist':
            playlists.append('%s (%s)' % (search_result['snippet']['title'],
                                        search_result['id']['playlistId']))

    context['embed_url'] = 'https://www.youtube.com/embed/'+ video_ids[0] + '?playlist="'

    for i in range(1, len(video_ids)):
        if i == len(video_ids)-1:
            context['embed_url'] += video_ids[i] + '"'
        else:
            context['embed_url'] += video_ids[i] + ','

    
    for i in range(len(video_urls)):
        context['video' + str(i)] = videos[i]
        context['url' + str(i)] = video_urls[i]
     

    print ('Videos:\n', '\n'.join(videos), '\n')

    return render(request, 'youtube.html', context)

        

def twitter(request):
    # function to retrieve tweets from Twitter API call
    context = {}
    context['content1'] = 'Relevant Tweets'

    # if request.method == 'POST':
    #     company = request.POST.get('stock', None)
    # context['content2'] = company

    # company = request.POST.get('stock', None)

    # company = 'AAPL'

    # if company:
    #     auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    #     auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_SECRET)

    #     api = tweepy.API(auth)
    #     api.update_status(company)

    tags = ['Apple', 'AAPL', 'news']
    client = twitter_client("localhost", 9003)
    client.run_client(tags)





    return render(request, 'twitter.html', context)




