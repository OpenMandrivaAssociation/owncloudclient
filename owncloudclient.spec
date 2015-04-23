%define major 0
%define libname %mklibname owncloudsync %{major}
%define develname %mklibname owncloudsync -d
%define beta beta1

Summary:	ownCloud desktop client
Name:		owncloudclient
Version:	1.8.1
Release:	0.%{beta}.2
License:	GPLv2+
Group:		Archiving/Backup
URL:		http://owncloud.org
Source0:	https://download.owncloud.com/desktop/stable/%{name}-%{version}-%{beta}.tar.bz2
Patch0:		0001-Fix-compilation-with-Qt-5.5.patch
BuildRequires:	cmake
BuildRequires:	qmake5
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(Qt5Core)
BuildRequires:	cmake(Qt5Network)
BuildRequires:	cmake(Qt5Xml)
BuildRequires:	cmake(Qt5WebKitWidgets)
BuildRequires:	cmake(Qt5WebKit)
BuildRequires:	cmake(Qt5PrintSupport)
BuildRequires:	cmake(Qt5Quick)
BuildRequires:	cmake(Qt5Widgets)
BuildRequires:	cmake(Qt5Test)
BuildRequires:	cmake(Qt5DBus)
BuildRequires:	cmake(Qt5LinguistTools)
BuildRequires:	cmake(Qt5Keychain)
# temoraily disable KF5
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
BuildRequires:	pkgconfig(neon)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires:	pkgconfig(openssl)
Requires:       %{libname} = %{EVRD}
%rename mirall

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
%setup -qn %{name}-%{version}-%{beta}
%apply_patches

%build
%cmake_qt5

%make

%install
%makeinstall_std -C build
find %{buildroot}%{_libdir} -name "*.a" -delete

# (tpg) needed symlink
ln -s %{_libdir}/owncloud/libocsync.so.%{version} %{buildroot}%{_libdir}/libocsync.so.%{major}

%files
%doc ChangeLog COPYING
%config(noreplace) %{_sysconfdir}/ownCloud/sync-exclude.lst
%dir %{_datadir}/owncloud
%dir %{_datadir}/owncloud/i18n
%{_bindir}/owncloud
%{_bindir}/owncloudcmd
%{_libdir}/owncloud/libocsync.so.%{major}
%{_libdir}/owncloud/libocsync.so.%{version}
%{_iconsdir}/hicolor/*/*/*.png
%{_datadir}/nautilus-python/extensions/syncstate.py
%{_datadir}/applications/owncloud.desktop
%{_datadir}/owncloud/i18n/*.qm

%files -n %{libname}
%{_libdir}/libowncloudsync.so.%{version}
%{_libdir}/libowncloudsync.so.%{major}
%{_libdir}/libocsync.so.%{major}

%files -n %{develname}
%doc ChangeLog COPYING *.md
%{_includedir}/owncloudsync
%{_libdir}/libowncloudsync.so
%{_libdir}/owncloud/libocsync.so
