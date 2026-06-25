# File Manager AI — Roadmap

## Текущий статус: v0.1.0 (Initial Release)

## v0.1.0 — Core ✅
- [x] TUI интерфейс (Textual)
- [x] Two-panel view (left/right)
- [x] AI интеграция (Ollama qwen2.5:7b)
- [x] Файловые операции (copy, move, delete, rename)
- [x] AI команды: rename, find, organize, summary
- [x] Duplicate finder
- [x] File statistics
- [x] Config system

## v0.2.0 — Planned
- [ ] Async AI commands (non-blocking)
- [ ] File preview (images, text, code)
- [ ] Batch operations
- [ ] Search by regex
- [ ] File tags/labels
- [ ] Theme customization

## v0.3.0 — Planned
- [ ] Plugin system
- [ ] Cloud storage integration
- [ ] SSH/SFTP support
- [ ] Git integration
- [ ] AI-powered file organization rules

## Зависимости
```
Python 3.10+
  ├── Textual (TUI framework)
  ├── httpx (HTTP client)
  └── Rich (formatting)

Ollama (qwen2.5:7b)
  └── AI-powered file operations
```
