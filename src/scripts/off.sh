#!/usr/bin/env bash

irsend send_start philips_rc282425 aux-power
sleep 1
irsend send_stop philips_rc282425 aux-power