from tkinter import *
from functools import partial
from time import sleep
from threading import Thread


class Node():
    mode = 0
    all = []

    start = []
    end = []

    blockade = []

    start_node = None
    end_node = None

    def __init__(self, x, y):
        
        self.x = x
        self.y = y

        self.g = 0
        self.h = 0
        self.f = 0

        self.parent = None

        Node.all.append(self)
    
    def __repr__(self):
        return f"Cell({self.x},{self.y})"
    
    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)

    def begin(self, event):

        Thread(target=self.a_star, daemon=True).start()

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

        
        elif Node.mode == 1:

            Node.end.append(x)
            Node.end.append(y)
            Node.end_node = self.get_node(x, y)
            
            Node.mode = 2
            self.node.configure(bg='red')

            root.bind('<Return>', self.begin)
            
            #print(self.heuristic(Node.start_node, Node.end_node))

        elif Node.mode == 2:
            self.node.configure(bg='black')
            Node.blockade.append(self.get_node(x, y))
            #print(Node.blockade)
            
            
    def heuristic(self, node1, node2):
        result = abs(node1.x - node2.x) + abs(node1.y-node2.y)
        return result
    

    def get_node(self, x, y):
        for node in Node.all:
            if node.x == x and node.y == y:
                return node

    def get_node_f(self, f_score):
        for node in Node.all:
            if node.f == f_score:
                return node
    
    @property
    def neighbour_list(self):
        node_list = [
            self.get_node(self.x - 1, self.y - 1),
            self.get_node(self.x - 1, self.y),
            self.get_node(self.x - 1, self.y + 1),
            self.get_node(self.x, self.y - 1),
            self.get_node(self.x + 1, self.y - 1),
            self.get_node(self.x + 1, self.y),
            self.get_node(self.x + 1, self.y + 1),
            self.get_node(self.x, self.y + 1),
        ]
        node_list = [node for node in node_list if node is not None]

        return node_list
    
    def a_star(self):
        open_list = []
        closed_list = []
        #closed_list = closed_list + Node.blockade
        current = 0
        Node.start_node.g = Node.start_node.h = Node.start_node.f = 0
        Node.end_node.g = Node.end_node.h = Node.end_node.f = 0

        #open_list.append(start_node)

        #Node.start_node.f = self.heuristic(Node.start_node, Node.end_node)
        #print(self.get_node_f(Node.start_node.f))

        open_list.append(Node.start_node)

    
        while len(open_list) > 0:

            current_node = open_list[0]
            current_index = 0
            
            

            for index, item in enumerate(open_list):
                #print(current_node, item, item.f, current_node.f)
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            root.update_idletasks()
            root.after(20)
            open_list.pop(current_index)
            #print("OPEN???", open_list)
            #print("close???", closed_list)
            closed_list.append(current_node)
            current_node.node.configure(bg = "light blue")

            # check if we reached the end

            if current_node == Node.end_node:
                #print("foo")
                total_path = []
                current = current_node
                Node.start_node.parent = None

                while current is not None:
                    root.update_idletasks()
                    root.after(20)
                    total_path.append(current)
                    current.node.configure(bg ="red")
                    current = current.parent

                    
                    
                
                total_path.append(Node.start_node)
                print (total_path)

                
                
                return True
            
            #print(current_node.x, type(current_node), type(Node.start_node))
            neighbour = current_node.neighbour_list
            
            for i in neighbour:
                root.update_idletasks()
                root.after(20)
                
                
                if i in closed_list or i in Node.blockade:
                    
                    continue

                i.node.configure(bg="blue")
                i.g = current_node.g + 1

                
                
                i.h = self.heuristic(i, Node.end_node)
                i.f = i.g + i.h

                for k in open_list:
                    if i == k and i.g > k.g:
                        continue
                
                
                i.parent = current_node
                #print(f"adding {i} to {open_list} because its not in {closed_list}", current_node)
                open_list.append(i)

        print("Fail!")


                     
 
        
root = Tk()
root.title("A* Algorithm")

node_frame = Frame(
    root
)
node_frame.place(x=0,y=0)

for x in range(25):
    for y in range(25):
        c = Node(x, y)
        c.create_node(node_frame)
        c.node.grid(column = x, row = y)

#root.bind('<Return>', Node.a_star)

#print(Node.start, Node.end)
root.mainloop()