# Velox on Arm64

Velox is a C++ database acceleration library which provides reusable, extensible, and high-performance data processing components. These components can be reused to build compute engines focused on different analytical workloads, including batch, interactive, stream processing, and AI/ML. Velox was created by Facebook and it is currently developed in partnership with Intel, ByteDance, and Ahana.  See https://github.com/facebookincubator/velox for more information.

What makes Velox interesting on Arm64 is it's use of the xsimd library.  xsimd provides a unified means for using SIMD features for library authors. Namely, it enables manipulation of batches of numbers with the same arithmetic operators as for single values. It also provides accelerated implementation of common mathematical functions operating on batches.  See https://github.com/xtensor-stack/xsimd.

## Build from Source

Note: the standard Velox installation assumes you are running Ubuntu 22.04 LTS and you have root access.  You'll need to modify Velox's setup scripts if this is not the case.

```bash
# Install flex and bison
sudo apt install -y flex bison

# Get the source
git clone --recursive https://github.com/facebookincubator/velox.git
cd velox
git submodule sync --recursive
git submodule update --init --recursive
```

We need to edit `scripts/setup-helper-functions.sh` to fix a bug and update the compiler flags for Arm64.
```bash
# Add missing sudo to ninja command
sed -i 's/ninja -C/sudo ninja -C/' setup-helper-functions.sh

# Fix the compiler flags for Arm
sed -i 's/-march=armv8-a+crc+crypto/-mcpu=neoverse-v1 -flax-vector-conversions -fsigned-char/' setup-helper-functions.sh
```

What are these flags and why do we need them?
 * `-flax-vector-conversions`: Let GCC permit conversions between vectors with differing element types.  This flag is needed because NEON differentiates between vectors of signed and unsigned types.  Without this flag, the compiler will not permit implicit cast operations between such vectors.  Velox relies on such implicit casts in several places so we must relax the compiler's vector conversion rules.
 * `-fsigned-char`: The C++ standard does not specify if `char` is signed or unsigned.  GCC on Arm impliments it as unsigned, but there are places in Velox where it is assumed to be signed.  This flag makes all occurrences of `char` be signed, like `signed char`.
 * `-mcpu=neoverse-n1`: Optional, but this enables the compiler to use all available architecture features and also perform micro-architectural tuning for the Neoverse N1 CPU core.  Using `-mcpu` should produce a more tuned binary than using the `-march` flag.

Now, compile Velox:
```bash
export CPU_TARGET=aarch64
./scripts/setup-ubuntu.sh 
make TREAT_WARNINGS_AS_ERRORS=0 ENABLE_WALL=0 CPU_TARGET=aarch64
```
