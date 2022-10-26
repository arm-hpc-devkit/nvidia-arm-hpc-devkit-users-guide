# Runtime CPU Detection

There are several ways to determine the available Arm CPU resources and topology at runtime, including:

 * CPU architecture and supported instructions
 * CPU manufacturer
 * Number of CPU sockets 
 * CPU cores per socket
 * Number of NUMA nodes
 * Number of NUMA nodes per socket
 * CPU cores per NUMA node

Well-established portable libraries like libnuma and hwloc are a great choice on Arm64.  You can also use Arm's CPUID registers or query OS files.  Since many of these methods serve the same function, you should choose the method that best fits your application.

If you're implementing your own approach, then please look at the Arm Architecture Registers, and especially the Main ID Register (MIDR_EL1): https://developer.arm.com/documentation/ddi0601/2020-12/AArch64-Registers/MIDR-EL1--Main-ID-Register

The source code for the `lscpu` utility is a great example of how to retrieve and use these registers.  For example, here's how to translate the CPU part number in the MIDR_EL1 register to a human-readable string: https://github.com/util-linux/util-linux/blob/master/sys-utils/lscpu-arm.c

Here's the output of `lscpu` on an AWS Graviton 3.
```
[jlinford@c7g-16xlarge-dy-c7g16xlarge-1 ~]$ lscpu
Architecture:        aarch64
Byte Order:          Little Endian
CPU(s):              64
On-line CPU(s) list: 0-63
Thread(s) per core:  1
Core(s) per socket:  64
Socket(s):           1
NUMA node(s):        1
Model:               1
BogoMIPS:            2100.00
L1d cache:           64K
L1i cache:           64K
L2 cache:            1024K
L3 cache:            32768K
NUMA node0 CPU(s):   0-63
Flags:               fp asimd evtstrm aes pmull sha1 sha2 crc32 atomics fphp asimdhp cpuid asimdrdm jscvt fcma lrcpc dcpop sha3 sm3 sm4 asimddp sha512 sve asimdfhm dit uscat ilrcpc flagm ssbs paca pacg dcpodp svei8mm svebf16 i8mm bf16 dgh rng
```

## CPU Hardware Capabilities

To make your binaries more portable across various Arm64 CPUs, you can use Arm64 hardware capabilities to determine the available instructions at runtime.  For example, a CPU core compliant with Armv8.4 must support dot-product, but dot-products are optional in Armv8.2 and Armv8.3.  A developer wanting to build an application or library that can detect the supported instructions in runtime, can follow this example:

```c
#include<sys/auxv.h>
......
  uint64_t hwcaps = getauxval(AT_HWCAP);
  has_crc_feature = hwcaps & HWCAP_CRC32 ? true : false;
  has_lse_feature = hwcaps & HWCAP_ATOMICS ? true : false;
  has_fp16_feature = hwcaps & HWCAP_FPHP ? true : false;
  has_dotprod_feature = hwcaps & HWCAP_ASIMDDP ? true : false;
  has_sve_feature = hwcaps & HWCAP_SVE ? true : false;
```

The full list of Arm64 hardware capabilities is defined in [glibc header file](https://github.com/bminor/glibc/blob/master/sysdeps/unix/sysv/linux/aarch64/bits/hwcap.h) and in the [Linux kernel](https://github.com/torvalds/linux/blob/master/arch/arm64/include/asm/hwcap.h).

## Example Source Code

Here's a complete yet simple example code that higlights some of the methods mentioned above.

```c
#include <stdio.h>
#include <sys/auxv.h>
#include <numa.h>

// https://developer.arm.com/documentation/ddi0601/2020-12/AArch64-Registers/MIDR-EL1--Main-ID-Register
typedef union
{
    struct {
        unsigned int revision : 4;
        unsigned int part : 12;
        unsigned int arch : 4;
        unsigned int variant : 4;
        unsigned int implementer : 8;
        unsigned int _RES0 : 32;
    };
    unsigned long bits;
} MIDR_EL1;

static MIDR_EL1 read_MIDR_EL1()
{
    MIDR_EL1 reg;
    asm("mrs %0, MIDR_EL1" : "=r" (reg.bits));
    return reg;
}


static const char * get_implementer_name(MIDR_EL1 midr)
{
    switch(midr.implementer) 
    {
        case 0xC0: return "Ampere";
        case 0x41: return "Arm";
        case 0x42: return "Broadcom";
        case 0x43: return "Cavium";
        case 0x44: return "DEC";
        case 0x46: return "Fujitsu";
        case 0x48: return "HiSilicon";
        case 0x49: return "Infineon";
        case 0x4D: return "Motorola";
        case 0x4E: return "NVIDIA";
        case 0x50: return "Applied Micro";
        case 0x51: return "Qualcomm";
        case 0x56: return "Marvell";
        case 0x69: return "Intel";
        default:   return "Unknown";
    }
}


static const char * get_part_name(MIDR_EL1 midr)
{
    switch(midr.implementer) 
    {
        case 0x41: // Arm Ltd.
            switch (midr.part) {
                case 0xd03: return "Cortex A53";
                case 0xd07: return "Cortex A57";
                case 0xd08: return "Cortex A72";
                case 0xd09: return "Cortex A73";
                case 0xd0c: return "Neoverse N1";
                case 0xd40: return "Neoverse V1";
                default:    return "Unknown";
            }
        case 0x42: // Broadcom
            switch (midr.part) {
                case 0x516: return "Vulcan";
                default:    return "Unknown";
            }
        case 0x43: // Cavium
            switch (midr.part) {
                case 0x0a1: return "ThunderX";
                case 0x0af: return "ThunderX2";
                default:    return "Unknown";
            }
        case 0x46: // Fujitsu
            switch (midr.part) {
                case 0x001: return "A64FX";
                default:    return "Unknown";
            }
        case 0x4E: // NVIDIA
            switch (midr.part) {
                case 0x000: return "Denver";
                case 0x003: return "Denver 2";
                case 0x004: return "Carmel";
                default:    return "Unknown";
            }
        case 0x50: // Applied Micro
            switch (midr.part) {
                case 0x000: return "EMAG 8180";
                default:    return "Unknown";
            }
        default: return "Unknown";
    }
}




int main(void) 
{
    // Main ID register
    MIDR_EL1 midr = read_MIDR_EL1();

    // CPU ISA capabilities
    unsigned long hwcaps = getauxval(AT_HWCAP);

    printf("CPU revision    : 0x%x\n", midr.revision);
    printf("CPU part number : 0x%x (%s)\n", midr.part, get_part_name(midr));
    printf("CPU architecture: 0x%x\n", midr.arch);
    printf("CPU variant     : 0x%x\n", midr.variant);
    printf("CPU implementer : 0x%x (%s)\n", midr.implementer, get_implementer_name(midr));
    printf("CPU LSE atomics : %sSupported\n", (hwcaps & HWCAP_ATOMICS) ? "" : "Not ");
    printf("CPU NEON SIMD   : %sSupported\n", (hwcaps & HWCAP_ASIMD)   ? "" : "Not ");
    printf("CPU SVE SIMD    : %sSupported\n", (hwcaps & HWCAP_SVE)     ? "" : "Not ");
    printf("CPU Dot-product : %sSupported\n", (hwcaps & HWCAP_ASIMDDP) ? "" : "Not ");
    printf("CPU FP16        : %sSupported\n", (hwcaps & HWCAP_FPHP)    ? "" : "Not ");
    printf("CPU BF16        : %sSupported\n", (hwcaps & HWCAP2_BF16)   ? "" : "Not ");

    if (numa_available() == -1) {
        printf("libnuma not available\n");
    }
    printf("CPU NUMA nodes  : %d\n", numa_num_configured_nodes());
    printf("CPU Cores       : %d\n", numa_num_configured_cpus());

    return 0;
}
```