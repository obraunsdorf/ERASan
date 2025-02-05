#!/bin/bash
TARGETTRIPLE=$(uname -m)-unknown-linux-gnu

# immediately stop building if error occurs
set -e

# Make sure that you set the environmetal settings by ERASan/env/env.sh

# Also make sure that you set the LLVM pass to ERASan.cpp by using ERASan/build/erasan.sh before conducting benchmark test
#
# cd ERASan/build
# ./erasan.sh
#

export TEST=$PWD
export BINARY_DIR=$TEST/../../build/semver
LIBRARY_DIR="$BUILD_DIR/rust/build/$TARGETTRIPLE/stage1/lib/rustlib/$TARGETTRIPLE/lib"
RLIBS=$(find $LIBRARY_DIR -name "*.rlib")
cp $TEST/../total.ll $TEST

erasan total.ll -erasan
opt --asan-module -S erasanOptAnalysis.ll -o erasanOptAnalysis.ll
llvm-as erasanOptAnalysis.ll -o erasanOptAnalysis.bc
llc -filetype=obj erasanOptAnalysis.bc -o erasanOptAnalysis.o
HASH=$(basename $(find $LIBRARY_DIR -name "libstd-*.rlib" | head -n 1) | sed 's/libstd-\(.*\)\.rlib/\1/')
clang erasanOptAnalysis.o -o erasan -L$LIBRARY_DIR -lstd-$HASH -lpthread -ldl -lm -fsanitize=address -lssl -lcrypto $RLIBS $RLIBS
cp erasan $BINARY_DIR
cd $BINARY_DIR
./erasan --bench

