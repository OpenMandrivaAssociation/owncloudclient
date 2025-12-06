%define	major 0
%define	libname %mklibname owncloudsync %{major}
%define	libowncloud_csync %mklibname libowncloud_csync %{major}
%define	devname %mklibname owncloudsync -d

%define	oname	ownCloud
%define	vversion 6.0.2

Summary:	The ownCloud Client
Name:		owncloudclient
Version:	6.0.2.17506
Release:	1
License:	GPLv2+
Group:	Archiving/Backup
Url:		https://owncloud.org
Source0:	https://download.owncloud.com/desktop/ownCloud/stable/%{version}/source/%{oname}-%{version}.tar.xz
#Source0:	https://github.com/owncloud/client/archive/%%{version}/%%{name}-%%{version}.zip
BuildRequires:	cmake >= 3.18
BuildRequires:	doxygen
BuildRequires:	git
BuildRequires:	graphviz
BuildRequires:	libre-graph-api-cpp-qt-client >= 1.0.4
BuildRequires:	python-sphinx
BuildRequires:	iniparser-devel >= 3.1
BuildRequires:	stdc++-devel
BuildRequires:	cmake(ECM) >= 6.0.0
BuildRequires:	cmake(KDSingleApplication-qt6)
BuildRequires:	cmake(LibreGraphAPI)
#BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Concurrent)
BuildRequires:	cmake(Qt6Core) >= 6.8.0
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Keychain)
BuildRequires:	cmake(Qt6LinguistTools)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6PrintSupport)
BuildRequires:	cmake(Qt6Quick)
BuildRequires:	cmake(Qt6QuickControls2)
BuildRequires:	cmake(Qt6QuickWidgets)
BuildRequires:	cmake(Qt6Sql)
BuildRequires:	cmake(Qt6Test)
#BuildRequires:	cmake(Qt6WebKitWidgets)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Xml)
BuildRequires:	pkgconfig(check) >= 0.9.5
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(libssh2)
BuildRequires:	pkgconfig(neon) >= 0.29.0
BuildRequires:	pkgconfig(openssl) >= 1.0.0
BuildRequires:	pkgconfig(smbclient)
BuildRequires:	pkgconfig(sqlite3) >= 3.9.0
BuildRequires:	pkgconfig(zlib)
Requires:	%{libname} = %{EVRD}
%rename	%{_lib}owncloud_csync
%rename	ocsync
%rename	mirall

%description
The ownCloud Desktop Client is a tool to synchronize files from ownCloud
Server with your computer.

%files
%license COPYING
%doc CHANGELOG.md README.md
#config(noreplace) %%{_sysconfdir}/ownCloud/sync-exclude.lst
%{_sysconfdir}/%{name}/%{oname}/sync-exclude.lst
%{_bindir}/owncloud
%{_bindir}/owncloudcmd
%{_datadir}/applications/owncloud.desktop
%{_datadir}/applications/owncloudcmd.desktop
%{_iconsdir}/hicolor/*/apps/owncloud.png
%{_datadir}/mime/packages/owncloud.xml

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared libraries for ownCloud client
Group:		System/Libraries
Requires:	%{libowncloud_csync} = %{EVRD}
Conflicts:	%{_lib}owncloudsync1 < %{EVRD}

%description -n %{libname}
Shared libraries for ownCloud client.

%files -n %{libname}
%license COPYING
%{_libdir}/libownCloudLibSync.so.%{vversion}
%{_libdir}/libownCloudLibSync.so.%{major}
%{_libdir}/plugins/%{oname}_vfs*.so
%{_libdir}/libownCloudResources.so.%{major}
%{_libdir}/libownCloudResources.so.%{vversion}
%{_libdir}/libowncloudGui.so
%{_libdir}/qml/org/%{oname}

#----------------------------------------------------------------------------

%package -n %{libowncloud_csync}
Summary:	Shared library for ownCloud client
Group:		System/Libraries
Conflicts:	%{_lib}owncloudsync1 < %{EVRD}

%description -n %{libowncloud_csync}
Shared library for ownCloud client.

%files -n %{libowncloud_csync}
%license COPYING
%{_libdir}/libownCloudCsync.so.%{major}
%{_libdir}/libownCloudCsync.so.%{vversion}

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Shared library for ownCloud client
Group:		Development/Other
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
This package contains development files for %{name}.

%files -n %{devname}
%license COPYING
%{_includedir}/%{oname}
%{_libdir}/libownCloudCsync.so
%{_libdir}/libownCloudLibSync.so
%{_libdir}/libownCloudResources.so
%{_libdir}/cmake/%{oname}/
%{_datadir}/mime/packages/owncloud.xml

#-----------------------------------------------------------------------------

%prep
%autosetup -p1 -n ownCloud-%{version}


%build
%cmake	 \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_INSTALL_LIBDIR=%{_libdir} \
	-DCMAKE_BUILD_TYPE=Release \
 	-DBUILD_TESTING=False \
	-DWITH_CRASHREPORTER=False \
	-DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir}/%{name} \
	-Wno-dev

%make_build


%install
%make_install -C build

# We use our macro to pick up docs
rm -rf %{buildroot}%{_docdir}/client/
