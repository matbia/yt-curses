import urllib.request, json
from textwrap import TextWrapper
from dateutil.parser import parse
from html import unescape
from subsmgr import *

api_url = 'https://hooktube.com/api'

class Video:
    def __init__(self, id, title, channel_id, channel_name, upload_date):
        self.id = id
        self.title = title
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.upload_date = upload_date

#Returns JSON data from URL
def send_request(url):
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={ 'User-Agent': '' })).read()) #Empty user agent to prevent 403 error

#Parses JSON into object list
def json_to_videos_list(data):
    videos = []
    for i in range(0, len(data['items'])):
        item = data['items'][i]
        videos.append(Video(item['id']['videoId'], unescape(item['snippet']['title']), item['snippet']['channelId'], item['snippet']['channelTitle'], parse(item['snippet']['publishedAt']).date()))
    return videos

def get_videos_from_channel(channel_id):
    videos = json_to_videos_list(send_request(api_url + '?mode=channel&id=' + channel_id))
    videos.sort(key=lambda v: v.upload_date, reverse = True) #Sort videos by upload date descending
    return videos

def search_videos(query):
    return json_to_videos_list(send_request(api_url + '?mode=search&q=' + urllib.parse.quote_plus(query)))[::-1]

def get_related_videos(video_id):
    return json_to_videos_list(send_request(api_url + '?mode=related&id=' + video_id))[::-1]

def load_subscriptions_videos():
    subscriptions = get_subscribed_channels()
    videos = []
    for x in range(0, len(subscriptions)):
        videos += json_to_videos_list(send_request(api_url + '?mode=channel&id=' + subscriptions[x]))
    videos.sort(key=lambda v: v.upload_date, reverse = True) #Sort videos by upload date descending
    return videos

#Returns a string containing video's views, rating, and description
def get_video_info(video_id):
    video_info = send_request(api_url + '?mode=video&id=' + video_id)['json_2']['items'][0]
    desc = video_info['snippet']['description']
    return 'Views: ' + video_info['statistics']['viewCount'] + '\nRating: ' + video_info['statistics']['likeCount'] + '/' + video_info['statistics']['dislikeCount'] + '\n\n' + desc
