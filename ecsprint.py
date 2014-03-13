#! /usr/bin/env python
from __future__ import print_function
import os
import sys
import subprocess
import argparse
import shlex
import pipes
import paramiko

# Python 3|2
try:
    quote = shlex.quote
except AttributeError:
    quote = pipes.quote

parser = argparse.ArgumentParser(description="Print on ECS printers")
parser.add_argument('-P', metavar="PRINTER", default="mfp0hdup", help="Printer name. Eg mfp0 or tp1hdup")
parser.add_argument('host', default="ecs.ox.ac.uk", help="Host. Eg m10es@ecs.ox.ac.uk")
parser.add_argument('files', default=[], nargs="+", help="File-names of files to be printed")
parser.add_argument('-c', metavar="COMMAND", default="lpr", help="Print command.")
parser.add_argument('--dryrun', action='store_true', help="Do not print.")
parser.add_argument('-args', help="Print args.")
parser.add_argument('-v', action="store_true", help="Verbose.")

args = parser.parse_args()
files = args.files

if args.v:
    print("Files: " + ", ".join(files))

# eg m10es@ecs.ox.ac.uk
userhost = args.host.split('@', 1)
if len(userhost)==1:
    user=None
    host=userhost[1].strip()
else:
    user = userhost[0].strip()
    host = (userhost[1] or "ecs.ox.ac.uk").strip()

if args.v:
    print("Connecting to %s@%s" % (user, host))

# Printer name. Default is mfp0 horizontal duplex. This is near the ug social area. You might want tp1hdup
printer = args.P

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.connect(host, username=user)

# Create a folder in /tmp (or wherever the system thinks is appropriate
# GNU style on the left, BSD style on the right. If GNU exits with 1, use BSD.
tmpdir_proc = "mktemp -d --suff .ecsprint || mktemp -d -t .ecsprint"

# Create the directory on the server. Get its location. Strip the newline at the end.
_, tmpdirOUT, tmpdirERR = ssh.exec_command(tmpdir_proc)
tmpdir = tmpdirOUT.readlines()[0].strip() + "/"

#Rsync! Whole files only. Relative mode. Set permissions so only we can read it. Output the file locations for printing.
rsync_args = ['rsync', '-WR', '--chmod=ugo-rwx,u+rw', '--out-format=%n'] + files + ['%s@%s:%s' % (user, host, tmpdir)]
rsync_output = subprocess.check_output(rsync_args)

# server_files lists all of the files on the server.
# Rsync lists directories as well as files. Lets filter them out.
server_files = list(map(lambda str: tmpdir+str , filter(lambda str: str[-1]!='/', rsync_output.decode("utf-8").split())))

if not args.dryrun:
    print_args = " ".join([args.c] + shlex.split(args.args) + ["-P %s" % printer] + server_files)
    if args.v:
        print(print_args)
    _, printout, printerr = ssh.exec_command(print_args)
    print(printout.read())
    print(printerr.read(), file=sys.stderr)

# Remove the temporary folder. I feel uneasy about this line.
rmtmp_proc = "rm -rf " + quote(tmpdir)
ssh.exec_command(rmtmp_proc)

ssh.close()