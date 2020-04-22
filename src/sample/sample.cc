#include <iostream>
#include <string>

#include "sample.h"

namespace SAMPLE_NAMESPACE {

void Sample::set_name(std::string name){
  _name = name;
}

void Sample::print(){
  std::cout << _name << std::endl;
}


} // namespace SAMPLE_NAMESPACE
