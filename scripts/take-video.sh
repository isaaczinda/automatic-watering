# move to the directory that this script is located in
cd -P -- "$(dirname -- "$0")"
cd ../python

# remove the old temporary video file
rm ../tmp/vid.avi

# record the video
ffmpeg -t $1 -f v4l2 -r 25 -video_size 640x480 -i /dev/video0 ../tmp/vid.avi

# upload the video
python3 upload_media.py --filepath ../tmp/vid.avi
