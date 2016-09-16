# TODO
# - -rt subpackage? -lang subpackage?
#
# Conditional build:
%bcond_with	lua		# LUA

Summary:	Vim-fork focused on extensibility and agility
Name:		neovim
Version:	0.1.5
Release:	0.2
License:	Apache v2.0
Group:		Applications/Editors/Vim
Source0:	https://github.com/neovim/neovim/archive/v%{version}/%{name}-%{version}.tar.gz
URL:		https://neovim.io/
Source1:	%{name}.desktop
Source2:	%{name}.svg
BuildRequires:	cmake >= 2.8.7
BuildRequires:	fdupes
BuildRequires:	gcc >= 6:4.4
BuildRequires:	hicolor-icon-theme
BuildRequires:	jemalloc-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtermkey-devel
BuildRequires:	libuv-devel
BuildRequires:	msgpack-devel >= 1.2.0
BuildRequires:	pkgconfig
#BuildRequires:	pkgconfig(vterm)
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	unibilium-devel
%if %{with lua}
BuildRequires:	lua51-BitOp
BuildRequires:	lua51-LPeg
BuildRequires:	lua51-mpack
BuildRequires:	luajit-devel
%endif
Requires:	desktop-file-utils
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Suggests:	python-neovim
Suggests:	python3-neovim
Suggests:	xsel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix	/usr/local

%description
Neovim is a refactor - and sometimes redactor - in the tradition of
Vim, which itself derives from Stevie. It is not a rewrite, but a
continuation and extension of Vim. Many rewrites, clones, emulators
and imitators exist; some are very clever, but none are Vim. Neovim
strives to be a superset of Vim, notwithstanding some intentionally
removed misfeatures; excepting those few and carefully-considered
excisions, Neovim is Vim. It is built for users who want the good
parts of Vim, without compromise, and more.

%prep
%setup -q

%if 0
# Remove __DATE__ and __TIME__.
BUILD_TIME=$(LC_ALL=C date -ur %{_sourcedir}/%{name}.changes +'%{H}:%{M}')
BUILD_DATE=$(LC_ALL=C date -ur %{_sourcedir}/%{name}.changes +'%{b} %{d} %{Y}')
sed -i "s/__TIME__/\"$BUILD_TIME\"/" $(grep -rl '__TIME__')
sed -i "s/__DATE__/\"$BUILD_DATE\"/" $(grep -rl '__DATE__')
%endif

%build
%if 0
%cmake \
	-DLUA_PRG=%{_bindir}/lua \
	-DUSE_BUNDLED=OFF		\
	-DLUAJIT_USE_BUNDLED=OFF \
	-DENABLE_JEMALLOC=ON \
\
	-DUSE_BUNDLED_JEMALLOC=ON \
	-DUSE_BUNDLED_UNIBILIUM=ON \
	-DUSE_BUNDLED_LIBTERMKEY=ON \
	-DUSE_BUNDLED_LIBVTERM=ON \
	-DUSE_BUNDLED_LIBUV=ON \
	-DUSE_BUNDLED_MSGPACK=ON \
	-DUSE_BUNDLED_LUAJIT=ON \
	-DUSE_BUNDLED_LUAROCKS=ON \
	-DUSE_BUNDLED_LUV=ON \

%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_iconsdir}/hicolor/scalable/apps}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/neovim.desktop
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/scalable/apps/neovim.svg

%find_lang nvim

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%update_icon_cache hicolor
%banner -e -o %{name} << 'EOF'

The Neovim executable is called 'nvim'. To use your existing Vim
configuration:
    ln -s ~/.vim ~/.config/nvim
    ln -s ~/.vimrc ~/.config/nvim/init.vim
See ':help nvim' for more information on Neovim.

If you want support for Python plugins such as YouCompleteMe, you need
to install a Python module in addition to Neovim itself.

See ':help provider-python' or this page for more information:
    http://neovim.io/doc/user/provider.html

If you have any questions, have a look at:
    https://github.com/neovim/neovim/wiki/FAQ.
EOF

%postun
%update_desktop_database
%update_icon_cache hicolor

%files -f nvim.lang
%defattr(644,root,root,755)
%doc BACKERS.md CONTRIBUTING.md LICENSE README.md
%attr(755,root,root) %{_bindir}/nvim
%{_datadir}/nvim
%{_desktopdir}/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.svg
%{_mandir}/man1/nvim.1*
