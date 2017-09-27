#include "tile_analysis.hpp"

extern "C" int Graph_Assembly_Outcome(int size, int *genome) {
  //LOAD GENOTYPE
  std::vector<int> genotype(size);
  for(int n=0;n<size; ++n) {
    genotype[n]=genome[n];
  }

  //DO ANALYSIS
  Clean_Genome(genotype,-1);
  
  if(Disjointed_Check(genotype))
    return -1; //Disjointed error
  else {
    int graph_result=Graph_Analysis(genotype);
    if(graph_result<=0)
      return graph_result;
    else {
      int steric_result=Steric_Check(genotype,-1);
      return steric_result>0? steric_result : 0;
    }
  }
}
