from django.shortcuts import render, HttpResponse
import numpy as np
from scipy.io import wavfile
from voiceprint.models import AudioModel
import json
import os
from voiceprint.predict import verify
import logging


# Create your views here.


def test(request):
    return render(request, 'test.html')


def index(request):
    waves = AudioModel.objects.all()
    return render(request, 'index.html', {"waves": waves})


def upload(request):
    if request.method == "POST":
        ID = str(request.POST['ID'])
        # if ID:

        if request.FILES['audioData']:
            strData = request.FILES['audioData'].read()
            wave_data = np.fromstring(strData[44:], dtype=np.int16)
            # # TODO 压缩为vector存入redis
            # if db.set(ID, wave_data):
            #     print("success")
            filename = "%s.wav" % ID
            wavfile.write(os.path.join("wav", filename), 8000, wave_data)
            curdir = os.path.abspath(os.curdir)
            filepath = os.path.join(curdir, "wav", filename)
            if os.path.exists(filepath):
                try:
                    if AudioModel.objects.get(aid=ID):
                        AudioModel.objects.filter(aid=ID).update(name=filename)
                        logging.info('%s已存在，更新成功' % ID)
                except Exception as e:
                    logging.info("异常信息为：%s" % e)
                    AudioModel.objects.create(aid=ID, name=filename)
                    logging.info('%s保存成功' % ID)

            waves = AudioModel.objects.all()
    return render(request, 'index.html', {"waves": waves})


def authenticate(request):
    if request.method == 'POST':
        aids = request.POST.getlist("audioFiles[]")
        filenames = []
        for aid in aids:
            curdir = os.path.abspath(os.curdir)
            filename = AudioModel.objects.get(aid=aid).name
            filenames.append(os.path.join(curdir, "wav", filename))
    # 身份认证
    result = verify(filenames)
    resp = {'status': 100, 'result': '%s和%s的相似度为：%.4f' % (*aids, result)}
    logging.info('%s和%s的相似度为：%.4f' % (*aids, result))
    return HttpResponse(json.dumps(resp), content_type="application/json")
