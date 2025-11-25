# Configuration Guide

## Application Configuration

Create a `config.json` file in `%APPDATA%\.windows_icon_enhancer\` to customize application behavior.

### Default Configuration

```json
{
    "theme": "dark",
    "auto_backup": true,
    "max_backups": 10,
    "check_updates": true,
    "enable_logging": true,
    "log_level": "INFO",
    "window_width": 1200,
    "window_height": 800,
    "window_maximized": false,
    "last_backup_path": "",
    "icon_preview_size": 128
}
```

### Configuration Options

#### Display Settings
- **theme**: UI theme ("light", "dark", or "system")
- **window_width**: Default window width in pixels
- **window_height**: Default window height in pixels
- **window_maximized**: Start window maximized
- **icon_preview_size**: Icon preview size in pixels

#### Backup Settings
- **auto_backup**: Create backups before changes
- **max_backups**: Maximum number of backups to keep
- **last_backup_path**: Path to last created backup

#### System Settings
- **enable_logging**: Enable application logging
- **log_level**: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **check_updates**: Check for updates on startup

## Command Line Options

```bash
# Run with custom config
python main.py --config path/to/config.json

# Restore from specific backup
python main.py --restore <backup_id>

# Execute batch configuration
python main.py --batch batch_config.json

# Verify system integrity
python main.py --verify

# Clear all caches
python main.py --clear-cache

# Extract icon from executable
python main.py --extract-icon "C:\Program Files\App\app.exe" --output icons/

# Help
python main.py --help
```

## Batch Configuration File

Create a JSON file to automate batch operations:

```json
{
    "operation": "replace_icons",
    "source_directory": "C:\\Users\\User\\Documents\\Folders",
    "icon_file": "C:\\Icons\\custom_folder.ico",
    "options": {
        "recursive": true,
        "create_backup": true,
        "restart_explorer": true,
        "batch_size": 50
    }
}
```

### Operation Types
- `replace_icons`: Replace icons for files/folders
- `convert_icons`: Convert icon formats
- `resize_icons`: Batch resize icons
- `backup_items`: Create backup of selected items
- `restore_items`: Restore from backups

## Registry Modifications

The application modifies the following registry paths:

### File Type Icons
```
HKEY_CURRENT_USER\Software\Classes\<.ext>\DefaultIcon
```

### Folder Icons
```
HKEY_CURRENT_USER\Software\Classes\Folder\DefaultIcon
```

### Shell Extensions
```
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts
```

All modifications are automatically backed up and can be restored.

## Permissions Requirements

### Required Permissions
- **User Folders**: Read/Write (Desktop, Pictures, etc.)
- **Program Files**: Administrator (for system-wide changes)
- **Windows System**: Administrator (for system icons)
- **Registry**: Read/Write to HKEY_CURRENT_USER

### Administrator Elevation
The application automatically requests administrator privileges when needed for:
- System icon changes
- Protected folder modifications
- Registry modifications
- Icon cache operations

## Troubleshooting Configuration

### Enable Debug Logging
Set `log_level` to `DEBUG` and check logs at:
```
%APPDATA%\.windows_icon_enhancer\logs\
```

### Reset Configuration
Delete the config file to restore defaults:
```powershell
Remove-Item "$env:APPDATA\.windows_icon_enhancer\config.json"
```

### Disable Auto Backups
```json
{
    "auto_backup": false
}
```

### Increase Backup Limit
```json
{
    "max_backups": 50
}
```

### Custom Icon Directory
Set environment variable:
```powershell
[Environment]::SetEnvironmentVariable("ICON_CACHE_DIR", "D:\CustomIcons", "User")
```
