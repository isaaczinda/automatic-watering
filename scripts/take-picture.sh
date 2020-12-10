# move to the directory that this script is located in
cd -P -- "$(dirname -- "$0")"
cd ../python

# remove the old temporary picture
rm ../tmp/pic.jpg

# setup webcam to take ideal pics
../scripts/setup-webcam.sh

# skip first 100 frames to allow the webcam to auto-adjust brightness and focus lens
fswebcam -r 1920x1080 -S 100 ../tmp/pic.jpg
python3 upload_media.py --filepath ../tmp/pic.jpg
