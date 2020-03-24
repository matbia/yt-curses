import urllib.request, json
from datetime import datetime
from textwrap import TextWrapper
from html import unescape
from subsmgr import *

api_url = 'https://invidio.us/api/v1/'
api_params = '?fields=videoId,title,author,authorId,published'

class Video:
    def __init__(self, id, title, channel_id, channel_name, upload_date):
        self.id = id
        self.title = title
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.upload_date = upload_date

#Returns JSON data from URL
def send_request(url):
    return json.loads(urllib.request.urlopen(urllib.request.Request(url)).read())

#Parses JSON into object list
def json_to_videos_list(data):
    videos = []
    for i in data:
        videos.append(Video(i['videoId'], unescape(i['title']), i['authorId'], i['author'], datetime.fromtimestamp(int(i['published']))))
    return videos

def get_videos_from_channel(channel_id):
    videos = json_to_videos_list(send_request(api_url + 'channels/videos/' + channel_id + api_params))
    return videos

def search_videos(query):
    return json_to_videos_list(send_request(api_url + 'search?' + api_params + '&q=' + urllib.parse.quote_plus(query)))[::-1]

def get_related_videos(video_id):
    return json_to_videos_list(send_request(api_url + '?mode=related&id=' + video_id))[::-1]

def load_subscriptions_videos():
    subscriptions = get_subscribed_channels()
    videos = []
    for x in range(0, len(subscriptions)):
        videos += get_videos_from_channel(subscriptions[x])
    videos.sort(key=lambda v: v.upload_date, reverse = True) #Sort videos by upload date descending
    return videos

#Returns a string containing video's views, rating, and description
def get_video_info(video_id):
    video_info = send_request(api_url + 'videos/' + video_id + '?fields=description,viewCount,likeCount,dislikeCount')
    desc = video_info['description']
    view_count = video_info['viewCount']
    like_count = video_info['likeCount']
    dislike_count = video_info['dislikeCount']
    rating = '{0:.2f}'.format(int(like_count) / int(dislike_count))
    return 'Views: ' + view_count + '\nRating: ' + like_count + '/' + dislike_count + ' (' + rating + ')\n\n' + desc
