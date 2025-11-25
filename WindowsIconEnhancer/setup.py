from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="WindowsIconEnhancer",
    version="1.0.0",
    author="Development Team",
    author_email="dev@windowsiconenhancer.dev",
    description="Professional Windows icon replacement and customization tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/WindowsIconEnhancer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Proprietary",
        "Operating System :: Microsoft :: Windows",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.10",
    install_requires=[
        "PyQt6>=6.6.0",
        "Pillow>=10.0.0",
        "psutil>=5.9.0",
        "pywin32>=306",
        "colorama>=0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "windows-icon-enhancer=main:main",
        ],
    },
)
