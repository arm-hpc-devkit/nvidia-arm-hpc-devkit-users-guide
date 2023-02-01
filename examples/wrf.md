# WRF on Arm64

The [Weather Research and Forecasting (WRF) Model](https://www.mmm.ucar.edu/weather-research-and-forecasting-model) is a next-generation mesoscale numerical weather prediction system designed for both atmospheric research and operational forecasting needs. It features two dynamical cores, a data assimilation system, and a software architecture facilitating parallel computation and system extensibility. 

Arm64 is supported by the standard WRF distribution as of WRF 4.3.3. The following is an example of how to perform the standard procedure to build and execute on Arm64.  See [http://www2.mmm.ucar.edu/wrf/users/download/get_source.html](http://www2.mmm.ucar.edu/wrf/users/download/get_source.html) for more details.

## Running the CONUS (Contiguous US) test
Build WRF using one of the methods described below (i.e. via Spack or manually).  
While in the WRF top-level directory (i.e. `WRFV4.4.2`), download a CONUS (Contiguous US) test deck from www2.mmm.ucar.edu:
 - 12km case, about 1.8GB: https://www2.mmm.ucar.edu/wrf/src/conus12km.tar.gz
 - 2.5km case, about 18GB: https://www2.mmm.ucar.edu/wrf/src/conus2.5km.tar.gz

The 12km and 2.5km cases are run in the same way.

```bash
cd $BUILD_DIR/WRFV4.4.2

# Copy the run directory template
cp -a run run_CONUS12km
cd run_CONUS12km

# Download the test case files and merge them into the run directory
curl -L https://www2.mmm.ucar.edu/wrf/src/conus12km.tar.gz | tar xvzf - --strip-components=1

# Unlimit the stack
ulimit -s unlimited

# Run with 8 MPI ranks, each having 10 OpenMP threads
OMP_NUM_THREADS=10 OMP_PLACES=cores OMP_PROC_BIND=close mpirun -np 8 -map-by socket:PE=10 ./wrf.exe 

# Track progress by watching the Rank 0 output file:
tail -f rsl.out.0000
```


## Quick Start with Spack
One of the easiest ways to use WRF on Arm64 is to install it via Spack.  Simply executing `spack install wrf` will install the latest version of WRF.  However, we recommend you also install a recent version of GCC and then use that GCC installation to build WRF to get the best performance.  For example, 
```bash
spack install gcc@12.1.0
spack load gcc@12.1.0
spack compiler find
spack install wrf %gcc@12.1.0
```

## Manually Build from Source

### Dependencies
WRF depends on the NetCDF Fortran library, which in turn requires the NetCDF C library and HDF5.  All these packages support Arm64 and build easily with GCC.  Be sure to set the environment variables `HDFDIR` and `NETCDF` to be the location of the HDF5 and NetCDF installations _Note: it is assumed that the Fortran NetCDF interface has been installed at the same location as the C library, i.e. they share the same `lib` and `include` directories._ 

```bash
# Create a build directory to hold WRF and all its dependencies
mkdir WRF
cd WRF

# Configure build environment
export BUILD_DIR=$PWD
export HDFDIR=$BUILD_DIR/opt
export HDF5=$BUILD_DIR/opt
export NETCDF=$BUILD_DIR/opt

# HDF5
curl -L https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.14/hdf5-1.14.0/src/hdf5-1.14.0.tar.gz | tar xvzf -
cd hdf5-1.14.0
 ./configure --prefix=$HDFDIR --enable-fortran --enable-parallel
make -j && make install
cd $BUILD_DIR

# Only set these _after_ HDF5 has compiled and installed
# Note that LDFLAGS only includes HDF5, not NETCDF
export CC=`which mpicc`
export CXX=`which mpicxx`
export FC=`which mpifort`
export CPPFLAGS="-I$HDFDIR/include" 
export CFLAGS="-I$HDFDIR/include" 
export FFLAGS="-I$HDFDIR/include" 
export LDFLAGS="-L$HDFDIR/lib -lhdf5_hl -lhdf5 -lz"
export PATH=$NETCDF/bin:$PATH
export LD_LIBRARY_PATH=$BUILD_DIR/opt/lib:$LD_LIBRARY_PATH

# NetCDF-c
curl -L https://github.com/Unidata/netcdf-c/archive/refs/tags/v4.9.0.tar.gz | tar xvzf -
cd netcdf-c-4.9.0
./configure --prefix=$NETCDF
make -j && make install
cd $BUILD_DIR

# NetCDF-f
curl -L https://github.com/Unidata/netcdf-fortran/archive/refs/tags/v4.6.0.tar.gz | tar xvzf -
cd netcdf-fortran-4.6.0/
 ./configure --prefix=$NETCDF
make -j && make install
cd $BUILD_DIR
```

### Download WRF Source
The latest WRF source code can be downloaded [here](https://github.com/wrf-model/WRF/releases). 
```bash
cd $BUILD_DIR
curl -L https://github.com/wrf-model/WRF/releases/download/v4.4.2/v4.4.2.tar.gz | tar xvzf -
cd WRFV4.4.2
```

### Configure and Compile WRF with GCC
Run WRF's configure script and select from the provided options.
It's best to select an option from the "Aarch64" row as this will add
`-mcpu=native` and other important compiler flags to the build line.
Other rows in the configuration options may not achieve the best performance.
Choose the default option for nesting (i.e. `1`). 

Make sure `configure` outputs messages like these:
 - `Will use NETCDF in dir: /home/jlinford/workspace/benchmarks/WRF/opt`
 - `Will use HDF5 in dir: /home/jlinford/workspace/benchmarks/WRF/opt`
If you see errors finding NetCDF or HDF5, resolve those errors before proceeding.

```bash
./configure
checking for perl5... no
checking for perl... found /usr/bin/perl (perl)
Will use NETCDF in dir: /home/jlinford/workspace/benchmarks/WRF/opt
Will use HDF5 in dir: /home/jlinford/workspace/benchmarks/WRF/opt
PHDF5 not set in environment. Will configure WRF for use without.
Will use 'time' to report timing information
$JASPERLIB or $JASPERINC not found in environment, configuring to build without grib2 I/O...
------------------------------------------------------------------------
Please select from among the following Linux aarch64 options:

  1. (serial)   2. (smpar)   3. (dmpar)   4. (dm+sm)   GNU (gfortran/gcc)
  2. (serial)   6. (smpar)   7. (dmpar)   8. (dm+sm)   GNU (gfortran/gcc)
  3. (serial)  10. (smpar)  11. (dmpar)  12. (dm+sm)   GCC (gfortran/gcc): Aarch64

Enter selection [1-12] : 11
------------------------------------------------------------------------
Compile for nesting? (1=basic, 2=preset moves, 3=vortex following) [default 1]:

Configuration successful!
```

Then use WRF's compile script to build the target executable:
```bash
# Reset build environment to include `-lnetcdf` in LDFLAGS
export CC=`which mpicc`
export CXX=`which mpicxx`
export FC=`which mpifort`
export CPPFLAGS="-I$HDFDIR/include" 
export CFLAGS="-I$HDFDIR/include" 
export FFLAGS="-I$HDFDIR/include" 
export LDFLAGS="-L$HDFDIR/lib -lnetcdf -lhdf5_hl -lhdf5 -lz"
export PATH=$NETCDF/bin:$PATH
export LD_LIBRARY_PATH=$BUILD_DIR/opt/lib:$LD_LIBRARY_PATH

# Start compilation on 80 cores
./compile -j 80 em_real >& compile.log &
# Watch compilation progress by following the log file:
tail -f compile.log
```

Look for this message at the end of the compilation log:
```
==========================================================================
build started:   Wed Feb  1 03:35:15 UTC 2023
build completed: Wed Feb 1 04:00:21 UTC 2023

--->                  Executables successfully built                  <---

-rwxrwxr-x 1 jlinford jlinford 38182176 Feb  1 04:00 main/ndown.exe
-rwxrwxr-x 1 jlinford jlinford 38284448 Feb  1 04:00 main/real.exe
-rwxrwxr-x 1 jlinford jlinford 37837912 Feb  1 04:00 main/tc.exe
-rwxrwxr-x 1 jlinford jlinford 45049424 Feb  1 03:58 main/wrf.exe

==========================================================================
```

### Optional: Compiling with Arm Compiler for Linux
If you plan to use the Arm Compiler for Linux (ACfL) instead of GCC, note that the stanza for ACfL is not yet part of the standard WRF package. Run WRF's configure script then choose an option 1-4 and select default for nesting. This will produce the `configure.wrf' file:
```
./configure
```
The `configure.wrf' file then needs modifying as follows.
```
sed -i 's/gcc/armclang/g' configure.wrf
sed -i 's/gfortran/armflang/g' configure.wrf
sed -i 's/mpicc/mpicc -DMPI2_SUPPORT/g' configure.wrf
sed -i 's/ -ftree-vectorize//g' configure.wrf
sed -i 's/length-none/length-0/g' configure.wrf
sed -i 's/-frecord-marker\=4/ /g' configure.wrf
sed -i 's/\-w \-O3 \-c/-mcpu=native \-w \-O3 \-c/g' configure.wrf
sed -i 's/\# \-g $(FCNOOPT).*/\-g/g' configure.wrf
sed -i 's/$(FCBASEOPTS_NO_G)/-mcpu=native $(OMP) $(FCBASEOPTS_NO_G)/g' configure.wrf
```
### Optional: Compiling with the NVIDIA HPC SDK
If you plan to use the Compilers that come with the NVIDIA HPC SDK, just like the Arm Compiler for Linux (ACfL), the stanza is not yet part of the standard WRF package. Run WRF's configure script then choose an option 1-4 and select default for nesting. This will produce the `configure.wrf' file:
```
./configure
```
The `configure.wrf' file then needs modifying as follows.
```
sed -i 's/gcc/nvc/g' configure.wrf
sed -i 's/gfortran/nvfortran/g' configure.wrf
sed -i 's/ -ftree-vectorize//g' configure.wrf
sed -i 's/ -fopenmp/-mp/g' configure.wrf
sed -i 's/#-fdefault-real-8/-i4/g' configure.wrf
sed -i 's/ -O3/ -O3 -fast -Minfo/g' configure.wrf
sed -i 's/-funroll-loops//g' configure.wrf
sed -i 's/-ffree-form -ffree-line-length-none/-Mfree/g' configure.wrf
sed -i 's/-fconvert=big-endian -frecord-marker=4/-byteswapio/g' configure.wrf
sed -i 's/\# \-g $(FCNOOPT).*/\-g/g' configure.wrf
sed -i 's/$(FCBASEOPTS_NO_G)/\-march=native $(OMP) $(FCBASEOPTS_NO_G)/g' configure.wrf
```

