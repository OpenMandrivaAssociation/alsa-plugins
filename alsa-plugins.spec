%define name alsa-plugins
%define beta 0
%if %beta
%define fname %name-%{version}%beta
%else
%define fname %name-%{version}
%endif

%define libname %mklibname %name

Summary: Advanced Linux Sound Architecture (ALSA) plugins
Name:    %name
Version: 1.0.15
%if %beta
Release: %mkrel 0.%{beta}.3
%else
Release: %mkrel 4
%endif
Source0:  ftp://ftp.alsa-project.org/pub/utils/%fname.tar.bz2
Patch0:  1.0.14-buffer-attr.patch
# (fc) 1.0.15-4mdv fix assert in pulse plugin (Alsa bug #3470) (HG)
Patch1:  alsa-plugins-1.0.15-fixpulseassert.patch
# (fc) 1.0.15-4mdv add minmax condition for pulse plugin (Alsa bug #2601) (HG)
Patch2:  alsa-plugins-1.0.15-pulse-minmax.patch
# (fc) 1.0.15-4mdv report XRUN state back to application (HG) (Fedora)
Patch3:  1.0.14-state-xrun.patch
Source1: jack.conf
Source2: pulseaudio.conf
Source3: pcm-oss.conf
Source4: samplerate.conf
Source5: upmix.conf
Source6: vdownmix.conf
Source7: pulse-default.conf
# All packages are LGPLv2+ with the exception of samplerate which is GPLv2+
License: GPLv2+ and LGPLv2+
BuildRoot: %_tmppath/%name-buildroot
Group: Sound
Url:   http://www.alsa-project.org

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

%package -n %{libname}
Summary: Advanced Linux Sound Architecture (ALSA) plugins
Group: Sound
Provides: %{name} = %{version}-%{release}
Obsoletes: %{name} < %{version}-%{release}
Requires: kernel >= 2.4.18
Requires: libalsa >= %version
Requires: %{name}-doc

%description -n %{libname}
Advanced Linux Sound Architecture (ALSA) utilities. Modularized architecture
with support for a large range of ISA and PCI cards. Fully compatible with
OSS/Lite (kernel sound drivers), but contains many enhanced features.

This is the plugins package, which allows you to manipulate ALSA settings.

%package doc
Summary: Advanced Linux Sound Architecture (ALSA) plugins
Group: Sound

%description doc
Documentation for %{name}

%package -n %{libname}-pulseaudio
Summary:        Alsa to PulseAudio backend
Group:          Sound
License:        LGPLv2+
Provides:	%{name}-pulseaudio = %{version}-%{release}
Conflicts:	%{libname} < 1.0.15-2mdv

%description -n %{libname}-pulseaudio
This plugin allows any program that uses the ALSA API to access a PulseAudio
sound daemon. In other words, native ALSA applications can play and record
sound across a network. There are two plugins in the suite, one for PCM and
one for mixer control.

%package -n %{libname}-jack
Requires:       jack-audio-connection-kit
Summary:        Jack PCM output plugin for ALSA
Group:          Sound
License:        LGPLv2+
Provides:	%{name}-jack = %{version}-%{release}
Conflicts:	%{libname} < 1.0.15-2mdv

%description -n %{libname}-jack
This plugin converts the ALSA API over JACK (Jack Audio Connection
Kit, http://jackit.sf.net) API.  ALSA native applications can work
transparently together with jackd for both playback and capture.

    ALSA apps (playback) -> ALSA-lib -> JACK plugin -> JACK daemon
    ALSA apps (capture) <- ALSA-lib <- JACK plugin <- JACK daemon

This plugin provides the PCM type "jack"

%prep
%setup -q -n %fname
%patch0 -p1 -b .buffer_attr
%patch1 -p1 -b .fixpulseassert
%patch2 -p1 -b .minmax-pulse
%patch3 -p1 -b .state-xrun

%build
%configure2_5x
make all

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std mkdir_p="mkdir -p"

install -d ${RPM_BUILD_ROOT}%{_sysconfdir}/alsa

install -d ${RPM_BUILD_ROOT}%{_datadir}/alsa/pcm
install -m 644 %SOURCE1 %SOURCE2 \
               %SOURCE4 %SOURCE5 %SOURCE6 \
                   ${RPM_BUILD_ROOT}%{_datadir}/alsa/pcm
install -m 644 %SOURCE7 \
                   ${RPM_BUILD_ROOT}%{_sysconfdir}/alsa

%clean
rm -rf $RPM_BUILD_ROOT

%files doc
%defattr(-,root,root)
%doc COPYING* doc/R* doc/*.txt

%files -n %{libname}
%defattr(-,root,root)
%exclude %{_libdir}/alsa-lib/*_pulse.so
%exclude %{_libdir}/alsa-lib/*_jack.so
%{_datadir}/alsa/pcm/samplerate.conf
%{_datadir}/alsa/pcm/upmix.conf
%{_datadir}/alsa/pcm/vdownmix.conf
%_libdir/alsa-lib/*


%files -n %{libname}-pulseaudio
%defattr(-,root,root,-)
%doc doc/README-pulse
%config(noreplace) %{_sysconfdir}/alsa/pulse-default.conf
%{_datadir}/alsa/pcm/pulseaudio.conf
%{_libdir}/alsa-lib/libasound_module_pcm_pulse.so
%{_libdir}/alsa-lib/libasound_module_ctl_pulse.so

%files -n %{libname}-jack
%defattr(-,root,root,-)
%doc doc/README-jack
%{_datadir}/alsa/pcm/jack.conf
%{_libdir}/alsa-lib/libasound_module_pcm_jack.so
