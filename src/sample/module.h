#ifndef MODULE_H
#define MODULE_H

#include <string>


namespace SAMPLE_NAMESPACE {

class Module
{
public:
  void set_name(std::string);
  void hello();

private:
  std::string _name;
};


} // namespace SAMPLE_NAMESPACE

#endif /* MODULE_H */
