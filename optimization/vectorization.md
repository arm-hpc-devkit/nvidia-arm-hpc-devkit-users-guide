# Arm SIMD Instructions: SVE and NEON

The Arm architecture provides two single-instruction-multiple-data (SIMD) instruction extensions: NEON and SVE.

Arm Advanced SIMD Instructions (a.k.a. "NEON") is the most common SIMD ISA for Arm64.  It is a fixed-length SIMD ISA that supports vectors of 128 bits.  The first Arm-based supercomputer to appear on the Top500 Supercomputers list ([_Astra_](https://www.sandia.gov/labnews/2018/11/21/astra-2/)) used NEON to accelerate linear algebra, and many applications and libraries are already taking advantage of NEON.  The Ampere Altra CPU found in the NVIDIA Arm HPC Developer Kit supports NEON vectorization.

More recently, Arm64 CPUs have started supporting [Arm Scalable Vector Extensions (SVE)](https://developer.arm.com/documentation/102476/latest/).  SVE is a length-agnostic SIMD ISA that supports more datatypes than NEON (e.g. FP16), offers more powerful instructions (e.g. gather/scatter), and supports vector lengths of more than 128 bits.  SVE is currently found in the AWS Graviton 3, Fujitsu A64FX, and the Alibaba Yitian 710.  SVE is not a new version of NEON, but an entirely new SIMD ISA in it's own right.  Most SVE-capable CPUs also support NEON.

Here's a quick summary of the SIMD capabilities of some of the currently available Arm64 CPUs:

|                        | Alibaba Yitian 710 | AWS Graviton3 | Fujitsu A64FX  | AWS Graviton2 | Ampere Altra |
| ---------------------- | ------------------ | ------------- | -------------- | ------------- | ------------ |
| CPU Core               | Neoverse N2        | Neoverse V1   | A64FX          | Neoverse N1   | Neoverse N1  |
| SIMD ISA               | SVE2 & NEON        | SVE & NEON    | SVE & NEON     | NEON only     | NEON only    |
| NEON Configuration     | 2x128              | 4x128         | 2x128          | 2x128         | 2x128        |
| SVE Configuration      | 2x128              | 2x256         | 2x512          | N/A           | N/A          |
| SVE Version            | 2                  | 1             | 1              | N/A           | N/A          |
| NEON FMLA FP64 TPeak   | 8                  | 16            | 8              | 8             | 8            |
| SVE FMLA FP64 TPeak    | 8                  | 16            | 32             | N/A           | N/A          |

Note that recent Arm64 CPUs provide the same peak theoretical performance for both NEON and SVE.  For example, the Graviton3 can either retire four 128-bit NEON operations or two 256-bit SVE operations.  The Yitian 710 takes this one step further and provides both NEON and SVE in the same configuration (2x128).  On paper, the peak performance of both SVE and NEON are the same for these CPUs, which means there's no intrinsic performance advantage for SVE vs. NEON, or vice versa.  (Note: there are micro-architectural details that can give one ISA a performance advantage over the other in certain conditions, but the upper limit on performance is always the same.)

However, SVE ([and especially SVE2](https://developer.arm.com/documentation/102340/0001/Introducing-SVE2)) is a much more capable SIMD ISA with support for complex datatypes and advanced features that enable vectorization of complicated code.  In practice, kernels that can't be vectorized in NEON _can_ be vectorized with SVE.  So while SVE won't beat NEON in a performance drag race, it can dramatically improve the performance of the application overall by vectorizing loops that would otherwise have executed with scalar instructions.  

Fortunately, auto-vectorizing compilers are usually the best choice when programming Arm SIMD ISAs.  The compiler will generally make the best decision on when to use SVE or NEON, and it will take advantage of SVE's advanced auto-vectorization features more easily than a human coding in intrinsics or assembly is likely to do.  **Generally speaking, you should not write SVE or NEON intrinsics.**  Instead, use the appropriate command line options with your auto-vectorizing compiler to realize the best performance for a given loop.  You may need to use compiler directives or make changes in the high level code to facilitate autovectorization, but this will be much easier and more maintainable than writing intrinsics.  Leave the finer details to the compiler and focus on code patterns that auto-vectorize well.


## Compiler-driven auto-vectorization
The key to maximizing auto-vectorization is to allow the compiler to take full advantage of the available hardware features.  By default, GCC and LLVM compilers take a conservative approach and do not enable advanced features unless explicitly told to do so.  The easiest way to enable all available features for GCC or LLVM is to use the `-mcpu` compiler flag. If you're compiling on the same CPU that the code will run on, use `-mcpu=native`.  Otherwise you can use `-mcpu=<target>` where `<target>` is one of the CPU identifiers, e.g. `-mcpu=neoverse-n1`.  The NVIDIA compilers take a more agressive approach.  By default, they assume the machine you are compiling on is the one you will run on and so will enable all available hardware features detected at compile time.  And whenever possible, use the most recent version of your compiler.  For example, GCC9 supported auto-vectorization fairly well, but GCC10 has shown impressive improvement over GCC9 in most cases. GCC12 further improves auto-vectorization.

The second key compiler feature is the compiler vectorization report.  GCC uses the `-fopt-info` flags to report on auto-vectorization success or failure.  You can use the generated informational messages to guide code annotations or transformations that will facilitate autovectorization.  For example, compiling with `-fopt-info-vec-missed` will report on which loops were not vectorized in a code like this:
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

Compiling with GCC 9:
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


## Relaxed vector conversions
Arm NEON differentiates between vectors of signed and unsigned types.  For example, GCC won't implicitly cast between vectors of signed and unsigned 64-bit integers:
```c
#include <arm_neon.h>
...
uint64x2_t u64x2;
int64x2_t s64x2;
// Error: cannot convert 'int64x2_t' to 'uint64x2_t' in assignment
u64x2 = s64x2;
```

To perform the cast, you must use NEON's `vreinterpretq` functions:
```c
u64x2 = vreinterpretq_u64_s64(s64x2);
```

Unfortunately, some codes written for other SIMD ISAs rely on these kinds of implicit conversions (see the [Velox example](../examples/velox.md)).  If you see errors about "no known conversion" in a code that builds for AVX but doesn't build for NEON then we might need to relax GCC's vector converversion rules: 
```
/tmp/velox/third_party/xsimd/include/xsimd/types/xsimd_batch.hpp:35:11: note:   no known conversion for argument 1 from ‘xsimd::batch<long int>’ to ‘const xsimd::batch<long unsigned int>&’
```
To allow implicit conversions between vectors with differing numbers of elements and/or incompatible element types, use the `-flax-vector-conversions` flag.  This flag should be fine for legacy code, but it should not be used for new code.  The safest option is to use the appropriate `vreinterpretq` calls.


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


## Additional resources

 * [Neon Intrinsics](https://developer.arm.com/architectures/instruction-sets/intrinsics/)
 * [Coding for Neon](https://developer.arm.com/documentation/102159/latest/)
 * [Neon Programmer's Guide for Armv8-A](https://developer.arm.com/architectures/instruction-sets/simd-isas/neon/neon-programmers-guide-for-armv8-a)
