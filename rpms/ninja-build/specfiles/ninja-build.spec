%if 0%{?rhel}
%define rpmmacrodir %{_rpmconfigdir}/macros.d
%endif
Name:           ninja-build
Version:        1.8.2
Release:        1.fb1%{?dist}
Summary:        A small build system with a focus on speed
License:        ASL 2.0
URL:            http://martine.github.com/ninja/
Source0:        https://github.com/martine/ninja/archive/v%{version}/ninja-%{version}.tar.gz
Source1:        ninja.vim
Source2:        macros.ninja
BuildRequires:  gcc-c++
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:  python34-devel
%define __python3 python3.4
%else
BuildRequires:  python3-devel
%endif
BuildRequires:  asciidoc
BuildRequires:  gtest-devel
BuildRequires:  re2c >= 0.11.3
Requires:       emacs-filesystem
Requires:       vim-filesystem
%if 0%{?facebook}
Obsoletes:      ninja <= %{version}
Provides:       ninja = %{version}
%endif

%description
Ninja is a small build system with a focus on speed. It differs from other
build systems in two major respects: it is designed to have its input files
generated by a higher-level build system, and it is designed to run builds as
fast as possible.

%prep
%autosetup -n ninja-%{version} -p1

%build
CFLAGS="%{optflags}" LDFLAGS="%{?__global_ldflags}" \
%if 0%{?rhel} && 0%{?rhel} < 7
%{__python2} \
%else
%{__python3} \
%endif
  configure.py --bootstrap --verbose
./ninja -v all
./ninja -v manual

%install
# TODO: Install ninja_syntax.py?
install -dpm0755 %{buildroot}%{_bindir}
install -Dpm0755 ninja -t %{buildroot}%{_bindir}/
install -Dpm0644 misc/bash-completion %{buildroot}%{_datadir}/bash-completion/completions/ninja
install -Dpm0644 misc/ninja-mode.el %{buildroot}%{_datadir}/emacs/site-lisp/ninja-mode.el
install -Dpm0644 misc/ninja.vim %{buildroot}%{_datadir}/vim/vimfiles/syntax/ninja.vim
install -Dpm0644 %{S:1} %{buildroot}%{_datadir}/vim/vimfiles/ftdetect/ninja.vim
install -Dpm0644 misc/zsh-completion %{buildroot}%{_datadir}/zsh/site-functions/_ninja
install -Dpm0644 %{S:2} %{buildroot}%{rpmmacrodir}/macros.ninja

ln -s ninja %{buildroot}%{_bindir}/ninja-build

%check
./ninja_test --gtest_filter=-SubprocessTest.SetWithLots

%files
%license COPYING
%doc HACKING.md README doc/manual.html
%{_bindir}/ninja
%{_bindir}/ninja-build
%{_datadir}/bash-completion/completions/ninja
%{_datadir}/emacs/site-lisp/ninja-mode.el
%{_datadir}/vim/vimfiles/syntax/ninja.vim
%{_datadir}/vim/vimfiles/ftdetect/ninja.vim
# zsh does not have a -filesystem package
%{_datadir}/zsh/
%{rpmmacrodir}/macros.ninja

%changelog
* Wed Jan 31 2018 Davide Cavalca <dcavalca@fb.com> - 1.8.2-1.fb1
- Add missing macro definition for CentOS 7

* Tue Sep 12 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.2-1
- Update to 1.8.2

* Thu Sep 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.1-1
- Update to 1.8.1

* Sat Sep 02 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Tue Aug 08 2017 Davide Cavalca <dcavalca@fb.com> - 1.7.2-6.fb1
- Facebook rebuild

* Tue Aug 01 2017 Kalev Lember <klember@redhat.com> - 1.7.2-6
- Backport an upstream patch to handle ostree setting 0 mtime

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 22 2017 Davide Cavalca <dcavalca@fb.com> - 1.7.2-4.fb1
- build fixes for CentOS 7
- replace broken internal ninja package

* Fri Apr 21 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.7.2-4
- Rename main executable to ninja (#1166135)
  (compatibility symlink is added)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Dec 03 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.7.2-2
- Add EPEL hacks

* Mon Nov 28 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.7.2-1
- Update to 1.7.2

* Mon Oct 10 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.7.1-3
- Fix install ninja.vim

* Sat Oct 08 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.7.1-2
- Add RPM macro

* Sat Jul 23 2016 Ben Boeckel <mathstuf@gmail.com> - 1.7.1-1
- update to 1.7.1
- fix bash completion for the binary rename (#1352330)
- disable test which fails to koji rlimit settings

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 16 2015 Ben Boeckel <mathstuf@gmail.com> - 1.6.0-2
- Add patch to rename mentions of the binary name

* Sun Jul 19 2015 Ben Boeckel <mathstuf@gmail.com> - 1.6.0-1
- Update to 1.6.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.5.3-3
- Rebuilt for GCC 5 C++11 ABI change

* Sun Feb 08 2015 Ben Boeckel <mathstuf@gmail.com> - 1.5.3-2
- Update bash-completions location

* Wed Dec 10 2014 Ben Boeckel <mathstuf@gmail.com> - 1.5.3-1
- Update to 1.5.3

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 05 2014 Christopher Meng <rpm@cicku.me> - 1.5.1-1
- Update to 1.5.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Nov 20 2013 Ben Boeckel <mathstuf@gmail.com> - 1.4.0-1
- Update to 1.4.0

* Sun Nov  3 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.3.4-4
- Use special %%doc to install all docs (#994005).

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Dan Horák <dan[at]danny.cz> - 1.3.4-2
- workaround possible too low limits for number of processes and open files,
  fixes build on ppc/ppc64 and s390(x)

* Sun Jun 09 2013 Ben Boeckel <mathstuf@gmail.com> - 1.3.4-1
- Update to 1.3.4
- Run test suite

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Nov 04 2012 Ben Boeckel <mathstuf@gmail.com> - 1.0.0-1
- Update to 1.0.0

* Thu Jul 19 2012 Ben Boeckel <mathstuf@gmail.com> - 0-0.6.20120719git5dc55a3
- Update to new snapshot

* Mon Jul 09 2012 Ben Boeckel <mathstuf@gmail.com> - 0-0.5.20120709gitb90d038
- Preserve timestamps on install
- Install as ninja-build to avoid conflicts with the ninja IRC package
- Update snapshot

* Tue Jun 19 2012 Ben Boeckel <mathstuf@gmail.com> - 0-0.4.20120605git54553d3
- Add an ftdetect file for ninja
- Fix zsh-stuff directory ownership

* Thu Jun 07 2012 Ben Boeckel <mathstuf@gmail.com> - 0-0.3.20120605git54553d3
- Add a Group tag

* Tue Jun 05 2012 Ben Boeckel <mathstuf@gmail.com> - 0-0.2.20120605git54553d3
- Update to new snapshot

* Fri Mar 30 2012 Ben Boeckel <mathstuf@gmail.com> - 0-0.1.20120330gitabd33d5
- Initial package
