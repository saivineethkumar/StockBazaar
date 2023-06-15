import sys
import unittest
sys.path.append('../..')
from src.frontend.cache import LRUCache

CACHE_SIZE = 2

class TestCaching(unittest.TestCase):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def initailize_cache(self):
        return LRUCache(CACHE_SIZE)

    def test_put_to_cache(self):
        '''
        Function to test add to cache
        '''
        print(f"Test add to cache call")
        cache = self.initailize_cache()
        #precondition test
        self.assertTrue(cache.get("stock_test") == None)
        #test add
        cache.put("stock_test", 1)
        self.assertTrue(cache.get("stock_test") == 1)
        print(f"Test complete!")

    def test_get_from_cache(self):
        '''
        Function to get call to cache
        '''
        print(f"Test get from cache call")
        cache = self.initailize_cache()
        #precondition test. Should return None when key is not present
        self.assertTrue(cache.get("stock_test") == None)
        cache.put("stock_test", 1)
        # test get
        self.assertTrue(cache.get("stock_test") == 1)
        # if key is already present it should update the cache
        cache.put("stock_test", 100)
        self.assertTrue(cache.get("stock_test") == 100)
        print(f"Test complete!")
   
    def test_eviction_policy(self):
        '''
        Function to test eviction policy. Least recently used key should be evicted when cache is full.
        '''
        print(f"Test evict the least recently used key when cache is full")
        cache = self.initailize_cache()
        cache.put("stock_test_1", 1)
        cache.put("stock_test_2", 2)

         #precondition test
        self.assertTrue(cache.get("stock_test_2") == 2)
        self.assertTrue(cache.get("stock_test_1") == 1)

        #Adding more items to cache
        cache.put("stock_test_3", 3)
        #stock_test_2 should be evicted and stock_test_3 should be present 
        
        self.assertTrue(cache.get("stock_test_3") == 3)
        self.assertTrue(cache.get("stock_test_2") == None)

        cache.put("stock_test_4" , 4)
        cache.put("stock_test_5" , 5)
        #stock_test_1 and stock_test_3 should be evicted and stock_test_4, stock_test_5 should be present 
        self.assertTrue(cache.get("stock_test_3") == None)
        self.assertTrue(cache.get("stock_test_1") == None)
        self.assertTrue(cache.get("stock_test_4") == 4)
        self.assertTrue(cache.get("stock_test_5") == 5)
        print(f"Test complete!")

if __name__ == '__main__':
    unittest.main()


