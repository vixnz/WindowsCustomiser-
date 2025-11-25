#!/usr/bin/env python
"""Build and packaging script for Windows Icon Enhancer Pro."""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import json
from datetime import datetime

# Configuration
PROJECT_NAME = "WindowsIconEnhancer"
VERSION = "1.0.0"
BUILD_DIR = Path("build")
DIST_DIR = Path("dist")
OUTPUT_DIR = Path("releases")

# Colors for output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'

def log_info(msg):
    print(f"{Colors.BLUE}[INFO]{Colors.END} {msg}")

def log_success(msg):
    print(f"{Colors.GREEN}[SUCCESS]{Colors.END} {msg}")

def log_warning(msg):
    print(f"{Colors.YELLOW}[WARNING]{Colors.END} {msg}")

def log_error(msg):
    print(f"{Colors.RED}[ERROR]{Colors.END} {msg}")

def run_command(cmd, description=""):
    """Run shell command and handle errors."""
    if description:
        log_info(description)
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        log_error(f"Command failed: {cmd}")
        if e.stderr:
            print(e.stderr)
        return False

def clean():
    """Clean build artifacts."""
    log_info("Cleaning build artifacts...")
    
    for dir_path in [BUILD_DIR, DIST_DIR, Path("build"), Path("dist"), Path(f"{PROJECT_NAME}.egg-info")]:
        if dir_path.exists():
            shutil.rmtree(dir_path)
            log_success(f"Removed {dir_path}")

def install_dependencies():
    """Install build dependencies."""
    log_info("Installing build dependencies...")
    
    dependencies = [
        "PyInstaller>=6.0.0",
        "wheel>=0.42.0",
        "setuptools>=68.0.0",
    ]
    
    for dep in dependencies:
        if not run_command(f"{sys.executable} -m pip install {dep}"):
            log_error(f"Failed to install {dep}")
            return False
    
    log_success("All dependencies installed")
    return True

def run_tests():
    """Run unit tests."""
    log_info("Running unit tests...")
    
    if not run_command(f'{sys.executable} -m unittest discover -s tests -p "test_*.py"'):
        log_error("Tests failed")
        return False
    
    log_success("All tests passed")
    return True

def build_executable():
    """Build executable using PyInstaller."""
    log_info("Building executable with PyInstaller...")
    
    spec_file = Path("windows_icon_enhancer.spec")
    if not spec_file.exists():
        log_error(f"Spec file not found: {spec_file}")
        return False
    
    if not run_command(f"{sys.executable} -m PyInstaller {spec_file}"):
        log_error("PyInstaller failed")
        return False
    
    log_success("Executable built successfully")
    return True

def build_wheel():
    """Build Python wheel."""
    log_info("Building Python wheel...")
    
    if not run_command(f"{sys.executable} setup.py bdist_wheel"):
        log_error("Wheel build failed")
        return False
    
    log_success("Wheel built successfully")
    return True

def create_installer():
    """Create NSIS installer (requires NSIS to be installed)."""
    log_info("Creating NSIS installer...")
    
    nsi_file = Path("installer.nsi")
    if not nsi_file.exists():
        log_warning("NSIS script not found, skipping installer creation")
        return True
    
    # Check if NSIS is available
    if not shutil.which("makensis"):
        log_warning("NSIS not found, skipping installer creation")
        return True
    
    if not run_command(f"makensis {nsi_file}"):
        log_error("NSIS installer creation failed")
        return False
    
    log_success("NSIS installer created")
    return True

def create_release_package():
    """Create release package."""
    log_info("Creating release package...")
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Copy executable
    exe_src = DIST_DIR / PROJECT_NAME / f"{PROJECT_NAME}.exe"
    if exe_src.exists():
        exe_dst = OUTPUT_DIR / f"{PROJECT_NAME}_v{VERSION}.exe"
        shutil.copy2(exe_src, exe_dst)
        log_success(f"Created {exe_dst}")
    
    # Copy wheel
    wheel_src = list(DIST_DIR.glob("*.whl"))
    if wheel_src:
        for wheel in wheel_src:
            wheel_dst = OUTPUT_DIR / wheel.name
            shutil.copy2(wheel, wheel_dst)
            log_success(f"Created {wheel_dst}")
    
    # Create manifest
    manifest = {
        "version": VERSION,
        "build_date": datetime.now().isoformat(),
        "files": {
            "executable": f"{PROJECT_NAME}_v{VERSION}.exe",
            "documentation": ["README.md", "USER_GUIDE.md", "CONFIG.md"],
        },
        "system_requirements": {
            "os": "Windows 10/11",
            "python": "3.10+",
            "memory": "2GB minimum",
            "disk_space": "500MB",
        },
    }
    
    manifest_file = OUTPUT_DIR / "MANIFEST.json"
    with open(manifest_file, "w") as f:
        json.dump(manifest, f, indent=2)
    
    log_success(f"Created manifest: {manifest_file}")
    return True

def generate_build_report():
    """Generate build report."""
    log_info("Generating build report...")
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    report = []
    report.append("=" * 80)
    report.append(f"Windows Icon Enhancer Pro - Build Report")
    report.append(f"Version: {VERSION}")
    report.append(f"Build Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 80)
    report.append("")
    
    report.append("Build Artifacts:")
    if OUTPUT_DIR.exists():
        for file in OUTPUT_DIR.glob("*"):
            if file.is_file():
                size = file.stat().st_size / (1024 * 1024)  # MB
                report.append(f"  ✓ {file.name} ({size:.2f}MB)")
    
    report.append("")
    report.append("System Requirements:")
    report.append("  • Windows 10 or later")
    report.append("  • 2GB RAM minimum")
    report.append("  • 500MB free disk space")
    report.append("")
    
    report.append("Installation Instructions:")
    report.append("  1. Download the executable from releases/")
    report.append("  2. Run WindowsIconEnhancer_vX.X.X.exe")
    report.append("  3. Follow the installation wizard")
    report.append("  4. Grant admin privileges when prompted")
    report.append("")
    
    report_text = "\n".join(report)
    print(report_text)
    
    # Save report
    report_file = OUTPUT_DIR / "BUILD_REPORT.txt"
    with open(report_file, "w") as f:
        f.write(report_text)
    
    log_success(f"Report saved: {report_file}")

def main():
    """Main build process."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Build and package Windows Icon Enhancer")
    parser.add_argument("--clean", action="store_true", help="Clean build artifacts")
    parser.add_argument("--test", action="store_true", help="Run tests")
    parser.add_argument("--exe", action="store_true", help="Build executable")
    parser.add_argument("--wheel", action="store_true", help="Build wheel")
    parser.add_argument("--installer", action="store_true", help="Create NSIS installer")
    parser.add_argument("--all", action="store_true", help="Perform all tasks")
    parser.add_argument("--release", action="store_true", help="Create release package")
    
    args = parser.parse_args()
    
    # Default to all
    if not any([args.clean, args.test, args.exe, args.wheel, args.installer, args.release]):
        args.all = True
    
    log_info(f"Starting build for {PROJECT_NAME} v{VERSION}")
    
    try:
        if args.clean or args.all:
            clean()
        
        if args.test or args.all:
            if not run_tests():
                sys.exit(1)
        
        if not install_dependencies():
            sys.exit(1)
        
        if args.exe or args.all:
            if not build_executable():
                sys.exit(1)
        
        if args.wheel or args.all:
            if not build_wheel():
                sys.exit(1)
        
        if args.installer or args.all:
            if not create_installer():
                pass  # Don't fail if installer creation fails
        
        if args.release or args.all:
            if not create_release_package():
                sys.exit(1)
        
        generate_build_report()
        log_success("Build completed successfully!")
        
    except KeyboardInterrupt:
        log_error("Build interrupted by user")
        sys.exit(130)
    except Exception as e:
        log_error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
