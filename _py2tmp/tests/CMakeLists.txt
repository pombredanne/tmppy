
file(GENERATE OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/py2tmp_test_config.py"
     CONTENT "
CXX='${CMAKE_CXX_COMPILER}'
CXX_COMPILER_NAME='${CMAKE_CXX_COMPILER_ID}'
CXX_COMPILER_VERSION='${CMAKE_CXX_COMPILER_VERSION}'
ADDITIONAL_LINKER_FLAGS='${CMAKE_EXE_LINKER_FLAGS}'
CMAKE_BUILD_TYPE='${CMAKE_BUILD_TYPE}'
MPYL_INCLUDE_DIR='${CMAKE_CURRENT_SOURCE_DIR}/../../include'
")

file(GENERATE OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/pytest.ini"
     CONTENT "
[pytest]
testpaths = \"${CMAKE_CURRENT_SOURCE_DIR}\"
addopts = -r a --tb=short
")

file(GENERATE OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/conftest.py"
     CONTENT "
")

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

set(INSTALL_INCLUDE_DIR include/fruit CACHE PATH "Installation directory for headers")

set(TMPPY_VERSION "0.1.3")

install(DIRECTORY include/fruit/
  DESTINATION "${INSTALL_INCLUDE_DIR}"
  FILES_MATCHING PATTERN "*.h")

set(CPACK_PACKAGE_NAME "TMPPy")
set(CPACK_PACKAGE_VENDOR "Marco Poletti")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "TMPPy - A Subset Of Python That Can Be Compiled to C++ Meta-Functions")
string(REGEX REPLACE "([^.]*)\\.([^.]*)\\.([^.]*)" "\\1" CPACK_PACKAGE_VERSION_MAJOR "${TMPPY_VERSION}")
string(REGEX REPLACE "([^.]*)\\.([^.]*)\\.([^.]*)" "\\2" CPACK_PACKAGE_VERSION_MINOR "${TMPPY_VERSION}")
string(REGEX REPLACE "([^.]*)\\.([^.]*)\\.([^.]*)" "\\3" CPACK_PACKAGE_VERSION_PATCH "${TMPPY_VERSION}")
set(CPACK_PACKAGE_VERSION "${TMPPY_VERSION}")
set(CPACK_PACKAGE_INSTALL_DIRECTORY "TMPPy")
