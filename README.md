# Treinamento de Alemão

Aplicação desktop Python usando Qt6 WebEngine para treinamento de idioma alemão com gerenciamento de base de dados JSON.

## Requisitos do Sistema

- Windows 11
- Python 3.11.11
- UV package manager

## Instalação

1. Clone o repositório:
```powershell
git clone https://github.com/jspcodificacao/antigravity.git
cd antigravity
```

2. Instale as dependências (UV irá criar o ambiente virtual automaticamente):
```powershell
uv sync
```

## Execução

```powershell
uv run python src/main.py
```

## Estrutura do Projeto

```
antigravity/
├── dados/                         # Diretório de dados
│   └── base_de_treinamento_alemao.json  # Base de dados (criada em runtime)
├── src/                           # Código fonte
│   ├── database/                  # Módulo de gerenciamento de dados
│   ├── ui/                        # Interface do usuário Qt6
│   └── web/                       # Recursos web (HTML/CSS/JS)
└── tests/                         # Testes
```

## Tecnologias

- **Python 3.11.11**
- **PySide6 6.8.1** - Qt6 para Python
- **jsonschema** - Validação de dados JSON
- **UV** - Gerenciador de pacotes e ambientes

## Licença

MIT
