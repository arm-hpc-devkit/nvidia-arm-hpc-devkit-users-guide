# Operating Systems available for NVIDIA Arm HPC Deveveloper Kit

 Name | Version | [LSE Support](optimizing.md#locksynchronization-intensive-workload) | Kernel page size | Recommended Minimum Kernel Version | Download | Comment
------ | ------ | ----- | ----- | ----- | ----- | -----
Ubuntu | 20.04 LTS or later | Yes | 4KB | TBD | LINK | Yes | 
Ubuntu | 18.04 LTS | Yes (*) | 4KB | TBD | LINK | Yes | (*) needs `apt install libc6-lse`
SuSE | 15 SP2 or later| Planned | 4KB | TBD | LINK | Yes | 
Redhat Enterprise Linux | 8.2 or later | Yes | 64KB | TBD | LINK | Yes | 
AlmaLinux | 8.4 or later | Yes | 64KB | TBD | LINK | Yes |
Alpine Linux | 3.12.7 or later | Yes (*) | 4KB | TBD | LINK | | (*) LSE enablement checked in version 3.14 |
CentOS | 8.2.2004 or later | No | 64KB | TBD | LINK | Yes | |
CentOS Stream | 8 | No (*) | 64KB (*) | TBD | LINK | |(*) details to be confirmed once AMI's are available|
Debian | 11 | Yes | 4KB | TBD | LINK | Yes |
Debian | 10 | Yes (*) | 4KB | TBD | LINK | Yes, as of Debian 10.7 (2020-12-07) |
FreeBSD | 12.1 or later | No | 4KB | TBD | No | Device hotplug and API shutdown don't work
FreeBSD | 13.0 or later | Yes | 4KB | TBD | No | Device hotplug and API shutdown don't work
Rocky Linux | 8.4 or later | Yes (*) | 64KB (*) | TBD | [ISOs](https://rockylinux.org/download) | [Release Notes](https://docs.rockylinux.org/release_notes/8-changelog/)
