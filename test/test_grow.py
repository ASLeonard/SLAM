import matplotlib
matplotlib.use('Agg')

print "Loading module"
import polyominomodel as pm
print "Growing unlabelled"
pm.GrowPoly([1,1,1,1,2,0,0,0],0)
print "Growing labelled"
pm.GrowPoly([1,1,1,1,2,0,0,0],0)
print "Saving gif"
pm.GrowPoly([1,1,1,1,2,0,0,0],0,"Test_Save")
