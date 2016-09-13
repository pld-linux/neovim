# TODO
# - -rt subpackage? -lang subpackage?
Summary:	Vim-fork focused on extensibility and agility
Name:		neovim
Version:	0.1.5
Release:	0.1
License:	Apache v2.0
Group:		Applications/Editors/Vim
Source0:	https://github.com/neovim/neovim/archive/v%{version}/%{name}-%{version}.tar.gz
URL:		https://neovim.io/
Source1:	%{name}.desktop
Source2:	%{name}.svg
BuildRequires:	cmake
BuildRequires:	fdupes
BuildRequires:	hicolor-icon-theme
BuildRequires:	jemalloc-devel
BuildRequires:	libmsgpack-devel >= 1.2.0
BuildRequires:	libmsgpackc-devel >= 1.2.0
BuildRequires:	libstdc++-devel
BuildRequires:	libuv-devel
BuildRequires:	lua51-BitOp
BuildRequires:	lua51-LPeg
BuildRequires:	lua51-mpack
BuildRequires:	luajit-devel
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(termkey)
BuildRequires:	pkgconfig(unibilium)
BuildRequires:	pkgconfig(vterm)
BuildRequires:	update-desktop-files
Suggests:	python-neovim
Suggests:	python3-neovim
Suggests:	xsel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

# Remove __DATE__ and __TIME__.
BUILD_TIME=$(LC_ALL=C date -ur %{_sourcedir}/%{name}.changes +'%{H}:%{M}')
BUILD_DATE=$(LC_ALL=C date -ur %{_sourcedir}/%{name}.changes +'%{b} %{d} %{Y}')
sed -i "s/__TIME__/\"$BUILD_TIME\"/" $(grep -rl '__TIME__')
sed -i "s/__DATE__/\"$BUILD_DATE\"/" $(grep -rl '__DATE__')

%build
%cmake \
	-DLUA_PRG=%{_bindir}/lua \
	-DUSE_BUNDLED=OFF		\
	-DLUAJIT_USE_BUNDLED=OFF \
	-DENABLE_JEMALLOC=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}/neovim.desktop
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/scalable/apps/neovim.svg

%find_lang nvim

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database
%icon_theme_cache_post

%postun
%update_desktop_database
%icon_theme_cache_postun

%files -f nvim.lang
%defattr(644,root,root,755)
%doc BACKERS.md CONTRIBUTING.md LICENSE README.md
%attr(755,root,root) %{_bindir}/nvim
%{_datadir}/nvim
%{_desktopdir}/%{name}.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.svg
%{_mandir}/man1/nvim.1*
