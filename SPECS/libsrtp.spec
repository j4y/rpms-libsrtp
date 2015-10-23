%global shortname srtp

Name:		libsrtp
Version:	1.5.0
Release:	2%{?dist}
Summary:	An implementation of the Secure Real-time Transport Protocol (SRTP)
Group:		System Environment/Libraries
License:	BSD
URL:		https://github.com/cisco/libsrtp
Source0:	https://github.com/cisco/libsrtp/archive/v%{version}.tar.gz
# Pkgconfig goodness
Source1:	libsrtp.pc
# Universal config.h
Source2:	config.h

# Seriously. Who doesn't do shared libs these days?
# And how does Chromium always manage to find these projects and use them?
Patch0:		libsrtp-1.5.0-shared.patch
Patch1:		libsrtp-srtp_aes_encrypt.patch
Patch2:		libsrtp-sha1-name-fix.patch

%description
This package provides an implementation of the Secure Real-time
Transport Protocol (SRTP), the Universal Security Transform (UST), and
a supporting cryptographic kernel.

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p1 -b .shared
%patch1 -p1 -b .srtp_aes_encrypt
%patch2 -p1 -b .sha1-name-fix

# Fix end-of-line encoding
sed -i 's/\r//g' doc/draft-irtf-cfrg-icm-00.txt

%if 0%{?rhel} > 0
%ifarch ppc64
sed -i 's/-z noexecstack//' Makefile.in
%endif
%endif

%build
export CFLAGS="%{optflags} -fPIC"
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -exec rm -f {} ';'
pushd %{buildroot}%{_libdir}
mv libsrtp.so libsrtp.so.1.0.0
ln -sf libsrtp.so.1.0.0 libsrtp.so
ln -sf libsrtp.so.1.0.0 libsrtp.so.1
popd

# Install the pkg-config file
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
install -m0644 %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig/
# Fill in the variables
sed -i "s|@PREFIX@|%{_prefix}|g" %{buildroot}%{_libdir}/pkgconfig/libsrtp.pc
sed -i "s|@LIBDIR@|%{_libdir}|g" %{buildroot}%{_libdir}/pkgconfig/libsrtp.pc
sed -i "s|@INCLUDEDIR@|%{_includedir}|g" %{buildroot}%{_libdir}/pkgconfig/libsrtp.pc

# Handle multilib issues with config.h
mv %{buildroot}%{_includedir}/%{shortname}/config.h %{buildroot}%{_includedir}/%{shortname}/config-%{__isa_bits}.h
cp -a %{SOURCE2} %{buildroot}%{_includedir}/%{shortname}/config.h

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc CHANGES LICENSE README TODO VERSION doc/*.txt doc/*.pdf
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{shortname}/
%{_libdir}/pkgconfig/libsrtp.pc
%{_libdir}/*.so

%changelog
* Fri Nov 14 2014 Tom Callaway <spot@fedoraproject.org> - 1.5.0-2
- fix library linking typo

* Fri Nov 14 2014 Tom Callaway <spot@fedoraproject.org>
- api changes between 1.4.4 and 1.5.0, bump sover to 1.0.0
- fix linking issue to make proper libsrtp.so.1

* Fri Oct 31 2014 Leif Madsen <leif@leifmadsen.com> - 1.5.0-1
- Update for 1.5.0 release.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-13.20101004cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-12.20101004cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 15 2014 Dennis Gilmore <dennis@ausil.us> - 1.4.4-11.20101004cvs
- update the config.h header aarch64 is a 64 bit arch though there is no multilib

* Mon Feb 10 2014 Tom Callaway <spot@fedoraproject.org> - 1.4.4-10.20101004cvs
- rename internal functions to avoid conflicts (bz 956340)

* Mon Dec 30 2013 Tom Callaway <spot@fedoraproject.org> - 1.4.4-9.20101004cvs
- apply fix for CVE-2013-2139 from https://github.com/cisco/libsrtp/pull/27

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-8.20101004cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-7.20101004cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 25 2012 Karsten Hopp <karsten@redhat.com> 1.4.4-6.20101004cvs
- use __PPC64__, not __ppc64__ which is undefined on PPC64 arch

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-5.20101004cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 21 2012 Tom Callaway <spot@fedoraproject.org> - 1.4.4-4.20101004cvs
- handle config.h multilib (bz787537)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-3.20101004cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-2.20101004cvs
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Jeffrey C. Ollie <jeff@ocjtech.us>
- Don't use '-z noexecstack' option for linker on PPC64 (EL6)

* Mon Oct  4 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.4.4-1.20101004cvs
- initial package
