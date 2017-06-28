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
from custom_log import SettingLogSingleton


#todays = datetime.date.today().strftime('%Y%m%d')
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = os.urandom(24)
Session(app)

#socketio = SocketIO(app)

imagepath = './static/trainer'
resultpath = './static/Reco'
Ipaddress = '192.168.1.101'
video_upload_path = './video_upload'
#recofile = './static/Reco/'str(todays)

global time_data
time_data = []

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
    for name in os.listdir(imgDir):
        imgPath = os.path.join(imgDir, name)

        if os.path.isfile(imgPath):
            continue

        if os.path.isdir(imgPath):
            imglist = []
            dist = {}
            for f in os.listdir(imgPath):

                if os.path.isfile(os.path.join(imgPath,f)) and f.lower().endswith(('.png', '.jpg')):
                    names,values = f.split('_')
                    values = int(values[1:2])
                    files = os.path.join(imgPath,f)
                    dist[files] = values
                    imglist.append(files)

            if len(imglist) > 0:
                fname[name] = max(dist.items(), key=lambda x: x[1])[0]
                fnum[name] = len(imglist)
                nimglist[name] = imglist

    return fname,fnum,nimglist

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
    resultimg = get_result_img(resultpath)
    recofile = get_recofile(resultpath)
    resultinfo, namelog, persons = readresulthisinfo(recofile)

    return render_template('index_car.html', headerimg=headerimg, persons=persons)

def get_confidence(imgfilename):
    """
    1003_c60.jpg -> c6
    """
    if not imgfilename:
        return ''

    confidence = ''
    path, filename = os.path.split(imgfilename)
    valueList = filename.split('.')
    try:
        valueList = valueList[0].split('_')
    except IndexError:
        return confidence

    try:
        confidence = valueList[1][0:2]
    except IndexError:
        confidence = ''

    return confidence

@app.route('/updateRecoResultData')
def updateData():
    global imagepath , resultpath
    headerimg, trainintime = get_head_img(imagepath)
    resultimg = get_result_img(resultpath)
    recofile = get_recofile(resultpath)
    resultinfo, namelog, persons = readresulthisinfo(recofile)

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
            if k in resultinfo:
                allInfo['resultLog'] = resultinfo[k]
            if k in namelog:
                allInfo['nameLog'] = namelog[k]

            destImgs = []
            for item in destImgsTemp:
                itemDict = {'imgSrc': '', 'confidence': ''}
                itemDict['imgSrc'] = item
                itemDict['confidence'] = get_confidence(item)
                destImgs.append(itemDict)

            allInfo['destImgs'] = destImgs
            totalResult[k] = allInfo

    return jsonify(totalResult)

def get_persons_count(recordlogfile):
    count = 0
    try:
        with open(recordlogfile, 'r') as fh:
            count = len(fh.readlines())
    except IOError:
        count = 0
    return count

@app.route('/facesdata')
def data():
    recordlogfile = get_recofile(resultpath)
    count = get_persons_count(recordlogfile)
    curr_time = int(round(time.time() * 1000))
    arr = []
    arr.append((curr_time, count))
    return json.dumps(arr)

@app.route('/personscount')
def facescount():
    recordlogfile = get_recofile(resultpath)
    count = get_persons_count(recordlogfile)

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
        
        #if count > 0:
            #command = "python /home/lurx/facedetect/trainFacev1.py --imgDir " + savepath
            #os.system(command)
            
    return render_template('upload.html', result=resutlstr)

@app.route('/start_work')
def start_work():
    video_name = request.args.get('mydata')
    obj = SettingLogSingleton()
    obj.add_message_to_setting_log('car start_work: ' + video_name)
    print(video_name)
    os.system('sh xstart.sh')
    return 'start work'

@app.route('/end_work')
def end_work():
    video_name = request.args.get('mydata')
    obj = SettingLogSingleton()
    obj.add_message_to_setting_log('car end_work: ' + video_name)
    print(video_name)
    os.system('sh xend.sh')
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
    # app.run(Ipaddress, port=8000,threaded=True)
    #socketio.run(app)
    app.run()
    #app.run(threaded=True)

