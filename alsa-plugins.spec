%define name alsa-plugins
%define version 1.0.20
%define alibversion %version
%define beta 0
%if %beta
%define fname %name-%{version}%beta
%else
%define fname %name-%{version}
%endif

%define libname %mklibname %name

Summary: Advanced Linux Sound Architecture (ALSA) plugins
Name:    %name
Version: %version
%if %beta
Release: %mkrel 0.%{beta}.1
%else
Release: %mkrel 5
%endif
Source0:  ftp://ftp.alsa-project.org/pub/plugins/%fname.tar.bz2
Source1: jack.conf
Source2: pulseaudio.conf
Source3: pcm-oss.conf
Source4: samplerate.conf
Source5: upmix.conf
Source6: vdownmix.conf
Source7: pulse-default.conf

Patch0001: 0001-alsa-plugins-pulse-Implement-pause.patch
Patch0002: 0002-pulse-get-rid-of-a-number-of-assert-s.patch
Patch0003: 0003-pulse-use-PA_CONTEXT_IS_GOOD-where-applicable.patch
Patch0004: 0004-pulse-unify-destruction-of-snd_pulse_t.patch
Patch0005: 0005-pulse-call-pa_threaded_mainloop_wait-to-handle-spuri.patch
Patch0006: 0006-pulse-replace-manual-mainloop-by-pa_mainloop_iterate.patch
Patch0007: 0007-pulse-move-a-couple-of-PCM-related-functions-from-pu.patch
Patch0008: 0008-pulse-get-rid-of-redundant-state-variable.patch
Patch0009: 0009-pulse-unify-stream-context-state-checks.patch
Patch0010: 0010-pulse-rework-object-destruction-paths-a-bit.patch
Patch0011: 0011-pulse-immediately-trigger-EIO-when-connection-is-dro.patch

# All packages are LGPLv2+ with the exception of samplerate which is GPLv2+
License: GPLv2+ and LGPLv2+
BuildRoot: %_tmppath/%name-buildroot
Group: Sound
Url:   http://www.alsa-project.org

BuildRequires: kernel-headers >= 2.4.0
BuildRequires: libalsa-devel >= %alibversion
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
Requires: libalsa >= %alibversion
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

# (tv) needed for biarch:
%package        pulse-config
Summary:        Alsa to PulseAudio backend configuration
Group:          Sound
License:        LGPLv2+
Conflicts:	%{libname}-pulseaudio  <= 1.0.16-6mdv2008.1
%ifarch %ix86
Conflicts:	lib64alsa-plugins-pulseaudio <= 1.0.16-6mdv2008.1
%endif
# (cg) For upgrading from old configuration system
Requires(post): libalsa-data >= 1.0.20-2
Requires(post): update-alternatives

%description pulse-config
This package contains configuration files for the pulse ALSA plugin.

%post pulse-config
# (cg) Check to see if the user has disabled pulse in the old style setup.
if [ -f %{_sysconfdir}/alsa/pulse-default.conf ]; then
  if grep "^#DRAKSOUND- " %{_sysconfdir}/alsa/pulse-default.conf 2>/dev/null >/dev/null; then
    update-alternatives --set soundprofile /etc/sound/profiles/alsa
  fi
fi

%package -n %{libname}-pulseaudio
Summary:        Alsa to PulseAudio backend
Group:          Sound
License:        LGPLv2+
Provides:	%{name}-pulseaudio = %{version}-%{release}
Conflicts:	%{libname} < 1.0.15-2mdv
Conflicts:	%{name} < 1.0.14-8mdv
Requires:	 %name-pulse-config

%description -n %{libname}-pulseaudio
This plugin allows any program that uses the ALSA API to access a PulseAudio
sound daemon. In other words, native ALSA applications can play and record
sound across a network. There are two plugins in the suite, one for PCM and
one for mixer control.

%package -n %{libname}-jack
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
%apply_patches

%build
libtoolize --copy --force
%configure2_5x
make all

%install
rm -rf %{buildroot}
%makeinstall_std mkdir_p="mkdir -p"

install -d %{buildroot}%{_sysconfdir}/alsa

install -d %{buildroot}%{_datadir}/alsa/pcm
install -m 644 %SOURCE1 %SOURCE2 \
               %SOURCE4 %SOURCE5 %SOURCE6 \
                   %{buildroot}%{_datadir}/alsa/pcm

# (cg) Include a configuration for when pulse is active
install -d  %{buildroot}%{_sysconfdir}/sound/profiles/pulse
install -m 644 %SOURCE7 \
                   %{buildroot}%{_sysconfdir}/sound/profiles/pulse/alsa-default.conf

%clean
rm -rf %{buildroot}

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


%files pulse-config
%defattr(-,root,root)
%{_sysconfdir}/sound/profiles/pulse/alsa-default.conf
%{_datadir}/alsa/pcm/pulseaudio.conf

%files -n %{libname}-pulseaudio
%defattr(-,root,root,-)
%doc doc/README-pulse
%{_libdir}/alsa-lib/libasound_module_pcm_pulse.so
%{_libdir}/alsa-lib/libasound_module_ctl_pulse.so
%{_libdir}/alsa-lib/libasound_module_conf_pulse.so

%files -n %{libname}-jack
%defattr(-,root,root,-)
%doc doc/README-jack
%{_datadir}/alsa/pcm/jack.conf
%{_libdir}/alsa-lib/libasound_module_pcm_jack.so
