#!/usr/bin/env python

# Compile a Fortran EzGet/LATS/CDMS application

usage = """
cd77 simplifies the process of building FORTRAN EzGet,
  CDMS, and LATS applications.

Usage: cd77.py [-ezget] [-cdms] [-lats] [-verbose] <f77-options>
  -ezget: Compile with the EzGet library
  -cdms: Compile with the CDMS library (DRS emulation)
  -lats: Compile with the LATS library
  -verbose: Print the generated f77 command
  <f77-options>: Options to be passed to f77

Note: Any combination of the options can be specified,
  in any order. -ezget implies -cdms.

Examples:
  cd77 -ezget -o ezsample ezsample.F
  cd77 -lats -verbose -o lats_sample lats_sample.f
"""

# Locations of libraries and include files on the various platforms

ezgetlib = {"irix6" : "-L/pcmdi/ktaylor/pcmdi/util/ezget/Sgi6.2 -lezget",
            "sunos5" : "-L/pcmdi/cirrus/ktaylor/ezget/solaris -lezget",
            "linux2" : "-L/usr/local/lib -lezget"}
cdmsinc = {"irix6" : "-I/usr/local/include -I/usr/local/HDF4.0r2/include",
           "sunos5" : "-I/usr/local/include",
           "linux2" : "-I/usr/local/include"}
cdmslib = {"irix6" : "-L/usr/local/lib -lcdms -lnetcdf -L/usr/local/HDF4.0r2/lib -lmfhdf -ldf -ljpeg -lz -ldrs",
           "sunos5" : "-L/usr/local/lib -lcdms -lmfhdf -ldf -ljpeg -lz -lnetcdf -lnsl -ldrs -lm -lsunmath",
           # "linux2" : "-L/usr/local/lib -lcdms -lnetcdf -lmfhdf -ldf -ljpeg -lz -lmfhdf -ldf -ljpeg -lz -ldrs -lm"
           "linux2" : "-L/usr/local/lib -lcdms -lnetcdf -ldrs -lm"
           }
latsinc = {"irix6" : "-I/usr/local/include",
           "sunos5" : "-I/usr/local/include",
           "linux2" : "-I/usr/local/include"}
latslib = {"irix6" : "-L/usr/local/lib -llats -lnetcdf -lm",
           "sunos5" : "-L/usr/local/lib -llats -lnetcdf -lnsl -lm",
           "linux2" : "-L/usr/local/lib -llats -lnetcdf -lm"}
f77exec = {"irix6" : "f77",
           "sunos5" : "f77",
           "linux2" : "pgf77"}

import sys, os, string

# Get the host type and major operating system version
def getplatform():
    uname = string.split(os.popen("uname -a",'r').readlines()[0])
    ostype = uname[0]
    osmajor = string.split(uname[2],".")[0]
    return string.lower(ostype+osmajor)

def main(argv):
    ezget = 0
    cdms = 0
    lats = 0
    verbose = 0
    includes = ""
    libs = ""
    
    f77opts = "-g"
    
    # Process the options
    for arg in argv[1:]:
        if arg=="-ezget":
            ezget = 1
            cdms = 1
        elif arg=="-cdms":
            cdms = 1
        elif arg=="-lats":
            lats = 1
        elif arg=="-verbose":
            verbose = 1
        else:
            f77opts = f77opts+' '+arg

    # Error if no options are set
    if not (ezget or cdms or lats):
        print usage
        sys.exit(0)

    # Get the platform and include, lib directives
    # for this platform
    platform = getplatform()
    try:
        f77 = f77exec[platform]
        if ezget:
            libs = libs+' '+ezgetlib[platform]
        if cdms:
            includes = includes+' '+cdmsinc[platform]
            libs = libs+' '+cdmslib[platform]
        if lats:
            includes = includes+' '+latsinc[platform]
            libs = libs+' '+latslib[platform]
    except KeyError:
        print "Platform not supported:",platform
        sys.exit(1)
            
    # Build and execute the command
    command = f77+" "+includes+f77opts+libs
    if verbose:
        print command
    os.system(command)

if __name__=='__main__':
    main(sys.argv)
