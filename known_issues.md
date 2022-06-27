# Recent Updates, Known Issues, and Workarounds

There is a huge amount of activity in the Arm software ecosystem and improvements are being
made on a daily basis. As a general rule, later versions of compilers and language runtimes
should be used whenever possible. 

## Recent Updates
The table below includes known recent changes to popular packages that improve performance.  If you know of others please let us know.  CONTACT

Package | Version | Improvements
--------|:-:|-------------
bazel	| [3.4.1+](https://github.com/bazelbuild/bazel/releases) | Pre-built bazel binary for Arm64. [See below](#bazel-on-linux) for installation. 
ffmpeg  |   4.3+  | Improved performance of libswscale by 50% with better NEON vectorization which improves the performance and scalability of ffmpeg multi-thread encoders. The changes are available in FFMPEG version 4.3.
HAProxy  | 2.4+  | A [serious bug](https://github.com/haproxy/haproxy/issues/958) was fixed. Additionally, building with `CPU=armv81` improves HAProxy performance by 4x so please rebuild your code with this flag.
mongodb | 4.2.15+ / 4.4.7+ / 5.0.0+ | Improved performance on Arm64, especially for internal JS engine. LSE support added in [SERVER-56347](https://jira.mongodb.org/browse/SERVER-56347).
MySQL   | 8.0.23+ | Improved spinlock behavior, compiled with -moutline-atomics if compiler supports it.
.NET | [5+](https://dotnet.microsoft.com/download/dotnet/5.0) | [.NET 5 significantly improved performance for ARM64](https://devblogs.microsoft.com/dotnet/Arm64-performance-in-net-5/). Here's an [AWS Blog](https://aws.amazon.com/blogs/compute/powering-net-5-with-aws-graviton2-benchmark-results/) with some performance results. 
OpenH264 | [2.1.1+](https://github.com/cisco/openh264/releases/tag/v2.1.1) | Pre-built Cisco OpenH264 binary for Arm64. 
PCRE2   | 10.34+  | Added NEON vectorization to PCRE's JIT to match first and pairs of characters. This may improve performance of matching by up to 8x. This fixed version of the library now is shipping with Ubuntu 20.04 and PHP 8.
PHP     | 7.4+    | PHP 7.4 includes a number of performance improvements that increase perf by up to 30%
pip     | 19.3+   | Enable installation of Python wheel binaries on Arm64.
PyTorch | 1.7+    | Enable Arm64 compilation and NEON optimization for fp32. Install from source. **Note:** *Requires GCC9 or later.*
ruby    | 3.0+ | Enable Arm64 optimizations that improve performance by as much as 40%. These changes have also been back-ported to the Ruby shipping with AmazonLinux2, Fedora, and Ubuntu 20.04.
zlib    | 1.2.8+  | For the best performance on Arm64 please use [zlib-cloudflare](https://github.com/cloudflare/zlib).


## Known Issues

### Postgres
Postgres performance can be heavily impacted by not using [LSE](langs/c-c++.md#large-system-extensions-lse).
Today, postgres binaries from distributions (e.g. Ubuntu) are not built with `-moutline-atomics` or `-march=armv8.2-a` which would enable LSE.  Note: Amazon RDS for PostgreSQL isn't impacted by this. 

In November 2021 PostgreSQL started to distribute Ubuntu 20.04 packages optimized with `-moutline-atomics`.
For Ubuntu 20.04, we recommend using the PostgreSQL PPA instead of the packages distributed by Ubuntu Focal.
Please follow [the instructions to set up the PostgreSQL PPA.](https://www.postgresql.org/download/linux/ubuntu/)

### Python Installation on Some Linux Distros
The default installation of pip on some Linux distributions is too old \(<19.3\) to install binary wheel packages released for Arm64.  To work around this, it is recommended to upgrade your pip installation using:
```
sudo python3 -m pip install --upgrade pip
```

## Bazel on Linux
The [Bazel build tool](https://www.bazel.build/) now releases a pre-built binary for Arm64. As of October 2020, this is not available in their custom Debian repo, and Bazel does not officially provide an RPM. Instead, we recommend using the [Bazelisk installer](https://docs.bazel.build/versions/master/install-bazelisk.html), which will replace your `bazel` command and [keep bazel up to date](https://github.com/bazelbuild/bazelisk/blob/master/README.md).

Below is an example using the [latest Arm64 binary release of Bazelisk](https://github.com/bazelbuild/bazelisk/releases/latest) as of October 2020:
```
wget https://github.com/bazelbuild/bazelisk/releases/download/v1.7.1/bazelisk-linux-arm64
chmod +x bazelisk-linux-arm64
sudo mv bazelisk-linux-arm64 /usr/local/bin/bazel
bazel
```

Bazelisk itself should not require further updates as its only purpose is to keep Bazel updated.

## zlib on Linux
Linux distributions, in general, use the original zlib without any optimizations. zlib-cloudflare has been updated to provide better and faster compression on Arm and x86. To use zlib-cloudflare:
```
git clone https://github.com/cloudflare/zlib.git
cd zlib
./configure --prefix=$HOME
make
make install
```
Make sure to have the full path to your lib at $HOME/lib in /etc/ld.so.conf and run ldconfig.

For users of OpenJDK, which is dynamically linked to the system zlib, you can set LD_LIBRARY_PATH to point to the directory where your newly built version of zlib-cloudflare is located or load that library with LD_PRELOAD.

You can check the libz that JDK is dynamically linked against with:
```
$ ldd /Java/jdk-11.0.8/lib/libzip.so | grep libz
libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007ffff7783000)
```
