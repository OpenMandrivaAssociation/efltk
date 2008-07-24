%define name	efltk
%define version	2.0.7
%define release	%mkrel 4

%define major		2.0
%define libname		%mklibname %{name} %major
%define develname	%mklibname %{name} -d

Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
Source: 	%{name}-%{version}.tar.gz
Summary:	A stable, small and fast cross-platform GUI ToolKit
URL: 		http://ede.sourceforge.net
License: 	LGPLv2+
Group: 		System/Libraries
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: 	gettext
BuildRequires:	libx11-devel
BuildRequires:	libxext-devel
BuildRequires:	freetype2-devel
BuildRequires:	libz-devel
BuildRequires:	libxrender-devel
BuildRequires:	fontconfig-devel
BuildRequires:	x11-proto-devel
BuildRequires:	xft2-devel 
BuildRequires:	mesagl-devel
BuildRequires:	mesaglu-devel
BuildRequires:	jpeg-devel
BuildRequires:	libpng-devel 

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
Requires: 	%{libname} = %{version}-%{release}
Provides:	efltk-devel
Obsoletes:	%{_lib}efltk2.0-devel

%description -n %{develname}
The efltk-devel package contains the header files and libraries needed
to develop programs that use the eFLTK libraries.

%package themes
Summary: Themes for eFLTK
Version: 	%{version}
Release: 	%{release}
Group: 		System/Libraries
Requires: 	%{libname} = %{version}

%description themes
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
%setup -q -n %{name}

%build
%configure --enable-xft --disable-mysql --disable-unixODBC --enable-opengl --enable-utf8 --enable-plugins
make

%install
# Why is this needed?
# AdamW - install stage breaks without it. I tested. 2007/06
install -d %{buildroot}/%{_prefix}
install -d %{buildroot}/%{_bindir}
install -d %{buildroot}/%{_includedir}
install -d %{buildroot}/%{_libdir}

%makeinstall
# I have a problem with locale
rm -fr %{buildroot}/%{_datadir}/locale/

%multiarch_binaries %{buildroot}%{_bindir}/efltk-config

%find_lang %name

%clean
rm -fr %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -n %{libname}
%{_libdir}/lib*.so.%{major}*

%files -n efluid
%defattr(-, root, root)
%{_bindir}/efluid

%files -n ecalc
%defattr(-, root, root)
%{_bindir}/ecalc

%files -n etranslate
%defattr(-, root, root)
%{_bindir}/etranslate

%files themes
%defattr(-, root, root)
%{_libdir}/fltk/*.theme

%files  -f %{name}.lang -n %{develname}
%defattr(-, root, root)
%doc doc/*
%{_libdir}/lib*.so
%{_includedir}/*
%multiarch %{_bindir}/multiarch-*-linux/*
%{_bindir}/efltk-config

