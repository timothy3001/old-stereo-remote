import crython
import http.server
import socketserver
from datetime import datetime, timedelta
import sys
import errno

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

    def log_message(self, format, *args):
        # Disabling annoying log messages
        return

    def do_POST(self):
        try:
            if self.path == "/volumeUp":
                print("HTTP: Turning volume up...")
                execute_bash(SCRIPT_VOLUME_UP)
                print("HTTP: Volume turned up!")
                self.send_ok()
            if self.path == "/volumeDown":
                print("HTTP: Turning volume down...")
                execute_bash(SCRIPT_VOLUME_DOWN)
                print("HTTP: Volume turned down!")
                self.send_ok()
            if self.path == "/powerOn":
                print("HTTP: Turning stereo on...")
                execute_bash(SCRIPT_ON)
                print("HTTP: Stereo turned on!")
                self.send_ok()
            if self.path == "/powerOff":
                print("HTTP: Turning stereo off...")
                execute_bash(SCRIPT_OFF)
                print("HTTP: Stereo turned off!")
                self.send_ok()
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
        except IOError as e:
            if e.errno == errno.EPIPE:
                pass
            else:
                raise


def bash_is_audio_playing():
    cmd = ['bash', SCRIPT_CHECK_PLAYING]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)

    o, e = proc.communicate(timeout=5)

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
            if last_playing_stop:
                print("Resumed playback...")
            else:
                print("Turning stereo on...")
                execute_bash(SCRIPT_ON)
                print("Stereo turned on!")
            currently_playing = True
            last_playing_stop = None
        elif not result and currently_playing:
            print("Playback stopping...")
            currently_playing = False
            last_playing_stop = datetime.now()
            print(f"Playback stopped at {last_playing_stop}!")
        elif not currently_playing and last_playing_stop:
            delta = datetime.now() - last_playing_stop
            if delta.total_seconds() > TIMEOUT_POWEROFF_SECONDS:
                print("Turning stereo off...")
                execute_bash(SCRIPT_OFF)
                last_playing_stop = None
                print("Stereo turned off!")

    except e as Exception:
        print('Could not check for playing state!')
        print(e)


def main():
    httpd = socketserver.TCPServer(('', PORT), OldRemoteHandler)

    crython.start()
    httpd.serve_forever()


main()
