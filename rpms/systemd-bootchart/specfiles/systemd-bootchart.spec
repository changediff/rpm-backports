Name:		systemd-bootchart
Version:	231
Release:	3%{?dist}
Summary:	Boot performance graphing tool 

License:	GPLv2+ and LGPLv2+
URL:		https://github.com/systemd/systemd-bootchart
Source0:	https://github.com/systemd/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.xz

BuildRequires: gcc
BuildRequires: systemd
BuildRequires: systemd-compat-libs
BuildRequires: libxslt-devel
BuildRequires: docbook-style-xsl
%{?systemd_requires}

%description
This package provides a binary which can be started during boot early boot to
capture informations about processes and services launched during bootup.
Resource utilization and process information are collected during the boot
process and are later rendered in an SVG chart. The timings for each services
are displayed separately.

%prep
%setup -q

%build
%configure
%make_build

%install
%make_install

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license LICENSE.GPL2
%license LICENSE.LGPL2.1
%doc README
%config(noreplace) %{_sysconfdir}/systemd/bootchart.conf
%{_unitdir}/systemd-bootchart.service
%{_unitdir}/../%{name}
%{_mandir}/man1/%{name}.1*
%{_mandir}/man5/bootchart.conf.5*
%{_mandir}/man5/bootchart.conf.d.5*

%changelog
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 231-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Sep 21 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 231-2
- Improve SPEC file thanks to suggestions during review

* Tue Sep 20 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 231-1
- Initial packaging
