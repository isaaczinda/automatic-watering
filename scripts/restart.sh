# move to the directory that this script is located in
cd -P -- "$(dirname -- "$0")"
cd ..

# log that we are restarting
timestamp=`date +%Y-%m-%d_%H-%M-%S`
echo "restarting at $timestamp" >> logs/restart.log

# restart
shutdown -r
