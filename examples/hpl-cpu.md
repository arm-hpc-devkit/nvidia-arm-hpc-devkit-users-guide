# HPL on Arm64 CPU

HPL is a software package that solves a (random) dense linear system in double precision (64 bits) arithmetic on distributed-memory computers. It can thus be regarded as a portable as well as freely available implementation of the High Performance Computing Linpack Benchmark.  HPL is notable as the primary benchmark for the [Top500 supercomputers list](https://top500.org/).

HPL's performance is entirely limited by DGEMM performance, so choosing the right BLAS library is critical.  Below we show how you can use different compilers with different BLAS libraries and provide reference numbers.

These benchmarks were generated from a known-good NVIDIA Arm HPC DevKit and provide a _lower bound_ for expected out-of-the-box performance.  They can be used to determine if your system is configured correctly and operating properly.  It's possible you may exceed these numbers.  **They are not indented for use in any competitive analysis.**

## Download HPL

Use this command to download and unpack the HPL source.  HPL uses tags to identify different build configurations (i.e. combinations of compilers and BLAS libraries), so you can use the same copy of the HPL source for multiple builds as long as the tags are unique.

```bash
curl -L https://www.netlib.org/benchmark/hpl/hpl-2.3.tar.gz | tar xvz
```


## NVIDIA HPC Compilers

### NVIDIA HPC SDK Math Libraries
TBD

### OpenBLAS
TBD

### BLIS
TBD

### Arm Performance Libraries (ArmPL)
TBD

## GNU Compilers

### NVIDIA HPC SDK Math Libraries
TBD

### OpenBLAS
TBD

### BLIS
TBD

### Arm Performance Libraries (ArmPL)
TBD

## Arm Compiler for Linux

### NVIDIA HPC SDK Math Libraries
TBD

### OpenBLAS
TBD

### BLIS
TBD

### Arm Performance Libraries (ArmPL)
TBD