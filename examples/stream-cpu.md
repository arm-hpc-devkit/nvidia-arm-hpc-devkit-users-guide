# STREAM on Arm64 CPU

**IMPORTANT**:
These benchmarks provide a _lower bound_ for expected out-of-the-box performance.  They can be used to determine if your system is configured correctly and operating properly.  It's possible you may exceed these numbers.  **They are not indented for use in any competitive analysis.**

 * [NVIDIA HPC SDK](#nvidia-hpc-sdk)
 * [GNU Compilers](#gnu-compilers)
 * [Arm Compiler for Linux (ACfL)](#arm-compiler-for-linux-acfl)


## Initial Configuration
STREAM is a defacto standard for measuring memory bandwidth.
The benchmark includes four kernels that operate on 1D arrays `a`, `b`, and `c`, with scalar `x`: 
 * **COPY**: `c = a`
 * **SCALE**: `b = x*a`
 * **ADD**: `c = a + b`
 * **TRIAD**: `a = b + x*c`

The kernels are executed in sequence in a loop.  Two parameters configure STREAM:
 * `STREAM_ARRAY_SIZE`: The number of double-precision elements in each array.
   It is critical to select a sufficiently large array size when measuring 
   bandwidth to/from main memory.
 * `NTIMES`: The number of iterations of the test loop.

There are many versions of STREAM, but they all use the same four fundamental kernels.  For simplicity we recommend you use this version: https://github.com/jlinford/stream.  This implementation is restructured to demonstrate the performance benefits of OpenMP,
effective use of NUMA, and features of the Arm architecture.  It uses a version of
stream that has been modified to enable dynamic memory allocation and to separate 
the kernel implementation from the benchmark driver.  This makes it the code easier
to read and faciliatates the use of external tools to measure the performance in 
each kernel.

```bash
# Clone the repo
cd $HOME/benchmarks
git clone https://github.com/jlinford/stream.git
# That's it!
```

The Makefile for https://github.com/jlinford/stream uses the `COMPILER` variable to select good default flags for various compilers.  At the time of this writing, GCC, NVIDIA, ACfL, and Futjisu compilers are supported.

## NVIDIA HPC SDK

To build with the NVIDIA compilers and run with OpenMP:

```bash
cd $HOME/benchmarks/stream
make clean run COMPILER=nvidia 
```

TRIAD should report approximately 170GB/s.  Please remember that this number is provided for reference only and should not be used in any competitive analysis.  
```
-------------------------------------------------------------
Function    Best Rate MB/s  Avg time     Min time     Max time
Copy:          168917.9     0.203749     0.203411     0.204257
Scale:         168201.7     0.204544     0.204277     0.204850
Add:           170183.6     0.303268     0.302847     0.303862
Triad:         170309.1     0.303220     0.302624     0.303913
-------------------------------------------------------------
```

## GNU Compilers

To build with GCC and run with OpenMP:

```bash
cd $HOME/benchmarks/stream
make clean run COMPILER=gnu 
```

TRIAD should report approximately 168GB/s.  Please remember that this number is provided for reference only and should not be used in any competitive analysis.  
```
-------------------------------------------------------------
Function    Best Rate MB/s  Avg time     Min time     Max time
Copy:          165916.1     0.207446     0.207091     0.207838
Scale:         168685.6     0.204652     0.203691     0.205092
Add:           167601.9     0.307983     0.307512     0.308406
Triad:         167755.8     0.307578     0.307230     0.307824
-------------------------------------------------------------
```

## Arm Compiler for Linux (ACfL)

To build with ACfL and run with OpenMP:

```bash
cd $HOME/benchmarks/stream
make clean run COMPILER=acfl
```

TRIAD should report approximately 168GB/s. Please remember that this number is provided for reference only and should not be used in any competitive analysis.  
```
-------------------------------------------------------------
Function    Best Rate MB/s  Avg time     Min time     Max time
Copy:          164732.6     0.209005     0.208579     0.209475
Scale:         166109.4     0.207151     0.206850     0.207815
Add:           169040.6     0.305355     0.304895     0.305726
Triad:         168924.2     0.305628     0.305105     0.306131
-------------------------------------------------------------
```

