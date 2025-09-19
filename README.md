# List Operations - Fixed Version

## Cài đặt dependencies

```bash
pip install -r requirements.txt
```

## Chạy tests

```bash
# Chạy tất cả tests
pytest test_list_ops.py -v

# Chạy tests với coverage
pytest test_list_ops.py --cov=list_ops

# Chạy test performance
python test_list_ops.py
```

## Chạy code chính

```bash
python list_ops.py
```

## Breaking Changes và Migration Guide

### Thay đổi API:

1. **Thêm type hints**: Function signature thay đổi từ `remove_duplicates(my_list)` thành `remove_duplicates(my_list: List[T]) -> List[T]`

2. **Thêm error handling**:

   - Input `None` sẽ raise `ValueError` thay vì crash
   - Non-list input sẽ raise `TypeError`

3. **Thêm function mới**: `remove_duplicates_simple()` cho hashable types

### Migration Guide:

**Trước:**

```python
result = remove_duplicates([1, 2, 2, 3])
```

**Sau:**

```python
# Không cần thay đổi gì - backward compatible
result = remove_duplicates([1, 2, 2, 3])

# Hoặc sử dụng simple version cho performance tốt hơn
result = remove_duplicates_simple([1, 2, 2, 3])
```

**Xử lý error cases:**

```python
# Trước: có thể crash
result = remove_duplicates(None)

# Sau: handle exceptions
try:
    result = remove_duplicates(None)
except ValueError as e:
    print(f"Error: {e}")
```

## Performance Improvements

- **Trước**: O(n²) - chậm với list lớn
- **Sau**: O(n) - nhanh hơn đáng kể với list lớn

## Dependencies

- Python 3.7+
- pytest (for testing)
- typing (built-in)
