"""
Main window for the German training application.
"""

import os
from pathlib import Path
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QMainWindow, QMessageBox
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWebChannel import QWebChannel

from ..database.db_manager import DatabaseManager
from .bridge import Bridge


class MainWindow(QMainWindow):
    """Main application window with WebEngine view."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        self.setWindowTitle("Treinamento de Alemão")
        self.resize(1200, 800)
        
        # Initialize database manager
        self.db_manager = DatabaseManager()
        try:
            self.db_manager.initialize_database()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro de Inicialização",
                f"Erro ao inicializar base de dados: {str(e)}"
            )
        
        # Create web view
        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)
        
        # Setup WebChannel for Qt-JavaScript communication
        self.channel = QWebChannel()
        self.bridge = Bridge(self.db_manager)
        self.channel.registerObject("bridge", self.bridge)
        self.web_view.page().setWebChannel(self.channel)
        
        # Setup permission handler for future microphone functionality
        self.web_view.page().featurePermissionRequested.connect(
            self._handle_feature_permission
        )
        
        # Create menu bar
        self._create_menu_bar()
        
        # Load initial page
        self._load_page("index.html")
        
    def _create_menu_bar(self):
        """Create the application menu bar."""
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("&Arquivo")
        
        exit_action = file_menu.addAction("&Sair")
        exit_action.triggered.connect(self.close)
        
        # Tools menu
        tools_menu = menu_bar.addMenu("&Ferramentas")
        
        db_action = tools_menu.addAction("&Manutenção da Base de Dados")
        db_action.triggered.connect(self._open_database_manager)
        
    def _open_database_manager(self):
        """Open the database management page."""
        self._load_page("database_manager.html")
        
    def _load_page(self, page_name: str):
        """
        Load an HTML page in the web view.
        
        Args:
            page_name: Name of the HTML file to load
        """
        # Get the path to the web directory
        web_dir = Path(__file__).parent.parent / "web"
        page_path = web_dir / page_name
        
        if not page_path.exists():
            QMessageBox.warning(
                self,
                "Página Não Encontrada",
                f"Arquivo não encontrado: {page_path}"
            )
            return
            
        url = QUrl.fromLocalFile(str(page_path.absolute()))
        self.web_view.setUrl(url)
        
    def _handle_feature_permission(self, url: QUrl, feature: QWebEnginePage.Feature):
        """
        Handle feature permission requests from web pages.
        Prepared for future microphone recording functionality.
        
        Args:
            url: URL requesting the permission
            feature: Feature being requested
        """
        # Grant permission for microphone access (for future functionality)
        if feature == QWebEnginePage.Feature.MediaAudioCapture:
            self.web_view.page().setFeaturePermission(
                url,
                feature,
                QWebEnginePage.PermissionPolicy.PermissionGrantedByUser
            )
        # Grant permission for media audio/video capture
        elif feature == QWebEnginePage.Feature.MediaAudioVideoCapture:
            self.web_view.page().setFeaturePermission(
                url,
                feature,
                QWebEnginePage.PermissionPolicy.PermissionGrantedByUser
            )
