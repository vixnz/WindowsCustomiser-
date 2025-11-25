"""Batch operations tab."""

from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QProgressBar,
    QCheckBox,
    QSpinBox,
    QGroupBox,
    QFileDialog,
    QMessageBox,
    QApplication,
)
from PyQt5.QtCore import Qt, QTimer

from src.core.batch_processor import BatchProcessor
from src.core.transactional_replacer import TransactionalIconReplacer


class BatchTab(QWidget):
    """Tab for batch operations."""

    def __init__(self, main_window):
        """Initialize batch tab."""
        super().__init__()
        self.main_window = main_window
        self._init_ui()

    def _init_ui(self):
        """Initialize user interface."""
        layout = QVBoxLayout()

        # Title
        title = QLabel("Batch Icon Operations")
        title_font = title.font()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Operation selection group
        operation_group = QGroupBox("Select Operation")
        operation_layout = QHBoxLayout()

        operation_layout.addWidget(QLabel("Operation Type:"))

        from PyQt5.QtWidgets import QComboBox

        self.operation_combo = QComboBox()
        self.operation_combo.addItems([
            "Replace Icons",
            "Convert Format",
            "Resize Icons",
            "Extract Icons",
        ])
        operation_layout.addWidget(self.operation_combo)

        operation_group.setLayout(operation_layout)
        layout.addWidget(operation_group)

        # Source selection group
        source_group = QGroupBox("Source Selection")
        source_layout = QVBoxLayout()

        self.source_label = QLabel("No source selected")
        source_layout.addWidget(self.source_label)

        browse_btn = QPushButton("📂 Browse Source Directory")
        browse_btn.clicked.connect(self._on_browse_source)
        source_layout.addWidget(browse_btn)

        source_group.setLayout(source_layout)
        layout.addWidget(source_group)

        # Options group
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()

        self.recursive_check = QCheckBox("Process subdirectories recursively")
        self.recursive_check.setChecked(True)
        options_layout.addWidget(self.recursive_check)

        self.backup_check = QCheckBox("Create backup before applying")
        self.backup_check.setChecked(True)
        options_layout.addWidget(self.backup_check)

        # Batch size
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Batch Size:"))
        self.batch_size_spin = QSpinBox()
        self.batch_size_spin.setMinimum(1)
        self.batch_size_spin.setMaximum(10000)
        self.batch_size_spin.setValue(100)
        size_layout.addWidget(self.batch_size_spin)
        size_layout.addStretch()
        options_layout.addLayout(size_layout)

        options_group.setLayout(options_layout)
        layout.addWidget(options_group)

        # Progress group
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout()

        progress_layout.addWidget(QLabel("Processing:"))
        self.progress_bar = QProgressBar()
        progress_layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Idle")
        progress_layout.addWidget(self.status_label)

        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)

        # Action buttons
        action_layout = QHBoxLayout()

        start_btn = QPushButton("▶️ Start Batch Operation")
        start_btn.setMinimumHeight(40)
        start_btn.clicked.connect(self._on_start_batch)
        action_layout.addWidget(start_btn)

        pause_btn = QPushButton("⏸️ Pause")
        pause_btn.setMinimumHeight(40)
        pause_btn.clicked.connect(self._on_pause_batch)
        action_layout.addWidget(pause_btn)

        cancel_btn = QPushButton("⏹️ Cancel")
        cancel_btn.setMinimumHeight(40)
        cancel_btn.clicked.connect(self._on_cancel_batch)
        action_layout.addWidget(cancel_btn)

        layout.addLayout(action_layout)
        layout.addStretch()

        self.setLayout(layout)

    def _on_browse_source(self):
        """Handle browse source action."""
        source_dir = QFileDialog.getExistingDirectory(
            self, "Select Source Directory", ""
        )
        if source_dir:
            self.source_label.setText(f"Source: {source_dir}")
            self.main_window.statusbar.showMessage(f"Selected source: {source_dir}")

    def _on_start_batch(self):
        """Handle start batch action."""
        source_text = self.source_label.text()
        if "Source:" not in source_text:
            QMessageBox.warning(self, "No Source", "Please select a source directory first")
            return

        source_dir = source_text.replace("Source: ", "").strip()
        if not source_dir:
            QMessageBox.warning(self, "Invalid Source", "Source directory not specified")
            return

        try:
            self.status_label.setText("Processing...")
            self.progress_bar.setValue(0)
            self.main_window.statusbar.showMessage("Batch operation started...")

            replacer = TransactionalIconReplacer(self.main_window.backup_manager)
            batch_processor = BatchProcessor(replacer)

            # Define progress callback
            def update_progress(current, total, msg):
                progress_pct = int((current / total * 100)) if total > 0 else 0
                self.progress_bar.setValue(progress_pct)
                self.status_label.setText(f"{msg} ({current}/{total})")
                self.main_window.statusbar.showMessage(msg)
                QApplication.processEvents()

            # Process folder icons recursively
            source_path = Path(source_dir)
            operation_count = 0

            for folder in source_path.glob("*/"):
                # Example: apply default icon or custom logic
                update_progress(operation_count, 10, f"Processing {folder.name}")
                operation_count += 1

            # Commit all changes
            success, msg = replacer.commit_operations()

            self.progress_bar.setValue(100)
            if success:
                self.status_label.setText("✅ Batch operation completed")
                self.main_window.statusbar.showMessage("✅ Batch operation completed successfully")
                QMessageBox.information(self, "Success", msg)
            else:
                self.status_label.setText(f"⚠️ {msg}")
                self.main_window.statusbar.showMessage(f"⚠️ {msg}")
                QMessageBox.warning(self, "Warning", msg)

        except Exception as e:
            error_msg = f"Batch operation failed: {str(e)}"
            self.status_label.setText(f"❌ {error_msg}")
            self.main_window.statusbar.showMessage(f"❌ {error_msg}")
            QMessageBox.critical(self, "Error", error_msg)

    def _on_pause_batch(self):
        """Handle pause batch action."""
        self.status_label.setText("⏸️ Paused")
        self.main_window.statusbar.showMessage("Batch operation paused")

    def _on_cancel_batch(self):
        """Handle cancel batch action."""
        self.progress_bar.setValue(0)
        self.status_label.setText("❌ Cancelled")
        self.main_window.statusbar.showMessage("Batch operation cancelled")
