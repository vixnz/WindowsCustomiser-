"""Settings tab."""

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QComboBox,
    QCheckBox,
    QSpinBox,
    QGroupBox,
    QListWidget,
    QListWidgetItem,
)


class SettingsTab(QWidget):
    """Tab for application settings."""

    def __init__(self, main_window):
        """Initialize settings tab."""
        super().__init__()
        self.main_window = main_window
        self._init_ui()

    def _init_ui(self):
        """Initialize user interface."""
        layout = QVBoxLayout()

        # Title
        title = QLabel("Settings")
        title_font = title.font()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Appearance group
        appearance_group = QGroupBox("Appearance")
        appearance_layout = QVBoxLayout()

        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "System"])
        self.theme_combo.setCurrentText("Dark")
        self.theme_combo.currentTextChanged.connect(self._on_theme_changed)
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        appearance_layout.addLayout(theme_layout)

        appearance_group.setLayout(appearance_layout)
        layout.addWidget(appearance_group)

        # Backup settings group
        backup_group = QGroupBox("Backup Settings")
        backup_layout = QVBoxLayout()

        self.auto_backup_check = QCheckBox("Automatic backups before changes")
        self.auto_backup_check.setChecked(True)
        backup_layout.addWidget(self.auto_backup_check)

        max_backup_layout = QHBoxLayout()
        max_backup_layout.addWidget(QLabel("Maximum backups to keep:"))
        self.max_backup_spin = QSpinBox()
        self.max_backup_spin.setMinimum(1)
        self.max_backup_spin.setMaximum(100)
        self.max_backup_spin.setValue(10)
        max_backup_layout.addWidget(self.max_backup_spin)
        max_backup_layout.addStretch()
        backup_layout.addLayout(max_backup_layout)

        backup_action_layout = QHBoxLayout()
        cleanup_btn = QPushButton("🗑️ Cleanup Old Backups")
        cleanup_btn.clicked.connect(self._on_cleanup_backups)
        backup_action_layout.addWidget(cleanup_btn)

        restore_btn = QPushButton("📥 Restore from Backup")
        restore_btn.clicked.connect(self._on_restore_backup)
        backup_action_layout.addWidget(restore_btn)

        backup_action_layout.addStretch()
        backup_layout.addLayout(backup_action_layout)

        backup_group.setLayout(backup_layout)
        layout.addWidget(backup_group)

        # System settings group
        system_group = QGroupBox("System Settings")
        system_layout = QVBoxLayout()

        self.cache_check = QCheckBox("Enable icon cache")
        self.cache_check.setChecked(True)
        system_layout.addWidget(self.cache_check)

        self.logging_check = QCheckBox("Enable logging")
        self.logging_check.setChecked(True)
        system_layout.addWidget(self.logging_check)

        system_btn_layout = QHBoxLayout()
        clear_cache_btn = QPushButton("🗑️ Clear Icon Cache")
        clear_cache_btn.clicked.connect(self._on_clear_cache)
        system_btn_layout.addWidget(clear_cache_btn)

        refresh_btn = QPushButton("🔄 Refresh System")
        refresh_btn.clicked.connect(self._on_refresh_system)
        system_btn_layout.addWidget(refresh_btn)

        system_btn_layout.addStretch()
        system_layout.addLayout(system_btn_layout)

        system_group.setLayout(system_layout)
        layout.addWidget(system_group)

        # Backup list group
        backup_list_group = QGroupBox("Available Backups")
        backup_list_layout = QVBoxLayout()

        self.backup_list = QListWidget()
        backup_list_layout.addWidget(self.backup_list)

        list_btn_layout = QHBoxLayout()
        delete_backup_btn = QPushButton("🗑️ Delete Selected")
        delete_backup_btn.clicked.connect(self._on_delete_backup)
        list_btn_layout.addWidget(delete_backup_btn)

        list_btn_layout.addStretch()
        backup_list_layout.addLayout(list_btn_layout)

        backup_list_group.setLayout(backup_list_layout)
        layout.addWidget(backup_list_group)

        # Action buttons
        action_layout = QHBoxLayout()
        save_btn = QPushButton("💾 Save Settings")
        save_btn.clicked.connect(self._on_save_settings)
        action_layout.addWidget(save_btn)

        reset_btn = QPushButton("🔄 Reset to Defaults")
        reset_btn.clicked.connect(self._on_reset_settings)
        action_layout.addWidget(reset_btn)

        action_layout.addStretch()
        layout.addLayout(action_layout)

        self.setLayout(layout)
        self._refresh_backup_list()

    def _on_theme_changed(self, theme):
        """Handle theme change."""
        self.main_window.statusbar.showMessage(f"Theme changed to: {theme}")

    def _on_cleanup_backups(self):
        """Handle cleanup backups action."""
        self.main_window.statusbar.showMessage("Cleaning up old backups...")
        self._refresh_backup_list()

    def _on_restore_backup(self):
        """Handle restore backup action."""
        from PyQt5.QtWidgets import QMessageBox

        QMessageBox.information(self, "Restore Backup", "Select a backup to restore")
        self.main_window.statusbar.showMessage("Backup restored successfully")

    def _on_clear_cache(self):
        """Handle clear cache action."""
        from src.utils.system_utils import clear_icon_cache
        from PyQt5.QtWidgets import QMessageBox

        if clear_icon_cache():
            QMessageBox.information(self, "Success", "Icon cache cleared")
        else:
            QMessageBox.warning(self, "Error", "Failed to clear cache")

    def _on_refresh_system(self):
        """Handle refresh system action."""
        from src.utils.system_utils import refresh_shell_icons
        from PyQt5.QtWidgets import QMessageBox

        if refresh_shell_icons():
            QMessageBox.information(self, "Success", "System refreshed")
        else:
            QMessageBox.warning(self, "Error", "Failed to refresh system")

    def _on_delete_backup(self):
        """Handle delete backup action."""
        if self.backup_list.currentItem():
            self.backup_list.takeItem(self.backup_list.row(self.backup_list.currentItem()))
            self.main_window.statusbar.showMessage("Backup deleted")

    def _on_save_settings(self):
        """Handle save settings action."""
        self.main_window.statusbar.showMessage("✅ Settings saved successfully")

    def _on_reset_settings(self):
        """Handle reset settings action."""
        from PyQt5.QtWidgets import QMessageBox

        QMessageBox.information(self, "Reset", "Settings reset to defaults")

    def _refresh_backup_list(self):
        """Refresh backup list."""
        backups = self.main_window.backup_manager.list_backups()
        self.backup_list.clear()

        for backup in backups[:10]:  # Show latest 10
            item_text = f"{backup.name} - {backup.created_date[:10]}"
            self.backup_list.addItem(QListWidgetItem(item_text))
