# Optimizing for Arm64

## Detecting Arm Hardware Capabilities at Runtime

There are several ways to determine the available Arm CPU resources and topology at runtime, including:

 * CPU architecture and supported instructions
 * CPU manufacturer
 * Number of CPU sockets 
 * CPU cores per socket
 * Number of NUMA nodes
 * Number of NUMA nodes per socket
 * CPU cores per NUMA node

See [Runtime CPU Detection](cpudetect.md) for more details and example code.


## Debugging Problems

It's possible that incorrect code will work fine on an existing system, but
produce an incorrect result when using a new compiler. This could be because
it relies on undefined behavior in the language (e.g. assuming char is signed in C/C++,
or the behavior of signed integer overflow), contains memory management bugs that
happen to be exposed by aggressive compiler optimizations, or incorrect ordering.
Below are some techniques / tools we have used to find issues
while migrating our internal services to newer compilers and Arm64.

### Using Sanitizers
The compiler may generate code and layout data slightly differently on Arm64
compared to an x86 system and this could expose latent memory bugs that were previously
hidden. On GCC, the easiest way to look for these bugs is to compile with the
memory sanitizers by adding the below to standard compiler flags:

```
    CFLAGS += -fsanitize=address -fsanitize=undefined
    LDFLAGS += -fsanitize=address  -fsanitize=undefined
```

Run the resulting binary, and any bugs detected by the sanitizers will cause
the program to exit immediately and print helpful stack traces and other
information.

### Ordering issues
Arm is weakly ordered, similar to POWER and other modern architectures, while
x86 is a variant of total-store-ordering (TSO).
Code that relies on TSO may lack barriers to properly order memory references.
Arm64 systems are [weakly ordered multi-copy-atomic](https://www.cl.cam.ac.uk/~pes20/armv8-mca/armv8-mca-draft.pdf).

While TSO allows reads to occur out-of-order with writes and a processor to
observe its own write before it is visible to others, the Armv8 memory model has
further relaxations for performance and power efficiency.
**Code relying on pthread mutexes or locking abstractions
found in C++, Java or other languages shouldn't notice any difference.** Code that
has a bespoke implementation of lockless data structures or implements its own
synchronization primitives will have to use the proper intrinsics and
barriers to correctly order memory transactions.  See [Locks, Synchronization, and Atomics](atomics.md) for more information.


### Architecture specific optimization
Sometimes code will have architecture specific optimizations. These can take many forms:
sometimes the code is optimized in assembly using specific instructions for
[CRC](https://github.com/php/php-src/commit/2a535a9707c89502df8bc0bd785f2e9192929422),
other times the code could be enabling a [feature](https://github.com/lz4/lz4/commit/605d811e6cc94736dd609c644404dd24c013fd6f)
that has been shown to work well on particular architectures. A quick way to see if any optimizations
are missing for Arm64 is to grep the code for "`__x86_64__`" preprocessor branches (`ifdef`) and see if there
is corresponding Arm64 code there too. If not, that might be something to improve.

### Lock/Synchronization intensive workload
All server-class Arm64 processors support low-cost atomic operations which can improve system throughput for CPU-to-CPU communication, locks, and mutexes. On recent Arm64 CPUs, the improvement can be up to an order of magnitude when using LSE atomics instead of load/store exclusives.  See [Locks, Synchronization, and Atomics](atomics.md) for details.

## Profiling the code
If you aren't getting the performance you expect, one of the best ways to understand what is
going on in the system is to compare profiles of execution and understand where the CPU cores are
spending time. This will frequently point to a hot function that could be optimized. 

Install the Linux perf tool:
```bash
# Redhat
sudo yum install perf

# Ubuntu
sudo apt-get install linux-tools-$(uname -r)
```

Record a profile:
```bash
# If the program is run interactively
sudo perf record -g -F99 -o perf.data ./your_program

# If the program is a service, sample all cpus (-a) and run for 60 seconds while the system is loaded
sudo perf record -ag -F99 -o perf.data  sleep 60
```

Look at the profile:
```bash
perf report
```

Additionally, there is a tool that will generate a visual representation of the output which can sometimes
be more useful:
```bash
git clone https://github.com/brendangregg/FlameGraph.git
perf script -i perf.data | FlameGraph/stackcollapse-perf.pl | FlameGraph/flamegraph.pl > flamegraph.svg
```