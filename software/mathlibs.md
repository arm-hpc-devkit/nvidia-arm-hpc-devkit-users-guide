# Math Libraries on Arm64

Many math libraries support Arm64 CPUs.  In many cases, open source math libraries like BLIS, OpenBLAS, FFTW, etc. can be substituted for libraries that have not yet announced support for Arm64 (e.g. Intel MKL).  Arm community members like NVIDIA, AWS, and Oracle are actively contributing to enabling Arm64 support wherever possible.

## GPU Math Libraries

All NVIDIA GPU math libraries work perfectly on Arm-hosted GPUs. In this case, the architecture of the host CPU is irrelevant.  If your application uses GPU-accelerated math libraries, proceed exactly as you would on any other platform.

## Multi-node Math Libraries

Generally speaking, all the multi-node math libraries you expect work well on Arm64.  Trilinos, PETSc, Hypre, SuperLU, and ParMETIS have been used at scale on the Astra system at Sandia (Marvell ThunderX2 with EDR InfiniBand) and at scale on AWS Graviton 2 with EFA.  GPU support has been tested in most of these same libraries at smaller scales.  Spack is often a good option for installing these libraries.
