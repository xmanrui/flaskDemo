# -*- coding: UTF-8 -*-

import os, datetime
import os.path
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from flask import jsonify
import time
import random
from flask import session
from flask_session import Session
import json
import string
import tool

#todays = datetime.date.today().strftime('%Y%m%d')
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
Session(app)

imagepath = './static/trainer'
resultpath = './static/Recoraw'
imgBase = '/home/lurx/facedetect/put'
Ipaddress = '192.168.91.1'
video_upload_path = './video_upload'
#recofile = './static/Reco/'str(todays)

def get_recofile(logfileDir):
    recofile = []
    for name in os.listdir(logfileDir):
        logfilepath = os.path.join(logfileDir, name)
        if os.path.isfile(logfilepath) and name.lower().endswith(('.log',)):
            recofile.append(name)
            continue
    recofile.sort(reverse=True)
    theFile = ""
    try:
        theFile = recofile[0]
    except IndexError:
        theFile = ""
    recofilepath = os.path.join(logfileDir, theFile)

    return recofilepath

@app.route('/')
def index():
    return render_template('index_speed.html')

def get_car_info_from_line(linestr):
    # speed: (time, speedvalue), carcount, showindex, type
    data = {'speed': [0, 0], 'count': 0, 'showindex': 0, 'type': 0}
    linestr = linestr.rstrip()
    linestr = linestr.rstrip(',')
    strsplit = linestr.split(',')
    if len(strsplit) == 3:
        data['speed'][0] = float(strsplit[0]) * 1000
        data['speed'][1] = int(float(strsplit[1]))
        data['count'] = int(strsplit[2])

    return data


def get_last_car_info(infofile):
    info = {}
    try:
        with open(infofile, 'r') as fh:
            lines = fh.readlines()
            if len(lines) > 0:
                lastline = lines[-1]
                info = get_car_info_from_line(lastline)
                info['showindex'] = len(lines) - 1
    except IOError:
        pass

    return info

def get_car_info(infofile, showindex):
    # time, speed, carcount, showindex
    info = []

    if showindex == 0:
        data = get_last_car_info(infofile)
        if len(data) > 0:
            info.append(data)
        return info

    lines = []
    try:
        with open(infofile, 'r') as fh:
            lines = fh.readlines()
    except IOError:
        pass

    if len(lines) - 1 > showindex:
        offset = showindex + 1
        lines = lines[offset:]

        for i, line in enumerate(lines):
            data = get_car_info_from_line(line)
            if len(data):
                data['showindex'] = offset + i
                info.append(data)
    return info

@app.route('/speed')
def data():
    showindex = request.args.get('showindex')
    showindex = int(showindex)
    print showindex
    car_info_log = get_recofile(resultpath)
    info = get_car_info(car_info_log, showindex)
    print info
    return json.dumps(info)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    resutlstr = ''
    if request.method == 'POST':
        username = request.form['username']
        savepath = os.path.join(imagepath, username)
        if not os.path.exists(savepath):
            os.makedirs(savepath)

        outputpath = os.path.join(resultpath, username)
        if not os.path.exists(outputpath):
            os.makedirs(outputpath)

        files = request.files.getlist('img')
        count = 0
        for item in files:
            if item:
                filename = secure_filename(item.filename)
                item.save(os.path.join(savepath, filename))
                resutlstr = 'Upload successful.'
                count += 1
        if count == 0:
           resutlstr = 'Please select image!!!'

        if count > 0:
            command = "python /home/lurx/facedetect/trainFacev2t.py --name " + username + "  --imgDir " + savepath
            if os.system(command) == 0:
                resutlstr = resutlstr + ' Training complete!'

    return render_template('upload.html', result=resutlstr)

@app.route('/start_work')
def start_work():
    mpath = request.args.get('mydata')
    mpath = os.path.join(video_upload_path, mpath)
    print(mpath)
    command = "python /home/lurx/facedetect/facedetectionv6t.py " + mpath
    os.system(command)
    return 'start work'

@app.route('/end_work')
def end_work():
    test = request.args.get('mydata')
    print(test)
    cmd = "ps -elf|grep 'facedetectionv6t.py'|grep -v grep|awk '{print $4}'|xargs kill -9"
    os.system(cmd)
    return 'end work'

@app.route('/get_video_src')
def get_video_src():
    local_list = tool.get_filename_from_dir(video_upload_path)
    mydata = request.args.get('mydata')
    origin_mydata = mydata.split(',')
    diff_set = set(local_list) - set(origin_mydata)  #  找出新的视频项
    video_list = list(diff_set)
    return jsonify(video_list)

@app.route('/multi_upload', methods=['GET', 'POST'])
def multi_upload():
    if request.method == 'POST':
        """Handle the upload of a file."""
        form = request.form
        # 这里获取绝对路径
        abpath = os.path.abspath(video_upload_path)
        tool.make_dir(abpath)

        for item in request.files.getlist("file"):
            filename = item.filename.rsplit("/")[0]
            # filename = secure_filename(item.filename) # 中文会有问题
            destination = "/".join([abpath, filename])
            print "Accept incoming file:", filename
            print "Save it to:", destination
            item.save(destination)

        return jsonify(status='ok', msg='OVER')
    else:
        return render_template('multi_upload.html')

@app.route('/clear_work')
def clear_work():
    test = request.args.get('mydata')
    print 'clear_work:', test
    return 'clear work'

@app.route('/poweroff')
def poweroff():
    print 'poweroff'
    return 'poweroff'

if __name__ == '__main__':
    #app.run(Ipaddress, port=8000,threaded=True)
    #socketio.run(app)
    # app.run()
    app.run()

