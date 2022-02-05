import sys
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

input_file = sys.argv[1]
output_file = sys.argv[2]

start_time = int(sys.argv[3])
end_time = int(sys.argv[4])

ffmpeg_extract_subclip(input_file, start_time, end_time, targetname=output_file)

# How to call it from MATLAB
"system(python input_file output_file start_time end_time)"
