#
# spec file for package gridengine
#
# Copyright (c) 2020 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#


Name:           gridengine
Version:        8.1.9
Release:        1
Summary:		Son of Grid engine
License:        SISSL and BSD-3-Clause and LGPL-3.0-or-later and MIT and GPL-3.0-or-later and GFDL-1.1
Url:            https://github.com/grisu48/gridengine
Source:         gridengine-8.1.9.tar.gz
BuildRequires:  gcc
BuildRequires:	tcsh
%if 0%{?rhel} > 7 || 0%{?suse_version} >= 1500 || 0%{?sle_version} >= 150000 
BuildRequires:	java-1_8_0-openjdk
BuildRequires:	java-1_8_0-openjdk-devel
BuildRequires:	libopenssl-devel
BuildRequires:	libdb-4_8-devel
%else
BuildRequires:	java-1.8.0-openjdk
BuildRequires:	java-1.8.0-openjdk-devel
BuildRequires:	libdb-devel
BuildRequires:	openssl-devel
%endif
BuildRequires:	javacc
BuildRequires:	junit
BuildRequires:	ant
BuildRequires:	automake
BuildRequires:	hwloc-devel
BuildRequires:	pam-devel
BuildRequires:	libXt-devel
BuildRequires:	motif-devel
BuildRequires:	xorg-x11-devel
BuildRequires:	ncurses-devel
# Required for tumbleweed only and we do not support Tumbleweed here
#BuildRequires:  libtirpc-devel
Requires:		insserv-compat
BuildRoot:		%{_tmppath}/%{name}-%{version}-build

%description

%prep
#%setup -q
%setup -q -n %{name}-%{version}

%build
cd sge-8.1.9/source
./scripts/bootstrap.sh -no-secure
./aimk -no-herd -no-secure -no-java

%install
export SGE_ROOT="%{buildroot}/usr/local/bin/sge"
cd sge-8.1.9/source
mkdir -p "$SGE_ROOT"
echo 'y'| scripts/distinst -local -allall -noexit `dist/util/arch`

%post
%postun

%files
%attr(-,root,root) /usr/local/bin/sge
%attr(640,root,root) /usr/local/bin/sge/examples/drmaa/*.c
%attr(640,root,root) /usr/local/bin/sge/include/*
%attr(640,root,root) /usr/local/bin/sge/pvm/src/*
%attr(640,root,root) /usr/local/bin/sge/util/resources/loadsensors/*.c
%attr(750,root,root) /usr/local/bin/sge/install*
%attr(750,root,root) /usr/local/bin/sge/install*
%attr(750,root,root) /usr/local/bin/sge/bin/*
%attr(750,root,root) /usr/local/bin/sge/utilbin/*
/usr/local/bin/sge/*
#%doc README

%changelog

