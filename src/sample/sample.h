#ifndef SAMPLE_H
#define SAMPLE_H

#include <string>


namespace SAMPLE_NAMESPACE {

class Sample
{
public:
  void set_name(std::string);
  void print();

private:
  std::string _name;
};


} // namespace SAMPLE_NAMESPACE

#endif /* SAMPLE_H */
