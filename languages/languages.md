# Language-specific Considerations
Applications built using interpreted or JIT'd languages (Python, Java, PHP, Node.js, etc.) should run as-is. This guide contains language specific sections with recommendations e.g. [Java](java.md) and [Python](python.md). If there is no language specific section, it is because there is no specific guidance beyond using a suitably current version of the language.  Simply proceed as you would on any other CPUs, Arm-based or otherwise.

Applications using compiled languages including C, C++ or Go, need to be compiled for the Arm64 architecture. Most modern builds (e.g. using Make) will just work when run natively on Arm64.  You’ll find language specific compiler recommendations in this repository: [C/C++](c-c++.md), [Go](golang.md), and [Rust](rust.md).  Again , if there is no specific guidance it's because everything works _exactly_ the same on Arm64 as on other platforms.

## Language Guides
 * [C/C++](c-c++.md)
 * [Fortran](fortran.md)
 * [Python](python.md)
 * [Rust](rust.md)
 * [Go](golang.md)
 * [Java](java.md)
 * [.NET](dotnet.md)

