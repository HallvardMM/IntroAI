"""File for task 3 the goal cell will move as time goes on"""
from Map import Map_Obj
class Node():
    """Class to define nodes"""
    def __init__(self, x=None, y=None, parent=None, distanceToStart=0, heuristic=0,totalCost=0):
        self.x = x
        self.y = y
        self.p = parent
        self.g = distanceToStart
        self.h = heuristic 
        self.f = totalCost

    def __repr__(self):
        """for printing nodes"""
        return "Node(x: "+str(self.x)+" y: "+str(self.y)+" parent: "+str(self.p)+")"

    def __eq__(self, node):
        """For checking if node is the same"""
        return self.x == node.x and self.y == node.y
    
    def __ne__(self, node):
        """For checking if node is different"""
        return self.x != node.x or self.y != node.y



def manhatten(nodepos, goalpos):
    """Returns the heuristics Manhatten distance"""
    return abs(nodepos[0]-goalpos[0])+abs(nodepos[1]-goalpos[1])

def euklid(nodepos, goalpos):  
    """Returns the heuristics Euklid distance"""
    return ((nodepos[0]-goalpos[0])**2+(nodepos[1]-goalpos[1])**2)**0.5

def combinedHeuristic(nodepos, goalpos, manhattenWeight=1, euklidWeight=0): #standard is manhattenWeight
    """Returns the weighted heuristics"""
    if manhattenWeight > 1 or manhattenWeight < 0:
        raise Exception("ManhattenWeight can't be under 0 or over 1")
    elif euklidWeight > 1 or euklidWeight < 0:
        raise Exception("EuklidWieght can't be under 0 or over 1")
    elif manhattenWeight+euklidWeight != 1:
        raise Exception("The sum of weights have to be 1")
    return manhattenWeight*manhatten(nodepos, goalpos) + euklidWeight*euklid(nodepos, goalpos)


def astar(map,heuristics):
    start = Node(map.get_start_pos()[1],map.get_start_pos()[0])
    goal = Node(map.get_goal_pos()[1],map.get_goal_pos()[0])
    openNodes = [start]
    closedNodes = []
    repaint = [] # List made for painting after function has runned
    while openNodes:
        index = 0
        lowestCostNode = openNodes[index] # FIFO queue
        for i in range(0,len(openNodes)):
            if openNodes[i].f < lowestCostNode.f:
                lowestCostNode = openNodes[i]
                index = i
        openNodes.pop(index)
        repaint.append([lowestCostNode.y,lowestCostNode.x])
        closedNodes.append(lowestCostNode)
        map.tick() # Moving goal
        goal = Node(map.get_goal_pos()[1],map.get_goal_pos()[0]) # Goal might have changed position
        if lowestCostNode == goal:
            return [lowestCostNode, repaint]
        for i in range(-1,2): 
            for j in range(-1,2):
                if (i!=0 or j!=0) and map.get_cell_value([lowestCostNode.y+i,lowestCostNode.x+j])!=-1:
                    distance = lowestCostNode.g+map.get_cell_value([lowestCostNode.y+i,lowestCostNode.x+j]) # Have to add cost of tile
                    heuristic = heuristics([lowestCostNode.x+j,lowestCostNode.y+i],[map.get_goal_pos()[1],map.get_goal_pos()[0]],0.5,0.5)
                    childNode = Node(lowestCostNode.x+j,lowestCostNode.y+i,lowestCostNode, distance, heuristic,distance+heuristic) 
                    if childNode not in closedNodes:
                        childInList=False
                        for k in range(0, len(openNodes)):
                            if openNodes[k]==childNode:
                                childInList=True
                                if openNodes[k].g>childNode.g: 
                                    openNodes.pop(k)
                                    openNodes.append(childNode)
                        if not childInList:
                            openNodes.append(childNode)
    return Node()
                            


def backTrack(goalNode,map):
    print(goalNode[0])
    """Paints the path green and checked nodes yellow"""
    node=goalNode[0]
    if node.x == None:
        print("No goal found :(")
    else:
        repaint=goalNode[1]
        for paint in repaint:
            map.replace_map_values([paint[0],paint[1]],7,map.get_end_goal_pos())
        while node != Node(map.get_start_pos()[1],map.get_start_pos()[0]):
            map.replace_map_values([node.y,node.x],5,map.get_end_goal_pos())
            node=node.p
        map.replace_map_values(map.get_start_pos(),6,map.get_end_goal_pos())
        map.show_map()



map5 = Map_Obj(task=5)

map5.show_map()
endNode5 = astar(map5, combinedHeuristic)
backTrack(endNode5, map5)
