### Compilers

Many commercial and open source compilers now support Arm64.  See [the compilers page](compilers.md) for details, recommendations, and best practices.  We also recommend you check the [language-specific considerations](#language-specific-considerations) below.

### Message Passing (MPI)

Practically all MPI libraries support Arm64 with the notable exception of Intel MPI.  See [the MPI page](mpi.md) for details, recommendations, and best practices.

### Math Libraries

Many math libraries support Arm64 CPUs.  In many cases, math libraries supporting Arm64 (e.g. BLIS, OpenBLAS, FFTW, etc.) can be substituted for libraries that have not yet announced support for Arm64 (e.g. Intel MKL).  Arm community members like NVIDIA, AWS, and Oracle are actively contributing to enabling Arm64 support wherever possible. See [the math libraries page](mathlibs.md) for details, recommendations, and best practices.  

All NVIDIA GPU math libraries work perfectly on Arm-hosted GPUs. In this case, the architecture of the host CPU is irrelevant.  If your application uses GPU-accelerated math libraries, proceed exactly as you would on any other platform.

### Spack and EasyBuild

Package managers like Spack and EasyBuild are a great way to get started with Arm64.  Spack is very well supported on Arm64 and can build full software stacks for CPU-only or CPU+GPU applications using GCC, LLVM, Arm, or NVIDIA compilers and math libraries.  Since the Ampere Altra CPU found in the NVIDIA Arm HPC Developer Kit is architecturally similar to the AWS Gravition 2, we recommend you use [AWS's Spack Rolling Binary Cache](https://aws.amazon.com/blogs/hpc/introducing-the-spack-rolling-binary-cache/) to accelerate your Spack software stack deployments.  [See this AWS blog post fore more details](https://aws.amazon.com/blogs/hpc/introducing-the-spack-rolling-binary-cache/).

### Containers
Docker, Kubernetes, Singuarlity, CharlieCloud, Saurs, and many more container engines and frameworks run with excellent performance on Arm64. Please refer [here](containers.md) for information about running container-based workloads.

### Operating Systems
Please check [here](os.md) for more information about which operating system to run on the NVIDIA Arm HPC Developer Kit.

### Recent Updates, Known Issues, and Workarounds
Please see [here](known_issues.md) for recently identified issues and their solutions.  Please also check the [AWS Graviton Getting Started Guide](https://github.com/aws/aws-graviton-getting-started) for known issues and workarounds.