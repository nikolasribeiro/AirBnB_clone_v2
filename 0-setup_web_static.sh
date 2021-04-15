#!/usr/bin/env bash
# Sets up the web servrs for the deployment of web_static

# Install nginx
sudo apt-get update -y
sudo apt-get install nginx -y

# make web directories
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

# Create a test HTML file
echo "<!DOCTYPE html>
<html>
<head>
</head>
<body>
This is a test.
</body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic links
# Create symbolic links
LINK="/data/web_static/current"
if [ -e $LINK ]; then
    sudo rm $LINK
    sudo ln -s /data/web_static/releases/test/ $LINK
else
    sudo ln -s /data/web_static/releases/test/ $LINK
fi

# Create owership
sudo chown -R ubuntu:ubuntu /data

# Update Nginx config to serve content to hbnb_static
ALIAS='location \/hbnb_static\/ {\n                 alias \/data\/web_static\/current\/;\n                 autoindex off;\n         }\n'
sudo sed -i "30i$ALIAS" /etc/nginx/sites-available/default

# restarts nginx server
sudo service nginx restart
