## Old stereo remote

This project is intended to modernize my old Philips stereo, but it should work
with other brands as well.

### Hardware

The basic idea is to use a raspberry pi zero W and attach an IR led and a
raspiaudio module to it. Using "raspotify" the raspberry turns into a Spotify
Connect client. Via lirc I can control the IR led and thus control the stereo.

### Software

I want the raspberry to control the stereo in a way with the least interaction
possible. As soon as the raspberry pi notices that music is played it should
turn on the stereo. When there is no music playing anymore I want it to power
off the stereo (after a delay). Via an HTTP backend I want to be able to control
the volume but also be able to manually turn the stereo on and off.

Features summarized:

- Turning the stereo automatically on when music is played
- Turning the stereo off after 5 minutes when there was no music
- Music will be streamed using raspotify as Spotify Connect client
- Controlling the stereo via IR
- HTTP Backend:

  - Volume up / down
  - Power On / Off

### Setup

Some things need to be done beforehand

#### Raspbian

Setup your Raspberry Pi, preferrably with Raspbian

#### Raspiaudio

Get yourself some audio output. I used the Raspiaudio shield. Set it up and make
sure it's working. One more note: It should be using alsamixer, I'm not sure
whether the audio recognition works oterwise.

#### Raspotify

If you go to the raspotify repository you'll find a How-To on how to install
raspotify. Get it working and test it!

#### LIRC

This is a tricky one... You need to get LIRC working and be able to send
commands via "irsend" command line tool. One tip ahead: There are thousands of
configuration already. You don't necessarily need to attach a receiver and map
your remote. If you do, you don't need to get the receiver working which is a
pain in the ... I tried for hours until I realized that **you cannot use the IR
receiver and the sending IR led at the same time**.

You need four IR commands for the to use this:

- Turning your stereo ON
- Turning your stereo OFF
- Volume up
- Volume down

Prepare bash scripts using `irsend` for sending those commands. These can later
be easily integrated into the application.
