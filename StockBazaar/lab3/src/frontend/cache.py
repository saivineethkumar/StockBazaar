'''
Class to represent a node in the doubly linked list.
'''
class Node:
    def __init__(self, key, val):
        self.key = key # Key of the node
        self.val = val # Value of the node
        self.next = None # pointer to the next node
        self.prev = None # pointer to the previous node

'''
Class to implement a Least Recently Used (LRU) Cache using a doubly linked list and a dictionary.
'''
class LRUCache:
    '''
    Initializes the LRUCache with the specified size.
    Arguments:
    - size: The maximum number of items that can be stored in the cache.
    '''
    def __init__(self, size):
        self.size = size # size of the cache
        self.curr_size = 0 # current size of the cache
        self.cache = {} # dictionary that maps cache keys to their corresponding nodes in the linked list. 
        self.head = Node(0, 0) # head of the doubly linked list 
        self.tail = Node(0, 0) # tail of the doubly linked list
        self.head.next = self.tail
        self.tail.prev = self.head
        
    '''
    Retrieves an item from the cache.
    Arguments:
    - key: The key whose value is to be retrieved.
    Returns:
    - If the key exists in the cache, the corresponding value is returned. Otherwise, None is returned.
    '''
    def get(self, key):
        # return None if key is not present in cache
        if key not in self.cache:
            return None
        # retrieve the node from the dictionary associated with the key
        curr = self.cache[key]
        # remove node from the linked list
        curr.next.prev = curr.prev
        curr.prev.next = curr.next

        # add the node to the beginning of the linked list
        curr.next = self.head.next
        curr.next.prev = curr
        self.head.next = curr
        curr.prev = self.head
        self.cache[key] = curr
        return curr.val
        
    '''
    Inserts or updates an item in the cache.
    Arguments:
    - key: The key to be inserted or updated.
    - value: The value to be associated with the key.
    '''
    def put(self, key, value):
        # remove from cache if already present
        if key in self.cache:
            self.remove(key)
        
        # if cache is full, remove the least recently used key
        if self.curr_size == self.size:
            self.removeLeastRecent()
        
        #create a new node and add to the head
        curr = Node(key, value)
        curr.next = self.head.next
        curr.next.prev = curr
        self.head.next = curr
        curr.prev = self.head
        self.cache[key] = curr
        # increase cache size by 1
        self.curr_size += 1

    '''
    Removes the least recently used key-value pair from the cache.
    '''
    def removeLeastRecent(self):
        # if size is 0 return
        if self.curr_size == 0:
            return
        # remove the last node from the linked list
        curr = self.tail.prev
        self.tail.prev = curr.prev
        curr.prev.next = self.tail
        #delete from the dictionary
        del self.cache[curr.key]
        # decrease size by 1
        self.curr_size -= 1
    '''
    Removes an item with the given key from the cache.
    Arguments:
    - key: The key to be removed.
    '''
    def remove(self, key):
        # return if key not present in the dictionary
        if key not in self.cache:
            return
        curr = self.cache[key]
        # remove from the linked list
        curr.prev.next = curr.next
        curr.next.prev = curr.prev
        # remove the key from the dictionary
        del self.cache[key]
        # decrease size by 1
        self.curr_size -= 1
        
