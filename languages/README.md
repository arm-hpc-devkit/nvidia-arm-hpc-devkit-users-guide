# Language-specific Considerations
This guide contains language specific sections with recommendations. If there is no language specific section, it is because there is no specific guidance beyond using a suitably current version of the language.  Simply proceed as you would on any other CPUs, Arm-based or otherwise.

Broadly speaking, applications built using interpreted or JIT'd languages ([Python](python.md), [Java](java.md), PHP, Node.js, etc.) should run as-is on Arm64. Applications using compiled languages including [C/C++](c-c++.md), [Fortran](fortran.md), [Go](golang.md), and [Rust](rust.md) need to be compiled for the Arm64 architecture.  Most modern build systems (Make, CMake, Ninja, etc.) will "just work" on Arm64.  Again , if there is no specific guidance it's because everything works _exactly_ the same on Arm64 as on other platforms.

## Language Guides
 * [C/C++](c-c++.md)
 * [Fortran](fortran.md)
 * [Python](python.md)
 * [Rust](rust.md)
 * [Go](golang.md)
 * [Java](java.md)
 * [.NET](dotnet.md)

