# TODO
# - -rt subpackage? -lang subpackage?
#
# Conditional build:
%bcond_with	prefer_lua		# Prefer Lua over LuaJit

%ifnarch %{ix86} %{x8664} %{arm} aarch64 mips mips64 mipsel ppc
%define		with_prefer_lua	1
%endif

%if %{with prefer_lua}
%define		lpeg_library	/usr/%{_lib}/lua/5.1/lpeg.so
%define		luv_includedir	/usr/include/lua5.1
%define		luv_library	/usr/%{_lib}/lua/5.1/luv.so
%else
%define		lpeg_library	/usr/%{_lib}/luajit/2.1/lpeg.so
%define		luv_includedir	/usr/include/luajit-2.1
%define		luv_library	/usr/%{_lib}/luajit/2.1/luv.so
%endif

Summary:	Vim-fork focused on extensibility and agility
Name:		neovim
Version:	0.11.4
Release:	1
License:	Apache v2.0
Group:		Applications/Editors/Vim
# Source0Download: https://github.com/neovim/neovim/releases
Source0:	https://github.com/neovim/neovim/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	0555b24bdb9770ab451d1129df04ceb9
URL:		https://neovim.io/
Source2:	%{name}.svg
Patch0:		desktop.patch
Patch1:		build-type.patch
Patch2:		luv.patch
Patch3:		luajit-lua52.patch
BuildRequires:	cmake >= 3.16
BuildRequires:	gcc >= 6:4.4
BuildRequires:	gettext-tools
BuildRequires:	libstdc++-devel
BuildRequires:	libuv-devel >= 1.28.0
BuildRequires:	lua-bitop >= 1.0.2
BuildRequires:	lua-mpack >= 1.0.2
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	tree-sitter-devel >= 0.25.0
BuildRequires:	unibilium-devel >= 2.0.0
BuildRequires:	utf8proc-devel
%if %{with prefer_lua}
BuildRequires:	lua-lpeg
BuildRequires:	lua51
BuildRequires:	lua51-devel
BuildRequires:	lua51-luv-devel >= 1.43.0
%else
BuildRequires:	luajit
BuildRequires:	luajit-devel
BuildRequires:	luajit-lpeg
BuildRequires:	luajit-luv-devel >= 1.43.0
%endif
Requires:	libuv >= 1.28.0
Requires:	%{?with_prefer_lua:lua51}%{!?with_prefer_lua:luajit}-luv
Requires:	lua%{!?with_prefer_lua:jit}-lpeg
Requires:	tree-sitter >= 0.25.0
Suggests:	%{name}-desktop = %{version}-%{release}
Suggests:	neovim-parser-c
Suggests:	neovim-parser-lua
Suggests:	neovim-parser-markdown
Suggests:	neovim-parser-query
Suggests:	neovim-parser-vim
Suggests:	neovim-parser-vimdoc
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

%package desktop
Summary:	Desktop files for Neovim
Group:		Applications/Editors/Vim
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description desktop
Desktop files for Neovim.

%prep
%setup -q
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1 -R
%patch -P 3 -p1

%build
%cmake -B build \
	-DPREFER_LUA=%{!?with_prefer_lua:OFF}%{?with_prefer_lua:ON} \
	-DLUA_PRG=%{!?with_prefer_lua:/usr/bin/luajit}%{?with_prefer_lua:/usr/bin/lua5.1} \
	-DLUA_INCLUDE_DIR=/usr/include/lua5.1 \
	-DUSE_BUNDLED=OFF \
	-DENABLE_JEMALLOC=ON \
	-DLPEG_LIBRARY=%{lpeg_library} \
	-DLUV_INCLUDE_DIR=%{luv_includedir} \
	-DLUV_LIBRARY=%{luv_library} \
	-DENABLE_TRANSLATIONS:BOOL=ON

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{/etc/xdg/nvim,%{_iconsdir}/hicolor/scalable/apps,%{_libdir}/nvim/parser}
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

%post desktop
%update_desktop_database
%update_icon_cache hicolor

%postun desktop
%update_desktop_database
%update_icon_cache hicolor

%files -f nvim.lang
%defattr(644,root,root,755)
%doc CONTRIBUTING.md LICENSE.txt README.md
%dir /etc/xdg/nvim
%config(noreplace) %verify(not md5 mtime size) /etc/xdg/nvim/init.vim
%attr(755,root,root) %{_bindir}/nvim
%{_mandir}/man1/nvim.1*
%{_datadir}/nvim
%dir %{_libdir}/nvim
%dir %{_libdir}/nvim/parser

%files desktop
%defattr(644,root,root,755)
%{_desktopdir}/nvim.desktop
%{_iconsdir}/hicolor/*/apps/nvim.png
%{_iconsdir}/hicolor/*/apps/nvim.svg
