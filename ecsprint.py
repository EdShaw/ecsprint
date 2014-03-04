#! /usr/local/bin/python3
import os
import sys
import subprocess

if len(sys.argv) == 3:
    file = sys.argv[1]
    # eg m10es@ecs.ox.ac.uk
    host = sys.argv[2]

    success = os.system('scp "%s" %s:%s' % (file, host, "~/ecs-print-payload"))

    # ssh -t -t to force allocate pseudo-terminal - See ssh man line 329
    ssh = subprocess.Popen(['ssh', host], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    output = ssh.communicate(bytes("lpr -P mfp0 ~/ecs-print-payload\n", "ascii"))

    # TODO: rm payload

    print(output[0].decode("utf-8"))
    if output[1]:
        print(output[1].decode("utf-8"))

else:
    #Todo
    print ("Usage here")
