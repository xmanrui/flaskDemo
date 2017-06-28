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
imgBase = 'F:/test'
Ipaddress = '127.0.0.1'
video_upload_path = './video_upload'
#recofile = './static/Reco/'str(todays)

global time_data
global pcount
global ptime
time_data = []
pcount = len(os.listdir(imgBase))
ptime = int(round(time.time() * 1000))

def get_head_img(imgDir):
    listname = {}
    traintime = {}
    for name in os.listdir(imgDir):
        imgPath = os.path.join(imgDir, name)
        listf = []
        if os.path.isdir(imgPath):
            for f in os.listdir(imgPath):
                if os.path.isfile(os.path.join(imgPath,f)) and f.lower().endswith(('.png', '.jpg', '.jpeg','.tiff','.tif','.bmp', '.ppm')):
                    filePath = os.path.join(imgPath,f)
                    listf.append(filePath)

            timestamp = os.path.getmtime(imgPath)
            date=datetime.datetime.fromtimestamp(timestamp)
            traintime[name]=date.strftime('%Y-%m-%d %H:%M:%S')

        if len(listf):
            #print name , listf[0]
            listname[name] = listf[0]

    return listname,traintime

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

def get_result_img(imgDir):
    fname = {}
    fnum = {}
    nimglist = {}
    nameinfos = {}
    for name in os.listdir(imgDir):
        imgPath = os.path.join(imgDir, name)

        if os.path.isfile(imgPath):
            continue

        if os.path.isdir(imgPath):
            imglist = []
            dist = {}
            for f in os.listdir(imgPath):

                if os.path.isfile(os.path.join(imgPath,f)) and f.lower().endswith(('.png', '.jpg')):

                    values = int(f[0:1])
                    files = os.path.join(imgPath, f)
                    dist[files] = values
                    imglist.append(files)

                    timetap = f[1:7]
                    location = '1003'
                    confidence = 'C' + f[0:1]
                    data = [timetap, location, confidence]
                    nameinfos.setdefault(name, []).append(data)

            if len(imglist) > 0:
                fname[name] = max(dist.items(), key=lambda x: x[1])[0]
                fnum[name] = len(imglist)
                nimglist[name] = imglist

    nameinfo = {}
    for keys, values in nameinfos.items():
        values.reverse()
        j = 0
        for i in values:
            nameinfo.setdefault(keys, []).append(i)
            j += 1
            if j > 3:
                break

    persons = len(os.listdir(imgBase))

    return fname, fnum, nimglist, nameinfo, nameinfos, persons

def readresulthisinfo(recofile):
    global time_data
    fh = open(recofile,'r')
    nameinfo = {}
    nameinfos = {}
    persons = '0'
    for line in fh.readlines():
        list = line.split(',')
        if len(list) > 3 :
            timetap = list[1]
            location = list[2]
            confidence = list[3]
            if len(list[3]) >= 3:  # c60 -> c6
                confidence = list[3][0:2]
            else:
                confidence = list[3]
            #times = list[4]
            data = (timetap,location,confidence)
            nameinfos.setdefault(list[0],[]).append(data)

            strs = list[4].split('.')[0]
            timetap = string.atoi(strs)
            datatap = int(list[5])
            time_data.append([timetap,datatap])

            persons = list[6].split('.')[0]

    fh.close()

    for keys , values in nameinfos.items():
        values.reverse()
        j = 0
        for i in values:
            nameinfo.setdefault(keys,[]).append(i)
            j += 1
            if j > 3:
                break

    return nameinfo,nameinfos,persons

@app.route('/')
def index():
    global imagepath, resultpath
    headerimg, trainintime = get_head_img(imagepath)
    persons = len(os.listdir(imgBase))
    return render_template('index_face.html', headerimg=headerimg, persons=persons)

def get_confidence(imgfilename):
    """
    1003_c60.jpg -> c6
    """
    if not imgfilename:
        return ''

    return 'c' + imgfilename.split('/')[-1][0:1]

@app.route('/updateRecoResultData')
def updateData():
    global imagepath , resultpath
    headerimg, trainintime = get_head_img(imagepath)
    resultimg = get_result_img(resultpath)

    totalResult = {}

    if resultimg:
        for k, v in resultimg[0].items():
            destImgsTemp = []
            allInfo = {'oneDestImg': '', 'destImgCount': 0, 'trainTime': '', 'destImgs': [], 'resultLog': [], 'nameLog': []}
            allInfo['oneDestImg'] = v
            if k in resultimg[1]:
                allInfo['destImgCount'] = resultimg[1][k]
            if k in trainintime:
                allInfo['trainTime'] = trainintime[k]
            if k in resultimg[2]:
                destImgsTemp = resultimg[2][k]

            allInfo['resultLog'] = resultimg[3][k]
            allInfo['nameLog'] = resultimg[4][k]

            destImgs = []
            for item in destImgsTemp:
                itemDict = {'imgSrc': '', 'confidence': ''}
                itemDict['imgSrc'] = item
                itemDict['confidence'] = 'c' + item.split('/')[-1][0:1]
                destImgs.append(itemDict)

            allInfo['destImgs'] = destImgs
            totalResult[k] = allInfo

    return jsonify(totalResult)

def get_persons_count(imgBase):
    return len(os.listdir(imgBase))

@app.route('/facesdata')
def data():
    global pcount, ptime
    count = get_persons_count(imgBase)
    dcount = count - pcount
    curr_time = int(round(time.time() * 1000))
    dtime = curr_time - ptime
    pcount = count
    ptime = curr_time
    arr = []
    counts = dcount * 1000 / dtime
    arr.append((curr_time, counts))
    return json.dumps(arr)

@app.route('/personscount')
def facescount():
    count = get_persons_count(imgBase)

    return jsonify(count)

@app.route('/has_newRecord')
def has_newRecord():
    result = False
    guid = request.args.get('datakey')
    recofile = get_recofile(resultpath)
    defaultValue = 'nodata'
    last_timestamp = session.get(guid, defaultValue)
    if last_timestamp == defaultValue:
        timestamp = get_new_timestamp(recofile)
        session[guid] = str(timestamp)
        result = True
    else:
        timestamp = get_new_timestamp(recofile)
        if last_timestamp != str(timestamp):
            session[guid] = str(timestamp)
            result = True
        else:
            result = False
    return jsonify(result)

def get_new_timestamp(recofile):
    newtimestamp = 0
    try:
        with open(recofile, 'r') as fh:
            arr = []
            for line in fh.readlines():
                splitlist = line.split(',')
                if len(splitlist) > 3:
                    strs = splitlist[4].split('.')[0]
                    timestamp = string.atoi(strs)
                    timestamp = timestamp * 1000
                    arr.append(timestamp)
            if len(arr) > 0:
                newtimestamp = arr[-1]

    except IOError:
        newtimestamp = 0
        print 'IOError'

    return newtimestamp
    
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
    app.run(Ipaddress, port=8000)
    #socketio.run(app)
    # app.run()
    # app.run(threaded=True)

