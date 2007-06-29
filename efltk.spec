%define cvsversion 0

%define name efltk
%define version 2.0.6

%if %cvsversion
%define release %mkrel 0.%{cvsver}.1
%elseif
%define release %mkrel 3
%endif

%define pakdir %{name}-%{version}
%define date %(echo `LC_ALL="C" date +"%a %b %d %Y"`)
%define cvsver 20060330

%define major 2.0
%define libname %mklibname %{name} %major
%define develname %mklibname %{name} -d

Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
%if %cvsversion
Source:         %{name}-%{cvsver}.tar.bz2
%elseif
Source: 	%{name}-%{version}.tar.bz2
%endif
# From upstream SVN: drop when new version released
Patch0:		efltk-2.0.6-gcc41.patch
Patch1:		efltk-2.0.6-x86_64.patch
# Find libraries when running efluid -c during build - AdamW 2007/06
Patch2:		efltk-2.0.6-findlib.patch

Summary:	A stable, small and fast cross-platform GUI ToolKit
URL: 		http://ede.sourceforge.net
License: 	LGPL
Group: 		System/Libraries

BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: 	gettext
BuildRequires:	libx11-devel libxext-devel freetype2-devel libz-devel libxrender-devel fontconfig-devel x11-proto-devel xft2-devel 
BuildRequires:	mesagl-devel mesaglu-devel jpeg-devel libpng-devel 

%description
Extended Fast Light Toolkit (eFLTK)
is a cross-platform C++ GUI toolkit for UNIX®/Linux® (X11), 
Microsoft® Windows®, and MacOS® X. eFLTK provides modern GUI 
functionality without the bloat and supports 3D graphics via 
OpenGL® and its built-in GLUT emulation. It is currently maintained 
by a small group of developers across the world with a central 
repository on SourceForge.

%package -n %{libname}
Summary: A stable, small and fast cross-platform GUI ToolKit
Version: 	%{version}
Release: 	%{release}
Group: 		System/Libraries
Provides:	%{name} = %{version}

%description -n %{libname}
Extended Fast Light Toolkit (eFLTK)
is a cross-platform C++ GUI toolkit for UNIX®/Linux® (X11), 
Microsoft® Windows®, and MacOS® X. eFLTK provides modern GUI 
functionality without the bloat and supports 3D graphics via 
OpenGL® and its built-in GLUT emulation. It is currently maintained 
by a small group of developers across the world with a central 
repository on SourceForge.

%package -n %{develname}
Summary: Header files and libraries for developing apps which will eFLTK
Version: 	%{version}
Release: 	%{release}
Group: 		Development/C++
Requires: 	%{libname} = %{version}
Provides:	efltk-devel
Obsoletes:	%{_lib}efltk2.0-devel

%description -n %{develname}
The efltk-devel package contains the header files and libraries needed
to develop programs that use the eFLTK libraries.

%package -n efltk-themes
Summary: Themes for eFLTK
Version: 	%{version}
Release: 	%{release}
Group: 		System/Libraries
Requires: 	%{libname} = %{version}

%description -n efltk-themes
This package contains themes which can be used with eFLTK. Note: in
version 2.0.2 these themes don't seem to work.

%package -n efluid
Summary: 	GUI designer for EDE / eFLTK
Version: 	%{version}
Release: 	%{release}
Group: 		Development/C++
Requires: 	%{libname} = %{version}

%description -n efluid
Efluid is a WYSIWYG GUI designer for the eFLTK toolkit. It can generate 
C++ code and export strings for translation in gettext format. It is 
still under development which means that it doesn't support some of the 
features of eFLTK.

%package -n ecalc
Summary: Scientific calculator for EDE
Version: 	%{version}
Release: 	%{release}
Group: 		Graphical desktop/Other
Requires: 	%{libname} = %{version}

%description -n ecalc
Ecalc is a scientific calculator for the Equinox Desktop Environment, made as
a demo of eFLTK toolkit.

%package -n etranslate
Summary: Program interface translation tool for EDE
Version: 	%{version}
Release: 	%{release}
Group: 		Development/Other
Requires: 	%{libname} = %{version}

%description -n etranslate
Etranslate is an editor of gettext (.PO) files. This format is commonly used 
in open-source projects such as EDE to enable localization of programs.

%prep
%if %cvsversion
%setup -q -n %{name}-%{cvsver}
%elseif
%setup -q -n %{name}
%endif
%patch0 -p1 -b .gcc41
%patch1 -p1 -b .x86_64
%patch2 -p1 -b .findlib

%build

%if %cvsversion
autoconf
%endif

%configure --enable-xft --disable-mysql --disable-unixODBC --enable-opengl --enable-utf8 --enable-plugins

make

%install

# Why is this needed?
# AdamW - install stage breaks without it. I tested. 2007/06

install -d $RPM_BUILD_ROOT/%{_prefix}
install -d $RPM_BUILD_ROOT/%{_bindir}
install -d $RPM_BUILD_ROOT/%{_includedir}
install -d $RPM_BUILD_ROOT/%{_libdir}

%makeinstall

# I have a problem with locale
rm -fr $RPM_BUILD_ROOT/%{_datadir}/locale/

%multiarch_binaries $RPM_BUILD_ROOT%{_bindir}/efltk-config

%find_lang %name

%clean
rm -fr $RPM_BUILD_ROOT

%post -n %libname -p /sbin/ldconfig

%postun -n %libname -p /sbin/ldconfig

%files -n %{libname}
%{_libdir}/lib*.so*

%files -n efluid
%defattr(-, root, root)
%{_bindir}/efluid

%files -n ecalc
%defattr(-, root, root)
%{_bindir}/ecalc

%files -n etranslate
%defattr(-, root, root)
%{_bindir}/etranslate

%files -n efltk-themes
%defattr(-, root, root)
%{_libdir}/fltk/*.theme

%files  -f %{name}.lang -n %{develname}
%defattr(-, root, root)
%doc doc/*
%defattr(-, root, root)
%{_includedir}/*
%multiarch %{_bindir}/multiarch-*-linux/*
%{_bindir}/*
#%{_libdir}/*.a
#%{_libdir}/*.la

