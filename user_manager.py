"""
User Management Module.

This module provides a comprehensive user management system with CRUD operations,
search functionality, and data export capabilities. It follows PEP 8 standards
and includes proper type hints and documentation.

Author: Refactored for PEP 8 compliance
Version: 2.0.0
"""

import csv
import json
from datetime import datetime
from typing import Dict, List, Optional


class UserManager:
    """
    A comprehensive user management system.
    
    This class provides methods for managing user data including adding, updating,
    deleting, and searching users. Data is persisted in JSON format.
    
    Attributes:
        data_file (str): Path to the JSON data file
        users_list (List[Dict]): List of user dictionaries
    """
    
    def __init__(self, data_file: str = "users.json") -> None:
        """
        Initialize the UserManager.
        
        Args:
            data_file (str): Path to the JSON file for data persistence.
                           Defaults to "users.json".
        """
        self.data_file = data_file
        self.users_list: List[Dict] = []
        self.load_users()
    
    def load_users(self) -> None:
        """
        Load users from the JSON data file.
        
        Creates an empty list if the file doesn't exist or contains invalid JSON.
        """
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                self.users_list = json.load(file)
        except FileNotFoundError:
            self.users_list = []
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in data file")
            self.users_list = []
        except Exception as e:
            print(f"Error loading users: {e}")
            self.users_list = []
    
    def save_users(self) -> None:
        """
        Save users to the JSON data file.
        
        Raises:
            IOError: If unable to write to the file
        """
        try:
            with open(self.data_file, 'w', encoding='utf-8') as file:
                json.dump(self.users_list, file, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Error saving users: {e}")
            raise
    
    def add_user(self, user_name: str, user_email: str, user_age: int) -> bool:
        """
        Add a new user to the system.
        
        Args:
            user_name (str): The user's name
            user_email (str): The user's email address (must be unique)
            user_age (int): The user's age
            
        Returns:
            bool: True if user was added successfully, False otherwise
            
        Raises:
            ValueError: If input parameters are invalid
        """
        if not user_name or not user_email:
            return False
        
        if not isinstance(user_age, int) or user_age < 0:
            return False
        
        # Check if user already exists
        for user in self.users_list:
            if user['email'] == user_email:
                return False
        
        new_user = {
            'id': len(self.users_list) + 1,
            'name': user_name,
            'email': user_email,
            'age': user_age,
            'created_date': datetime.now().isoformat(),
            'is_active': True
        }
        
        self.users_list.append(new_user)
        self.save_users()
        return True
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """
        Retrieve a user by their ID.
        
        Args:
            user_id (int): The user's ID
            
        Returns:
            Optional[Dict]: User dictionary if found, None otherwise
        """
        for user in self.users_list:
            if user['id'] == user_id:
                return user
        return None
    
    def get_users_by_age_range(self, min_age: int, max_age: int) -> List[Dict]:
        """
        Get users within a specific age range.
        
        Args:
            min_age (int): Minimum age (inclusive)
            max_age (int): Maximum age (inclusive)
            
        Returns:
            List[Dict]: List of users within the age range
        """
        if min_age > max_age:
            return []
        
        result_list = []
        for user in self.users_list:
            if min_age <= user['age'] <= max_age:
                result_list.append(user)
        return result_list
    
    def update_user_status(self, user_id: int, new_status: bool) -> bool:
        """
        Update a user's active status.
        
        Args:
            user_id (int): The user's ID
            new_status (bool): New active status
            
        Returns:
            bool: True if update was successful, False otherwise
        """
        user = self.get_user_by_id(user_id)
        if user:
            user['is_active'] = new_status
            self.save_users()
            return True
        return False
    
    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user from the system.
        
        Args:
            user_id (int): The user's ID
            
        Returns:
            bool: True if user was deleted, False if not found
        """
        for i, user in enumerate(self.users_list):
            if user['id'] == user_id:
                del self.users_list[i]
                self.save_users()
                return True
        return False
    
    def get_active_users_count(self) -> int:
        """
        Get the count of active users.
        
        Returns:
            int: Number of active users
        """
        return sum(1 for user in self.users_list if user['is_active'])
    
    def search_users_by_name(self, search_term: str) -> List[Dict]:
        """
        Search users by name (case-insensitive).
        
        Args:
            search_term (str): The search term
            
        Returns:
            List[Dict]: List of users matching the search term
        """
        if not search_term:
            return []
        
        results = []
        search_lower = search_term.lower()
        
        for user in self.users_list:
            if search_lower in user['name'].lower():
                results.append(user)
        return results
    
    def export_users_to_csv(self, output_file: str = "users_export.csv") -> bool:
        """
        Export users to a CSV file.
        
        Args:
            output_file (str): Path to the output CSV file
            
        Returns:
            bool: True if export was successful, False otherwise
        """
        if not self.users_list:
            return False
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = self.users_list[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for user in self.users_list:
                    writer.writerow(user)
            return True
        except Exception as e:
            print(f"Export error: {e}")
            return False
    
    def get_all_users(self) -> List[Dict]:
        """
        Get all users in the system.
        
        Returns:
            List[Dict]: List of all users
        """
        return self.users_list.copy()
    
    def get_user_count(self) -> int:
        """
        Get the total number of users.
        
        Returns:
            int: Total number of users
        """
        return len(self.users_list)
    
    def clear_all_users(self) -> None:
        """
        Clear all users from the system.
        
        Warning: This action cannot be undone!
        """
        self.users_list = []
        self.save_users()


def main() -> None:
    """
    Example usage of the UserManager class.
    """
    # Initialize the user manager
    user_manager = UserManager("test_users.json")
    
    # Add some users
    user_manager.add_user("Nguyễn Văn An", "an@example.com", 25)
    user_manager.add_user("Trần Thị Bình", "binh@example.com", 30)
    user_manager.add_user("Lê Văn Cường", "cuong@example.com", 28)
    
    # Display statistics
    print(f"Total users: {user_manager.get_user_count()}")
    print(f"Active users: {user_manager.get_active_users_count()}")
    
    # Search and filter
    young_users = user_manager.get_users_by_age_range(20, 35)
    print(f"Users aged 20-35: {len(young_users)}")
    
    # Search by name
    search_results = user_manager.search_users_by_name("Nguyễn")
    print(f"Users with 'Nguyễn' in name: {len(search_results)}")
    
    # Export to CSV
    if user_manager.export_users_to_csv("users_backup.csv"):
        print("Users exported to CSV successfully")


if __name__ == "__main__":
    main()