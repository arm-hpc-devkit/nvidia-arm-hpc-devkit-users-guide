# Example Applications
Following these step-by-step instructions is a great way to get started with your new Arm64 system.  The codes presented here represent major HPC application areas and are a good starting point for running similar applications on Arm64.  Per-code recommendations and best practices are also provided to help give a sense for how applications from these areas generally work on Arm64.

## Benchmarks and Health Tests

These benchmarks were generated from a known-good NVIDIA Arm HPC DevKit and provide a _lower bound_ for expected out-of-the-box performance.  They can be used to determine if your system is configured correctly and operating properly.  It's possible you may exceed these numbers.  **They are not indented for use in any competitive analysis.**

 * [HPL on CPU](hpl-cpu/hpl-cpu.md)
 * [HPCG on CPU](hpcg-cpu.md)
 * [STREAM on CPU](stream-cpu.md)

## Modeling and Simulation

The high memory bandwidth of the Ampere Altra CPU makes it an excellent platform for CPU-only HPC applications.  

  * [OpenFOAM](openfoam.md)
  * [WRF](wrf.md)
  * [BWA-MEM2](bwa-mem2.md)
  * [GROMACS](gromacs.md)

## Machine Learning

  * [TensorFlow GPU-accelerated Training and Inference](tensorflow-gpu.md)
  * [Tensorflow On-CPU Inference](tensorflow-cpu.md)

## Data Science

  * [RAPIDS](rapids.md)
  