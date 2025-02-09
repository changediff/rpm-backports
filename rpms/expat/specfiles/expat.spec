%global unversion 2_2_5

Summary: An XML parser library
Name: expat
Version: %(echo %{unversion} | sed 's/_/./g')
Release: 4%{?dist}
Source: https://github.com/libexpat/libexpat/archive/R_%{unversion}.tar.gz#/expat-%{version}.tar.gz
URL: https://libexpat.github.io/
License: MIT
BuildRequires: autoconf, libtool, xmlto, gcc-c++
Patch0: expat-2.2.5-doc2man.patch

%description
This is expat, the C library for parsing XML, written by James Clark. Expat
is a stream oriented XML parser. This means that you register handlers with
the parser prior to starting the parse. These handlers are called when the
parser discovers the associated structures in the document being parsed. A
start tag is an example of the kind of structures for which you may
register handlers.

%package devel
Summary: Libraries and header files to develop applications using expat
Requires: expat%{?_isa} = %{version}-%{release}

%description devel
The expat-devel package contains the libraries, include files and documentation
to develop XML applications with expat.

%package static
Summary: expat XML parser static library
Requires: expat-devel%{?_isa} = %{version}-%{release}

%description static
The expat-static package contains the static version of the expat library.
Install it if you need to link statically with expat.

%prep
%setup -q -n libexpat-R_%{unversion}/expat
%patch0 -p2 -b .doc2man
sed -i 's/install-data-hook/do-nothing-please/' lib/Makefile.am
./buildconf.sh

%build
export CFLAGS="$RPM_OPT_FLAGS -fPIC"
export DOCBOOK_TO_MAN="xmlto man --skip-validation"
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%check
make check

%ldconfig_scriptlets

%files
%{!?_licensedir:%global license %%doc}
%doc AUTHORS Changes
%license COPYING
%{_bindir}/*
%{_libdir}/lib*.so.*
%{_mandir}/*/*
/usr/share/doc/expat/AUTHORS
/usr/share/doc/expat/Changes

%files devel
%doc doc/reference.html doc/*.png doc/*.css examples/*.c
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*.h

%files static
%{_libdir}/lib*.a

%changelog
* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.2.5-2
- Switch to %%ldconfig_scriptlets

* Thu Nov  2 2017 Joe Orton <jorton@redhat.com> - 2.2.5-1
- update to 2.2.5 (#1508667)

* Mon Aug 21 2017 Joe Orton <jorton@redhat.com> - 2.2.4-1
- update to 2.2.4 (#1483359)

* Fri Aug  4 2017 Joe Orton <jorton@redhat.com> - 2.2.3-1
- fix tests with unsigned char (upstream PR 109)
- update to 2.2.3 (#1473266)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 14 2017 Joe Orton <jorton@redhat.com> - 2.2.2-2
- update to 2.2.2 (#1470891)

* Fri Jul  7 2017 Joe Orton <jorton@redhat.com> - 2.2.1-2
- trim unnecessary doc, examples content

* Mon Jun 19 2017 Joe Orton <jorton@redhat.com> - 2.2.1-1
- update to 2.2.1 (#1462474)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jun 21 2016 Joe Orton <jorton@redhat.com> - 2.2.0-1
- update to 2.2.0 (#1247348)

* Thu Jun 16 2016 Joe Orton <jorton@redhat.com> - 2.1.1-2
- add security fixes for CVE-2016-0718, CVE-2012-6702, CVE-2016-5300,
  CVE-2016-4472

* Mon Apr 18 2016 David Tardon <dtardon@redhat.com> - 2.1.1-1
- new upstream release

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 2.1.0-11
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> - 2.1.0-9
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 17 2013 Joe Orton <jorton@redhat.com> - 2.1.0-6
- fix "xmlwf -h" output (#948534)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 13 2012 Joe Orton <jorton@redhat.com> - 2.1.0-3
- add -static subpackage (#722647)

* Fri Mar 30 2012 Joe Orton <jorton@redhat.com> - 2.1.0-1
- ship .pc file, move library back to libdir (#808399)

* Mon Mar 26 2012 Joe Orton <jorton@redhat.com> - 2.1.0-1
- update to 2.1.0 (#806602)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  8 2010 Joe Orton <jorton@redhat.com> - 2.0.1-10
- revised fix for CVE-2009-3560 regression (#544996)

* Sun Jan 31 2010 Joe Orton <jorton@redhat.com> - 2.0.1-9
- drop static libraries (#556046)
- add fix for regression in CVE-2009-3560 patch (#544996)

* Tue Dec  1 2009 Joe Orton <jorton@redhat.com> - 2.0.1-8
- add security fix for CVE-2009-3560 (#533174)
- add security fix for CVE-2009-3720 (#531697)
- run the test suite

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.0.1-5
- Autorebuild for GCC 4.3

* Wed Jan 23 2008 Joe Orton <jorton@redhat.com> 2.0.1-4
- chmod 644 even more documentation (#429806)

* Tue Jan  8 2008 Joe Orton <jorton@redhat.com> 2.0.1-3
- chmod 644 the documentation (#427950)

* Wed Aug 22 2007 Joe Orton <jorton@redhat.com> 2.0.1-2
- rebuild

* Wed Aug  8 2007 Joe Orton <jorton@redhat.com> 2.0.1-1
- update to 2.0.1
- fix the License tag
- drop the .la file

* Sun Feb  4 2007 Joe Orton <jorton@redhat.com> 1.95.8-10
- remove trailing dot in Summary (#225742)
- use preferred BuildRoot per packaging guidelines (#225742)

* Tue Jan 30 2007 Joe Orton <jorton@redhat.com> 1.95.8-9
- regenerate configure/libtool correctly (#199361)
- strip DSP files from examples (#186889)
- fix expat.h compilation with g++ -pedantic (#190244)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.95.8-8.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.95.8-8.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.95.8-8.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Joe Orton <jorton@redhat.com> 1.95.8-8
- restore .la file for apr-util

* Mon Jan 30 2006 Joe Orton <jorton@redhat.com> 1.95.8-7
- move library to /lib (#178743)
- omit .la file (#170031)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Mar  8 2005 Joe Orton <jorton@redhat.com> 1.95.8-6
- rebuild

* Thu Nov 25 2004 Ivana Varekova <varekova@redhat.com> 1.95.8
- update to 1.95.8

* Wed Jun 16 2004 Jeff Johnson <jbj@jbj.org> 1.95.7-4
- add -fPIC (#125586).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jun 11 2004 Jeff Johnson <jbj@jbj.org> 1.95.7-2
- fix: malloc failure from dbus test suite (#124747).

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Feb 22 2004 Joe Orton <jorton@redhat.com> 1.95.7-1
- update to 1.95.7, include COPYING file in main package

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Sep 17 2003 Matt Wilson <msw@redhat.com> 1.95.5-6
- rebuild again for #91211

* Tue Sep 16 2003 Matt Wilson <msw@redhat.com> 1.95.5-5
- rebuild to fix gzip'ed file md5sums (#91211)

* Tue Jun 17 2003 Jeff Johnson <jbj@redhat.com> 1.95.5-4
- rebuilt because of crt breakage on ppc64.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Nov 11 2002 Jeff Johnson <jbj@redhat.com> 1.95.5-1
- update to 1.95.5.

* Mon Aug 19 2002 Trond Eivind Glomsrød <teg@redhat.com> 1,95.4-1
- 1.95.4. 1.95.3 was withdrawn by the expat developers.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jun  6 2002 Trond Eivind Glomsrød <teg@redhat.com> 1,95.3-1
- 1.95.3

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Mar 22 2002 Trond Eivind Glomsrød <teg@redhat.com>
- Change a prereq in -devel on main package to a req
- License from MIT/X11 to BSD

* Mon Mar 11 2002 Trond Eivind Glomsrød <teg@redhat.com>
- 1.95.2

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Tue Oct 24 2000 Jeff Johnson <jbj@redhat.com>
- update to 1.95.1

* Sun Oct  8 2000 Jeff Johnson <jbj@redhat.com>
- Create.

