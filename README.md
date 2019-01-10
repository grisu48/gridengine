# Gridengine

This repository contains a fork of the [Son of Grid Engine](https://arc.liv.ac.uk/trac/SGE) project in conjunction with some documentation and fixes to get the gridengine working on more recent Linux systems.

# Building

Before building make sure you are relaxed and your cup of coffee (or filling of your choice) is full and well temperated.

Then take a deep breath and be prepared for turbulence.

**In general the build process consists of the following steps**

* Build the dependency tool and create dependencies with `aimk`
* Compile with `aimk`

The suggested (working) build options are: `aimk -no-herd -no-java`

## OpenSUSE 15.0 LEAP

*Instructions updated on 10.01.2019*

Install **Requirements** with

    zypper install java-1_8_0-openjdk java-1_8_0-openjdk-devel gcc ant automake hwloc-devel libopenssl-1_0_0-devel libdb-4_8-devel pam-devel libXt-devel motif-devel xorg-x11-devel
	# Notes: * for the openjdk you can also use a more recent version
	         * The version libopenssl-1_0_0-devel is required and needs to uninstall the (by default) installed version 1.1

Prepare the environment by executing the `bootstrap.sh` script

    cd sge-8.1.9/source
    ./scripts/bootstrap.sh

Then build the SGE using

    ./aimk -no-herd -no-java
    # No HADOOP support and no Java support
    # Note Java is not needed for qmon!

The build process takes some time. The generated binaries are (in my case) in the `LINUXAMD64` folder in `sources`

Now install the binaries to `SGE_ROOT`:

    export SGE_ROOT="/opt/sge/"   # Or whereever you want to install the grid engine to
    scripts/distinst -local -allall -noexit # asks for confirmation
    cd $SGE_ROOT
    ./inst_sge -m -x -csp  # or run ./start_gui_installer

Done ``:-)`

## Known issues

    ../sh.proc.c:153:16: error: storage size of ‘w’ isn’t known
         union wait w;

This error was the whole reason for forking the repository. Comment out line 51 in 

    50: #if defined(_BSD) || (defined(IRIS4D) && __STDC__) || defined(__lucid) || defined(linux) || defined(__GNU__) || defined(__GLIBC__)
    51: //# define BSDWAIT
    52: #endif /* _BSD || (IRIS4D && __STDC__) || __lucid || glibc */

