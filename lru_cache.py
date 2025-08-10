import random
import time
from collections import OrderedDict

class LRUCache:
    """
    LRU (Least Recently Used) cache implementation using OrderedDict.
    Stores key-value pairs up to a specified capacity.
    Supports selective invalidation of cached ranges containing a given index.
    """
    def __init__(self, capacity=1000):
        """
        Initialize the LRU cache with given capacity.
        
        Args:
            capacity (int): Maximum number of cached items.
        """
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        """
        Retrieve value for the given key and mark it as recently used.
        
        Args:
            key (tuple): Key to look up in cache.
            
        Returns:
            Cached value if key exists, otherwise -1.
        """
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        """
        Add or update the key with value in cache and mark it recently used.
        If capacity is exceeded, evicts the least recently used item.
        
        Args:
            key (tuple): Cache key.
            value: Value to store.
        """
        if key in self.cache:
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity:
                self.cache.popitem(last=False)
        self.cache[key] = value

    def invalidate_ranges_containing(self, index):
        """
        Invalidate (remove) all cached ranges that include the specified index.
        
        Args:
            index (int): Index which invalidates all ranges containing it.
        """
        keys_to_remove = [k for k in self.cache.keys() if k[0] <= index <= k[1]]
        for k in keys_to_remove:
            del self.cache[k]

def range_sum_no_cache(arr, L, R):
    """
    Calculate sum of array elements in range [L, R] without caching.
    
    Args:
        arr (list): Input array.
        L (int): Left index of range.
        R (int): Right index of range.
        
    Returns:
        int: Sum of elements from L to R inclusive.
    """
    return sum(arr[L:R+1])

def update_no_cache(arr, index, value):
    """
    Update the element at given index in array without caching.
    
    Args:
        arr (list): Input array.
        index (int): Index to update.
        value (int): New value to assign.
    """
    arr[index] = value

def range_sum_with_cache(arr, cache, L, R):
    """
    Calculate sum of array elements in range [L, R] using LRU cache.
    If range sum is cached, returns cached result.
    Otherwise computes sum, caches it, and returns the value.
    
    Args:
        arr (list): Input array.
        cache (LRUCache): Cache instance.
        L (int): Left index of range.
        R (int): Right index of range.
        
    Returns:
        int: Sum of elements from L to R inclusive.
    """
    res = cache.get((L, R))
    if res == -1:
        res = sum(arr[L:R+1])
        cache.put((L, R), res)
    return res

def update_with_cache(arr, cache, index, value):
    """
    Update the element at given index in array and invalidate cached ranges
    that contain this index.
    
    Args:
        arr (list): Input array.
        cache (LRUCache): Cache instance.
        index (int): Index to update.
        value (int): New value to assign.
    """
    arr[index] = value
    cache.invalidate_ranges_containing(index)

def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    """
    Generate a list of queries consisting of 'Range' sum queries and 'Update' operations.
    Majority of 'Range' queries target a fixed set of 'hot' (frequently accessed) ranges.
    
    Args:
        n (int): Size of the array.
        q (int): Number of queries to generate.
        hot_pool (int): Number of hot ranges.
        p_hot (float): Probability that a 'Range' query is from hot pool.
        p_update (float): Probability that a query is an 'Update'.
    
    Returns:
        list: List of queries formatted as tuples.
            - ('Range', L, R) for sum queries.
            - ('Update', index, value) for updates.
    """
    hot = [(random.randint(0, n//2), random.randint(n//2, n-1)) for _ in range(hot_pool)]
    queries = []
    for _ in range(q):
        if random.random() < p_update:
            idx = random.randint(0, n-1)
            val = random.randint(1, 1000)
            queries.append(("Update", idx, val))
        else:
            if random.random() < p_hot:
                left, right = random.choice(hot)
            else:
                left = random.randint(0, n-1)
                right = random.randint(left, n-1)
            queries.append(("Range", left, right))
    return queries

def run_test():
    """
    Run performance test comparing execution time of queries with and without LRU caching.
    Prints the time taken and speedup factor.
    """
    N = 100_000
    Q = 50_000

    # Initialize the array with random values
    array = [random.randint(1, 1000) for _ in range(N)]
    queries = make_queries(N, Q)

    # Run queries without cache
    start = time.time()
    for q in queries:
        if q[0] == "Range":
            range_sum_no_cache(array, q[1], q[2])
        else:
            update_no_cache(array, q[1], q[2])
    no_cache_time = time.time() - start

    # Run queries with cache
    array_cache = array.copy()
    cache = LRUCache(capacity=1000)

    start = time.time()
    for q in queries:
        if q[0] == "Range":
            range_sum_with_cache(array_cache, cache, q[1], q[2])
        else:
            update_with_cache(array_cache, cache, q[1], q[2])
    cache_time = time.time() - start

    print(f"Without cache: {no_cache_time:.2f} seconds")
    print(f"With LRU cache: {cache_time:.2f} seconds (speedup ×{no_cache_time/cache_time:.2f})")

if __name__ == "__main__":
    run_test()
