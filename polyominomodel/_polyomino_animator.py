#!/usr/bin/env python

import ctypes
import os
import matplotlib.pyplot as plt



from random import randint
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation,ImageMagickWriter
from sys import platform

from _polyomino_builder import PolyominoBuilder




    
## WRAPPER SECTION ##

Poly_Lib='unloaded'
try:
    abspath=os.path.abspath(os.path.dirname(__file__))
    if platform.startswith('linux'):
        Poly_Lib=ctypes.cdll.LoadLibrary('{}/CLAM.so'.format(abspath))
    elif platform.startswith('darwin'):
        Poly_Lib=ctypes.cdll.LoadLibrary('{}/CLAM.dylib'.format(abspath))
    Poly_Lib.Graph_Assembly_Outcome.restype=ctypes.c_int
    Poly_Lib.Graph_Assembly_Outcome.argtype=[ctypes.c_int,ctypes.POINTER(ctypes.c_int)]
except:
    Poly_Lib=False

def GraphAssemblyOutcome(genotype):
    if Poly_Lib:
        genotype_Pointer=(ctypes.c_int*len(genotype))(*genotype)
        return Poly_Lib.Graph_Assembly_Outcome(len(genotype),genotype_Pointer)
    else:
        return "Unable to load cdll properly"


def get_lib():
    return Poly_Lib

## GENETYPE HELPERS ##

def GenerateGenotype(genome_length,colours=-1):
    if colours==-1:
        colours=genome_length*4+1
    return [randint(0,colours) for i in xrange(genome_length*4)]

def GenerateBDGenotype(genome_length,colours=-1,max_attempts=1000):
    if colours==-1:
        colours=genome_length*4+1
    trial_genotype=[randint(0,colours) for i in xrange(genome_length*4)]
    attempts=0
    while GraphAssemblyOutcome(trial_genotype)<=0:
         trial_genotype=[randint(0,colours) for i in xrange(genome_length*4)]
         attempts+=1
         if attempts>max_attempts:
             return [0,0,0,0]
    return trial_genotype


        
## ANIMATION SECTION ##
ERROR_CODES={0:'Steric Mismatch',-1:'Disjointed Genotype',-2:'Double Branching Point',-3:'Invalid SIFE',-4:'Disjointed Branching Point',-5:'Infinite Internal Loop',-6:'Internal Branching Point',-7:'Multiple Internal Loops',-8:'Single Tile Branching Point',-9:'External Infinite Loop',-10:'Uncuttable Infinite Loop',-11:'Irreducible Loops',-12:'No Loops',-13:'Unbounded Loop Growth'}

def LabelTile(ax,tile,position,rotation):
    for (x,y,i) in zip([0.475,0.1,0.475,0.85],[0.85,0.475,0.1,0.475],range(4)):
        ax.text(x+position[0],y+position[1],str(tile[(i+rotation)%4]), verticalalignment='center', horizontalalignment='center',rotation=-90*rotation)

def SetTightBounds(ax,data):
    plt.axis([min([i[0][0][0] for i in data])-0.25,max([i[0][0][0] for i in data])+1.25,min([i[0][0][1] for i in data])-0.25,max([i[0][0][1] for i in data])+1.25])
    

def GrowPoly(genotype,tile_labels=True,growing=False,write_it=False,fps_par=1.25):
    assert(len(genotype)%4==0),  "Genotype length is invalid, each tile must have 4 faces"
    assert(len(genotype)<=40), "Very long genotype, currently not allowed"

    ## c++ ##
    if Poly_Lib:
        assembly_outcome=GraphAssemblyOutcome(genotype);
        if assembly_outcome<=0:
            print '**Bad phenotype**\nRejection due to: {}'.format(ERROR_CODES[assembly_outcome])
    else:
        print "No outcome information available"
    ## end c++ ##

    fig = plt.figure(figsize=(10,10))
    plt.axis('off')
    ax = plt.gca()
    ax.set_aspect(1)
    COLORS=['royalblue','darkgreen','firebrick','chocolate','orchid','goldenrod','navy','olive','lime','teal']
    HATCHES=['//','\\','+','O','.','*','o']

    def init():
        pass

    temporary_tiles=[]
    data=list(PolyominoBuilder(genotype))
    def AnimateBuild(i):
        if i and growing:
            SetTightBounds(ax,data[:i])
        
        ## FIRST FRAME ##
        if i==0:
            ax.add_patch(Rectangle((0,0),0.95,0.95,fill=True,alpha=1,facecolor=COLORS[0],edgecolor='k',lw=2))
            temporary_tiles.append(Rectangle((0,0),0.95,0.95,fill=False,alpha=1,edgecolor='r',lw=2))
            ax.add_patch(temporary_tiles[0])
            ax.text(.475,.475,'SEED',verticalalignment='center',horizontalalignment='center',fontsize=10)
            if tile_labels:
                LabelTile(ax,genotype[:4],(0,0),0)
            if growing:
                plt.axis([-0.25,1.25,-0.25,+1.25])

        ## SECOND FRAME ##
        elif i==1:
            temporary_tiles.pop().remove()
        
        ## THIRD FRAME ##
        elif i==2:
            for key in data[0][1]:
                potential_tiles=[t_type[0] for t_type in data[0][1][key]]
                for j,pt in enumerate(set(potential_tiles)):
                    temporary_tiles.append(Rectangle(key,0.95,0.95,fill=True,alpha=0.25,facecolor=COLORS[pt],edgecolor='k',lw=2,hatch=HATCHES[j%7]))
                    ax.add_patch(temporary_tiles[-1])

        ## LAST FRAMES ##
        elif i>len(data)*2:
            pass
        
        ## !!FURTHER FRAMES!! ##
        elif i%2:
            current_tile=data[i/2][0]
            ax.add_patch(Rectangle(current_tile[0],0.95,0.95,fill=True,alpha=1,facecolor=COLORS[current_tile[1][0]],edgecolor='k',lw=2))
            temporary_tiles.append(Rectangle(current_tile[0],0.95,0.95,fill=False,alpha=1,edgecolor='r',lw=2))
            ax.add_patch(temporary_tiles[-1])
            if tile_labels:
                LabelTile(ax,genotype[current_tile[1][0]*4:current_tile[1][0]*4+4],current_tile[0],current_tile[1][1])
            
        else:
            while temporary_tiles:
                temporary_tiles.pop().remove()
            for key in data[i/2-1][1]:
                potential_tiles=[t_type[0] for t_type in data[i/2-1][1][key]]
                for j,pt in enumerate(set(potential_tiles)):
                    temporary_tiles.append(Rectangle(key,0.95,0.95,fill=True,alpha=0.25,facecolor=COLORS[pt],edgecolor='k',lw=2,hatch=HATCHES[j%7]))
                    ax.add_patch(temporary_tiles[-1])   

    if not growing:
        SetTightBounds(ax,data)
        
    anim = FuncAnimation(fig, AnimateBuild,init_func=init,frames=len(data)*2+5, interval=200, blit=False,repeat=False)
    plt.tight_layout()
    #fig.set_tight_layout(True)
    
    if type(write_it)==str:
        writer = ImageMagickWriter(fps=fps_par)
        print "Writing {}.gif to current directory\nfps set as {}".format(write_it,fps_par)
        anim.save('{}.gif'.format(write_it), writer=writer)
    else:
        #pass
        plt.show(block=False)
        

