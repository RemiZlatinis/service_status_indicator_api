#!/bin/bash

# This is the simplest possible example of a checking script.

# This line simulates a checking script can take a while to be executed.
sleep 60

# [IMPORTANT!] 
# Note that a service script must echo one of
# ['ok' | 'update' | 'warning' | 'failure']
# these texts are the values that represent the service status. 
echo 'ok' 