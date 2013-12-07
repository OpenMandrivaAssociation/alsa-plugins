%define libname %mklibname %{name}

Summary:	Advanced Linux Sound Architecture (ALSA) plugins
Name:		alsa-plugins
Version:	1.0.27
Release:	4
# All packages are LGPLv2+ with the exception of samplerate which is GPLv2+
License:	GPLv2+ and LGPLv2+
Group:		Sound
Url:		http://www.alsa-project.org
Source0:	ftp://ftp.alsa-project.org/pub/plugins/%{name}-%{version}.tar.bz2
Source1:	jack.conf
Source2:	pulseaudio.conf
Source3:	pcm-oss.conf
Source4:	samplerate.conf
Source5:	upmix.conf
Source6:	vdownmix.conf
Source7:	pulse-default.conf
Patch1:		alsa-plugins-1.0.19-missing-avutil.patch

BuildRequires:	kernel-headers >= 2.4.0
BuildRequires:	pkgconfig(alsa) >= %{version}
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libpulse) >= 0.8
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(speex)

%description
Advanced Linux Sound Architecture (ALSA) utilities. Modularized architecture
with support for a large range of ISA and PCI cards. Fully compatible with
OSS/Lite (kernel sound drivers), but contains many enhanced features.

This is the plugins package, which allows you to manipulate ALSA settings.

%package -n	%{libname}
Summary:	Advanced Linux Sound Architecture (ALSA) plugins
Group:		Sound
%rename		%{name}

%description -n	%{libname}
Advanced Linux Sound Architecture (ALSA) utilities. Modularized architecture
with support for a large range of ISA and PCI cards. Fully compatible with
OSS/Lite (kernel sound drivers), but contains many enhanced features.

This is the plugins package, which allows you to manipulate ALSA settings.

%package	doc
Summary:	Advanced Linux Sound Architecture (ALSA) plugins
Group:		Sound
BuildArch:	noarch

%description	doc
Documentation for %{name}.

# (tv) needed for biarch:
%package	pulse-config
Summary:	Alsa to PulseAudio backend configuration
Group:		Sound
License:	LGPLv2+
# (cg) For upgrading from old configuration system
Requires(post):	libalsa-data >= 1.0.20-2
Requires(post):	update-alternatives

%description	pulse-config
This package contains configuration files for the pulse ALSA plugin.

%package -n	%{libname}-pulseaudio
Summary:	Alsa to PulseAudio backend
Group:		Sound
License:	LGPLv2+
Provides:	%{name}-pulseaudio = %{version}-%{release}
Conflicts:	%{libname} < 1.0.15-2
Conflicts:	%{name} < 1.0.14-8
Requires:	%{name}-pulse-config
%ifarch x86_64
# (cg) Suggest the 32 bit plugin on 64 bits to ensure compatibility
#      with (typically closed source) 32 bit apps.
Suggests:	lib%{name}-pulseaudio
%endif

%description -n	%{libname}-pulseaudio
This plugin allows any program that uses the ALSA API to access a PulseAudio
sound daemon. In other words, native ALSA applications can play and record
sound across a network. There are two plugins in the suite, one for PCM and
one for mixer control.

%package -n	%{libname}-jack
Summary:	Jack PCM output plugin for ALSA
Group:		Sound
License:	LGPLv2+
Provides:	%{name}-jack = %{version}-%{release}
Conflicts:	%{libname} < 1.0.15-2

%description -n	%{libname}-jack
This plugin converts the ALSA API over JACK (Jack Audio Connection
Kit, http://jackit.sf.net) API.  ALSA native applications can work
transparently together with jackd for both playback and capture.

    ALSA apps (playback) -> ALSA-lib -> JACK plugin -> JACK daemon
    ALSA apps (capture) <- ALSA-lib <- JACK plugin <- JACK daemon

This plugin provides the PCM type "jack"

%prep
%setup -q
%apply_patches

%build
autoreconf -fi
%configure2_5x
%make LIBS='-pthread'

%install
%makeinstall_std mkdir_p="mkdir -p"

install -d %{buildroot}%{_datadir}/alsa/pcm
install -m644 %{SOURCE1} %{SOURCE2} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{buildroot}%{_datadir}/alsa/pcm

# (cg) Include a configuration for when pulse is active
install -m644 %{SOURCE7} -D %{buildroot}%{_sysconfdir}/sound/profiles/pulse/alsa-default.conf

# We already include those in other places
rm %{buildroot}%{_datadir}/alsa/alsa.conf.d/{50-pulseaudio.conf,99-pulseaudio-default.conf.example}

%post pulse-config
# (cg) Check to see if the user has disabled pulse in the old style setup.
if [ -f %{_sysconfdir}/alsa/pulse-default.conf ]; then
  if grep -q "^#DRAKSOUND- " %{_sysconfdir}/alsa/pulse-default.conf; then
    update-alternatives --set soundprofile %{_sysconfdir}/sound/profiles/alsa
  fi
fi

%files doc
%doc COPYING* doc/R* doc/*.txt

%files -n %{libname}
%exclude %{_libdir}/alsa-lib/*_pulse.so
%exclude %{_libdir}/alsa-lib/*_jack.so
%{_datadir}/alsa/pcm/samplerate.conf
%{_datadir}/alsa/pcm/upmix.conf
%{_datadir}/alsa/pcm/vdownmix.conf
%{_libdir}/alsa-lib/*

%files pulse-config
%{_sysconfdir}/sound/profiles/pulse/alsa-default.conf
%{_datadir}/alsa/pcm/pulseaudio.conf

%files -n %{libname}-pulseaudio
%doc doc/README-pulse
%{_libdir}/alsa-lib/libasound_module_pcm_pulse.so
%{_libdir}/alsa-lib/libasound_module_ctl_pulse.so
%{_libdir}/alsa-lib/libasound_module_conf_pulse.so

%files -n %{libname}-jack
%doc doc/README-jack
%{_datadir}/alsa/pcm/jack.conf
%{_libdir}/alsa-lib/libasound_module_pcm_jack.so
