"""
Min-Heap implementation (array-based)
Goal: support add(), remove(), peek() with clear, human-friendly comments.

Coded by Dhanya Sridhar
"""

from typing import List, Optional  # Type hints for readability (lists and optional returns)

# ---------- Index helper functions (treat the list like a binary tree) ----------

def left_child(parent: int) -> int:      # Given a parent index, compute left child index
    return 2 * parent + 1                # Formula for left child in 0-based array heap

def right_child(parent: int) -> int:     # Given a parent index, compute right child index
    return 2 * (parent + 1)              # Equivalent to 2*parent + 2 (right child formula)

def parent(child: int) -> int:           # Given a child index, compute its parent index
    return (child - 1) // 2              # Integer division gives the parent position

def swap(heap_array: list, i: int, j: int) -> None:  # Swap two elements inside the array
    """Swap two array elements in place (only if they are different positions)."""
    if i != j:                                       # No-op if indices are the same
        temp = heap_array[i]                         # Store first value temporarily
        heap_array[i] = heap_array[j]                # Move second value into first slot
        heap_array[j] = temp                         # Put temp (first value) into second slot

# ---------- MinHeap class (stores strings; top is always the smallest string) ----------

class MinHeap:
    def __init__(self):                   # Constructor: start with an empty list
        self.a: List[str] = []            # Underlying array that represents the heap

    # Shortcuts to our index helpers so code below is tidy
    def _parent(self, i: int) -> int: return parent(i)      # Parent index for i
    def _left(self, i: int) -> int: return left_child(i)     # Left child index for i
    def _right(self, i: int) -> int: return right_child(i)   # Right child index for i

    def is_empty(self) -> bool:           # True if the heap has no elements
        return len(self.a) == 0

    # Safety check used in asserts: verifies the min-heap property everywhere
    def _is_valid_heap(self) -> bool:
        n = len(self.a)                                   # Number of items in heap
        for i in range(n):                                # Check each node i
            l, r = self._left(i), self._right(i)          # Compute children indices
            if l < n and not (self.a[i] <= self.a[l]):    # If left child exists and is smaller than parent → bad
                return False
            if r < n and not (self.a[i] <= self.a[r]):    # If right child exists and is smaller than parent → bad
                return False
        return True                                       # All checks passed

    # Move a node up while it is smaller than its parent (fixes violations after insert)
    def _sift_up(self, i: int) -> None:
        while i > 0:                                      # While the node has a parent
            p = self._parent(i)                           # Get parent index
            if self.a[i] < self.a[p]:                     # If child is smaller than parent (violation)
                swap(self.a, i, p)                        # Swap child up, parent down
                i = p                                     # Continue from parent's new position
            else:
                break                                     # Stop when order is correct

    # Move a node down while it is larger than one of its children (fixes after remove)
    def _sift_down(self, i: int) -> None:
        n = len(self.a)                                   # Current heap size
        while True:                                       # Keep trying to move down
            l, r = self._left(i), self._right(i)          # Children indices
            smallest = i                                  # Assume current node is smallest
            if l < n and self.a[l] < self.a[smallest]:    # If left child exists and is smaller
                smallest = l
            if r < n and self.a[r] < self.a[smallest]:    # If right child exists and is smaller
                smallest = r
            if smallest != i:                             # If a child is smaller than current
                swap(self.a, i, smallest)                 # Swap current with the smaller child
                i = smallest                              # Continue from the child's new position
            else:
                break                                     # Stop when current is ≤ both children

    # Public: insert a value and keep heap valid
    def add(self, x: str) -> None:
        self.a.append(x)                                  # Put new value at the end (next open slot)
        self._sift_up(len(self.a) - 1)                    # Pull it up until parent ≤ child
        assert self._is_valid_heap()                      # Sanity check in development

    # Public: look at the smallest value without removing it
    def peek(self) -> Optional[str]:
        return None if self.is_empty() else self.a[0]     # Root holds the minimum

    # Public: remove and return the smallest value
    def remove(self) -> Optional[str]:
        if self.is_empty():                                # If nothing to remove, return None
            return None
        min_val = self.a[0]                                # Save the root (smallest)
        last = self.a.pop()                                # Take the last element off the array
        if self.a:                                         # If the heap still has elements
            self.a[0] = last                               # Move last element to the root hole
            self._sift_down(0)                             # Push it down until children ≥ parent
        assert self._is_valid_heap()                       # Sanity check in development
        return min_val                                     # Return the minimum we removed

# Convenience factory (optional, just for nicer syntax in tests)
def make_heap() -> MinHeap:
    return MinHeap()

# ---------- Demo / self-tests ----------
if __name__ == "__main__":
    # Build a heap from a set of strings
    h = make_heap()                                       # Create a new min-heap
    data = ["pear", "apple", "orange", "banana", "grape", "apricot", "kiwi"]  # Sample data
    for s in data:                                        # Insert all items
        h.add(s)

    print("Peek (should be 'apple'):", h.peek())          # Show the smallest without removing

    out = [h.remove() for _ in range(len(data))]          # Pop everything out in sorted order
    print("Removed order:", out)                          # Should be ascending lexicographically

    # Edge cases
    h2 = make_heap()                                      # New empty heap
    print("Remove on empty:", h2.remove())                # Expect None
    h2.add("z")                                           # Insert one item
    print("Peek after one insert:", h2.peek())            # Expect 'z'
    print("Remove one:", h2.remove())                     # Expect 'z'
    print("Remove again (empty):", h2.remove())           # Expect None

    # Another deterministic test
    seq = ["m", "c", "t", "a", "x", "b", "d", "d", "c"]   # Mixed order with duplicates
    h3 = make_heap()                                      # New heap
    for s in seq: h3.add(s)                               # Insert items
    popped = [h3.remove() for _ in range(len(seq))]       # Remove all
    print("Sorted input: ", sorted(seq))                  # Expected order
    print("Heap popped:  ", popped)                       # What the heap produced

    print(" All tests completed.")