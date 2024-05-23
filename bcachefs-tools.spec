Summary:	Userspace tools for bcachefs
Summary(pl.UTF-8):	Narzędzia przestrzeni użytkownika do bcachefs
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
%ifnarch x32
BuildRequires:	clang-devel
%else
BuildRequires:	clang-devel(x86-64)
%endif
BuildRequires:	keyutils-devel
BuildRequires:	libaio-devel
BuildRequires:	libblkid-devel
BuildRequires:	libfuse3-devel >= 3.7
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

%description -l pl.UTF-8
Bcachefs to nowy zaawansowany system plików dla Linuksa, kładący
nacisk na wiarygodności, solidności i kompletnym zestawie funkcji,
których można oczekiwać od nowoczesnego systemu plików.

Ten pakiet zawiera narzędzia przestrzeni użytkownika do bcachefs.

%prep
%setup -q
%patch0 -p1

%build
export RUSTFLAGS="%{rpmrustflags}"
export PKG_CONFIG_ALLOW_CROSS=1
export BINDGEN_EXTRA_CLANG_ARGS="%{rpmcflags} %{rpmcppflags}"
%ifnarch x32
export LIBCLANG_PATH="%{_libdir}"
%else
export LIBCLANG_PATH=/usr/lib64
%endif
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
%attr(755,root,root) %{_sbindir}/fsck.fuse.bcachefs
%attr(755,root,root) %{_sbindir}/mkfs.bcachefs
%attr(755,root,root) %{_sbindir}/mkfs.fuse.bcachefs
%attr(755,root,root) %{_sbindir}/mount.bcachefs
%attr(755,root,root) %{_sbindir}/mount.fuse.bcachefs
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

# initramfs subpackage?
#%{_datadir}/initramfs-tools/hooks/bcachefs
#%{_datadir}/initramfs-tools/scripts/local-premount/bcachefs
