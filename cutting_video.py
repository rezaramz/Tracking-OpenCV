import sys
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--output_file', '-o', help='The path the output video is written into.')
parser.add_argument('--input_file', '-i', help='The path to the input video.')
parser.add_argument('--start_time', '-s', help='The start time.')
parser.add_argument('--end_time', '-e', help='The end time.')

args = parser.parse_args()

input_file = args.input_file
output_file = args.output_file
start_time = args.start_time
end_time = args.end_time

ffmpeg_extract_subclip(input_file, start_time, end_time, targetname=output_file)

# How to call it from MATLAB
"system(python input_file output_file start_time end_time)"
