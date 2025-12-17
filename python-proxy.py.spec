#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_with	python3 # CPython 3.x module (more robust version built from python3-proxy.py.spec)

Summary:	Lightweight HTTP, HTTPS, WebSockets Proxy Server in Python
Summary(pl.UTF-8):	Lekki serwer proxy HTTP, HTTPS i WebSockets w Pythonie
Name:		python-proxy.py
# keep 0.x here for python2 support
Version:	0.3
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/proxy-py/
Source0:	https://files.pythonhosted.org/packages/source/p/proxy-py/proxy.py-%{version}.tar.gz
# Source0-md5:	ce6d6500ae1c67baf682fcc5bc2ef62f
URL:		https://pypi.org/project/proxy.py/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	python3-setuptools
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lightweight HTTP, HTTPS, WebSockets Proxy Server in a single Python
file. Features:
- No external dependency other than standard Python library
- Support for http, https and websockets request proxy
- Optimize for large file uploads and downloads
- IPv4 and IPv6 support
- Basic authentication support

%description -l pl.UTF-8
Lekki serwer proxy HTTP, HTTPS i WebSockets w pojedynczym pliku
Pythona. Cechy:
- brak zewnętrznych zależności innych niż biblioteka standardowa
  Pythona
- obsługa przekazywania żądań http, https, websockets
- zoptymalizowany pod kątem przesyłania i pobierania dużych plików
- obsługa IPv4 i IPv6
- obsługa uwierzytelniania Basic

%package -n python3-proxy.py
Summary:	Lightweight HTTP, HTTPS, WebSockets Proxy Server in Python
Summary(pl.UTF-8):	Lekki serwer proxy HTTP, HTTPS i WebSockets w Pythonie
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.7

%description -n python3-proxy.py
Lightweight HTTP, HTTPS, WebSockets Proxy Server in a single Python
file. Features:
- No external dependency other than standard Python library
- Support for `http`, `https` and `websockets` request proxy
- Optimize for large file uploads and downloads
- IPv4 and IPv6 support
- Basic authentication support

%description -n python3-proxy.py -l pl.UTF-8
Lekki serwer proxy HTTP, HTTPS i WebSockets w pojedynczym pliku
Pythona. Cechy:
- brak zewnętrznych zależności innych niż biblioteka standardowa
  Pythona
- obsługa przekazywania żądań http, https, websockets
- zoptymalizowany pod kątem przesyłania i pobierania dużych plików
- obsługa IPv4 i IPv6
- obsługa uwierzytelniania Basic

%prep
%setup -q -n proxy.py-%{version}

%build
%if %{with python2}
%py_build
%endif

%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean

%{__mv} $RPM_BUILD_ROOT%{_bindir}/proxy.py{,-2}
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/proxy.py{,-3}
ln -sf proxy.py-3 $RPM_BUILD_ROOT%{_bindir}/proxy.py
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/proxy.py-2
%{py_sitescriptdir}/proxy.py[co]
%{py_sitescriptdir}/proxy.py-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-proxy.py
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/proxy.py-3
%{_bindir}/proxy.py
%{py3_sitescriptdir}/proxy.py
%{py3_sitescriptdir}/__pycache__/proxy.cpython-*.py[co]
%{py3_sitescriptdir}/proxy.py-%{version}-py*.egg-info
%endif
