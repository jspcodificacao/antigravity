"""
Qt-JavaScript bridge for communication between Python backend and web frontend.
"""

import json
from typing import Dict, Any
from PySide6.QtCore import QObject, Slot, Signal

from ..database.db_manager import DatabaseManager


class Bridge(QObject):
    """Bridge class to expose Python methods to JavaScript via QWebChannel."""
    
    # Signals for communicating back to JavaScript
    dataUpdated = Signal(str)  # Emits JSON string of updated data
    errorOccurred = Signal(str)  # Emits error message
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize the bridge.
        
        Args:
            db_manager: DatabaseManager instance
        """
        super().__init__()
        self.db_manager = db_manager
        
    @Slot(result=str)
    def get_all_data(self) -> str:
        """
        Get all database data as JSON string.
        
        Returns:
            JSON string of all data
        """
        try:
            data = self.db_manager.load_database()
            return json.dumps(data, ensure_ascii=False)
        except Exception as e:
            error_msg = f"Error loading data: {str(e)}"
            self.errorOccurred.emit(error_msg)
            return json.dumps({"error": error_msg})
            
    @Slot(str, result=bool)
    def add_character(self, char: str) -> bool:
        """
        Add a character to discarded characters list.
        
        Args:
            char: Character to add
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.db_manager.add_character(char)
            self.dataUpdated.emit(self.get_all_data())
            return True
        except Exception as e:
            self.errorOccurred.emit(f"Error adding character: {str(e)}")
            return False
            
    @Slot(str, result=bool)
    def remove_character(self, char: str) -> bool:
        """
        Remove a character from discarded characters list.
        
        Args:
            char: Character to remove
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.db_manager.remove_character(char)
            self.dataUpdated.emit(self.get_all_data())
            return True
        except Exception as e:
            self.errorOccurred.emit(f"Error removing character: {str(e)}")
            return False
            
    @Slot(str, str, str, result=bool)
    def add_phrase(self, palavra: str, frase: str, ipa: str) -> bool:
        """
        Add a new phrase.
        
        Args:
            palavra: Reference word
            frase: Complete phrase
            ipa: IPA transcription
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.db_manager.add_phrase(palavra, frase, ipa)
            self.dataUpdated.emit(self.get_all_data())
            return True
        except Exception as e:
            self.errorOccurred.emit(f"Error adding phrase: {str(e)}")
            return False
            
    @Slot(str, str, str, result=bool)
    def update_phrase(self, palavra: str, frase: str, ipa: str) -> bool:
        """
        Update an existing phrase.
        
        Args:
            palavra: Reference word
            frase: Complete phrase
            ipa: IPA transcription
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.db_manager.update_phrase(palavra, frase, ipa)
            self.dataUpdated.emit(self.get_all_data())
            return True
        except Exception as e:
            self.errorOccurred.emit(f"Error updating phrase: {str(e)}")
            return False
            
    @Slot(str, result=bool)
    def delete_phrase(self, palavra: str) -> bool:
        """
        Delete a phrase.
        
        Args:
            palavra: Reference word
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.db_manager.delete_phrase(palavra)
            self.dataUpdated.emit(self.get_all_data())
            return True
        except Exception as e:
            self.errorOccurred.emit(f"Error deleting phrase: {str(e)}")
            return False
