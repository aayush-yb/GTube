import requests
from urllib.parse import urlparse, parse_qs
from xml.etree import ElementTree

from requests.auth import HTTPProxyAuth

proxies = {"http":"172.31.100.14:3128"}
auth = HTTPProxyAuth("edcguest", "edcguest")
OK = 200

def get_video_id(url):
    """ Get YouTube video ID from YouTube URL """

    if not url:
        return ""

    if "embed" in url:
        return url.split("/")[-1]

    parse_result = urlparse(url)
    query = parse_qs(parse_result.query)
    return query["v"][0]


def transcribe_video(youtube_url, ghost=True):
    """ Transcribe YouTube video. """
    id = get_video_id(youtube_url)
    url = "http://video.google.com/timedtext?lang=en&v={}".format(id)
    print(url)
    response = requests.get(url, proxies=proxies, auth=auth)
    return response.status_code, response.content


def search_keywords(youtube_url, keyword):
    """ Search for keyword in a YouTube video."""
    print("hihihihi")
    timestamps = list()
    if not keyword or not youtube_url:
        return timestamps
    status_code, content = transcribe_video(youtube_url)
	
    print(content)
    if not content:
        print("NO CONTENT")
        return timestamps

    if status_code == OK:
        tree = ElementTree.fromstring(content)
        print(keyword)
        for node in tree:
            print(node.text)
            if keyword in node.text:
                print(node.text)
                print(node.attrib)
                timestamps.append(float(node.attrib["start"]))

    print(timestamps)
    return timestamps


if __name__ == '__main__':
    url = "https://www.youtube.com/watch?v=d0NHOpeczUU"
    keyword = "sort"
    timestamps = search_keywords(url, keyword)
    print(timestamps)
