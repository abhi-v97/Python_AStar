from tkinter import *
from functools import partial
from time import sleep
from threading import Thread

# time (ms) to wait between checking each node. 0 for instant result, 20 to see each step (and it looks cool)
t = 0


class Node():

    # mode controls the flow of the program
    # all and blockade are lists for pathfinding
    mode = 0
    all = []
    blockade = []

    start_node = None
    end_node = None

    def __init__(self, x, y):

        # x and y are used to find the node's position
        # g is the distance between current and start node
        # h is the heuristic, estimated distance between current node and end node
        # f = g + h, i.e. total cost of node
        # parent is the node preceding the current node
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

    # multithreading used as without it, tkinter window freezes after roughly five seconds
    # the code works without it, it eventually spits out the result. But GUI stops updating.
    def begin(self, event):
        Thread(target=self.a_star, daemon=True).start()

    def create_node(self, location):
        node = Button(location,
                      width=4,
                      height=2,
                      # text=f"{self.x},{self.y}", # put x, y values as text in the node, for debugging the algorithm
                      command=partial(self.click, x, y),
                      state="normal"
                      )

        # used for the blockade function
        # <Enter> event triggers after mouse hover
        node.bind('<Enter>', partial(self.create_blockade, x, y))
        self.node = node

    # function that triggers upon mouse click, set start and end nodes
    def click(self, x, y):
        if Node.mode == 0:

            Node.start_node = self.get_node(x, y)
            Node.mode = 1
            self.node.configure(bg='green')

        elif Node.mode == 1:

            Node.end_node = self.get_node(x, y)
            Node.mode = 2
            self.node.configure(bg='red')

            # Allow pathfinding to begin AFTER start and end are set
            root.bind('<Return>', self.begin)

        elif Node.mode == 2:
            # used for the create_blockade method
            Node.mode = 3

        else:
            Node.mode = 2

    def create_blockade(self, x, y, event):

        if Node.mode == 3:

            foo = self.get_node(x, y)
            foo.node.configure(bg='black')
            Node.blockade.append(foo)

    # Helper methods to grab node based on x and y
    def get_node(self, x, y):
        for node in Node.all:
            if node.x == x and node.y == y:
                return node

    def get_node_f(self, f_score):
        for node in Node.all:
            if node.f == f_score:
                return node

    # return list of available neighbours
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
        # get node returns None for nodes that don't exist, eg those outside the boundary
        # list comprehension to remove None items created for edge cases
        node_list = [
            node for node in node_list if node is not None and node not in Node.blockade]

        return node_list

    def a_star(self):

        # open list is possible nodes that may lead to the end
        # closed list are nodes that have gone through the while loop already
        open_list = []
        closed_list = []

        open_list.append(Node.start_node)

        while len(open_list) > 0:

            current_node = open_list[0]
            current_index = 0

            # Pick the node with smallest f from open list
            for index, item in enumerate(open_list):
                #print(current_node, item, item.f, current_node.f)
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Update the GUI
            root.update_idletasks()
            root.after(t)

            # Remove node from open list, add it to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            current_node.node.configure(bg="purple")

            # check if we reached the end
            if current_node == Node.end_node:

                # print("foo")
                total_path = []
                current = current_node
                Node.start_node.parent = None

                # Keep cycling through parents until you hit start node, whose parent is None
                while current is not None:
                    root.update_idletasks()
                    root.after(t)
                    total_path.append(current)
                    current.node.configure(bg="red")
                    current = current.parent

                total_path.reverse()
                print(total_path)

                return total_path

            #print(current_node.x, type(current_node), type(Node.start_node))
            neighbour = current_node.neighbour_list
            # print(neighbour)

            for i in neighbour:
                root.update_idletasks()
                root.after(t)

                # go back to start of for loop
                if i in closed_list or i in Node.blockade:
                    continue

                # Set f, g, h values
                i.g = current_node.g + 1
                i.h = ((i.x - Node.end_node.x)**2) + \
                    ((i.y - Node.end_node.y)**2)
                i.f = i.g + i.h
                i.node.configure(bg="blue")

                # additional check if g score is better or not
                for k in open_list:
                    if i == k or i.g > k.g:
                        continue

                i.parent = current_node
                #print(f"adding {i} to {open_list} because its not in {closed_list}", current_node)
                if i not in open_list:
                    open_list.append(i)
            current_node.node.configure(bg="light blue")

        # If open list has been exhausted without reaching the end, print Fail
        print("Fail!")


root = Tk()
root.title("A* Algorithm")
root.geometry("1000x1100")

node_frame = Frame(
    root
)
node_frame.place(x=0, y=0)

for x in range(25):
    for y in range(25):
        c = Node(x, y)
        c.create_node(node_frame)
        c.node.grid(column=x, row=y)

#print(Node.start, Node.end)
root.mainloop()
