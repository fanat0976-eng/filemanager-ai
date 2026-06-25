# Checklist — File Manager AI v0.1.0

## Готовность к PR

### Код
- [x] main.py — точка входа
- [x] app.py — TUI приложение (Textual)
- [x] ai.py — AI интеграция (Ollama)
- [x] operations.py — файловые операции
- [x] config.py — конфигурация

### Функционал
- [x] Two-panel интерфейс
- [x] Навигация по папкам
- [x] AI rename (F4)
- [x] AI find (F6)
- [x] AI organize (F7)
- [x] AI summary (F8)
- [x] File copy (F3)
- [x] File delete (Delete)
- [x] Duplicate finder (Ctrl+D)
- [x] File statistics (stats)
- [x] Old files finder (old N)

### Тесты
- [x] All imports work
- [x] FilePanel creation
- [x] file_stats
- [x] find_duplicates
- [x] create_dir
- [x] Ollama connection
- [x] Config load
- [x] App creation

### Документация
- [x] README.md
- [x] Hotkeys documented
- [x] Dependencies listed

### Дополнительно
- [x] .gitignore
- [x] start.bat
- [x] pyproject.toml
- [x] Bug fixes (FilePanel ID, Hebrew text, error handling)

## Known Issues
- AI commands block UI (not async yet)
- No CI/CD yet

## Ready for PR
- [x] All tests pass
- [x] No critical bugs
- [x] Documentation complete
