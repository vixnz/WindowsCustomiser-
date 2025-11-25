"""Batch processing engine."""

import logging
from pathlib import Path
from typing import List, Callable, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class BatchOperationType(Enum):
    """Batch operation types."""

    REPLACE_ICONS = "replace_icons"
    CONVERT_ICONS = "convert_icons"
    RESIZE_ICONS = "resize_icons"
    BACKUP_ITEMS = "backup_items"
    RESTORE_ITEMS = "restore_items"


@dataclass
class BatchOperation:
    """Definition of a batch operation."""

    operation_type: BatchOperationType
    source_items: List[Path]
    target_icon: Optional[Path] = None
    options: dict = None
    description: str = ""

    def __post_init__(self):
        """Initialize defaults."""
        if self.options is None:
            self.options = {}


@dataclass
class BatchResult:
    """Result of a batch operation."""

    total_items: int
    successful_items: int
    failed_items: int
    skipped_items: int
    errors: List[Tuple[Path, str]]  # (item, error_message)
    duration_seconds: float = 0.0


class BatchProcessor:
    """Processes batch operations."""

    def __init__(self):
        """Initialize batch processor."""
        self.current_operation: Optional[BatchOperation] = None
        self.progress_callback: Optional[Callable[[int, int], None]] = None
        self.error_callback: Optional[Callable[[Path, str], None]] = None

    def set_progress_callback(self, callback: Callable[[int, int], None]) -> None:
        """Set callback for progress updates."""
        self.progress_callback = callback

    def set_error_callback(self, callback: Callable[[Path, str], None]) -> None:
        """Set callback for error reporting."""
        self.error_callback = callback

    def process_batch(self, operation: BatchOperation) -> BatchResult:
        """Process a batch operation."""
        import time

        start_time = time.time()
        self.current_operation = operation

        result = BatchResult(
            total_items=len(operation.source_items),
            successful_items=0,
            failed_items=0,
            skipped_items=0,
            errors=[],
        )

        try:
            for index, item in enumerate(operation.source_items):
                # Update progress
                if self.progress_callback:
                    self.progress_callback(index + 1, result.total_items)

                # Process item
                success = self._process_item(operation, item)

                if success:
                    result.successful_items += 1
                elif success is None:
                    result.skipped_items += 1
                else:
                    result.failed_items += 1

        except Exception as e:
            logger.error(f"Batch processing error: {e}")

        result.duration_seconds = time.time() - start_time
        return result

    def _process_item(self, operation: BatchOperation, item: Path) -> Optional[bool]:
        """Process single item in batch."""
        try:
            if not item.exists():
                logger.warning(f"Item not found: {item}")
                return None

            if operation.operation_type == BatchOperationType.REPLACE_ICONS:
                return self._replace_icon(item, operation.target_icon)
            elif operation.operation_type == BatchOperationType.CONVERT_ICONS:
                return self._convert_icon(item, operation.options)
            elif operation.operation_type == BatchOperationType.RESIZE_ICONS:
                return self._resize_icon(item, operation.options)
            elif operation.operation_type == BatchOperationType.BACKUP_ITEMS:
                return self._backup_item(item)
            elif operation.operation_type == BatchOperationType.RESTORE_ITEMS:
                return self._restore_item(item)

            return False
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error processing {item}: {error_msg}")
            if self.error_callback:
                self.error_callback(item, error_msg)
            return False

    def _replace_icon(self, target: Path, icon_path: Path) -> bool:
        """Replace icon for a target."""
        try:
            # Import here to avoid circular imports
            from ..core.icon_manager import IconManager

            icon_manager = IconManager()
            is_valid, error = icon_manager.validate_icon(icon_path)
            if not is_valid:
                raise ValueError(f"Invalid icon: {error}")

            # TODO: Implement actual icon replacement
            logger.info(f"Would replace icon for {target} with {icon_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to replace icon: {e}")
            return False

    def _convert_icon(self, source: Path, options: dict) -> bool:
        """Convert icon format."""
        try:
            from ..core.icon_manager import IconManager

            icon_manager = IconManager()
            target_format = options.get("target_format", "ico")
            target_path = source.with_suffix(f".{target_format}")

            return icon_manager.convert_icon(source, target_path, target_format)
        except Exception as e:
            logger.error(f"Failed to convert icon: {e}")
            return False

    def _resize_icon(self, icon_path: Path, options: dict) -> bool:
        """Resize icon."""
        try:
            from ..core.icon_manager import IconManager

            icon_manager = IconManager()
            size = tuple(options.get("size", (256, 256)))
            resized = icon_manager.resize_icon(icon_path, size)

            if resized:
                target_path = icon_path.with_stem(icon_path.stem + "_resized")
                resized.save(target_path)
                return True

            return False
        except Exception as e:
            logger.error(f"Failed to resize icon: {e}")
            return False

    def _backup_item(self, item: Path) -> bool:
        """Backup item."""
        try:
            from ..core.backup_manager import BackupManager
            from ..utils.config import ConfigManager

            config_manager = ConfigManager()
            backup_manager = BackupManager(config_manager.get_backup_dir())

            return backup_manager.create_backup([item]) is not None
        except Exception as e:
            logger.error(f"Failed to backup item: {e}")
            return False

    def _restore_item(self, item: Path) -> bool:
        """Restore item from backup."""
        try:
            # TODO: Implement actual restore logic
            logger.info(f"Would restore item: {item}")
            return True
        except Exception as e:
            logger.error(f"Failed to restore item: {e}")
            return False

    def cancel_operation(self) -> None:
        """Cancel current operation."""
        self.current_operation = None
        logger.info("Batch operation cancelled")
