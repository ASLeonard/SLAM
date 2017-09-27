#include "tile_analysis.hpp"

extern "C" int Graph_Assembly_Outcome(int size, int *genome) {
  std::vector<int> genotype(size);
  for(int n=0;n<size; ++n) {
    genotype[n]=genome[n];
  }
  return Get_Phenotype_Fitness(genotype,-1,false);
}
