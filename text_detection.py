import cv2
from imageai.Detection import ObjectDetection
from moviepy.editor import VideoFileClip
import os
from PIL import Image
import pytesseract

proxy = 'http://edcguest:edcguest@172.31.102.14:3128'

os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy

def convert_to_photo_text(filepath, keyword):
    print(cv2.__version__)
    filepath = './static/images/video_text.mp4'
    vidcap = cv2.VideoCapture(filepath)
    success,image = vidcap.read()
    count = 0
    success = True
    clip = VideoFileClip(filepath)
    clipDuration = clip.duration;
    while success:
      vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*9000))
      cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
      success,image = vidcap.read()
      print ('Read a new frame: ', success)
      count += 1
    clipDuration /= count;
    frameTime = []
    finalTime = []
    for i in range (count):
        frameTime.append(i*clipDuration);
    print(frameTime)
    execution_path = os.getcwd()
    for i in range (count):
        text = pytesseract.image_to_string(Image.open("frame%d.jpg" % i), lang = "eng")
        print(text.lower())
        if keyword in text.lower():
            finalTime.append(frameTime[i])
    print(finalTime)
    return finalTime
# convert_to_photo_text("video_text.mp4", "hashes")