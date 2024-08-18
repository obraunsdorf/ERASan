TARGETTRIPLE=$(uname -m)-unknown-linux-gnu
# #!/bin/sh
export S2HOME=`pwd`/..
export BUILD_DIR=$S2HOME/build
export PATH=$BUILD_DIR/rust/build/$TARGETTRIPLE/llvm/bin:$PATH
export PATH=$BUILD_DIR/rust/build/$TARGETTRIPLE/stage0/bin:$PATH
export PATH=$BUILD_DIR/rust/build/$TARGETTRIPLE/stage1/bin:$PATH
export PATH=$BUILD_DIR/SVF/Release-build/bin:$PATH
export LLVM_CONFIG=$BUILD_DIR/rust/build/$TARGETTRIPLE/llvm/bin/llvm-config
export CARGO=$BUILD_DIR/rust/build/$TARGETTRIPLE/stage0/bin/cargo

export LD_LIBRARY_PATH=$BUILD_DIR/rust/build/$TARGETTRIPLE/stage1/lib/rustlib/$TARGETTRIPLE/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$BUILD_DIR/rust/build/$TARGETTRIPLE/llvm/lib/clang/14.0.6/lib/linux:$LD_LIBRARY_PATH
