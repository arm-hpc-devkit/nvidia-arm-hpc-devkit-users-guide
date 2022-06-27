# Java on Arm64

Java is a general-purpose programming language. Compiled Java code can run on all platforms that support Java, without the need for recompilation. Java applications are typically compiled to bytecode that can run on any Java virtual machine (JVM) regardless of the underlying computer architecture. _[Wikipedia](https://en.wikipedia.org/wiki/Java_(programming_language))_

Java is well supported and generally performant out-of-the-box on Arm64. While Java 8 is fully supported on Arm64, some customers haven't been able to obtain the CPU's full performance benefit until they switched to Java 11.

This page includes specific details about building and tuning Java applications on Arm64.

## Java JVM Options
There are numerous options that control the JVM and may lead to better performance. Two that have shown large (1.5x) improvements in some Java workloads are:

 * Eliminating tiered compilation: `-XX:-TieredCompilation`
 * Restricting the size of the code cache to enable Arm64 cores to better predict branches: `-XX:ReservedCodeCacheSize=64M -XX:InitialCodeCacheSize=64M`
 
These are helpful on some workloads but can hurt on others so testing with and without them is essential.

## Java Stack Size
For some JVMs, the default stack size for Java threads (i.e. `ThreadStackSize`) is 2MB on Arm64 instead of the 1MB used on x86_64. You can check the default with:
```
$ java -XX:+PrintFlagsFinal -version | grep ThreadStackSize
     intx CompilerThreadStackSize = 2048  {pd product} {default}
     intx ThreadStackSize         = 2048  {pd product} {default}
     intx VMThreadStackSize       = 2048  {pd product} {default}
```
The default can be easily changed on the command line with either `-XX:ThreadStackSize=<kbytes>` or `-Xss<bytes>`. Notice that `-XX:ThreadStackSize` interprets its argument as kilobytes whereas `-Xss` interprets it as bytes. So `-XX:ThreadStackSize=1024` and `-Xss1m` will both set the stack size for Java threads to 1 megabyte:
```
$ java -Xss1m -XX:+PrintFlagsFinal -version | grep ThreadStackSize
     intx CompilerThreadStackSize                  = 2048                                   {pd product} {default}
     intx ThreadStackSize                          = 1024                                   {pd product} {command line}
     intx VMThreadStackSize                        = 2048                                   {pd product} {default}
```

Usually, there's no need to change the default because the thread stack will be committed lazily as it grows. No matter the default, the thread will always only commit as much stack as it really uses (at page size granularity). However, there's one exception to this rule if [Transparent Huge Pages](https://www.kernel.org/doc/html/latest/admin-guide/mm/transhuge.html) (THP) are turned on by default on a system. In that case, the THP page size of 2MB matches exactly with the 2MB default stack size on Arm64 and most stacks will be backed up by a single huge page of 2MB. This means that the stack will be completely committed to memory right from the start. If you're using hundreds or even thousands of threads, this memory overhead can be considerable.

To mitigate this issue, you can either manually change the stack size on the command line (as described above) or you can change the default for THP from `always` to `madvise`:
```
# cat /sys/kernel/mm/transparent_hugepage/enabled
[always] madvise never
# echo madvise > /sys/kernel/mm/transparent_hugepage/enabled
# cat /sys/kernel/mm/transparent_hugepage/enabled
always [madvise] never
```

Notice that even if the the default is changed from `always` to `madvise`, the JVM can still use THP for the Java heap and code cache if you specify `-XX:+UseTransparentHugePages` on the command line.

## Looking for x86 shared-objects in JARs
Java JARs can include shared-objects that are architecture specific. Some Java libraries check
if these shared objects are found and if they are they use a JNI to call to the native library
instead of relying on a generic Java implementation of the function. While the code might work,
without the JNI the performance can suffer.

A quick way to check if a JAR contains such shared objects is to simply unzip it and check if
any of the resulting files are shared-objects and if an Arm64 shared-object is missing:
```
$ unzip foo.jar
$ find . -name "*.so" -exec file {} \;
```
For each x86-64 ELF file, check there is a corresponding aarch64 ELF file in the binaries. With some common packages (e.g. commons-crypto) we've seen that even though a JAR can be built supporting Arm manually, artifact repositories such as Maven don't have updated versions. 

## Building multi-arch JARs
Java is meant to be a write once, and run anywhere language.  When building Java artifacts that
contain native code, it is important to build those libraries for each major architecture to provide
a seamless and optimally performing experience for all consumers.  Code that runs well on both Arm64 and x86
increases the package's utility.

There is nominally a multi-step process to build the native shared objects for each supported architecture before doing the final packaging with Maven, SBT, Gradle etc. Below is an example of how to create your JAR using Maven that contains shared libraries for multiple distributions and architectures:

```
# You will need access to two systems: one x86 and one Arm64.

# On the x86 system:
$ cd java-lib
$ mvn package
$ find target/ -name "*.so" -type f -print

# Note the directory this so file is in.  It will be in a directory
# such as: target/classes/org/your/class/hierarchy/native/OS/ARCH/lib.so

# Now, log into the Arm64 system
$ cd java-lib
$ mvn package

# Repeat the below two steps for each OS and ARCH combination you want to release
$ mkdir target/classes/org/your/class/hierarchy/native/OS/ARCH
$ scp other-system:~/your-java-lib/target/classes/org/your/class/hierarchy/native/OS/ARCH/lib.so target/classes/org/your/class/hierarchy/native/OS/ARCH/

# Create the jar packaging with maven.  It will include the additional
# native libraries even though they were not built directly by this maven process.
$ mvn package

# When creating a single Jar for all platform native libraries, 
# the release plugin's configuration must be modified to specify 
# the plugin's `preparationGoals` to not include the clean goal.
# See http://maven.apache.org/maven-release/maven-release-plugin/prepare-mojo.html#preparationGoals
# For more details.

# To do a release to Maven Central and/or Sonatype Nexus:
$ mvn release:prepare
$ mvn release:perform
```

This is one way to do the JAR packaging with all the libraries in a single JAR.  To build all the JARs, we recommend to build on native machines, but it can also be done via Docker using the buildx plug-in, or by cross-compiling inside your build-environment.

There are two additional options for releasing jars with native code.  You can use a manager plugin such as the [nar maven plugin](https://maven-nar.github.io/) to manage each platform specific Jar.  Or, you can release individual architecture specific jars, and then use one system to download these released jars and package them into a combined Jar with a final `mvn release:perform`.  An example of this method can be found in the [Leveldbjni-native](https://github.com/fusesource/leveldbjni) `pom.xml` files. 


## Profiling Java applications
For languages that rely on a JIT (such an Java), the symbol information that is captured is lacking, making it difficult to understand where runtime is being consumed. Similar to the code profiling example above, `libperf-jvmti.so` can be used to dump symbols for JITed code as the JVM runs.

```bash
# Compile your Java application with -g

# find where libperf-jvmti.so is on your distribution

# Run your java app with -agentpath:/path/to/libperf-jvmti.so added to the command line
# Launch perf record on the system
$ perf record -g -k 1 -a -o perf.data sleep 5

# Inject the generated methods information into the perf.data file
$ perf inject -j -i perf.data -o perf.data.jit

# Process the new file, for instance via Brendan Gregg's Flamegraph tools
$ perf script -i perf.data.jit | ./FlameGraph/stackcollapse-perf.pl | ./FlameGraph/flamegraph.pl > ./flamegraph.svg
```