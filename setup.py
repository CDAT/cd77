from __future__ import print_function
from distutils.core import setup
import glob,subprocess

p = subprocess.Popen(("git","describe","--tags"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
try:
  descr = p.stdout.readlines()[0].strip()
  Version = "-".join(descr.split("-")[:-2])
  if Version == "":
    Version = descr
except:
  Version = "1.0"
  descr = Version

p = subprocess.Popen(("git","log","-n1","--pretty=short"),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
try:
  commit = p.stdout.readlines()[0].split()[1]
except:
  commit = ""
f = open("version.py","w")
print("__version__ = '%s'" % Version, file=f)
print("__git_tag_describe__ = '%s'" % descr, file=f)
print("__git_sha1__ = '%s'" % commit, file=f)
f.close()

setup (name         = 'cd77',
       version      = descr,
       author       = 'AIMS/LLNL',
       description  = 'simple command line builder to link fortran to PCMDI tools',
       url          = 'http://github.com/UV-CDAT/cd77',
       packages     = ['cd77'],
       package_dir  = {'cd77': '',
                      },
       scripts      = ['cd77','cd77.py'],
      )
