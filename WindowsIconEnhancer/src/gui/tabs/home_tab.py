"""Home tab."""

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QGroupBox,
)
from PyQt5.QtCore import Qt


class HomeTab(QWidget):
    """Home tab with quick access to main features."""

    def __init__(self, main_window):
        """Initialize home tab."""
        super().__init__()
        self.main_window = main_window
        self._init_ui()

    def _init_ui(self):
        """Initialize user interface."""
        layout = QVBoxLayout()

        # Title
        title = QLabel("Welcome to Windows Icon Enhancer Pro")
        title_font = title.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Quick access group
        quick_group = QGroupBox("Quick Access")
        quick_layout = QHBoxLayout()

        # Buttons
        change_folder_btn = QPushButton("📁 Change Folder Icons")
        change_folder_btn.setMinimumHeight(60)
        change_folder_btn.clicked.connect(self._on_change_folders)
        quick_layout.addWidget(change_folder_btn)

        change_file_btn = QPushButton("📄 Change File Type Icons")
        change_file_btn.setMinimumHeight(60)
        change_file_btn.clicked.connect(self._on_change_files)
        quick_layout.addWidget(change_file_btn)

        change_shortcut_btn = QPushButton("🔗 Change Shortcut Icons")
        change_shortcut_btn.setMinimumHeight(60)
        change_shortcut_btn.clicked.connect(self._on_change_shortcuts)
        quick_layout.addWidget(change_shortcut_btn)

        batch_btn = QPushButton("⚙️ Batch Operations")
        batch_btn.setMinimumHeight(60)
        batch_btn.clicked.connect(self._on_batch_operations)
        quick_layout.addWidget(batch_btn)

        quick_group.setLayout(quick_layout)
        layout.addWidget(quick_group)

        # Recent changes group
        recent_group = QGroupBox("Recent Changes")
        recent_layout = QVBoxLayout()

        recent_label = QLabel("No recent changes yet")
        recent_layout.addWidget(recent_label)

        recent_group.setLayout(recent_layout)
        layout.addWidget(recent_group)

        # Stats group
        stats_group = QGroupBox("Statistics")
        stats_layout = QHBoxLayout()

        stats_layout.addWidget(QLabel("Icons Changed: 0"))
        stats_layout.addWidget(QLabel("Backups Available: 0"))
        stats_layout.addWidget(QLabel("Total Size: 0 MB"))

        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)

        # Stretch
        layout.addStretch()

        # Footer with status
        footer = QLabel("💡 Tip: Use batch operations for faster processing of multiple items")
        footer_font = footer.font()
        footer_font.setPointSize(9)
        footer_font.setItalic(True)
        footer.setFont(footer_font)
        layout.addWidget(footer)

        self.setLayout(layout)

    def _on_change_folders(self):
        """Handle change folders action."""
        self.main_window.tabs.setCurrentIndex(1)

    def _on_change_files(self):
        """Handle change files action."""
        self.main_window.tabs.setCurrentIndex(2)

    def _on_change_shortcuts(self):
        """Handle change shortcuts action."""
        self.main_window.tabs.setCurrentIndex(3)

    def _on_batch_operations(self):
        """Handle batch operations action."""
        self.main_window.tabs.setCurrentIndex(4)
