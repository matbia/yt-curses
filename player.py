from subprocess import Popen
from os import path

mpv_log_path = path.join(path.dirname(__file__), 'mpv.log')
mpv_no_video_proc = None #mpv --no-video instance

#Creates a new mpv instance and plays the video with given ID
def play_video(id):
    with open(mpv_log_path, 'a') as logfile:
        Popen(['mpv', 'https://youtu.be/' + id, '--msg-level=all=warn,ao/alsa=error'], stdout=logfile, stderr=logfile)

#Plays audio from video with given ID and returns true, or terminates exisiting mpv --no-video instance and returns false
def toggle_play_audio(id):
    global mpv_no_video_proc
    if mpv_no_video_proc:
        mpv_no_video_proc.terminate()
        mpv_no_video_proc = None
        return False
    else:
        with open(mpv_log_path, 'a') as logfile:
            mpv_no_video_proc = Popen(['mpv', 'https://youtu.be/' + id, '--no-video', '--msg-level=all=warn,ao/alsa=error'], stdout=logfile, stderr=logfile)
        return True

def cleanup():
    if mpv_no_video_proc:
        mpv_no_video_proc.terminate()
