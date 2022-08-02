# Fortran on Arm64

## Availability and Standards Compliance
There are many Fortran compilers available for Arm64 including:
 * [NVIDIA HPC Compiler](https://docs.nvidia.com/hpc-sdk/compilers/hpc-compilers-user-guide/index.html)
 * Cray/HPE Compiler
 * GCC
 * LLVM
 * Arm Compiler for Linux

The NVIDIA HPC Compiler is a direct decedent of the popular PGI Fortran compiler, so it accepts the same compiler flags.  GCC and LLVM operate more-or-less the same on Arm64 as on other architectures except for the `-mcpu` flag, as described below.  The Arm Compiler for Linux is based on LLVM and includes additional optimizations for Arm Neoverse cores that make it a highly performant compiler for CPU-only applications.  However, it is missing some Fortran 2008 and OpenMP 4.5+ features that may be desirable for GPU-accelerated applications.  


## Enabling Arm Architecture Specific Features
For gfortran on Arm64, `-mcpu=` acts as both specifying the appropriate architecture and tuning and it's generally better to use that vs `-march` or `-mtune` if you're building for a specific CPU.  You can find additional details in this [presentation from Arm Inc. to Stony Brook University](https://www.stonybrook.edu/commcms/ookami/_pdf/Linford_OokamiUGM_2022.pdf).

CPU       | Flag    | gfortran version      | LLVM verison
----------|---------|-------------------|-------------
Any Arm64 | `-mcpu=native` | gfortran-9+ | flang/LLVM 10+
Ampere Altra | `-mcpu=neoverse-n1` | gfortran-9+ | flang/LLVM 10+


## Compilers
Whenever possible, please use the latest compiler version available on your system. Newer compilers provide better support and optimizations for Arm64 processors. Many codes will demonstrate at least 15% better performance when using GCC 10 vs. GCC 7.  The table below shows GCC and LLVM compiler versions available in Linux distributions. Starred version marks the default system compiler.

Distribution    | GCC                  | Clang/LLVM
----------------|----------------------|-------------
Ubuntu 22.04    | 9, 10, 11*, 12       | 11, 12, 13, 14*
Ubuntu 20.04    | 7, 8, 9*, 10         | 6, 7, 8, 9, 10, 11, 12
Ubuntu 18.04    | 4.8, 5, 6, 7*, 8     | 3.9, 4, 5, 6, 7, 8, 9, 10
Debian10        | 7, 8*                | 6, 7, 8
Red Hat EL8     | 8*, 9, 10            | 10
SUSE Linux ES15 | 7*, 9, 10            | 7


## Large-System Extensions (LSE)
All server-class Arm64 processors support low-cost atomic operations which can improve system throughput for CPU-to-CPU communication, locks, and mutexes. On recent Arm64 CPUs, the improvement can be up to an order of magnitude when using LSE atomics instead of load/store exclusives.  See [Locks, Synchronization, and Atomics](../optimization/atomics.md) for details.


### Enabling LSE
gfortran's `-mcpu=native` flag enables all instructions supported by the host CPU, including LSE.  If you're cross compiling, use the appropriate `-mcpu` option for your target CPU, e.g. `-mcpu=neoverse-n1` for the Ampere Altra CPU. You can check which Arm features gfortran will enable with the `-mcpu=native` flag by using this command:
```bash
gcc -dM -E -mcpu=native - < /dev/null | grep ARM_FEATURE
```
For example, on the Ampere Altra CPU with GCC 9.4, we see "`__ARM_FEATURE_ATOMICS 1
`" indicating that LSE atomics are enabled:
```c
gcc -dM -E -mcpu=native - < /dev/null | grep ARM_FEATURE
#define __ARM_FEATURE_ATOMICS 1
#define __ARM_FEATURE_UNALIGNED 1
#define __ARM_FEATURE_AES 1
#define __ARM_FEATURE_IDIV 1
#define __ARM_FEATURE_QRDMX 1
#define __ARM_FEATURE_DOTPROD 1
#define __ARM_FEATURE_CRYPTO 1
#define __ARM_FEATURE_FP16_SCALAR_ARITHMETIC 1
#define __ARM_FEATURE_FP16_VECTOR_ARITHMETIC 1
#define __ARM_FEATURE_FMA 1
#define __ARM_FEATURE_CLZ 1
#define __ARM_FEATURE_SHA2 1
#define __ARM_FEATURE_CRC32 1
#define __ARM_FEATURE_NUMERIC_MAXMIN 1
```

### Checking for LSE in a binary
To confirm that LSE instructions are used, the output of the `objdump` command line utility should contain LSE instructions:
```bash
$ objdump -d app | grep -i 'cas\|casp\|swp\|ldadd\|stadd\|ldclr\|stclr\|ldeor\|steor\|ldset\|stset\|ldsmax\|stsmax\|ldsmin\|stsmin\|ldumax\|stumax\|ldumin\|stumin' | wc -l
```
To check whether the application binary contains load and store exclusives:
```bash
$ objdump -d app | grep -i 'ldxr\|ldaxr\|stxr\|stlxr' | wc -l
```
