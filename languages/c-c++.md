# C/C++ on Arm64

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
All Arm64 processors have support for the Large-System Extension (LSE) which was first introduced in Armv8.1. LSE provides low-cost atomic operations which can improve system throughput for CPU-to-CPU communication, locks, and mutexes. The improvement can be up to an order of magnitude when using LSE instead of load/store exclusives.

The POSIX threads library needs LSE atomic instructions.  LSE is important for locking and thread synchronization routines.  The following systems distribute a libc compiled with LSE instructions:
- Ubuntu 18.04 (needs `apt install libc6-lse`),
- Ubuntu 20.04,
- Ubuntu 22.04.

The compiler needs to generate LSE instructions for applications that use atomic operations.  For example, the code of databases like PostgreSQL contain atomic constructs; c++11 code with std::atomic statements translate into atomic operations.  GCC's `-mcpu=native` flag enables all instructions supported by the host CPU, including LSE.  To confirm that LSE instructions are created, the output of `objdump` command line utility should contain LSE instructions:
```
$ objdump -d app | grep -i 'cas\|casp\|swp\|ldadd\|stadd\|ldclr\|stclr\|ldeor\|steor\|ldset\|stset\|ldsmax\|stsmax\|ldsmin\|stsmin\|ldumax\|stumax\|ldumin\|stumin' | wc -l
```
To check whether the application binary contains load and store exclusives:
```
$ objdump -d app | grep -i 'ldxr\|ldaxr\|stxr\|stlxr' | wc -l
```

## Porting SSE or AVX Intrinsics to NEON
When programs contain code with x64 intrinsics, the following procedure can help
to quickly obtain a working program on Arm64, assess performance, profile hot spots, and improve the quality of code.

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


## Signed vs. Unsigned char
The C standard doesn't specify the signedness of char. On x86 char is signed by
default while on Arm it is unsigned by default. This can be addressed by using
standard int types that explicitly specify the signedness (e.g. `uint8_t` and `int8_t`)
or compile with `-fsigned-char`.


## Arm Instructions for Machine Learning
Many Arm64 CPUs support [Arm dot-product instructions](https://community.arm.com/developer/tools-software/tools/b/tools-software-ides-blog/posts/exploring-the-arm-dot-product-instructions) commonly used for Machine Learning (quantized) inference workloads, and [Half precision floating point (FP16)](https://developer.arm.com/documentation/100067/0612/Other-Compiler-specific-Features/Half-precision-floating-point-intrinsics).  These features enable performant and power efficient machine learning by doubling the number of operations per second and reducing the memory footprint compared to single precision floating point (\_float32), all while still enjoying large dynamic range.  Compiling with `-mcpu=native` will enable these features, when available.  [See this detailed guide on running TensorFlow on the NVIDIA Arm HPC DevKit for more information.](tensorflow.md)
