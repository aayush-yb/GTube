import cv2
from imageai.Detection import ObjectDetection
from moviepy.editor import VideoFileClip
import os

proxy = 'http://edcguest:edcguest@172.31.102.14:3128'

os.environ['http_proxy'] = proxy 
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy

def convert_to_photo(filepath, keyword):
    print(cv2.__version__)
    filepath = './static/images/video2.mp4'
    vidcap = cv2.VideoCapture(filepath)
    success,image = vidcap.read()
    count = 0
    success = True
    clip = VideoFileClip(filepath)
    clipDuration = clip.duration;
    while success:
      vidcap.set(cv2.CAP_PROP_POS_MSEC,(count*3000))
      cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
      success,image = vidcap.read()
      print ('Read a new frame: ', success)
      count += 1
    clipDuration /= count;
    print(keyword)
    frameTime = []
    finalTime = []
    for i in range (count):
        frameTime.append(i*clipDuration);
    print(frameTime)
    execution_path = os.getcwd()
    for i in range (count):
        detector = ObjectDetection()
        detector.setModelTypeAsRetinaNet()
        detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
        detector.loadModel()
        detections = detector.detectObjectsFromImage(input_image=os.path.join(execution_path , "frame%d.jpg" % i), output_image_path=os.path.join(execution_path , "framenew%d.jpg" % i))

        for eachObject in detections:
            #print(eachObject["name"] , " : " , eachObject["percentage_probability"] )
            if(eachObject["name"] == keyword and eachObject["percentage_probability"] > 50.0):
                #print("found at frame number", i)
                finalTime.append(frameTime[i])
    print(finalTime)
    return finalTime
# convert_to_photo("videoplayback.mp4", "person")
