if grep -q RUNNING /proc/asound/card*/*p/*/status 2>&1; then
   echo 1
else
   echo 0
fi