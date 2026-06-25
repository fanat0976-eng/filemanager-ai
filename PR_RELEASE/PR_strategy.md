# PR Strategy — File Manager AI

## Когда делать PR

### v0.1.0 (Initial Release)
- **Когда:** Все тесты проходят, документация готова
- **Куда:** `main`
- **Кто:** Один мейнтейнер
- **Review:** 1-2 ревьюера

## Naming Conventions

### Branches
```
feat/core — основной функционал
fix/bugs — исправления
docs/readme — документация
```

### Commits
```
feat(app): add TUI file manager with Textual
feat(ai): add Ollama integration for smart operations
feat(ops): add file operations (copy, move, delete, rename)
fix(panel): add id parameter for widget queries
fix(ai): handle Hebrew text, add error handling
docs(readme): add usage guide
chore(ci): add GitHub Actions workflow
```

## PR Description Template

```markdown
## Summary
CLI файловый менеджер с AI-помощником для умного управления файлами.

## Features
- Two-panel TUI interface (Textual)
- AI-powered: rename, find, organize, summary
- File operations: copy, move, delete, rename
- Duplicate finder
- File statistics
- Ollama integration (qwen2.5:7b)

## Testing
```bash
python main.py
# или
start.bat
```

## Hotkeys
- Tab: switch panel
- Enter: open folder
- F4: AI rename
- F7: AI organize
- F8: AI summary
- Ctrl+D: find duplicates
- Q: quit

## Dependencies
- Python 3.10+
- Textual (TUI)
- httpx (HTTP client)
- Rich (formatting)
- Ollama (local AI)
```

## Review Checklist

### Для ревьюера
- [ ] Код читаемый и понятный
- [ ] Есть docstrings
- [ ] Тесты покрывают основные кейсы
- [ ] Нет security issues
- [ ] Документация актуальна
- [ ] Ollama интеграция работает

## Post-Merge

### После merge
- [ ] Создать GitHub Release v0.1.0
- [ ] Написать README
- [ ] Добавить CI/CD
