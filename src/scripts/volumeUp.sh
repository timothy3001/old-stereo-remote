#!/usr/bin/env bash

irsend send_start philips_rc282425 KEY_VOLUMEUP
sleep 3
irsend send_stop philips_rc282425 KEY_VOLUMEUP