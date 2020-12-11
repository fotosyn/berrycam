

# BerryCam Support

### Steps to get BerryCam up and running on your Raspberry Pi and iOS device 

### Preparation : 
[1. What you need](#items-you-will-need) / [2. Getting started](#useful-guides-to-get-started)  / [3. Camera set-up](#setting-up-the-camera)
### Capturing images : 
[4. The BerryCam script](#installing-and-running-the-berrycam-script) / [5. Using the BerryCam app](#using-the-berrycam-app-to-capture-images) / [6. Troubleshooting](#troubleshooting)

---

# Items you will need

It's important that you have the following items to run BerryCam.

1. A Raspberry Pi computer (any model) with WiFi connectivity.
2. An SD card. Most models now take the Micro SD type although some work with standard sized SD cards.
3. All the necessary leads (power supply, HDMI cable, mouse and keyboard, if working from Raspberry Pi OS desktop).
4. A working WiFi connection.
5. A Raspberry Pi camera module (V1, V2, NoIR and HQ Camera all work).
6. An iOS device running iOS 14 (iPhone or iPad).

---

# Useful guides to get started

> Before we get into the detail of setting up and using BerryCam, here are some useful resources. It's worthwhile taking the time to explore these pages as they will help you get your Raspberry Pi up and running for the first time. If you're familiar with all of this you may wish to [skip this part](#setting-up-the-camera)

[Setting up your Raspberry Pi](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up)
Here you’ll learn about your Raspberry Pi, what things you need to use it, and how to set it up.

[Using your Raspberry Pi](https://projects.raspberrypi.org/en/projects/raspberry-pi-using)
Learn about Raspberry Pi OS, included software, and how to adjust some key settings to your needs.

 [Remote access using the Terminal/SSH](https://www.raspberrypi.org/documentation/remote-access/)
It's recommended you take a look at the resources here as you will need to use Terminal and some basic commands to install BerryCam and run the Python script.

[Other Frequently Asked Questions](https://www.raspberrypi.org/documentation/faqs/)
A wide range of information related to the hardware and software to get up and running with the various models of Raspberry Pi

[Back to top](#top)

---

# Setting up the camera
> You will need to physically connect the Raspberry Pi camera module using the supplied ribbon cable. This is generally the same process for all models although the connector may be positioned slightly differently, or in the case of Raspberry Pi Zero, require a different connector ribbon cable. If you've done this already, again you may wish to [skip this part](#installing-and-running-the-berrycam-script)

[Getting started with the Camera Module](https://projects.raspberrypi.org/en/projects/getting-started-with-picamera)
Learn how to connect the Raspberry Pi Camera Module to your Raspberry Pi in preparation for use with BerryCam

[Basic usage of raspistill](https://www.raspberrypi.org/documentation/usage/camera/raspicam/raspistill.md)
BerryCam uses raspistill to capture images on the Raspberry Pi. You won't need this reference guide to use BerryCam yet it is handy if you want to learn more and take things even further. 

[A guide to all the Raspberry Pi camera applications](https://www.raspberrypi.org/documentation/raspbian/applications/camera.md)
This useful reference covers all the commands for the applications provided with the Raspberry Pi. These include **raspistill**, **raspivid**, **raspiyuv** and **raspividyuv**. All applications are driven from the [command line](https://www.raspberrypi.org/documentation/remote-access/).

[Back to top](#top)

---

# Installing and running the BerryCam script

> We will be using the **command line** to set up and run the BerryCam Python script. Be sure to read the guides on the [command line](https://www.raspberrypi.org/documentation/usage/terminal/)

There are two ways we can interact with the Raspberry Pi. The easiest and best documented way to do this is using the Raspberry Pi OS desktop. This requires a display, keyboard and mouse. Start by reading ***using the Raspberry Pi OS desktop*** below

If this isn't possible, you can connect using a [VNC client](https://magpi.raspberrypi.org/articles/vnc-raspberry-pi) or directly using terminal on a Mac or an SSH client like [PuTTy](https://www.putty.org) on a Windows PC. If this is how you need to connect, start with ***using the command line from another machine***

### Using the Raspberry Pi OS desktop

Start LXTerminal on the Raspberry Pi using the icon (a small black window icon with a white arrow) on the top tool bar desktop. You will be presented with a window like this.

![\[Raspberry Pi OS Terminal\]](https://raw.githubusercontent.com/fotosyn/berrycam/master/Assets/raspberry-pi-os-terminal.png)

First of all, we will need to find the IP address of the Raspberry Pi on your network. To do this type in 

```
ifconfig
``` 
and press return. This will return quite a bit of information. the only part you will need is highlighted in light grey (to show you where to look) in the screenshow below.

![\[Raspberry Pi OS Terminal IP Address\]](https://raw.githubusercontent.com/fotosyn/berrycam/master/Assets/raspberry-pi-os-ipaddress.png)

Take a note of this number (IP address) as you will need it later on in the BerryCam app to connect.

### Using the command line from another machine

> **Before you begin** – you will need to know the connected IP address of your Raspberry Pi.  If you can't use the Raspberry Pi OS desktop, you can get this from your broadband router control panel (your provider will have given you this information when it was set up) or if you use a WiFi mesh network like Google WiFi this number (IP address) will be available under Connected Devices in the Google WiFi app. **Take a note of this number (IP address) as you will need it later on in the BerryCam app to connect.**

To connect using a remote command line on a terminal, we need to use a protocol called SSH. You can use Terminal on a Mac (press cmd + space and type 'terminal' to launch this) or  [PuTTy](https://www.putty.org) on a Windows PC.

**When connecting, you'll be using using your Raspberry Pi username and password.**  This is normally `pi`for the username and `raspberry` for the password. It is recommended that you [change this](https://www.raspberrypi.org/documentation/linux/usage/users.md) to something only you know.

Connecting using MacOS Terminal:

![\[MacOS Terminal\]](https://raw.githubusercontent.com/fotosyn/berrycam/master/Assets/macos-terminal.png)

Connecting using PuTTy:

![\[PuTTy Terminal\]](https://raw.githubusercontent.com/fotosyn/berrycam/master/Assets/putty-terminal.jpg)

To connect, enter 

```
ssh pi@YOUR_IP_ADDRESS
``` 
replacing YOUR_IP_ADDRESS with the number you took note of and enter your password when prompted. There will be no typing input when entering the password on some cases, so be sure to focus on entering the right keystrokes.

### Download and install BerryCam onto your Raspberry Pi

First of all make sure you're in the home directory for the user you are logged in as. This will normally be 'pi' and is located `/home/pi/`

You can double check this using the 

```
pwd
``` 
command. If you find you are in a different directory simply use:

```
cd /home/pi
```

or 

```
cd /home/<your-user-name>/
```

Next, we need to clone the BerryCam script into your home folder. Within the terminal, simply type:


```
git clone https://github.com/fotosyn/berrycam.git
```

After some activity, the `berryCam.py` file will be copied onto your Raspberry Pi. This will be in a folder named berrycam. If you receive an error at this point (command not found), you will need to install git which can be done by typing:

```
sudo apt-get update
sudo apt-get install git
```

(Once this is complete, you'll need to repeat the clone step again.)

To check the `berryCam.py` file has been downloaded and unpacked, or set up as a file issue the command:

```
ls
```

This will list files currently in home. You will notice the new folder named berrycam. Change to this directory with:

```
cd berrycam
```

You can now check the required script has been downloaded. In the command line, enter again:

```
ls
```

You will see a number of files and a folder. Amongs these there should be a Python **berryCam.py** file. This is needed to provide the link between the iOS device and the Raspberry Pi.

Check that you have Python 3.7.0 by issuing the command:

```
python3 --version
```

If you have a version lower than this, we recommend you check the [Troubleshooting](#troubleshooting) guide.


###  Running the BerryCam Python script on your Raspberry Pi

BerryCam needs to be run as a Python process to provide the necessary links to allow the BerryCam iOS app to trigger the camera, provide previews and save files. To run simply enter:

```
sudo nohup python3 berryCam.py > berryCam.log & tail -f berryCam.log
```

The Python script will run in the background and you will see the following message:

```
B E R R Y C A M -- Listening on port 8000 
Please ensure your BerryCam App is installed and running on your iOS Device
```

You can close terminal and as long as the Raspberry Pi has power will continue to run BerryCam.

If you experience any problems at this point, please check [Troubleshooting](#troubleshooting)

[Back to top](#top)

---

## Using the BerryCam app to capture images

> Make sure you have downloaded and installed the BerryCam app onto your iOS device, and that both devices are connected on the same local network (generally your cellular connection won't work. Wifi will be easiest). 


[![Download on the App Store](https://raw.githubusercontent.com/fotosyn/berrycam/master/Assets/app-store-badge.png)](https://apps.apple.com/app/berrycam-take-images-with-a-raspberry-pi-camera/id687071023)

To set up the connection on the iOS App, tap the settings button (ellipsis icon), scroll down to **Raspberry Pi Settings**

1. Select the correct version of camera you are using with your Raspberry Pi (this will dictate the output size of the image to be captured)
2. Update your IP address with the one given when you issued the `ifconfig` comnmand
3. Make sure you're using the correct port number. In most cases this will be 8000 and is set to this as default.

Once complete, select **Done** and you will be returned to the main screen. After a brief pause, BerryCam will detect your Raspberry Pi and the capture button will change to green. If this does not happen, check all of the steps above and make sure the IP address entered is correct.

### You can now start capturing images! 

Simply press the large green capture (camera) button. After a short pause, the image will then appear in your iOS device. You can experiment with various capture parameters by revisiting the settings panel and updating. There's no need to worry about losing any captures you make. 

Images are saved locally to the Pi, and can be accessed in any web browser by going back into settings (ellipsis menu) and selecting 'Review images on Raspberry Pi' or entering the address below into a browser on a device on the same local network:

```
http://YOUR_IP_ADDRESS:8000/berrycam/
``` 

You can also save or share the currently captured image directly from the iOS device using the share button. 

BerryCam is a quick and easy way to unlock experimentation with the Raspberry Pi camera modules. Try combinations of image effects, exposure controls and white balance to create some striking photographs!

[Back to top](#top)

---

# Troubleshooting

If you are running an earlier version of Python3, pre version 3.3 then you will encounter a problem with the flush=true parameter in the `berryCam.py` script. 

### Check your version of Python3

To check the version supply the command

```
python3 --version
```

If this returns less than 3.7.0 then there are a few things you can do.


### Things you can do:

**1. Upgrade your Raspberry Pi OS**

You could install a newer version of Raspberry Pi OS which has newer versions of Python. This is definitely the most direct route to consider if you're blowing the dust off a trusty Pi that's been sitting in the cupboard. 

See [Setting up your Raspberry Pi](https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up) to get the latest version of Raspberry Pi OS and flash to your SD card.

**2. Update Python3 to version 3.7.0**

Alternatively, you can update your version of Python3. Be aware that this will a fair amount of time and involves a number of steps that need to be followed in this specific order. To update to the newest version with the following commands:

Download and extract the latest version of Python3 logged in as root

```
sudo su
```
```
cd /usr/src
```
```
wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tgz
```
```
tar -xf Python-3.7.0.tgz
```

Install dependencies

```
apt-get update
```
```
apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev
```

Configure and install Python 3 (this part may take some time)

```
cd Python-3.7.0
```
```
./configure --enable-optimizations
```
```
make altinstall
```

Update the link to the newly installed version of Python

```
ln -s /usr/local/bin/python3.7 /usr/local/bin/python3
```

Check the version of Python (should return 3.7.0)

```
python3 --version
```

Thanks to [Samx18](https://samx18.io/blog/2018/09/05/python3_raspberrypi.html) for the original guide to this detail.

Perform a reboot of the Pi to be doubly sure that this has been applied.

You should then be able to launch BerryCam using the command.:

```
sudo nohup python3 berryCam.py > berryCam.log & tail -f berryCam.log
```


[Back to top](#top)
