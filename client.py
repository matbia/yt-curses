import urllib.request, json, datetime, sys
from textwrap import TextWrapper
from html import unescape
from subsmgr import *
from player import *

api_params = '?fields=videoId,title,author,authorId,published,lengthSeconds'

#Load API URL of selected Invidious instance
try:
    with open(path.join(path.dirname(__file__), 'api.txt')) as f:
        api_url = unescape(f.readline()).rstrip()
except FileNotFoundError:
    sys.exit('ERROR: api.txt not found')


class Video:
    def __init__(self, id, title, length, channel_id, channel_name, upload_date):
        self.id = id
        self.title = title
        self.length = length
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
        vlen = str(datetime.timedelta(seconds=i['lengthSeconds']))
        vpub = (lambda v: datetime.datetime.fromtimestamp(int(v['published'])) if 'published' in v else 'N/A in current mode')(i)
        videos.append(Video(i['videoId'], unescape(i['title']), vlen, i['authorId'], i['author'], vpub))
    return videos

def get_videos_from_channel(channel_id):
    return json_to_videos_list(send_request(api_url + 'channels/videos/' + channel_id + api_params))

def search_videos(query):
    return json_to_videos_list(send_request(api_url + 'search?' + api_params + '&q=' + urllib.parse.quote_plus(query)))[::-1]

def get_recommended_videos(video_id):
    return json_to_videos_list(send_request(api_url + 'videos/' + video_id + '?fields=recommendedVideos')['recommendedVideos'])

def load_subscriptions_videos():
    videos = []
    for s in get_subscribed_channels():
        videos += get_videos_from_channel(s)
    videos.sort(key=lambda v: v.upload_date, reverse = True) #Sort videos by upload date descending
    return videos

#Returns JSON containing video's views, rating, and description
def get_video_info(video_id):
    return send_request(api_url + 'videos/' + video_id + '?fields=description,viewCount,likeCount,dislikeCount')
