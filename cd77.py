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

cdat_libs_locations = ""
for l in cdat_info.cdunif_library_directories+["/usr/X11R6/lib",]:
    cdat_libs_locations+=" -L"+l

cdat_inc_locations = ""
for l in cdat_info.cdunif_include_directories:
    cdat_inc_locations+=" -I"+l


# Locations of libraries and include files on the various platforms

ezgetlib =  "-lezget"
cdmslib = "-ldrs -l" + " -l".join(cdat_info.cdunif_libraries)
latslib = "-llats -lnetcdf -lm"
f77lib = "-lgfortran"
         

f77exec = "gfortran"


def main(argv):
    ezget = 0
    cdms = 0
    lats = 0
    verbose = 0
    includes = ""
    libs = f77lib

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

    # Constructs the command line
    if ezget:
        libs = libs + ' ' + ezgetlib
    if cdms:
        libs = libs + ' ' + cdmslib
    if lats:
        libs = libs + ' ' + latslib

    command = "%s %s %s %s %s" % (f77exec, f77opts, cdat_inc_locations, cdat_libs_locations, libs)
    # Execute the command

    # -C not needed these days
    command = command.replace(" -C ", " ")

    if verbose:
        print command
    os.system(command)

if __name__ == '__main__':
    main(sys.argv)
