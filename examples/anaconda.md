# Anaconda, Miniconda, Conda, and Mamba on Arm64
Anaconda is a distribution of the Python and R programming languages for scientific computing that aims to simplify package management and deployment.


## Anaconda
Anaconda announced [support for Arm64 via AWS Graviton 2 on May 14, 2021](https://www.anaconda.com/blog/anaconda-aws-graviton2). The Ampere Altra CPU found in the NVIDIA Arm HPC DevKit is based on the same Arm Neoverse N1 core as the AWS Gravition2, so Anaconda also supports the Ampere Altra.  *IMPORTANT*: if you encounter errors about missing libraries, see [the dependency information below](#a-quick-note-on-dependencies).

```bash
# Download Anaconda installer
wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-aarch64.sh
# Run the installer
bash Anaconda3-2022.05-Linux-aarch64.sh
```

Additional installation instructions can be found at https://docs.anaconda.com/anaconda/install/graviton2/.


## Miniconda Eaxmple
Anaconda also offers a lightweight version called [Miniconda](https://docs.conda.io/en/latest/miniconda.html) which is a small, bootstrap version of Anaconda that includes only conda, Python, the packages they depend on, and a small number of other useful packages, including pip, zlib and a few others. 

Here is an example on how to use Miniconda to install [numpy](https://numpy.org/) and [pandas](https://pandas.pydata.org/) for Python 3.9.  The resulting installation has a much smaller footprint than the full Anaconda.

The first step is to install conda:
```bash
# Download Miniconda installer
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh
# Run the installer
bash Miniconda3-latest-Linux-aarch64.sh
```

Once installed, you can either use the `conda` command directly to install packages, or write an environment definition file and create the corresponding environment.

Here's an example to install [numpy](https://numpy.org/) and [pandas](https://pandas.pydata.org/) (`arm64-example.yml`):
```yaml
name: arm64-example
dependencies:
  - numpy
  - pandas
```

The next step is to instantiate the environment from that definition:
```bash
conda env create -f arm64-example.yml
```
And you can now use numpy and pandas.


## Mamba

Mamba is a fast, robust, and cross-platform package manager that is fully compatible with conda packages and supports most of conda’s commands.  It fully supports Arm64.  See https://mamba.readthedocs.io/en/latest/# for details.


## A quick note on dependencies

This isn't really an Arm64 requirement since it applies to all platforms.  The installers mentioned in this document don't pull in distro-provided dependencies.  If you see an error like this:
```
/data/jlinford/anaconda3/bin/gtk-query-immodules-3.0: error while loading shared libraries: libXfixes.so.3: cannot open shared object file: No such file or directory
```
then search for the missing library and install the appropriate package. For example, on Ubuntu Server 20.04:
```bash
sudo apt-get install libxi6 libgconf-2-4 libxfixes3 libxcursor1
```
It may take a few tries to get all the dependencies sorted, especially if you're working on a minimal installation of the OS.