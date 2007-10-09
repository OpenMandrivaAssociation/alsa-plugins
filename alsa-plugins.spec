%define beta rc1
%if %beta
%define fname %name-%{version}%beta
%else
%define fname %name-%{version}
%endif

Summary: Advanced Linux Sound Architecture (ALSA) plugins
Name:    alsa-plugins
Version: 1.0.15
%if %beta
Release: %mkrel 0.%{beta}.1
%else
Release: %mkrel 7
%endif
Source:  ftp://ftp.alsa-project.org/pub/utils/%fname.tar.bz2
Patch0:  1.0.14-buffer-attr.patch
License: GPL
BuildRoot: %_tmppath/%name-buildroot
Group: Sound
Url:   http://www.alsa-project.org

Requires: kernel >= 2.4.18
Requires: libalsa >= %version
BuildRequires: kernel-headers >= 2.4.0
BuildRequires: libalsa-devel >= %version
BuildRequires: libpulseaudio-devel >= 0.8
BuildRequires: ncurses-devel
BuildRequires: jackit-devel
BuildRequires: ffmpeg-devel
BuildRequires: speex-devel

%description
Advanced Linux Sound Architecture (ALSA) utilities. Modularized architecture
with support for a large range of ISA and PCI cards. Fully compatible with
OSS/Lite (kernel sound drivers), but contains many enhanced features.

This is the plugins package, which allows you to manipulate ALSA settings.

%prep
%setup -q -n %fname
%patch0 -p1 -b .buffer_attr

%build
%configure2_5x
make all

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std mkdir_p="mkdir -p"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc COPYING* doc/R* doc/*.txt
%_libdir/alsa-lib/*



