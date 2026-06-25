"""File Operations — safe file operations with confirmation."""
import os
import shutil
from pathlib import Path
from datetime import datetime, timedelta


def safe_delete(path: Path, trash: bool = True) -> str:
    """Delete file/dir. Move to trash if trash=True."""
    if not path.exists():
        return f"File not found: {path.name}"

    if trash:
        trash_dir = Path.home() / ".filemanager-trash"
        trash_dir.mkdir(exist_ok=True)
        dest = trash_dir / f"{path.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.move(str(path), str(dest))
        return f"Moved to trash: {path.name}"
    else:
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
        return f"Deleted: {path.name}"


def safe_rename(src: Path, new_name: str) -> str:
    """Rename file/dir."""
    if not src.exists():
        return f"Not found: {src.name}"
    dest = src.parent / new_name
    if dest.exists():
        return f"Already exists: {new_name}"
    src.rename(dest)
    return f"Renamed: {src.name} → {new_name}"


def safe_copy(src: Path, dest_dir: Path) -> str:
    """Copy file/dir to destination."""
    if not src.exists():
        return f"Not found: {src.name}"
    dest = dest_dir / src.name
    if dest.exists():
        return f"Already exists: {dest.name}"
    if src.is_dir():
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)
    return f"Copied: {src.name} → {dest_dir.name}/"


def safe_move(src: Path, dest_dir: Path) -> str:
    """Move file/dir to destination."""
    if not src.exists():
        return f"Not found: {src.name}"
    dest = dest_dir / src.name
    if dest.exists():
        return f"Already exists: {dest.name}"
    shutil.move(str(src), str(dest))
    return f"Moved: {src.name} → {dest_dir.name}/"


def create_dir(path: Path, name: str) -> str:
    """Create directory."""
    new_dir = path / name
    if new_dir.exists():
        return f"Already exists: {name}"
    new_dir.mkdir(parents=True)
    return f"Created: {name}/"


def find_duplicates(path: Path) -> list[dict]:
    """Find duplicate files by content hash."""
    import hashlib

    seen = {}
    duplicates = []

    for entry in path.rglob("*"):
        if entry.is_file() and not entry.name.startswith("."):
            try:
                content = entry.read_bytes()
                hash_val = hashlib.md5(content).hexdigest()
                if hash_val in seen:
                    duplicates.append({
                        "original": seen[hash_val],
                        "duplicate": entry,
                        "size": entry.stat().st_size,
                    })
                else:
                    seen[hash_val] = entry
            except (PermissionError, OSError):
                continue

    return duplicates


def find_old_files(path: Path, days: int = 30) -> list[Path]:
    """Find files older than N days."""
    cutoff = datetime.now() - timedelta(days=days)
    old_files = []

    for entry in path.rglob("*"):
        if entry.is_file() and not entry.name.startswith("."):
            mtime = datetime.fromtimestamp(entry.stat().st_mtime)
            if mtime < cutoff:
                old_files.append(entry)

    return sorted(old_files, key=lambda p: p.stat().st_mtime)


def file_stats(path: Path) -> dict:
    """Get directory statistics."""
    total_files = 0
    total_dirs = 0
    total_size = 0
    by_ext = {}

    for entry in path.rglob("*"):
        if entry.name.startswith("."):
            continue
        if entry.is_dir():
            total_dirs += 1
        else:
            total_files += 1
            size = entry.stat().st_size
            total_size += size
            ext = entry.suffix.lower() or "no_ext"
            by_ext[ext] = by_ext.get(ext, 0) + 1

    return {
        "files": total_files,
        "dirs": total_dirs,
        "total_size": total_size,
        "by_extension": dict(sorted(by_ext.items(), key=lambda x: -x[1])[:10]),
    }
