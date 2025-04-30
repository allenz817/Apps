from setuptools import setup, find_packages

setup(
    name="financial-statement-ocr",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'openpyxl',
        'pytesseract',
        'opencv-python',
        'Pillow',
        'numpy'
    ],
    entry_points={
        'console_scripts': [
            'financial-ocr=src.main:main',
        ],
    },
    description="A tool for extracting tables from financial statements using OCR",
    author="Your Name",
    author_email="your.email@example.com",
)