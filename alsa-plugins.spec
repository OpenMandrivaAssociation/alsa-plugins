%define libname %mklibname %{name}

Summary:	Advanced Linux Sound Architecture (ALSA) plugins
Name:		alsa-plugins
Version:	1.1.1
Release:	2
# All packages are LGPLv2+ with the exception of samplerate which is GPLv2+
License:	GPLv2+ and LGPLv2+
Group:		Sound
Url:		http://www.alsa-project.org
Source0:	ftp://ftp.alsa-project.org/pub/plugins/%{name}-%{version}.tar.bz2
Source1:	jack.conf
Source2:	pulseaudio.conf
Source3:	oss.conf
Source4:	samplerate.conf
Source5:	upmix.conf
Source6:	vdownmix.conf
Source7:	pulse-default.conf
Source8:	a52.conf
Source9:	speex.conf
BuildRequires:	kernel-headers >= 2.4.0
BuildRequires:	pkgconfig(alsa) >= %{version}
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libavcodec)
BuildRequires:	pkgconfig(libpulse) >= 0.8
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(speexdsp)

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

%package doc
Summary:	Advanced Linux Sound Architecture (ALSA) plugins
Group:		Sound
BuildArch:	noarch

%description doc
Documentation for %{name}.

%package -n	%{libname}-pulseaudio
Summary:	Alsa to PulseAudio backend
Group:		Sound
License:	LGPLv2+
Provides:	%{name}-pulseaudio = %{version}-%{release}
Conflicts:	%{libname} < 1.0.15-2
Conflicts:	%{name} < 1.0.14-8
%rename		%{name}-pulse-config
Requires(post):	update-alternatives
%if "%{_lib}" == "lib64"
# (cg) Suggest the 32 bit plugin on 64 bits to ensure compatibility
#      with (typically closed source) 32 bit apps.
Suggests:	lib%{name}-pulseaudio
Suggests:	pulseaudio-client-config
# (proyvind): Ensure that both packages gets upgraded at the same time for
#             biarch in order to avoid possible file conflicts between config
#             files on upgrade (as urpmi lacks support for ensuring that all
#             packages that owns a specific file gets upgraded during the
#             same transaction.
Conflicts:	lib%{name}-pulseaudio < %{EVRD} lib%{name}-pulseaudio > %{EVRD}
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

%package -n	%{libname}-a52
Summary:	A52/AC3 output plugin for ALSA
Group:		System/Libraries
License:	LGPLv2+
Provides:	%{name}-a52 = %{version}-%{release}
Conflicts:	%{libname} < 1.0.25-6

%description -n	%{libname}-a52
This plugin supports Digital 5.1 AC3 emulation over S/PDIF (IEC958).

%prep
%setup -q
%apply_patches
autoreconf -fi

%build
# (tpg) fix compilation with speexdsp
export CFLAGS="$CFLAGS -DHAVE_STDINT_H"
%configure \
	--with-speex=lib

%make LIBS='-pthread'

%install
%makeinstall_std mkdir_p="mkdir -p"

install -d %{buildroot}%{_datadir}/alsa/pcm
install -m644 %{SOURCE1} %{SOURCE2} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE9} %{buildroot}%{_datadir}/alsa/pcm
install -m644 %{SOURCE5} %{buildroot}%{_datadir}/alsa/alsa.conf.d/a52.conf

# (cg) Include a configuration for when pulse is active
install -m644 %{SOURCE7} -D %{buildroot}%{_sysconfdir}/sound/profiles/pulse/alsa-default.conf

# We already include those in other places
rm %{buildroot}%{_datadir}/alsa/alsa.conf.d/{50-pulseaudio.conf,99-pulseaudio-default.conf.example}

%post -n %{libname}-pulseaudio
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
%exclude %{_libdir}/alsa-lib/*_a52.so
%{_datadir}/alsa/pcm/samplerate.conf
%{_datadir}/alsa/pcm/speex.conf
%{_datadir}/alsa/pcm/upmix.conf
%{_datadir}/alsa/pcm/vdownmix.conf
%{_libdir}/alsa-lib/*

%files -n %{libname}-pulseaudio
%doc doc/README-pulse
%{_sysconfdir}/sound/profiles/pulse/alsa-default.conf
%{_datadir}/alsa/pcm/pulseaudio.conf
%{_libdir}/alsa-lib/libasound_module_pcm_pulse.so
%{_libdir}/alsa-lib/libasound_module_ctl_pulse.so
%{_libdir}/alsa-lib/libasound_module_conf_pulse.so

%files -n %{libname}-jack
%doc doc/README-jack
%{_datadir}/alsa/pcm/jack.conf
%{_libdir}/alsa-lib/libasound_module_pcm_jack.so

%files -n %{libname}-a52
%{_datadir}/alsa/alsa.conf.d/a52.conf
%{_libdir}/alsa-lib/libasound_module_pcm_a52.so
