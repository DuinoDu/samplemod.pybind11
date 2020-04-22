# Minimum CMake required
cmake_minimum_required(VERSION 3.1)
project(libsample C CXX)
set(CMAKE_VERBOSE_MAKEFILE ON)

## set args
#option(XXX_ARGS "Description" OFF)

# Set C++11 as standard for the whole project
set(CMAKE_CXX_STANDARD 11)

set(_ROOT ${PROJECT_SOURCE_DIR}/src/sample)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wnon-virtual-dtor")
set(CMAKE_C_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -O0")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -O0")

if(NOT SAMPLE_NAMESPACE)
    set(SAMPLE_NAMESPACE "sample")
endif()

# Build the libraries with -fPIC
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

file(GLOB_RECURSE __tmp_srcs "${_ROOT}/*.h" "${_ROOT}/*.cc")
list(REMOVE_ITEM __tmp_srcs "${_ROOT}/cpp2py_export.cc")
list(APPEND _SRCS ${__tmp_srcs})
add_library(sample ${_SRCS})

if("${PY_EXT_SUFFIX}" STREQUAL "")
  set(PY_EXT_SUFFIX ".so")
endif()

add_library(sample_cpp2py_export MODULE "${_ROOT}/cpp2py_export.cc")
set_target_properties(sample_cpp2py_export PROPERTIES PREFIX "")
set_target_properties(sample_cpp2py_export
                      PROPERTIES COMPILE_FLAGS "-fvisibility=hidden")
set_target_properties(sample_cpp2py_export PROPERTIES SUFFIX ${PY_EXT_SUFFIX})
set_target_properties(sample_cpp2py_export
                      PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})
target_include_directories(sample_cpp2py_export PRIVATE
                           $<BUILD_INTERFACE:${_ROOT}>
                           $<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}>
                           $<INSTALL_INTERFACE:include>
                           ${PYTHON_INCLUDE_DIR})

# pybind11 is a header only lib
find_package(pybind11 2.2)
if(pybind11_FOUND)
  target_include_directories(sample_cpp2py_export PUBLIC
    ${pybind11_INCLUDE_DIRS})
else()
  if(EXISTS ${_ROOT}/../../third_party/pybind11/include/pybind11/pybind11.h)
    target_include_directories(sample_cpp2py_export PUBLIC
      ${_ROOT}/../../third_party/pybind11/include)
  else()
    message(FATAL_ERROR "cannot find pybind")
  endif()
endif()

# Assume everything else is like gcc
target_link_libraries(sample_cpp2py_export
                      PRIVATE "-Wl,--whole-archive" $<TARGET_FILE:sample>
                              "-Wl,--no-whole-archive")
set_target_properties(sample_cpp2py_export
                      PROPERTIES LINK_FLAGS "-Wl,--exclude-libs,ALL")
target_link_libraries(sample_cpp2py_export PRIVATE sample)

# Export include directories
set(_INCLUDE_DIRS "${_ROOT}" "${CMAKE_CURRENT_BINARY_DIR}")
get_directory_property(hasParent PARENT_DIRECTORY)
if(hasParent)
  set(_INCLUDE_DIRS ${_INCLUDE_DIRS} PARENT_SCOPE)
endif()

# # ---[ ONNX Interface for Framework Integratin (ONNXIFI)
# add_library(onnxifi INTERFACE)
# target_include_directories(onnxifi INTERFACE
#   $<BUILD_INTERFACE:${_ROOT}>
#   $<INSTALL_INTERFACE:include>)

# install(DIRECTORY ${_ROOT}
#         DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
#         FILES_MATCHING
#         PATTERN "*.h")
# install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/onnx
#         DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
#         FILES_MATCHING
#         PATTERN "*.h")
# 
# install(TARGETS
#   sample 
#   EXPORT ONNXTargets 
#   DESTINATION ${CMAKE_INSTALL_LIBDIR})

# if(ONNX_BUILD_TESTS)
#   include(${ONNX_ROOT}/cmake/unittest.cmake)
# endif()

include(cmake/summary.cmake)
print_summary()
