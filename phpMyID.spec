Summary:	Single user Identity Provider for OpenID authentication
Summary(pl.UTF-8):	Prosty dostawca identyfikatorów użytkowników do uwierzytelniania OpenID
Name:		phpMyID
Version:	0.6
Release:	0.3
License:	GPL
Group:		Applications/WWW
Source0:	http://siege.org/projects/phpMyID/%{name}-%{version}.tgz
# Source0-md5:	f1f000c370ca4a402e26f10a04d50329
Source1:	%{name}-apache.conf
Source2:	%{name}.php
Patch0:		%{name}.patch
URL:		http://siege.org/projects/phpMyID/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	php(pcre)
Requires:	php(session)
Requires:	webapps
Requires:	webserver(php) >= 4.2.0
Suggests:	php(bcmath)
Suggests:	php(gmp)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
phpMyID is a small, fairly lightweight, standalone, single user
Identity Provider for OpenID authentication. It comprises a single PHP
script that can be used by one individual to run their own personal
OpenID "IdP."

%description -l pl.UTF-8
phpMyID to mały, dość lekki i samodzielny dostawca identyfikatorów
użytkowników (Idendity Provider) do uwierzytelniania OpenID. Składa
się z pojedynczego skryptu PHP, który może być używany w celu
uruchomienia własnego "IdP" OpenID.

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}
cp -a MyID.php $RPM_BUILD_ROOT%{_appdir}
cp -a MyID.config.php $RPM_BUILD_ROOT%{_sysconfdir}/config.php
cp -a %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/index.php
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -a %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG README FAQ
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%{_appdir}
