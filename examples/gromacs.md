# GROMACS on Arm64 CPU with NVIDIA GPU

GROMACS is a versatile package to perform molecular dynamics, i.e. simulate the Newtonian equations of motion for systems with hundreds to millions of particles and is a community-driven project. See https://www.gromacs.org/.

One of GROMACS' attractive features is a high level of optimization for multiple devices, including both Arm64 CPUs and NVIDIA GPUs.  This example will show how to run GROMACS on either the CPU, the GPU, or both!

## Benchmark Files

We'll use the standard Gromacs benchmark data set, ADH.
```bash
mkdir gromacs
cd gromacs
wget ftp://ftp.gromacs.org/benchmarks/ADH_bench_systems.tar.gz
tar xvzf ADH_bench_systems.tar.gz
```

## NVIDIA NGC Container

The easiest way to run GROMACS is to use the optimized GROMACS containers available via NVIDIA NGC. See [the containers page](../software/containers.md) for detailed instructions on how to enable NGC on your NVIDIA DevKit.  For more general information, see https://docs.nvidia.com/ngc/ for prerequisites and setup steps for all HPC containers and instructions for pulling NGC containers.

We'll be using the GROMACS container available at https://catalog.ngc.nvidia.com/orgs/hpc/containers/gromacs.  Start by preprocessing the ADH benchmark files:
```bash
# Navigate to the ADH benchmarks directory
cd gromacs/ADH
# Run the GROMACS preprocessor
docker run -ti --runtime nvidia -v /dev/infiniband:/dev/inifiniband -v $(pwd)/adh_cubic:/benchmark --workdir /benchmark nvcr.io/hpc/gromacs:2022.1 sh -c "gmx grompp -f pme_verlet.mdp"
```

### Running on GPU and CPU
We'll want to map the MPI ranks (`ntmpi`) and OpenMP threads (`ntomp`) such that `ntmpi * ntomp` is equal to all CPU cores, and `ntmpi` is a multiple of the number of GPUs available.  The NVIDIA Arm HPC DevKit has 80 CPU cores and two A100 GPUs, and keeping `ntomp` at about 8 generally produces the best performmance.  Therefore we use:
 * `-ntmpi 10`: Ten MPI ranks, five GPU tasks per GPU
 * `-ntomp 8`: Eight OpenMP threads per MPI rank.

To enable GPU acceleration, we need to indicate which parts of the computation will execute on the CPU, and which will execute on the GPU.  GROMACS provides functionality to account for a wide range of different types of force calculations. For most simulations, the three most important classes (in terms of computational expense) are specified with these command line options:
 * `-nb`: Non-bonded short-range forces
 * `-bonded`: Bonded short-range forces
 * `-pme`: Particle Mesh Ewald (PME) long-range forces

For example, to calculate non-bonded short-range forces on the GPU, use `-nb gpu`.  Or, to calculate these forces on the CPU, use `-nb cpu`.  Note that calculating on the CPU only will take _dramatically_ longer than calcluating on the GPU.  For more information about GROMACS command line options, see [the GROMACS manual](https://manual.gromacs.org/current/index.html).

```bash
# Run GROMACS
docker run -ti --runtime nvidia -v /dev/infiniband:/dev/inifiniband -v $(pwd)/adh_cubic:/benchmark --workdir /benchmark nvcr.io/hpc/gromacs:2022.1 sh -c "gmx mdrun -v -nsteps 100000 -resetstep 90000 -noconfout -ntmpi 10 -ntomp 8 -nb gpu -bonded gpu -pme gpu -npme 1 -nstlist 400 -s topol.tpr"
```

Using two A100 GPUs, you should see a score of about 240 ns/day:
```
               Core t (s)   Wall t (s)        (%)
       Time:      576.388        7.206     7999.1
                 (ns/day)    (hour/ns)
Performance:      239.835        0.100
```

### Additional optimizations for NVIDIA GPU

This [technical blog post from NVIDIA](https://developer.nvidia.com/blog/creating-faster-molecular-dynamics-simulations-with-gromacs-2020/) lists three envrionment variables that can be set to further improve performance in this benchmark.  Note that there are some trade-offs in using these options.
 * `GMX_GPU_DD_COMMS=true`: enable halo exchange communications between PP tasks
 * `GMX_GPU_PME_PP_COMMS=true`: enable communications between PME and PP tasks
 * `GMX_FORCE_UPDATE_DEFAULT_GPU=true`: enable the update and constraints part of the timestep for multi-GPU

 The combination of these settings triggers all optimizations, including dependencies such as GPU-acceleration of buffer operations.  When using these options, it's best to keep a low number of MPI ranks and increase the number of OpenMP threads.  The suggested layout for these options with two GPUs and 80 CPU cores is four MPI ranks with 20 OpenMP threads each.  Use the `--env` flag to set the environment variables in the container:
```bash
docker run -ti --runtime nvidia -v /dev/infiniband:/dev/inifiniband -v $(pwd)/adh_cubic:/benchmark --workdir /benchmark --env GMX_GPU_DD_COMMS=true --env GMX_GPU_PME_PP_COMMS=true --env GMX_FORCE_UPDATE_DEFAULT_GPU=true nvcr.io/hpc/gromacs:2022.1 sh -c "gmx mdrun -v -nsteps 100000 -resetstep 90000 -noconfout -ntmpi 4 -ntomp 20 -nb gpu -bonded gpu -pme gpu -npme 1 -pin on -nstlist 400 -s topol.tpr"
```

With these additional environment variables, you should see about 320 ns/day:
```
               Core t (s)   Wall t (s)        (%)
       Time:      434.716        5.437     7996.2
                 (ns/day)    (hour/ns)
Performance:      317.881        0.076
```


### Interactive shell in GROMACS container

The following command will launch an interactive shell in the GROMACS container using `nvidia-docker` mounting `$HOME/data` from the underlying system as `/data` in the container:

```
$ docker run -it --rm --runtime nvidia --privileged -v $HOME/data:/data nvcr.io/hpc/gromacs:2022.1
```
The command line options are:
 * `-it`: start container with an interactive terminal (short for `--interactive --tty`)
 * `--rm`: make container ephemeral (removes container on exit)
 * `-v host_path:/data`: bind mount `host_path` into the container as `/data`
 * `--runtime nvidia`: allow nvidia GPU's
 * `--privileged`: allow other devices like InfiniBand 
   * See also: [How-to: Deploy RDMA accelerated Docker container over InfiniBand fabric](https://docs.nvidia.com/networking/pages/releaseview.action?pageId=15049785)

This should produce a root prompt within the container.


## Installing from source

Spack is the easiest way to build GROMACS from source.

```bash
# Close the Spack repo, if you haven't already
git clone https://github.com/spack/spack.git
# Recommended but optional: use the latest GCC from Spack.  You may be able to use other compilers, but this is known to work well.
spack install gcc+binutils+piclibs
# Add the new GCC installation to your environment
spack load gcc
# Update Spack's compiler configuration
spack compiler find

# Install GROMACS with GPU acceleration
spack install -j80 gromacs+cuda %gcc@12.1.0
# If no GPUs available, install unaccelerated GROMACS
spack install -j80 gromacs %gcc@12.1.0
```