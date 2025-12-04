"""
Database manager for German training application.
Handles CRUD operations for the JSON database.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from jsonschema import ValidationError

from .schema import validate_database, get_default_database


class DatabaseManager:
    """Manages the JSON database for German training data."""
    
    def __init__(self, db_path: str = "dados/base_de_treinamento_alemao.json"):
        """
        Initialize the database manager.
        
        Args:
            db_path: Path to the JSON database file
        """
        self.db_path = Path(db_path)
        self._data: Optional[Dict[str, Any]] = None
        
    def initialize_database(self) -> None:
        """
        Create the database file if it doesn't exist.
        Creates parent directories if needed.
        """
        # Create parent directory if it doesn't exist
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.db_path.exists():
            # Create new database with default structure
            default_data = get_default_database()
            self.save_database(default_data)
            
    def load_database(self) -> Dict[str, Any]:
        """
        Load database from file.
        
        Returns:
            Database data dictionary
            
        Raises:
            FileNotFoundError: If database file doesn't exist
            json.JSONDecodeError: If file contains invalid JSON
            ValidationError: If data doesn't match schema
        """
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database file not found: {self.db_path}")
            
        with open(self.db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Validate against schema
        validate_database(data)
        self._data = data
        return data
        
    def save_database(self, data: Dict[str, Any]) -> None:
        """
        Save database to file.
        
        Args:
            data: Database data to save
            
        Raises:
            ValidationError: If data doesn't match schema
        """
        # Validate before saving
        validate_database(data)
        
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        self._data = data
        
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """
        Validate data against schema.
        
        Args:
            data: Data to validate
            
        Returns:
            True if valid
            
        Raises:
            ValidationError: If data doesn't match schema
        """
        return validate_database(data)
        
    # CRUD operations for comparacao_de_frases_caracteres_descartados
    
    def add_character(self, char: str) -> None:
        """
        Add a character to the discarded characters list.
        
        Args:
            char: Character or string to add
            
        Raises:
            ValueError: If character already exists
        """
        data = self.load_database()
        
        if char in data["comparacao_de_frases_caracteres_descartados"]:
            raise ValueError(f"Character '{char}' already exists in the list")
            
        data["comparacao_de_frases_caracteres_descartados"].append(char)
        self.save_database(data)
        
    def remove_character(self, char: str) -> None:
        """
        Remove a character from the discarded characters list.
        
        Args:
            char: Character or string to remove
            
        Raises:
            ValueError: If character doesn't exist
        """
        data = self.load_database()
        
        if char not in data["comparacao_de_frases_caracteres_descartados"]:
            raise ValueError(f"Character '{char}' not found in the list")
            
        data["comparacao_de_frases_caracteres_descartados"].remove(char)
        self.save_database(data)
        
    def list_characters(self) -> List[str]:
        """
        Get list of all discarded characters.
        
        Returns:
            List of discarded characters
        """
        data = self.load_database()
        return data["comparacao_de_frases_caracteres_descartados"].copy()
        
    # CRUD operations for frases_para_pronuncia_com_palavra_de_referencia
    
    def add_phrase(self, palavra_referencia: str, frase: str, transcricao_ipa: str) -> None:
        """
        Add a new phrase with reference word.
        
        Args:
            palavra_referencia: Reference word (unique key)
            frase: Complete phrase in German
            transcricao_ipa: IPA phonetic transcription
            
        Raises:
            ValueError: If reference word already exists
        """
        data = self.load_database()
        
        if palavra_referencia in data["frases_para_pronuncia_com_palavra_de_referencia"]:
            raise ValueError(f"Reference word '{palavra_referencia}' already exists")
            
        data["frases_para_pronuncia_com_palavra_de_referencia"][palavra_referencia] = {
            "frase": frase,
            "transcricao_ipa": transcricao_ipa
        }
        self.save_database(data)
        
    def update_phrase(self, palavra_referencia: str, frase: str, transcricao_ipa: str) -> None:
        """
        Update an existing phrase.
        
        Args:
            palavra_referencia: Reference word (unique key)
            frase: Complete phrase in German
            transcricao_ipa: IPA phonetic transcription
            
        Raises:
            ValueError: If reference word doesn't exist
        """
        data = self.load_database()
        
        if palavra_referencia not in data["frases_para_pronuncia_com_palavra_de_referencia"]:
            raise ValueError(f"Reference word '{palavra_referencia}' not found")
            
        data["frases_para_pronuncia_com_palavra_de_referencia"][palavra_referencia] = {
            "frase": frase,
            "transcricao_ipa": transcricao_ipa
        }
        self.save_database(data)
        
    def delete_phrase(self, palavra_referencia: str) -> None:
        """
        Delete a phrase by reference word.
        
        Args:
            palavra_referencia: Reference word (unique key)
            
        Raises:
            ValueError: If reference word doesn't exist
        """
        data = self.load_database()
        
        if palavra_referencia not in data["frases_para_pronuncia_com_palavra_de_referencia"]:
            raise ValueError(f"Reference word '{palavra_referencia}' not found")
            
        del data["frases_para_pronuncia_com_palavra_de_referencia"][palavra_referencia]
        self.save_database(data)
        
    def get_phrase(self, palavra_referencia: str) -> Dict[str, str]:
        """
        Get a phrase by reference word.
        
        Args:
            palavra_referencia: Reference word (unique key)
            
        Returns:
            Dictionary with 'frase' and 'transcricao_ipa'
            
        Raises:
            ValueError: If reference word doesn't exist
        """
        data = self.load_database()
        
        if palavra_referencia not in data["frases_para_pronuncia_com_palavra_de_referencia"]:
            raise ValueError(f"Reference word '{palavra_referencia}' not found")
            
        return data["frases_para_pronuncia_com_palavra_de_referencia"][palavra_referencia].copy()
        
    def list_phrases(self) -> Dict[str, Dict[str, str]]:
        """
        Get all phrases.
        
        Returns:
            Dictionary of all phrases with reference words as keys
        """
        data = self.load_database()
        return data["frases_para_pronuncia_com_palavra_de_referencia"].copy()
