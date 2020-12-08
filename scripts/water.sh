# move to the directory that this script is located in
cd -P -- "$(dirname -- "$0")"
cd ..

# video length is 10 seconds longer than pump length
# this ensures that we see water flow start and stop
pump_length=$1
video_length=$(($pump_length + 10))

./scripts/take-video.sh $video_length &
sleep 5

python3 python/pump.py --seconds $pump_length
