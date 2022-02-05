import cv2, os#, sys


def make_video(directory, output_video, fps=24):

    files = os.listdir(directory)
    files.sort()

    img_array = []

    for file_ in files:
        img = cv2.imread('{}/{}'.format(directory, file_))
        if img is None:
            continue
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)

    out = cv2.VideoWriter('{}/{}'.format(directory, output_video), cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
    
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

