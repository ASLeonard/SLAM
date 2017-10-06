#!/usr/bin/env python

import ctypes
import sys
import os
import matplotlib.pyplot as plt

from collections import defaultdict
from copy import copy
from random import choice
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation,ImageMagickWriter

## UTILS ##

def cycleList(inputList,numCycles):
    return inputList[-numCycles:] + inputList[:-numCycles]

## WRAPPER SECTION ##
Poly_Lib='init'
try:
    abspath=os.path.abspath(os.path.dirname(__file__))
    Poly_Lib=ctypes.cdll.LoadLibrary('{}/CLAM.so'.format(abspath))
    Poly_Lib.Graph_Assembly_Outcome.restype=ctypes.c_int
    Poly_Lib.Graph_Assembly_Outcome.argtype=[ctypes.c_int,ctypes.POINTER(ctypes.c_int)]
except:
    Poly_Lib='Failed'

def GraphAssemblyOutcome(genotype):
    genotype_Pointer=(ctypes.c_int*len(genotype))(*genotype)
    return Poly_Lib.Graph_Assembly_Outcome(len(genotype),genotype_Pointer)

def TimeIt(tops):
    for top in tops:
        Graph_Assembly_Outcome(top)

## POLYOMINO BUILDER ##

def InteractionMatrix(input_face):
    return  (1-input_face%2)*(input_face-1)+(input_face%2)*(input_face+1) if input_face>0 else input_face

def PolyominoBuilder(genotype):
    SIZE_LIMIT=len(genotype)**2
    POLYOMINO_GRID=defaultdict(tuple)
    POSSIBLE_GRID=defaultdict(list)
    IMPOSSIBLE_GRID=set()
    TILE_TYPES=[genotype[i:i+4] for i in xrange(0, len(genotype), 4)]

    def placeTile(tType,position,orientation):
        POLYOMINO_GRID[position]=(tType,orientation)
        return position,(tType,orientation)

    def identifyValidNeighbours(position):
        centerType,centerOrientation=POLYOMINO_GRID[position]
        identifyValidNeighbour(position,centerType,centerOrientation,(position[0],position[1]+1),0)#Check Top
        identifyValidNeighbour(position,centerType,centerOrientation,(position[0]+1,position[1]),1)#Check Right
        identifyValidNeighbour(position,centerType,centerOrientation,(position[0],position[1]-1),2)#Check Bottom
        identifyValidNeighbour(position,centerType,centerOrientation,(position[0]-1,position[1]),3)#Check Left
                
    def identifyValidNeighbour(position,centerType,centerOrientation,checkPosition,increment):
        if checkPosition in POLYOMINO_GRID:
            return False
        bindingEdge=cycleList(TILE_TYPES[centerType],centerOrientation)[increment]
        oppositeBindingEdgeIndex=(increment+2)%4
        for i,tile in enumerate(TILE_TYPES):
            for cycNum in xrange(4):
                if bindingEdge!=0 and cycleList(tile,cycNum)[oppositeBindingEdgeIndex]==InteractionMatrix(bindingEdge):
                    POSSIBLE_GRID[checkPosition].append((i,cycNum))

    placement=placeTile(0,(0,0),0)
    identifyValidNeighbours((0,0))
    yield placement,copy(POSSIBLE_GRID)
    while len(POSSIBLE_GRID)>0:
        newPolyominoPosition,newPolyominoDetails=choice([(position, tileDetail) for position, tileDetails in POSSIBLE_GRID.iteritems() for tileDetail in tileDetails])
        POSSIBLE_GRID.pop(newPolyominoPosition)
        placement= placeTile(newPolyominoDetails[0],newPolyominoPosition,newPolyominoDetails[1])
        identifyValidNeighbours(newPolyominoPosition)
        if len(POLYOMINO_GRID)>SIZE_LIMIT:
            return
        else:
            yield placement,copy(POSSIBLE_GRID)
        
## ANIMATION SECTION ##
ERROR_CODES={0:'Steric Mismatch',-1:'Disjointed Genotype',-2:'Double Branching Point',-3:'Invalid SIFE',-4:'Disjointed Branching Point',-5:'Infinite Internal Loop',-6:'Internal Branching Point',-7:'Multiple Internal Loops',-8:'Single Tile Branching Point',-9:'External Infinite Loop',-10:'Uncuttable Infinite Loop',-11:'Irreducible Loops',-12:'No Loops',-13:'Unbounded Loop Growth'}

def LabelTile(ax,tile,position,rotation):
    ax.text(.475+position[0],.85+position[1],str(tile[rotation]), verticalalignment='center', horizontalalignment='center',rotation=rotation*90)
    ax.text(.475+position[0],.1+position[1],str(tile[(2+rotation)%4]), verticalalignment='center', horizontalalignment='center',rotation=rotation*-90)
    ax.text(.85+position[0],.475+position[1],str(tile[(3+rotation)%4]), verticalalignment='center', horizontalalignment='center',rotation=rotation*-90)
    ax.text(.1+position[0],.475+position[1],str(tile[(1+rotation)%4]), verticalalignment='center', horizontalalignment='center',rotation=rotation*-90)

def SetTightBounds(ax,data):
    plt.axis([min([i[0][0][0] for i in data])-0.25,max([i[0][0][0] for i in data])+1.25,min([i[0][0][1] for i in data])-0.25,max([i[0][0][1] for i in data])+1.25])
    

def GrowPoly(genotype,tile_labels=True,write_it=False,fps_par=1.25):
    assert(len(genotype)%4==0),  "Genotype length is invalid, each tile must have 4 faces"
    assert(len(genotype)<=40), "Very long genotype, currently not allowed"

    ## c++ ##
    if Poly_Lib!='Failed':
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
    HATCHES=['//','\\','+','O', '.']

    def init():
        pass

    temporary_tiles=[]
    data=list(PolyominoBuilder(genotype))
    def AnimateBuild(i):
        ## FIRST FRAME ##
        if i==0:
            ax.add_patch(Rectangle((0,0),0.95,0.95,fill=True,alpha=1,facecolor=COLORS[0],edgecolor='k',lw=2))
            
            temporary_tiles.append(Rectangle((0,0),0.95,0.95,fill=False,alpha=1,edgecolor='r',lw=2))
            ax.add_patch(temporary_tiles[0])
            ax.text(.475,.475,'SEED',verticalalignment='center',horizontalalignment='center',fontsize=10)
            if tile_labels:
                LabelTile(ax,genotype[:4],(0,0),0)

        ## SECOND FRAME ##
        elif i==1:
            temporary_tiles.pop().remove()
            return
        
        ## THIRD FRAME ##
        elif i==2:
            for key in data[0][1]:
                potential_tiles=[t_type[0] for t_type in data[0][1][key]]
                for j,pt in enumerate(set(potential_tiles)):
                    temporary_tiles.append(Rectangle(key,0.95,0.95,fill=True,alpha=0.25,facecolor=COLORS[pt],edgecolor='k',lw=2,hatch=HATCHES[j%5]))
                    ax.add_patch(temporary_tiles[-1])

        ## LAST FRAMES ##
        elif i>len(data)*2:
            return
        
        ## !!FURTHER FRAMES!! ##
        elif i%2:
            current_tile=data[i/2][0]
            ax.add_patch(Rectangle(current_tile[0],0.95,0.95,fill=True,alpha=1,facecolor=COLORS[current_tile[1][0]],edgecolor='k',lw=2))
            temporary_tiles.append(Rectangle(current_tile[0],0.95,0.95,fill=False,alpha=1,edgecolor='r',lw=2))
            ax.add_patch(temporary_tiles[-1])
            if tile_labels:
                LabelTile(ax,genotype[current_tile[1][0]*4:current_tile[1][0]*4+4],current_tile[0],current_tile[1][1])
            
        elif i%2==0:
            while temporary_tiles:
                temporary_tiles.pop().remove()
            for key in data[i/2-1][1]:
                potential_tiles=[t_type[0] for t_type in data[i/2-1][1][key]]
                for j,pt in enumerate(set(potential_tiles)):
                    temporary_tiles.append(Rectangle(key,0.95,0.95,fill=True,alpha=0.25,facecolor=COLORS[pt],edgecolor='k',lw=2,hatch=HATCHES[j%5]))
                    ax.add_patch(temporary_tiles[-1])   

    
    SetTightBounds(ax,data)
    anim = FuncAnimation(fig, AnimateBuild,init_func=init,frames=len(data)*2+5, interval=200, blit=False,repeat=False)
    plt.tight_layout()
    
    if type(write_it)==str:
        writer = ImageMagickWriter(fps=fps_par)
        print "Writing {}.gif to current directory\nfps set as {}".format(write_it,fps_par)
        anim.save('{}.gif'.format(write_it), writer=writer)
    else:
        plt.show(block=False)
        

