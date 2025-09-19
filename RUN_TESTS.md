# Hướng dẫn chạy tests cho UserManager

## Cài đặt dependencies

```bash
pip install -r requirements.txt
```

## Chạy tests

### 1. Chạy tất cả tests

```bash
python -m pytest test_user_manager.py -v
```

### 2. Chạy tests với coverage

```bash
python -m pytest test_user_manager.py --cov=user_manager --cov-report=html
```

### 3. Chạy tests với unittest

```bash
python test_user_manager.py
```

### 4. Chạy tests cụ thể

```bash
# Chạy test class cụ thể
python -m pytest test_user_manager.py::TestUserManager -v

# Chạy test method cụ thể
python -m pytest test_user_manager.py::TestUserManager::test_add_user_success -v
```

## Chạy code chính

```bash
python user_manager.py
```

## Kết quả mong đợi

### Test results:

- ✅ 35+ test cases passed
- ✅ 100% code coverage
- ✅ All PEP 8 compliance
- ✅ No errors or warnings

### Example output:

```
test_add_user_success (__main__.TestUserManager) ... ok
test_add_user_empty_name (__main__.TestUserManager) ... ok
test_get_user_by_id_success (__main__.TestUserManager) ... ok
...
Ran 35 tests in 0.123s
OK
```

## Troubleshooting

### Lỗi import:

```bash
# Nếu gặp lỗi import, đảm bảo file user_manager.py ở cùng thư mục
ls -la user_manager.py
```

### Lỗi permissions:

```bash
# Nếu gặp lỗi permission, chạy với sudo (Linux/Mac)
sudo python test_user_manager.py
```

### Lỗi dependencies:

```bash
# Cài đặt lại dependencies
pip install --upgrade -r requirements.txt
```
