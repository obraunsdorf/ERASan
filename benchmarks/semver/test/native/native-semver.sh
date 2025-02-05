#!/bin/bash
TARGETTRIPLE=$(uname -m)-unknown-linux-gnu

# immediately stop building if error occurs
set -e

# Make sure that you set the environmetal settings by ERASan/env/env.sh
export TEST=$PWD
export BINARY_DIR=$TEST/../../build/semver
LIBRARY_DIR="$BUILD_DIR/rust/build/$TARGETTRIPLE/stage1/lib/rustlib/$TARGETTRIPLE/lib"
RLIBS=$(find $LIBRARY_DIR -name "*.rlib")
cp $TEST/../total.ll $TEST

llvm-as total.ll -o total.bc
llc -filetype=obj total.bc -o total.o
HASH=$(basename $(find $LIBRARY_DIR -name "libstd-*.rlib" | head -n 1) | sed 's/libstd-\(.*\)\.rlib/\1/')
clang total.o -o native -L$LIBRARY_DIR -lstd-$HASH -lpthread -ldl -lm -lssl -lcrypto $RLIBS $RLIBS
cp native $BINARY_DIR
cd $BINARY_DIR
./native --bench