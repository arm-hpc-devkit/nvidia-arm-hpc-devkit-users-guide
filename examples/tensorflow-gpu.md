# TensorFlow on A100 GPUs and Arm64 CPUs

TensorFlow is an open source platform for machine learning. It provides 
comprehensive tools and libraries in a flexible architecture allowing easy 
deployment across a variety of platforms and devices. NGC Containers are the easiest 
way to get started with TensorFlow. The TensorFlow NGC Container comes with all 
dependencies included, providing an easy place to start developing common 
applications, such as conversational AI, natural language processing (NLP), 
recommenders, and computer vision.


## NVIDIA TensorFlow NGC Container
The NVIDIA NGC container registry includes GPU-accelerated Arm64 builds of TensorFlow.  For most cases, this will be your best option both in terms of ease of use and performance. 

The [TensorFlow NGC Container](https://catalog.ngc.nvidia.com/orgs/nvidia/containers/tensorflow) is optimized for GPU acceleration, and contains a 
validated set of libraries that enable and optimize GPU performance. This container 
may also contain modifications to the TensorFlow source code in order to maximize 
performance and compatibility. This container also contains software for 
accelerating ETL (DALI, RAPIDS), Training (cuDNN, NCCL), and Inference (TensorRT) 
workloads.  See https://catalog.ngc.nvidia.com/orgs/nvidia/containers/tensorflow for 
more information.


### Example: Mask-RCNN For TensorFlow 2
Mask R-CNN is a convolution-based neural network for the task of object instance segmentation. The paper describing the model can be found [here](https://arxiv.org/abs/1703.06870). NVIDIA’s Mask R-CNN is an optimized version of [Google's TPU implementation](https://github.com/tensorflow/tpu/tree/master/models/official/mask_rcnn), leveraging mixed precision arithmetic using Tensor Cores while maintaining target accuracy. 

This model is trained with mixed precision using Tensor Cores on the NVIDIA Ampere GPU. Therefore, researchers can get results 2.2x faster than training without Tensor Cores, while experiencing the benefits of mixed precision training.  See the [NVIDIA Deep Learning Examples](https://github.com/NVIDIA/DeepLearningExamples/tree/master/TensorFlow2/Segmentation/MaskRCNN) for more details.

1. Download Mask-RCNN example files
```bash
# Clone the NVIDIA Deep Learning Examples repository
git clone https://github.com/NVIDIA/DeepLearningExamples.git

# Go to the MaskRCNN example for TensorFlow
cd DeepLearningExamples/TensorFlow2/Segmentation/MaskRCNN
```

2. Update the Dockerfile to fix references to outdated software versions.  Newer versions of these packages support Arm64.
```bash
# Update software versions in Dockerfile to enable Arm64 support
cat | patch -p0 << "EOF"
--- Dockerfile  2022-07-07 15:35:29.824463000 -0700
+++ Dockerfile.patched  2022-07-07 15:36:47.041457000 -0700
@@ -12,7 +12,7 @@
 # See the License for the specific language governing permissions and
 # limitations under the License.

-ARG FROM_IMAGE_NAME=nvcr.io/nvidia/tensorflow:21.02-tf2-py3
+ARG FROM_IMAGE_NAME=nvcr.io/nvidia/tensorflow:22.06-tf2-py3
 FROM ${FROM_IMAGE_NAME}

 LABEL model="MaskRCNN"
@@ -30,10 +30,10 @@
     cd /opt/pybind11 && cmake . && make install && pip install .


-# update protobuf 3 to 3.3.0
+# update protobuf 3 to 3.18.2
 RUN \
-    curl -OL https://github.com/protocolbuffers/protobuf/releases/download/v3.3.0/protoc-3.3.0-linux-x86_64.zip && \
-    unzip -u protoc-3.3.0-linux-x86_64.zip -d protoc3 && \
+    curl -OL https://github.com/protocolbuffers/protobuf/releases/download/v3.18.2/protoc-3.18.2-linux-aarch_64.zip && \
+    unzip -u protoc-3.18.2-linux-aarch_64.zip -d protoc3 && \
     mv protoc3/bin/* /usr/local/bin/ && \
     mv protoc3/include/* /usr/local/include/
EOF
```

3. Update example files to support TensorFlow2.
```bash
cat | patch -p0 <<"EOF"
--- mrcnn_tf2/runtime/run.py      2022-07-07 16:01:33.565361000 -0700
+++ mrcnn_tf2/runtime/run.py.patched      2022-07-07 16:01:27.167354000 -0700
@@ -112,11 +112,9 @@
         logging.info('XLA is activated')

     if params.amp:
-        policy = tf.keras.mixed_precision.experimental.Policy("mixed_float16", loss_scale="dynamic")
-        tf.keras.mixed_precision.experimental.set_policy(policy)
+        tf.keras.mixed_precision.set_global_policy("mixed_float16")
         logging.info('AMP is activated')

-
 def create_model(params):
     model = MaskRCNN(
         params=params,
EOF
```

4. Build the container image
```bash
nvidia-docker build -t nvidia_mrcnn_tf2 .
```

5. Benchmark model training
```bash
# Start an interactive session in the NGC container
# Use bind mounts to retain data between runs
docker run --gpus all -it --rm \
        --shm-size=2g \
        --ulimit memlock=-1 \
        --ulimit stack=67108864 \
        -v /tmp/mask-rcnn/data:/data \
        -v /tmp/mask-rcnn/weights:/weights \
        nvidia_mrcnn_tf2

# Note: skip this step if you already have the preprocessed data
# Download and preprocess the dataset (approximately 25GB)
cd /workspace/mrcnn_tf2/dataset
bash download_and_preprocess_coco.sh /data

# Note: skip this step if you already have the preprocessed data
# Download the pre-trained ResNet-50 weights.
python scripts/download_weights.py --save_dir=/weights

# Start training on 2 GPUs
cd /workspace/mrcnn_tf2
# Optional: if you see an error message like this:
#   ImportError: /usr/lib/aarch64-linux-gnu/libgomp.so.1: cannot allocate memory in static TLS block
# ... then set LD_PRELOAD like this:
#   export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1
python scripts/train.py --gpus 2 --batch_size 24
```


### Example: F-LM on Arm64 with 2xA100 GPUs

```bash
# Start an interactive session in the NGC container
# Use bind mounts in $HOME/big_lstm to retain data
docker run --gpus all -it --rm \
        -v $HOME/big_lstm/data:/data \
        -v $HOME/big_lstm/logs:/logs \
        --ipc=host \
        --ulimit memlock=-1 \
        --ulimit stack=67108864 \
        nvcr.io/nvidia/tensorflow:23.01-tf1-py3

# Go to the example directory
cd /workspace/nvidia-examples/big_lstm

# Download the training data
./download_1b_words_data.sh

# Training for up to 180 seconds
python single_lm_train.py \
        --mode=train \
        --logdir=/logs \
        --num_gpus=2 \
        --datadir=/data/1-billion-word-language-modeling-benchmark-r13output \
        --hpconfig run_profiler=False,max_time=180,num_steps=20,num_shards=8,num_layers=2,learning_rate=0.2,max_grad_norm=1,keep_prob=0.9,emb_size=1024,projected_size=1024,state_size=8192,num_sampled=8192,batch_size=512

# Evaulation 
python single_lm_train.py \
        --mode=eval_full \
        --logdir=/logs \
        --num_gpus=2 \
        --datadir=/data/1-billion-word-language-modeling-benchmark-r13output \
        --hpconfig run_profiler=False,num_steps=20,num_shards=8,num_layers=2,learning_rate=0.2,max_grad_norm=1,keep_prob=0.9,emb_size=1024,projected_size=1024,state_size=8192,num_sampled=8192,batch_size=512
```

