import polyominomodel as pm
import pytest
    
def test_grow_unlabelled():
    success=True
    try:
        pm.GrowPoly([1,1,1,1,2,0,0,0],0)
    except:
        sucess=False
    assert(success), "failed model"

def test_grow_labelled():
    success=True
    try:
        pm.GrowPoly([1,1,1,1,2,0,0,0],1)
    except:
        sucess=False
    assert(success), "failed model"

def test_genotype_generator():
    pm.GenerateGenotype(5)

def test_BD_genotype_generator():
    pm.GenerateBDGenotype(2)

#def test_analysis():
#    print "cdll loading from ",pm._polyomino_animator.abspath
#    assert(type(pm.GraphAssemblyOutcome(pm.GenerateGenotype(3)))==int), "Did not load CDLL properly"
    

