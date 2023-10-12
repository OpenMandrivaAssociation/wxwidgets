# disable python bytecompile outside python dirs
%global _python_bytecompile_extra 0

%bcond_without gtk
%bcond_without qt
%bcond_without motif
# FIXME wine build is broken
%bcond_with wine

%define oname	wxWidgets

%define api	%(echo %{version} |cut -d. -f1-2)
%define major	0
%define apind	%(echo %{api} |tr -d .)
%define dev	%mklibname wxu %{api} -d
%define qtdev	%mklibname wxqtu %{api} -d
%define gtkdev	%mklibname wxgtku %{api} -d
%define motifdev	%mklibname wxmotifu %{api} -d

%define gitdate %{nil}

Summary:        The Wx widgets library
Name:           wxwidgets
Version:        3.2.3
Release:        1
License:        wxWidgets Library Licence
Group:          System/Libraries
URL:            http://www.wxwidgets.org/
Source0:        https://github.com/wxWidgets/wxWidgets/releases/download/v%{version}/wxWidgets-%{version}.tar.bz2
Source1:	https://github.com/wxWidgets/Catch/archive/ee4acb6ae6e32a02bc012d197aa82b1ca7a493ab/catch.tar.gz
Patch0:         wxWidgets-2.9.5-fix-linking.patch
Patch1:         wxWidgets-2.9.5-multiarch-includes.patch
# Originally from Gentoo
Patch2:         wxWidgets-3.0.4-collision.patch
# From Fedora
Patch3:		wxGTK3-3.0.3-abicheck.patch
Patch4:		wxwidgets-3.1.5-qt-flags.patch

#BuildRequires:  bakefile
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:	jbig-devel
BuildRequires:  pkgconfig(libtiff-4)
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(cppunit)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
%if %{with qt}
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5OpenGL)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Test)
%endif
%if %{with gtk}
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(webkit2gtk-4.0)
%endif
%if %{with wine}
BuildRequires:	wine-devel
%endif
%if %{with motif}
BuildRequires:	motif-devel
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xmu)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xt)
%endif
BuildRequires:  pkgconfig(libmspack)
BuildRequires:  pkgconfig(libnotify) >= 0.7
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  pkgconfig(cppunit)
BuildRequires:  pkgconfig(cairo)
BuildRequires:	pkgconfig(libsecret-1)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(liblzma)
Provides:	wxwidgets%{api} = %{EVRD}
%rename		wxgtk3.1
%rename		wxqt3.1

%description
wxWidgets is a free C++ library for cross-platform GUI development.
With wxWidgets, you can create applications for different GUIs (Qt, GTK,
Motif/LessTif, MS Windows, Mac) from the same source code.

%global baselibs wx_baseu \\\
wx_baseu_net \\\
wx_baseu_xml
%global wxlibs %{baselibs}

%if %{with gtk}
%global gtklibs \\\
wx_gtk3u_adv \\\
wx_gtk3u_aui \\\
wx_gtk3u_core \\\
wx_gtk3u_gl \\\
wx_gtk3u_html \\\
wx_gtk3u_media \\\
wx_gtk3u_propgrid \\\
wx_gtk3u_qa \\\
wx_gtk3u_ribbon \\\
wx_gtk3u_richtext \\\
wx_gtk3u_stc \\\
wx_gtk3u_xrc \\\
wx_gtk3u_webview
%global wxlibs %{wxlibs} %{gtklibs}
%endif

%if %{with qt}
%global qtlibs \\\
wx_qtu_adv \\\
wx_qtu_aui \\\
wx_qtu_core \\\
wx_qtu_gl \\\
wx_qtu_html \\\
wx_qtu_media \\\
wx_qtu_propgrid \\\
wx_qtu_qa \\\
wx_qtu_ribbon \\\
wx_qtu_richtext \\\
wx_qtu_stc \\\
wx_qtu_xrc
%global wxlibs %{wxlibs} %{qtlibs}
%endif

%if %{with motif}
%global motiflibs \\\
wx_motifu_adv \\\
wx_motifu_aui \\\
wx_motifu_core \\\
wx_motifu_gl \\\
wx_motifu_html \\\
wx_motifu_media \\\
wx_motifu_propgrid \\\
wx_motifu_qa \\\
wx_motifu_ribbon \\\
wx_motifu_richtext \\\
wx_motifu_stc \\\
wx_motifu_xrc
%global wxlibs %{wxlibs} %{motiflibs}
%endif

%{expand:%(for lib in %{wxlibs}; do cat << EOF
%%global libname$lib %%mklibname $lib %{api} %{major}
%%package -n %%{libname$lib}
Summary:        wxWidgets $lib shared library
Group:          System/Libraries
Requires:       %{name}%{api} >= %{EVRD}
EOF
done)}

%{expand:%(for lib in %{wxlibs}; do cat << EOF
%%description -n %%{libname$lib}
This package contains the library needed to run programs dynamically
linked with the wxWidgets.
EOF
done)}

%{expand:%(for lib in %{wxlibs}; do cat << EOF
%%files -n %%{libname$lib}
%{_libdir}/lib$lib-%{api}.so.%{major}{,.*}
%if "$lib" == "wx_gtk3u_webview"
%dir %{_libdir}/wx/%{api}/web-extensions/
%{_libdir}/wx/%{api}/web-extensions/webkit2_extu-%{api}.so
%endif
EOF
done)}

%package -n %{dev}
Summary:	Core (not widget dependent) Development files for wxWidgets
Group:		Development/C++
Requires:	%{expand:%(for lib in %{baselibs}; do echo -n "%%{libname$lib} = %{EVRD} "; done)}

%description -n %{dev}
Core (not widget dependent) Development files for wxWidgets

%package -n %{qtdev}
Summary:        Header files and development documentation for wxQt - unicode
Group:          Development/C++
Requires:	%{expand:%(for lib in %{qtlibs}; do echo -n "%%{libname$lib} = %{EVRD} "; done)}
Requires:	%{dev} = %{EVRD}
Provides:       libwxqtu%{api}-devel = %{EVRD}
Provides:       wxqtu%{api}-devel = %{EVRD}
Provides:       wxqt%{api}-devel = %{EVRD}
Provides:	wxqt-devel = %{EVRD}
Provides:       libwxqt%{api}-devel = %{EVRD}
Provides:       %{name}-devel = %{EVRD}
Requires(post):         update-alternatives
Requires(postun):       update-alternatives

%description -n %{qtdev}
Header files for the unicode enabled version of wxQt, the Qt port of
the wxWidgets library.

%package -n %{motifdev}
Summary:        Header files and development documentation for wxMotif - unicode
Group:          Development/C++
Requires:	%{expand:%(for lib in %{motiflibs}; do echo -n "%%{libname$lib} = %{EVRD} "; done)}
Requires:	%{dev} = %{EVRD}
Provides:       libwxmotifu%{api}-devel = %{EVRD}
Provides:       wxmotifu%{api}-devel = %{EVRD}
Provides:       wxmotif%{api}-devel = %{EVRD}
Provides:	wxmotif-devel = %{EVRD}
Provides:       libwxmotif%{api}-devel = %{EVRD}
Provides:       %{name}-devel = %{EVRD}
Requires(post):         update-alternatives
Requires(postun):       update-alternatives

%description -n %{motifdev}
Header files for the unicode enabled version of wxMotif, the Motif port of
the wxWidgets library.

%package -n %{gtkdev}
Summary:        Header files and development documentation for wxGTK - unicode
Group:          Development/C++
Requires:	%{expand:%(for lib in %{gtklibs}; do echo -n "%%{libname$lib} = %{EVRD} "; done)}
Requires:	%{dev} = %{EVRD}
Provides:       libwxgtku%{api}-devel = %{EVRD}
Provides:       wxgtku%{api}-devel = %{EVRD}
Provides:       wxgtk%{api}-devel = %{EVRD}
Provides:	wxgtk-devel = %{EVRD}
Provides:       libwxgtk%{api}-devel = %{EVRD}
Provides:       %{name}-devel = %{EVRD}
Requires(post):         update-alternatives
Requires(postun):       update-alternatives

%description -n %{gtkdev}
Header files for the unicode enabled version of wxGTK, the GTK+ port of
the wxWidgets library.

%prep
%setup -qn %{oname}-%{version}
rm -rf 3rdparty/catch
cd 3rdparty
tar xf %{S:1}
mv Catch-* catch
cd ..
%autopatch -p1

# fix plugin dir for 64-bit
sed -i -e 's|/lib|/%{_lib}|' src/unix/stdpaths.cpp

find samples demos -name .cvsignore -delete

aclocal --force -I$PWD/build/aclocal
autoconf -f
libtoolize --copy --force

# This code dereferences type-punned pointers like there's no tomorrow.
export CFLAGS="%{optflags} -fno-strict-aliasing"
export CXXFLAGS="%{optflags} -fno-strict-aliasing"

# --disable-optimise prevents our $RPM_OPT_FLAGS being overridden
# (see OPTIMISE in configure).
# --enable-utf8 breaks python-wxwidgets
%global common_options \\\
	--prefix=%{_prefix} \\\
	--libdir=%{_libdir} \\\
	--enable-intl \\\
	--enable-unicode \\\
	--with-opengl \\\
	--with-sdl \\\
	--with-libmspack \\\
	--with-libpng=sys \\\
	--with-libjpeg=sys \\\
	--with-libtiff=sys \\\
	--with-zlib=sys \\\
	--with-regex=sys \\\
	--with-liblzma=yes \\\
	--with-libnotify=sys \\\
	--with-expat=sys \\\
	--with-cxx=17 \\\
	--enable-cxx11 \\\
	--disable-utf8 \\\
	--enable-repro-build \\\
	--enable-pch \\\
	--disable-optimise \\\
	--enable-calendar \\\
	--enable-compat28 \\\
	--enable-controls \\\
	--enable-msgdlg \\\
	--enable-dirdlg \\\
	--enable-numberdlg \\\
	--enable-splash \\\
	--enable-textdlg \\\
	--enable-graphics_ctx \\\
	--enable-grid \\\
	--enable-catch_segvs \\\
	--enable-mediactrl \\\
	--enable-dataviewctrl \\\
	--disable-permissive \\\
	--enable-ipv6 \\\
	--enable-plugins \\\
	--enable-xlocale \\\
	--enable-config \\\
	--enable-protocols \\\
	--enable-ftp \\\
	--enable-http \\\
	--enable-fileproto \\\
	--enable-sockets \\\
	--enable-dataobj \\\
	--enable-ipc \\\
	--enable-baseevtloop \\\
	--enable-epollloop \\\
	--enable-selectloop \\\
	--enable-any \\\
	--enable-arcstream \\\
	--enable-base64 \\\
	--enable-backtrace \\\
	--enable-cmdline \\\
	--enable-datetime \\\
	--enable-debugreport \\\
	--enable-dialupman \\\
	--enable-dynlib \\\
	--enable-dynamicloader \\\
	--enable-exceptions \\\
	--enable-ffile \\\
	--enable-file \\\
	--enable-filehistory \\\
	--enable-filesystem \\\
	--enable-fontenum \\\
	--enable-fontmap \\\
	--enable-fs_archive \\\
	--enable-fs_inet \\\
	--enable-fs_zip \\\
	--enable-fsvolume \\\
	--enable-fswatcher \\\
	--enable-geometry \\\
	--enable-log \\\
	--enable-longlong \\\
	--enable-mimetype \\\
	--enable-printfposparam \\\
	--enable-secretstore \\\
	--enable-snglinst \\\
	--enable-sound \\\
	--enable-stdpaths \\\
	--enable-stopwatch \\\
	--enable-streams \\\
	--enable-sysoptions \\\
	--enable-tarstream \\\
	--enable-textbuf \\\
	--enable-textfile \\\
	--enable-timer \\\
	--enable-variant \\\
	--enable-zipstream \\\
	--enable-url \\\
	--enable-protocol \\\
	--enable-protocol-http \\\
	--enable-protocol-ftp \\\
	--enable-protocol-file \\\
	--enable-threads \\\
	--enable-docview \\\
	--enable-help \\\
	--enable-html \\\
	--enable-htmlhelp \\\
	--enable-xrc \\\
	--enable-aui \\\
	--enable-propgrid \\\
	--enable-ribbon \\\
	--enable-stc \\\
	--enable-constraints \\\
	--enable-loggui \\\
	--enable-logwin \\\
	--enable-logdialog \\\
	--enable-mdi \\\
	--enable-mdidoc \\\
	--enable-mediactrl \\\
	--enable-richtext \\\
	--enable-postscript \\\
	--enable-printarch \\\
	--enable-svg \\\
	--enable-webview \\\
	--enable-graphics_ctx \\\
	--enable-clipboard \\\
	--enable-dnd \\\
	--enable-markup \\\
	--enable-accel \\\
	--enable-actindicator \\\
	--enable-addremovectrl \\\
	--enable-animatectrl \\\
	--enable-bannerwindow \\\
	--enable-artstd \\\
	--enable-bmpbutton \\\
	--enable-bmpcombobox \\\
	--enable-button \\\
	--enable-calendar \\\
	--enable-caret \\\
	--enable-checkbox \\\
	--enable-checklst \\\
	--enable-choice \\\
	--enable-choicebook \\\
	--enable-collpane \\\
	--enable-colourpicker \\\
	--enable-combobox \\\
	--enable-comboctrl \\\
	--enable-commandlinkbutton \\\
	--enable-dataviewctrl \\\
	--enable-datepick \\\
	--enable-detect_sm \\\
	--enable-dirpicker \\\
	--enable-display \\\
	--enable-editablebox \\\
	--enable-filectrl \\\
	--enable-filepicker \\\
	--enable-fontpicker \\\
	--enable-gauge \\\
	--enable-grid \\\
	--enable-headerctrl \\\
	--enable-hyperlink \\\
	--enable-imaglist \\\
	--enable-infobar \\\
	--enable-listbook \\\
	--enable-listbox \\\
	--enable-listctrl \\\
	--enable-notebook \\\
	--enable-notifmsg \\\
	--enable-odcombobox \\\
	--enable-popupwin \\\
	--enable-prefseditor \\\
	--enable-privatefonts \\\
	--enable-radiobox \\\
	--enable-radiobtn \\\
	--enable-richmsgdlg \\\
	--enable-richtooltip \\\
	--enable-rearrangectrl \\\
	--enable-sash \\\
	--enable-scrollbar \\\
	--enable-searchctrl \\\
	--enable-slider \\\
	--enable-spinbtn \\\
	--enable-spinctrl \\\
	--enable-splitter \\\
	--enable-statbmp \\\
	--enable-statbox \\\
	--enable-statline \\\
	--enable-stattext \\\
	--enable-statusbar \\\
	--enable-taskbaricon \\\
	--enable-tbarnative \\\
	--enable-textctrl \\\
	--enable-timepick \\\
	--enable-tipwindow \\\
	--enable-togglebtn \\\
	--enable-toolbar \\\
	--enable-toolbook \\\
	--enable-treebook \\\
	--enable-treectrl \\\
	--enable-treelist \\\
	--enable-commondlg \\\
	--enable-aboutdlg \\\
	--enable-choicedlg \\\
	--enable-coldlg \\\
	--enable-filedlg \\\
	--enable-finddlg \\\
	--enable-fontdlg \\\
	--enable-dirdlg \\\
	--enable-msgdlg \\\
	--enable-numberdlg \\\
	--enable-splash \\\
	--enable-textdlg \\\
	--enable-tipdlg \\\
	--enable-progressdlg \\\
	--enable-wizarddlg \\\
	--enable-menus \\\
	--enable-miniframe \\\
	--enable-tooltips \\\
	--enable-splines \\\
	--enable-mousewheel \\\
	--enable-validators \\\
	--enable-busyinfo \\\
	--enable-hotkey \\\
	--enable-joystick \\\
	--enable-dragimage \\\
	--enable-uiactionsim \\\
	--enable-dctransform \\\
	--enable-webviewwebkit \\\
	--enable-palette \\\
	--enable-image \\\
	--enable-gif \\\
	--enable-pcx \\\
	--enable-tga \\\
	--enable-iff \\\
	--enable-pnm \\\
	--enable-xpm \\\
	--enable-ico_cur \\\
	--enable-autoidman \\\
	--enable-std_containers_compat \\\
	--enable-arcstream \\\
	--disable-rpath

%if %{with gtk}
mkdir build-gtk
cd build-gtk
# In OMV %%configure passes disable-static options by default to ensure, we have shared libraries. 
# This broke build for this package, because it see it as: unrecognized options: --disable-static, --disable-silent-rules
# Solution is below:
CC="%{__cc}" CXX="%{__cxx}" ../configure \
	%{common_options} \
	--with-gtk=3
cd ..
%endif

%if %{with qt}
mkdir build-qt
cd build-qt
CC="%{__cc}" CXX="%{__cxx}" ../configure \
	%{common_options} \
	--with-qt
cd ..
%endif

%if %{with wine}
mkdir build-wine
cd build-wine
CC="winegcc" CXX="wineg++" WINDRES="wrc" ../configure \
	%{common_options} \
	--with-wine
cd ..
%endif

%if %{with motif}
mkdir build-motif
cd build-motif
CC="%{__cc}" CXX="%{__cxx}" ../configure \
	%{common_options} \
	--with-motif
cd ..
%endif

find . -name Makefile |xargs sed -i -e 's|--version-script|--undefined-version,--version-script|g'

%build
%if %{with gtk}
%make_build -C build-gtk
%endif

%if %{with wine}
%make_build -C build-wine
%endif

%if %{with motif}
%make_build -C build-motif
%endif

%if %{with qt}
%make_build -C build-qt
%endif

# Why isn't this this part of the main build? Need to investigate.
%make_build -C locale allmo

#gw prepare samples
pushd build-qt/demos
        make clean
        rm -f makefile* demos.bkl
popd

pushd build-qt/samples
        make clean
        rm -f makefile* samples.bkl
popd

find build-qt/demos build-qt/samples -name Makefile|xargs perl -pi -e 's^CXXC =.*^CXXC=\$(CXX) `wx-config --cflags`^'
find build-qt/demos build-qt/samples -name Makefile|xargs perl -pi -e 's^EXTRALIBS =.*^EXTRALIBS=^'
find build-qt/demos build-qt/samples -name Makefile|xargs perl -pi -e 's^SAMPLES_RPATH_FLAG =.*^SAMPLES_RPATH_FLAG=^'

%install
%if %{with wine}
%make_install -C build-wine
%endif

%if %{with motif}
%make_install -C build-motif
%endif

%if %{with gtk}
%make_install -C build-gtk
%endif

%if %{with qt}
%make_install -C build-qt
%endif

# dummy translation file
find %{buildroot} -name "wxmsw.mo" -delete

ln -s wx-config-%{api} %{buildroot}%{_bindir}/wx-config

%find_lang wxstd-%{api}

%post -n %{dev}
ln -sf %{_bindir}/wxrc-%{api} %{_bindir}/wxrc

%postun -n %{dev}
rm -f %{_bindir}/wxrc

%post -n %{qtdev}
ln -sf %{_libdir}/wx/config/qt-unicode-%{api} %{_bindir}/wx-config-%{api}
ln -sf %{_libdir}/wx/config/qt-unicode-%{api} %{_bindir}/wx-config

%postun -n %{qtdev}
if [ "$1" -eq "0" ]; then
	rm -f %{_bindir}/wx-config-%{api}
	rm -f %{_bindir}/wx-config
fi

%post -n %{gtkdev}
ln -sf %{_libdir}/wx/config/gtk3-unicode-%{api} %{_bindir}/wx-config-%{api}
ln -sf %{_libdir}/wx/config/gtk3-unicode-%{api} %{_bindir}/wx-config

%postun -n %{gtkdev}
if [ "$1" -eq "0" ]; then
	rm -f %{_bindir}/wx-config-%{api}
	rm -f %{_bindir}/wx-config
fi

%post -n %{motifdev}
ln -sf %{_libdir}/wx/config/motif-unicode-%{api} %{_bindir}/wx-config-%{api}
ln -sf %{_libdir}/wx/config/motif-unicode-%{api} %{_bindir}/wx-config

%postun -n %{motifdev}
if [ "$1" -eq "0" ]; then
	rm -f %{_bindir}/wx-config-%{api}
	rm -f %{_bindir}/wx-config
fi

%files -f wxstd-%{api}.lang
%doc README.md

%files -n %{dev}
%doc samples/ docs/ demos/
%ghost %{_bindir}/wx-config
%ghost %{_bindir}/wx-config-%{api}
%ghost %{_bindir}/wxrc
%{_bindir}/wxrc-%{api}
%{_includedir}/wx-%{api}/
%if %{with qt}
%exclude %{_includedir}/wx-%{api}/wx/qt
%endif
%if %{with gtk}
%exclude %{_includedir}/wx-%{api}/wx/gtk
%endif
%if %{with motif}
%exclude %{_includedir}/wx-%{api}/wx/motif
%endif
%dir %{_libdir}/wx/
%dir %{_libdir}/wx/include/
%dir %{_libdir}/wx/config
%{_libdir}/libwx_baseu-%{api}.so
%{_libdir}/libwx_baseu_net-%{api}.so
%{_libdir}/libwx_baseu_xml-%{api}.so
%{_datadir}/bakefile/presets/wx*
%{_datadir}/aclocal/wxwin%{apind}.m4
%{_libdir}/wx/%{api}/sound_sdlu-%{api}.so

%if %{with qt}
%files -n %{qtdev}
%dir %{_libdir}/wx/include/qt-unicode-%{api}/
%dir %{_libdir}/wx/include/qt-unicode-%{api}/wx/
%{_libdir}/wx/config/qt-unicode-%{api}
%{_libdir}/wx/include/qt-unicode-%{api}/wx/setup.h
%{_includedir}/wx-%{api}/wx/qt
%{_libdir}/libwx_qtu_adv-%{api}.so
%{_libdir}/libwx_qtu_aui-%{api}.so
%{_libdir}/libwx_qtu_core-%{api}.so
%{_libdir}/libwx_qtu_gl-%{api}.so
%{_libdir}/libwx_qtu_html-%{api}.so
%{_libdir}/libwx_qtu_media-%{api}.so
%{_libdir}/libwx_qtu_propgrid-%{api}.so
%{_libdir}/libwx_qtu_qa-%{api}.so
%{_libdir}/libwx_qtu_ribbon-%{api}.so
%{_libdir}/libwx_qtu_richtext-%{api}.so
%{_libdir}/libwx_qtu_stc-%{api}.so
%{_libdir}/libwx_qtu_xrc-%{api}.so
%endif

%if %{with motif}
%files -n %{motifdev}
%dir %{_libdir}/wx/include/motif-unicode-%{api}/
%dir %{_libdir}/wx/include/motif-unicode-%{api}/wx/
%{_libdir}/wx/config/motif-unicode-%{api}
%{_libdir}/wx/include/motif-unicode-%{api}/wx/setup.h
%{_includedir}/wx-%{api}/wx/motif
%{_libdir}/libwx_motifu_adv-%{api}.so
%{_libdir}/libwx_motifu_aui-%{api}.so
%{_libdir}/libwx_motifu_core-%{api}.so
%{_libdir}/libwx_motifu_gl-%{api}.so
%{_libdir}/libwx_motifu_html-%{api}.so
%{_libdir}/libwx_motifu_media-%{api}.so
%{_libdir}/libwx_motifu_propgrid-%{api}.so
%{_libdir}/libwx_motifu_qa-%{api}.so
%{_libdir}/libwx_motifu_ribbon-%{api}.so
%{_libdir}/libwx_motifu_richtext-%{api}.so
%{_libdir}/libwx_motifu_stc-%{api}.so
%{_libdir}/libwx_motifu_xrc-%{api}.so
%endif

%if %{with gtk}
%files -n %{gtkdev}
%dir %{_libdir}/wx/include/gtk3-unicode-%{api}/
%dir %{_libdir}/wx/include/gtk3-unicode-%{api}/wx/
%{_libdir}/wx/config/gtk3-unicode-%{api}
%{_libdir}/wx/include/gtk3-unicode-%{api}/wx/setup.h
%{_includedir}/wx-%{api}/wx/gtk
%{_libdir}/libwx_gtk3u_adv-%{api}.so
%{_libdir}/libwx_gtk3u_aui-%{api}.so
%{_libdir}/libwx_gtk3u_core-%{api}.so
%{_libdir}/libwx_gtk3u_gl-%{api}.so
%{_libdir}/libwx_gtk3u_html-%{api}.so
%{_libdir}/libwx_gtk3u_media-%{api}.so
%{_libdir}/libwx_gtk3u_propgrid-%{api}.so
%{_libdir}/libwx_gtk3u_qa-%{api}.so
%{_libdir}/libwx_gtk3u_ribbon-%{api}.so
%{_libdir}/libwx_gtk3u_richtext-%{api}.so
%{_libdir}/libwx_gtk3u_stc-%{api}.so
%{_libdir}/libwx_gtk3u_webview-%{api}.so
%{_libdir}/libwx_gtk3u_xrc-%{api}.so
%endif
