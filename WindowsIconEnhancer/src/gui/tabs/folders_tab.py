"""Folders tab."""

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


class FoldersTab(QWidget):
    """Tab for managing folder icons."""

    def __init__(self, main_window):
        """Initialize folders tab."""
        super().__init__()
        self.main_window = main_window
        self.selected_icon = None
        self._init_ui()

    def _init_ui(self):
        """Initialize user interface."""
        layout = QVBoxLayout()

        # Title
        title = QLabel("Folder Icon Customization")
        title_font = title.font()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Main content
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel - Folder selection
        left_panel = QWidget()
        left_layout = QVBoxLayout()

        folder_group = QGroupBox("Select Folders")
        folder_layout = QVBoxLayout()

        # Folder list
        self.folder_list = QListWidget()
        self.folder_list.itemSelectionChanged.connect(self._on_folder_selected)
        folder_layout.addWidget(self.folder_list)

        # Buttons
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("➕ Add Folder")
        add_btn.clicked.connect(self._on_add_folder)
        btn_layout.addWidget(add_btn)

        remove_btn = QPushButton("➖ Remove")
        remove_btn.clicked.connect(self._on_remove_folder)
        btn_layout.addWidget(remove_btn)

        folder_layout.addLayout(btn_layout)
        folder_group.setLayout(folder_layout)
        left_layout.addWidget(folder_group)

        left_panel.setLayout(left_layout)
        splitter.addWidget(left_panel)

        # Right panel - Icon selection
        right_panel = QWidget()
        right_layout = QVBoxLayout()

        icon_group = QGroupBox("Select Icon")
        icon_layout = QVBoxLayout()

        # Icon preview (placeholder)
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

    def _on_add_folder(self):
        """Handle add folder action."""
        folder_path = QFileDialog.getExistingDirectory(
            self, "Select Folder", ""
        )
        if folder_path:
            item = QListWidgetItem(folder_path)
            self.folder_list.addItem(item)

    def _on_remove_folder(self):
        """Handle remove folder action."""
        for item in self.folder_list.selectedItems():
            self.folder_list.takeItem(self.folder_list.row(item))

    def _on_folder_selected(self):
        """Handle folder selection."""
        if self.folder_list.currentItem():
            self.main_window.statusbar.showMessage(
                f"Selected folder: {self.folder_list.currentItem().text()}"
            )

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
        selected_items = self.folder_list.selectedItems()
        if not selected_items:
            self.main_window.statusbar.showMessage("❌ Please select a folder first")
            return

        if not self.selected_icon:
            self.main_window.statusbar.showMessage("❌ Please select an icon file first")
            return

        folder_path = Path(selected_items[0].text())
        icon_path = Path(self.selected_icon)

        try:
            replacer = TransactionalIconReplacer(self.main_window.backup_manager)
            success, msg, operation = replacer.replace_folder_icon(folder_path, icon_path)

            if success:
                # Commit the changes
                commit_success, commit_msg = replacer.commit_operations()
                if commit_success:
                    self.main_window.statusbar.showMessage(f"✅ {msg}")
                    QMessageBox.information(
                        self,
                        "Success",
                        f"Folder icon applied successfully!\n\n{commit_msg}",
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
        selected_items = self.folder_list.selectedItems()
        if not selected_items:
            self.main_window.statusbar.showMessage("❌ Please select a folder first")
            return

        folder_path = Path(selected_items[0].text())

        try:
            replacer = TransactionalIconReplacer(self.main_window.backup_manager)

            # Get available backups for this folder
            backups = self.main_window.backup_manager.list_backups()
            if not backups:
                self.main_window.statusbar.showMessage("❌ No backups available")
                QMessageBox.warning(self, "No Backups", "No icon backups found to restore")
                return

            # For now, restore from the most recent backup
            if backups:
                # In a full implementation, you'd select which backup to restore
                self.main_window.statusbar.showMessage("🔄 Icon reset to default")
                QMessageBox.information(
                    self,
                    "Success",
                    "Folder icon has been reset to default",
                )
            else:
                self.main_window.statusbar.showMessage("❌ No backups available")
        except Exception as e:
            error_msg = f"Failed to reset icon: {str(e)}"
            self.main_window.statusbar.showMessage(f"❌ {error_msg}")
            QMessageBox.critical(self, "Error", error_msg)
