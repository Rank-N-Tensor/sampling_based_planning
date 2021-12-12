id1 = []
id2 = []
edge = open("edges.csv", "r")
for x in edge:  # this for loop takes in to account nodes and their parents
    x = str(x)
    if x[0] is not "#":
        le = x.split(",")
        id1.append(int(le[1]))
        id2.append(int(le[0]))
parent_dict = {}  # this is a dictionary that encapsulates the relation between nodes
for i in range(len(id1)):
    parent_dict[id1[i]] = id2[i]
goal = id1[len(id1) - 1]
start = id2[0]
path = []
i = parent_dict[goal]
path.append(goal)
path.append(i)
j = None
while (
    j is not start
):  # this loop searches for the parent  of the node and adds it to the path list
    j = parent_dict[i]
    i = j
    path.append(j)
path.reverse()
path_file = open(
    "RRT_Path_project.csv", "w"
)  # the following code generates the csv file
path_file.write(str(path)[1 : len(str(path)) - 1])
