from tkinter import *
from functools import partial


class Node():
    mode = 0
    all = []

    start = []
    end = []

    start_node = None
    end_node = None

    def __init__(self, x, y):
        
        self.x = x
        self.y = y

        self.g = 0
        self.h = 0
        self.f = 0

        Node.all.append(self)
    
    def __repr__(self):
        return f"Cell({self.x},{self.y})"

    def create_node(self, location):
        node = Button(location,
        width = 4,
        height = 2,
        text=f"{self.x},{self.y}",
        command=partial(self.click, x, y), 
        state="normal"
        )

        self.node = node

    def click(self, x, y):
        if Node.mode == 0:

            Node.start.append(x)
            Node.start.append(y)
            Node.start_node = self.get_node(x, y)
            
            Node.mode = 1
            self.node.configure(bg='green')
            
            #print(Node.all)
            

        
        elif Node.mode == 1:

            Node.end.append(x)
            Node.end.append(y)
            
            Node.mode = 2
            self.node.configure(bg='red')

        elif Node.mode == 2:
            self.node.configure(bg='black')
            
            root.bind('<Return>', self.a_star)
            
    
    def heuristic(self, node1, node2):
        result = abs(node1[0] - node2[0]) + abs(node1[1]-node2[1])
        return result
    

    def get_node(self, x, y):
        for node in Node.all:
            if node.x == x and node.y == y:
                return node

    def get_node_f(self, f_score):
        for node in Node.all:
            if node.f == f_score:
                return node
    
    def a_star(self, event):
        open_list = []
        closed = []
        current = 0

        #open_list.append(start_node)

        Node.start_node.f = self.heuristic(Node.start, Node.end)
        print(Node.start_node.f)
        
        #while len(open_list) > 0:
        #current = f_score.index(5)
        #self.get_node(min(f_score))
        #print("Cur", current)
            #if current == Node.end:
                #break
                
            


        
        


    
            






root = Tk()
root.title("A* Algorithm")

node_frame = Frame(
    root
)
node_frame.place(x=0,y=0)

for x in range(10):
    for y in range(10):
        c = Node(x, y)
        c.create_node(node_frame)
        c.node.grid(column = x, row = y)



#print(Node.start, Node.end)
root.mainloop()