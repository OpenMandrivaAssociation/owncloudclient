%define major 0
%define libname %mklibname owncloudsync %{major}
%define develname %mklibname owncloudsync -d

Summary:	owncloud desktop client
Name:		mirall
Version:	1.7.0
Release:	2
License:	GPLv2+
Group:		Archiving/Backup
URL:		http://owncloud.org
Source0:	https://download.owncloud.com/desktop/stable/%{name}-%{version}.tar.bz2
BuildRequires:	cmake
BuildRequires:	qt4-devel
BuildRequires:	pkgconfig(QtWebKit)
BuildRequires:	pkgconfig(neon)
BuildRequires:	qtkeychain-devel
BuildRequires:	pkgconfig(sqlite3)
Requires:       %{libname} = %{EVRD}

%description
With ownCloud you can sync & share your files,
calendar, contacts and more.Access your data from
all your devices, on an open platform you can
extend and modify.

%package -n %{libname}
Summary:	Shared library for ownCloud client
Group:		System/Libraries

%description -n %{libname}
Shared library for ownCloud client.

%package -n %{develname}
Summary:	Developmnet files for ownCloud client
Group:		Development/Other
Requires:       %{libname} = %{EVRD}
Provides:       %{name}-devel = %{EVRD}

%description -n %{develname}
Development files and headers for %{name}.

%prep
%setup -q

%build
%cmake_qt4 \
	-DBUILD_WITH_QT4=on

%make owncloud

%install
%makeinstall_std -C build
find %{buildroot}%{_libdir} -name "*.a" -delete

%files
%doc ChangeLog COPYING
%config(noreplace) %{_sysconfdir}/ownCloud/sync-exclude.lst
%dir %{_datadir}/owncloud
%dir %{_datadir}/owncloud/i18n
%{_bindir}/owncloud
%{_bindir}/owncloudcmd
%{_libdir}/owncloud/libocsync.so.%{major}*
%{_iconsdir}/hicolor/*/*/*.png
%{_datadir}/nautilus-python/extensions/syncstate.py
%{_datadir}/applications/owncloud.desktop
%{_datadir}/owncloud/i18n/*.qm

%files -n %{libname}
%{_libdir}/libowncloudsync.so.%{version}
%{_libdir}/libowncloudsync.so.%{major}

%files -n %{develname}
%doc ChangeLog COPYING *.md
%{_includedir}/httpbf.h
%{_includedir}/owncloudsync
%{_libdir}/libowncloudsync.so
%{_libdir}/owncloud/libocsync.so
