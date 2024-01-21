Summary:	Userspace tools for bcachefs
Name:		bcachefs-tools
Version:	1.4.1
Release:	0.1
License:	GPL v2+
Group:		Applications/System
Source0:	https://evilpiepirate.org/bcachefs-tools/%{name}-vendored-%{version}.tar.zst
# Source0-md5:	2cbe55823812642656b2496f22bcf175
Patch0:		rust-target.patch
URL:		https://bcachefs.org/
BuildRequires:	cargo
BuildRequires:	clang-devel
BuildRequires:	keyutils-devel
BuildRequires:	libaio-devel
BuildRequires:	libblkid-devel
BuildRequires:	libsodium-devel
BuildRequires:	libuuid-devel
BuildRequires:	llvm-devel
BuildRequires:	lz4-devel
BuildRequires:	pkgconfig
BuildRequires:	systemd-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel
BuildRequires:	userspace-rcu-devel
BuildRequires:	zlib-devel
BuildRequires:	zstd
BuildRequires:	zstd-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%define		filterout_c	-fvar-tracking-assignments

%description
Bcachefs is an advanced new filesystem for Linux, with an emphasis on
reliability and robustness and the complete set of features one would
expect from a modern filesystem.

This package contains userspace tools to manage bcachefs.

%prep
%setup -q
%patch0 -p1

%build
export RUSTFLAGS="%{rpmrustflags}"
export PKG_CONFIG_ALLOW_CROSS=1
export BINDGEN_EXTRA_CLANG_ARGS="%{rpmcflags} %{rpmcppflags}"
%{__make} \
	V=1 \
	PREFIX="%{_prefix}" \
	ROOT_SBINDIR="%{_sbindir}" \
	LIBEXECDIR="%{_libexecdir}" \
	CC="%{__cc}" \
	EXTRA_CFLAGS="%{rpmcflags}" \
	EXTRA_LDFLAGS="%{rpmldflags}" \
	CARGO="%__cargo" \
	CARGO_BUILD_ARGS="-v --release --target %rust_target" \
	CARGO_TARGET="%rust_target"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8}
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	V=1 \
	PREFIX="%{_prefix}" \
	ROOT_SBINDIR="%{_sbindir}" \
	LIBEXECDIR="%{_libexecdir}" \
	CARGO="%__cargo" \
	CARGO_BUILD_ARGS="-v --release --target %rust_target" \
	CARGO_TARGET="%rust_target"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_sbindir}/bcachefs
%attr(755,root,root) %{_sbindir}/fsck.bcachefs
%attr(755,root,root) %{_sbindir}/mkfs.bcachefs
%attr(755,root,root) %{_sbindir}/mount.bcachefs
%attr(755,root,root) %{_libexecdir}/bcachefsck_all
%attr(755,root,root) %{_libexecdir}/bcachefsck_fail
%{systemdunitdir}/bcachefsck@.service
%{systemdunitdir}/bcachefsck_all.service
%{systemdunitdir}/bcachefsck_all.timer
%{systemdunitdir}/bcachefsck_all_fail.service
%{systemdunitdir}/bcachefsck_fail@.service
%{systemdunitdir}/system-bcachefsck.slice
/lib/udev/rules.d/64-bcachefs.rules
%{_mandir}/man8/bcachefs.8*
