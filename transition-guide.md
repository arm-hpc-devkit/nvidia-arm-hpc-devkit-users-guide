# Considerations when Transitioning Workloads to Arm64

Today, Arm CPUs power application servers, micro-services, high-performance computing, CPU-based machine learning inference, video encoding, electronic design automation, gaming, open-source databases, and in-memory caches. In most cases transitioning to Arm64 CPUs is simple and straightforward.  This transition guide provides a step-by-step approach to assess your workload to identify and address any potential software changes that might be needed.

## Introduction - Identifying Target Workloads

The quickest and easiest workloads to transition are Linux-based, and built using open-source components or in-house applications where you control the source code. Many open source projects already support Arm64, and having access to the source code allows you to build from source if pre-built artifacts do not already exist. There is also a large and growing set of Independent Software Vendor (ISV) software available for Arm64 (a non-exhaustive list can be found [here](isv.md). However if you license software you’ll want to check with the respective ISV to ensure they already, or have plans to, support Arm.

The following transition guide is organized into a logical sequence of steps as follows:

* [Learning and exploring](#learning-and-exploring)
    * Step 1 -  [Optional] Understand the NVIDIA Arm HPC Developer Kit and review key documentation
    * Step 2 - Explore your workload, and inventory your current software stack
* [Plan your workload transition](#plan-your-workload-transition)
    * Step 3 - Install and configure your application environment
    * Step 4 - [Optional] Build your application(s) and/or container images
* [Test and optimize your workload](#test-and-optimize-your-workload)
    * Step 5 - Testing and optimizing your workload
    * Step 6 - Performance testing

### Learning and Exploring

**Step 1 - [Optional] Understand the NVIDIA Arm HPC Developer Kit and review key documentation**

* [Optional] Start by reviewing [the NVIDIA Arm HPC Developer Kit product page](https://developer.nvidia.com/arm-hpc-devkit).
* [Optional] Watch these recommended presentations to learn more about getting started, porting and tuning applications, and expected performance for key applications:
  * [First hands-on experiences using the NVIDIA Arm HPC Developer Kit](https://www.nvidia.com/en-us/on-demand/session/gtcspring22-s41624/?playlistId=playList-de66fcc9-9c4e-423e-8b03-01e229c610e0)
  * [Getting started with ARM software development: 86 the x86 dependencies in your code](https://www.nvidia.com/en-us/on-demand/session/gtcspring22-s41702/?playlistId=playList-de66fcc9-9c4e-423e-8b03-01e229c610e0)
  * [Port, Profile, and Tune HPC Applications for Arm-based Supercomputers](https://www.nvidia.com/en-us/on-demand/session/gtcspring22-s41788/?playlistId=playList-de66fcc9-9c4e-423e-8b03-01e229c610e0)
  * [Introducing Developer Tools for Arm and NVIDIA systems](https://www.nvidia.com/en-us/on-demand/session/gtcspring21-s32163/?playlistId=playList-de66fcc9-9c4e-423e-8b03-01e229c610e0)

**Step 2 -  Explore your workload, and inventory your current software stack**

Before starting the transition, you will need to inventory your current software stack so you can identify the path to equivalent software versions that support Arm64. At this stage it can be useful to think in terms of software you download (e.g. open source packages, container images, libraries), software you build and software you procure/license. Areas to review:

* [Operating system](os.md), pay attention to specific versions that support Arm64 (usually more recent are better)
* If your workload is container based, check container images you consume for Arm64 support. Keep in mind, many container images now support multiple architectures which simplifies consumption of those images in a mixed-architecture environment. 
* All the libraries, frameworks and runtimes used by the application.
* Tools used to build, deploy and test your application (e.g. compilers, test suites, CI/CD pipelines, provisioning tools and scripts). Note there are language specific sections in this getting started guide with useful pointers to getting the best performance from Arm64 processors.
* Tools and/or agents used to deploy and manage the application in production (e.g. monitoring tools or security agents)
* This guide contains language specifics sections where you'll find additional per-language guidance:
  * [C/C++](c-c++.md)
  * [Go](golang.md)
  * [Java](java.md)
  * [.NET](dotnet.md) 
  * [Python](python.md)
  * [Rust](rust.md)

As a rule, the more current your software environment the more likely you will obtain the full performance entitlement from Arm64.

For each component of your software stack, check for Arm64 support. A large portion of this can be done using existing system configuration and deployment scripts.  As your scripts run and install packages, you will get messages for any missing components.  Some may build from source automatically while others will cause the script to fail. Pay attention to software versions: more current software is easier to transition and will deliver the best performance. If you do need to perform upgrades prior to adopting Arm64, you might consider doing that using an existing x86 environment to minimize the number of changed variables.  We have seen examples where upgrading OS version on x86 was far more involved and time consuming than transitioning to Arm64 after the upgrade. For more details on checking for software support please see Appendix A.

Note: When locating software be aware that some tools, including GCC, refer to the architecture as AArch64, others including the Linux Kernel, call it arm64. When checking packages across various repositories, you’ll find those different naming conventions.


### Plan your workload transition

**Step 3-  Install and configure your application environment**

Complete the installation of your software stack based on the inventory created in Step 2. In many cases your installation scripts can be used as-is or with minor modifications to reference architecture specific versions of components where necessary. The first time through this may be an iterative process as you resolve any remaining dependencies. 

**Step 4 - Build your application(s) and/or container images**

Applications built using interpreted or JIT'd languages (Python, Java, PHP, Node.js, etc.) should run as-is. This guide contains language specific sections with recommendations e.g. [Java](java.md) and [Python](python.md). If there is no language specific section, it is because there is no specific guidance beyond using a suitably current version of the language.  Simply proceed as you would on any other CPUs, Arm-based or otherwise.

Applications using compiled languages including C, C++ or Go, need to be compiled for the Arm64 architecture. Most modern builds (e.g. using Make) will just work when run natively on Arm64.  You’ll find language specific compiler recommendations in this repository: [C/C++](c-c++.md), [Go](golang.md), and [Rust](rust.md).  Again , if there is no specific guidance it's because everything works _exactly_ the same on Arm64 as on other platforms.

Just like an operating system, container images are architecture specific. You will need to build Arm64 container images. You might wish to build multi-arch container images that can run automatically on either x86-64 or Arm64. Check out the [container section](containers.md) of this guide for more details.

You will also need to review any functional and unit test suite(s) to ensure you can test the new build artifacts with the same test coverage you have already for x86 artifacts.

### Test and optimize your workload

**Step 5 - Testing and optimizing your workload**

Now that you have your application stack on Aarch64, you should run your test suite to ensure all regular unit and functional tests pass. Resolve any test failures in the application(s) or test suites until you are satisfied everything is working as expected. Most errors should be related to the modifications and updated software versions you have installed during the transition. (Tip: when upgrading software versions, first test them using an existing x86 environment to minimize the number of variables changed at once. If issues occur then resolve them using the current x86 environment before continuing with the new Arm64 environment). If you suspect architecture specific issues then please have a look to our [C/C++ section ](c-c++.md) which gives advice on how to solve them.

**Step 6 - Performance testing**

With your fully functional application its time to establish a performance baseline on Arm64. In most cases, you should expect performance parity, or even gains.  This guide has sections dedicated to [Optimization](optimizing.md) and a [Performance Runbook](perfrunbook/grace_perfrunbook.md) for you to follow during this stage.

### _Appendix A - locating packages for Arm64/_

Remember: When locating software be aware that some tools, including  GCC, refer to the architecture as AArch64, others including the Linux Kernel, call it arm64. When checking packages across various repositories, you’ll find those different naming conventions, and in some cases just "ARM".

The main ways to check and places to look for will be:

* Package repositories of your chosen Linux distribution. Arm64 support within Linux distributions is largely complete: for example, Debian, which has the largest package repository, has over 98% of its packages built for the Arm64 architecture.
* Container image registry. Amazon ECR now offers [public repositories](https://docs.aws.amazon.com/AmazonECR/latest/public/public-repositories.html) that you can search for [arm64 images](https://gallery.ecr.aws/?architectures=ARM+64&page=1). DockerHub allows you to search for a specific architecture ([e.g. arm64](https://hub.docker.com/search?type=image&architecture=arm64)).
    * Note: Specific to containers you may find an amd64 (x86-64) container image you currently use transitioned to a multi-architecture container image when adding Arm64 support. This means you may not find an explicit Arm64 container, so be sure to check for both as projects may chose to vend discrete images for x86-64 and Arm64 while other projects chose to vend a multi-arch image supporting both architectures.
* On GitHub, you can check for Arm64 versions in the release section. However, some projects don’t use the release section, or only release source archives, so you may need to visit the main project webpage and check the download section. You can also search the GitHub project for "arm64" or "AArch64" to see whether the project has any Arm64 code contributions or issues. Even if a project does not currently produce builds for Arm64, in many cases an Arm64 version of those packages will be available through Linux distributions or additional package repositories (e.g. [EPEL](https://www.redhat.com/en/blog/whats-epel-and-how-do-i-use-it)). You can search for packages using a package search tool such as [pkgs.org](https://pkgs.org/).
* The download section or platform support matrix of your software vendors, look for references to Arm64, AArch64, AWS Gravition, Ampere Altra, or NVIDIA Grace.
