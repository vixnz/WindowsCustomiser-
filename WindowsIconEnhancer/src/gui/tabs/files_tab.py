"""File types tab."""

from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QFileDialog,
    QGroupBox,
    QSplitter,
    QMessageBox,
)
from PyQt5.QtCore import Qt

from src.core.transactional_replacer import TransactionalIconReplacer


class FilesTab(QWidget):
    """Tab for managing file type icons."""

    def __init__(self, main_window):
        """Initialize files tab."""
        super().__init__()
        self.main_window = main_window
        self.selected_icon = None
        self._init_ui()

    def _init_ui(self):
        """Initialize user interface."""
        layout = QVBoxLayout()

        # Title
        title = QLabel("File Type Icon Customization")
        title_font = title.font()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Main content
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel - File type selection
        left_panel = QWidget()
        left_layout = QVBoxLayout()

        file_group = QGroupBox("Select File Types")
        file_layout = QVBoxLayout()

        # File type list
        self.file_list = QListWidget()
        self.file_list.itemSelectionChanged.connect(self._on_file_selected)

        # Add common file types
        common_types = [
            ".txt - Text Files",
            ".doc - Word Documents",
            ".pdf - PDF Files",
            ".xlsx - Excel Spreadsheets",
            ".pptx - PowerPoint Presentations",
            ".jpg - JPEG Images",
            ".png - PNG Images",
            ".mp4 - Video Files",
            ".mp3 - Audio Files",
            ".zip - Archive Files",
        ]

        for file_type in common_types:
            self.file_list.addItem(QListWidgetItem(file_type))

        file_layout.addWidget(self.file_list)

        # Buttons
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("➕ Add Custom")
        add_btn.clicked.connect(self._on_add_custom)
        btn_layout.addWidget(add_btn)

        remove_btn = QPushButton("➖ Remove")
        remove_btn.clicked.connect(self._on_remove_file)
        btn_layout.addWidget(remove_btn)

        file_layout.addLayout(btn_layout)
        file_group.setLayout(file_layout)
        left_layout.addWidget(file_group)

        left_panel.setLayout(left_layout)
        splitter.addWidget(left_panel)

        # Right panel - Icon selection
        right_panel = QWidget()
        right_layout = QVBoxLayout()

        icon_group = QGroupBox("Select Icon")
        icon_layout = QVBoxLayout()

        # Icon preview
        self.icon_preview = QLabel("No icon selected")
        self.icon_preview.setMinimumHeight(128)
        self.icon_preview.setStyleSheet(
            "border: 1px solid gray; background-color: #f0f0f0;"
        )
        self.icon_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.addWidget(self.icon_preview)

        # Icon file selection
        icon_btn_layout = QHBoxLayout()
        browse_btn = QPushButton("📂 Browse Icons")
        browse_btn.clicked.connect(self._on_browse_icons)
        icon_btn_layout.addWidget(browse_btn)
        icon_layout.addLayout(icon_btn_layout)

        icon_group.setLayout(icon_layout)
        right_layout.addWidget(icon_group)

        # Action buttons
        action_group = QGroupBox("Actions")
        action_layout = QVBoxLayout()

        apply_btn = QPushButton("✅ Apply Icon")
        apply_btn.clicked.connect(self._on_apply_icon)
        apply_btn.setMinimumHeight(40)
        action_layout.addWidget(apply_btn)

        reset_btn = QPushButton("🔄 Reset to Default")
        reset_btn.clicked.connect(self._on_reset_icon)
        reset_btn.setMinimumHeight(40)
        action_layout.addWidget(reset_btn)

        action_group.setLayout(action_layout)
        right_layout.addWidget(action_group)

        right_layout.addStretch()
        right_panel.setLayout(right_layout)
        splitter.addWidget(right_panel)

        layout.addWidget(splitter)
        self.setLayout(layout)

    def _on_file_selected(self):
        """Handle file selection."""
        if self.file_list.currentItem():
            self.main_window.statusbar.showMessage(
                f"Selected: {self.file_list.currentItem().text()}"
            )

    def _on_add_custom(self):
        """Handle add custom file type."""
        from PyQt5.QtWidgets import QInputDialog

        file_ext, ok = QInputDialog.getText(
            self, "Add Custom File Type", "Enter file extension (e.g., .xyz):"
        )
        if ok and file_ext:
            self.file_list.addItem(QListWidgetItem(file_ext))

    def _on_remove_file(self):
        """Handle remove file type."""
        for item in self.file_list.selectedItems():
            self.file_list.takeItem(self.file_list.row(item))

    def _on_browse_icons(self):
        """Handle browse icons action."""
        icon_path, _ = QFileDialog.getOpenFileName(
            self, "Select Icon File", "", "Icon Files (*.ico *.cur);;All Files (*)"
        )
        if icon_path:
            self.selected_icon = icon_path
            self.main_window.statusbar.showMessage(f"Selected icon: {icon_path}")

    def _on_apply_icon(self):
        """Handle apply icon action."""
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            self.main_window.statusbar.showMessage("❌ Please select a file type first")
            return

        if not self.selected_icon:
            self.main_window.statusbar.showMessage("❌ Please select an icon file first")
            return

        file_type_text = selected_items[0].text()
        # Extract extension from "label - description" format
        file_ext = file_type_text.split(" - ")[0].strip() if " - " in file_type_text else file_type_text
        icon_path = Path(self.selected_icon)

        try:
            replacer = TransactionalIconReplacer(self.main_window.backup_manager)
            success, msg, operation = replacer.replace_file_type_icon(file_ext, icon_path)

            if success:
                # Commit the changes
                commit_success, commit_msg = replacer.commit_operations()
                if commit_success:
                    self.main_window.statusbar.showMessage(f"✅ {msg}")
                    QMessageBox.information(
                        self,
                        "Success",
                        f"File type icon updated successfully!\n\n{commit_msg}",
                    )
                else:
                    self.main_window.statusbar.showMessage(f"⚠️ {commit_msg}")
                    QMessageBox.warning(self, "Warning", commit_msg)
            else:
                self.main_window.statusbar.showMessage(f"❌ {msg}")
                QMessageBox.critical(self, "Error", msg)
        except Exception as e:
            error_msg = f"Failed to apply icon: {str(e)}"
            self.main_window.statusbar.showMessage(f"❌ {error_msg}")
            QMessageBox.critical(self, "Error", error_msg)

    def _on_reset_icon(self):
        """Handle reset icon action."""
        selected_items = self.file_list.selectedItems()
        if not selected_items:
            self.main_window.statusbar.showMessage("❌ Please select a file type first")
            return

        file_type_text = selected_items[0].text()
        # Extract extension from "label - description" format
        file_ext = file_type_text.split(" - ")[0].strip() if " - " in file_type_text else file_type_text

        try:
            replacer = TransactionalIconReplacer(self.main_window.backup_manager)

            # Remove file type icon by resetting to default
            success, msg, operation = replacer.replace_file_type_icon(
                file_ext, Path()  # Empty path to reset
            )

            if success:
                commit_success, commit_msg = replacer.commit_operations()
                if commit_success:
                    self.main_window.statusbar.showMessage("✅ Icon reset successfully")
                    QMessageBox.information(self, "Success", "File type icon reset to default")
            else:
                self.main_window.statusbar.showMessage(f"⚠️ {msg}")

        except Exception as e:
            error_msg = f"Failed to reset icon: {str(e)}"
            self.main_window.statusbar.showMessage(f"❌ {error_msg}")
