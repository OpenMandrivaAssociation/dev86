%define		bccdir	%{_libdir}/bcc

Summary: 	A real mode 80x86 assembler and linker
Name:		dev86
Version:	0.16.18
Release:	3
License: 	GPLv2
Group:		Development/Other
Url:		http://homepage.ntlworld.com/robert.debath/
Source0:	http://homepage.ntlworld.com/robert.debath/dev86/Dev86src-%{version}.tar.gz
Patch0:		dev86-noelks.patch
Patch1:		dev86-64bit.patch
Patch2:		dev86-nostrip.patch
Patch3:		dev86-overflow.patch
Patch4:		dev86-long.patch
Patch5:		dev86-print-overflow.patch
Patch6:		dev86-copt.patch
ExclusiveArch:	%{ix86} ppc x86_64 %{arm}
Provides:	bin86

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

%files
%doc README MAGIC Contributors README.bootblocks README.copt README.dis88
%doc README.elksemu README.unproto README-0.4.bin86 README.bin86 ChangeLog.bin86
%dir %{bccdir}
%{_bindir}/*
%{bccdir}/*
%{_mandir}/man1/*
%exclude %{bccdir}/i386/lib*
%exclude %{bccdir}/include

%files devel
%doc README
%dir %{bccdir}/include
%{bccdir}/include/*
%{bccdir}/i386/lib*

