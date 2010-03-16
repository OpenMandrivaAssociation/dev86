Summary:	A real mode 80x86 assembler and linker
Name:		dev86
Version:	0.16.17
Release:	%mkrel 7
License:	GPL
Group:		Development/Other
Url:		http://homepage.ntlworld.com/robert.debath/dev86/
Source0:	http://homepage.ntlworld.com/robert.debath/dev86/Dev86src-%{version}.tar.bz2
Patch5:		dev86-0.16.3-missing-header.patch.bz2
#Patch6:		dev86-0.16.16-overflow.patch.bz2
Patch7:		dev86-0.16.17-x86_64-no-elksemu.patch
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Obsoletes:	bin86
Provides:	bin86
ExclusiveArch:	%{ix86} ppc x86_64

%description
The dev86 package provides an assembler and linker for real mode 80x86
instructions. You'll need to have this package installed in order to
build programs that run in real mode, including LILO and the kernel's
bootstrapping code, from their sources.

You should install dev86 if you intend to build programs that run in real
mode from their source code.

%package	devel
Summary:	A development files for dev86
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description	devel
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
%patch5 -p1 -b .errno
#%patch6 -p1 -b .overflow
%patch7 -p1 -b .x86-64-no-elksemu

mkdir -p lib/bcc
ln -s ../../include lib/bcc/include

%build
make <<!FooBar!
5
quit
!FooBar!

%install
rm -rf $RPM_BUILD_ROOT

make DIST=$RPM_BUILD_ROOT MANDIR=%{_mandir} install install-man

#install -m755 -s $RPM_BUILD_ROOT/lib/elksemu $RPM_BUILD_ROOT%{_bindir}
#rm -rf $RPM_BUILD_ROOT/lib/

pushd $RPM_BUILD_ROOT%{_bindir}
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

# move header files out of %{_includedir} and into %{_libdir}/bcc/include
#mv $RPM_BUILD_ROOT%{_includedir} $RPM_BUILD_ROOT%{_libdir}/bcc

%clean
rm -rf $RPM_BUILD_ROOT

%define bccdir %{_prefix}/lib/bcc

%files
%defattr(-,root,root)
%doc README MAGIC Contributors README.bootblocks README.copt README.dis88
%doc README.elksemu README.unproto README-0.4.bin86 README.bin86 ChangeLog.bin86
%dir %{bccdir}
#%dir %{bccdir}/i86
#%dir %{bccdir}/i386
%{_bindir}/*
#%{bccdir}/bcc-cc1
#%{bccdir}/copt
#%{bccdir}/unproto
#%{bccdir}/i86/crt*
#%{bccdir}/i386/crt*
#%{bccdir}/i86/rules*
%{bccdir}/*
#%{_libdir}/liberror.txt
%{_mandir}/man1/*
%exclude %{bccdir}/i386/lib*

%files devel
%defattr(-,root,root)
%doc README
%dir %{bccdir}/include
%{bccdir}/include/*
#%{bccdir}/i86/lib*
%{bccdir}/i386/lib*
