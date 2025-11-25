"""Explorer icons tab."""

from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QGroupBox,
    QMessageBox,
    QProgressBar,
)
from PyQt5.QtCore import Qt

from src.core.transactional_replacer import TransactionalIconReplacer


class ExplorerTab(QWidget):
    """Tab for customizing Windows Explorer icons."""

    def __init__(self, main_window):
        """Initialize explorer tab."""
        super().__init__()
        self.main_window = main_window
        self.selected_icon = None
        self._init_ui()

    def _init_ui(self):
        """Initialize user interface."""
        layout = QVBoxLayout()

        # Title
        title = QLabel("Windows Explorer Icons")
        title_font = title.font()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Info group
        info_group = QGroupBox("Information")
        info_layout = QVBoxLayout()
        info_layout.addWidget(
            QLabel(
                "Change the appearance of common Windows Explorer icons:\n"
                "• Folder icons\n"
                "• File type icons\n"
                "• Drive icons\n\n"
                "This applies custom icons to all matching items system-wide."
            )
        )
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # Icon selection group
        icon_group = QGroupBox("Select Custom Icon")
        icon_layout = QVBoxLayout()

        self.icon_path_label = QLabel("No icon selected")
        self.icon_path_label.setStyleSheet("background-color: #f0f0f0; padding: 10px;")
        icon_layout.addWidget(self.icon_path_label)

        browse_btn = QPushButton("📂 Browse Icon File")
        browse_btn.clicked.connect(self._on_browse_icon)
        browse_btn.setMinimumHeight(35)
        icon_layout.addWidget(browse_btn)

        icon_group.setLayout(icon_layout)
        layout.addWidget(icon_group)

        # Options group
        options_group = QGroupBox("Select Icons to Change")
        options_layout = QVBoxLayout()

        # Create buttons for different icon categories
        self.apply_all_folders_btn = QPushButton("📁 Change ALL Folder Icons")
        self.apply_all_folders_btn.clicked.connect(self._on_change_all_folders)
        self.apply_all_folders_btn.setMinimumHeight(40)
        self.apply_all_folders_btn.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold;"
        )
        options_layout.addWidget(self.apply_all_folders_btn)

        self.apply_system_folders_btn = QPushButton("🖥️ Change System Folder Icons")
        self.apply_system_folders_btn.clicked.connect(self._on_change_system_folders)
        self.apply_system_folders_btn.setMinimumHeight(40)
        options_layout.addWidget(self.apply_system_folders_btn)

        self.apply_common_files_btn = QPushButton("📄 Change Common File Icons")
        self.apply_common_files_btn.clicked.connect(self._on_change_common_files)
        self.apply_common_files_btn.setMinimumHeight(40)
        options_layout.addWidget(self.apply_common_files_btn)

        self.apply_drives_btn = QPushButton("💾 Change Drive Icons")
        self.apply_drives_btn.clicked.connect(self._on_change_drives)
        self.apply_drives_btn.setMinimumHeight(40)
        options_layout.addWidget(self.apply_drives_btn)

        options_group.setLayout(options_layout)
        layout.addWidget(options_group)

        # Progress group
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout()

        self.progress_bar = QProgressBar()
        progress_layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Ready")
        progress_layout.addWidget(self.status_label)

        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)

        # Reset button
        reset_btn = QPushButton("🔄 Reset All Explorer Icons to Default")
        reset_btn.clicked.connect(self._on_reset_all)
        reset_btn.setMinimumHeight(40)
        reset_btn.setStyleSheet("background-color: #ff9800; color: white;")
        layout.addWidget(reset_btn)

        layout.addStretch()
        self.setLayout(layout)

    def _on_browse_icon(self):
        """Handle browse icon action."""
        icon_path, _ = QFileDialog.getOpenFileName(
            self, "Select Icon File", "", "Icon Files (*.ico *.exe *.dll);;All Files (*)"
        )
        if icon_path:
            self.selected_icon = icon_path
            self.icon_path_label.setText(f"✓ {Path(icon_path).name}")
            self.main_window.statusbar.showMessage(f"Selected icon: {icon_path}")

    def _on_change_all_folders(self):
        """Change all folder icons."""
        if not self.selected_icon:
            QMessageBox.warning(self, "No Icon Selected", "Please select an icon file first")
            return

        try:
            self.status_label.setText("Applying to all folders...")
            self.progress_bar.setValue(10)

            replacer = TransactionalIconReplacer(self.main_window.backup_manager)
            icon_path = Path(self.selected_icon)

            # Apply to common folder types
            folder_extensions = [".folder", "Folder"]
            successful = 0

            for ext in folder_extensions:
                success, msg, _ = replacer.replace_file_type_icon(ext, icon_path)
                if success:
                    successful += 1
                self.progress_bar.setValue(30 + (successful * 20))

            # Commit changes
            commit_success, commit_msg = replacer.commit_operations()

            if commit_success:
                self.progress_bar.setValue(100)
                self.status_label.setText(f"✅ Applied to {successful} folder categories")
                self.main_window.statusbar.showMessage("✅ All folder icons updated successfully")
                QMessageBox.information(
                    self,
                    "Success",
                    f"Applied custom icon to all folders\n\n{commit_msg}",
                )
            else:
                self.status_label.setText(f"⚠️ {commit_msg}")
                QMessageBox.warning(self, "Warning", commit_msg)

        except Exception as e:
            error_msg = f"Failed to change folder icons: {str(e)}"
            self.status_label.setText(f"❌ {error_msg}")
            self.main_window.statusbar.showMessage(f"❌ {error_msg}")
            QMessageBox.critical(self, "Error", error_msg)

    def _on_change_system_folders(self):
        """Change system folder icons (Desktop, Documents, etc)."""
        if not self.selected_icon:
            QMessageBox.warning(self, "No Icon Selected", "Please select an icon file first")
            return

        try:
            self.status_label.setText("Applying to system folders...")
            self.progress_bar.setValue(10)

            replacer = TransactionalIconReplacer(self.main_window.backup_manager)
            icon_path = Path(self.selected_icon)

            # System folder types
            system_folders = [
                "Desktop",
                "Documents",
                "Downloads",
                "Music",
                "Pictures",
                "Videos",
            ]

            successful = 0
            for folder_type in system_folders:
                success, msg, _ = replacer.replace_file_type_icon(
                    f".{folder_type.lower()}", icon_path
                )
                if success:
                    successful += 1
                self.progress_bar.setValue(10 + (successful * 12))

            # Commit changes
            commit_success, commit_msg = replacer.commit_operations()

            if commit_success:
                self.progress_bar.setValue(100)
                self.status_label.setText(f"✅ Applied to {successful} system folders")
                self.main_window.statusbar.showMessage(
                    "✅ System folder icons updated successfully"
                )
                QMessageBox.information(
                    self,
                    "Success",
                    f"Applied custom icon to system folders\n\n{commit_msg}",
                )
            else:
                self.status_label.setText(f"⚠️ {commit_msg}")
                QMessageBox.warning(self, "Warning", commit_msg)

        except Exception as e:
            error_msg = f"Failed to change system folder icons: {str(e)}"
            self.status_label.setText(f"❌ {error_msg}")
            self.main_window.statusbar.showMessage(f"❌ {error_msg}")
            QMessageBox.critical(self, "Error", error_msg)

    def _on_change_common_files(self):
        """Change common file type icons."""
        if not self.selected_icon:
            QMessageBox.warning(self, "No Icon Selected", "Please select an icon file first")
            return

        try:
            self.status_label.setText("Applying to common file types...")
            self.progress_bar.setValue(10)

            replacer = TransactionalIconReplacer(self.main_window.backup_manager)
            icon_path = Path(self.selected_icon)

            # Common file types
            common_files = [
                ".txt",
                ".pdf",
                ".doc",
                ".docx",
                ".xlsx",
                ".xls",
                ".ppt",
                ".pptx",
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".mp3",
                ".mp4",
                ".zip",
                ".rar",
                ".exe",
            ]

            successful = 0
            total = len(common_files)

            for file_ext in common_files:
                success, msg, _ = replacer.replace_file_type_icon(file_ext, icon_path)
                if success:
                    successful += 1
                self.progress_bar.setValue(10 + int((successful / total) * 80))

            # Commit changes
            commit_success, commit_msg = replacer.commit_operations()

            if commit_success:
                self.progress_bar.setValue(100)
                self.status_label.setText(f"✅ Applied to {successful}/{total} file types")
                self.main_window.statusbar.showMessage(
                    "✅ Common file type icons updated successfully"
                )
                QMessageBox.information(
                    self,
                    "Success",
                    f"Applied custom icon to {successful} file types\n\n{commit_msg}",
                )
            else:
                self.status_label.setText(f"⚠️ {commit_msg}")
                QMessageBox.warning(self, "Warning", commit_msg)

        except Exception as e:
            error_msg = f"Failed to change file type icons: {str(e)}"
            self.status_label.setText(f"❌ {error_msg}")
            self.main_window.statusbar.showMessage(f"❌ {error_msg}")
            QMessageBox.critical(self, "Error", error_msg)

    def _on_change_drives(self):
        """Change drive/removable media icons."""
        if not self.selected_icon:
            QMessageBox.warning(self, "No Icon Selected", "Please select an icon file first")
            return

        try:
            self.status_label.setText("Applying to drive icons...")
            self.progress_bar.setValue(10)

            replacer = TransactionalIconReplacer(self.main_window.backup_manager)
            icon_path = Path(self.selected_icon)

            # Drive types
            drive_types = [
                ".drive",
                ".floppy",
                ".cdrom",
                ".removable",
            ]

            successful = 0
            for drive_type in drive_types:
                success, msg, _ = replacer.replace_file_type_icon(drive_type, icon_path)
                if success:
                    successful += 1
                self.progress_bar.setValue(10 + (successful * 20))

            # Commit changes
            commit_success, commit_msg = replacer.commit_operations()

            if commit_success:
                self.progress_bar.setValue(100)
                self.status_label.setText(f"✅ Applied to {successful} drive types")
                self.main_window.statusbar.showMessage(
                    "✅ Drive icons updated successfully"
                )
                QMessageBox.information(
                    self,
                    "Success",
                    f"Applied custom icon to drive types\n\n{commit_msg}",
                )
            else:
                self.status_label.setText(f"⚠️ {commit_msg}")
                QMessageBox.warning(self, "Warning", commit_msg)

        except Exception as e:
            error_msg = f"Failed to change drive icons: {str(e)}"
            self.status_label.setText(f"❌ {error_msg}")
            self.main_window.statusbar.showMessage(f"❌ {error_msg}")
            QMessageBox.critical(self, "Error", error_msg)

    def _on_reset_all(self):
        """Reset all explorer icons to default."""
        reply = QMessageBox.question(
            self,
            "Reset All Icons",
            "Are you sure you want to reset all Explorer icons to Windows defaults?",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.No:
            return

        try:
            self.status_label.setText("Resetting icons...")
            self.progress_bar.setValue(50)

            replacer = TransactionalIconReplacer(self.main_window.backup_manager)

            # Rollback all pending operations
            count, msg = replacer.rollback_all_operations()

            self.progress_bar.setValue(100)
            self.status_label.setText(f"✅ {msg}")
            self.main_window.statusbar.showMessage("✅ All Explorer icons reset to default")
            QMessageBox.information(
                self,
                "Success",
                f"All Explorer icons have been reset to Windows defaults\n\n{msg}",
            )

        except Exception as e:
            error_msg = f"Failed to reset icons: {str(e)}"
            self.status_label.setText(f"❌ {error_msg}")
            self.main_window.statusbar.showMessage(f"❌ {error_msg}")
            QMessageBox.critical(self, "Error", error_msg)
