# -*- coding: utf-8 -*-

#!/usr/bin/python

import argparse

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = ''
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def youtube_search():
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    q='APPLE+news+AAPL',
    part='id,snippet',
    order='date',
    type='video',
    maxResults=50
  ).execute()

  videos = []
  for search_result in search_response.get('items', []):
    if search_result['id']['kind'] == 'youtube#video':
      videos.append('%s (https://www.youtube.com/watch?v=%s)' % (search_result['snippet']['title'],
                                 search_result['id']['videoId']))

  for index in range(len(videos)):
    print ('Videos:\n', videos[index])

if __name__ == '__main__':
  youtube_search()

