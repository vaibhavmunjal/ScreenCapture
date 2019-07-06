import os
import sys

PREVIEW_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'preview')

print(PREVIEW_DIR)
def welcome_img():
    wel_img = os.path.join(PREVIEW_DIR, 'welcome.png')
    welcome_frame = open(wel_img, 'rb').read()
    yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + welcome_frame + b'\r\n\r\n')


def err_img():
    err_img = os.path.join(PREVIEW_DIR, 'err.png')
    err_frame = open(err_img + "326.gif", 'rb').read()
    yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + err_frame + b'\r\n\r\n')


def start_clip():
    start_frames = [open(os.path.join(PREVIEW_DIR, clip) + '.png', 'rb').read() for clip in ['3', '2', '1']]
    print(start_frames)
    for start_frame in start_frames:
        print(start_frame)
        yield (b'--frame\r\n'
                b'Content-Type: image/png\r\n\r\n' + start_frame + b'\r\n\r\n')


def end_event():
    end_img = os.path.join(PREVIEW_DIR, 'end.png')
    end_frame = open(end_img, 'rb').read()
    yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + end_frame + b'\r\n\r\n')
