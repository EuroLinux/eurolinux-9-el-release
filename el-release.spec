%define debug_package %{nil}
%define product_family EuroLinux
%define release_name Sarajevo
%define base_release_version 9
%define full_release_version 9.0
%define dist_release_version 9

%define beta Beta
%define beta_part %{?beta:-%{beta}}
# We need to create one
#%define swid_regid euro-linux.com
%define dist .el%{dist_release_version}

Name:           el-release
Version:        %{full_release_version}
Release:        0.1%{?dist}
Summary:        %{product_family} release file
Group:          System Environment/Base
License:        GPLv2

Obsoletes:      centos-stream-release
Obsoletes:      centos-stream-release-eula
# Change this when there will be Oracle 9.0 or remove this comment for
# EuroLinux 9.1 - author: AB
Obsoletes:      oraclelinux-release
Obsoletes:      oraclelinux-release-eula
Obsoletes:      redhat-release
Obsoletes:      redhat-release-client
Obsoletes:      redhat-release-client
Obsoletes:      redhat-release-computenode
Obsoletes:      redhat-release-computenode
# There is no need to make second package for EULA
Obsoletes:      redhat-release-eula
Obsoletes:      redhat-release-everything
Obsoletes:      redhat-release-server
Obsoletes:      redhat-release-server
Obsoletes:      redhat-release-workstation
Obsoletes:      redhat-release-workstation
Provides:       base-module(platform:el%{base_release_version})
Provides:       centos-stream-release = %{version}
Provides:       centos-stream-release-eula
Provides:       el-release-eula
Provides:       oraclelinux-release = %{version}
Provides:       oraclelinux-release-eula
Provides:       redhat-release = %{base_release_version}
Provides:       redhat-release = %{version}
Provides:       redhat-release = %{version}-%{release}
Provides:       redhat-release-client
Provides:       redhat-release-client
Provides:       redhat-release-computenode
Provides:       redhat-release-computenode
Provides:       redhat-release-eula
Provides:       redhat-release-everything = %{version}
Provides:       redhat-release-server
Provides:       redhat-release-server
Provides:       redhat-release-workstation
Provides:       redhat-release-workstation
# 9
Provides:       system-release = %{base_release_version}
# 9.0,9.1,... etc
Provides:       system-release = %{version}
Provides:       system-release = %{version}-%{release}
Provides:       system-release(releasever) = %{base_release_version}

# Comment this because it does not make any sense
# Recommends:     redhat-release-eula
# Keep it in git repo, so there is no need to make this sources versioned in
# that way
Source1:        85-display-manager.preset
Source2:        90-default.preset
Source3:        99-default-disable.preset
# We don't need them
#Source4:        redhat-release-productids-9.0-beta-20210817074921.tar.gz
# SWIDTAG is on the whishlist -> After release Q1 or Q2 2022
#Source5:        RHEL-%{full_release_version}%{?beta_part}-swidtag.tar.gz
Source6:        50-redhat.conf
Source7:        90-default-user.preset

Source50:       RPM-GPG-KEY-eurolinux9
Source70:       eurolinux.repo

Source200:      EULA
Source201:      GPL

# Change this after obtaining SB certificates from the rh-boot team Secure Boot
# Signing Certificates
#Source400:      sb-certs-9-2021.9.tar.bz2


%description
%{product_family} release files

# TODO SB
#%package -n eurolinux-sb-certs
#Summary: %{distro} public secureboot certificates
#Group: System Environment/Base
#Provides: system-sb-certs = %{version}-%{release}
#Provides: redhat-sb-certs = %{version}-%{release}
#BuildArch: noarch


#%description -n eurolinux-sb-certs
#Secure Boot certificates


%prep


%build
echo OK


%install
rm -rf %{buildroot}

# create /etc
mkdir -p %{buildroot}/etc
mkdir -p %{buildroot}/%{_prefix}/lib

# create /etc/system-release and /etc/el-release 
echo "%{product_family} release %{full_release_version}%{?beta: %{beta}} (%{release_name})" > %{buildroot}/etc/el-release
ln -s el-release %{buildroot}/etc/system-release
ln -s el-release %{buildroot}/etc/redhat-release

# create /usr/lib/os-release
cat << EOF >>%{buildroot}/%{_prefix}/lib/os-release
NAME="%{product_family}"
VERSION="%{full_release_version} (%{release_name})"
ID="eurolinux"
ID_LIKE="rhel fedora centos"
VERSION_ID="%{full_release_version}"
PLATFORM_ID="platform:el%{base_release_version}"
PRETTY_NAME="%{product_family} %{full_release_version}%{?beta: %{beta}} (%{release_name})"
ANSI_COLOR="0;34"
CPE_NAME="cpe:/o:eurolinux:eurolinux:%{base_release_version}"
HOME_URL="https://www.euro-linux.com/"
BUG_REPORT_URL="https://github.com/EuroLinux/eurolinux-distro-bugs-and-rfc/"
DOCUMENTATION_URL="https://docs.euro-linux.com"
# We keep it for build scripts only
REDHAT_SUPPORT_PRODUCT="EuroLinux"
REDHAT_SUPPORT_PRODUCT_VERSION="%{base_release_version}"
EOF

# create /etc/os-release symlink
ln -s ../%{_prefix}/lib/os-release %{buildroot}/%{_sysconfdir}/os-release

# create /etc/system/release-cpe
echo "cpe:/o:eurolinux:eurolinux:%{base_release_version}" > %{buildroot}/etc/system-release-cpe

# create /etc/issue and /etc/issue.net
echo '\S' > %{buildroot}/etc/issue
echo 'Kernel \r on an \m' >> %{buildroot}/etc/issue
cp %{buildroot}/etc/issue %{buildroot}/etc/issue.net
echo >> %{buildroot}/etc/issue
mkdir -p %{buildroot}%{_sysconfdir}/issue.d

mkdir -p -m 755 %{buildroot}/etc/pki/rpm-gpg
install -m 644 %{SOURCE50} %{buildroot}/etc/pki/rpm-gpg

## set up the dist tag macros
mkdir -p %{buildroot}%{_rpmmacrodir}
cat > %{buildroot}%{_rpmmacrodir}/macros.dist << EOF
# dist macros.

%%eurolinux_ver %{base_release_version}
%%eurolinux %{base_release_version}
%%centos_ver %{base_release_version}
%%centos %{base_release_version}
%%rhel %{base_release_version}
%%dist .el%{base_release_version}
%%el%{base_release_version} 1
%%dist %%{!?distprefix0:%%{?distprefix}}%%{expand:%%{lua:for i=0,9999 do print("%%{?distprefix" .. i .."}") end}}%{dist}%%{?with_bootstrap:%{__bootstrap}}
%%__bootstrap         ~bootstrap
EOF

### dist tag macros end

# make el-release a protected package
# original A move from RH that make migration a little bit harder
install -p -d -m 755 %{buildroot}/etc/dnf/protected.d/
touch el-release.conf
echo el-release > redhat-release.conf
install -p -c -m 0644 el-release.conf %{buildroot}/etc/dnf/protected.d/
rm -f el-release.conf

# Create doc dir
mkdir -p -m 755 %{buildroot}/%{_docdir}/el-release
ln -s el-release %{buildroot}/%{_docdir}/redhat-release
# make /usr/share/el-release symlink redhat-release
mkdir -p -m 755 %{buildroot}/%{_datadir}/el-release
ln -s el-release %{buildroot}/%{_datadir}/redhat-release
install -m 644 %{SOURCE200} %{buildroot}/%{_datadir}/el-release
install -m 644 %{SOURCE201} %{buildroot}/%{_docdir}/el-release

# copy systemd presets
mkdir -p %{buildroot}/%{_prefix}/lib/systemd/system-preset/
mkdir -p %{buildroot}/%{_prefix}/lib/systemd/user-preset
install -m 0644 %{SOURCE1} %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE2} %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE3} %{buildroot}/%{_prefix}/lib/systemd/system-preset/

install -m 0644 %{SOURCE7} %{buildroot}%{_prefix}/lib/systemd/user-preset/
install -m 0644 %{SOURCE3} %{buildroot}%{_prefix}/lib/systemd/user-preset/

# copy sysctl presets
mkdir -p %{buildroot}/%{_prefix}/lib/sysctl.d/
install -m 0644 %{SOURCE6} %{buildroot}/%{_prefix}/lib/sysctl.d/

mkdir -p -m 755 %{buildroot}/etc/yum.repos.d
mkdir -p -m 755 %{buildroot}/etc/dnf/vars
echo %{base_release_version} > %{buildroot}/etc/dnf/vars/releasever

# Copy eurolinux.repo
install -m 644 %{SOURCE70} %{buildroot}/etc/yum.repos.d

# Copy SWID tags 
# FIXME after SWID tags
#mkdir -p -m 755 %{buildroot}%{_prefix}/lib/swidtag/%{swid_regid}
#if ! [ %{_arch} = "i386" ] ; then
#    install -p -m 644 RHEL-%{full_release_version}%{?beta_part}-swidtag/com.redhat.RHEL-%{base_release_version}-%{_arch}.swidtag %{buildroot}%{_prefix}/lib/swidtag/%{swid_regid}/
#    install -p -m 644 RHEL-%{full_release_version}%{?beta_part}-swidtag/com.redhat.RHEL-%{full_release_version}%{?beta_part}-%{_arch}.swidtag %{buildroot}%{_prefix}/lib/swidtag/%{swid_regid}/
#fi
#mkdir -p -m 755 %{buildroot}/etc/pki/swid/CA/%{swid_regid}
#mkdir -p -m 755 %{buildroot}/etc/swid/swidtags.d
#ln -sr %{buildroot}%{_prefix}/lib/swidtag/%{swid_regid} %{buildroot}/etc/swid/swidtags.d/%{swid_regid}
#install -p -m 644 RHEL-%{full_release_version}%{?beta_part}-swidtag/redhatcodesignca.cert %{buildroot}/etc/pki/swid/CA/%{swid_regid}/


# Copy secureboot certificates
# FIXME after SB
#install -d -m 0755 %{buildroot}%{_sysconfdir}/pki/sb-certs/
#install -d -m 0755 %{buildroot}%{_datadir}/pki/sb-certs/

# Install aarch64 certs
#install -m 644 sb-certs/redhatsecurebootca5.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-aarch64.cer
#ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-aarch64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-ca-aarch64.cer

#install -m 644 sb-certs/redhatsecureboot501.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-aarch64.cer
#ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-aarch64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-kernel-aarch64.cer

#install -m 644 sb-certs/redhatsecureboot502.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-aarch64.cer
#ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-aarch64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-grub2-aarch64.cer

#install -m 644 sb-certs/redhatsecureboot503.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-fwupd-aarch64.cer
#ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-fwupd-aarch64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-fwupd-aarch64.cer

# Install ppc64le certs
#install -m 644 sb-certs/redhatsecurebootca6.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-ppc64le.cer
#ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-ppc64le.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-ca-ppc64le.cer

#install -m 644 sb-certs/redhatsecureboot601.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-ppc64le.cer
#ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-ppc64le.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-kernel-ppc64le.cer

#install -m 644 sb-certs/redhatsecureboot602.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-ppc64le.cer
#ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-ppc64le.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-grub2-ppc64le.cer

# Install s390x certs
#install -m 644 sb-certs/redhatsecurebootca3.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-s390x.cer
#ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-s390x.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-ca-s390x.cer

#install -m 644 sb-certs/redhatsecureboot302.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-s390x.cer
#ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-s390x.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-kernel-s390x.cer

# Install x86_64 certs
#install -m 644 sb-certs/redhatsecurebootca5.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-x86_64.cer
#ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-x86_64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-ca-x86_64.cer

#install -m 644 sb-certs/redhatsecureboot501.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-x86_64.cer
#ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-x86_64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-kernel-x86_64.cer

#install -m 644 sb-certs/redhatsecureboot502.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-x86_64.cer
#ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-x86_64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-grub2-x86_64.cer

#install -m 644 sb-certs/redhatsecureboot503.cer %{buildroot}%{_datadir}/pki/sb-certs/secureboot-fwupd-x86_64.cer
#ln -sr %{buildroot}%{_datadir}/pki/sb-certs/secureboot-fwupd-x86_64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-fwupd-x86_64.cer


%clean
rm -rf %{buildroot}


%files
%defattr(0644,root,root,0755)
/etc/el-release
/etc/redhat-release
/etc/system-release
%config /etc/os-release
%config /etc/system-release-cpe
%config(noreplace) /etc/issue
%config(noreplace) /etc/issue.net
%dir %{_sysconfdir}/issue.d
/etc/dnf/protected.d/el-release.conf
/etc/pki/rpm-gpg/
%{_rpmmacrodir}/macros.dist
%{_docdir}/el-release/*
%{_docdir}/redhat-release
%{_prefix}/lib/systemd/system-preset/*
%{_prefix}/lib/systemd/user-preset/*
%{_prefix}/lib/sysctl.d/50-redhat.conf
%{_prefix}/lib/os-release

/etc/yum.repos.d/
%config(noreplace) /etc/dnf/vars/*
# FIXME
#/etc/swid/swidtags.d
#%{_prefix}/lib/swidtag/%{swid_regid}
#/etc/pki/swid/CA/%{swid_regid}
# EULA etc
%{_datadir}/el-release/*
%{_datadir}/redhat-release




#%files -n redhat-sb-certs
## Note to future packagers:
# The symlinks are not %config(noreplace) intentionally. We want them to be
# restored if this package is updated.
#%dir %{_sysconfdir}/pki/sb-certs
#%dir %{_datadir}/pki/sb-certs
#%{_sysconfdir}/pki/sb-certs/*.cer
#%{_datadir}/pki/sb-certs/*.cer


%changelog
* Sat Jan 29 2022 Alex Baranowski <alex@euro-linux.com> - 9.0-0.1
- Initial Release for EuroLinux 9 beta
- Sarajevo as Codename (Can change - Pool still in progress)
- Based on redhat-release 9.0-2.11
