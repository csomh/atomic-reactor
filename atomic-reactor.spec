%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?python2_version: %global python2_version %(%{__python2} -c "import sys; sys.stdout.write(sys.version[:3])")}
%endif

%if 0%{?rhel} && 0%{?rhel} <= 7
%{!?py2_build: %global py2_build %{__python2} setup.py build}
%{!?py2_install: %global py2_install %{__python2} setup.py install --skip-build --root %{buildroot}}
%endif

%if (0%{?fedora} >= 22 || 0%{?rhel} >= 8)
%global with_python3 1
%global binaries_py_version %{python3_version}
%else
%global binaries_py_version %{python2_version}
%endif

%if 0%{?fedora}
# rhel/epel has no flexmock, pytest-capturelog
%global with_check 1
%endif

%global owner projectatomic
%global project atomic-reactor

%global commit 6ba19de82d99d74a777221abdbaa7037fd50c1e7
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global dock_obsolete_vr 1.3.7-2

Name:           %{project}
Version:        1.6.27
Release:        1%{?dist}

Summary:        Improved builder for Docker images
Group:          Development/Tools
License:        BSD
URL:            https://github.com/%{owner}/%{project}
Source0:        https://github.com/%{owner}/%{project}/archive/%{commit}/%{project}-%{commit}.tar.gz

BuildArch:      noarch

%if 0%{?with_check}
BuildRequires:  git
%endif # with_check

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if 0%{?with_check}
BuildRequires:  pytest
BuildRequires:  python-pytest-capturelog
BuildRequires:  python-dockerfile-parse >= 0.0.5
BuildRequires:  python-docker-py
BuildRequires:  python-flexmock >= 0.10.2
BuildRequires:  python-six
BuildRequires:  python-osbs-client
BuildRequires:  python-backports-lzma
BuildRequires:  python2-responses
# BuildRequires:  python3-jsonschema
%endif # with_check

%if 0%{?with_python3}
Requires:       python3-atomic-reactor = %{version}-%{release}
%else
Requires:       python-atomic-reactor = %{version}-%{release}
%endif # with_python3
Requires:       git >= 1.7.10

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?with_check}
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-capturelog
BuildRequires:  python3-dockerfile-parse >= 0.0.5
BuildRequires:  python3-docker
BuildRequires:  python3-flexmock >= 0.10.2
BuildRequires:  python3-six
BuildRequires:  python3-osbs-client
BuildRequires:  python3-responses
BuildRequires:  python3-jsonschema
BuildRequires:  python3-PyYAML
BuildRequires:  python-docker-squash >= 1.0.0-0.3
%endif # with_check
%endif # with_python3

Provides:       dock = %{version}-%{release}
Obsoletes:      dock < %{dock_obsolete_vr}

%description
Simple Python tool with command line interface for building Docker
images. It contains a lot of helpful functions which you would
probably implement if you started hooking Docker into your
infrastructure.


%package -n python-atomic-reactor
Summary:        Python 2 Atomic Reactor library
Group:          Development/Tools
License:        BSD
Requires:       python-docker-py
Requires:       python-requests
Requires:       python-setuptools
Requires:       python-dockerfile-parse >= 0.0.5
Requires:       python-docker-squash >= 1.0.0-0.3
Requires:       python-backports-lzma
Requires:       python-jsonschema
Requires:       PyYAML
Provides:       python-dock = %{version}-%{release}
Obsoletes:      python-dock < %{dock_obsolete_vr}
%{?python_provide:%python_provide python-atomic-reactor}

%description -n python-atomic-reactor
Simple Python 2 library for building Docker images. It contains
a lot of helpful functions which you would probably implement if
you started hooking Docker into your infrastructure.

%package -n python-atomic-reactor-koji
Summary:        Koji plugin for Atomic Reactor
Group:          Development/Tools
Requires:       python-atomic-reactor = %{version}-%{release}
Requires:       koji
Provides:       dock-koji = %{version}-%{release}
Provides:       python-dock-koji = %{version}-%{release}
Obsoletes:      dock-koji < 1.2.0-3
Obsoletes:      python-dock-koji < %{dock_obsolete_vr}
%{?python_provide:%python_provide python-atomic-reactor-koji}

%description -n python-atomic-reactor-koji
Koji plugin for Atomic Reactor


%package -n python-atomic-reactor-metadata
Summary:        Plugin for submitting metadata to OSBS
Group:          Development/Tools
Requires:       python-atomic-reactor = %{version}-%{release}
Requires:       osbs
Provides:       dock-metadata = %{version}-%{release}
Provides:       python-dock-metadata = %{version}-%{release}
Obsoletes:      dock-metadata < 1.2.0-3
Obsoletes:      python-dock-metadata < %{dock_obsolete_vr}
%{?python_provide:%python_provide python-atomic-reactor-metadata}

%description -n python-atomic-reactor-metadata
Plugin for submitting metadata to OSBS


%package -n python-atomic-reactor-rebuilds
Summary:        Plugins for automated rebuilds
Group:          Development/Tools
Requires:       python-atomic-reactor = %{version}-%{release}
Requires:       osbs >= 0.15
%{?python_provide:%python_provide python-atomic-reactor-rebuilds}

%description -n python-atomic-reactor-rebuilds
Plugins for automated rebuilds


%if 0%{?with_python3}
%package -n python3-atomic-reactor
Summary:        Python 3 Atomic Reactor library
Group:          Development/Tools
License:        BSD
Requires:       python3-docker-py
Requires:       python3-requests
Requires:       python3-setuptools
Requires:       python3-dockerfile-parse >= 0.0.5
Requires:       python3-docker-squash >= 1.0.0-0.3
Requires:       python3-jsonschema
Requires:       python3-PyYAML
Provides:       python3-dock = %{version}-%{release}
Obsoletes:      python3-dock < %{dock_obsolete_vr}
%{?python_provide:%python_provide python3-atomic-reactor}

%description -n python3-atomic-reactor
Simple Python 3 library for building Docker images. It contains
a lot of helpful functions which you would probably implement if
you started hooking Docker into your infrastructure.


%package -n python3-atomic-reactor-koji
Summary:        Koji plugin for Atomic Reactor
Group:          Development/Tools
Requires:       python3-atomic-reactor = %{version}-%{release}
Requires:       koji
Provides:       python3-dock-koji = %{version}-%{release}
Obsoletes:      python3-dock-koji < %{dock_obsolete_vr}
%{?python_provide:%python_provide python3-atomic-reactor-koji}

%description -n python3-atomic-reactor-koji
Koji plugin for Atomic Reactor


%package -n python3-atomic-reactor-metadata
Summary:        Plugin for submitting metadata to OSBS
Group:          Development/Tools
Requires:       python3-atomic-reactor = %{version}-%{release}
Requires:       osbs
Provides:       python3-dock-metadata = %{version}-%{release}
Obsoletes:      python3-dock-metadata < %{dock_obsolete_vr}
%{?python_provide:%python_provide python3-atomic-reactor-metadata}

%description -n python3-atomic-reactor-metadata
Plugin for submitting metadata to OSBS

%package -n python3-atomic-reactor-rebuilds
Summary:        Plugins for automated rebuilds
Group:          Development/Tools
Requires:       python3-atomic-reactor = %{version}-%{release}
Requires:       osbs >= 0.15
%{?python_provide:%python_provide python3-atomic-reactor-rebuilds}

%description -n python3-atomic-reactor-rebuilds
Plugins for automated rebuilds
%endif # with_python3


%prep
%setup -qn %{name}-%{commit}


%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif # with_python3


%install
%if 0%{?with_python3}
%py3_install
mv %{buildroot}%{_bindir}/atomic-reactor %{buildroot}%{_bindir}/atomic-reactor-%{python3_version}
ln -s %{_bindir}/atomic-reactor-%{python3_version} %{buildroot}%{_bindir}/atomic-reactor-3
%endif # with_python3

%py2_install
mv %{buildroot}%{_bindir}/atomic-reactor %{buildroot}%{_bindir}/atomic-reactor-%{python2_version}
ln -s %{_bindir}/atomic-reactor-%{python2_version} %{buildroot}%{_bindir}/atomic-reactor-2
ln -s %{_bindir}/atomic-reactor-%{binaries_py_version} %{buildroot}%{_bindir}/atomic-reactor

# ship reactor in form of tarball so it can be installed within build image
cp -a %{sources} %{buildroot}/%{_datadir}/%{name}/atomic-reactor.tar.gz

mkdir -p %{buildroot}%{_mandir}/man1
cp -a docs/manpage/atomic-reactor.1 %{buildroot}%{_mandir}/man1/


%if 0%{?with_check}
%check
%if 0%{?with_python3}
LANG=en_US.utf8 py.test-%{python3_version} -vv tests
%endif # with_python3

LANG=en_US.utf8 py.test-%{python2_version} -vv tests
%endif # with_check


%files
%doc README.md
%{_mandir}/man1/atomic-reactor.1*
%{!?_licensedir:%global license %doc}
%license LICENSE
%{_bindir}/atomic-reactor

%files -n python-atomic-reactor
%doc README.md
%doc docs/*.md
%{!?_licensedir:%global license %doc}
%license LICENSE
%{_bindir}/atomic-reactor-%{python2_version}
%{_bindir}/atomic-reactor-2
%dir %{python2_sitelib}/atomic_reactor
%{python2_sitelib}/atomic_reactor/*.*
%{python2_sitelib}/atomic_reactor/cli
%{python2_sitelib}/atomic_reactor/plugins
%{python2_sitelib}/atomic_reactor/schemas
%exclude %{python2_sitelib}/atomic_reactor/koji_util.py*
%exclude %{python2_sitelib}/atomic_reactor/plugins/exit_koji_promote.py*
%exclude %{python2_sitelib}/atomic_reactor/plugins/exit_koji_import.py*
%exclude %{python2_sitelib}/atomic_reactor/plugins/exit_sendmail.py*
%exclude %{python2_sitelib}/atomic_reactor/plugins/exit_store_metadata_in_osv3.py*
%exclude %{python2_sitelib}/atomic_reactor/plugins/post_import_image.py*
%exclude %{python2_sitelib}/atomic_reactor/plugins/post_koji_upload.py*
%exclude %{python2_sitelib}/atomic_reactor/plugins/pre_add_filesystem.py*
%exclude %{python2_sitelib}/atomic_reactor/plugins/pre_bump_release.py*
%exclude %{python2_sitelib}/atomic_reactor/plugins/pre_koji.py*
%exclude %{python2_sitelib}/atomic_reactor/plugins/pre_koji_parent.py*
%exclude %{python2_sitelib}/atomic_reactor/plugins/pre_inject_parent_image.py*
%exclude %{python2_sitelib}/atomic_reactor/plugins/pre_fetch_maven_artifacts.py*
%exclude %{python2_sitelib}/atomic_reactor/plugins/pre_stop_autorebuild_if_disabled.py*
%exclude %{python2_sitelib}/integration-tests

%{python2_sitelib}/atomic_reactor-%{version}-py2.*.egg-info
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/atomic-reactor.tar.gz
%{_datadir}/%{name}/images


%files -n python-atomic-reactor-koji
%{python2_sitelib}/atomic_reactor/koji_util.py*
%{python2_sitelib}/atomic_reactor/plugins/pre_add_filesystem.py*
%{python2_sitelib}/atomic_reactor/plugins/pre_bump_release.py*
%{python2_sitelib}/atomic_reactor/plugins/pre_koji.py*
%{python2_sitelib}/atomic_reactor/plugins/pre_koji_parent.py*
%{python2_sitelib}/atomic_reactor/plugins/pre_inject_parent_image.py*
%{python2_sitelib}/atomic_reactor/plugins/pre_fetch_maven_artifacts.py*
%{python2_sitelib}/atomic_reactor/plugins/post_koji_upload.py*
%{python2_sitelib}/atomic_reactor/plugins/exit_koji_promote.py*
%{python2_sitelib}/atomic_reactor/plugins/exit_koji_import.py*


%files -n python-atomic-reactor-metadata
%{python2_sitelib}/atomic_reactor/plugins/exit_store_metadata_in_osv3.py*

%files -n python-atomic-reactor-rebuilds
%{python2_sitelib}/atomic_reactor/plugins/exit_sendmail.py*
%{python2_sitelib}/atomic_reactor/plugins/post_import_image.py*
%{python2_sitelib}/atomic_reactor/plugins/pre_stop_autorebuild_if_disabled.py*


%if 0%{?with_python3}
%files -n python3-atomic-reactor
%doc README.md
%doc docs/*.md
%{!?_licensedir:%global license %doc}
%license LICENSE
%{_bindir}/atomic-reactor-%{python3_version}
%{_bindir}/atomic-reactor-3
%{_mandir}/man1/atomic-reactor.1*
%dir %{python3_sitelib}/atomic_reactor
%dir %{python3_sitelib}/atomic_reactor/__pycache__
%{python3_sitelib}/atomic_reactor/*.*
%{python3_sitelib}/atomic_reactor/cli
%{python3_sitelib}/atomic_reactor/plugins
%{python3_sitelib}/atomic_reactor/schemas
%{python3_sitelib}/atomic_reactor/__pycache__/*.py*
%exclude %{python3_sitelib}/atomic_reactor/koji_util.py
%exclude %{python3_sitelib}/atomic_reactor/plugins/exit_koji_promote.py
%exclude %{python3_sitelib}/atomic_reactor/plugins/exit_koji_import.py
%exclude %{python3_sitelib}/atomic_reactor/plugins/exit_sendmail.py
%exclude %{python3_sitelib}/atomic_reactor/plugins/exit_store_metadata_in_osv3.py
%exclude %{python3_sitelib}/atomic_reactor/plugins/post_import_image.py
%exclude %{python3_sitelib}/atomic_reactor/plugins/post_koji_upload.py
%exclude %{python3_sitelib}/atomic_reactor/plugins/pre_add_filesystem.py
%exclude %{python3_sitelib}/atomic_reactor/plugins/pre_bump_release.py
%exclude %{python3_sitelib}/atomic_reactor/plugins/pre_check_and_set_rebuild.py
%exclude %{python3_sitelib}/atomic_reactor/plugins/pre_koji.py
%exclude %{python3_sitelib}/atomic_reactor/plugins/pre_koji_parent.py
%exclude %{python3_sitelib}/atomic_reactor/plugins/pre_inject_parent_image.py
%exclude %{python3_sitelib}/atomic_reactor/plugins/pre_stop_autorebuild_if_disabled.py
%exclude %{python3_sitelib}/atomic_reactor/plugins/pre_fetch_maven_artifacts.py*
%exclude %{python3_sitelib}/atomic_reactor/plugins/__pycache__/exit_koji_promote*.py*
%exclude %{python3_sitelib}/atomic_reactor/plugins/__pycache__/exit_koji_import*.py*
%exclude %{python3_sitelib}/atomic_reactor/plugins/__pycache__/exit_sendmail*.py*
%exclude %{python3_sitelib}/atomic_reactor/plugins/__pycache__/exit_store_metadata_in_osv3*.py*
%exclude %{python3_sitelib}/atomic_reactor/plugins/__pycache__/post_import_image*.py*
%exclude %{python3_sitelib}/atomic_reactor/plugins/__pycache__/post_koji_upload*.py*
%exclude %{python3_sitelib}/atomic_reactor/plugins/__pycache__/pre_bump_release*.py*
%exclude %{python3_sitelib}/atomic_reactor/plugins/__pycache__/pre_add_filesystem*.py*
%exclude %{python3_sitelib}/atomic_reactor/plugins/__pycache__/pre_check_and_set_rebuild*.py*
%exclude %{python3_sitelib}/atomic_reactor/plugins/__pycache__/pre_koji*.py*
%exclude %{python3_sitelib}/atomic_reactor/plugins/__pycache__/pre_koji_parent*.py*
%exclude %{python3_sitelib}/atomic_reactor/plugins/__pycache__/pre_inject_parent_image*.py*
%exclude %{python3_sitelib}/atomic_reactor/plugins/__pycache__/pre_stop_autorebuild_if_disabled*.py*
%exclude %{python3_sitelib}/atomic_reactor/plugins/__pycache__/pre_fetch_maven_artifacts*.py*
%exclude %{python3_sitelib}/integration-tests

%{python3_sitelib}/atomic_reactor-%{version}-py3.*.egg-info
%dir %{_datadir}/%{name}
# ship reactor in form of tarball so it can be installed within build image
%{_datadir}/%{name}/atomic-reactor.tar.gz
# dockerfiles for build images
# there is also a script which starts docker in privileged container
# (is not executable, because it's meant to be used within provileged containers, not on a host system)
%{_datadir}/%{name}/images


%files -n python3-atomic-reactor-koji
%{python3_sitelib}/atomic_reactor/koji_util.py
%{python3_sitelib}/atomic_reactor/__pycache__/koji_util*.py*
%{python3_sitelib}/atomic_reactor/plugins/pre_add_filesystem.py
%{python3_sitelib}/atomic_reactor/plugins/pre_bump_release.py
%{python3_sitelib}/atomic_reactor/plugins/pre_koji.py
%{python3_sitelib}/atomic_reactor/plugins/pre_koji_parent.py
%{python3_sitelib}/atomic_reactor/plugins/pre_inject_parent_image.py
%{python3_sitelib}/atomic_reactor/plugins/pre_fetch_maven_artifacts.py
%{python3_sitelib}/atomic_reactor/plugins/post_koji_upload.py
%{python3_sitelib}/atomic_reactor/plugins/exit_koji_promote.py
%{python3_sitelib}/atomic_reactor/plugins/exit_koji_import.py
%{python3_sitelib}/atomic_reactor/plugins/__pycache__/pre_add_filesystem*.py*
%{python3_sitelib}/atomic_reactor/plugins/__pycache__/pre_bump_release*.py*
%{python3_sitelib}/atomic_reactor/plugins/__pycache__/pre_koji*.py*
%{python3_sitelib}/atomic_reactor/plugins/__pycache__/pre_koji_parent*.py*
%{python3_sitelib}/atomic_reactor/plugins/__pycache__/pre_inject_parent_image*.py*
%{python3_sitelib}/atomic_reactor/plugins/__pycache__/pre_fetch_maven_artifacts.py
%{python3_sitelib}/atomic_reactor/plugins/__pycache__/post_koji_upload.py
%{python3_sitelib}/atomic_reactor/plugins/__pycache__/exit_koji_promote*.py*
%{python3_sitelib}/atomic_reactor/plugins/__pycache__/exit_koji_import*.py*


%files -n python3-atomic-reactor-metadata
%{python3_sitelib}/atomic_reactor/plugins/exit_store_metadata_in_osv3.py
%{python3_sitelib}/atomic_reactor/plugins/__pycache__/exit_store_metadata_in_osv3*.py*

%files -n python3-atomic-reactor-rebuilds
%{python3_sitelib}/atomic_reactor/plugins/exit_sendmail.py
%{python3_sitelib}/atomic_reactor/plugins/post_import_image.py
%{python3_sitelib}/atomic_reactor/plugins/pre_check_and_set_rebuild.py
%{python3_sitelib}/atomic_reactor/plugins/pre_stop_autorebuild_if_disabled.py
%{python3_sitelib}/atomic_reactor/plugins/__pycache__/exit_sendmail*.py*
%{python3_sitelib}/atomic_reactor/plugins/__pycache__/post_import_image*.py*
%{python3_sitelib}/atomic_reactor/plugins/__pycache__/pre_check_and_set_rebuild*.py*
%{python3_sitelib}/atomic_reactor/plugins/__pycache__/pre_stop_autorebuild_if_disabled*.py*
%endif  # with_python3


%changelog
* Wed Oct 04 2017 Robert Cerven <rcerven@redhat.com> - 1.6.27-1
- new upstream release: 1.6.27

* Mon Sep 11 2017 Robert Cerven <rcerven@redhat.com> - 1.6.26.3-1
- new upstream release: 1.6.26.3

* Wed Sep 06 2017 Robert Cerven <rcerven@redhat.com> - 1.6.26.2-1
- new upstream release: 1.6.26.2

* Wed Sep 06 2017 Robert Cerven <rcerven@redhat.com> - 1.6.26.1-1
- new upstream release: 1.6.26.1

* Tue Sep 05 2017 Robert Cerven <rcerven@redhat.com> - 1.6.26-1
- new upstream release: 1.6.26

* Mon Jul 31 2017 Robert Cerven <rcerven@redhat.com> - 1.6.25-1
- new upstream release: 1.6.25

* Wed Jun 28 2017 Robert Cerven <rcerven@redhat.com> - 1.6.24.1-1
- new upstream release: 1.6.24.1

* Tue Jun 27 2017 Robert Cerven <rcerven@redhat.com> - 1.6.24-1
- new upstream release: 1.6.24

* Tue Apr 04 2017 Robert Cerven <rcerven@redhat.com> - 1.6.23-1
- new upstream release: 1.6.23

* Mon Mar 06 2017 Robert Cerven <rcerven@redhat.com> - 1.6.22-1
- new upstream release: 1.6.22

* Mon Feb 13 2017 Vadim Rutkovsky <vrutkovs@redhat.com> - 1.16.21-1
- 1.6.21 release

* Mon Feb 6 2017 Vadim Rutkovsky <vrutkovs@redhat.com> - 1.16.20-1
- 1.6.20 release

* Wed Nov 29 2016 Vadim Rutkovsky <vrutkovs@redhat.com> - 1.16.19-1
- 1.6.19 release

* Wed Nov 11 2016 Vadim Rutkovsky <vrutkovs@redhat.com> - 1.16.18-1
- 1.6.18 release

* Wed Sep 21 2016 Vadim Rutkovsky <vrutkovs@redhat.com> - 1.16.17-1
- 1.6.17 release

* Tue Sep 13 2016 Luiz Carvalho <lucarval@redhat.com>  - 1.6.16-1
- 1.6.16 release

* Thu Aug 18 2016 Martin Milata <mmilata@redhat.com> - 1.6.15-1
- 1.6.15 release

* Mon Aug 01 2016 Tim Waugh <twaugh@redhat.com> - 1.6.14-1
- 1.6.14 release

* Fri Jul 08 2016 Tim Waugh <twaugh@redhat.com> - 1.6.13-1
- 1.6.13 release

* Mon Jul 4 2016 Vadim Rutkovsky <vrutkovs@redhat.com> - 1.6.12-1
- 1.6.12 release

* Fri Jun 24 2016 Vadim Rutkovsky <vrutkovs@redhat.com> - 1.6.11-1
- 1.6.11 release

* Thu Jun 09 2016 Tim Waugh <twaugh@redhat.com>
- Move the bump_release plugin to the koji subpackage since it uses Koji.

* Wed Jun 08 2016 Martin Milata <mmilata@redhat.com> - 1.6.10-1
- 1.6.10 release

* Thu May 26 2016 Martin Milata <mmilata@redhat.com> - 1.6.9-1
- 1.6.9 release

* Mon May 23 2016 Martin Milata <mmilata@redhat.com> - 1.6.8-1
- New pre_add_filesystem plugin. (Tim Waugh <twaugh@redhat.com>)
- New koji_util module in koji package. (Tim Waugh <twaugh@redhat.com>)
- 1.6.8 release

* Fri Apr 22 2016 Martin Milata <mmilata@redhat.com> - 1.6.7-1
- 1.6.7 release

* Tue Apr 12 2016 Martin Milata <mmilata@redhat.com> - 1.6.6-1
- 1.6.6 release

* Mon Apr 11 2016 Martin Milata <mmilata@redhat.com> - 1.6.5-1
- Move koji_promote plugin to koji package now that it is used in the
  main workflow. (Tim Waugh <twaugh@redhat.com>)
- 1.6.5 release

* Thu Apr 07 2016 Martin Milata <mmilata@redhat.com> - 1.6.4-1
- 1.6.4 release

* Thu Feb 04 2016 Martin Milata <mmilata@redhat.com> - 1.6.3-1
- 1.6.3 release

* Mon Feb 01 2016 Martin Milata <mmilata@redhat.com> - 1.6.2-1
- 1.6.2 release
- BuildRequires python-flexmock >= 0.10.2 due to
  https://github.com/bkabrda/flexmock/issues/6

* Fri Jan 15 2016 Martin Milata <mmilata@redhat.com> - 1.6.1-1
- 1.6.1 release

* Fri Nov 20 2015 Jiri Popelka <jpopelka@redhat.com> - 1.6.0-4
- use py_build & py_install macros
- use python_provide macro
- ship executables per packaging guidelines

* Thu Nov 05 2015 Jiri Popelka <jpopelka@redhat.com> - 1.6.0-3
- %%check section

* Mon Oct 19 2015 Slavek Kabrda <bkabrda@redhat.com> - 1.6.0-2
- add requirements on python{,3}-docker-scripts

* Mon Oct 19 2015 Tomas Tomecek <ttomecek@redhat.com> - 1.6.0-1
- 1.6.0 release

* Tue Sep 08 2015 Tomas Tomecek <ttomecek@redhat.com> - 1.5.1-1
- 1.5.1 release

* Fri Sep 04 2015 Tomas Tomecek <ttomecek@redhat.com> - 1.5.0-2
- workaround lack of python-pygit2

* Fri Sep 04 2015 Tomas Tomecek <ttomecek@redhat.com> - 1.5.0-1
- 1.5.0 release

* Tue Jul 28 2015 bkabrda <bkabrda@redhat.com> - 1.4.0-2
- fix issues found during Fedora re-review (rhbz#1246702)

* Thu Jul 16 2015 Tomas Tomecek <ttomecek@redhat.com> - 1.4.0-1
- new upstream release 1.4.0

* Tue Jun 30 2015 Jiri Popelka <jpopelka@redhat.com> - 1.3.7-3
- define macros for RHEL-6

* Mon Jun 22 2015 Slavek Kabrda <bkabrda@redhat.com> - 1.3.7-2
- rename to atomic-reactor

* Mon Jun 22 2015 Martin Milata <mmilata@redhat.com> - 1.3.7-1
- new upstream release 1.3.7

* Wed Jun 17 2015 Jiri Popelka <jpopelka@redhat.com> - 1.3.6-2
- update hash

* Wed Jun 17 2015 Tomas Tomecek <ttomecek@redhat.com> - 1.3.6-1
- new upstream release 1.3.6

* Tue Jun 16 2015 Tomas Tomecek <ttomecek@redhat.com> - 1.3.5-1
- new upstream release 1.3.5

* Fri Jun 12 2015 Tomas Tomecek <ttomecek@redhat.com> - 1.3.4-1
- new upstream release 1.3.4

* Wed Jun 10 2015 Jiri Popelka <jpopelka@redhat.com> - 1.3.3-2
- BuildRequires:  python-docker-py

* Wed Jun 10 2015 Jiri Popelka <jpopelka@redhat.com> - 1.3.3-1
- new upstream release 1.3.3

* Mon Jun 01 2015 Tomas Tomecek <ttomecek@redhat.com> - 1.3.2-1
- new upstream release 1.3.2

* Wed May 27 2015 Tomas Tomecek <ttomecek@redhat.com> - 1.3.1-1
- new upstream release 1.3.1

* Mon May 25 2015 Tomas Tomecek <ttomecek@redhat.com> - 1.3.0-1
- new upstream release 1.3.0

* Tue May 19 2015 Jiri Popelka <jpopelka@redhat.com> - 1.2.1-3
- fix el7 build

* Tue May 19 2015 Jiri Popelka <jpopelka@redhat.com> - 1.2.1-2
- rebuilt

* Tue May 19 2015 Martin Milata <mmilata@redhat.com> - 1.2.1-1
- new upstream release 1.2.1

* Thu May 14 2015 Jiri Popelka <jpopelka@redhat.com> - 1.2.0-4
- enable Python 3 build

* Thu May 07 2015 Slavek Kabrda <bkabrda@redhat.com> - 1.2.0-3
- Introduce python-dock subpackage
- Rename dock-{koji,metadata} to python-dock-{koji,metadata}
- move /usr/bin/dock to /usr/bin/dock2, /usr/bin/dock is now a symlink

* Tue May 05 2015 Jiri Popelka <jpopelka@redhat.com> - 1.2.0-2
- require python[3]-setuptools

* Tue Apr 21 2015 Tomas Tomecek <ttomecek@redhat.com> - 1.2.0-1
- new upstream release 1.2.0

* Tue Apr 07 2015 Tomas Tomecek <ttomecek@redhat.com> - 1.1.3-1
- new upstream release 1.1.3

* Thu Apr 02 2015 Martin Milata <mmilata@redhat.com> - 1.1.2-1
- new upstream release 1.1.2

* Thu Mar 19 2015 Jiri Popelka <jpopelka@redhat.com> - 1.1.1-2
- separate executable for python 3

* Tue Mar 17 2015 Tomas Tomecek <ttomecek@redhat.com> - 1.1.1-1
- new upstream release 1.1.1

* Fri Feb 20 2015 Tomas Tomecek <ttomecek@redhat.com> - 1.1.0-1
- new upstream release 1.1.0

* Wed Feb 11 2015 Tomas Tomecek <ttomecek@redhat.com> - 1.0.0-2
- spec: fix python 3 packaging
- fix license in %%files
- comment on weird stuff (dock.tar.gz, docker.sh)

* Thu Feb 05 2015 Tomas Tomecek <ttomecek@redhat.com> - 1.0.0-1
- initial 1.0.0 upstream release

* Wed Feb 04 2015 Tomas Tomecek <ttomecek@redhat.com> 1.0.0.b-1
- new upstream release: beta

* Mon Dec 01 2014 Tomas Tomecek <ttomecek@redhat.com> 1.0.0.a-1
- complete rewrite (ttomecek@redhat.com)
- Use inspect_image() instead of get_image() when checking for existence (#4).
  (twaugh@redhat.com)

* Mon Nov 10 2014 Tomas Tomecek <ttomecek@redhat.com> 0.0.2-1
- more friendly error msg when build img doesnt exist (ttomecek@redhat.com)
- implement postbuild plugin system; do rpm -qa plugin (ttomecek@redhat.com)
- core, logs: wait for container to finish and then gather output
  (ttomecek@redhat.com)
- core, df copying: df was not copied when path wasn't provided
  (ttomecek@redhat.com)
- store dockerfile in results dir (ttomecek@redhat.com)

* Mon Nov 03 2014 Jakub Dorňák <jdornak@redhat.com> 0.0.1-1
- new package built with tito

* Sun Nov  2 2014 Jakub Dorňák <jdornak@redhat.com> - 0.0.1-1
- Initial package
