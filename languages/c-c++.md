# C/C++ on Arm64

## Availability and Standards Compliance
There are many C/C++ compilers available for Arm64 including:
 * [NVIDIA HPC Compiler](https://docs.nvidia.com/hpc-sdk/compilers/hpc-compilers-user-guide/index.html)
 * Cray/HPE Compiler
 * GCC
 * LLVM
 * Arm Compiler for Linux

The NVIDIA HPC Compiler is a direct decedent of the popular PGI C/C++ compiler, so it accepts the same compiler flags.  GCC and LLVM operate more-or-less the same on Arm64 as on other architectures except for the `-mcpu` flag, as described below.  The Arm Compiler for Linux is based on LLVM and includes additional optimizations for Arm Neoverse cores that make it a highly performant compiler for CPU-only applications.  However, it is missing some Fortran 2008 and OpenMP 4.5+ features that may be desirable for GPU-accelerated applications.  


## Enabling Arm Architecture Specific Features
For GCC on Arm64, `-mcpu=` acts as both specifying the appropriate architecture and tuning and it's generally better to use that vs `-march` or `-mtune` if you're building for a specific CPU.  You can find additional details in this [presentation from Arm Inc. to Stony Brook University](https://www.stonybrook.edu/commcms/ookami/_pdf/Linford_OokamiUGM_2022.pdf).

CPU       | Flag    | GCC version      | LLVM verison
----------|---------|-------------------|-------------
Any Arm64 | `-mcpu=native` | GCC-9+ | Clang/LLVM 10+
Ampere Altra | `-mcpu=neoverse-n1` | GCC-9+ | Clang/LLVM 10+

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

GCC's `-mcpu=native` flag enables all instructions supported by the host CPU, including LSE.  If you're cross compiling, use the appropriate `-mcpu` option for your target CPU, e.g. `-mcpu=neoverse-n1` for the Ampere Altra CPU. You can check which Arm features GCC will enable with the `-mcpu=native` flag by using this command:
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

## Porting SSE or AVX Intrinsics
To quickly get a prototype running on Arm64, one can use
https://github.com/DLTcollab/sse2neon a translator of x64 intrinsics to NEON.
sse2neon provides a quick starting point in porting performance critical codes
to Arm.  It shortens the time needed to get an Arm working program that then
can be used to extract profiles and to identify hot paths in the code.  A header
file `sse2neon.h` contains several of the functions provided by standard x64
include files like `xmmintrin.h`, only implemented with NEON instructions to
produce the exact semantics of the x64 intrinsic.  Once a profile is
established, the hot paths can be rewritten directly with NEON intrinsics to
avoid the overhead of the generic sse2neon translation.

Note that GCC's `__sync` built-ins are outdated and may be biased towards the x86 memory model.  Use `__atomic` versions of these functions instead of the `__sync` versions.  See https://gcc.gnu.org/onlinedocs/gcc/_005f_005fatomic-Builtins.html for more details.


## Signed vs. Unsigned char
The C standard doesn't specify the signedness of char. On x86 char is signed by
default while on Arm it is unsigned by default. This can be addressed by using
standard int types that explicitly specify the signedness (e.g. `uint8_t` and `int8_t`)
or compile with `-fsigned-char`.


## Arm Instructions for Machine Learning
Many Arm64 CPUs support [Arm dot-product instructions](https://community.arm.com/developer/tools-software/tools/b/tools-software-ides-blog/posts/exploring-the-arm-dot-product-instructions) commonly used for Machine Learning (quantized) inference workloads, and [Half precision floating point (FP16)](https://developer.arm.com/documentation/100067/0612/Other-Compiler-specific-Features/Half-precision-floating-point-intrinsics).  These features enable performant and power efficient machine learning by doubling the number of operations per second and reducing the memory footprint compared to single precision floating point (\_float32), all while still enjoying large dynamic range.  Compiling with `-mcpu=native` will enable these features, when available.  See [the examples page](../examples/README.md) for examples of how to use these features in ML frameworks like TensorFlow and PyTorch.
