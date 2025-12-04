"""
Treinamento de Alemão - Application Entry Point
Qt6 Desktop Application for German Language Training
"""

import sys
from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("Treinamento de Alemão")
    app.setOrganizationName("JSP Codificação")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
