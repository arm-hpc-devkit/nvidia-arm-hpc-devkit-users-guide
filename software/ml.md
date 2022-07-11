# AI, ML, and DL Frameworks

Many AI, ML, and DL frameworks work well on Arm64-based platforms.  In most cases, you will want to use the Arm-hosted GPU for training or inference.  You may also wish to use the CPU for inference.  See [the examples page](../examples/examples.md) for more information.

The following are known to work well on the NVIDIA Arm HPC Developer Kit:
 * TensorRT: An SDK for high-performance deep learning inference, includes a deep learning inference optimizer and runtime that delivers low latency and high throughput for inference applications.
 * NVIDIA Triton Inference Server: An open-source inference serving software that helps standardize model deployment and execution, delivering fast and scalable AI in production.
 * PyTorch: A GPU accelerated tensor computational framework. Functionality can be extended with common Python libraries such as NumPy and SciPy.
 * TensorFlow: An open source platform for machine learning, providing comprehensive tools and libraries in a flexible architecture allowing easy deployment across a variety of platforms and devices.  
   * Example: [GPU-accelerated training with TensorFlow](../examples/tensorflow-gpu.md) 
   * Example: [on-CPU inference with TensorFlow](../examples/tensorflow-cpu.md)