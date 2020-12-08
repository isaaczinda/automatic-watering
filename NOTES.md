# Add user to Sudoers
```
su -
adduser -aG sudo isaac
visudo
```

Then add to the sudoers file


# To take a webcam pic
```
sudo apt-get install fswebcam
sudo usermod -aG video isaac
fswebcam -r 960x720 image2.jpg
```

# install SSH
```
sudo apt-get install openssh-server
sudo systemctl enable ssh
```

# setup ngrok to start on startup

 - install ngrok in /usr/local/bin
 - get auth token from website @ save to file as determined

 - make this file in ~/.ngrok2


 ```yml
// use spaces here instead of tabs, or else yaml will barf
authtoken: <your-auth-token>
tunnels:
  default:
    proto: tcp
    addr: 22
 ```

To run the ngrok command on startup, create the file
/lib/systemd/system/ngrok.service:

```
[Unit]
Description=Ngrok
After=network.service

[Service]
type=simple
User=isaac
ExecStart=/usr/bin/ngrok start --all --config="/home/isaac/.ngrok2/ssh-config.yml"
Restart=on-failure

[Install]
WantedBy=multi-user.target
```


to "enable" (start on pi boot) ngrok.service: `sudo systemctl enable ngrok.service`
to start the service:
to view logs: `sudo journalctl -u ngrok.service`

# crontabs

to edit: `crontab -e`

`*/2 * * * * echo "test" 2>&1 /some/test/path.log` -- run the command every 2m

# how to change username

https://thepihut.com/blogs/raspberry-pi-tutorials/how-to-change-the-default-account-username-and-password

# setup default wifi

In /etc/wpa_supplicant/wpa_supplicant.conf, add the line `priority 2`:

```
network={
   ssid="wifi_B"
   psk="passwordOfB"
   priority=2
}
```

All networks are by default priority 0, and whichever has the highest
priority is selected on boot to connect to.

# to change so that just a few users can use SSH:

https://ostechnix.com/allow-deny-ssh-access-particular-user-group-linux/

# setup scripts for running

To install Drive upload:

`pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`



# Notes
 - need to use webcam on usb3.0
