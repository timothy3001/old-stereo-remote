#!/usr/bin/env bash

irsend send_start philips_rc282425 KEY_AUX
sleep 8
irsend send_stop philips_rc282425 KEY_AUX
sleep 2
irsend send_start philips_rc282425 KEY_AUX
sleep 8
irsend send_stop philips_rc282425 KEY_AUX