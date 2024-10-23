%define debug_package %{nil}
%define product_family EuroLinux
%define release_name San Marino
%define base_release_version 9
%define full_release_version 9.4
%define dist_release_version 9

# We need to create one
#%define swid_regid euro-linux.com
%define dist .el%{dist_release_version}

Name:           el-release
Version:        %{full_release_version}
Release:        3.0%{?dist}
Summary:        %{product_family} release file
Group:          System Environment/Base
License:        GPLv2
BuildArch:      noarch

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
Provides:       redhat-release-computenode
Provides:       redhat-release-eula
Provides:       redhat-release-everything = %{version}
Provides:       redhat-release-server
Provides:       redhat-release-workstation
# 9
Provides:       system-release = %{base_release_version}
# 9.0,9.1,... etc
Provides:       system-release = %{version}
Provides:       system-release = %{version}-%{release}
Provides:       system-release(releasever) = %{base_release_version}
# obsolete rhc and insights-client
Obsoletes:      rhc
Obsoletes:      insights-client

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

# Signing Certificate
Source400:      eurolinux.cer


%description
%{product_family} release files

%package -n eurolinux-sb-certs
Summary: %{distro} public secureboot certificates
Group: System Environment/Base
Provides: system-sb-certs = %{version}-%{release}
Provides: redhat-sb-certs = %{version}-%{release}
BuildArch: noarch


%description -n eurolinux-sb-certs
Secure Boot certificates


%prep

%build

%install
rm -rf %{buildroot}

# create /etc
mkdir -p %{buildroot}/etc
mkdir -p %{buildroot}/%{_prefix}/lib

# create /etc/system-release and /etc/el-release
echo "%{product_family} release %{full_release_version} (%{release_name})" > %{buildroot}/etc/el-release
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
PRETTY_NAME="%{product_family} %{full_release_version} (%{release_name})"
ANSI_COLOR="0;34"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:eurolinux:eurolinux:%{base_release_version}"
HOME_URL="https://www.euro-linux.com/"
DOCUMENTATION_URL="https://docs.euro-linux.com"
BUG_REPORT_URL="https://github.com/EuroLinux/eurolinux-distro-bugs-and-rfc/"
REDHAT_SUPPORT_PRODUCT="EuroLinux"
REDHAT_SUPPORT_PRODUCT_VERSION="%{base_release_version}"
EOF
# create /etc/os-release symlink
ln -s ../%{_prefix}/lib/os-release %{buildroot}/%{_sysconfdir}/os-release

# create /etc/system/release-cpe
echo "cpe:/o:eurolinux:eurolinux:%{base_release_version}" > %{buildroot}/etc/system-release-cpe

# create /etc/issue, /etc/issue.net and /etc/issue.d
echo '\S' > %{buildroot}/etc/issue
echo 'Kernel \r on an \m' >> %{buildroot}/etc/issue
cp %{buildroot}/etc/issue %{buildroot}/etc/issue.net
echo >> %{buildroot}/etc/issue
mkdir -p %{buildroot}%{_sysconfdir}/issue.d

# copy GPG keys
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
%%__bootstrap         ~bootstrap
%%dist %%{!?distprefix0:%%{?distprefix}}%%{expand:%%{lua:for i=0,9999 do print("%%{?distprefix" .. i .."}") end}}%{dist}%%{?with_bootstrap:%{__bootstrap}}
%%el%{base_release_version} 1
EOF

### dist tag macros end

# make el-release a protected package
# original A move from RH that make migration a little bit harder
install -p -d -m 755 %{buildroot}/etc/dnf/protected.d/
touch el-release.conf
echo el-release > redhat-release.conf
install -p -c -m 0644 el-release.conf %{buildroot}/etc/dnf/protected.d/
rm -f el-release.conf


# use unbranded datadir
mkdir -p -m 755 %{buildroot}/%{_datadir}/el-release
ln -s el-release %{buildroot}/%{_datadir}/redhat-release
install -m 644 %{SOURCE201}  %{buildroot}/%{_datadir}/redhat-release

# Create doc dir
mkdir -p -m 755 %{buildroot}/%{_docdir}/el-release
# make /usr/share/el-release symlink redhat-release
ln -s el-release %{buildroot}/%{_docdir}/redhat-release
install -m 644  %{SOURCE200}  %{buildroot}/%{_docdir}/el-release


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

# Make dir for yum/dnf repos/vars
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
install -d -m 0755 %{buildroot}%{_sysconfdir}/pki/sb-certs/
install -d -m 0755 %{buildroot}%{_datadir}/pki/sb-certs/

# Install aarch64 certs
install -m 644 %{SOURCE400} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-aarch64.cer
install -m 644 %{SOURCE400} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-aarch64.cer
install -m 644 %{SOURCE400} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-aarch64.cer
install -m 644 %{SOURCE400} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-fwupd-aarch64.cer

# Install x86_64 certs
install -m 644 %{SOURCE400} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-ca-x86_64.cer
install -m 644 %{SOURCE400} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-kernel-x86_64.cer
install -m 644 %{SOURCE400} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-grub2-x86_64.cer
install -m 644 %{SOURCE400} %{buildroot}%{_datadir}/pki/sb-certs/secureboot-fwupd-x86_64.cer

# Link x86_64 certs
ln -sr %{buildroot}%{_datadir}%{_datadir}/pki/sb-certs/secureboot-ca-x86_64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-ca-x86_64.cer
ln -sr %{buildroot}%{_datadir}%{_datadir}/pki/sb-certs/secureboot-kernel-x86_64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-kernel-x86_64.cer
ln -sr %{buildroot}%{_datadir}%{_datadir}/pki/sb-certs/secureboot-grub2-x86_64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-grub2-x86_64.cer
ln -sr %{buildroot}%{_datadir}%{_datadir}/pki/sb-certs/secureboot-fwupd-x86_64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-fwupd-x86_64.cer

# Link aarch64 certs
ln -sr %{buildroot}%{_datadir}%{_datadir}/pki/sb-certs/secureboot-ca-aarch64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-ca-aarch64.cer
ln -sr %{buildroot}%{_datadir}%{_datadir}/pki/sb-certs/secureboot-kernel-aarch64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-kernel-aarch64.cer
ln -sr %{buildroot}%{_datadir}%{_datadir}/pki/sb-certs/secureboot-grub2-aarch64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-grub2-aarch64.cer
ln -sr %{buildroot}%{_datadir}%{_datadir}/pki/sb-certs/secureboot-fwupd-aarch64.cer %{buildroot}%{_sysconfdir}/pki/sb-certs/secureboot-fwupd-aarch64.cer

%clean
rm -rf %{buildroot}

%post
# File to be edited
file="/etc/motd"

# Define the multi-line string to be appended or checked
# Note: The leading newline ensures the text starts on a new line when appended
text='
!!!
Last packages for EuroLinux distribution were released on 23rd October 2024.
The EuroLinux team advises and supports migration to Rocky Linux using the instructions linked below:
https://docs.euro-linux.com/HowTo/migrate_to_rocky_linux/

For technical support services check:
https://euro-linux.com/en/software/technical-support/
'

# Escape special characters and newlines in the text for use in sed
# This allows sed to correctly match the text in the file
text_escaped=$(echo "$text" | sed -n '
    H                   # Append each line to the hold space
    1h                  # On first line, copy to hold space instead of appending to wipe out the initial \n in hold space
    ${                  # On last line...
      g                 # Get the entire text from hold space
      s/[\/&\.]/\\&/g     # Escape forward slashes, ampersands, dots
      s/\n/\\n/g        # Replace newlines with \n
      p                 # Print the escaped text
    }
  '
)

# Check if file is empty OR if it doesn't contain the text, then append
if [ ! -s "$file" ] || sed -ni '
  H                     # Append each line to the hold space
  1h                    # On first line, copy to hold space instead of appending to wipe out the initial \n in hold space
  ${                    # On last line...
    g                   # Get the entire file content from hold space
    s/'"$text_escaped"'/&/  # Try to substitute the escaped text with same text (it might be another text in the future)
    p                   # Print the result (for debugging, can be removed)
    Ta                  # If substitution failed (text not found), branch to label a (like append)
    q1                  # If text was found, exit sed with status 1
    :a                  # Label for branch
    q                   # Exit sed with status 0 if text was not found
  }
' $file
then
  # Append the text to the file if it's empty or doesn't contain the text
  echo "$text" >> "$file"
fi

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

/etc/yum.repos.d
%config(noreplace) /etc/dnf/vars/*
# FIXME waiting for swid tag
#/etc/swid/swidtags.d
#%{_prefix}/lib/swidtag/%{swid_regid}
#/etc/pki/swid/CA/%{swid_regid}
# EULA etc
%{_datadir}/el-release/*
%{_datadir}/redhat-release




%files -n eurolinux-sb-certs
## Note to future packagers:
# The symlinks are not %config(noreplace) intentionally. We want them to be
# restored if this package is updated.
%dir %{_sysconfdir}/pki/sb-certs
%dir %{_datadir}/pki/sb-certs
%{_sysconfdir}/pki/sb-certs/*.cer
%{_datadir}/pki/sb-certs/*.cer


%changelog
* Wed Oct 23 2024 Paweł Piasek <pp@euro-linux.com> - 9.4-3.0
- Add note about EuroLinux EOL to motd

* Tue May 07 2024 Alex Baranowski <ab@euro-linux.com> - 9.4-2.0
- 9.4 GA release (San Marino)

* Tue Nov 07 2023 Paweł Piasek <pp@euro-linux.com> - 9.3-1.0
- 9.3 GA release

* Sat Sep 30 2023 Paweł Piasek <pp@euro-linux.com> - 9.3-0.0
- prepare for 9.3beta

* Tue May 09 2023 <pp@euro-linux.com> - 9.2-1.0
- prepare for GA release

* Thu May 04 2023 <pp@euro-linux.com> - 9.2-0.2
- New code name for 9.2beta
- BuildArch: noarch

* Mon Apr 03 2023 Paweł Piasek <pp@euro-linux.com> - 9.2-0.1
- 9.2 Beta release

* Fri Nov 25 2022 Kamil Aronowski <ka@euro-linux.com> - 9.1-2.1
- SecureBoot certificates

* Wed Nov 23 2022 Paweł Piasek <pp@euro-linux.com> - 9.1-2.0
- Setup links to mirrorlist in eurolinux.repo

* Thu Nov 10 2022 Paweł Piasek <pp@euro-linux.com> - 9.1-1.1
- remove beta tags from repos. Prepare for GA version.

* Tue Oct 18 2022 Paweł Piasek <pp@euro-linux.com> - 9.1-1.0
- Initial release for EuroLinux 9.1 beta
- Based on redhat-release-9.1-1.8

* Mon Sep 26 2022 Alex Baranowski <ab@euro-linux.com> - 9.0-0.8
- Remove comment from /etc/os-release as not all parsers support it correctly

* Tue Jun 28 2022 Paweł Piasek <pp@euro-linux.com> - 9.0-0.7
- Obsoletes rhc and inights-client packages.

* Tue Jun 07 2022 Alex Baranowski <ab@euro-linux.com> - 9.0-0.6
- Remove beta macro so it's impossible to build package wrongly

* Sun May 29 2022 Alex Baranowski <ab@euro-linux.com> - 9.0-0.5
- Change PowerTools to CBR

* Sun May 29 2022 Alex Baranowski <ab@euro-linux.com> - 9.0-0.4
- Update release

* Tue May 24 2022 Pawel Piasek  <pp@euro-linux.com> - 9.0-0.3
- For GA release

* Sun Feb 27 2022 Alex Baranowski <alex@euro-linux.com>  - 9.0-0.2
- Now el-release uses proper beta repos.

* Sat Jan 29 2022 Alex Baranowski <alex@euro-linux.com> - 9.0-0.1
- Initial Release for EuroLinux 9 beta
- Sarajevo as Codename (Can change - Pool still in progress)
- Based on redhat-release 9.0-2.11
