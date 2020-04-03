import crython
import http.server
import socketserver
from datetime import datetime, timedelta

import subprocess


SCRIPT_ON = "./scripts/on.sh"
SCRIPT_OFF = "./scripts/off.sh"
SCRIPT_VOLUME_DOWN = "./scripts/volumeDown.sh"
SCRIPT_VOLUME_UP = "./scripts/volumeUp.sh"
SCRIPT_CHECK_PLAYING = "./scripts/checkPlaying.sh"
PORT = 8080

TIMEOUT_POWEROFF_SECONDS = 60

currently_playing = False
last_playing_stop = None


def execute_bash(bash_string):
    try:
        subprocess.call(['bash', bash_string])
    except e as Exception:
        print(f'Could not execute script {bash_string}!')
        print(e)


class OldRemoteHandler(http.server.BaseHTTPRequestHandler):
    def send_ok(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        if self.path == "/volumeUp":
            execute_bash(SCRIPT_VOLUME_UP)
            self.send_ok()
        if self.path == "/volumeDown":
            execute_bash(SCRIPT_VOLUME_DOWN)
            self.send_ok()
        if self.path == "/powerOn":
            execute_bash(SCRIPT_ON)
            self.send_ok()
        if self.path == "/powerOff":
            execute_bash(SCRIPT_OFF)
            self.send_ok()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()


def bash_is_audio_playing():
    cmd = ['bash', SCRIPT_CHECK_PLAYING]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    print("starting")
    o, e = proc.communicate(timeout=5)
    print("done")

    output = o.decode('ascii').strip()
    error = e.decode('ascii').strip()

    if output == "0":
        return False
    elif output == "1":
        return True
    else:
        raise Exception("Did not receive valid output. STDERR: " + error)


@crython.job(second=range(0, 60, 5))
def check_is_playing():
    global currently_playing
    global last_playing_stop

    try:
        result = bash_is_audio_playing()

        if result and not currently_playing:
            execute_bash(SCRIPT_ON)
            currently_playing = True
            last_playing_stop = None
        elif not result and currently_playing:
            currently_playing = False
            last_playing_stop = datetime.now()
        elif not currently_playing and last_playing_stop:
            delta = datetime.now() - last_playing_stop
            if delta.total_seconds() > TIMEOUT_POWEROFF_SECONDS:
                execute_bash(SCRIPT_OFF)

    except e as Exception:
        print('Could not check for playing state!')
        print(e)


def main():
    httpd = socketserver.TCPServer(('', PORT), OldRemoteHandler)

    crython.start()
    httpd.serve_forever()


main()
