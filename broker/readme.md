### Before you run the docker, run this first: 

`docker run --rm -it -v ./config:/mosquitto/config eclipse-mosquitto mosquitto_passwd -c /mosquitto/config/passwords.txt your_username`