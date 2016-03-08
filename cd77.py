#!/usr/bin/env python
import sys
import os
import cdat_info

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
cdat_location = sys.prefix + "/Externals"
# Locations of libraries and include files on the various platforms

ezgetlib = {
    #"irix6" : "-L/pcmdi/ktaylor/pcmdi/util/ezget/Sgi6.2 -lezget",
    #"sunos5" : "-L/pcmdi/cirrus/ktaylor/ezget/solaris -lezget",
    "linux2": "-L" + cdat_location + "/lib -lezget",
    "darwin": "-L" + cdat_location + "/lib -lezget"}
cdmsinc = {
    #"irix6" : "-I"+cdat_location+"/include -I"+cdat_location+"/HDF4.0r2/include",
    #"sunos5" : "-I"+cdat_location+"/include",
    "linux2": "-I" + cdat_location + "/include",
    "darwin": "-I" + cdat_location + "/include"}
cdmslib = {
    #"irix6" : "-L"+cdat_location+"/lib -lcdms -lnetcdf -L"+cdat_location+"/HDF4.0r2/lib -lmfhdf -ldf -ljpeg -lz -ldrs",
    #"sunos5" : "-L"+cdat_location+"/lib -lcdms -lmfhdf -ldf -ljpeg -lz -lnetcdf -lnsl -ldrs -lm -lsunmath",
    # "linux2" : "-L"+cdat_location+"/lib -ldrs -lcdms -lnetcdf -lmfhdf -ldf -ljpeg -lz -lmfhdf -ldf -ljpeg -lz -lm"
    "linux2": "-L" + cdat_location + "/lib  -ldrs -l" + " -l".join(cdat_info.cdunif_libraries),
    "darwin": "-L" + cdat_location + "/lib  -ldrs -l" + " -l".join(cdat_info.cdunif_libraries)
}
latsinc = {
    #"irix6" : "-I"+cdat_location+"/include",
    #"sunos5" : "-I"+cdat_location+"/include",
    "linux2": "-I" + cdat_location + "/include",
    "darwin": "-I" + cdat_location + "/include"}
latslib = {
    #"irix6" : "-L"+cdat_location+"/lib -llats -lnetcdf -lm",
    #"sunos5" : "-L"+cdat_location+"/lib -llats -lnetcdf -lnsl -lm",
    "linux2": "-L" + cdat_location + "/lib -llats -lnetcdf -lm",
    "darwin": "-L" + cdat_location + "/lib -llats -lnetcdf -lm"}

f77lib = {"linux2": "-lgfortran",
          "darwin": "-lgfortran"}

f77exec = {
    #"irix6" : "f77",
    #"sunos5" : "f77",
    "linux2": "gfortran",
    "darwin": "gfortran"}


# Get the host type and major operating system version
def getplatform():
    return sys.platform


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
        if arg == "-ezget":
            ezget = 1
            cdms = 1
        elif arg == "-cdms":
            cdms = 1
        elif arg == "-lats":
            lats = 1
        elif arg == "-verbose":
            verbose = 1
        else:
            f77opts = f77opts + ' ' + arg

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
            libs = libs + ' ' + ezgetlib[platform]
        if cdms:
            includes = includes + ' ' + cdmsinc[platform]
            libs = libs + ' ' + cdmslib[platform]
        if lats:
            includes = includes + ' ' + latsinc[platform]
            libs = libs + ' ' + latslib[platform]
    except KeyError:
        print "Platform not supported:", platform
        sys.exit(1)

    # Build and execute the command
    command = f77 + " " + includes + " " + \
        f77opts + " " + f77lib[platform] + " " + libs
    # -C not needed these days
    command = command.replace(" -C ", " ")
    if verbose:
        print "UVCDAT LOCATION:", cdat_location
        print command
    os.system(command)

if __name__ == '__main__':
    main(sys.argv)
