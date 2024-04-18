%define major 0
%define libname %mklibname owncloudsync %{major}
%define libowncloud_csync %mklibname libowncloud_csync %{major}
%define devname %mklibname owncloudsync -d

%define vversion 5.2.1

Summary:	The ownCloud Client
Name:		owncloudclient
Version:	5.2.1.13040
Release:	1
License:	GPLv2+
Group:		Archiving/Backup
Url:		https://owncloud.org
Source0:	https://download.owncloud.com/desktop/ownCloud/stable/%{version}/source/ownCloud-%{version}.tar.xz
#Source0:	http://download.owncloud.com/desktop/stable/%{name}-%{version}.14058.tar.xz
#Source0:	https://github.com/owncloud/client/archive/%{version}/%{name}-%{version}.zip

BuildRequires:	stdc++-devel
BuildRequires:	doxygen
BuildRequires:	graphviz
BuildRequires:	iniparser-devel >= 3.1
BuildRequires:  libre-graph-api-cpp-qt-client
BuildRequires:	cmake(LibreGraphAPI)
BuildRequires:	cmake(KDSingleApplication-qt6)
BuildRequires:	python-sphinx
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6Xml)
#BuildRequires:	cmake(Qt6WebKitWidgets)
#BuildRequires:	cmake(Qt5WebKit)
BuildRequires:	cmake(Qt6PrintSupport)
BuildRequires:	cmake(Qt6Quick)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Test)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6LinguistTools)
BuildRequires:	cmake(Qt6Keychain)
BuildRequires:	cmake(Qt6Concurrent)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Sql)
#BuildRequires:	cmake(KF5Archive)
#BuildRequires:	cmake(KF5Bookmarks)
#BuildRequires:	cmake(KF5CoreAddons)
#BuildRequires:	cmake(KF5Config)
#BuildRequires:	cmake(KF5ConfigWidgets)
#BuildRequires:	cmake(KF5DBusAddons)
#BuildRequires:	cmake(KF5KIO)
#BuildRequires:	cmake(KF5KDELibs4Support)
#BuildRequires:	cmake(KF5Parts)
#BuildRequires:	cmake(KF5Activities)
#BuildRequires:	cmake(KF5Konq)
BuildRequires:	pkgconfig(check) >= 0.9.5
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(libssh2)
BuildRequires:	pkgconfig(neon) >= 0.29.0
BuildRequires:	pkgconfig(openssl) >= 1.0.0
BuildRequires:	pkgconfig(smbclient)
BuildRequires:	pkgconfig(sqlite3) >= 3.8.0
BuildRequires:	pkgconfig(zlib)
Requires:	%{libname} = %{EVRD}
%rename		%{_lib}owncloud_csync
%rename		ocsync
%rename		mirall

%description
The ownCloud Desktop Client is a tool to synchronize files from ownCloud
Server with your computer.

%files
%doc COPYING README.md
%config(noreplace) %{_sysconfdir}/ownCloud/sync-exclude.lst
%{_bindir}/owncloud
%{_bindir}/owncloudcmd
%{_iconsdir}/hicolor/*/*/*.png
%{_datadir}/applications/owncloud.desktop
%{_datadir}/caja-python/extensions/syncstate-ownCloud.py
%{_datadir}/nemo-python/extensions/syncstate-ownCloud.py
%{_datadir}/nautilus-python/extensions/syncstate-ownCloud.py
%{_datadir}/kservices5/ownclouddolphinactionplugin.desktop

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Shared library for ownCloud client
Group:		System/Libraries
Requires:	%{libowncloud_csync} = %{EVRD}
Conflicts:	%{_lib}owncloudsync1 < %{EVRD}

%description -n %{libname}
Shared library for ownCloud client.

%files -n %{libname}
%{_libdir}/libowncloudsync.so.%{vversion}
%{_libdir}/libowncloudsync.so.%{major}
%{_libdir}/libownclouddolphinpluginhelper.so
%{_libdir}/plugins/*.so
%{_libdir}/plugins/kf5/overlayicon/*.so
%{_libdir}/libowncloudResources.so.%{major}
%{_libdir}/libowncloudResources.so.%{vversion}

#----------------------------------------------------------------------------

%package -n %{libowncloud_csync}
Summary:	Shared library for ownCloud client
Group:		System/Libraries
Conflicts:	%{_lib}owncloudsync1 < %{EVRD}

%description -n %{libowncloud_csync}
Shared library for ownCloud client.

%files -n %{libowncloud_csync}
%doc COPYING *.md
%{_libdir}/libowncloud_csync.so.%{major}
%{_libdir}/libowncloud_csync.so.%{vversion}

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Shared library for ownCloud client
Group:		Development/Other
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}

%description -n %{devname}
This package contains development files for %{name}.

%files -n %{devname}
%doc COPYING *.md
%{_includedir}/ownCloud
%{_libdir}/libowncloud_csync.so
%{_libdir}/libowncloudsync.so
%{_libdir}/libowncloudResources.so
%{_libdir}/cmake/ownCloud/
%{_datadir}/mime/packages/owncloud.xml

#-----------------------------------------------------------------------------

%prep
%setup -qn ownCloud-%{version}
%autopatch -p1


%build
%cmake	-DINOTIFY_LIBRARY="%{_libdir}/libc.so" \
	-DWITH_DOC="True" \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DCMAKE_INSTALL_LIBDIR=%{_libdir} \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir}/%{name}    

%make_build


%install
%make_install -C build
#chmod +x %{buildroot}%{_datadir}/nemo-python/extensions/syncstate-ownCloud.py
#chmod +x %{buildroot}%{_datadir}/nautilus-python/extensions/syncstate-ownCloud.py

# Dirty fix
#pushd %{buildroot}%{_libdir}
#cp owncloud/libocsync.so.%{major} libocsync.so.%{major}
#popd



# We use our macro to pick up docs
rm -rf %{buildroot}%{_docdir}/client/

# Fix perms
#chmod -x %{buildroot}%{_datadir}/nautilus-python/extensions/syncstate-ownCloud.py
#chmod -x %{buildroot}%{_datadir}/nemo-python/extensions/syncstate-ownCloud.py
