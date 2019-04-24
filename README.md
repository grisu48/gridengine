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

Done

## CentOS 7 (1810)

*Instructions updated on 18.01.2019*

**IMPORTANT**: Please build the SGE not under root! I encountered some cryptic linker errors as root, that disappeared when building as unprivileged user. Also ... (shame on me!) you should never build as root anyways ...

Install **Requirements** with

    yum install csh java-1.8.0-openjdk java-1.8.0-openjdk-devel gcc ant automake hwloc-devel openssl-devel libdb-devel pam-devel libXt-devel motif-devel ncurses-libs ncurses-devel

Then, as unprivileged user, go into a `tmux` or `screen` session and start the building process with

    cd sge-8.1.9/source
    ./scripts/bootstrap.sh
    
    ./aimk -no-herd -no-java
    # No HADOOP support and no Java support
    # Note Java is not needed for qmon!

If you encounter some cryptic linker errors (undefined reference to tputs, tgoto, ecc.) make sure you build as unprivileged user!

The build process takes some time. The generated binaries are (in my case) in the `LINUXAMD64` folder in `sources`

Now install the binaries to `SGE_ROOT`:

    export SGE_ROOT="/opt/sge/"   # Or whereever you want to install the grid engine to
    scripts/distinst -local -allall -noexit # asks for confirmation
    cd $SGE_ROOT
    ./inst_sge -m -x -csp  # or run ./start_gui_installer

Done.

### Build with Java

For the graphical installer, you need to run `aimk` with java support. For that you will need the following additional dependencies

    yum install ant-junit junit javacc

Then building should work with

    ./scripts/bootstrap.sh
    ./aimk -no-herd

If you get Java version errors, please adjust `build.properties` for your needs.

# Firewall

In order to make SGE run, you will need to open the following ports

    firewall-cmd --add-port=992/udp --permanent
    firewall-cmd --add-port=6444/tcp --permanent
    firewall-cmd --add-port=6445/tcp --permanent
    firewall-cmd --reload

# Configuration

## OpenMPI

In case you want to use OpenMPI, make sure to compile OpenMPI with `--with-sge` support.

In case you are using [Spack](https://spack.io), compile OpenMPI with `schedulers="sge" on`

    spack install openmpi%gcc@8.2.0 schedulers="sge"

You will also need to set `control_slaves` and `job_is_first_task` to `true`

    $ qconf -sp openmpi
    pe_name            openmpi
    slots              1024
    user_lists         NONE
    xuser_lists        NONE
    start_proc_args    NONE
    stop_proc_args     NONE
    allocation_rule    $fill_up
    control_slaves     TRUE
    job_is_first_task  TRUE
    urgency_slots      min
    accounting_summary FALSE
    qsort_args         NONE

# Known issues

## `storage size of ‘w’ isn’t known`

    ../sh.proc.c:153:16: error: storage size of ‘w’ isn’t known
         union wait w;

This error was the whole reason for forking the repository. Comment out line 51 in ``sge-8.1.9/source/3rdparty/qtcsh/sh.proc.c` as follows:

    50: #if defined(_BSD) || (defined(IRIS4D) && __STDC__) || defined(__lucid) || defined(linux) || defined(__GNU__) || defined(__GLIBC__)
    51: //# define BSDWAIT
    52: #endif /* _BSD || (IRIS4D && __STDC__) || __lucid || glibc */

## Linker errors: `undefined reference to tputs, tgoto, ecc.`

I encountered this error when building as root. Try building as unprivileged user (**which you should do anyways!**)

## Java version errors

Some weird java version not supported errors occurred to me, when building on OpenSuSE 15 LEAP. Edit the file `build.properties` and put there a more recent Java version like

    # sge-8.1.9/source/build.properties
    javac.debug=true
    javac.deprecated=true
    default.sge.javac.source=1.6
    default.sge.javac.target=1.6
    jgdi.javac.source=1.6
    jgdi.javac.target=1.6
    jjsv.javac.source=1.6
    jjsv.javac.target=1.6
    hadoop.javac.source=1.6
    hadoop.javac.target=1.6

That should fix the issue.
