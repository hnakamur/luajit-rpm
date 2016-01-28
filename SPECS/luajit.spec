Name:           luajit
Version:        2.0.4
Release:        3%{?dist}
Summary:        Just-In-Time Compiler for Lua
License:        MIT
URL:            http://luajit.org/
Source0:        http://luajit.org/download/LuaJIT-%{version}.tar.gz

%if 0%{?rhel}
ExclusiveArch:  %{ix86} x86_64
%endif

%description
LuaJIT implements the full set of language features defined by Lua 5.1.
The virtual machine (VM) is API- and ABI-compatible to the standard
Lua interpreter and can be deployed as a drop-in replacement.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains development files for %{name}.

%prep
%setup -q -n LuaJIT-%{version}
echo '#!/bin/sh' > ./configure
chmod +x ./configure

# preserve timestamps (cicku)
sed -i -e '/install -m/s/-m/-p -m/' Makefile

%ifarch x86_64
%global multilib_flag MULTILIB=lib64
%endif

%build
%configure
# Q= - enable verbose output
# E= @: - disable @echo messages
# NOTE: we use amalgamated build as per documentation suggestion doc/install.html
make amalg Q= E=@: PREFIX=%{_prefix} TARGET_STRIP=: \
           CFLAGS="%{optflags}" \
           %{?multilib_flag} \
           %{?_smp_mflags}

%install
# PREREL= - disable -betaX suffix
# INSTALL_TNAME - executable name
%make_install PREFIX=%{_prefix} \
              %{?multilib_flag}

rm -rf _tmp_html ; mkdir _tmp_html
cp -a doc _tmp_html/html

# Remove static .a
find %{buildroot} -type f -name *.a -delete

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license COPYRIGHT
%doc README
%{_bindir}/%{name}
%{_bindir}/%{name}-%{version}
%{_libdir}/libluajit*.so.*
%{_mandir}/man1/luajit*
%{_datadir}/%{name}-%{version}/

%files devel
%doc _tmp_html/html/
%{_includedir}/luajit-2.0/
%{_libdir}/libluajit*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Aug 07 2015 Oliver Haessler <oliver@redhat.com> - 2.0.4-3
- only build x86_64 on EPEL as luajit has no support for ppc64

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 21 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.4-1
- 2.0.4

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 09 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.3-3
- rebuild against lua 5.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 13 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.3-1
- 2.0.3 upstream release

* Sun Dec 15 2013 Clive Messer <clive.messer@communitysqueeze.org> - 2.0.2-9
- Apply luajit-path64.patch on x86_64.

* Mon Dec 09 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.2-8
- Fix strip (thanks Ville Skyttä)

* Fri Dec 06 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.2-7
- Fix executable binary

* Mon Dec 02 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.2-6
- Fix .pc

* Sun Dec 01 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.2-5
- Fixed short-circuit builds (schwendt)

* Sat Nov 30 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.2-4
- Preserve timestamps at install

* Fri Nov 29 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.2-3
- fixed some issues found by besser82
- Moved html-docs to -devel subpackage (besser82)
 
* Thu Nov 28 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.2-2
- Re-update

* Mon Sep 02 2013 Muayyad Alsadi <alsadi@gmail.com> - 2.0.2-1
- Update to new upstream version
- remove PREREL= option

* Mon Feb 06 2012 Andrei Lapshin - 2.0.0-0.4.beta9
- Update to new upstream version
- Rename main executable to luajit
- Remove BuildRoot tag and %%clean section

* Sun Oct 09 2011 Andrei Lapshin - 2.0.0-0.3.beta8
- Enable debug build
- Enable verbose build output
- Move libluajit-*.so to -devel
- Add link to upstream hotfix #1

* Tue Jul 05 2011 Andrei Lapshin <alapshin@gmx.com> - 2.0.0-0.2.beta8
- Append upstream hotfix #1

* Sun Jul 03 2011 Andrei Lapshin <alapshin@gmx.com> - 2.0.0-0.1.beta8
- Initial build
