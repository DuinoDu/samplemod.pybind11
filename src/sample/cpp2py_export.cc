#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <climits>
#include <limits>
#include <unordered_map>

#include "sample.h"

namespace SAMPLE_NAMESPACE {
namespace py = pybind11;
using namespace pybind11::literals;

PYBIND11_MODULE(sample_cpp2py_export, sample_cpp2py_export) {
  sample_cpp2py_export.doc() = "Python interface to sample";

  // Submodule `submodule`
  auto submodule = sample_cpp2py_export.def_submodule("submodule");
  submodule.doc() = "submodule description";
}

} // namespace SAMPLE_NAMESPACE
