# WRF on Arm64

The [Weather Research and Forecasting (WRF) Model](https://www.mmm.ucar.edu/weather-research-and-forecasting-model) is a next-generation mesoscale numerical weather prediction system designed for both atmospheric research and operational forecasting needs. It features two dynamical cores, a data assimilation system, and a software architecture facilitating parallel computation and system extensibility. 

Arm64 is supported by the standard WRF distribution as of WRF 4.3.3. The following is an example of how to perform the standard procedure to build and execute on Arm64.  See [http://www2.mmm.ucar.edu/wrf/users/download/get_source.html](http://www2.mmm.ucar.edu/wrf/users/download/get_source.html) for more details.

## Quick Start with Spack

One of the easiest ways to use WRF on Arm64 is to install it via Spack.  Simply executing `spack install wrf` will install the latest version of WRF.  However, we recommend you also install a recent version of GCC and then use that GCC installation to build WRF to get the best performance.  For example, 
```bash
spack install gcc@12.1.0
spack load gcc@12.1.0
spack compiler find
spack install wrf %gcc@12.1.0
```

## Build from Source

### Dependencies
WRF depends on the NetCDF Fortran library, which in turn requires the NetCDF C library and HDF5.  All these packages support Arm64 and build easily with GCC.  Be sure to set the environment variables `HDFDIR` and `NETCDF` to be the location of the HDF5 and NetCDF installations _Note: it is assumed that the Fortran NetCDF interface has been installed at the same location as the C library, i.e. they share the same `lib` and `include` directories._ 

### Download WRF Source
The WRF source code can be downloaded [here](https://github.com/wrf-model/WRF/releases). E.g.  
```bash
wget https://github.com/wrf-model/WRF/archive/refs/tags/v4.4.tar.gz
```
Once downloaded, unpack the archive and `cd` into the `WRF-4.4` folder.
```bash
tar v4.4.tar.gz
cd WRF-4.4
```

### Configure and Compile WRF with GCC
Run WRF's configure script then choose an option 1-4 and select default for nesting. This will produce the `configure.wrf' file:
```
./configure
```
For faster parallel compilations, edit Line 507 of the "compile" script and increase from 20 to the max number of parallel threads available (change `"$second_word" <= "20"`) Then use WRF's compile script to build the target executable:
``` 
./compile -j 80 em_real >& compile.log &
```

### \[Optional\] Compiling with Arm Compiler for Linux
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

### CONUS 12km test
Download a CONUS (Contiguous US) test deck from www2.mmm.ucar.edu. The 12km case is around 1.8GB.
```bash
wget https://www2.mmm.ucar.edu/wrf/src/conus12km.tar.gz
```

Copy the existing `run` directory to a new location, for example:
```bash
cp -r run run_CONUS12km
cd run_CONUS12km
```
then extract `conus12km.tar.gz` into the `run_CONUS12km` directory.

It may be necessary to increase the stack size before running:
```
ulimit -s unlimited
```

Execute the test problem using a symlink to the WRF executable in the `run_CONUS12km` directory, for example:
```
OMP_NUM_THREADS=10 OMP_PLACES=cores OMP_PROC_BIND=close mpirun -np 8 -map-by socket:PE=10 ./wrf.exe 
```

### CONUS 2.5km test
The 2.5km test deck is also available from www2.mmm.ucar.edu and is around 18GB.
```
wget https://www2.mmm.ucar.edu/wrf/src/conus2.5km.tar.gz
```
Follow steps as for the 12km case.
