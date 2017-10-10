from collections import defaultdict
from random import choice
from copy import copy

## UTILS ##

def cycleList(inputList,numCycles):
    return inputList[-numCycles:] + inputList[:-numCycles]

def InteractionMatrix(input_face):
    return  (1-input_face%2)*(input_face-1)+(input_face%2)*(input_face+1) if input_face>0 else input_face

## END UTILS ##

## POLYOMINO BUILDER ##

def PolyominoBuilder(genotype,build_strategy='random'):
    SIZE_LIMIT=len(genotype)**2
    POLYOMINO_GRID=defaultdict(tuple)
    POSSIBLE_GRID=defaultdict(list)
    IMPOSSIBLE_GRID=set()
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
                    if build_strategy=='dfs' or build_strategy=='bfs':
                        if checkPosition not in possible_grid_order:
                            possible_grid_order.append(checkPosition)
                        else:
                            if build_strategy=='dfs':
                                possible_grid_order.remove(checkPosition)
                                possible_grid_order.append(checkPosition)
                            else:
                                pass

    placement=placeTile(0,(0,0),0)
    identifyValidNeighbours((0,0))
    yield placement,copy(POSSIBLE_GRID)
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
        if len(POLYOMINO_GRID)>SIZE_LIMIT:
            return
        else:
            yield placement,copy(POSSIBLE_GRID)

## END POLYOMINO BUILDER ##
