"""Shortcuts tab."""

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


class ShortcutsTab(QWidget):
    """Tab for managing shortcut icons."""

    def __init__(self, main_window):
        """Initialize shortcuts tab."""
        super().__init__()
        self.main_window = main_window
        self.selected_icon = None
        self._init_ui()

    def _init_ui(self):
        """Initialize user interface."""
        layout = QVBoxLayout()

        # Title
        title = QLabel("Shortcut Icon Customization")
        title_font = title.font()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Main content
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel - Shortcut selection
        left_panel = QWidget()
        left_layout = QVBoxLayout()

        shortcut_group = QGroupBox("Select Shortcuts")
        shortcut_layout = QVBoxLayout()

        # Shortcut list
        self.shortcut_list = QListWidget()
        self.shortcut_list.itemSelectionChanged.connect(self._on_shortcut_selected)
        shortcut_layout.addWidget(self.shortcut_list)

        # Buttons
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("➕ Add Shortcut")
        add_btn.clicked.connect(self._on_add_shortcut)
        btn_layout.addWidget(add_btn)

        remove_btn = QPushButton("➖ Remove")
        remove_btn.clicked.connect(self._on_remove_shortcut)
        btn_layout.addWidget(remove_btn)

        shortcut_layout.addLayout(btn_layout)
        shortcut_group.setLayout(shortcut_layout)
        left_layout.addWidget(shortcut_group)

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

    def _on_add_shortcut(self):
        """Handle add shortcut action."""
        shortcut_path, _ = QFileDialog.getOpenFileName(
            self, "Select Shortcut", "", "Shortcut Files (*.lnk);;All Files (*)"
        )
        if shortcut_path:
            item = QListWidgetItem(shortcut_path)
            self.shortcut_list.addItem(item)

    def _on_remove_shortcut(self):
        """Handle remove shortcut action."""
        for item in self.shortcut_list.selectedItems():
            self.shortcut_list.takeItem(self.shortcut_list.row(item))

    def _on_shortcut_selected(self):
        """Handle shortcut selection."""
        if self.shortcut_list.currentItem():
            self.main_window.statusbar.showMessage(
                f"Selected: {self.shortcut_list.currentItem().text()}"
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
        selected_items = self.shortcut_list.selectedItems()
        if not selected_items:
            self.main_window.statusbar.showMessage("❌ Please select a shortcut first")
            return

        if not self.selected_icon:
            self.main_window.statusbar.showMessage("❌ Please select an icon file first")
            return

        shortcut_path = Path(selected_items[0].text())
        icon_path = Path(self.selected_icon)

        try:
            replacer = TransactionalIconReplacer(self.main_window.backup_manager)
            success, msg, operation = replacer.replace_shortcut_icon(shortcut_path, icon_path)

            if success:
                # Commit the changes
                commit_success, commit_msg = replacer.commit_operations()
                if commit_success:
                    self.main_window.statusbar.showMessage(f"✅ {msg}")
                    QMessageBox.information(
                        self,
                        "Success",
                        f"Shortcut icon updated successfully!\n\n{commit_msg}",
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
        selected_items = self.shortcut_list.selectedItems()
        if not selected_items:
            self.main_window.statusbar.showMessage("❌ Please select a shortcut first")
            return

        shortcut_path = Path(selected_items[0].text())

        try:
            replacer = TransactionalIconReplacer(self.main_window.backup_manager)

            # Rollback the last operation for this shortcut if available
            success, msg = replacer.rollback_last_operation()
            if success:
                self.main_window.statusbar.showMessage("✅ Icon reset successfully")
                QMessageBox.information(self, "Success", msg)
            else:
                # If no pending operations, show message
                self.main_window.statusbar.showMessage("ℹ️ No changes to undo")
                QMessageBox.information(
                    self, "No Changes", "There are no pending changes to undo for this shortcut"
                )
        except Exception as e:
            error_msg = f"Failed to reset icon: {str(e)}"
            self.main_window.statusbar.showMessage(f"❌ {error_msg}")
