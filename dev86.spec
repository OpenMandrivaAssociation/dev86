%define		bccdir	%{_libdir}/bcc

Summary: 	A real mode 80x86 assembler and linker
Name:		dev86
Version:	0.16.18
Release:	%mkrel 2
License: 	GPLv2
Group:		Development/Other
URL:		http://homepage.ntlworld.com/robert.debath/
Source:		http://homepage.ntlworld.com/robert.debath/dev86/Dev86src-%{version}.tar.gz
Patch0:		dev86-noelks.patch
Patch1:		dev86-64bit.patch
Patch2:		dev86-nostrip.patch
Patch3:		dev86-overflow.patch
Patch4:		dev86-long.patch
Patch5:		dev86-print-overflow.patch
Patch6:		dev86-copt.patch
Buildroot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Obsoletes:	bin86
Provides:       bin86
ExclusiveArch:  %{ix86} ppc x86_64 %{arm}

%description
The dev86 package provides an assembler and linker for real mode 80x86
instructions. You'll need to have this package installed in order to
build programs that run in real mode, including LILO and the kernel's
bootstrapping code, from their sources.

You should install dev86 if you intend to build programs that run in real
mode from their source code.

%package        devel
Summary:        A development files for dev86
Group:          Development/Other
Requires:       %{name} = %{version}-%{release}

%description    devel
The dev86 package provides an assembler and linker for real mode 80x86
instructions. You'll need to have this package installed in order to
build programs that run in real mode, including LILO and the kernel's
bootstrapping code, from their sources.

The dev86-devel package provides C headers need to use bcc, the C
compiler for real mode x86.

You should install dev86 if you intend to build programs that run in real
mode from their source code.

Note that you don't need dev86-devel package in order to build
a kernel.

%prep
%setup -q
%patch0 -p1 -b .noelks
%if %_lib == lib64
%patch1 -p1 -b .64bit
%endif
%patch2 -p1 -b .nostrip
%patch3 -p1 -b .overflow
%patch4 -p1 -b .long
%patch5 -p1 -b .print-overflow
%patch6 -p1 -b .copt

%build
# the main makefile doesn't allow parallel build
make <<!FooBar!
5
quit
!FooBar!

%install
rm -rf %{buildroot}

make DIST=%{buildroot} MANDIR=%{_mandir} LIBDIR=%{bccdir} INCLDIR=%{bccdir} install install-man

pushd %{buildroot}%{_bindir}
rm -f nm86 size86
ln objdump86 nm86
ln objdump86 size86
popd

# %doc --parents would be overkill
for i in elksemu unproto bin86 copt dis88 bootblocks; do
        ln -f $i/README README.$i
done
ln -f bin86/README-0.4 README-0.4.bin86
ln -f bin86/ChangeLog ChangeLog.bin86

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README MAGIC Contributors README.bootblocks README.copt README.dis88
%doc README.elksemu README.unproto README-0.4.bin86 README.bin86 ChangeLog.bin86
%dir %{bccdir}
%{_bindir}/*
%{bccdir}/*
%{_mandir}/man1/*
%exclude %{bccdir}/i386/lib*
%exclude %{bccdir}/include

%files devel
%defattr(-,root,root)
%doc README
%dir %{bccdir}/include
%{bccdir}/include/*
%{bccdir}/i386/lib*



%changelog
* Sat Sep 24 2011 Andrey Bondrov <abondrov@mandriva.org> 0.16.18-2mdv2012.0
+ Revision: 701172
- Fix directories

  + Matthew Dawkins <mattydaw@mandriva.org>
    - added arch arm to exclusivearch

* Mon Apr 18 2011 Antoine Ginies <aginies@mandriva.com> 0.16.18-1
+ Revision: 655812
- release 0.1.6.18 (from fedora)

  + Oden Eriksson <oeriksson@mandriva.com>
    - rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 0.16.17-7mdv2010.1
+ Revision: 522451
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 0.16.17-6mdv2010.0
+ Revision: 413349
- rebuild

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 0.16.17-5mdv2009.0
+ Revision: 220599
- rebuild

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 0.16.17-4mdv2008.1
+ Revision: 149170
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sun Jul 01 2007 Christiaan Welvaart <spturtle@mandriva.org> 0.16.17-3mdv2008.0
+ Revision: 46283
- build on x86-64 as well
- patch7: fix build on non-x86 archs (no elksemu)

* Fri Jun 22 2007 Adam Williamson <awilliamson@mandriva.org> 0.16.17-2mdv2008.0
+ Revision: 42798
- rebuild for 2008
- Import dev86



* Sun Jul 23 2006 Emmanuel Andry <eandry@mandriva.org> 0.16.17-1mdv2007.0
- 0.16.17
- Fix URL and source
- %%mkrel
- drop patch 6 (applied upstream)

* Wed Dec 22 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 0.16.16-1mdk
- 0.16.16
- Fix invalid memory allocation in bcc.c:build_prefix () (P6 from fedora)
- drop P0-P4
- cleanups

* Sat Jun 19 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 0.16.3-3mdk
- build on ppc as well

* Thu Jul 24 2003 Götz Waschk <waschk@linux-mandrake.com> 0.16.3-2mdk
- small patch to make it compile with the current gcc

* Wed Nov 06 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.16.3-1mdk
- new release
- fix build
- fix %%doc overwriting README

* Tue Mar 26 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.15.5-3mdk
- add Url
- rpmlint cleanups

* Fri Sep 28 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.15.5-2mdk
- Provides: bin86 as well.

* Sat May 26 2001 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.15.5-1mdk
- Merge rh patches.
- 0.15.5.

* Tue Nov 28 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.15.1-2mdk
- Make almost rpmlint happy.

* Thu Sep 14 2000 Francis Galiegue <fg@mandrakesoft.com> 0.15.1-1mdk
- Use links, not symlinks!
- 0.15.1
- include ar86 (why wasn't it in before?)

* Tue Aug 08 2000 Thierry Vignaud <tvignaud@mandrakesoft.com> 0.15.0-3mdk
- split out -devel package (needed only for elks developpers ...)
- make rpmlint happier
- use macros ...

* Wed Jul 19 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.15.0-2mdk
- BM.

* Wed Jun 14 2000 Chmouel Boudjnah <chmouel@mandrakesoft.com> 0.15.0-1mdk
- First mandrake version from rh package.
