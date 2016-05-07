#!/bin/bash
echo '*** ' $1 >> AP_signal.txt
airport eth0 -s >> AP_signal.txt
