# Quick Reference - Windows Icon Enhancer Pro

## 🚀 Quick Start

### Run Application
```powershell
cd c:\Users\vixnz\Test\WindowsIconEnhancer
python main.py
```

### Run Tests
```powershell
# All tests
python -m unittest discover -s tests -p "test_*.py" -v

# Specific test file
python -m unittest tests.test_integration -v

# Single test
python -m unittest tests.test_integration.TestCompleteWorkflow.test_full_workflow -v
```

### Build Executable
```powershell
# Clean and test
python build.py --clean --test

# Build exe
python build.py --exe

# Create release package
python build.py --release

# All-in-one
python build.py --all
```

---

## 📁 Key File Locations

### Core Engine
- `src/core/transactional_replacer.py` - Main icon replacement logic
- `src/core/lnk_handler.py` - Shortcut manipulation
- `src/utils/permission_manager.py` - Admin/UAC handling
- `src/core/backup_manager.py` - Backup storage

### GUI Components
- `src/gui/main_window.py` - Main window
- `src/gui/tabs/folders_tab.py` - Folder icon customization
- `src/gui/tabs/files_tab.py` - File type customization
- `src/gui/tabs/shortcuts_tab.py` - Shortcut customization
- `src/gui/tabs/batch_tab.py` - Batch operations

### Build & Deployment
- `build.py` - Build automation
- `windows_icon_enhancer.spec` - PyInstaller config
- `installer.nsi` - NSIS installer script
- `requirements.txt` - Dependencies

### Documentation
- `README.md` - Project overview
- `USER_GUIDE.md` - End-user documentation
- `CONFIG.md` - Configuration guide
- `PRODUCTION_STATUS.md` - Production readiness report
- `PHASE_5_SUMMARY.md` - Phase 5 completion details

---

## 🧪 Test Status

### All 32 Tests Passing ✅

**Unit Tests (19)**
- `test_icon_manager.py`: 5 tests
- `test_backup_manager.py`: 7 tests
- `test_registry_manager.py`: 5 tests
- `test_batch_processor.py`: 2 tests

**Integration Tests (13)**
- `test_integration.py`:
  - IconReplacementWorkflow: 4 tests
  - BatchOperations: 3 tests
  - PermissionManagement: 5 tests
  - CompleteWorkflow: 1 test

---

## 🔧 Main Classes & Usage

### TransactionalIconReplacer
```python
from src.core.transactional_replacer import TransactionalIconReplacer
from src.core.backup_manager import BackupManager

backup_mgr = BackupManager("./backups")
replacer = TransactionalIconReplacer(backup_mgr)

# Replace folder icon
success, msg, op = replacer.replace_folder_icon(
    Path("C:/Users/Demo/MyFolder"),
    Path("C:/Users/Demo/custom.ico")
)

if success:
    # Commit creates permanent backup
    replacer.commit_operations()
else:
    # Rollback any changes
    replacer.rollback_last_operation()
```

### PermissionManager
```python
from src.utils.permission_manager import PermissionManager

perm_mgr = PermissionManager()

# Check if admin is needed
needs_admin = perm_mgr.is_admin_required("C:/Program Files/app")

# Validate operation can proceed
can_proceed, msg, needs_elev = perm_mgr.validate_operation_permissions(
    "replace_file_type", 
    ".txt"
)

if needs_elev:
    perm_mgr.request_elevation("Need admin to change system icons")
```

### LNKShortcutHandler
```python
from src.core.lnk_handler import LNKShortcutHandler

handler = LNKShortcutHandler()

# Read shortcut properties
props = handler.read_shortcut(Path("C:/Users/User/Desktop/app.lnk"))

# Set custom icon
handler.set_shortcut_icon(
    Path("C:/Users/User/Desktop/app.lnk"),
    Path("C:/Users/User/custom.ico")
)
```

---

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    PyQt6 GUI                            │
│  ┌──────────────────────────────────────────────────┐   │
│  │ Main Window (6 Tabs + Status Bar + System Tray) │   │
│  │                                                  │   │
│  │ Tabs:                                           │   │
│  │ • Home - Welcome & Overview                     │   │
│  │ • Folders - Customize folder icons             │   │
│  │ • Files - Customize file type icons            │   │
│  │ • Shortcuts - Customize .lnk icons             │   │
│  │ • Batch - Multi-item operations                │   │
│  │ • Settings - Configuration                     │   │
│  └──────────────────────────────────────────────────┘   │
│                          ↓                               │
├─────────────────────────────────────────────────────────┤
│              Core Engine Layer                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │ TransactionalIconReplacer                       │   │
│  │ • replace_folder_icon()                         │   │
│  │ • replace_file_type_icon()                      │   │
│  │ • replace_shortcut_icon()                       │   │
│  │ • rollback_last_operation()                     │   │
│  │ • commit_operations()                           │   │
│  └──────────────────────────────────────────────────┘   │
│                          ↓                               │
│  ┌────────────┬──────────────────┬──────────────────┐   │
│  ↓            ↓                  ↓                  ↓    │
│┌─────────┐ ┌──────────┐ ┌──────────────┐ ┌────────────┐│
││Registry ││ File Sys ││ LNK Handler  ││ Backup Mgr │││
││ Manager ││ (desktop ││ (COM/pywin32)││ (JSON)    │││
││         ││ .ini)    ││              ││           │││
│└─────────┘ └──────────┘ └──────────────┘ └────────────┘│
│                                                         │
├─────────────────────────────────────────────────────────┤
│           Windows Integration Layer                      │
│  • Registry (HKEY_CURRENT_USER)                        │
│  • File System (desktop.ini, attributes)              │
│  • Windows COM (WScript.Shell for shortcuts)          │
│  • UAC Elevation (via ctypes/subprocess)              │
└─────────────────────────────────────────────────────────┘
```

---

## 🔐 Security Model

### Safe by Design
- ✅ No system-wide changes (HKEY_CURRENT_USER only)
- ✅ User-level operations (no kernel modifications)
- ✅ Permission validation before operations
- ✅ Automatic backup before any changes
- ✅ Transactional with rollback capability

### Admin Privileges
- Only requested when needed
- UAC dialog shown to user
- Detected via `ctypes.windll.shell.IsUserAnAdmin()`
- System-protected paths automatically identified

---

## 📈 Performance Characteristics

| Operation | Time | Notes |
|-----------|------|-------|
| Single folder icon | <500ms | File I/O + registry |
| Single file type | <100ms | Registry only |
| Single shortcut | <300ms | COM initialization |
| Batch 10 items | ~5s | Sequential processing |
| GUI startup | <2s | PyQt6 initialization |
| Full test suite | 1.5s | All 32 tests |

---

## 🐛 Troubleshooting

### GUI Won't Start
```powershell
# Check Python installation
python --version

# Check PyQt6
python -c "import PyQt6; print(PyQt6.__version__)"

# Check all dependencies
pip list | findstr PyQt6
```

### Tests Failing
```powershell
# Run with verbose output
python -m unittest discover -s tests -p "test_*.py" -v

# Check test requirements
cd tests
python test_integration.py
```

### Icon Changes Not Appearing
- Refresh Windows Explorer (F5)
- Restart file manager
- Restart Windows if system files changed
- Check backup manager for recent changes

### Permission Denied Errors
- Run as Administrator
- Check file permissions
- Verify icon file exists and readable
- Check folder not in system-protected location

---

## 📋 Deployment Checklist

- [ ] All tests passing (`python -m unittest discover -s tests`)
- [ ] No syntax errors (`python -m py_compile src/**/*.py`)
- [ ] Build automation working (`python build.py --test`)
- [ ] Documentation reviewed (README, USER_GUIDE, CONFIG)
- [ ] Backup location verified (`%APPDATA%\.windows_icon_enhancer\backups\`)
- [ ] PyInstaller working (`python build.py --exe`)
- [ ] NSIS installer ready (if distributing)
- [ ] Version bumped in setup.py and build.py
- [ ] Release notes prepared
- [ ] Code-signing certificate ready (optional)

---

## 📞 Support

### For Users
- See `USER_GUIDE.md` for usage instructions
- Check `CONFIG.md` for configuration options
- Review `PRODUCTION_STATUS.md` for system requirements

### For Developers
- See `PHASE_5_SUMMARY.md` for architecture
- Review `PRODUCTION_STATUS.md` for detailed specs
- Check inline code comments for implementation details

---

## ✨ Current Feature Set

### ✅ Implemented
- Folder icon customization (desktop.ini)
- File type icon customization (Registry)
- Shortcut icon customization (COM)
- Batch operations with progress
- Automatic backup creation
- Rollback capability
- Permission validation
- UAC elevation
- Professional PyQt6 GUI
- Build automation
- Comprehensive test coverage

### 🔄 Future Enhancements
- Icon creation/editing within app
- Cloud backup synchronization
- Advanced filtering
- Icon pack downloads
- System theme integration
- Scheduled backups

---

## 📄 License & Credits

Built with Python 3.14 + PyQt6 + Pillow + pywin32

For production deployment, ensure all dependencies are properly licensed.

---

**Last Updated:** November 25, 2025  
**Version:** 1.0.0  
**Status:** ✅ Production Ready
