#for converting raw model output into
#analyzable .txt file format
#.txt files 1st line is num of nodes
#then each following line a unique edge
#e.g. 0 1
#     0 3    &etc.

def main():
    g_rot = [[0, '.', 1, 9, 5, 4], [1, '.', 0, 4, 8, 3, 11, 10, 9], [2, '.', 7, 9, 10], [3, '.', 1, 8, 4, 7, 6, 11], [4, '.', 0, 5, 7, 3, 8, 1], 
            [5, '.', 0, 9, 7, 4], [6, '.', 3, 7, 10, 11], [7, '.', 2, 10, 6, 3, 4, 5, 9], [8, '.', 1, 4, 3], [9, '.', 0, 1, 10, 2, 7, 5], 
            [10, '.', 1, 11, 6, 7, 2, 9], [11, '.', 1, 3, 6, 10]]
    
    h_rot = [[0, '.', 2, 3, 10, 8, 7, 11], [1, '.', 2, 6, 5], [2, '.', 0, 11, 4, 6, 1, 5, 3], [3, '.',0, 2, 5, 10], [4, '.', 2, 11, 9, 6], 
            [5, '.', 1, 6, 8, 10, 3, 2], [6, '.', 1, 2, 4, 9, 8, 5], [7, '.', 0, 8, 11], [8, '.', 0, 10, 5, 6, 9, 11, 7], [9, '.', 4, 11, 8, 6], 
            [10, '.', 0, 3, 5, 8], [11, '.', 0, 7, 8, 9, 4, 2]]

    vertex = 0

    rotation_system_output = open(input("please enter filename for output\n"), "w")
    num_nodes = len(g_rot) #never working with empty entry systems
    #for "old" formatting, for Sage input, this is unnecessary
    #rotation_system_output.write( num_nodes + "\n")
    for i in g_rot:
        vertex = i[0]
        for j in range(2, len(i)):
          #for input to eluc
          #rotation_system_output.write(vertex + " " + g_rot[i][j] + "\n")

          #for input to Sage
          rotation_system_output.write("(" + str(vertex) + "," + str(i[j]) + "),")

    rotation_system_output.write("\n\n")

    for i in h_rot:
        vertex = i[0]
        for j in range(2, len(i)-1):
          #for input to eluc
          #rotation_system_output.write(vertex + " " + g_rot[i][j] + "\n")
          
          #for input to Sage
          rotation_system_output.write("(" + str(vertex) + "," + str(i[j]) + "),")
    #to avoid ending file with a newline (throws a bug if otherwise)
    i = len(h_rot)-1
    rotation_system_output.write("(" + str(vertex) + "," + str(h_rot[i][-1]) + ")")





if __name__ == "__main__":
    main()