# Arkouda Server and Client on Arm64

![Arkouda Logo](https://github.com/Bears-R-Us/arkouda/raw/master/pictures/arkouda_wide_marker1.png)

Arkouda allows a user to interactively issue massively parallel computations on distributed data using functions and syntax that mimic NumPy, the underlying computational library used in the vast majority of Python data science workflows. The computational heart of Arkouda is a Chapel interpreter that accepts a pre-defined set of commands from a client and uses Chapel's built-in machinery for multi-locale and multithreaded execution. Arkouda has benefited greatly from Chapel's distinctive features and has also helped guide the development of the language.  For more details see https://github.com/Bears-R-Us/arkouda.

## Initial Configuration

Clone the Arkouda repo.  The following steps will take place inside the repo directory.
```bash
git clone https://github.com/Bears-R-Us/arkouda.git
cd arkouda
```
We recommend using GCC version 11 or later.  For example, Spack is an easy way to install GCC 12.1.0:
```bash
# Install spack, if you haven't already
git clone https://github.com/spack/spack.git

# Install gcc+binutils, if you haven't already
spack install gcc@12.1.0+binutils
spack load gcc@12.1.0+binutils
spack compiler find
```

## Install Arkouda Client
We will use [Miniconda](https://docs.conda.io/en/latest/miniconda.html) to provide a Python environment and manage Python dependencies.  
```bash
# Install Miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh
chmod +x Miniconda3-latest-Linux-aarch64.sh
./Miniconda3-latest-Linux-aarch64.sh -b

# Add Miniconda3 to the environment
source ~/.bashrc

# Make sure you're in the Arkouda repo directory.
cd arkouda

# Developer conda env
conda env create -f arkouda-env-dev.yml
conda activate arkouda-dev

# User conda env
conda env create -f arkouda-env.yml     
conda activate arkouda

# Install client and server dependencies
conda install -y jupyter 
conda install -y cmake>=3.11.0

# Install the Arkouda Client Package
pip install -e .
```


## Install Chapel
```bash
# Download and unpack the Chapel source in the location where you wish to install Chapel
curl -L https://github.com/chapel-lang/chapel/releases/download/1.27.0/chapel-1.27.0.tar.gz | tar xvzf -

cd chapel-1.27.0

# Set CHPL_HOME
export CHPL_HOME=$PWD

# Add chpl to PATH
source $CHPL_HOME/util/setchplenv.bash

# Set remaining env variables and execute make
# Arkouda documentation recommends adding these variables to a ~/.chplconfig file to prevent having to export them again
cat > ~/.chplconfig <<EOF
CHPL_COMM=gasnet
CHPL_COMM_SUBSTRATE=smp
CHPL_TARGET_CPU=native
CHPL_RE2=bundled
CHPL_LLVM=bundled
EOF
source ~/.chplconfig

# Build Chapel
export GASNET_QUIET=Y
export CHPL_RT_OVERSUBSCRIBED=yes
cd $CHPL_HOME
make -j80 && make -j80 chpldoc

# Add Chapel to your environment
export PATH=$CHPL_HOME/bin/linux64-aarch64:$PATH
```


## Build the Arkouda Server
```bash
# Make sure you're in the Arkouda repo directory.
cd arkouda

# Confirm Chapel version 1.25 or higher
(arkouda-dev) [jlinford@amp001 arkouda]$ chpl --version
chpl version 1.27.0
  built with LLVM version 14.0.0
Copyright 2020-2022 Hewlett Packard Enterprise Development LP
Copyright 2004-2019 Cray Inc.
(See LICENSE file for more details)

# Edit Makefile.paths and add the location of the Arkouda conda environment
# to the first line as shown below
# For example, `cat Makefile.paths` should produce something like: 
#     $(eval $(call add-path,/global/home/groups/amp/miniconda3/envs/arkouda))
#                            ^ 
# Note that there is no space after 'add-path'
cat Makefile.paths

# Build the server
make -j80
```
Here's an an example of the Chapel pass report for a successful build on an Ampere Altra Q80-30 CPU:
```
Pass               Name                   Main    Check    Clean     Time    %     Accum    %                                                                                  
---- ---------------------------------  -------  -------  -------  ------- -----  ------- -----                                                                                
  42 makeBinary                         607.002    0.000    3.069  610.072  47.9  610.072  47.9                                                                                
  13 resolve                            462.449    0.204    3.705  466.358  36.6  1076.430  84.6                                                                               
  41 codegen                             67.254    0.000    0.219   67.473   5.3  1143.903  89.9                                                                               
  22 parallel                            16.878    0.141    0.433   17.452   1.4  1161.355  91.3                                                                               
  20 callDestructors                     14.703    0.000    0.367   15.070   1.2  1176.425  92.4                                                                               
  29 copyPropagation                     13.750    0.101    1.210   15.061   1.2  1191.486  93.6                                                                               
  26 inlineFunctions                      9.320    0.224    2.563   12.107   1.0  1203.593  94.6                                                                               
  36 insertWideReferences                10.182    0.103    0.339   10.623   0.8  1214.216  95.4                                                                               
  33 loopInvariantCodeMotion             10.219    0.086    0.204   10.509   0.8  1224.726  96.2                                                                               
  21 lowerIterators                       7.300    0.148    1.128    8.576   0.7  1233.302  96.9                                                                               
  27 scalarReplace                        4.158    0.168    1.758    6.084   0.5  1239.386  97.4                                                                               
  28 refPropagation                       4.556    0.131    1.364    6.052   0.5  1245.438  97.9                                                                               
  40 denormalize                          4.866    0.000    0.878    5.744   0.5  1251.182  98.3                                                                               
  23 prune                                1.710    0.123    1.861    3.694   0.3  1254.876  98.6                                                                               
  30 deadCodeElimination                  3.328    0.084    0.211    3.622   0.3  1258.498  98.9                                                                               
  37 optimizeOnClauses                    2.077    0.103    0.239    2.419   0.2  1260.917  99.1                                                                               
  39 insertLineNumbers                    1.164    0.105    0.253    1.522   0.1  1262.439  99.2                                                                               
  34 prune2                               1.132    0.086    0.223    1.441   0.1  1263.880  99.3                                                                               
  32 localizeGlobals                      0.701    0.084    0.201    0.986   0.1  1264.866  99.4                                                                               
   9 normalize                            0.940    0.000    0.031    0.971   0.1  1265.836  99.5                                                                               
  19 lowerErrorHandling                   0.749    0.000    0.142    0.891   0.1  1266.728  99.5                                                                               
  18 cullOverReferences                   0.620    0.011    0.155    0.786   0.1  1267.513  99.6                                                                               
  17 flattenFunctions                     0.629    0.011    0.138    0.777   0.1  1268.291  99.7                                                                               
   1 parse                                0.691    0.000    0.013    0.704   0.1  1268.995  99.7                                                                               
  35 returnStarTuplesByRefArgs            0.230    0.086    0.209    0.525   0.0  1269.520  99.8                                                                               
   7 scopeResolve                         0.470    0.001    0.027    0.499   0.0  1270.018  99.8                                                                               
  25 removeUnnecessaryAutoCopyCalls       0.032    0.082    0.252    0.366   0.0  1270.385  99.8                                                                               
  38 addInitCalls                         0.003    0.103    0.240    0.345   0.0  1270.730  99.9                                                                               
  24 bulkCopyRecords                      0.005    0.083    0.243    0.331   0.0  1271.061  99.9                                                                               
  15 checkResolved                        0.176    0.000    0.137    0.313   0.0  1271.374  99.9                                                                               
  31 removeEmptyRecords                   0.000    0.083    0.196    0.280   0.0  1271.653  99.9                                                                               
  14 resolveIntents                       0.122    0.011    0.136    0.269   0.0  1271.922  99.9                                                                               
  11 buildDefaultFunctions                0.131    0.000    0.028    0.159   0.0  1272.081 100.0                                                                               
  16 replaceArrayAccessesWithRefTemps     0.000    0.011    0.136    0.147   0.0  1272.228 100.0                                                                               
     init                                 0.098    0.000    0.000    0.098   0.0  1272.326 100.0                                                                               
   2 checkParsed                          0.076    0.001    0.007    0.085   0.0  1272.410 100.0                                                                               
   6 cleanup                              0.045    0.000    0.009    0.055   0.0  1272.465 100.0                                                                               
  12 createTaskFunctions                  0.017    0.010    0.023    0.050   0.0  1272.515 100.0                                                                               
  10 checkNormalized                      0.009    0.001    0.017    0.026   0.0  1272.541 100.0                                                                               
     driverCleanup                        0.019    0.000    0.000    0.019   0.0  1272.560 100.0                                                                               
   5 expandExternArrayCalls               0.001    0.000    0.006    0.007   0.0  1272.568 100.0                                                                               
   8 flattenClasses                       0.000    0.000    0.007    0.007   0.0  1272.574 100.0                                                                               
   3 docs                                 0.000    0.000    0.007    0.007   0.0  1272.581 100.0                                                                               
   4 readExternC                          0.000    0.000    0.007    0.007   0.0  1272.587 100.0                                                                               
     startup                              0.000    0.000    0.000    0.000   0.0  1272.587 100.0                                                                               

     total time                         1247.814    2.384   22.390  1272.587
```

## Test Arkouda
Use `make check` to run the builtin correctness checks.  For example:
```bash
(arkouda) [jlinford@amp001 arkouda]$ make check    
INFO:root:Starting "['/global/home/groups/amp/arkouda/arkouda_server', '--trace=false', '--serverConnectionInfo=/global/home/groups/amp/arkouda/ak-server-info', '-nl 2', '--Ser
verPort=5555']"
<jemalloc>: Unsupported system page size
INFO:root:Running client "['python3', '/global/home/groups/amp/arkouda/tests/check.py', 'localhost', '5555']"
    _         _                   _
   / \   _ __| | _____  _   _  __| | __ _
  / _ \ | '__| |/ / _ \| | | |/ _` |/ _` |
 / ___ \| |  |   < (_) | |_| | (_| | (_| |
/_/   \_\_|  |_|\_\___/ \__,_|\__,_|\__,_|


Client Version: v2022.07.08+6.g9d84d1ea.dirty
<jemalloc>: Unsupported system page size
>>> Sanity checks on the arkouda_server
connected to arkouda server tcp://*:5555                                                                                                                                        
check boolean : Passed 
check arange : Passed
check linspace : Passed
check ones : Passed
check zeros : Passed
check argsort : Passed
check coargsort : Passed
check sort : Passed
check get slice [::2] : Passed
check set slice [::2] = value: Passed
check set slice [::2] = pda: Passed
check (compressing) get bool iv : Passed
check (expanding) set bool iv = value: Passed
check (expanding) set bool iv = pda: Passed
check (gather) get integer iv: Passed
check (scatter) set integer iv = value: Passed
check (scatter) set integer iv = pda: Passed
check get integer idx : Passed
check set integer idx = value: Passed
disconnected from arkouda server tcp://*:5555
INFO:root:Running client "['python3', '/global/home/groups/amp/arkouda/util/test/shutdown.py', 'localhost', '5555']"
<jemalloc>: Unsupported system page size
connected to arkouda server tcp://*:5555
Success running checks
```