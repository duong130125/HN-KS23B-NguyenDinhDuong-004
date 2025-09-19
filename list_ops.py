"""
List operations module with optimized duplicate removal function.
Fixed performance issues and added proper error handling.
"""

from typing import List, TypeVar, Optional, Union

T = TypeVar('T')


def remove_duplicates(my_list: List[T]) -> List[T]:
    """
    Remove duplicates from a list while preserving order.
    
    Performance improvement: O(n) instead of O(n²) using set for lookups.
    Added type hints and proper error handling.
    
    Args:
        my_list: Input list that may contain duplicates
        
    Returns:
        List with duplicates removed, preserving original order
        
    Raises:
        TypeError: If input is not a list
        ValueError: If input list is None
    """
    # Input validation
    if my_list is None:
        raise ValueError("Input list cannot be None")
    if not isinstance(my_list, list):
        raise TypeError(f"Expected list, got {type(my_list).__name__}")
    
    # Handle empty list edge case
    if not my_list:
        return []
    
    # Optimized O(n) algorithm using set for O(1) lookups
    seen = set()
    unique_items = []
    
    for item in my_list:
        # Handle unhashable types (like lists, dicts) by converting to tuple
        if isinstance(item, (list, dict)):
            # Convert to tuple for hashing, but this changes the item type
            # Better to use a different approach for complex objects
            item_key = tuple(item) if isinstance(item, list) else tuple(sorted(item.items()))
        else:
            item_key = item
            
        if item_key not in seen:
            seen.add(item_key)
            unique_items.append(item)
    
    return unique_items


def remove_duplicates_simple(my_list: List[T]) -> List[T]:
    """
    Simplified version for hashable types only.
    Use this for basic types (int, str, float, tuple).
    """
    if my_list is None:
        raise ValueError("Input list cannot be None")
    if not isinstance(my_list, list):
        raise TypeError(f"Expected list, got {type(my_list).__name__}")
    
    if not my_list:
        return []
    
    seen = set()
    unique_items = []
    
    for item in my_list:
        if item not in seen:
            seen.add(item)
            unique_items.append(item)
    
    return unique_items


# Example usage (only runs when script is executed directly)
if __name__ == "__main__":
    # Test cases
    test_list = [1, 2, 2, 3, 4, 4, 5]
    result = remove_duplicates(test_list)
    print(f"Original: {test_list}")
    print(f"Unique: {result}")
    
    # Test edge cases
    print(f"Empty list: {remove_duplicates([])}")
    print(f"Single item: {remove_duplicates([42])}")
    print(f"All same: {remove_duplicates([1, 1, 1, 1])}")
