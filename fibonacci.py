import timeit
from functools import lru_cache
import matplotlib.pyplot as plt

# --- Splay Tree Implementation ---

class SplayNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root

        # Key lies in left subtree
        if key < root.key:
            if root.left is None:
                return root
            # Zig-Zig (Left Left)
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._right_rotate(root)
            # Zig-Zag (Left Right)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._left_rotate(root.left)
            return root if root.left is None else self._right_rotate(root)

        else:
            # Key lies in right subtree
            if root.right is None:
                return root
            # Zag-Zig (Right Left)
            if key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._right_rotate(root.right)
            # Zag-Zag (Right Right)
            elif key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._left_rotate(root)
            return root if root.right is None else self._left_rotate(root)

    def insert(self, key, value):
        if self.root is None:
            self.root = SplayNode(key, value)
            return

        self.root = self._splay(self.root, key)

        if self.root.key == key:
            # Update value if key exists
            self.root.value = value
            return

        node = SplayNode(key, value)

        if key < self.root.key:
            node.right = self.root
            node.left = self.root.left
            self.root.left = None
            self.root = node
        else:
            node.left = self.root
            node.right = self.root.right
            self.root.right = None
            self.root = node

    def find(self, key):
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            return self.root.value
        return None

# --- Fibonacci with LRU Cache ---

@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

# --- Fibonacci with Splay Tree caching ---

def fibonacci_splay(n, tree):
    cached = tree.find(n)
    if cached is not None:
        return cached
    if n <= 1:
        tree.insert(n, n)
        return n
    val = fibonacci_splay(n-1, tree) + fibonacci_splay(n-2, tree)
    tree.insert(n, val)
    return val

# --- Measurement ---

def measure_time(func, *args, repeats=5):
    timer = timeit.Timer(lambda: func(*args))
    times = timer.repeat(repeat=repeats, number=1)
    return sum(times) / len(times)

def main():
    ns = list(range(0, 351, 50))  # Зменшено максимум n до 350

    lru_times = []
    splay_times = []

    for n in ns:
        fibonacci_lru.cache_clear()
        t_lru = measure_time(fibonacci_lru, n)

        tree = SplayTree()
        t_splay = measure_time(fibonacci_splay, n, tree)

        lru_times.append(t_lru)
        splay_times.append(t_splay)

        print(f"n={n:<4} | LRU time: {t_lru:.8f} s | Splay time: {t_splay:.8f} s")

    # --- Print formatted table ---
    print("\n{:<10} {:<20} {:<20}".format("n", "LRU Cache Time (s)", "Splay Tree Time (s)"))
    print("-" * 50)
    for n, t_lru, t_splay in zip(ns, lru_times, splay_times):
        print(f"{n:<10} {t_lru:<20.8f} {t_splay:<20.8f}")

    # --- Plotting ---

    plt.figure(figsize=(12, 6))
    plt.plot(ns, lru_times, 'o-', label='LRU Cache')
    plt.plot(ns, splay_times, 's-', label='Splay Tree')
    plt.xlabel('n (Fibonacci number index)')
    plt.ylabel('Average Execution Time (seconds)')
    plt.title('Fibonacci Calculation Time: LRU Cache vs Splay Tree')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
