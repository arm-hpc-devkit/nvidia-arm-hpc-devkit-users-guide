# Getting started with the NVIDIA Arm HPC Developer Kit
This guide includes how-to guides, sample code, recommendations, and technical best practices to help new users get started with Arm-based systems like the NVIDIA Arm HPC Developer Kit.  While it is intended for the users and administrators of NVIDIA's Arm-based platforms, this guide is also generically useful for anyone running code on Arm CPUs.


## Contents
* [Introduction to Arm64 and the NVIDIA Arm HPC Developer Kit](#introduction-to-arm64-and-the-nvidia-hpc-developer-kit)
* [Transitioning Workloads to Arm64](transition-guide.md)
  * [Commercial Software (ISV)](isv.md)
* [Examples](examples/examples.md)
  * Benchmarks and Health Tests
    * NVIDIA HPC-Benchmarks
    * HPL on CPU
    * HPCG on CPU
    * STREAM on CPU
  * [Modeling and Simulation](examples/examples.md#modeling-and-simulation)
    * [OpenFOAM](examples/openfoam.md)
    * [WRF](examples/wrf.md)
    * [BWA-MEM2](examples/bwa-mem2.md)
    * [... see all mod-sim examples](examples/examples.md#modeling-and-simulation)
  * [Machine Learning](examples/examples.md#machine-learning)
    * [TensorFlow GPU-accelerated Training and Inference](tensorflow-gpu.md)
    * [Tensorflow On-CPU Inference](tensorflow-cpu.md)
    * [... see all ML examples](examples/examples.md#machine-learning)
  * [Data Science](examples/examples.md#data-science)
    * [RAPIDS](examples/rapids.md)
    * [... see all DS examples](examples/examples.md#data-science)
  * ... and more! [See the full list of examples here](examples/examples.md)
* [Supported Software](software/software.md) (See [the full list](software/software.md))
  * [Machine Learning](software/ml.md)
  * [Compilers](software/compilers.md) and [CUDA](software/cuda.md)
  * [Message Passing (MPI)](software/mpi.md)
  * [Math Libraries](software/mathlibs.md)
  * [Containers](software/containers.md)
  * [Operating Systems](software/os.md)
  * ... and more! [See here for more details](software/software.md)
* [Optimizing for Arm64](optimization/optimization.md)
  * [Arm SIMD Instructions: SVE and NEON](optimization/vectorization.md)
  * [Arm Atomic Instructions: LSE](optimization/optimization.md#locksynchronization-intensive-workload)
* [Language-specific Considerations](languages/languages.md)
  * [C/C++](languages/c-c++.md)
  * [Fortran](languages/fortran.md)
  * [Python](languages/python.md)
  * [Rust](languages/rust.md)
  * [Go](languages/golang.md)
  * [Java](languages/java.md)
  * [.NET](languages/dotnet.md)
* [Additional Resources](#additional-resources)
* [Acknowledgements](#acknowledgements)


## Introduction to Arm64 and the NVIDIA HPC Developer Kit
The NVIDIA Arm HPC Developer Kit (simply "DevKit" in this guide) is an integrated hardware and software platform for creating, evaluating, and benchmarking HPC, AI, and scientific computing applications on a heterogeneous GPU- and CPU-accelerated computing system. The kit includes an Arm CPU, dual NVIDIA A100 Tensor Core GPUs, and the NVIDIA HPC SDK suite of tools.  [See the product page for more information.](https://developer.nvidia.com/arm-hpc-devkit)

This validated platform provides quick and easy bring-up and a stable environment for accelerated code execution and evaluation, performance analysis, system experimentation, and system characterization.
 * Delivers a validated system for quick and easy bring-up in familiar HPC environments
 * Offers a stable hardware and software platform for development and performance analysis of accelerated HPC, AI, and scientific computing applications
 * Enables experimentation and characterization of high-performance, NVIDIA-accelerated, Arm server-based system architectures

Hardware | Specification
-------- | --------
Model	   | GIGABYTE G242-P32, 2U server
CPU	     | 1x Ampere Altra Q80-30 (Arm processor)
GPU	     | 2x NVIDIA A100 GPU
Memory	 | 512G DDR4 memory
Storage	 | 6TB SAS/ SATA 3.5″
Network	 | 2x NVIDIA® BlueField®-2 E-Series DPU: 200GbE/HDR single-port QSFP56

The DevKit CPU uses the Arm architecture.  The Arm architecture powers over *two hundred billion* chips across practically all computing domains, so the term "Arm" is somewhat overloaded.  Various communities refer to the architecture as "Arm", "ARM", "Arm64", "AArch64", "arm64", etc.  You may also find the term "SBSA" used to refer to server-class Arm CPUs.  For simplicity, this guide will use the term **"Arm64"** to refer to any CPU built on the Armv8 or Armv9 standards and implementing [Arm's Server Base System Architecture (SBSA)](https://developer.arm.com/documentation/den0029/latest).  This includes CPUs like:

 * [Ampere Altra](https://amperecomputing.com/processors/ampere-altra/) (NVIDIA Arm HPC Developer Kit)
 * [NVIDIA Grace](https://www.nvidia.com/en-us/data-center/grace-cpu/)
 * [AWS Graviton](https://aws.amazon.com/ec2/graviton/) 
 * [Alibaba Yitian](https://fuse.wikichip.org/news/tag/yitian-710/)

This guide will call out differences between Arm64 CPUs as needed.  Note that this guide is not intended for mobile and embedded Arm CPUs e.g. NVIDIA Tegra.  While many of the general principles and approaches presented here will hold true for mobile and embedded Arm platforms, this guide is focused on server-class platforms.


## Additional resources
 * [NVIDIA Arm HPC Developer Kit](https://developer.nvidia.com/arm-hpc-devkit)
 * [Neoverse N1 Software Optimization Guide](https://documentation-service.arm.com/static/5f05e93dcafe527e86f61acd)
 * [Armv8 reference manual](https://documentation-service.arm.com/static/60119835773bb020e3de6fee)
 * [Package repository search tool](https://pkgs.org/)


# Acknowledgements
This guide was inspired by and borrows from the excellent [AWS Graviton Getting Started Guide](https://github.com/aws/aws-graviton-getting-started).  The authors of this guide gratefully acknowledge the work of the AWS engineers and thank AWS for freely providing this valuable information in the public domain.


**Feedback?** jlinford@nvidia.com
