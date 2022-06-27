# Rust on Arm64

Rust is supported on Linux/Arm64 systems as a tier1 platform, just like x86.

### Large-System Extensions (LSE)

LSE improves system throughput for CPU-to-CPU communication, locks, and mutexes.
The improvement can be up to an order of magnitude when using LSE instead of
load/store exclusives. LSE can be enabled in Rust and we've seen cases on 
larger machines where performance is improved by over 3x by setting the `RUSTFLAGS`
environment variable and rebuilding your project.

```
export RUSTFLAGS="-Ctarget-cpu=neoverse-n1"
cargo build --release
```
