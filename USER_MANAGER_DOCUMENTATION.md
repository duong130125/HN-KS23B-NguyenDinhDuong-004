# UserManager Module - Hướng dẫn sử dụng chi tiết

## 1. Mô tả tổng quan

**UserManager** là một module Python được thiết kế để quản lý thông tin người dùng một cách hiệu quả. Module này cung cấp các chức năng cơ bản để:

- Thêm, sửa, xóa người dùng
- Tìm kiếm và lọc người dùng theo các tiêu chí khác nhau
- Quản lý trạng thái hoạt động của người dùng
- Xuất dữ liệu người dùng ra file CSV
- Lưu trữ dữ liệu dưới dạng JSON

### Chức năng chính:
- ✅ Quản lý CRUD (Create, Read, Update, Delete) cho người dùng
- ✅ Tìm kiếm người dùng theo tên
- ✅ Lọc người dùng theo độ tuổi
- ✅ Quản lý trạng thái hoạt động
- ✅ Xuất dữ liệu ra CSV
- ✅ Lưu trữ dữ liệu persistent

## 2. Hướng dẫn cài đặt

### Dependencies cần thiết:
```python
# Built-in modules (không cần cài đặt thêm)
import json
import datetime
import csv
from typing import List, Dict, Optional
```

### Cài đặt:
```bash
# Không cần cài đặt thêm dependencies
# Chỉ cần Python 3.7+ với typing support
```

### Cấu trúc file:
```
project/
├── user_manager.py          # Module chính
├── users.json              # File lưu trữ dữ liệu (tự động tạo)
└── users_export.csv        # File xuất dữ liệu (tùy chọn)
```

## 3. API Documentation

### Class: `UserManager`

#### Constructor
```python
def __init__(self, data_file: str = "users.json") -> None
```

**Tham số:**
- `data_file` (str): Đường dẫn đến file JSON lưu trữ dữ liệu. Mặc định: "users.json"

**Ví dụ:**
```python
# Sử dụng file mặc định
manager = UserManager()

# Sử dụng file tùy chỉnh
manager = UserManager("my_users.json")
```

#### Methods

### `add_user(user_name: str, user_email: str, user_age: int) -> bool`

Thêm người dùng mới vào hệ thống.

**Tham số:**
- `user_name` (str): Tên người dùng (bắt buộc)
- `user_email` (str): Email người dùng (bắt buộc, phải unique)
- `user_age` (int): Tuổi người dùng

**Giá trị trả về:**
- `bool`: True nếu thêm thành công, False nếu thất bại

**Ví dụ:**
```python
success = manager.add_user("Nguyễn Văn An", "an@example.com", 25)
if success:
    print("Thêm người dùng thành công!")
else:
    print("Thêm người dùng thất bại!")
```

**Trường hợp ngoại lệ:**
- Trả về False nếu tên hoặc email trống
- Trả về False nếu email đã tồn tại

### `get_user_by_id(user_id: int) -> Optional[Dict]`

Lấy thông tin người dùng theo ID.

**Tham số:**
- `user_id` (int): ID của người dùng

**Giá trị trả về:**
- `Optional[Dict]`: Thông tin người dùng hoặc None nếu không tìm thấy

**Ví dụ:**
```python
user = manager.get_user_by_id(1)
if user:
    print(f"Tên: {user['name']}, Email: {user['email']}")
else:
    print("Không tìm thấy người dùng!")
```

### `get_users_by_age_range(min_age: int, max_age: int) -> List[Dict]`

Lấy danh sách người dùng trong khoảng tuổi nhất định.

**Tham số:**
- `min_age` (int): Tuổi tối thiểu
- `max_age` (int): Tuổi tối đa

**Giá trị trả về:**
- `List[Dict]`: Danh sách người dùng trong khoảng tuổi

**Ví dụ:**
```python
young_users = manager.get_users_by_age_range(18, 30)
print(f"Có {len(young_users)} người dùng từ 18-30 tuổi")
```

### `update_user_status(user_id: int, new_status: bool) -> bool`

Cập nhật trạng thái hoạt động của người dùng.

**Tham số:**
- `user_id` (int): ID của người dùng
- `new_status` (bool): Trạng thái mới (True = hoạt động, False = không hoạt động)

**Giá trị trả về:**
- `bool`: True nếu cập nhật thành công, False nếu không tìm thấy người dùng

**Ví dụ:**
```python
# Vô hiệu hóa người dùng
success = manager.update_user_status(1, False)
if success:
    print("Đã vô hiệu hóa người dùng!")
```

### `delete_user(user_id: int) -> bool`

Xóa người dùng khỏi hệ thống.

**Tham số:**
- `user_id` (int): ID của người dùng cần xóa

**Giá trị trả về:**
- `bool`: True nếu xóa thành công, False nếu không tìm thấy

**Ví dụ:**
```python
success = manager.delete_user(1)
if success:
    print("Đã xóa người dùng!")
```

### `get_active_users_count() -> int`

Đếm số lượng người dùng đang hoạt động.

**Giá trị trả về:**
- `int`: Số lượng người dùng đang hoạt động

**Ví dụ:**
```python
active_count = manager.get_active_users_count()
print(f"Có {active_count} người dùng đang hoạt động")
```

### `search_users_by_name(search_term: str) -> List[Dict]`

Tìm kiếm người dùng theo tên (không phân biệt hoa thường).

**Tham số:**
- `search_term` (str): Từ khóa tìm kiếm

**Giá trị trả về:**
- `List[Dict]`: Danh sách người dùng khớp với từ khóa

**Ví dụ:**
```python
results = manager.search_users_by_name("Nguyễn")
print(f"Tìm thấy {len(results)} người dùng có tên chứa 'Nguyễn'")
```

### `export_users_to_csv(output_file: str = "users_export.csv") -> bool`

Xuất danh sách người dùng ra file CSV.

**Tham số:**
- `output_file` (str): Tên file CSV xuất ra. Mặc định: "users_export.csv"

**Giá trị trả về:**
- `bool`: True nếu xuất thành công, False nếu có lỗi

**Ví dụ:**
```python
success = manager.export_users_to_csv("backup_users.csv")
if success:
    print("Xuất dữ liệu thành công!")
```

## 4. Ví dụ sử dụng thực tế

### Ví dụ cơ bản - Quản lý người dùng đơn giản

```python
from user_manager import UserManager

# Khởi tạo manager
manager = UserManager("my_users.json")

# Thêm người dùng
manager.add_user("Nguyễn Văn An", "an@example.com", 25)
manager.add_user("Trần Thị Bình", "binh@example.com", 30)
manager.add_user("Lê Văn Cường", "cuong@example.com", 28)

# Lấy thông tin người dùng
user = manager.get_user_by_id(1)
print(f"Người dùng: {user['name']} - {user['email']}")

# Tìm kiếm người dùng
results = manager.search_users_by_name("Nguyễn")
print(f"Tìm thấy {len(results)} người dùng")

# Đếm người dùng hoạt động
active_count = manager.get_active_users_count()
print(f"Có {active_count} người dùng đang hoạt động")
```

### Ví dụ nâng cao - Hệ thống quản lý nhân viên

```python
from user_manager import UserManager
import datetime

class EmployeeManager:
    def __init__(self):
        self.user_manager = UserManager("employees.json")
    
    def add_employee(self, name, email, age, department):
        """Thêm nhân viên mới"""
        success = self.user_manager.add_user(name, email, age)
        if success:
            # Cập nhật thông tin bổ sung
            user = self.user_manager.get_user_by_id(
                len(self.user_manager.users_list)
            )
            user['department'] = department
            user['hire_date'] = datetime.datetime.now().isoformat()
            self.user_manager.save_users()
        return success
    
    def get_employees_by_department(self, department):
        """Lấy nhân viên theo phòng ban"""
        employees = []
        for user in self.user_manager.users_list:
            if user.get('department') == department:
                employees.append(user)
        return employees
    
    def generate_employee_report(self):
        """Tạo báo cáo nhân viên"""
        total = len(self.user_manager.users_list)
        active = self.user_manager.get_active_users_count()
        
        print(f"=== BÁO CÁO NHÂN VIÊN ===")
        print(f"Tổng số nhân viên: {total}")
        print(f"Nhân viên đang hoạt động: {active}")
        print(f"Nhân viên không hoạt động: {total - active}")
        
        # Xuất báo cáo ra CSV
        self.user_manager.export_users_to_csv("employee_report.csv")

# Sử dụng
emp_manager = EmployeeManager()
emp_manager.add_employee("Nguyễn Văn An", "an@company.com", 25, "IT")
emp_manager.add_employee("Trần Thị Bình", "binh@company.com", 30, "HR")
emp_manager.generate_employee_report()
```

### Ví dụ xử lý lỗi và validation

```python
from user_manager import UserManager

def safe_add_user(manager, name, email, age):
    """Thêm người dùng với validation"""
    try:
        # Validation
        if not name or not email:
            print("Tên và email không được để trống!")
            return False
        
        if age < 0 or age > 150:
            print("Tuổi không hợp lệ!")
            return False
        
        # Kiểm tra email đã tồn tại
        for user in manager.users_list:
            if user['email'] == email:
                print("Email đã tồn tại!")
                return False
        
        # Thêm người dùng
        success = manager.add_user(name, email, age)
        if success:
            print(f"Đã thêm người dùng: {name}")
        else:
            print("Thêm người dùng thất bại!")
        
        return success
        
    except Exception as e:
        print(f"Lỗi: {e}")
        return False

# Sử dụng
manager = UserManager()
safe_add_user(manager, "Nguyễn Văn An", "an@example.com", 25)
```

## 5. Best Practices

### 5.1 Quản lý dữ liệu
- **Backup định kỳ**: Luôn backup file JSON trước khi thực hiện thay đổi lớn
- **Validation**: Kiểm tra dữ liệu đầu vào trước khi thêm/sửa
- **Error handling**: Luôn xử lý exceptions khi làm việc với file

### 5.2 Performance
- **Lazy loading**: Chỉ load dữ liệu khi cần thiết
- **Batch operations**: Thực hiện nhiều thao tác cùng lúc để giảm I/O
- **Indexing**: Sử dụng dictionary để tìm kiếm nhanh hơn

### 5.3 Security
- **Input sanitization**: Làm sạch dữ liệu đầu vào
- **File permissions**: Đặt quyền truy cập phù hợp cho file dữ liệu
- **Data encryption**: Mã hóa dữ liệu nhạy cảm

### 5.4 Code organization
```python
# Tốt: Tách biệt logic
class UserService:
    def __init__(self):
        self.manager = UserManager()
    
    def create_user(self, user_data):
        # Business logic here
        pass

# Tránh: Trộn lẫn logic
def add_user_with_validation_and_email_sending(name, email, age):
    # Quá nhiều trách nhiệm trong một function
    pass
```

## 6. Troubleshooting

### 6.1 Lỗi thường gặp

#### Lỗi: "FileNotFoundError"
```python
# Nguyên nhân: File JSON không tồn tại
# Giải pháp: Module tự động tạo file mới
manager = UserManager("new_file.json")  # Sẽ tạo file mới
```

#### Lỗi: "json.JSONDecodeError"
```python
# Nguyên nhân: File JSON bị hỏng
# Giải pháp: Backup và tạo lại file
import shutil
shutil.copy("users.json", "users_backup.json")
# Xóa file hỏng và tạo lại
```

#### Lỗi: "Permission denied"
```python
# Nguyên nhân: Không có quyền ghi file
# Giải pháp: Kiểm tra quyền file
import os
print(f"File writable: {os.access('users.json', os.W_OK)}")
```

### 6.2 Debug và monitoring

```python
def debug_user_manager(manager):
    """Debug function để kiểm tra trạng thái"""
    print(f"Total users: {len(manager.users_list)}")
    print(f"Active users: {manager.get_active_users_count()}")
    
    # Kiểm tra dữ liệu
    for i, user in enumerate(manager.users_list):
        print(f"User {i+1}: {user['name']} - {user['email']} - Active: {user['is_active']}")

# Sử dụng
manager = UserManager()
debug_user_manager(manager)
```

### 6.3 Performance issues

```python
# Vấn đề: Tìm kiếm chậm với danh sách lớn
# Giải pháp: Sử dụng dictionary để index
class OptimizedUserManager(UserManager):
    def __init__(self, data_file="users.json"):
        super().__init__(data_file)
        self._email_index = {}
        self._name_index = {}
        self._build_indexes()
    
    def _build_indexes(self):
        """Xây dựng index để tìm kiếm nhanh"""
        for user in self.users_list:
            self._email_index[user['email']] = user['id']
            self._name_index[user['name'].lower()] = user['id']
    
    def get_user_by_email(self, email):
        """Tìm kiếm theo email - O(1)"""
        user_id = self._email_index.get(email)
        if user_id:
            return self.get_user_by_id(user_id)
        return None
```

### 6.4 Data recovery

```python
def recover_from_backup(backup_file="users_backup.json"):
    """Khôi phục dữ liệu từ backup"""
    try:
        import shutil
        shutil.copy(backup_file, "users.json")
        manager = UserManager()
        print("Khôi phục dữ liệu thành công!")
        return manager
    except Exception as e:
        print(f"Lỗi khôi phục: {e}")
        return None
```

## 7. Kết luận

UserManager module cung cấp một giải pháp đơn giản và hiệu quả để quản lý dữ liệu người dùng. Với API đơn giản và dễ sử dụng, module này phù hợp cho các ứng dụng nhỏ đến trung bình.

**Ưu điểm:**
- API đơn giản, dễ sử dụng
- Không cần database phức tạp
- Hỗ trợ đầy đủ CRUD operations
- Có thể mở rộng dễ dàng

**Hạn chế:**
- Không phù hợp với dữ liệu lớn
- Không có transaction support
- Thiếu các tính năng advanced như pagination, sorting

**Khuyến nghị:**
- Sử dụng cho prototype hoặc ứng dụng nhỏ
- Cân nhắc chuyển sang database thực sự khi dữ liệu lớn
- Luôn backup dữ liệu quan trọng
