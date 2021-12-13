from django.http import request, response
from django.http import HttpResponse
from django.shortcuts import render

import yfinance as yf
import numpy as np
import pandas as pd

from datetime import datetime, timedelta
from textwrap import dedent
import time


def welcome(request):
    context = {}
    context['content1'] = 'Welcome to Personalized Company Research Dashboard!'
    context['content2'] = 'EECS E6893 Project: '
    context['content3'] = 'Created by Shambhavi Roy, Saravanan Govindarajan, and Rahul Lokesh'
    context['content4'] = """This is a personalized company research dashboard to help you understand the company of your choice in the US stock market. 
                            For your selection of company, our tool will help you see the current stock market price, current trending videos, and real-time sentiment through tweets."""
    
    context['content5'] = 'You have selected company:'

    # print(request.POST.get('stock'))
    # stock_wanted = request.POST.get('stock')

    # context['content6'] = stock_wanted

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


# def get_yahoo(request):
#     # checking yfinance
#     context = {}

#     # get ticker from form - tried AAPL as example
#     ticker = 'AAPL'
#     tick = yf.Ticker(ticker)
#     tick_hist = tick.history(period = '1d', interval = '1m')

#     # get open, high, low, close, volume
#     context['date'] = tick_hist.index[-1]
#     context['open'] = tick_hist['Open'].iloc[-1]
#     context['high'] = tick_hist['High'].iloc[-1]
#     context['low'] = tick_hist['Low'].iloc[-1]
#     context['close'] = tick_hist['Close'].iloc[-1]
#     context['volume'] = tick_hist['Volume'].iloc[-1]

#     return render(request, 'welcome.html', context) 



def stock(request):
    # function to retrieve youtube videos from API call
    context = {}
    context['content1'] = 'Relevant Youtube Videos'
    
    # how to get response from form to a different page?
    print(request.POST.get('stock'))
    stock_wanted = request.POST.get('stock')
    context['content2'] = stock_wanted
        
    return render(request, 'stock.html', context)




    # choice = request.POST.get('stock', False)

    # context = {}
    # context['content1'] = 'Stock Information'

    # context['content2'] = 'You have selected company:'
    # context['content3'] = choice
    # return render(request, 'stock.html', {'stock':choice})



def get_videos(request):
    # function to retrieve youtube videos from API call
    context = {}
    # context['content1'] = 'Stock Information'
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
        q='Apple (AAPL)',
        part='id, snippet',
        relevanceLanguage = 'en',
        maxResults=10
        # maxResults=options.max_results
    ).execute()

    videos = []
    channels = []
    playlists = []
    video_urls = []
    url = ''

    # Add each result to the appropriate list, and then display the lists of
    # matching videos, channels, and playlists.
    for search_result in search_response.get('items', []):
        if search_result['id']['kind'] == 'youtube#video':
            videos.append('%s (%s)' % (search_result['snippet']['title'],
                                    search_result['id']['videoId']))
            url = 'https://www.youtube.com/watch?v=' + str(search_result['id']['videoId'])
            print('URL:', url)
            video_urls.append(url)
        elif search_result['id']['kind'] == 'youtube#channel':
            channels.append('%s (%s)' % (search_result['snippet']['title'],
                                    search_result['id']['channelId']))
        elif search_result['id']['kind'] == 'youtube#playlist':
            playlists.append('%s (%s)' % (search_result['snippet']['title'],
                                        search_result['id']['playlistId']))
        # url = 'https://www.youtube.com/watch?v=${result.id.videoId}'
        

    print ('Videos:\n', '\n'.join(videos), '\n')
    #   print ('Channels:\n', '\n'.join(channels), '\n')
    #   print ('Playlists:\n', '\n'.join(playlists), '\n')
    # return video_urls

    return render(request, 'stock.html', context)