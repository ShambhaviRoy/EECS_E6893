from django.http import request
from django.shortcuts import render

def welcome(request):
    context = {}
    context['content1'] = 'Welcome to Personalized Company Research Dashboard!'
    context['content2'] = 'EECS E6893 Project: '
    context['content3'] = 'Created by Shambhavi Roy, Saravanan Govindarajan, and Rahul Lokesh'
    context['content4'] = """This is a personalized company research dashboard to help you understand the company of your choice in the US stock market. 
                            For your selection of company, our tool will help you see the current stock market price, current trending videos, and real-time sentiment through tweets."""
    return render(request, 'welcome.html', context)

def stock(request):
    # function to retrieve youtube videos from API call
    context = {}
    context['content1'] = 'Stock Information'
    return render(request, 'stock.html', context)

# class CreateMyModelView(request):
#     model = MyModel
#     form_class = MyModelForm
#     template_name = 'myapp/template.html'
#     success_url = 'myapp/success.html'


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