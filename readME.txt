Implementation of the RRT algorithm. The challenge is to generate samples at the goal config. This is accomplished by using weighted probabilites in the form of a 
function. the problem is split into two seprate scripts. one of the programs generates the Tree and the other generates the path. The RRT program works by creating using a sampler function
to take weighted samples for a list of all possible samples. subsequently , it uses a function to find the nearest node based on euclidean distance. then, it performs a collision check 
and if said node passes the collision check , its added to the tree with an edge connecting the two aforementioned nodes. this process is continued until an edge to the goal node is created

The planner program does a simple search from the goal node. that is, it finds its parent and continues this process until the start node is reached. these nodes are added to a list which
is then reversed to generate the path file.

