#include <iostream>
#include <string>

#include "module.h"

namespace SAMPLE_NAMESPACE {

void Module::set_name(std::string name){
  _name = name;
}

void Module::hello(){
  std::cout << _name << std::endl;
}


} // namespace SAMPLE_NAMESPACE
