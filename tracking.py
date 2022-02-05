import cv2, os
import argparse
import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
import shutil
np.random.seed(0)
try:
    os.remove('.tmp.txt')
except:
    pass
########################################################
def random_color_generator(n: int):
    colors = []
    for i in range(n + 1):
        res = np.random.randint(0, 256, 3)
        colors.append( (int(res[0]), int(res[1]), int(res[2])) )
    return colors

########################################################
parser = argparse.ArgumentParser(description='Object tracking program. Author: Mohammadreza Ramzanpour')
parser.add_argument('--input_video', '-i', help='The path to the input video file.')
parser.add_argument('--output_file', '-o', help='The output file which contains the bounding boxes of the tracked objects.')
parser.add_argument('--format', '-f', help='The format of the pictures to be saved from result of the tracking. default: png')
parser.add_argument('--make_video', '-m', help='If True, a video will be created from the saved resultant images.')

args = parser.parse_args()

video_file = args.input_video

if args.output_file is None:
    output_file = video_file[0:video_file.find('.')] + '.csv'
else:
    output_file = args.output_file

if args.format is None:
    format_ = 'png'
else:
    format_ = args.format
    if format_[0] == '.':
        format_ = format_[1:]

if args.make_video is None:
    make_video = False
else:
    if args.make_video.lower() == 'true':
        make_video = True
    elif args.make_video.lower() == 'false':
        make_video = False


try:
    save_directory = output_file[0:output_file.find('.')]
    os.mkdir(save_directory)
except:
    save_directory = output_file[0:output_file.find('.')]
    shutil.rmtree(save_directory)
    os.mkdir(save_directory)

#########################################################

vid = cv2.VideoCapture(video_file)
tracker = cv2.TrackerMIL_create() # good performance
ret, frame = vid.read()

## Select boxes
bboxes = []
colors = [] 

c = 1
while True:
  # draw bounding boxes over objects
  # selectROI's default behaviour is to draw box starting from the center
  # when fromCenter is set to false, you can draw box starting from top left corner
  bbox = cv2.selectROI('MultipleTracking', frame, False, fromCenter=False)
  bboxes.append(bbox)
  print('Box {} Selected -- Press Enter to select next object or hit q to exit'.format(c))
  c += 1
  if cv2.waitKey(0) & 0xff == ord('Q'.lower()):
      cv2.destroyWindow('MultipleTracking')
      break

##########################################################
# CALIBRATION PROCESS BY SELECTING TWO POINTS
def read_click(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        with open('.tmp.txt', 'a') as f:
            f.write('%d,%d\n' % (x, y))
            
def read_point():
    x_ = np.array(pd.read_csv('.tmp.txt', header=None))
    try:
        os.remove('.tmp.txt')
    except:
        pass
    return x_


ret, frame = vid.read()
cv2.imshow('Calibration', frame)
cv2.setMouseCallback('Calibration', read_click)
cv2.setMouseCallback('Calibration', read_click)
cv2.waitKey(0)
cv2.destroyWindow('Calibration')
points = read_point()
p1, p2 = points[0], points[1]
calib_distance = float(input('Enter the distance between those two selected points: '))
cv2.circle(frame, (p1[0], p1[1]), 2, (0, 0, 255), 2)
cv2.circle(frame, (p2[0], p2[1]), 2, (0, 0, 255), 2)
cv2.imshow('SelectedPoints', frame)
cv2.waitKey(0)
cv2.destroyWindow('SelectedPoints')
# np.linalg.norm(p1 - p2)
np.savetxt('{}/points.txt'.format(save_directory), points, fmt='%d', delimiter=',')
with open('{}/points.txt'.format(save_directory, ), 'a') as f:
    f.write('%.2f' % calib_distance)


#############################################################

colors_boxes = random_color_generator(c)

multi_tracker = cv2.legacy_MultiTracker.create()

for bbox in bboxes:
    multi_tracker.add(cv2.legacy.TrackerMIL_create(), frame, bbox)


def draw_box(img, bbox, color):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), (x + w, y + h), color, 3, 1)
    cv2.putText(img, 'Track', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)  


fw = open('{}/{}'.format(save_directory, output_file), 'w')
fw.write('n,x,y,w,h\n')

# Writing selected frames by user
for i, bbox in enumerate(bboxes):
    fw.write('%d,%d,%d,%d,%d\n' % (i+1, *bbox))

count = 1
while True:
    timer = cv2.getTickCount()
    ret, frame = vid.read()
    if not ret:
        break

    success, bboxes = multi_tracker.update(frame)

    if success:
        for i, bbox in enumerate(bboxes):
            clr = colors_boxes[i]
            draw_box(frame, bbox, clr)
            fw.write('%d,%.2f,%.2f,%.2f,%.2f\n' % (i+1,*bbox))
    else:
        cv2.putText(frame, 'Lost', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        fw.write(',,,\n')


    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    cv2.putText(frame, 'fps={}'.format(round(fps)), (50, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)    
    cv2.imshow('Tracking', frame)
    cv2.imwrite('{}/{}.{}'.format(save_directory, str(count).zfill(10), format_), frame)
    count = count + 1

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
fw.close()

if make_video:
    from video_maker import make_video
    make_video(directory=save_directory, output_video=video_file[0:video_file.find('.')] + '_trk' + video_file[video_file.find('.'):])
