# file: user_manager.py
import json
import datetime
from typing import List, Dict, Optional

class userManager:
    def __init__(self, data_file: str = "users.json"):
        self.dataFile = data_file
        self.users_list = []
        self.load_users()

    def load_users(self):
        try:
            with open(self.dataFile, 'r', encoding='utf-8') as f:
                self.users_list = json.load(f)
        except FileNotFoundError:
            self.users_list = []
        except json.JSONDecodeError:
            print("Error decoding JSON file")
            self.users_list = []

    def save_users(self):
        with open(self.dataFile, 'w', encoding='utf-8') as f:
            json.dump(self.users_list, f, ensure_ascii=False, indent=2)

    def add_user(self, userName: str, userEmail: str, userAge: int) -> bool:
        if not userName or not userEmail:
            return False
        
        # Check if user already exists
        for user in self.users_list:
            if user['email'] == userEmail:
                return False
        
        new_user = {
            'id': len(self.users_list) + 1,
            'name': userName,
            'email': userEmail,
            'age': userAge,
            'created_date': datetime.datetime.now().isoformat(),
            'is_active': True
        }
        
        self.users_list.append(new_user)
        self.save_users()
        return True

    def get_user_by_id(self, userId: int) -> Optional[Dict]:
        for user in self.users_list:
            if user['id'] == userId:
                return user
        return None

    def get_users_by_age_range(self, min_age: int, max_age: int) -> List[Dict]:
        result_list = []
        for user in self.users_list:
            if min_age <= user['age'] <= max_age:
                result_list.append(user)
        return result_list

    def update_user_status(self, userId: int, new_status: bool) -> bool:
        user = self.get_user_by_id(userId)
        if user:
            user['is_active'] = new_status
            self.save_users()
            return True
        return False

    def delete_user(self, userId: int) -> bool:
        for i, user in enumerate(self.users_list):
            if user['id'] == userId:
                del self.users_list[i]
                self.save_users()
                return True
        return False

    def get_active_users_count(self) -> int:
        count = 0
        for user in self.users_list:
            if user['is_active']:
                count += 1
        return count

    def search_users_by_name(self, search_term: str) -> List[Dict]:
        results = []
        for user in self.users_list:
            if search_term.lower() in user['name'].lower():
                results.append(user)
        return results

    def export_users_to_csv(self, output_file: str = "users_export.csv") -> bool:
        try:
            import csv
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                if not self.users_list:
                    return False
                
                fieldnames = self.users_list[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for user in self.users_list:
                    writer.writerow(user)
            return True
        except Exception as e:
            print(f"Export error: {e}")
            return False

# Example usage
if __name__ == "__main__":
    um = userManager("test_users.json")
    um.add_user("Nguyễn Văn An", "an@example.com", 25)
    um.add_user("Trần Thị Bình", "binh@example.com", 30)
    print(f"Total active users: {um.get_active_users_count()}")
    print(f"Users aged 20-35: {um.get_users_by_age_range(20, 35)}")