# CSCI 561, HW1, FALL 2020
# Author: Wentao Zhou
# The project would implement BFS, UCS, A* algorithm to guide an agent
# to find the shortest path from the given input file.
import time
def main():
    start = time.time()
    f = open("input34.txt", "r")
    lines = f.readlines()
    dic = {
        '1': [1, 0, 0],
        '2': [-1, 0, 0],
        '3': [0, 1, 0],
        '4': [0, -1, 0],
        '5': [0, 0, 1],
        '6': [0, 0, -1],
        '7': [1, 1, 0],
        '8': [1, -1, 0],
        '9': [-1, 1, 0],
        '10': [-1, -1, 0],
        '11': [1, 0, 1],
        '12': [1, 0, -1],
        '13': [-1, 0, 1],
        '14': [-1, 0, -1],
        '15': [0, 1, 1],
        '16': [0, 1, -1],
        '17': [0, -1, 1],
        '18': [0, -1, -1]
        }
    dic_act = {}
    # map each spots to its actions
    for i in range(5, 5+int(lines[4].strip())):
        lists = lines[i].strip().split()
        dic_act[str([int(lists[0]), int(lists[1]), int(lists[2])])] = lists[3:]
    line = lines[2].strip().split()
    entrance = [int(line[0]), int(line[1]), int(line[2])]
    line = lines[3].strip().split()
    ex = [int(line[0]), int(line[1]), int(line[2])]
    if (lines[0] == "BFS\n"):
        predecessor = BFS(lines,dic,dic_act,entrance,ex)
        outputBFS(predecessor,entrance,ex)
    elif(lines[0] == "UCS\n"):
        predecessor = UCS(lines, dic, dic_act, entrance, ex)
    elif(lines[0] == "A*\n"):
        A(lines, dic, dic_act,entrance, ex)
    print(time.time() - start)

# print out the result of BFS algorithm
def outputBFS(predecessor,entrance,ex):
    path = []
    node = ex
    path.append(node)
    output = ""
    outf = open("output.txt", "w")
    if (predecessor == None):
        outf.write("FAIL")
        return
    while(predecessor[str(node)] != None):
        path.insert(0, predecessor[str(node)])
        node = str(predecessor[str(node)])
    outf.write(str(len(path)-1))
    outf.write("\n")
    outf.write(str(len(path)))
    outf.write("\n")
    outf.write(str(entrance[0]) + " " + str(entrance[1]) + " " + str(entrance[2]) + " 0\n")
    for i in range(1, len(path)):
        outf.write(str(path[i][0]) + " " + str(path[i][1]) + " " + str(path[i][2]) + " 1")
        if (i != len(path)-1):
            outf.write("\n")
    

# implement BFS algorithm
def BFS(lines, dic, dic_act,entrance,ex):
    visited = set() #visited
    line = entrance
    queue = []
    queue.append([int(line[:3][0]),int(line[:3][1]),int(line[:3][2])]) # put entrance in queue
    predecessor = {str([int(line[:3][0]),int(line[:3][1]),int(line[:3][2])]): None} # key: current node, value: predecessor
    while queue:
        s = queue.pop(0)
        t = str(s)
        if t not in visited:
            visited.add(t)
            if (t in dic_act.keys()):
                line = dic_act[t]
                for i in range(0, len(line)): # number of actions
                    temp = s.copy()
                    temp[0] += dic[line[i]][0]
                    temp[1] += dic[line[i]][1]
                    temp[2] += dic[line[i]][2] # get the next available positions from the list of actions
                    t = str(temp)
                    if (t not in predecessor.keys()):
                        predecessor[t] = s # to find the path, connect current position to its predecessor
                    if (temp == ex):
                        return predecessor
                    if (t not in visited):
                        queue.append(temp)
    return None

# implement USC algorithm
def UCS(lines, dic, dic_act, entrance, ex):
    visited = set() #visited
    line = entrance
    queue = []
    queue.append([int(line[:3][0]),int(line[:3][1]),int(line[:3][2])])
    predecessor = {str([int(line[:3][0]),int(line[:3][1]),int(line[:3][2])]): None} # key: current node, value: predecessor
    dic_cost = {str([int(line[:3][0]),int(line[:3][1]),int(line[:3][2])]): 0} # map each position to its 
    flag = False
    while queue:
        s = queue.pop(0)
        if (s == ex):
            break;
        st = str(s)
        if st not in visited:
            visited.add(st)
            if st in dic_act.keys():
                line = dic_act[st]
                for i in range(0, len(line)):
                    temp = s.copy()
                    if (int(line[i]) <= 6):
                        cost = 10 + dic_cost[st] # get the cost of path
                    else:
                        cost = 14 + dic_cost[st]
                    for k in range(3):
                        temp[k] += dic[line[i]][k]
                    t = str(temp)
                    if (t not in dic_cost.keys()):
                        dic_cost[t] = cost
                    if (t not in predecessor.keys()):
                        predecessor[t] = s
                    if (t not in visited):
                        index = -1
                        for i in range(0, len(queue)):
                            if (dic_cost[t] < dic_cost[str(queue[i])]):
                                index = i
                                break;
                        if (index != -1):
                            queue.insert(index, temp)
                        else:
                            queue.append(temp)
    # I've found the shortest path, now output
    path = []
    node = ex
    path.append(node)
    cost = 0
    outf = open("output.txt", "w")
    if (str(node) not in predecessor.keys()):
        outf.write("FAIL")
        return
    while(predecessor[str(node)] != None):
        path.insert(0, predecessor[str(node)])
        node = str(predecessor[str(node)])
    outf.write(str(dic_cost[str(ex)]))
    outf.write("\n")
    outf.write(str(len(path)))
    outf.write("\n")
    outf.write(str(entrance[0]) + " " + str(entrance[1]) + " " + str(entrance[2]) + " 0\n")
    for i in range(1, len(path)):
        outf.write(str(path[i][0]) + " " + str(path[i][1]) + " " + str(path[i][2]) + " " + str(dic_cost[str(path[i])] - cost))
        if (i != len(path)-1):
            outf.write("\n")
        cost = dic_cost[str(path[i])]

    

# implment A* algorithm         
def A(lines, dic, dic_act, entrance, ex):
    visited = set() #visited
    line = entrance
    queue = []
    queue.append([int(line[:3][0]),int(line[:3][1]),int(line[:3][2])])
    predecessor = {str([int(line[:3][0]),int(line[:3][1]),int(line[:3][2])]): None} # key: current node, value: predecessor
    dic_cost = {str([int(line[:3][0]),int(line[:3][1]),int(line[:3][2])]): 0}
    dic_heu = {str([int(line[:3][0]),int(line[:3][1]),int(line[:3][2])]): 10}
    flag = False
    while queue:
        s = queue.pop(0)
        if (s == ex):
            break
        st = str(s)
        if st not in visited:
            visited.add(st)
            if st in dic_act.keys():
                line = dic_act[st]
                for i in range(0, len(line)):
                    temp = s.copy()
                    if (int(line[i]) <= 6):
                        cost = 10 + dic_cost[st]
                    else:
                        cost = 14 + dic_cost[st]
                    for k in range(3):
                        temp[k] += dic[line[i]][k]
                    t = str(temp)
                    if (t not in dic_cost.keys()):
                        dic_cost[t] = cost
                    if (t not in predecessor.keys()):
                        predecessor[t] = s
                    if (t not in dic_heu.keys()):
                        if (temp != ex):
                            dic_heu[t] = cost + 10 # 10 is heuristic value
                        else:
                            dic_heu[t] = cost
                    if (t not in visited):
                        index = -1
                        for i in range(0, len(queue)):
                            if (dic_heu[t] < dic_heu[str(queue[i])]):
                                index = i
                                break;
                        if (index != -1):
                            queue.insert(index, temp)
                        else:
                            queue.append(temp)
            
    path = []
    node = ex
    path.append(node)
    cost = 0
    outf = open("output.txt", "w")
    if (str(node) not in predecessor.keys()):
        outf.write("FAIL")
        return 
    while(predecessor[str(node)] != None):
        path.insert(0, predecessor[str(node)])
        node = str(predecessor[str(node)])
    outf.write(str(dic_cost[str(ex)]))
    outf.write("\n")
    outf.write(str(len(path)))
    outf.write("\n")
    outf.write(str(entrance[0]) + " " + str(entrance[1]) + " " + str(entrance[2]) + " 0\n")
    for i in range(1, len(path)):
        outf.write(str(path[i][0]) + " " + str(path[i][1]) + " " + str(path[i][2]) + " " + str(dic_cost[str(path[i])] - cost))
        if (i != len(path)-1):
            outf.write("\n")
        cost = dic_cost[str(path[i])]
    

main()

