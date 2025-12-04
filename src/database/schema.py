"""
JSON Schema definition and validation for German training database.
"""

import json
from typing import Dict, Any
from jsonschema import validate, ValidationError

# JSON Schema for the German training database
DATABASE_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Base de Treinamento para o Idioma Alemão",
    "type": "object",
    "required": [
        "comparacao_de_frases_caracteres_descartados",
        "frases_para_pronuncia_com_palavra_de_referencia"
    ],
    "properties": {
        "comparacao_de_frases_caracteres_descartados": {
            "type": "array",
            "description": "Lista de caracteres ou strings que devem ser descartados (ignorados) durante a comparação de frases.",
            "items": {
                "type": "string"
            }
        },
        "frases_para_pronuncia_com_palavra_de_referencia": {
            "type": "object",
            "description": "Dicionário onde a CHAVE é a palavra de referência (garantindo unicidade) e o VALOR é o objeto com os detalhes.",
            "additionalProperties": {
                "type": "object",
                "required": [
                    "frase",
                    "transcricao_ipa"
                ],
                "properties": {
                    "frase": {
                        "type": "string",
                        "description": "A frase completa em alemão."
                    },
                    "transcricao_ipa": {
                        "type": "string",
                        "description": "Transcrição fonética da frase no formato IPA (International Phonetic Alphabet)."
                    }
                }
            }
        }
    }
}

# Default empty database structure
DEFAULT_DATABASE = {
    "comparacao_de_frases_caracteres_descartados": [],
    "frases_para_pronuncia_com_palavra_de_referencia": {}
}


def validate_database(data: Dict[str, Any]) -> bool:
    """
    Validate database data against the JSON schema.
    
    Args:
        data: Database data to validate
        
    Returns:
        True if valid
        
    Raises:
        ValidationError: If data doesn't match schema
    """
    validate(instance=data, schema=DATABASE_SCHEMA)
    return True


def get_default_database() -> Dict[str, Any]:
    """
    Get a copy of the default empty database structure.
    
    Returns:
        Default database dictionary
    """
    return json.loads(json.dumps(DEFAULT_DATABASE))
