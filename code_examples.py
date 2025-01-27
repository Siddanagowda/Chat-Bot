"""Collection of commonly requested code examples."""

BINARY_SEARCH = '''```python
def binary_search(arr, target):
    """Performs a binary search on a sorted array.
    
    Args:
        arr (list): The sorted array to search
        target: The value to search for
    
    Returns:
        int: The index of the target value in the array, or -1 if not found
    """
    low = 0
    high = len(arr) - 1
    
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
            
    return -1

# Example usage:
arr = [1, 3, 5, 7, 9, 11, 13, 15]
target = 7
result = binary_search(arr, target)
print(f"Target {target} found at index: {result}")  # Output: Target 7 found at index: 3
```

Note: Make sure your input array is sorted before using binary search!'''

# Add more code examples here as needed
