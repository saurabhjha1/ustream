#!/usr/bin/python3 
import os
import sys
import subprocess as subp
import logging 
from flask import Flask, redirect, url_for, request, render_template, send_from_directory
import json

app = Flask(__name__, template_folder="web/")

def parse_config():
    fname = os.path.realpath(os.path.dirname(__file__)) + os.sep + "config.json"
    config = json.load(open(fname, 'r'))
    return config


logging.basicConfig(filename="/tmp/ustream",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


def persist_state(state):
    if state == "run":
        f = open("/tmp/zoom.run", 'w')
        os.sync()
        f.close()
    elif state == "stop":
        os.remove("/tmp/zoom.run")

def is_running():
    if os.path.exists("/tmp/zoom.run"):
        return True
    else:
        return False


@app.route("/", methods=['GET', 'POST'])
def index():
    config = parse_config()
    meetingId = config['id']
    meeting = f"https://zoom.us/j/{meetingId}"
    msg = ""
    status = 200
    if request.method == 'POST':
        if request.form.get('action1'):
            msg, status = launch_zoom()
            
        elif  request.form.get('action2'):
            msg, status = stop_zoom()
        return render_template('index.html', msg=msg, meeting=meeting)
    elif request.method == 'GET':
        if is_running():
            msg, status = "zoom is running", 200
        else:
            msg, status = "zoom is not running", 200
        return render_template('index.html', msg=msg, meeting=meeting)
    
    return render_template("index.html")

@app.route('/start')
def launch_zoom():
    logging.info("launching zoom")
    if is_running() == False:
        config = parse_config()
        logging.info(config)
        meetingId = config['id']
        meetingPass = config['pass']
        logging.info("zoom is currently not running")
        zoom = subp.run(["xdg-open", f"zoommtg://zoom.us/join?action=join&confno={meetingId}&pwd={meetingPass}"])

        if zoom.returncode == 0:
            persist_state("run")
            return "success", 200
        else:
            return "could not launch", 404
    else:
        return "already running", 200


@app.route('/stop')
def stop_zoom():
    if is_running() == True:
        zkill = subp.run(["killall", "zoom"], capture_output=True)
        status = str(zkill).strip()
        logging.info(status)
        if zkill.returncode == 1:
            if "no process" in status:
                persist_state("stop")
                return "zoom already stop deleting state", 200
            else:
                return "failed to stop zoom", 200
        elif zkill.returncode == 0:
            persist_state("stop")
            return "stopped zoom", 200
    else:
        return "zoom is not running", 200

@app.route('/fav.png')
def favicon():
    logging.info(app.root_path)
    return send_from_directory(os.path.join(app.root_path, 'web'), 'fav.png')

if __name__ == '__main__':
    logging.info("started the app")
    app.run(debug = True, host='0.0.0.0',  port=4040)
