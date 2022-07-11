# HPL on Arm64 CPU

**IMPORTANT**:
These benchmarks provide a _lower bound_ for expected out-of-the-box performance.  They can be used to determine if your system is configured correctly and operating properly.  It's possible you may exceed these numbers.  **They are not indented for use in any competitive analysis.**

 * [NVIDIA HPC Compilers](#nvidia-hpc-compilers)
   * [NVIDIA HPC SDK Math Libraries](#nvidia-hpc-sdk-math-libraries)
   * BLIS
   * Arm Performance Libraries
 * [GNU Compilers](#gnu-compilers)
   * OpenBLAS
   * BLIS
   * Arm Performance Libraries


## Introduction

HPL is a software package that solves a (random) dense linear system in double precision (64 bits) arithmetic on distributed-memory computers. It can thus be regarded as a portable as well as freely available implementation of the High Performance Computing Linpack Benchmark.  HPL is notable as the primary benchmark for the [Top500 supercomputers list](https://top500.org/).

HPL's performance is entirely limited by DGEMM performance, so choosing the right BLAS library is critical.  Below we show how you can use different compilers with different BLAS libraries and provide reference numbers.  As stated above, these benchmarks are **not** indented for use in any competitive analysis.


## Initial Configuration
HPL uses tags to identify different build configurations (i.e. combinations of compilers and BLAS libraries), so you can use the same copy of the HPL source for multiple builds as long as the tags are unique.  Follow these steps to download and configure a fresh copy of the HPC source.

```bash
# Download and unpack the HPL source in $HOME/benchmarks
# Note: If you wish to work from directory other than $HOME/benchmarks 
#       then be careful to update 'TOPdir' in the make configuration 
#       files as described below.
mkdir -p $HOME/benchmarks
cd $HOME/benchmarks
curl -L https://www.netlib.org/benchmark/hpl/hpl-2.3.tar.gz | tar xvz

# Initialize a generic HPL configuration file
cd hpl-2.3/setup
bash make_generic

# The make_generic script will create a new file named "Make.UNKNOWN"
# We will use Make.UNKNOWN as the starting point for new configurations
# with different combinations of compilers and BLAS libraries
ls -l Make.generic
```

## HPL.dat
HPL takes its input parameters from a file named `HPL.dat` in the same directory as the `xhpl` executable.  Here is an [example HPL.dat file](HPL.dat) suitable for 512GiB of memory and 80 CPU cores:
```
HPLinpack benchmark input file
Innovative Computing Laboratory, University of Tennessee
HPL.out      output file name (if any) 
6            device out (6=stdout,7=stderr,file)
1            # of problems sizes (N)
231936         Ns
1            # of NBs
192           NBs
0            PMAP process mapping (0=Row-,1=Column-major)
1            # of process grids (P x Q)
8            Ps
10            Qs
16.0         threshold
1            # of panel fact
2            PFACTs (0=left, 1=Crout, 2=Right)
1            # of recursive stopping criterium
4            NBMINs (>= 1)
1            # of panels in recursion
2            NDIVs
1            # of recursive panel fact.
1            RFACTs (0=left, 1=Crout, 2=Right)
1            # of broadcast
1            BCASTs (0=1rg,1=1rM,2=2rg,3=2rM,4=Lng,5=LnM)
1            # of lookahead depth
1            DEPTHs (>=0)
2            SWAP (0=bin-exch,1=long,2=mix)
64           swapping threshold
0            L1 in (0=transposed,1=no-transposed) form
0            U  in (0=transposed,1=no-transposed) form
1            Equilibration (0=no,1=yes)
8            memory alignment in double (> 0)
##### This line (no. 32) is ignored (it serves as a separator). ######
0                               Number of additional problem sizes for PTRANS
1200 10000 30000                values of N
0                               number of additional blocking sizes for PTRANS
40 9 8 13 13 20 16 32 64        values of NB
```

## NVIDIA HPC Compilers

### NVIDIA HPC SDK Math Libraries

The NVIDIA HPC SDK includes BLAS libraries for CPUs as well as GPUs.  Follow these steps to use the NVIDIA-provided CPU BLAS library.

1. Load the NVIDIA HPC Compilers module file.
```bash
module use /opt/nvidia/hpc_sdk/modulefiles/
module load nvhpc/22.5
```

2. Confirm that the `mpifort` wrapper is invoking the NVIDIA Fortran Compiler and check the compiler version.  Note that version 22.5 of the compiler targets Neoverse N1, which is the best option for the Ampere Altra CPU used in the NVIDIA Arm HPC DevKit.
```bash
jlinford@brewster:~/benchmarks/hpl-2.3$ mpifort -show
nvfortran -I/opt/nvidia/hpc_sdk/Linux_aarch64/22.5/comm_libs/openmpi/openmpi-3.1.5/include -I/opt/nvidia/hpc_sdk/Linux_aarch64/22.5/comm_libs/openmpi/openmpi-3.1.5/lib -Wl,-rpath -Wl,$ORIGIN:$ORIGIN/../../lib:$ORIGIN/../../../lib:$ORIGIN/../../../compilers/lib:$ORIGIN/../../../../compilers/lib:$ORIGIN/../../../../../compilers/lib -rpath /opt/nvidia/hpc_sdk/Linux_aarch64/22.5/comm_libs/openmpi/openmpi-3.1.5/lib -L/opt/nvidia/hpc_sdk/Linux_aarch64/22.5/comm_libs/openmpi/openmpi-3.1.5/lib -lmpi_usempif08 -lmpi_usempi_ignore_tkr -lmpi_mpifh -lmpi

jlinford@brewster:~/benchmarks/hpl-2.3$ mpifort --version

nvfortran 22.5-0 linuxarm64 target on aarch64 Linux -tp neoverse-n1
NVIDIA Compilers and Tools
Copyright (c) 2022, NVIDIA CORPORATION & AFFILIATES.  All rights reserved.
```

3. Create a new HPL configuration file from the `Make.UNKNOWN` template.  The patch file can be found here: [NVIDIA_HPC_SDK.patch](NVIDIA_HPC_SDK.patch)
```bash
cd hpl-2.3
cp setup/Make.UNKNOWN Make.NVIDIA_HPC_SDK
patch -p0 < NVIDIA_HPC_SDK.patch
```
Here's a summary of the changes:
```diff
64c64
< ARCH         = NVIDIA_HPC_SDK
---
> ARCH         = UNKNOWN
70c70
< TOPdir       = $(HOME)/benchmarks/hpl-2.3
---
> TOPdir       = $(HOME)/hpl
95,97c95,97
< LAdir        = /opt/nvidia/hpc_sdk/Linux_aarch64/22.5/compilers
< LAinc        = -I$(LAdir)/include
< LAlib        = -L$(LAdir)/lib -lblas
---
> LAdir        =
> LAinc        =
> LAlib        = -lblas
159c159
< HPL_OPTS     = -DHPL_CALL_CBLAS -DHPL_DETAILED_TIMING
---
> HPL_OPTS     =
173c173
< LINKER       = mpicc
---
> LINKER       = mpif77
```

4. Compile
```bash
make arch=NVIDIA_HPC_SDK
```
The resulting executable is at `hpl-2.3/bin/NVIDIA_HPC_SDK/xhpl`.

5. Run
Use the provided [example HPL.dat file](HPL.dat) to solve a 512GiB problem on 80 CPU cores. 
```bash
# Go to the bin directory
cd $HOME/benchmarks/hpl-2.3/bin/NVIDIA_HPC_SDK
# Download the example HPL.dat file
wget "https://raw.githubusercontent.com/arm-hpc-devkit/nvidia-arm-hpc-devkit-users-guide/main/examples/hpl-cpu/HPL.dat"
# Recommended: Flush the page cache.  `free` should report "buff/cache" close to zero 
echo 1 | sudo tee /proc/sys/vm/drop_caches
free
# Run HPL on 80 cores
#  - Set OpenMP threads to "1" as a precaution
#  - Bind MPI ranks to cores
#  - Report process bindings to stdout so we can confirm all's well 
export OMP_NUM_THREADS=1
mpirun -np 80 --report-bindings --map-by core ./xhpl
```
If everything is working properly you should see an HPL score of approximately 1.5 FP64 TeraFLOPS:
```
SCORE
```
Please remember that this number is provided for reference only and should not be used in any competitive analysis.  

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