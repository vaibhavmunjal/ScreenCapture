from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.views.decorators import gzip
from django.contrib.staticfiles.templatetags.staticfiles import static

import cv2
import numpy
from PIL import ImageGrab
import json

from .utils import welcome_img, err_img, start_clip, end_event

import os
import sys

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'captured', 'output.avi')

status = None


def index(request):
    return render(request, "screen/index.html")


def stop_screen(request, method=["POST"]):
    global status
    request_status = request.body.decode('utf-8')
    screen_status = json.loads(request_status)
    status = screen_status['status']
    if status == 'stop':
        status = 'end'
        screen = {'status':'stopped'}
        return JsonResponse(screen)
    screen = {'status':'still recording'}
    return JsonResponse(screen)


def start_screen(request, method=["POST"]):
    global status
    request_status = request.body.decode('utf-8')
    screen_status = json.loads(request_status)
    status = screen_status['status']
    print('status == ' + status)
    screen = {'status': 'stream_started'}
    return JsonResponse(screen)


def end_stream(request):
    global status
    if not status:
        return HttpResponse(welcome_img(),
                            content_type='multipart/x-mixed-replace; boundary=frame')

    elif status == 'end':
        status = None
        return HttpResponse(end_event(),
                            content_type='multipart/x-mixed-replace; boundary=frame')



def stream_screen(request):
    return StreamingHttpResponse(stream_scrn(),
            content_type='multipart/x-mixed-replace; boundary=frame')


def stream_scrn():
    global status
    print(status)
    fourcc = cv2.VideoWriter_fourcc(*'MPEG')
    out = cv2.VideoWriter(OUTPUT_DIR, fourcc, 20, (1366, 768))

    while status == 'start':
        img = ImageGrab.grab()
        np_img = numpy.array(img)
        frame = cv2.cvtColor(np_img, cv2.COLOR_BGR2RGB)
        out.write(frame)
        ret, jpeg = cv2.imencode('.jpg', frame)
        if ret:
            byte_data = jpeg.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + byte_data + b'\r\n\r\n')
    else:
        if status == 'stop':
            out.release()
            cv2.destroyAllWindows()
            end_event()
    if status == 'stop':
            out.release()
            cv2.destroyAllWindows()
            err_img()
    end_event()
