"""AI Integration — Ollama-powered file operations."""
import httpx
from pathlib import Path


OLLAMA_URL = "http://127.0.0.1:11434"
MODEL = "qwen2.5:7b"


def ask_ai(prompt: str, context: str = "") -> str:
    """Send prompt to Ollama and get response."""
    system = (
        "Ты — AI-помощник файлового менеджера. "
        "Отвечай кратко и по делу. "
        "Если просят действие с файлами — давай конкретные команды."
    )
    if context:
        system += f"\n\nКонтекст (содержимое папки):\n{context}"

    try:
        r = httpx.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                "stream": False,
            },
            timeout=30,
        )
        return r.json()["message"]["content"]
    except Exception as e:
        return f"[red]AI error: {e}[/]"


def scan_directory(path: Path, max_files: int = 50) -> str:
    """Scan directory and return summary for AI context."""
    lines = []
    count = 0
    for entry in sorted(path.iterdir(), key=lambda p: p.name):
        if entry.name.startswith(".") or count >= max_files:
            continue
        if entry.is_dir():
            lines.append(f"  📁 {entry.name}/")
        else:
            size = entry.stat().st_size
            lines.append(f"  📄 {entry.name} ({size}B)")
        count += 1
    if count >= max_files:
        lines.append("  ... and more")
    return "\n".join(lines)


def suggest_rename(file_path: Path) -> str:
    """AI suggests better name for file."""
    context = scan_directory(file_path.parent)
    return ask_ai(
        f"Предложи новое имя для файла: {file_path.name}\n"
        f"Тип: {'папка' if file_path.is_dir() else 'файл'}\n"
        f"Расширение: {file_path.suffix}",
        context=context,
    )


def find_files_by_description(path: Path, description: str) -> str:
    """AI finds files matching description."""
    context = scan_directory(path, max_files=100)
    return ask_ai(
        f"Найди файлы по описанию: {description}\n"
        f"Верни список подходящих файлов с кратким объяснением.",
        context=context,
    )


def organize_suggestion(path: Path) -> str:
    """AI suggests how to organize files."""
    context = scan_directory(path, max_files=100)
    return ask_ai(
        "Предложи структуру папок для организации этих файлов. "
        "Сгруппируй по типу, дате или назначению. "
        "Дай конкретные команды mkdir и mv.",
        context=context,
    )


def summarize_directory(path: Path) -> str:
    """AI summarizes directory contents."""
    context = scan_directory(path, max_files=100)
    return ask_ai(
        "Кратко опиши что в этой папке. "
        "Какие файлы, для чего они, есть ли что-то интересное.",
        context=context,
    )
