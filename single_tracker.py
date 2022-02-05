import cv2, os
import pandas as pd
import matplotlib.pyplot as plt

vid = cv2.VideoCapture('short_version.mp4')

tracker = cv2.TrackerMIL_create() # good performance
# tracker = cv2.legacy.TrackerMOSSE_create()
# tracker = cv2.legacy.TrackerCSRT_create()
# tracker = cv2.TrackerGOTURN_create()
# tracker = cv2.legacy.TrackerBoosting_create()
# tracker = cv2.TrackerMIL_create() # good performance
# tracker = cv2.legacy.TrackerTLD_create()
# tracker = cv2.legacy.TrackerKCF_create()

ret, frame = vid.read()
bbox = cv2.selectROI('Tracking', frame, False)
tracker.init(frame, bbox)

def draw_box(img, bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), (x + w, y + h), (128, 0, 128), 3, 1)
    cv2.putText(img, 'Track', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)  


try:
    os.mkdir('data')
except:
    pass

fw = open('output.txt', 'w')
fw.write('x,y,w,h\n')

count = 1
while True:
    timer = cv2.getTickCount()
    ret, frame = vid.read()
    if not ret:
        break

    success, bbox = tracker.update(frame)

    if success:
        draw_box(frame, bbox)
        fw.write('%.2f,%.2f,%.2f,%.2f\n' % (bbox[0], bbox[1], bbox[2], bbox[3]))
    else:
        cv2.putText(frame, 'Lost', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        fw.write(',,,\n')


    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    cv2.putText(frame, 'fps={}'.format(round(fps)), (50, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)    
    cv2.imshow('Tracking', frame)
    cv2.imwrite('data/{}.png'.format(count), frame)
    count = count + 1

    if cv2.waitKey(1) & 0xff == ord('q'):
        break
fw.close()


#VISUALIZE
df = pd.read_csv('output.txt', header=0).dropna(axis=0, how='any')
center_x = df.loc[:, 'x'] + 0.5 * df.loc[:, 'w']
center_x = center_x - center_x[0]
center_y = -1 * (df.loc[:, 'y'] + 0.5 * df.loc[:, 'h'])
center_y = center_y - center_y[0]

plt.scatter(center_x, center_y)
