ustream
===
The idea of ustream is to stream yourself on to a remote computer from any camera-enabled device on the internet to the remote computer with a display. In simple words, I want to create a video conferencing tool with the ability to (i) initiate the connection from my personal device such as phone,  and (ii) accept the connection on the remote computer. 

My usecase is simple: I am parent of two talking birds ([Indian ring necks](https://en.wikipedia.org/wiki/Rose-ringed_parakeet)) who mostly talk gibberish but it is important for them to socialize with me and my wife. It is difficult (not impossible) to train them to pick my call (or call me). Therefore, I needed to build an app that will help me establish the call without their intervention.   

I had three basic requirements while creating this mini app. 
* ability to stream myself from anywhere in the world (i.e., should be able to leverage internet to establish connection.)
* ability to use my phone to establish the connection as that is the only device I never forget to carry.
* use existing free teleconferencing software such as zoom, skype, hangouts (or whatever Google is calling their video conferencing tool these days). This will ensure small code base and ability to quickly adapt code if needed. I created this app in less than an hour just before an upcoming vacation. 

### How does it work
---
I am using zoom as a teleconferencing software. 
I wanted to create a quick connection (involving as few clicks as possible) which meant removing the need to insert any meeting details on the remote zoom instance. Thus, as of now, whenever I go for vacation, I precreate a zoom meeting and store the details on the remote machine (or update it via ssh if needed).

There are two devices involved: (i) remote computer at home which my birds are going to use, and (ii) personal device with me (e.g., my phone).

* On remote computer, we run a webserver (as a start-up application that starts with the machine). This webserver launches zoom app and joins the conference call upon receiving the start request (http://\<server\>:\<port\>/start), and ends the call upon receiving the stop request (http://\<server\>:\<port\>/stop). 

* On personal device, I can simply join the conference call. 

Ofcourse, I had to enable some default settings to make this resilient and autonomous:
* Launch the webserver as soon as the user logs in (a start-up application on ubuntu.) One could also launch this as cronjob/daemon, however, it is a bit tricky to do that as zoom requires Xserver already running. I decided not to do that as it would have complicated the setting.
* Auto login the user that launches the `ustream` webserver. 
* Auto restart the remote machine if it crashes. I have a powerful server that comes with such features. You can buy watchdogs to enable this on servers that does not have such a feature. 

Note
==
Launching the webserver and exposing your ip/port without proper authentication on the internet can be dangerous (and must be avoided at all costs). The future version of this application will natively provide authentication. 
I use a proxy server to enable secure access and prevent attacks. I am omitting these details here but may decide to write a blog in future showing the steps. 