# Getting started with the NVIDIA Arm HPC Developer Kit
This guide includes how-to guides, sample code, recommendations, and technical best practices to help new users get started with Arm-based systems like the NVIDIA Arm HPC Developer Kit.  While it is intended for the users and administrators of NVIDIA's Arm-based platforms, this guide is also generically useful for anyone running code on Arm CPUs.


## Contents
* [Introduction to Arm64 and the NVIDIA Arm HPC Developer Kit](#introduction-to-arm64-and-the-nvidia-hpc-developer-kit)
* [Transitioning Workloads to Arm64](#transitioning-workloads-to-arm64)
  * [Commercial Software (ISV)](isv.md)
* [Examples](examples.md) 
  * [OpenFOAM](apps/openfoam.md)
  * [WRF](apps/wrf.md)
  * [BWA-MEM2](apps/bwa-mem2.md)
  * [On-CPU Inference with TensorFlow](apps/tensorflow-cpu.md)
  * ... and more! [See this page](applications.md)
* [Supported Software](software.md)
  * [PyTorch](apps/pytorch-gpu.md), [TensorFlow](apps/tensorflow-gpu.md), and[TensorRT](tensorrt.md)
  * [Compilers](compilers.md) and [CUDA](cuda.md)
  * [Message Passing (MPI)](mpi.md)
  * [Math Libraries](mathlibs.md)
  * [Containers](containers.md)
  * [Operating Systems](os.md)
  * ... and more!  [See below](#software-ecosystem)
* [Optimizing for Arm64](optimizing.md)
  * [Arm SIMD Instructions: SVE and NEON](vectorization.md)
  * [Arm Atomic Instructions: LSE](optimizing.md#locksynchronization-intensive-workload)
* [Language-specific Considerations](#language-specific-considerations)
  * [C/C++](langs/c-c++.md)
  * [Go](langs/golang.md)
  * [Java](langs/java.md)
  * [.NET](langs/dotnet.md)
  * [Python](langs/python.md)
  * [Rust](langs/rust.md) 
* [Additional Resources](#additional-resources)
* [Acknowledgements](#acknowledgements)


## Introduction to Arm64 and the NVIDIA HPC Developer Kit

The NVIDIA Arm HPC Developer Kit (simply "DevKit" in this guide) is an integrated hardware and software platform for creating, evaluating, and benchmarking HPC, AI, and scientific computing applications on a heterogeneous GPU- and CPU-accelerated computing system. The kit includes an Arm CPU, an NVIDIA A100 Tensor Core GPU server, and the NVIDIA HPC SDK suite of tools.  [See the product page for more information.](https://developer.nvidia.com/arm-hpc-devkit)

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

 * [Ampere Altra](https://amperecomputing.com/processors/ampere-altra/), which powers the DevKit
 * [NVIDIA Grace](https://www.nvidia.com/en-us/data-center/grace-cpu/)
 * [AWS Graviton](https://aws.amazon.com/ec2/graviton/) 
 * [Alibaba Yitian](https://fuse.wikichip.org/news/tag/yitian-710/)

This guide will call out differences between Arm64 CPUs as needed.  Note that this guide is not intended for mobile and embedded Arm CPUs e.g. NVIDIA Tegra.  While many of the general principles and approaches presented here will hold true for mobile and embedded Arm platforms, this guide is focused on server-class platforms.

## Transitioning Workloads to Arm64
If you are new to Arm64 and want to understand how to identify target workloads, how to plan a transition project, how to test your workloads, and finally how to deploy in production, please read [the key considerations to take into account when transitioning workloads to Arm64](transition-guide.md)

### Commercial Independent Software Vendors (ISV)
There is a large and growing set of Independent Software Vendor (ISV) software available for Arm64.  As an example, an _incomplete, non-exhaustive_ list of products publicly listing Arm64 support can be found [here](isv.md). If your favorite ISV product isn't listed, it **does not** mean it's not supported on Arm64.  Check with the respective ISV to ensure they already, or have plans to, support Arm64.


## Application Examples

Following an example is a great way to get started with a new system.  Here are a few examples of representative codes from major HPC application areas.  You can use these to get a sense for how applications generally work on Arm64.

  * [OpenFOAM](openfoam.md)
  * [WRF](wrf.md)
  * [On-CPU Inference with TensorFlow](tensorflow.md)

## Supported Software




## Optimizing for Arm64
Please see [here](optimizing.md) for general debugging and profiling information.


## Language-specific Considerations
Applications built using interpreted or JIT'd languages should run as-is. Applications using compiled languages including C, C++ or Go, need to be compiled for the Arm64 architecture. Most modern builds (e.g. using Make) will just work when run natively on Arm64.  You’ll find language-specific recommendations below.  If there is no language-specific section, it is because there is no guidance beyond using a suitably current version of the language.

 * [C/C++](c-c++.md)
 * [Go](golang.md)
 * [Java](java.md)
 * [.NET](dotnet.md)
 * [Python](python.md)
 * [Rust](rust.md)


## Additional resources
 * [NVIDIA HPC DevKit](https://developer.nvidia.com/arm-hpc-devkit)
 * [Neoverse N1 Software Optimization Guide](https://documentation-service.arm.com/static/5f05e93dcafe527e86f61acd)
 * [Armv8 reference manual](https://documentation-service.arm.com/static/60119835773bb020e3de6fee)
 * [Package repository search tool](https://pkgs.org/)


# Acknowledgements
This guide was inspired by and borrows from the excellent [AWS Gravton Getting Started Guide](https://github.com/aws/aws-graviton-getting-started).  The authors of this guide gratefully acknowledge the work of the AWS engineers and sincerely thank AWS for freely providing this valuable information in the public domain.


**Feedback?** jlinford@nvidia.com
