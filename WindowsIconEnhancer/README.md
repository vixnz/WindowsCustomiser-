# Windows Icon Enhancer Pro

A professional-grade Windows desktop application for bulk customization and replacement of system icons, folder icons, file type icons, and application shortcuts with an intuitive GUI interface.

## Features

### Core Functionality
- **Bulk Icon Replacement**: Change icons in batch operations across multiple files/folders
- **Icon Database**: Pre-loaded collection of professional icon packs
- **Live Preview**: Real-time preview of selected icons before applying changes
- **Backup & Restore**: Automatic system backup before modifications with one-click restore
- **Theme Support**: Light, Dark, and System themes
- **Undo/Redo**: Full history tracking for all operations

### Advanced Features
- **Folder Icon Customization**: Change icons for specific folders and shortcuts
- **File Type Icons**: Customize icons for specific file extensions
- **Application Shortcuts**: Replace icons on desktop shortcuts and start menu items
- **Batch Operations**: Process multiple items simultaneously
- **Icon Search**: Powerful search and filter system
- **Custom Icon Upload**: Import your own icon collections
- **System Tray Integration**: Access from system tray
- **Context Menu Integration**: Right-click menu for quick icon changes
- **Progress Tracking**: Real-time progress monitoring for batch operations

### System Integration
- **Windows Registry Management**: Safe registry modifications with validation
- **System Permissions**: Automatic elevation handling for system-protected items
- **Shell Context Menus**: Integrate with Windows Explorer
- **Icon Cache Management**: Clear and rebuild icon caches

## Installation

### Prerequisites
- Python 3.10 or higher
- Windows 7 or later (10/11 recommended)
- Administrator privileges (for system icon changes)

### Setup

```bash
# Clone or download the project
cd WindowsIconEnhancer

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Usage

### Basic Workflow
1. **Select Target**: Choose what you want to customize (folder, file type, shortcut, etc.)
2. **Choose Icon**: Browse or search for your desired icon
3. **Preview**: See how it will look before applying
4. **Apply**: Execute the change with one click
5. **Backup Automatically**: All changes are backed up

### Batch Operations
1. Go to the "Batch" tab
2. Select multiple items using the file browser
3. Choose an icon for all selected items
4. Configure batch settings (replace subdirectories, etc.)
5. Preview and execute

### Managing Backups
- **Automatic Backups**: Created before each icon change
- **Restore**: Access from Settings → Backup Manager
- **Custom Backups**: Create named backups for specific snapshots
- **Cleanup**: Remove old backups to free space

## Project Structure

```
WindowsIconEnhancer/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── icon_manager.py          # Icon operations
│   │   ├── registry_manager.py      # Registry operations
│   │   ├── backup_manager.py        # Backup/restore
│   │   └── batch_processor.py       # Batch operations
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── main_window.py           # Main application window
│   │   ├── tabs/
│   │   │   ├── home_tab.py
│   │   │   ├── folders_tab.py
│   │   │   ├── files_tab.py
│   │   │   ├── shortcuts_tab.py
│   │   │   ├── batch_tab.py
│   │   │   └── settings_tab.py
│   │   ├── dialogs/
│   │   │   ├── icon_picker.py
│   │   │   ├── batch_config.py
│   │   │   ├── settings_dialog.py
│   │   │   └── backup_manager_ui.py
│   │   └── widgets/
│   │       ├── icon_preview.py
│   │       ├── progress_widget.py
│   │       └── icon_grid.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_operations.py
│   │   ├── system_utils.py
│   │   ├── validators.py
│   │   ├── logger.py
│   │   └── config.py
│   └── resources/
│       ├── icons.qrc
│       └── styles.qss
├── tests/
│   ├── __init__.py
│   ├── test_icon_manager.py
│   ├── test_registry.py
│   └── test_backup.py
├── backups/                         # System backups stored here
├── main.py                          # Application entry point
├── requirements.txt                 # Python dependencies
├── setup.py                         # Installation script
└── README.md                        # This file
```

## Configuration

Create a `config.ini` file in the root directory:

```ini
[Application]
theme=dark
auto_backup=true
max_backups=10
check_updates=true

[Paths]
backup_dir=./backups
icon_cache_dir=%APPDATA%\WindowsIconEnhancer\cache

[Advanced]
registry_backup=true
enable_logging=true
log_level=INFO
```

## System Requirements

- **Disk Space**: Minimum 500MB (depends on icon collections)
- **Memory**: Minimum 2GB RAM (4GB+ recommended)
- **UAC**: Admin privileges needed for system-wide changes

## Troubleshooting

### Icons not changing
- Check system UAC settings
- Run as Administrator
- Verify file permissions
- Check backup integrity

### Registry errors
- Ensure admin privileges
- Check if antivirus is blocking changes
- Review logs for detailed error information

### Performance issues
- Reduce icon library size
- Clear icon cache
- Check system resources
- Update GPU drivers

## Safety Features

✅ **Automatic Backups**: Before every change
✅ **Transaction Rollback**: Undo any operation
✅ **Permission Validation**: Checks before modification
✅ **Registry Verification**: Validates changes
✅ **Icon Cache Purge**: Safe refresh mechanism
✅ **Error Recovery**: Graceful failure handling

## Advanced Options

### Command Line
```bash
# Restore from backup
python main.py --restore <backup_id>

# Batch process icons
python main.py --batch <config_file>

# Verify system integrity
python main.py --verify

# Clear cache
python main.py --clear-cache
```

### Plugins
The application supports custom plugins for icon sources and processing filters.

## Performance Tips

1. **Batch Processing**: Use batch operations for 50+ items
2. **Icon Cache**: Regularly clear cache for optimal performance
3. **Disk Space**: Maintain at least 2GB free space
4. **Memory**: Close unnecessary applications
5. **Registry**: Keep registry defragmented

## Contributing

Contributions are welcome! Please submit pull requests with:
- Clear description of changes
- Updated documentation
- Test cases for new features

## License

Proprietary - Windows Icon Enhancer Pro
All rights reserved. For personal use only.

## Support

For issues, feature requests, or support:
- Create an issue in the repository
- Contact: support@windowsiconenhancer.dev
- Documentation: https://docs.windowsiconenhancer.dev

## Changelog

### v1.0.0 (Initial Release)
- Core icon replacement engine
- PyQt6-based GUI
- Backup/restore system
- Batch operations
- Theme support
- Windows Registry integration

## Roadmap

- [ ] Cloud icon sync
- [ ] AI-powered icon recommendations
- [ ] Icon animation support
- [ ] Team/enterprise deployment
- [ ] Icon editor (create custom icons)
- [ ] Advanced search with AI
- [ ] Real-time collaboration
- [ ] Web-based management dashboard

---

**Version**: 1.0.0  
**Last Updated**: November 25, 2025  
**Compatibility**: Windows 7 and later
