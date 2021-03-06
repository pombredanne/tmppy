#!/bin/bash -x

set -e

# This only exists in OS X, but it doesn't cause issues in Linux (the dir doesn't exist, so it's
# ignored).
export PATH="/usr/local/opt/coreutils/libexec/gnubin:$PATH"

case $COMPILER in
gcc-4.9)
    export CC=gcc-4.9
    export CXX=g++-4.9
    ;;
    
gcc-5)
    export CC=gcc-5
    export CXX=g++-5
    ;;
    
gcc-6)
    export CC=gcc-6
    export CXX=g++-6
    ;;
    
gcc-7)
    export CC=gcc-7
    export CXX=g++-7
    ;;

clang-3.5)
    export CC=clang-3.5
    export CXX=clang++-3.5
    ;;

clang-3.6)
    export CC=clang-3.6
    export CXX=clang++-3.6
    ;;

clang-3.7)
    export CC=clang-3.7
    export CXX=clang++-3.7
    ;;

clang-3.8)
    export CC=clang-3.8
    export CXX=clang++-3.8
    ;;

clang-3.9)
    export CC=clang-3.9
    export CXX=clang++-3.9
    ;;

clang-4.0)
    case "$OS" in
    linux)
        export CC=clang-4.0
        export CXX=clang++-4.0
        ;;
    osx)
        export CC=/usr/local/opt/llvm/bin/clang-4.0
        export CXX=/usr/local/opt/llvm/bin/clang++
        ;;
    *) echo "Error: unexpected OS: $OS"; exit 1 ;;
    esac
    ;;

clang-default)
    export CC=clang
    export CXX=clang++
    ;;

*)
    echo "Unrecognized value of COMPILER: $COMPILER"
    exit 1
esac

run_make() {
  make -j$N_JOBS
}

echo CXX version: $($CXX --version)
echo C++ Standard library location: $(echo '#include <vector>' | $CXX -x c++ -E - | grep 'vector\"' | awk '{print $3}' | sed 's@/vector@@;s@\"@@g' | head -n 1)
echo Normalized C++ Standard library location: $(readlink -f $(echo '#include <vector>' | $CXX -x c++ -E - | grep 'vector\"' | awk '{print $3}' | sed 's@/vector@@;s@\"@@g' | head -n 1))

case "$1" in
DebugPlain)           CMAKE_ARGS=(-DCMAKE_BUILD_TYPE=Debug   -DCMAKE_CXX_FLAGS="$STLARG -Werror -pedantic -D_GLIBCXX_DEBUG -O2") ;;
ReleasePlain)         CMAKE_ARGS=(-DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS="$STLARG -Werror -pedantic") ;;
*) echo "Error: you need to specify one of the supported postsubmit modes (see postsubmit.sh)."; exit 1 ;;
esac

SOURCES_PATH="$PWD"

# This is not needed on Travis CI, but it's sometimes needed when running postsubmit.sh locally, to avoid "import
# file mismatch" errors.
rm -rf */tests/__pycache__/ */tests/*.pyc */tests/*/__pycache__/ */tests/*/*.pyc

rm -rf build
mkdir build
cd build
cmake .. "${CMAKE_ARGS[@]}"
echo
echo "Content of CMakeFiles/CMakeError.log:"
if [ -f "CMakeFiles/CMakeError.log" ]
then
  cat CMakeFiles/CMakeError.log
fi
echo
run_make

cd _py2tmp/tests
run_make
# We specify the path explicitly because old versions of pytest (e.g. the one in Ubuntu 14.04)
# don't support the testpaths setting in pytest.ini, so they will ignore it and they would
# otherwise run no tests.
py.test -n auto -r a "$SOURCES_PATH"/_py2tmp/tests
cd ../../

make install
