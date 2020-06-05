#!/usr/bin/env bash

irsend send_start philips_rc282425 aux-power
sleep 8
irsend send_stop philips_rc282425 aux-power
sleep 2
irsend send_start philips_rc282425 aux-power
sleep 8
irsend send_stop philips_rc282425 aux-power