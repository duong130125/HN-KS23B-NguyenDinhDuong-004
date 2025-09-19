"""
Unit tests for list_ops.py module.
Tests both normal cases and edge cases for the remove_duplicates function.
"""

import pytest
from list_ops import remove_duplicates, remove_duplicates_simple


class TestRemoveDuplicates:
    """Test cases for remove_duplicates function."""
    
    def test_basic_duplicates(self):
        """Test basic duplicate removal functionality."""
        input_list = [1, 2, 2, 3, 4, 4, 5]
        expected = [1, 2, 3, 4, 5]
        result = remove_duplicates(input_list)
        assert result == expected
        assert result is not input_list  # Should return new list
    
    def test_no_duplicates(self):
        """Test list with no duplicates."""
        input_list = [1, 2, 3, 4, 5]
        expected = [1, 2, 3, 4, 5]
        result = remove_duplicates(input_list)
        assert result == expected
    
    def test_all_duplicates(self):
        """Test list with all same elements."""
        input_list = [1, 1, 1, 1, 1]
        expected = [1]
        result = remove_duplicates(input_list)
        assert result == expected
    
    def test_empty_list(self):
        """Test empty list edge case."""
        result = remove_duplicates([])
        assert result == []
    
    def test_single_element(self):
        """Test list with single element."""
        result = remove_duplicates([42])
        assert result == [42]
    
    def test_string_duplicates(self):
        """Test with string elements."""
        input_list = ["a", "b", "b", "c", "a", "d"]
        expected = ["a", "b", "c", "d"]
        result = remove_duplicates(input_list)
        assert result == expected
    
    def test_mixed_types(self):
        """Test with mixed data types."""
        input_list = [1, "a", 2, "a", 3, 1]
        expected = [1, "a", 2, 3]
        result = remove_duplicates(input_list)
        assert result == expected
    
    def test_none_values(self):
        """Test with None values."""
        input_list = [1, None, 2, None, 3]
        expected = [1, None, 2, 3]
        result = remove_duplicates(input_list)
        assert result == expected
    
    def test_float_duplicates(self):
        """Test with float values."""
        input_list = [1.0, 2.0, 2.0, 3.0, 1.0]
        expected = [1.0, 2.0, 3.0]
        result = remove_duplicates(input_list)
        assert result == expected
    
    def test_preserve_order(self):
        """Test that order is preserved."""
        input_list = [3, 1, 2, 1, 3, 2]
        expected = [3, 1, 2]
        result = remove_duplicates(input_list)
        assert result == expected
    
    def test_nested_lists(self):
        """Test with nested lists (unhashable types)."""
        input_list = [[1, 2], [3, 4], [1, 2], [5, 6]]
        expected = [[1, 2], [3, 4], [5, 6]]
        result = remove_duplicates(input_list)
        assert result == expected
    
    def test_dictionaries(self):
        """Test with dictionaries (unhashable types)."""
        input_list = [{"a": 1}, {"b": 2}, {"a": 1}, {"c": 3}]
        expected = [{"a": 1}, {"b": 2}, {"c": 3}]
        result = remove_duplicates(input_list)
        assert result == expected
    
    def test_none_input(self):
        """Test error handling for None input."""
        with pytest.raises(ValueError, match="Input list cannot be None"):
            remove_duplicates(None)
    
    def test_non_list_input(self):
        """Test error handling for non-list input."""
        with pytest.raises(TypeError, match="Expected list, got str"):
            remove_duplicates("not a list")
        
        with pytest.raises(TypeError, match="Expected list, got int"):
            remove_duplicates(42)
    
    def test_large_list_performance(self):
        """Test performance with larger list."""
        # Create a list with many duplicates
        large_list = list(range(1000)) * 2  # 2000 elements with 1000 duplicates
        result = remove_duplicates(large_list)
        assert len(result) == 1000
        assert result == list(range(1000))


class TestRemoveDuplicatesSimple:
    """Test cases for remove_duplicates_simple function."""
    
    def test_basic_functionality(self):
        """Test basic functionality of simple version."""
        input_list = [1, 2, 2, 3, 4, 4, 5]
        expected = [1, 2, 3, 4, 5]
        result = remove_duplicates_simple(input_list)
        assert result == expected
    
    def test_hashable_types_only(self):
        """Test that simple version works with hashable types."""
        input_list = [1, "a", (1, 2), 1, "a", (1, 2)]
        expected = [1, "a", (1, 2)]
        result = remove_duplicates_simple(input_list)
        assert result == expected
    
    def test_error_handling(self):
        """Test error handling in simple version."""
        with pytest.raises(ValueError):
            remove_duplicates_simple(None)
        
        with pytest.raises(TypeError):
            remove_duplicates_simple("not a list")


class TestEdgeCases:
    """Test various edge cases and corner conditions."""
    
    def test_boolean_values(self):
        """Test with boolean values."""
        input_list = [True, False, True, False, True]
        expected = [True, False]
        result = remove_duplicates(input_list)
        assert result == expected
    
    def test_zero_and_empty_string(self):
        """Test with zero and empty string."""
        input_list = [0, "", 0, "", 1]
        expected = [0, "", 1]
        result = remove_duplicates(input_list)
        assert result == expected
    
    def test_negative_numbers(self):
        """Test with negative numbers."""
        input_list = [-1, -2, -1, 0, -2, 1]
        expected = [-1, -2, 0, 1]
        result = remove_duplicates(input_list)
        assert result == expected
    
    def test_very_large_numbers(self):
        """Test with very large numbers."""
        input_list = [10**10, 10**10, 10**11]
        expected = [10**10, 10**11]
        result = remove_duplicates(input_list)
        assert result == expected


# Performance test (optional, can be run separately)
def test_performance_comparison():
    """Compare performance between original O(n²) and optimized O(n) algorithms."""
    import time
    
    # Create test data
    test_data = list(range(1000)) * 10  # 10,000 elements with 1000 unique
    
    # Test optimized version
    start_time = time.time()
    result_optimized = remove_duplicates(test_data)
    optimized_time = time.time() - start_time
    
    # Verify correctness
    assert len(result_optimized) == 1000
    assert result_optimized == list(range(1000))
    
    print(f"Optimized version took {optimized_time:.4f} seconds")
    print(f"Result length: {len(result_optimized)}")


if __name__ == "__main__":
    # Run performance test if executed directly
    test_performance_comparison()
