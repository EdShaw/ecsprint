ecsprint
========

Print from your machine on the CS department printers. 

Eg:
```
> ecsprint.py m10es@ecs.ox.ac.uk -P mfp0hdup  file1.txt file2.pdf file3.c
```

Dependencies:
-------------

* [ssh key login](https://help.ubuntu.com/community/SSH/OpenSSH/Keys "Guide")
* python2.x
* paramiko:
``` 
pip install paramiko 
```

Python 3+ support to come with paramiko...


```
Help:

usage: ecsprint.py [-h] [-P PRINTER] [-c COMMAND] [--dryrun] [-args ARGS] [-v]
                   host files [files ...]

Print on ECS printers

positional arguments:
  host        Host. Eg m10es@ecs.ox.ac.uk
  files       File-names of files to be printed

optional arguments:
  -h, --help  show this help message and exit
  -P PRINTER  Printer name. Eg mfp0 or tp1hdup
  -c COMMAND  Print command.
  --dryrun    Do not print.
  -args ARGS  Print args.
  -v          Verbose.
```
