"""Main application window."""

import logging
from pathlib import Path
from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QStatusBar,
    QMenuBar,
    QMenu,
    QSystemTrayIcon,
    QApplication,
    QMessageBox,
    QAction,
)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import Qt, QTimer

from src.utils import ConfigManager, setup_logger, is_admin, request_admin_privileges
from src.core import BackupManager

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self):
        """Initialize main window."""
        super().__init__()

        self.config_manager = ConfigManager()
        self.backup_manager = BackupManager(self.config_manager.get_backup_dir())

        self.setWindowTitle("Windows Icon Enhancer Pro")
        self.setGeometry(100, 100, 1200, 800)

        # Check if maximized from last session
        if self.config_manager.get("window_maximized"):
            self.showMaximized()

        # Load window geometry
        width = self.config_manager.get("window_width", 1200)
        height = self.config_manager.get("window_height", 800)
        self.resize(width, height)

        # Initialize UI
        self._init_ui()
        self._create_menu_bar()
        self._create_status_bar()
        self._create_system_tray()

        # Check admin status (optional - skip if not available)
        try:
            if not is_admin():
                self._show_admin_warning()
        except Exception:
            # If admin check fails, just continue anyway
            pass

    def _init_ui(self):
        """Initialize user interface."""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Create tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Import tabs here to avoid circular imports
        from src.gui.tabs import (
            HomeTab,
            FoldersTab,
            FilesTab,
            ShortcutsTab,
            BatchTab,
            SettingsTab,
        )

        # Add tabs
        self.tabs.addTab(HomeTab(self), "🏠 Home")
        self.tabs.addTab(FoldersTab(self), "📁 Folders")
        self.tabs.addTab(FilesTab(self), "📄 File Types")
        self.tabs.addTab(ShortcutsTab(self), "🔗 Shortcuts")
        self.tabs.addTab(BatchTab(self), "⚙️ Batch Operations")
        self.tabs.addTab(SettingsTab(self), "⚙️ Settings")

        central_widget.setLayout(layout)

    def _create_menu_bar(self):
        """Create menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        open_action = QAction("&Open Icon...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self._on_open_icon)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu("&Edit")

        undo_action = QAction("&Undo", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.triggered.connect(self._on_undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction("&Redo", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.triggered.connect(self._on_redo)
        edit_menu.addAction(redo_action)

        # Tools menu
        tools_menu = menubar.addMenu("&Tools")

        clear_cache_action = QAction("Clear &Icon Cache", self)
        clear_cache_action.triggered.connect(self._on_clear_cache)
        tools_menu.addAction(clear_cache_action)

        refresh_action = QAction("&Refresh Explorer", self)
        refresh_action.triggered.connect(self._on_refresh_explorer)
        tools_menu.addAction(refresh_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        about_action = QAction("&About", self)
        about_action.triggered.connect(self._on_about)
        help_menu.addAction(about_action)

    def _create_status_bar(self):
        """Create status bar."""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Ready")

    def _create_system_tray(self):
        """Create system tray icon."""
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(self.style().SP_FileIcon))

        tray_menu = QMenu()
        show_action = tray_menu.addAction("Show")
        show_action.triggered.connect(self.show_window)
        hide_action = tray_menu.addAction("Hide")
        hide_action.triggered.connect(self.hide)
        tray_menu.addSeparator()
        exit_action = tray_menu.addAction("Exit")
        exit_action.triggered.connect(QApplication.quit)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self._on_tray_icon_activated)
        self.tray_icon.show()

    def _on_tray_icon_activated(self, reason):
        """Handle tray icon activation."""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show_window()

    def show_window(self):
        """Show main window."""
        self.showNormal()
        self.raise_()
        self.activateWindow()

    def _on_open_icon(self):
        """Handle open icon action."""
        from PyQt5.QtWidgets import QFileDialog

        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Open Icon File", "", "Icon Files (*.ico *.cur);;All Files (*)"
        )

        if file_path:
            self.statusbar.showMessage(f"Opened: {file_path}")

    def _on_undo(self):
        """Handle undo action."""
        self.statusbar.showMessage("Undo not yet implemented")

    def _on_redo(self):
        """Handle redo action."""
        self.statusbar.showMessage("Redo not yet implemented")

    def _on_clear_cache(self):
        """Handle clear cache action."""
        from src.utils.system_utils import clear_icon_cache

        if clear_icon_cache():
            QMessageBox.information(self, "Success", "Icon cache cleared successfully")
        else:
            QMessageBox.warning(self, "Error", "Failed to clear icon cache")

    def _on_refresh_explorer(self):
        """Handle refresh explorer action."""
        from src.utils.system_utils import restart_explorer

        if restart_explorer():
            QMessageBox.information(
                self, "Success", "Explorer restarted successfully"
            )
        else:
            QMessageBox.warning(self, "Error", "Failed to restart explorer")

    def _on_about(self):
        """Handle about action."""
        QMessageBox.information(
            self,
            "About Windows Icon Enhancer Pro",
            "Version 1.0.0\n\n"
            "A professional Windows desktop enhancement tool for "
            "customizing and replacing system icons.\n\n"
            "© 2025 All rights reserved.",
        )

    def _show_admin_warning(self):
        """Show admin warning."""
        self.statusbar.showMessage(
            "⚠️ Running without admin privileges. Some features may be limited."
        )

    def closeEvent(self, event):
        """Handle window close event."""
        # Save window state
        self.config_manager.set("window_width", self.width())
        self.config_manager.set("window_height", self.height())
        self.config_manager.set("window_maximized", self.isMaximized())

        # Minimize to tray instead of closing
        if self.tray_icon.isVisible():
            self.hide()
            event.ignore()
        else:
            event.accept()
