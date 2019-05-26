#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs

Summary:	Local and remote ZeroConf service discovery for hardware resources
Summary(pl.UTF-8):	Lokalne i zdalne wykrywanie usług ZeroConf dla zasobów sprzętowych
Name:		hwsd
Version:	2.0.1
Release:	1
License:	LGPL v2.1 (library), GPL v3+ (applications)
Group:		Libraries
#Source0Download: https://github.com/Eyescale/hwsd/releases
Source0:	https://github.com/Eyescale/hwsd/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	d2285a1d878a12905fe9a062bc158aae
Patch0:		servus.patch
URL:		https://github.com/Eyescale/hwsd/
BuildRequires:	Eyescale-CMake
BuildRequires:	Lunchbox-devel >= 1.10
BuildRequires:	OpenGL-GLX-devel
BuildRequires:	Qt5Core-devel
BuildRequires:	Qt5Network-devel
BuildRequires:	Servus-devel
# just to satisfy cmake projects stupidity (FIXME)
BuildRequires:	Servus-qt-devel
BuildRequires:	boost-devel >= 1.41.0
BuildRequires:	cmake >= 3.1
%{?with_apidocs:BuildRequires:	doxygen}
BuildRequires:	libstdc++-devel
BuildRequires:	libstdc++-devel >= 6:4.2
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libX11-devel
Requires:	Lunchbox >= 1.10
Requires:	QtNetwork >= 4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
HW-SD is a library and daemon for the discovery and announcement of
hardware resources using ZeroConf. It enables auto-configuration of
ad-hoc GPU clusters and multi-GPU machines.

%description -l pl.UTF-8
HW-SD to biblioteka i demon do wyszukiwania i rozgłaszania zasobów
sprzętowych przy użyciu ZeroConfa. Pozwala na automatyczną
konfigurację ad-hocowych klastrów GPU i maszyn o wielu GPU.

%package devel
Summary:	Header files for HW-SD library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki HW-SD
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Lunchbox-devel >= 1.10
Requires:	Servus-devel
Requires:	libstdc++-devel

%description devel
Header files for HW-SD library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki HW-SD.

%package apidocs
Summary:	HW-SD API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki HW-SD
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description apidocs
API documentation for HW-SD library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki HW-SD.

%prep
%setup -q
%patch0 -p1

rmdir CMake/common
ln -s %{_datadir}/Eyescale-CMake CMake/common

%build
install -d build
cd build
%cmake ..

%{__make}

%if %{with apidocs}
doxygen doc/Doxyfile
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/hwsd/doc

install -d $RPM_BUILD_ROOT%{_examplesdir}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/hwsd/examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.txt README.md doc/Changelog.md
%attr(755,root,root) %{_bindir}/hw_sd
%attr(755,root,root) %{_bindir}/hw_sd_list
%attr(755,root,root) %{_libdir}/libhwsd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhwsd.so.4
%attr(755,root,root) %{_libdir}/libhwsd_gpu_glx.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhwsd_gpu_glx.so.4
%attr(755,root,root) %{_libdir}/libhwsd_gpu_dns_sd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhwsd_gpu_dns_sd.so.4
%attr(755,root,root) %{_libdir}/libhwsd_net_sys.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhwsd_net_sys.so.4
%attr(755,root,root) %{_libdir}/libhwsd_net_dns_sd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libhwsd_net_dns_sd.so.4

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libhwsd.so
%attr(755,root,root) %{_libdir}/libhwsd_gpu_glx.so
%attr(755,root,root) %{_libdir}/libhwsd_gpu_dns_sd.so
%attr(755,root,root) %{_libdir}/libhwsd_net_sys.so
%attr(755,root,root) %{_libdir}/libhwsd_net_dns_sd.so
%{_includedir}/hwsd
%dir %{_datadir}/hwsd
%{_datadir}/hwsd/CMake
%{_examplesdir}/%{name}-%{version}

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc build/doc/html/*
%endif
