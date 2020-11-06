# TODO
# - -rt subpackage? -lang subpackage?
# - <meta>-xxx keybindings (alt+something) incompatibility
#   https://github.com/neovim/neovim/issues/5576
#
# Conditional build:
%bcond_without	lua		# Prefer Lua over LuaJit

Summary:	Vim-fork focused on extensibility and agility
Name:		neovim
Version:	0.3.8
Release:	1
License:	Apache v2.0
Group:		Applications/Editors/Vim
# Source0Download: https://github.com/neovim/neovim/releases
Source0:	https://github.com/neovim/neovim/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	6b0eda6c3c6261c82f8a61f9c2d85fcd
URL:		https://neovim.io/
Source2:	%{name}.svg
Patch0:		desktop.patch
Patch1:		https://github.com/neovim/neovim/pull/12142.patch
# Patch1-md5:	40bf36c33b4c49270243b39b916e164c
BuildRequires:	cmake >= 2.8.7
BuildRequires:	gcc >= 6:4.4
BuildRequires:	gettext-devel
BuildRequires:	jemalloc-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtermkey-devel
BuildRequires:	libuv-devel
BuildRequires:	libvterm-devel < 0.1.3
BuildRequires:	lua-bitop >= 1.0.2
BuildRequires:	lua-lpeg
BuildRequires:	lua-mpack >= 1.0.2
BuildRequires:	msgpack-devel >= 1.1.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	unibilium-devel
%if %{with lua}
BuildRequires:	lua51
BuildRequires:	lua51-devel
%else
BuildRequires:	luajit-devel
%endif
Requires:	desktop-file-utils
Requires:	gtk-update-icon-cache
Requires:	hicolor-icon-theme
Suggests:	python-neovim
Suggests:	python3-neovim
Suggests:	ruby-neovim
Suggests:	xsel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# gcc 4.0 and better turn on _FORTIFY_SOURCE=2 automatically. This currently
# does not work with Neovim due to some uses of dynamically-sized structures.
# See https://github.com/neovim/neovim/issues/223 for details.
%define		filterout_c	-Wp,-D_FORTIFY_SOURCE=2

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
%patch0 -p1
%patch1 -p1

%build
install -d .deps build
cd .deps
%cmake \
	-DUSE_BUNDLED=OFF \
	-DUSE_BUNDLED_JEMALLOC=OFF \
	-DUSE_BUNDLED_UNIBILIUM=OFF \
	-DUSE_BUNDLED_LIBTERMKEY=OFF \
	-DUSE_BUNDLED_LIBVTERM=OFF \
	-DUSE_BUNDLED_LIBUV=OFF \
	-DUSE_BUNDLED_MSGPACK=OFF \
	-DUSE_BUNDLED_LUAJIT=OFF \
	-DUSE_BUNDLED_LUAROCKS=OFF \
	-DUSE_BUNDLED_LUV=OFF \
	../third-party
%{__make}

cd ../build
%cmake \
	-DLUA_PRG=/usr/bin/lua5.1 \
	-DENABLE_JEMALLOC=ON \
	-DLUAJIT_USE_BUNDLED=OFF \
	-DLIBUV_USE_BUNDLED=OFF \
	-DMSGPACK_USE_BUNDLED=OFF \
	-DUNIBILIUM_USE_BUNDLED=OFF \
	-DLIBTERMKEY_USE_BUNDLED=OFF \
	-DLIBVTERM_USE_BUNDLED=OFF \
	-DJEMALLOC_USE_BUNDLED=OFF \
	..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/etc/xdg/nvim,%{_iconsdir}/hicolor/scalable/apps}
touch $RPM_BUILD_ROOT/etc/xdg/nvim/init.vim
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/scalable/apps/nvim.svg

%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/cs.cp1250
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ja.euc-jp
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ko.UTF-8
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/no
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/pl.UTF-8
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/sk.cp1250
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/zh_CN.UTF-8
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/zh_TW.UTF-8

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
%dir /etc/xdg/nvim
%config(noreplace) %verify(not md5 mtime size) /etc/xdg/nvim/init.vim
%attr(755,root,root) %{_bindir}/nvim
%{_mandir}/man1/nvim.1*
%{_datadir}/nvim
%{_desktopdir}/nvim.desktop
%{_pixmapsdir}/nvim.png
%{_iconsdir}/hicolor/*/apps/nvim.svg
