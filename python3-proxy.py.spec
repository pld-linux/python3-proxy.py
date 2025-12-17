# TODO: doc and tests when possible
#
# Conditional build:
%bcond_with	doc	# Sphinx documentation (doesn't work on sdist)
%bcond_with	tests	# unit+functional tests (many require network or other stuff)

Summary:	Fast lightweight, pluggable proxy server in Python
Summary(pl.UTF-8):	Szybki, lekki serwer proxy w Pythonie z obsługą wtyczek
Name:		python3-proxy.py
Version:	2.4.10
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/proxy-py/
Source0:	https://files.pythonhosted.org/packages/source/p/proxy-py/proxy_py-%{version}.tar.gz
# Source0-md5:	25e702e05484acfe57b2f4a3e9d85989
URL:		https://pypi.org/project/proxy.py/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm >= 7.0.3
%if %{with tests}
BuildRequires:	python3-h2 >= 4.1.0
BuildRequires:	python3-hpack >= 4.0.0
BuildRequires:	python3-hyperframe >= 6.0.1
# for test_http2.py (enable when httpx is available)
#BuildRequires:	python3-httpx >= 0.27.0
BuildRequires:	python3-pytest >= 8.1.1
BuildRequires:	python3-pytest-asyncio >= 0.21.1
BuildRequires:	python3-pytest-cov >= 5.0.0
BuildRequires:	python3-pytest-mock >= 3.14.0
BuildRequires:	python3-pytest-xdist >= 3.5.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-furo >= 2021.11.15
BuildRequires:	python3-linkify-it-py >= 2.0
BuildRequires:	python3-myst_parser >= 0.17.2
BuildRequires:	python3-sphinxcontrib-apidoc >= 0.3.0
BuildRequires:	python3-sphinxcontrib-towncrier >= 0.2.0
BuildRequires:	sphinx-pdg-3 >= 4.3.2
%endif
Requires:	python3-modules >= 1:3.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lightweight proxy server in Python. Features:
- drop-in alternative to ngrok
- fast & scalable
- lightweight
- programmable
- can listen on multiple addresses and ports
- real-time dashboard
- secure
- private
- Man-In-The-Middle TLS decryption
- supported protocols for proxy requests: http(s), http2, websockets
- support for HAProxy Protocol
- static file server support
- optimized for large file uploads and downloads
- IPv4 and IPv6 support
- unix domain socket support
- Basic authentication support
- PAC (Proxy Auto-configuration) support

%description -l pl.UTF-8
Lekki serwer proxy w Pythonie. Cechy:
- zamiennik dla ngrok
- szybki i skalowalny
- lekki
- programowalny
- może nasłuchiwać na wielu adresach i portach
- pulpit odświeżany w czasie rzeczywistym
- bezpieczny
- prywatny
- odszyfrowywanie TLS jako Man-In-The-Middle
- obsługiwan protokoły żądań proxy: http(s), http2, websockets
- obsługa protokołu HAProxy
- obsługa sersera plików statycznych
- zoptymalizowany pod kątem przesyłania i pobierania dużych plików
- obsługa IPv4 i IPv6
- obsługa gniazd uniksowych
- obsługa uwierzytelniania Basic
- obsługa PAC (Proxy Auto-configuration)

%prep
%setup -q -n proxy_py-%{version}

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_asyncio.plugin,pytest_mock.plugin \
%{__python3} -m pytest tests --ignore tests/http/proxy/test_http2.py
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

# "proxy" binary name would be too common, use traditional "proxy.py" name
%{__mv} $RPM_BUILD_ROOT%{_bindir}/proxy{,.py-3}
ln -sf proxy.py-3 $RPM_BUILD_ROOT%{_bindir}/proxy.py

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md SECURITY.md
%attr(755,root,root) %{_bindir}/grout
%attr(755,root,root) %{_bindir}/proxy.py-3
%{_bindir}/proxy.py
%{py3_sitescriptdir}/proxy
%{py3_sitescriptdir}/proxy_py-%{version}.dist-info
