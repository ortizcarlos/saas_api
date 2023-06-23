import os
import shutil


for p in __import__('pathlib').Path('.').rglob('*.py[co]'): p.unlink()

for p in __import__('pathlib').Path('.').rglob('__pycache__'): p.rmdir()