"""
Unit tests for UserManager class.

This module contains comprehensive tests for all UserManager functionality
including CRUD operations, search, filtering, and edge cases.

Author: Test suite for PEP 8 compliant UserManager
Version: 1.0.0
"""

import json
import os
import tempfile
import unittest
from unittest.mock import patch, mock_open

from user_manager import UserManager


class TestUserManager(unittest.TestCase):
    """Test cases for UserManager class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.temp_file_path = self.temp_file.name
        
        # Initialize UserManager with temporary file
        self.user_manager = UserManager(self.temp_file_path)
    
    def tearDown(self):
        """Clean up after each test method."""
        # Remove temporary file
        if os.path.exists(self.temp_file_path):
            os.unlink(self.temp_file_path)
    
    def test_init_with_default_file(self):
        """Test initialization with default file."""
        manager = UserManager()
        self.assertEqual(manager.data_file, "users.json")
        self.assertEqual(manager.users_list, [])
    
    def test_init_with_custom_file(self):
        """Test initialization with custom file."""
        manager = UserManager("custom.json")
        self.assertEqual(manager.data_file, "custom.json")
        self.assertEqual(manager.users_list, [])
    
    def test_load_users_empty_file(self):
        """Test loading users from empty file."""
        # Create empty file
        with open(self.temp_file_path, 'w') as f:
            f.write('[]')
        
        manager = UserManager(self.temp_file_path)
        self.assertEqual(manager.users_list, [])
    
    def test_load_users_with_data(self):
        """Test loading users from file with data."""
        test_data = [
            {"id": 1, "name": "Test User", "email": "test@example.com", 
             "age": 25, "created_date": "2023-01-01", "is_active": True}
        ]
        
        with open(self.temp_file_path, 'w') as f:
            json.dump(test_data, f)
        
        manager = UserManager(self.temp_file_path)
        self.assertEqual(len(manager.users_list), 1)
        self.assertEqual(manager.users_list[0]["name"], "Test User")
    
    def test_load_users_file_not_found(self):
        """Test loading users when file doesn't exist."""
        non_existent_file = "non_existent.json"
        manager = UserManager(non_existent_file)
        self.assertEqual(manager.users_list, [])
    
    def test_load_users_invalid_json(self):
        """Test loading users with invalid JSON."""
        with open(self.temp_file_path, 'w') as f:
            f.write('invalid json content')
        
        manager = UserManager(self.temp_file_path)
        self.assertEqual(manager.users_list, [])
    
    def test_save_users(self):
        """Test saving users to file."""
        test_user = {
            "id": 1,
            "name": "Test User",
            "email": "test@example.com",
            "age": 25,
            "created_date": "2023-01-01",
            "is_active": True
        }
        
        self.user_manager.users_list = [test_user]
        self.user_manager.save_users()
        
        # Verify file was created and contains correct data
        with open(self.temp_file_path, 'r') as f:
            saved_data = json.load(f)
        
        self.assertEqual(len(saved_data), 1)
        self.assertEqual(saved_data[0]["name"], "Test User")
    
    def test_add_user_success(self):
        """Test adding a user successfully."""
        result = self.user_manager.add_user("John Doe", "john@example.com", 30)
        
        self.assertTrue(result)
        self.assertEqual(len(self.user_manager.users_list), 1)
        self.assertEqual(self.user_manager.users_list[0]["name"], "John Doe")
        self.assertEqual(self.user_manager.users_list[0]["email"], "john@example.com")
        self.assertEqual(self.user_manager.users_list[0]["age"], 30)
        self.assertTrue(self.user_manager.users_list[0]["is_active"])
        self.assertIsNotNone(self.user_manager.users_list[0]["created_date"])
    
    def test_add_user_empty_name(self):
        """Test adding user with empty name."""
        result = self.user_manager.add_user("", "john@example.com", 30)
        self.assertFalse(result)
        self.assertEqual(len(self.user_manager.users_list), 0)
    
    def test_add_user_empty_email(self):
        """Test adding user with empty email."""
        result = self.user_manager.add_user("John Doe", "", 30)
        self.assertFalse(result)
        self.assertEqual(len(self.user_manager.users_list), 0)
    
    def test_add_user_negative_age(self):
        """Test adding user with negative age."""
        result = self.user_manager.add_user("John Doe", "john@example.com", -5)
        self.assertFalse(result)
        self.assertEqual(len(self.user_manager.users_list), 0)
    
    def test_add_user_duplicate_email(self):
        """Test adding user with duplicate email."""
        # Add first user
        self.user_manager.add_user("John Doe", "john@example.com", 30)
        
        # Try to add second user with same email
        result = self.user_manager.add_user("Jane Doe", "john@example.com", 25)
        self.assertFalse(result)
        self.assertEqual(len(self.user_manager.users_list), 1)
    
    def test_get_user_by_id_success(self):
        """Test getting user by ID successfully."""
        self.user_manager.add_user("John Doe", "john@example.com", 30)
        user = self.user_manager.get_user_by_id(1)
        
        self.assertIsNotNone(user)
        self.assertEqual(user["name"], "John Doe")
    
    def test_get_user_by_id_not_found(self):
        """Test getting user by non-existent ID."""
        user = self.user_manager.get_user_by_id(999)
        self.assertIsNone(user)
    
    def test_get_users_by_age_range(self):
        """Test getting users by age range."""
        # Add users with different ages
        self.user_manager.add_user("Young User", "young@example.com", 20)
        self.user_manager.add_user("Middle User", "middle@example.com", 30)
        self.user_manager.add_user("Old User", "old@example.com", 50)
        
        # Test age range 25-40
        users = self.user_manager.get_users_by_age_range(25, 40)
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["name"], "Middle User")
        
        # Test age range 15-25
        users = self.user_manager.get_users_by_age_range(15, 25)
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["name"], "Young User")
    
    def test_get_users_by_age_range_invalid(self):
        """Test getting users with invalid age range."""
        users = self.user_manager.get_users_by_age_range(40, 20)  # min > max
        self.assertEqual(len(users), 0)
    
    def test_update_user_status_success(self):
        """Test updating user status successfully."""
        self.user_manager.add_user("John Doe", "john@example.com", 30)
        
        result = self.user_manager.update_user_status(1, False)
        self.assertTrue(result)
        
        user = self.user_manager.get_user_by_id(1)
        self.assertFalse(user["is_active"])
    
    def test_update_user_status_not_found(self):
        """Test updating status of non-existent user."""
        result = self.user_manager.update_user_status(999, False)
        self.assertFalse(result)
    
    def test_delete_user_success(self):
        """Test deleting user successfully."""
        self.user_manager.add_user("John Doe", "john@example.com", 30)
        
        result = self.user_manager.delete_user(1)
        self.assertTrue(result)
        self.assertEqual(len(self.user_manager.users_list), 0)
    
    def test_delete_user_not_found(self):
        """Test deleting non-existent user."""
        result = self.user_manager.delete_user(999)
        self.assertFalse(result)
    
    def test_get_active_users_count(self):
        """Test getting count of active users."""
        # Add users with different statuses
        self.user_manager.add_user("Active User 1", "active1@example.com", 25)
        self.user_manager.add_user("Active User 2", "active2@example.com", 30)
        self.user_manager.add_user("Inactive User", "inactive@example.com", 35)
        
        # Deactivate one user
        self.user_manager.update_user_status(3, False)
        
        active_count = self.user_manager.get_active_users_count()
        self.assertEqual(active_count, 2)
    
    def test_search_users_by_name(self):
        """Test searching users by name."""
        self.user_manager.add_user("John Smith", "john@example.com", 30)
        self.user_manager.add_user("Jane Smith", "jane@example.com", 25)
        self.user_manager.add_user("Bob Johnson", "bob@example.com", 35)
        
        # Search for "Smith"
        results = self.user_manager.search_users_by_name("Smith")
        self.assertEqual(len(results), 2)
        
        # Search for "john" (case insensitive)
        results = self.user_manager.search_users_by_name("john")
        self.assertEqual(len(results), 2)
        
        # Search for non-existent name
        results = self.user_manager.search_users_by_name("NonExistent")
        self.assertEqual(len(results), 0)
    
    def test_search_users_by_name_empty_term(self):
        """Test searching with empty search term."""
        results = self.user_manager.search_users_by_name("")
        self.assertEqual(len(results), 0)
    
    def test_export_users_to_csv_success(self):
        """Test exporting users to CSV successfully."""
        # Add some users
        self.user_manager.add_user("John Doe", "john@example.com", 30)
        self.user_manager.add_user("Jane Doe", "jane@example.com", 25)
        
        # Export to CSV
        csv_file = "test_export.csv"
        result = self.user_manager.export_users_to_csv(csv_file)
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(csv_file))
        
        # Clean up
        if os.path.exists(csv_file):
            os.unlink(csv_file)
    
    def test_export_users_to_csv_empty_list(self):
        """Test exporting empty user list."""
        result = self.user_manager.export_users_to_csv("empty_export.csv")
        self.assertFalse(result)
    
    def test_get_all_users(self):
        """Test getting all users."""
        self.user_manager.add_user("User 1", "user1@example.com", 25)
        self.user_manager.add_user("User 2", "user2@example.com", 30)
        
        all_users = self.user_manager.get_all_users()
        self.assertEqual(len(all_users), 2)
        
        # Verify it returns a copy, not the original list
        all_users.append({"test": "data"})
        self.assertEqual(len(self.user_manager.users_list), 2)
    
    def test_get_user_count(self):
        """Test getting user count."""
        self.assertEqual(self.user_manager.get_user_count(), 0)
        
        self.user_manager.add_user("User 1", "user1@example.com", 25)
        self.assertEqual(self.user_manager.get_user_count(), 1)
        
        self.user_manager.add_user("User 2", "user2@example.com", 30)
        self.assertEqual(self.user_manager.get_user_count(), 2)
    
    def test_clear_all_users(self):
        """Test clearing all users."""
        # Add some users
        self.user_manager.add_user("User 1", "user1@example.com", 25)
        self.user_manager.add_user("User 2", "user2@example.com", 30)
        
        self.assertEqual(self.user_manager.get_user_count(), 2)
        
        # Clear all users
        self.user_manager.clear_all_users()
        self.assertEqual(self.user_manager.get_user_count(), 0)
    
    def test_user_id_auto_increment(self):
        """Test that user IDs auto-increment correctly."""
        self.user_manager.add_user("User 1", "user1@example.com", 25)
        self.user_manager.add_user("User 2", "user2@example.com", 30)
        self.user_manager.add_user("User 3", "user3@example.com", 35)
        
        self.assertEqual(self.user_manager.users_list[0]["id"], 1)
        self.assertEqual(self.user_manager.users_list[1]["id"], 2)
        self.assertEqual(self.user_manager.users_list[2]["id"], 3)
    
    def test_created_date_format(self):
        """Test that created_date is in ISO format."""
        self.user_manager.add_user("Test User", "test@example.com", 25)
        user = self.user_manager.get_user_by_id(1)
        
        # Check that created_date is a valid ISO format string
        from datetime import datetime
        try:
            datetime.fromisoformat(user["created_date"])
        except ValueError:
            self.fail("created_date is not in valid ISO format")
    
    def test_unicode_support(self):
        """Test support for Unicode characters in names."""
        unicode_name = "Nguyễn Văn An"
        result = self.user_manager.add_user(unicode_name, "unicode@example.com", 25)
        
        self.assertTrue(result)
        user = self.user_manager.get_user_by_id(1)
        self.assertEqual(user["name"], unicode_name)
    
    def test_large_dataset_performance(self):
        """Test performance with larger dataset."""
        # Add 100 users
        for i in range(100):
            self.user_manager.add_user(f"User {i}", f"user{i}@example.com", 20 + i)
        
        # Test search performance
        results = self.user_manager.search_users_by_name("User 5")
        self.assertEqual(len(results), 1)
        
        # Test age range performance
        results = self.user_manager.get_users_by_age_range(30, 50)
        self.assertEqual(len(results), 21)  # Users 10-30 (ages 30-50)


class TestUserManagerEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.close()
        self.temp_file_path = self.temp_file.name
        self.user_manager = UserManager(self.temp_file_path)
    
    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.temp_file_path):
            os.unlink(self.temp_file_path)
    
    def test_save_users_io_error(self):
        """Test handling of IO errors during save."""
        # Create a read-only file to simulate IO error
        with open(self.temp_file_path, 'w') as f:
            f.write('[]')
        os.chmod(self.temp_file_path, 0o444)  # Read-only
        
        self.user_manager.users_list = [{"test": "data"}]
        
        with self.assertRaises(IOError):
            self.user_manager.save_users()
    
    def test_export_csv_io_error(self):
        """Test handling of IO errors during CSV export."""
        self.user_manager.add_user("Test User", "test@example.com", 25)
        
        # Try to export to a directory that doesn't exist
        result = self.user_manager.export_users_to_csv("/nonexistent/path/file.csv")
        self.assertFalse(result)
    
    def test_age_boundary_values(self):
        """Test boundary values for age."""
        # Test age 0
        result = self.user_manager.add_user("Baby", "baby@example.com", 0)
        self.assertTrue(result)
        
        # Test very large age
        result = self.user_manager.add_user("Old Person", "old@example.com", 150)
        self.assertTrue(result)
    
    def test_email_case_sensitivity(self):
        """Test that email comparison is case-sensitive."""
        self.user_manager.add_user("User 1", "test@example.com", 25)
        
        # Try to add user with same email but different case
        result = self.user_manager.add_user("User 2", "TEST@EXAMPLE.COM", 30)
        self.assertFalse(result)  # Should fail due to case-sensitive comparison


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
