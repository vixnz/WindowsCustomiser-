"""Core package."""

from .icon_manager import IconManager, IconInfo
from .backup_manager import BackupManager, BackupInfo
from .registry_manager import RegistryManager
from .batch_processor import BatchProcessor, BatchOperation, BatchOperationType
from .transactional_replacer import TransactionalIconReplacer, IconReplaceTarget
from .lnk_handler import LNKShortcutHandler
from .context_menu_manager import ContextMenuManager

__all__ = [
    "IconManager",
    "IconInfo",
    "BackupManager",
    "BackupInfo",
    "RegistryManager",
    "BatchProcessor",
    "BatchOperation",
    "BatchOperationType",
    "TransactionalIconReplacer",
    "IconReplaceTarget",
    "LNKShortcutHandler",
    "ContextMenuManager",
]
