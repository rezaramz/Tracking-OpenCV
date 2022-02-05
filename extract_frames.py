import cv2, os

video_file = 'ferret_video1.mp4'
vid = cv2.VideoCapture(video_file)
os.mkdir('data')

# frame
currentframe = 0
  
while(True):
      
    # reading from frame
    ret,frame = vid.read()
  
    if ret:
        # if video is still left continue creating images
        name = './data/frame' + str(currentframe) + '.jpg'
        print ('Creating...' + name)
  
        # writing the extracted images
        cv2.imwrite(name, frame)
  
        # increasing counter so that it will
        # show how many frames are created
        currentframe += 1
    else:
        break
  
# Release all space and windows once done
vid.release()
cv2.destroyAllWindows()