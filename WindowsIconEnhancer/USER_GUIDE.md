# User Guide

## Getting Started

### Initial Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Application**
   ```bash
   python main.py
   ```

3. **Grant Admin Privileges**
   - When prompted, click "Yes" to run with administrator privileges
   - This is required for full functionality

### Main Interface

The application features a tabbed interface with the following sections:

#### 🏠 Home Tab
Quick access to main features and recent changes overview.

**Features:**
- Quick action buttons
- Recent changes list
- Statistics dashboard
- Tips and tricks

#### 📁 Folders Tab
Customize icons for specific folders.

**How to use:**
1. Click "➕ Add Folder" to select folders
2. Click "📂 Browse Icons" to select custom icon
3. Click "✅ Apply Icon" to apply changes
4. Use "🔄 Reset to Default" to restore original icons

#### 📄 File Types Tab
Change icons for specific file extensions.

**Common file types:**
- Documents (.txt, .doc, .docx, .pdf)
- Spreadsheets (.xlsx, .xls)
- Presentations (.pptx)
- Images (.jpg, .png, .bmp, .gif)
- Videos (.mp4, .avi, .mkv)
- Audio (.mp3, .wav, .flac)
- Archives (.zip, .rar, .7z)

**How to use:**
1. Select file type from list or add custom
2. Click "📂 Browse Icons" to select icon
3. Click "✅ Apply Icon" to apply changes

#### 🔗 Shortcuts Tab
Customize icons for application shortcuts.

**How to use:**
1. Click "➕ Add Shortcut" and select .lnk files
2. Select icon file
3. Click "✅ Apply Icon"

#### ⚙️ Batch Operations Tab
Process multiple icons at once.

**Operation Types:**
- Replace Icons: Apply same icon to multiple items
- Convert Format: Convert between icon formats
- Resize Icons: Batch resize icons
- Extract Icons: Extract from executable files

**How to use:**
1. Select operation type
2. Click "📂 Browse Source Directory"
3. Configure options
4. Click "▶️ Start Batch Operation"

#### ⚙️ Settings Tab
Configure application behavior and manage backups.

**Options:**
- **Appearance**: Theme selection
- **Backup Settings**: Auto backup and retention
- **System Settings**: Cache and logging
- **Backup Management**: View, restore, delete backups

## Common Tasks

### Change a Folder Icon

1. Go to **📁 Folders** tab
2. Click **➕ Add Folder** and select the folder
3. Click **📂 Browse Icons** and choose an icon
4. Click **✅ Apply Icon**
5. Explorer will refresh automatically

### Change File Type Icons

1. Go to **📄 File Types** tab
2. Select the file type from the list
3. Click **📂 Browse Icons** and select icon
4. Click **✅ Apply Icon**
5. File explorer will update

### Restore Original Icons

1. Go to **⚙️ Settings** tab
2. Click **📥 Restore from Backup**
3. Select the backup to restore
4. Confirm the restoration

### Batch Process Multiple Items

1. Go to **⚙️ Batch Operations** tab
2. Select operation type
3. Browse and select source directory
4. Configure options:
   - Check "Process subdirectories" if needed
   - Ensure "Create backup before applying" is checked
5. Click **▶️ Start Batch Operation**
6. Monitor progress bar

### Clean Up Backups

1. Go to **⚙️ Settings** tab
2. Click **🗑️ Cleanup Old Backups**
3. Confirm deletion of old backups

## Tips & Tricks

### Performance
- Use batch operations for 50+ items
- Close other applications before batch processing
- Keep at least 2GB free disk space

### Safety
- Always create backups before bulk changes
- Test with a single item first
- Export backups to external storage

### Icon Sources
- Windows System Icons: `C:\Windows\System32`
- Application Icons: Program Files folders
- Online: Search "icon packs" for free collections
- Create custom: Use icon editors like paint.net

### Keyboard Shortcuts
- `Ctrl+O`: Open icon file
- `Ctrl+Z`: Undo operation
- `Ctrl+Shift+Z`: Redo operation
- `Ctrl+Q`: Quit application
- `F5`: Refresh explorer
- `F1`: Show help

## Troubleshooting

### Icons Not Changing
**Solutions:**
- Ensure running with admin privileges
- Try refreshing explorer (Tools → Refresh Explorer)
- Clear icon cache (Settings → Clear Icon Cache)
- Check file permissions
- Restart Windows Explorer

### Permission Denied Error
**Solutions:**
- Run as Administrator
- Check file ownership
- Disable antivirus temporarily
- Check file-locking software

### Cannot Find Icon File
**Solutions:**
- Verify file path is correct
- Check file format is supported (.ico, .cur, .bmp, .png)
- Ensure file is not corrupted
- Try extracting from executable first

### Application Crashes
**Solutions:**
- Check logs: `%APPDATA%\.windows_icon_enhancer\logs\`
- Restart application
- Clear cache and try again
- Restore from backup

### Icons Reverted After Restart
**Solutions:**
- Windows may cache icons
- Clear icon cache (Settings tab)
- Restart Windows Explorer
- Clear browser cache if using web shortcuts

## Advanced Usage

### Command Line Batch Processing

```bash
# Restore specific backup
python main.py --restore backup_id_here

# Verify system integrity
python main.py --verify

# Clear all caches
python main.py --clear-cache

# Batch process from config file
python main.py --batch my_batch_config.json
```

### Custom Batch Configuration

Create `batch_config.json`:
```json
{
    "operation": "replace_icons",
    "source_directory": "C:\\Users\\User\\Desktop\\MyFolders",
    "icon_file": "C:\\Icons\\my_icon.ico",
    "options": {
        "recursive": true,
        "create_backup": true,
        "batch_size": 50
    }
}
```

Run:
```bash
python main.py --batch batch_config.json
```

### Scheduling Batch Operations

Use Windows Task Scheduler:
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (daily/weekly)
4. Action: Start program
5. Program: `python.exe`
6. Arguments: `C:\path\to\main.py --batch config.json`

## Support & Resources

- **Documentation**: Check README.md
- **Config Guide**: See CONFIG.md
- **Logs**: `%APPDATA%\.windows_icon_enhancer\logs\`
- **Backups**: `%APPDATA%\.windows_icon_enhancer\backups\`

## Data Privacy

The application:
- ✅ Stores data locally only
- ✅ Does not collect telemetry
- ✅ Does not require internet connection
- ✅ No external API calls
- ✅ Automatic backups for safety
