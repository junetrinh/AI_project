# if we want to get more information, change this flag to true
print_flag = False

class priority_queue:
    
    def __init__(self):
        self.heap = []
        self.last_i = -1

    # function to manipulate the indexes
    def _get_parent_i(self, i):
        return int((i-1)/2)

    def _get_left_child_i(self, i):
        return int(2*i + 1)

    def _get_right_child_i(self, i):
        return int(2*i + 2)

    def _up_heap(self):
        #bring the item store at last node to the correct position regard the sorting key
        SORT_KEY = 0
    
        # case where heap is sorted/empty
        if len(self.heap) <= 1:
            return
        

        # i will use iteration to swap, in order to save recursive's call space. 
        item_i = self.last_i
        parent_i = self._get_parent_i(item_i)

        examined_node = self.heap[item_i]
        parent_node = self.heap[parent_i]

        while item_i == 0 or examined_node[SORT_KEY] <= parent_node[SORT_KEY] :
            # perform swap
            self.heap[parent_i] = examined_node
            self.heap[item_i] = parent_node

            # go up the tree
            item_i = parent_i
            parent_i = self._get_parent_i(parent_i)
            parent_node = self.heap[parent_i]

        # after exit the loop the position of examanined node should be correct.


    def _find_highest_priority_child_i(self, item_i):
        left_i = self._get_left_child_i(item_i)
        right_i = self._get_right_child_i(item_i)
        # outter most leaf
        if left_i > self.last_i and right_i > self.last_i:
            return -1

        highest_priority = -1
        #print("left: " + str(left_i) + ", right: " + str(right_i) + " || last: " + str(self.last_i))
        if (left_i <= self.last_i
                and right_i > self.last_i ): 
            highest_priority = left_i
        
        if (left_i > self.last_i
                and right_i <= self.last_i ): 
            highest_priority = right_i

        if (left_i <= self.last_i
                and right_i <= self.last_i ): 
            highest_priority = left_i

            if(self.heap[right_i] < self.heap[left_i]):
                highest_priority = right_i

        return highest_priority


    def _down_heap(self, item_i_):
        SORT_KEY = 0

        item_i = item_i_
        highest_p_child = self._find_highest_priority_child_i(item_i)
        #print("highest: " + str(highest_p_child))
        while item_i < self.last_i and highest_p_child > -1:
            # perform swap
            dummy_node = self.heap[item_i]
            if print_flag:
                print("Swap: " + str(dummy_node) + " <-> " + str(self.heap[highest_p_child]) + " || last:" + str(self.last_i))
            self.heap[item_i] = self.heap[highest_p_child]
            self.heap[highest_p_child] = dummy_node

            item_i = highest_p_child
            highest_p_child = self._find_highest_priority_child_i(item_i)

    def add(self, key_val, item):

        HIGHEST_PRIORITY = 0
        OUT_OF_ORDER_I = 0

        self.last_i += 1
        self.heap.append((key_val, item))

        # bring the item to its correct position
        self._up_heap()
        # print("Current list:")
        # for (i, item) in self.heap:
        #     print("(" + str(i) + "," + item + ")")
        # print("-- --")

        
    def pop(self):
        HIGHEST_PRIORITY = 0
        OUT_OF_ORDER_I = 0

        # swap the lowest priority/ root node of the tree with the outter most leaf
        return_node = self.heap[HIGHEST_PRIORITY]

        self.heap[HIGHEST_PRIORITY] = self.heap[self.last_i]
        self.heap[self.last_i] = return_node

        # remove and fixing the heap by perform a down heap
        self.heap.pop(self.last_i)
        self.last_i -= 1
        if print_flag:
            print("\n\nBefore fix:----------------------------------------------------------------")
            for (i, item) in self.heap:
                print("(" + str(i) + "," + item + ")")
            print("-- --")

        self._down_heap(OUT_OF_ORDER_I)
        if print_flag:
            print("After fix:")
            for (i, item) in self.heap:
                print("(" + str(i) + "," + item + ")")
            print("-- ------------------------------------------------------ \n")
        return return_node

    def clear(self):
        self.heap.clear()
        self.last_i = -1

    def top():
        if self.last_i > -1:
            return self.heap[0]
        return -1
    
        
def print_node(node):
    print("(" + str(node[0]) + "," +  node[1] + ")")

p_queue = priority_queue() 

p_queue.add(0, "c")
p_queue.add(25, "d")
p_queue.add(1, "e")
p_queue.add(1, "e")
p_queue.add(8, "g")
p_queue.add(18, "f")
p_queue.add(4, "cc")

while p_queue.last_i > -1:
    node = p_queue.pop()

    print_node(node)