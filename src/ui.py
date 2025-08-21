"""
User interface for application interaction and data management.
This class provides methods for:
- Getting user input (keyword, package selection, CSV URL)
- Confirming actions
- Showing summaries, errors and success messages
"""
from typing import List 


class UserInterface:
    """Manages user interaction"""
    
    @staticmethod
    def get_keyword_input() -> str:
        """Ask user to enter a keyword to filter data"""
        while True:
            keyword = input("Enter a keyword to filter data: ").strip()
            if keyword:
                return keyword
            print("Please enter a valid keyword.")
    
    @staticmethod
    def get_package_selection(filtered_packages: List[str]) -> str:
        """Ask user to select a package from the filtered list"""
        if not filtered_packages:
            return ""
        
        print("\nAvailable packages:")
        for i, package in enumerate(filtered_packages[:10], 1):  # Show only first 10
            print(f"{i}. {package}")
        
        if len(filtered_packages) > 10:
            print(f"... and {len(filtered_packages) - 10} other packages")
        
        while True:
            selection = input("\nEnter the name of the data you want to select: ").strip()
            if selection in filtered_packages:
                return selection
            print("Please select a valid package from the list.")
    
    @staticmethod
    def get_manual_csv_url() -> str:
        """Ask user to manually enter a CSV URL"""
        while True:
            url = input("Enter CSV file URL manually: ").strip()
            if url and url.startswith('http'):
                return url
            print("Please enter a valid URL starting with http.")
    
    @staticmethod
    def confirm_action(message: str) -> bool: # The `message` parameter is a string containing the message to show to the user
        """Ask user for action confirmation"""
        while True:
            response = input(f"{message} (y/n): ").strip().lower()
            if response in ['y', 'yes', 's', 'si']:
                return True
            elif response in ['n', 'no']:
                return False
            print("Please answer with 'y' for yes or 'n' for no.")
    
    @staticmethod
    def display_summary(summary: dict): # The `summary` parameter is a dictionary containing data to display
        """Show a data summary"""
        print("\n=== DATA SUMMARY ===")
        print(f"Total number of records: {summary.get('total_records', 0)}")
        print(f"Number of columns: {len(summary.get('columns', []))}")
        
        if summary.get('columns'):
            print("\nAvailable columns:")
            for col in summary.get('columns', []):
                print(f"  - {col}")
    """
    Methods to provide user feedback during application execution.
    These methods are used to show error, success or informative messages to the user.
    They use emojis to make messages clearer and visually distinctive.
    """
    @staticmethod
    def show_error(message: str):
        """Show an error message"""
        print(f"❌ ERROR: {message}")
    
    @staticmethod
    def show_success(message: str):
        """Show a success message"""
        print(f"✅ SUCCESS: {message}")
    
    @staticmethod
    def show_info(message: str):
        """Show an informative message"""
        print(f"ℹ️  INFO: {message}")
