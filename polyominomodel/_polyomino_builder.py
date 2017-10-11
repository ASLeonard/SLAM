from collections import defaultdict
from random import choice
from copy import deepcopy

## UTILS ##

def cycleList(inputList,numCycles):
    """Cyclicly rotates list by numCycles times clockwise"""
    return inputList[-numCycles:] + inputList[:-numCycles]

def InteractionMatrix(input_face):
    """Conjugate face according to asymmetric definitions"""
    return  (1-input_face%2)*(input_face-1)+(input_face%2)*(input_face+1) if input_face>0 else input_face

## END UTILS ##

## POLYOMINO BUILDER ##

def PolyominoBuilder(genotype,build_strategy='random',size_threshold=-1):
    """
    Generator which builds the SLAM phenotype for a given genotype

    genotype: the genotype to build
    build_strategy: 'random'/'dfs' (depth first) /'bfs'(breadth first), how new tiles are placed
    size_threshold: max tiles allowed assembly
    
    yields the new tile position and the updated potential tiles
    """
    if size_threshold<=0:
        size_threshold=(len(genotype)**2)/2.
        
    POLYOMINO_GRID=defaultdict(tuple)
    POSSIBLE_GRID=defaultdict(list)
    TILE_TYPES=[genotype[i:i+4] for i in xrange(0, len(genotype), 4)]

    if build_strategy=='dfs' or build_strategy=='bfs':
        possible_grid_order=[]
    else:
        build_strategy='random'

    def placeTile(tType,position,orientation):
        POLYOMINO_GRID[position]=(tType,orientation)
        return position,(tType,orientation)

    def identifyValidNeighbours(position):
        centerType,centerOrientation=POLYOMINO_GRID[position]
        for (x,y,i) in zip([0,1,0,-1],[1,0,-1,0],range(4)):
            identifyValidNeighbour(position,centerType,centerOrientation,(position[0]+x,position[1]+y),i)#

                
    def identifyValidNeighbour(position,centerType,centerOrientation,checkPosition,increment):
        if checkPosition in POLYOMINO_GRID:
            return False
        bindingEdge=cycleList(TILE_TYPES[centerType],centerOrientation)[increment]
        for i,tile in enumerate(TILE_TYPES):
            for cycNum in xrange(4):
                if bindingEdge and cycleList(tile,cycNum)[(increment+2)%4]==InteractionMatrix(bindingEdge):
                    if (i,cycNum) in POSSIBLE_GRID[checkPosition]:
                        continue
                    POSSIBLE_GRID[checkPosition].append((i,cycNum))
                    if build_strategy=='dfs' or build_strategy=='bfs':
                        if checkPosition not in possible_grid_order:
                            possible_grid_order.append(checkPosition)
                        else:
                            if build_strategy=='dfs':
                                possible_grid_order.remove(checkPosition)
                                possible_grid_order.append(checkPosition)

    placement=placeTile(0,(0,0),0)
    identifyValidNeighbours((0,0))
    yield placement,deepcopy(POSSIBLE_GRID)
    while len(POSSIBLE_GRID)>0:
        if build_strategy=='random':
            newPolyominoPosition,newPolyominoDetails=choice([(position, tileDetail) for position, tileDetails in POSSIBLE_GRID.iteritems() for tileDetail in tileDetails])
        elif build_strategy=='dfs':
            newPolyominoPosition,newPolyominoDetails= (possible_grid_order[-1],POSSIBLE_GRID[possible_grid_order.pop()][-1])
        elif build_strategy=='bfs':
            newPolyominoPosition,newPolyominoDetails= (possible_grid_order[0],POSSIBLE_GRID[possible_grid_order.pop(0)][0])

        POSSIBLE_GRID.pop(newPolyominoPosition)
        placement= placeTile(newPolyominoDetails[0],newPolyominoPosition,newPolyominoDetails[1])
        identifyValidNeighbours(newPolyominoPosition)
        if len(POLYOMINO_GRID)>size_threshold:
            return
        else:
            yield placement,deepcopy(POSSIBLE_GRID)

## END POLYOMINO BUILDER ##
