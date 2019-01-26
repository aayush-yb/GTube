from __future__ import unicode_literals
import json

from flask import Flask, redirect, request, render_template, jsonify
from youtube_transcriber import search_keywords

import argparse
import os
import re
from itertools import starmap
import multiprocessing

import pysrt
import imageio
import youtube_dl
import chardet
import nltk
imageio.plugins.ffmpeg.download()
nltk.download('punkt')

from moviepy.editor import VideoFileClip, concatenate_videoclips
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.lsa import LsaSummarizer


imageio.plugins.ffmpeg.download()


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/sum', methods=['POST'])
def summariser():
    url = request.form["url2"];
    fun(url)
    return render_template('index.html')

@app.route('/search_keyword', methods=['POST'])
def searchKeyWord():
    url = request.form["url"]
    keyword = request.form["keyword"]
    result = search_keywords(url, keyword)
    if not result:
        return jsonify(dict())
    return jsonify(timeStamp(result))


def timeStamp(list_time):

    format_time = dict()
    i = 0
    for time in list_time:
        m, s = divmod(time, 60)
        h, m = divmod(m, 60)
        format_time[str(i)] = {"%dh%02dm%02ds" % (h, m, s): time}
        i += 1
    return format_time


def summarize(srt_file, n_sentences, language="english"):
    parser = PlaintextParser.from_string(
        srt_to_txt(srt_file), Tokenizer(language))
    stemmer = Stemmer(language)
    summarizer = LsaSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(language)
    segment = []
    for sentence in summarizer(parser.document, n_sentences):
        index = int(re.findall("\(([0-9]+)\)", str(sentence))[0])
        item = srt_file[index]
        segment.append(srt_segment_to_range(item))
    return segment


def srt_to_txt(srt_file):

    text = ''
    for index, item in enumerate(srt_file):
        if item.text.startswith("["):
            continue
        text += "(%d) " % index
        text += item.text.replace("\n", "").strip("...").replace(
                                     ".", "").replace("?", "").replace("!", "")
        text += ". "
    return text


def srt_segment_to_range(item):
    start_segment = item.start.hours * 60 * 60 + item.start.minutes * \
        60 + item.start.seconds + item.start.milliseconds / 1000.0
    end_segment = item.end.hours * 60 * 60 + item.end.minutes * \
        60 + item.end.seconds + item.end.milliseconds / 1000.0
    return start_segment, end_segment


def time_regions(regions):
    return sum(starmap(lambda start, end: end - start, regions))


def find_summary_regions(srt_filename, duration=30, language="english"):

    srt_file = pysrt.open(srt_filename)

    enc = chardet.detect(open(srt_filename, "rb").read())['encoding']
    srt_file = pysrt.open(srt_filename, encoding=enc)

    # generate average subtitle duration
    subtitle_duration = time_regions(
        map(srt_segment_to_range, srt_file)) / len(srt_file)
    # compute number of sentences in the summary file
    n_sentences = duration / subtitle_duration
    print(subtitle_duration)
    print(n_sentences)
    summary = summarize(srt_file, n_sentences, language)
    total_time = time_regions(summary)
    too_short = total_time < duration
    if too_short:
        while total_time < duration:
            n_sentences += 1
            summary = summarize(srt_file, n_sentences, language)
            total_time = time_regions(summary)
    else:
        while total_time > duration:
            n_sentences -= 1
            summary = summarize(srt_file, n_sentences, language)
            total_time = time_regions(summary)
    return summary


def create_summary(filename, regions):
    subclips = []
    input_video = VideoFileClip(filename)
    last_end = 0
    for (start, end) in regions:
        subclip = input_video.subclip(start, end)
        subclips.append(subclip)
        last_end = end
    return concatenate_videoclips(subclips)


def get_summary(filename="1.mp4", subtitles="1.srt"):
    clip = VideoFileClip(filename)
    regions = find_summary_regions(subtitles, clip.duration/10, "english")
    summary = create_summary(filename, regions)
    base, ext = os.path.splitext(filename)
    output = "/home/ayushghd/Documents/imp/GTube/static/images/{0}_1.mp4".format(base)
    summary.to_videofile(
                output,
                codec="libx264",
                temp_audiofile="temp.m4a", remove_temp=True, audio_codec="aac")
    return True


def download_video_srt(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': '1.%(ext)s',
        'subtitlesformat': 'srt',
        'writeautomaticsub': True,
    }

    movie_filename = ""
    subtitle_filename = ""
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # ydl.download([subs])
        result = ydl.extract_info("{}".format(url), download=True)
        movie_filename = ydl.prepare_filename(result)
        subtitle_info = result.get("requested_subtitles")
        # subtitle_language = subtitle_info.keys()[0]
        subtitle_language = "en"
        # subtitle_ext = subtitle_info.get(subtitle_language).get("ext")
        subtitle_ext = "vtt"
        subtitle_filename = movie_filename.replace(".mp4", ".%s.%s" %
                                                   (subtitle_language,
                                                    subtitle_ext))
    return movie_filename, subtitle_filename


def fun(url):
    movie_filename, subtitle_filename = download_video_srt(url)
    summary_retrieval_process = multiprocessing.Process(target=get_summary, args=(movie_filename, subtitle_filename))
    summary_retrieval_process.start()
    summary_retrieval_process.join()
    os.remove(movie_filename)
    os.remove(subtitle_filename)
    print("[sum.py] Remove the original files")

if __name__ == '__main__':
    app.run()
