#!/usr/bin/env python3
"""Comprehensive bug check for File Manager AI."""
import sys
from pathlib import Path

print(f"=== Python {sys.version} ===\n")

errors = []

# Test 1: Imports
print("1. Testing imports...")
for mod_name, mod_path in [
    ("app", "app.py"),
    ("ai", "ai.py"),
    ("operations", "operations.py"),
    ("config", "config.py"),
]:
    try:
        __import__(mod_name)
        print(f"   {mod_name}.py OK")
    except Exception as e:
        print(f"   {mod_name}.py FAIL: {e}")
        errors.append(f"import {mod_name}: {e}")

# Test 2: FilePanel
print("\n2. Testing FilePanel...")
try:
    from app import FilePanel
    p = FilePanel(".", "left", id="left-panel")
    print(f"   FilePanel OK: name={p.name}, id={p.id}")
except Exception as e:
    print(f"   FilePanel FAIL: {e}")
    errors.append(f"FilePanel: {e}")

# Test 3: Operations
print("\n3. Testing operations...")
from operations import file_stats, find_duplicates, find_old_files, create_dir, safe_delete, safe_rename

try:
    stats = file_stats(Path("."))
    print(f"   file_stats: {stats['files']} files, {stats['dirs']} dirs")
except Exception as e:
    print(f"   file_stats FAIL: {e}")
    errors.append(f"file_stats: {e}")

try:
    dupes = find_duplicates(Path("."))
    print(f"   find_duplicates: {len(dupes)} found")
except Exception as e:
    print(f"   find_duplicates FAIL: {e}")
    errors.append(f"find_duplicates: {e}")

try:
    old = find_old_files(Path("."), 365)
    print(f"   find_old_files: {len(old)} old files")
except Exception as e:
    print(f"   find_old_files FAIL: {e}")
    errors.append(f"find_old_files: {e}")

try:
    result = create_dir(Path("."), "__test_dir__")
    print(f"   create_dir: {result}")
    import shutil
    shutil.rmtree("__test_dir__", ignore_errors=True)
except Exception as e:
    print(f"   create_dir FAIL: {e}")
    errors.append(f"create_dir: {e}")

# Test 4: AI (Ollama)
print("\n4. Testing AI (Ollama)...")
try:
    import httpx
    r = httpx.get("http://127.0.0.1:11434/api/tags", timeout=3)
    models = [m["name"] for m in r.json()["models"]]
    print(f"   Ollama OK: {len(models)} models")
    has_qwen = any("qwen2.5:7b" in m for m in models)
    print(f"   qwen2.5:7b: {'available' if has_qwen else 'NOT FOUND'}")
except Exception as e:
    print(f"   Ollama FAIL: {e}")
    errors.append(f"Ollama: {e}")

# Test 5: scan_directory
print("\n5. Testing scan_directory...")
try:
    from ai import scan_directory
    ctx = scan_directory(Path("."))
    print(f"   scan_directory: {len(ctx)} chars")
except Exception as e:
    print(f"   scan_directory FAIL: {e}")
    errors.append(f"scan_directory: {e}")

# Test 6: Config
print("\n6. Testing config...")
try:
    from config import load_config
    cfg = load_config()
    print(f"   load_config: {list(cfg.keys())}")
except Exception as e:
    print(f"   config FAIL: {e}")
    errors.append(f"config: {e}")

# Test 7: App creation
print("\n7. Testing app creation...")
try:
    from app import FileManagerApp
    app = FileManagerApp()
    print(f"   FileManagerApp OK")
except Exception as e:
    print(f"   FileManagerApp FAIL: {e}")
    errors.append(f"FileManagerApp: {e}")

# Summary
print("\n" + "=" * 40)
if errors:
    print(f"ERRORS FOUND: {len(errors)}")
    for e in errors:
        print(f"  - {e}")
else:
    print("ALL TESTS PASSED!")
print("=" * 40)
