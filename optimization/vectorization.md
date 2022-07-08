# Arm SIMD Instructions: SVE and NEON

The Arm architecture provides two single-instruction-multiple-data (SIMD) instruction extensions: NEON and SVE.  

Arm Advanced SIMD Instructions (a.k.a. "NEON") is the most common SIMD ISA for Arm64.  It is a fixed-length SIMD ISA that supports vectors of 128 bits.  The first Arm-based supercomputer to appear on the Top500 Supercomputers list ([_Astra_](https://www.sandia.gov/labnews/2018/11/21/astra-2/)) used NEON to accelerate linear algebra, and many applications and libraries are already taking advantage of NEON.  The Ampere Altra CPU found in the NVIDIA Arm HPC Developer Kit supports NEON vectorization.

More recently, Arm64 CPUs have started supporting Arm Scalable Vector Extensions (SVE).  SVE is a length-agnostic SIMD ISA that improves on NEON by supporting more datatypes (e.g. FP16), more powerful instructions (e.g. gather/scatter), and vector lengths of more than 128 bits.  SVE is currently found in the AWS Graviton 3 (2x256 bits), Fujitsu A64FX (2x512 bits), and the Alibaba Yitian 710 (2x128 bits).  All of these CPUs also support NEON.  The Ampere Altra CPU found in the NVIDIA DevKit does not support SVE, only NEON.

This guide is written for developers writing new code or libraries. It presents various ways to take advantage of SIMD instructions whether through compiler auto-vectorization or writing intrinsics.  It also explains how to build portable code that can detect, at runtime, which instructions are available in the host CPU.  This enables developers to  build one binary that supports cores with different capabilities. For example, to support one binary that would run on the NVIDIA Arm HPC Developer Kit with NEON, or the AWS Graviton 3 with SVE.

## Compiler-driven auto-vectorization
Whenever possible, use the most recent version of your compiler.  GCC9 supported NEON auto-vectorization fairly well, but GCC10 has shown impressive improvement over GCC9 in most cases. GCC12 further improves auto-vectorization.

Compiling with `-fopt-info-vec-missed` is good practice to check which loops were not vectorized.  For example, given a code like this:
```c
  1 // test.c 
...
  5 float   a[1024*1024];
  6 float   b[1024*1024];
  7 float   c[1024*1024];
...
 37 for (j=0; j<128;j++) { // outer loop, not expected to be vectorized
 38   for (i=0; i<n ; i+=1){ // inner loop, ideal for vectorization
 39         c[i]=a[i]*b[i]+j;
 40   }
 41 }
```

and compiling with GCC 9:
```
$ gcc test.c -fopt-info-vec-missed -O3
test.c:37:1: missed: couldn't vectorize loop
test.c:39:8: missed: not vectorized: complicated access pattern.
test.c:38:1: missed: couldn't vectorize loop
test.c:39:6: missed: not vectorized: complicated access pattern.
```

Line 37 is the outer loop, which is not expected to vectorize.  But, the inner loop is a prime candidate for vectorization.  A small change to the code to guarantee that the inner loop would always be aligned to 128-bit SIMD will be enough for GCC 9 to auto-vectorize it.
```c
  1 // test.c 
...
  5 float   a[1024*1024];
  6 float   b[1024*1024];
  7 float   c[1024*1024];
...
 19 #if(__aarch64__)
 20 #define ARM_NEON_WIDTH  128
 21 #define VF32    ARM_NEON_WIDTH/32
 22 #else
 23 #define VF32    1
 33 #endif
...
 37 for (j=0; j<128;j++) { // outer loop, not expected to be vectorized
 38   for (i=0; i<( n - n%VF32 ); i+=1){ // forcing inner loop to multiples of 4 iterations
 39         c[i]=a[i]*b[i]+j;
 40   }
 41   // epilog loop
 42   if (n%VF32)
 43         for ( ; i < n; i++) 
 44                 c[i] = a[i] * b[i]+j;
 45 }
```

The code above is forcing the inner loop to iterate multiples of 4 (128-bit SIMD / 32-bit per float). Results:

```
$ gcc test.c -fopt-info-vec-missed -O3
test.c:37:1: missed: couldn't vectorize loop
test.c:37:1: missed: not vectorized: loop nest containing two or more consecutive inner loops cannot be vectorized
```
And the outer loop is still not vectorized as expected, but the inner loop is now vectorized and 3-4x faster. 

As compiler capabilities improve over time, such techniques are rarely needed. Only if your application cannot update to the most recent compilers should you take this approach.  

## Runtime detection of supported SIMD instructions

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

## Porting codes with SSE/AVX intrinsics to NEON

### Detecting Arm64 systems

Projects may fail to build on Arm64 with `error: unrecognized command-line
option '-msse2'`, or `-mavx`, `-mssse3`, etc.  These compiler flags enable x86
vector instructions.  The presence of this error means that the build system may
be missing the detection of the target system, and continues to use the x86
target features compiler flags when compiling for Arm64.

To detect an Arm64 system, the build system can use:
```bash
(test $(uname -m) = "aarch64" && echo "arm64 system") || echo "other system"
```

Another way to detect an arm64 system is to compile, run, and check the return
value of a C program:
```c
# cat << EOF > check-arm64.c
int main () {
#ifdef __aarch64__
  return 0;
#else
  return 1;
#endif
}
EOF

# gcc check-arm64.c -o check-arm64
# (./check-arm64 && echo "arm64 system") || echo "other system"
```

### Translating x86 intrinsics to NEON

When programs contain code with x86 intrinsics, drop-in intrinsic translation tools like [SIMDe](https://github.com/simd-everywhere/simde) or [sse2neon](https://github.com/DLTcollab/sse2neon) can be used to quickly obtain a working program on Arm64.  This is a good starting point for rewriting the x86 intrinsics in either NEON or SVE and will quickly get a prototype up and running.  For example, to port code using AVX2 intrinsics with SIMDe:
```c
#define SIMDE_ENABLE_NATIVE_ALIASES
#include "simde/x86/avx2.h"
```

SIMDe provides a quick starting point to port performance critical codes
to Arm64.  It shortens the time needed to get a working program that then
can be used to extract profiles and to identify hot paths in the code.
Once a profile is established, the hot paths can be rewritten to avoid the overhead of the generic translation.

Since you're rewriting your x86 intrinsics, you might want to take this opportunity to create a more portable version.  Here are some suggestions to consider:

 1. Rewrite in native C/C++, Fortran, or another high-level compiled language.  Compilers are constantly improving, and technologies like Arm SVE enable the autovectorization of codes that formally wouldn't vectorize.  You may be able to avoid platform-specific intrinsics entirely and let the compiler do all the work.

 2. If your application is written in C++, use `std::experimental::simd` from the C++ Parallelism Technical Specification V2 via the `<experimental/simd>` header.

 3. Use the [SLEEF Vectorized Math Library](https://sleef.org/) as a header-based set of "portable intrinsics"
 
 4. Instead of Time Stamp Counter (TSC) RDTSC intrinsics, use standards-compliant portable timers, e.g., `std::chrono` (C++), `clock_gettime` (C/POSIX), `omp_get_wtime` (OpenMP), `MPI_Wtime` (MPI), etc.

 5. 


## Additional resources

 * [Neon Intrinsics](https://developer.arm.com/architectures/instruction-sets/intrinsics/)
 * [Coding for Neon](https://developer.arm.com/documentation/102159/latest/)
 * [Neon Programmer's Guide for Armv8-A](https://developer.arm.com/architectures/instruction-sets/simd-isas/neon/neon-programmers-guide-for-armv8-a)
