# Operating Systems on Arm64

Current versions of popular Linux distributions (Ubuntu, RedHat, etc.) support Arm64 to the same level as other architectures.  The NVIDIA Arm HPC Developer Kit has been internally tested and qualified using Ubuntu 20.04 and RHEL 8.4 operating systems, but other distributions may also work.


## RedHat Enterprise Linux and Derivatives
Name | Version | [LSE Support](../optimization/optimization.md#locksynchronization-intensive-workload) | Kernel page size | Download | Comment
------ | ------ | ----- | ----- | ----- | -----
RHEL | 9.0 | Yes | 64KB | [ISO](https://developers.redhat.com/content-gateway/file/rhel-9.0-aarch64-dvd.iso) | 
RHEL | 8.6 | Yes | 64KB | [ISO](https://developers.redhat.com/content-gateway/file/rhel-8.6-aarch64-dvd.iso) | 
RHEL | 8.4 | Yes | 64KB | [ISO](https://developers.redhat.com/content-gateway/file/rhel-8.4-aarch64-dvd.iso) | NVIDIA tested and qualified on DevKit
RHEL | 8.2 | Yes | 64KB | [ISO](https://developers.redhat.com/content-gateway/file/rhel-8.2-aarch64-dvd.iso) | 
Rocky Linux | 8.4 or later | Yes | 64KB | [ISO](https://download.rockylinux.org/pub/rocky/8/isos/aarch64/Rocky-8.6-aarch64-dvd1.iso) |
CentOS Stream | 9 | No | 64KB | [ISO](https://mirrors.centos.org/mirrorlist?path=/9-stream/BaseOS/aarch64/iso/CentOS-Stream-9-latest-aarch64-dvd1.iso&redirect=1&protocol=https) | 
CentOS Stream | 8 | No | 64KB | [Mirror List](http://isoredirect.centos.org/centos/8-stream/isos/aarch64/) | 
CentOS | 8.2 or later | No | 64KB | [ISO](http://bay.uchicago.edu/centos-vault/8.2.2004/isos/aarch64/CentOS-8.2.2004-aarch64-dvd1.iso) | 


## Ubuntu
 Name | Version | [LSE Support](../optimization/optimization.md#locksynchronization-intensive-workload) | Kernel page size | Download | Comment
------ | ------ | ----- | ----- | ----- | -----
Ubuntu | 22.04 LTS | Yes | 4KB | [ISO](https://cdimage.ubuntu.com/releases/22.04/release/ubuntu-22.04-live-server-arm64.iso) | 
Ubuntu | 20.04 LTS | Yes | 4KB | [ISO](https://cdimage.ubuntu.com/releases/20.04/release/ubuntu-20.04.4-live-server-arm64.iso) | NVIDIA tested and qualified on DevKit
Ubuntu | 18.04 LTS | Yes (*) | 4KB | [ISO](https://cdimage.ubuntu.com/releases/18.04/release/ubuntu-18.04.6-server-arm64.iso) | (*) needs `apt install libc6-lse`


## SUSE Linux Enterprise Server
 Name | Version | [LSE Support](../optimization/optimization.md#locksynchronization-intensive-workload) | Kernel page size | Download | Comment
------ | ------ | ----- | ----- | ----- | -----
SLES | 15 SP2 or later | Planned | 4KB | [SUSE Download](https://www.suse.com/download/sles/) | 


## Others
Name | Version | [LSE Support](../optimization/optimization.md#locksynchronization-intensive-workload) | Kernel page size | Download | Comment
------ | ------ | ----- | ----- | ----- | -----
AlmaLinux | 9.0 | Yes | 64KB | [Mirror List](https://mirrors.almalinux.org/isos/aarch64/9.0.html) | 
AlmaLinux | 8.6 | Yes | 64KB | [Mirror List](https://mirrors.almalinux.org/isos/aarch64/8.6.html) | 
Alpine Linux | 3.12.7 or later | Yes (*) | 4KB | [ISO](https://dl-cdn.alpinelinux.org/alpine/v3.16/releases/aarch64/alpine-standard-3.16.0-aarch64.iso) | (*) LSE enablement checked in version 3.14 |
Debian | 11 (Bullseye) | Yes | 4KB | [ISO](https://cdimage.debian.org/debian-cd/current/arm64/iso-dvd/debian-11.3.0-arm64-DVD-1.iso) |
Debian | 10 (Buster) | Yes (*) | 4KB | [ISO](https://cdimage.debian.org/cdimage/archive/10.12.0/arm64/iso-dvd/debian-10.12.0-arm64-DVD-1.iso) | LSE supported as of Debian 10.7 (2020-12-07)
FreeBSD | 13.0 or later | Yes | 4KB | [ISO](https://download.freebsd.org/releases/arm64/aarch64/ISO-IMAGES/13.1/FreeBSD-13.1-RELEASE-arm64-aarch64-disc1.iso) | Some DevKit hardware features are not supported





