# Container-based workloads on Arm64

Containerization has long been of interest to the Arm community.  Today, Arm64 CPUs are exceptionally well optimized for and can be considered ideal for container-based workloads.

## Preparing for Arm64

The first step for leveraging the benefits of Arm64 systems as container hosts is to ensure all production software dependencies support the Arm64 architecture, as one cannot run images built for an x86_64 host on an Arm64 host, and vice versa.

Most of the container ecosystem supports both architectures, and often does so transparently through [multiple-architecture (multi-arch)](https://www.docker.com/blog/multi-platform-docker-builds/) images, where the correct image for the host architecture is deployed automatically.

The major container image repositories, including [Dockerhub](https://hub.docker.com), [Quay](https://www.quay.io), and [Amazon Elastic Container Registry (ECR)](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html) all support [multi-arch](https://aws.amazon.com/blogs/containers/introducing-multi-architecture-container-images-for-amazon-ecr/) images.

### Creating Multi-arch container images

While most images already support multi-arch (i.e. arm64 and x86_64/amd64), we describe couple of ways for developers to to create a multi-arch image if needed.

1. [Docker Buildx](https://github.com/docker/buildx#getting-started)
2. Using a CI/CD Build Pipeline such as [Amazon CodePipeline](https://github.com/aws-samples/aws-multiarch-container-build-pipeline) to coordinate native build and manifest generation.

### Deploying to Arm64

Most container orchestration platforms support both arm64 and x86_64 hosts. As an example, here is an _incomplete, non-exhaustive_ list of popular software within the container ecosystem that explicitly supports Arm64.

| Name                      | URL                           | Comment                |
| :-----                    |:-----                         | :-----                 |
| Tensorflow | https://hub.docker.com/r/armswdev/tensorflow-arm-neoverse |  |
| PyTorch | https://hub.docker.com/r/armswdev/pytorch-arm-neoverse |Use tags with *-openblas* for performance reasons until confirmed otherwise|
| Istio	| https://github.com/istio/istio/releases/	| 1) arm64 binaries as of 1.6.x release series<br>2) [Istio container build instructions](https://github.com/aws/aws-graviton-getting-started/blob/main/containers-workarounds.md#Istio)|
| Envoy	| https://www.envoyproxy.io/docs/envoy/v1.18.3/start/docker ||
| Traefik | https://github.com/containous/traefik/releases	|| 	 
| Flannel | https://github.com/coreos/flannel/releases	 ||	 
| Helm | https://github.com/helm/helm/releases/tag/v2.16.9 || 
| Jaeger | https://github.com/jaegertracing/jaeger/pull/2176 | | 
| Fluent-bit |https://github.com/fluent/fluent-bit/releases/ | compile from source |
| core-dns |https://github.com/coredns/coredns/releases/ | | 
| external-dns | https://github.com/kubernetes-sigs/external-dns/blob/master/docs/faq.md#which-architectures-are-supported | support from 0.7.5+ |
| Prometheus | https://prometheus.io/download/	 	 | |
|containerd	 | https://github.com/containerd/containerd/issues/3664 |	nightly builds provided for arm64 | 
| kube-state-metrics | https://github.com/kubernetes/kube-state-metrics/issues/1037 | use k8s.gcr.io/kube-state-metrics/kube-state-metrics:v2.0.0-beta for arm64 |  
| cluster-autoscaler | https://github.com/kubernetes/autoscaler/pull/3714 | arm64 support as of v1.20.0 | 
|gRPC  | 	https://github.com/protocolbuffers/protobuf/releases/	 | protoc/protobuf support	 |
|Nats	 | 	https://github.com/nats-io/nats-server/releases/	 	 | |
|CNI	 | 	https://github.com/containernetworking/plugins/releases/	| | 	  
|Cri-o	 | 	https://github.com/cri-o/cri-o/blob/master/README.md#installing-crio | tested on Ubuntu 18.04 and 20.04	|
|Trivy	 | 	https://github.com/aquasecurity/trivy/releases/	 	 | |
|Argo	 | 	https://github.com/argoproj/argo-cd/releases 	 	 | arm64 images published as of 2.3.0 |
|Cilium	| https://docs.cilium.io/en/stable/contributing/development/images/ |  Multi arch supported from v 1.10.0 |	 
|Calico	| https://hub.docker.com/r/calico/node/tags?page=1&ordering=last_updated |  Multi arch supported on master |	 
|Tanka	 | 	https://github.com/grafana/tanka/releases	 	 | |
|Consul	 | 	https://www.consul.io/downloads	 	 | |
|Nomad	 | 	https://www.nomadproject.io/downloads	| | 	 
|Packer	 | 	https://www.packer.io/downloads	 	 | |
|Vault	 | 	https://www.vaultproject.io/downloads	| | 
|Terraform | https://github.com/hashicorp/terraform/issues/14474 | arm64 support as of v0.14.0 | 	 	 
|Flux	 | 	https://github.com/fluxcd/flux/releases/ | |
|Pulumi | https://github.com/pulumi/pulumi/issues/4868 | arm64 support as of v2.23.0 |
|New Relic	 | 	https://download.newrelic.com/infrastructure_agent/binaries/linux/arm64/ | |
|Datadog - EC2	 | 	https://www.datadoghq.com/blog/datadog-arm-agent/ ||
|Datadog - Docker	 | 	https://hub.docker.com/r/datadog/agent-arm64	|| 	 
|Dynatrace	 | 	https://www.dynatrace.com/news/blog/get-out-of-the-box-visibility-into-your-arm-platform-early-adopter/	 ||	 
|Grafana	 | 	https://grafana.com/grafana/download?platform=arm ||
|Loki	 | 	https://github.com/grafana/loki/releases ||
|kube-bench | https://github.com/aquasecurity/kube-bench/releases/tag/v0.3.1 ||
|metrics-server | https://github.com/kubernetes-sigs/metrics-server/releases/tag/v0.3.7 | docker image is multi-arch from v.0.3.7 |
| Flatcar Container Linux | https://www.flatcar.org | arm64 support in Stable channel as of 3033.2.0 |

**If your software isn't listed above, it doesn't mean it won't work!**

Many products work on arm64 but don't explicitly distribute arm64 binaries or build multi-arch images *(yet)*. NVIDIA, AWS, Arm, and many developers in the community are working with maintainers and contributing expertise and code to enable full binary or multi-arch support.

## Kubernetes

Kubernetes fully supports Arm64.

If all of your containerized workloads support Arm64, then you can run your cluster with Arm64 nodes exclusively.  However, if you have some workloads that can only run on x86, or if you just want to be able to run both x86 and Arm64 nodes in the same cluster, then there are a couple of ways to accomplish that:

 * **Multiarch Images**: 
 If you are able to use multiarch images (see above) for all containers in your cluster, then you can simply run a mix of x86 and Arm64 nodes without any further action. The multiarch image manifest will ensure that the correct image layers are pulled for a given node's architecture.
 
 * **Built-in labels**: 
 You can schedule pods on nodes according to the `kubernetes.io/arch` [label](https://kubernetes.io/docs/reference/labels-annotations-taints/#kubernetes-io-arch). This label is automatically added to nodes by Kubernetes and allows you to schedule pods accordingly with a [node selector](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#nodeselector) like this: 
 ```
nodeSelector:
  kubernetes.io/arch: amd64
```
 * **Using taints**:
 Taints are especially helpful if adding Arm64 nodes to an existing cluster with mostly x86-only containers. While using the built-in `kubernetes.io/arch` label requires you to explicitly use a node selector to place x86-only containers on the right instances, tainting Arm64 instances prevents Kubernetes from scheduling incompatible containers on them without requiring you to change any existing configuration. For example, you can do this with a managed node group using eksctl by adding `--kubelet-extra-args '--register-with-taints=arm=true:NoSchedule'` to the kubelet startup arguments as documented [here](https://eksctl.io/usage/eks-managed-nodes/). Note that if you only taint Arm64 instances and don't specify any node selectors, then you will need to ensure that the images you build for Arm64 are multiarch images that can also run on x86 instance types. Alternatively, you can build Arm64-only images and ensure that they are only scheduled onto Arm64 images using node selectors.

## Further Reading

* [Building multi-arch docker images with buildx](https://tech.smartling.com/building-multi-architecture-docker-images-on-arm-64-c3e6f8d78e1c)
* [Unifying Arm software development with Docker](https://community.arm.com/developer/tools-software/tools/b/tools-software-ides-blog/posts/unifying-arm-software-development-with-docker)
* [Modern multi-arch builds with docker](https://duske.me/posts/modern-multiarch-builds-with-docker/)
