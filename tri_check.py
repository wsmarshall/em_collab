from pysat.solvers import *
from itertools import *
from sys import argv

N = None

#want to encode 2 types of variables, each type has 3 subscripts 
#so we need computable bijection from N4 to N. 
#we just use original composed multiple times

def encode(pos1, pos2):
    return pos1*N + pos2 + 1

def decode(val):
    val -= 1
    return (val // N, val % N)

def enc4(p1,p2,p3,p4):
    #needs to be this order since second position is implicitly less than n
    return encode(encode(encode(p1,p2),p3),p4)

def dec4(val):
    tup_init = decode(val)
    tup_sec = decode(tup_init[0])
    tup_third = decode(tup_sec[0])
    return (tup_third[0], tup_third[1], tup_sec[1], tup_init[1])

# PySAT solves formulas in conjunctive normal form, i.e., an 
# "and-of-ors". Each time you add a clause, you list out the variables,
# negating them if they are negated in the formula. E.g., if we wanted
# to include the clause (x_1 V x_2 V ~x_3), we would write
# "phi.add_clause([1, 2, -3])

def at_most_one(phi, indices):
    for i,j in combinations(indices, 2):
        phi.add_clause([-i, -j])

def at_least_one(phi, indices):          
    phi.add_clause(list(indices))

def exactly_one(phi, indices):
    at_least_one(phi, indices)
    at_most_one(phi, indices)

    #a_(u,i,v) true iff u's rotation is st positiion i is occupied by vertex v
    #l_(u,v,w) true iff u's rotations is st w comes after v

#compute degree of all vertices
def degree_dic(edges):
    degree = {}
    for x in range(len(edges)):
        val = 0
        for i in range(len(edges[x])):
            if edges[x][i] == True:
                val +=1
        degree.update({x: val})
    return degree

def find_rotation(edges, constraint = ''):
    # the solver starts out with an empty formula, and we add our
    # desired clauses
    deg = degree_dic(edges)
    #print(deg)
    phi = Glucose4()
    #no vertices can occupy a position greater than degree of u
    c1, c2, c3, c4 = [],[], [],[]
    for u in range(N):
        for i in range(deg[u], N):
            for v in range(N):
                # tup = (0,u,i,v)
                # print(tup)
                c1.append(enc4(0,u,i,v))
                phi.add_clause([-enc4(0,u,i,v)])
    # #for all vertices, no position can be occupied by a non neighbor
    # print("c1:")
    # print(c1)
    for u in range(N):
        for v in range(N):
            if not edges[u][v]:
                for i in range(N):
                    c2.append(enc4(0,u,i,v))
                    phi.add_clause([-enc4(0,u,i,v)])
    #for all vertices nonneighbors cannot follow or be followed by anything
    #print("c2")
    #print(c2)
    for u in range(N):
        for v in range(N):
            if not edges[u][v]:
                for w in range(N):
                    c3.append(enc4(1,u,v,w))
                    phi.add_clause([-enc4(1,u,v,w)])
                    c4.append(enc4(1,u,w,v))
                    phi.add_clause([-enc4(1,u,w,v)])

    # print("c3")
    # print(c3)
    # print("c4")
    # print(c4)
    #exactly one constraints 
    # "for any fixed u, only one v can be in position i"
    
    e1, e2, e3, e4 =[],[],[],[]


    for u in range(N):
        for i in range(deg[u]):
            e1.extend([enc4(0,u,i,v) for v in range(N)])
            e1.append("b")
            exactly_one(phi, [enc4(0,u,i,v) for v in range(N)])
    
    for u in range(N):
        for v in range(N):
            if edges[u][v]:
                e2.extend([enc4(0,u,i,v) for i in range(deg[u])])
                e2.append("b")
                exactly_one(phi, [enc4(0,u,i,v) for i in range(deg[u])])

    for u in range(N):
        for v in range(N):
            if edges[u][v]:
                e3.extend([enc4(1,u,v,w) for w in range(N)])
                e3.append("b")
                exactly_one(phi, [enc4(1,u,v,w) for w in range(N)])  

    for u in range(N):
        for w in range(N):
            if edges[u][w]:
                e4.extend([enc4(1,u,v,w) for v in range(N) if edges[u][v]])
                e4.append("b")
                exactly_one(phi, [enc4(1,u,v,w) for v in range(N) if edges[u][v]])               


    # print("e1")
    # print(e1)
    # print("e2")
    # print(e2)
    # print("e3")
    # print(e3)
    # print("e4")
    # print(e4)

    #enforce array implies linked

    for u in range(N):
        for i in range(deg[u]):
            for v in range(N):
                if edges[u][v]:
                    for w in range(N):
                        if edges[u][w]:
                            phi.add_clause([-enc4(0,u,i,v),-enc4(0,u,(i+1)% deg[u],w), enc4(1,u,v,w)])


    #enforce rule delta* (mine)
    for u in range(N):
        for v in range(N):
            for w in range(N): 
                phi.add_clause([-enc4(1,u,v,w), enc4(1,v,w,u) ])

    # #enforce rule delta* (tim's)
    # for u in range(N):
    #     for v in range(N):
    #         for w in range(N): 
    #             phi.add_clause([-enc4(1,u,v,w), enc4(1,v,w,u)])
    #             phi.add_clause([-enc4(1,u,v,w), enc4(1,w,u,v)])

    #enforcing first position for each non constraint vertex
    for u in range(N):
        v = None
        for i in range(N):
            if edges[u][i]:
                v = i
                break
        phi.add_clause([enc4(0,u,0,v)])



    #enforce constraint
    #currently not checking if constraint is valid (ie vertices all exist, connected to first vertex,etc)
    if constraint != '':
        constraint = constraint.split(',')
        rot = constraint[1:]
        #print(rot)
        #test1, test2= [], []
        # for x in range(len(rot)):
        #     #test1.append([(0,constraint[0],x, rot[x])])
        #     phi.add_clause([enc4(0,int(constraint[0]),x, int(rot[x]))])
        for x in range(len(rot)):
            #test2.append([(1, constraint[0], rot[x], rot[(x+1)%len(rot)])])
            phi.add_clause([enc4(1, int(constraint[0]), int(rot[x]), int(rot[(x+1)%len(rot)]))])
        #print(test1)
        #print(test2)
        

    

    if phi.solve():
        #k>0 picks out the true variables
        model = sorted([dec4(k) for k in phi.get_model() if k > 0])
        print(model)
        return model
        




def main():
    global N
    f = open(argv[1], 'r')
    # the file format consists of the following:
    #    - the first line is the number of vertices
    #    - each subsequent line is the endpoints of an edge
    N = int(next(f))
    edges = [[False for _ in range(N)] for _ in range(N)]
    for line in f:
        tokens = line.split()
        u = int(tokens[0])
        v = int(tokens[1])
        edges[u][v] = True
        edges[v][u] = True
    
    #constraint = input("please enter constraint\n")

    #if rotation system exists it has form \{v_i. n1 n2 n3 ...\}
    #for each vertex in the system, where n_1 is a cyclic permutation of neighbors
    #constraint format: string of numbers of form v_i n1 n2 n3 ... separated by comma
    #represents one row in a possible rotation system, forces the search to look for systems with this row
    model_var = find_rotation(edges)

    if model_var is not None:
    
        #model, and hence array is sorted lex
        array_only = [(t[1], t[3]) for t in model_var if t[0]==0]
        current_vertex = array_only[0][0]
        rotation= []
        current_ver_array = [current_vertex, "."]
        for t in array_only:
            #check if tuple first component is equal to current
            if t[0] == current_vertex:
                #if so append, if not start new
                current_ver_array.append(t[1])
            else:
                rotation.append(current_ver_array)
                current_vertex= t[0]
                current_ver_array = [current_vertex,".",t[1]]
        rotation.append(current_ver_array)
        print(rotation)

    else: 
        print("sorry")


if __name__ == "__main__":
    main()
