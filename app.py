"""Main TUI Application — Textual-based file manager with AI."""
import asyncio
import os
from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Input, DataTable
from textual.binding import Binding
from textual.containers import Horizontal
from ai import ask_ai, scan_directory, suggest_rename, find_files_by_description, organize_suggestion, summarize_directory
from operations import safe_delete, safe_rename, safe_copy, safe_move, create_dir, find_duplicates, find_old_files, file_stats


class FilePanel(Static):
    """Single file panel (left or right)."""

    def __init__(self, path: str = ".", name: str = "left", id: str = None):
        super().__init__(name=name, id=id)
        self.current_path = Path(path).resolve()
        self.files: list[Path] = []

    def compose(self) -> ComposeResult:
        yield DataTable(id=f"files-{self.name}")
        yield Static(str(self.current_path), id=f"path-{self.name}")

    def load_files(self):
        table = self.query_one(f"#files-{self.name}", DataTable)
        table.clear()
        table.add_columns("Name", "Size", "Type")
        self.files = []
        try:
            entries = sorted(self.current_path.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
            for entry in entries:
                if entry.name.startswith("."):
                    continue
                self.files.append(entry)
                size = self._format_size(entry.stat().st_size) if entry.is_file() else "DIR"
                ftype = "folder" if entry.is_dir() else entry.suffix.lower() or "file"
                table.add_row(entry.name, size, ftype, key=str(entry))
        except PermissionError:
            table.add_row("Permission denied", "", "")

    def _format_size(self, size: int) -> str:
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"

    def selected_file(self) -> Path | None:
        table = self.query_one(f"#files-{self.name}", DataTable)
        if table.cursor_row is not None and table.cursor_row < len(self.files):
            return self.files[table.cursor_row]
        return None

    def update_status(self, text: str):
        self.query_one(f"#path-{self.name}").update(text)


class FileManagerApp(App):
    """Main application with AI-powered file management."""

    CSS = """
    Screen { background: $surface }
    #left-panel { width: 50%; border-right: solid $primary }
    #right-panel { width: 50% }
    DataTable { height: 1fr }
    #path-left, #path-right { height: 1; background: $primary; color: $text }
    #command-input { dock: bottom; height: 3 }
    #ai-output { dock: bottom; height: 8; background: $surface; border-top: solid $accent; padding: 1 }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("tab", "switch_panel", "Switch"),
        Binding("enter", "select", "Open"),
        Binding("backspace", "go_up", "Up"),
        Binding("f2", "rename", "Rename"),
        Binding("f3", "copy", "Copy"),
        Binding("f4", "ai_rename", "AI Rename"),
        Binding("f5", "refresh", "Refresh"),
        Binding("f6", "ai_find", "AI Find"),
        Binding("f7", "ai_organize", "AI Organize"),
        Binding("f8", "ai_summary", "AI Summary"),
        Binding("delete", "delete", "Delete"),
        Binding("ctrl+d", "duplicates", "Duplicates"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield FilePanel(".", "left", id="left-panel")
            yield FilePanel(".", "right", id="right-panel")
        yield Input(placeholder="Command (cd, mkdir, ai...) or prompt...", id="command-input")
        yield Static("[bold green]AI Output:[/] Ready", id="ai-output")
        yield Footer()

    def on_mount(self):
        self.active_panel = "left"
        self.query_one("#left-panel").load_files()
        self.query_one("#right-panel").load_files()

    def action_switch_panel(self):
        self.active_panel = "right" if self.active_panel == "left" else "left"

    def action_select(self):
        panel = self.query_one(f"#{self.active_panel}-panel")
        selected = panel.selected_file()
        if selected and selected.is_dir():
            panel.current_path = selected.resolve()
            panel.load_files()
        elif selected and selected.is_file():
            self.notify(f"📄 {selected.name} ({self._fmt_size(selected.stat().st_size)})")

    def action_go_up(self):
        panel = self.query_one(f"#{self.active_panel}-panel")
        parent = panel.current_path.parent
        if parent != panel.current_path:
            panel.current_path = parent
            panel.load_files()

    def action_refresh(self):
        self.query_one("#left-panel").load_files()
        self.query_one("#right-panel").load_files()

    def action_delete(self):
        panel = self.query_one(f"#{self.active_panel}-panel")
        selected = panel.selected_file()
        if selected:
            result = safe_delete(selected, trash=True)
            self._show_ai(result)
            panel.load_files()

    def action_rename(self):
        panel = self.query_one(f"#{self.active_panel}-panel")
        selected = panel.selected_file()
        if selected:
            self.notify(f"Rename: {selected.name} → type new name in command input")

    def action_copy(self):
        src_panel = self.query_one(f"#{self.active_panel}-panel")
        other = "right" if self.active_panel == "left" else "left"
        dest_panel = self.query_one(f"#{other}-panel")
        selected = src_panel.selected_file()
        if selected:
            result = safe_copy(selected, dest_panel.current_path)
            self._show_ai(result)
            dest_panel.load_files()

    async def action_ai_rename(self):
        panel = self.query_one(f"#{self.active_panel}-panel")
        selected = panel.selected_file()
        if selected:
            self._show_ai(f"[bold]AI анализ: {selected.name}[/]")
            try:
                suggestion = await asyncio.to_thread(suggest_rename, selected)
                self._show_ai(f"AI предлагает:\n{suggestion}")
            except Exception as e:
                self._show_ai(f"[red]AI error: {e}[/]")

    def action_ai_find(self):
        input_w = self.query_one("#command-input")
        input_w.placeholder = "Опишите что ищете..."
        input_w.focus()

    async def action_ai_organize(self):
        panel = self.query_one(f"#{self.active_panel}-panel")
        self._show_ai("[bold]AI анализирует структуру...[/]")
        try:
            suggestion = await asyncio.to_thread(organize_suggestion, panel.current_path)
            self._show_ai(f"AI предлагает организовать:\n{suggestion}")
        except Exception as e:
            self._show_ai(f"[red]AI error: {e}[/]")

    async def action_ai_summary(self):
        panel = self.query_one(f"#{self.active_panel}-panel")
        self._show_ai("[bold]AI анализирует папку...[/]")
        try:
            summary = await asyncio.to_thread(summarize_directory, panel.current_path)
            self._show_ai(f"AI описание:\n{summary}")
        except Exception as e:
            self._show_ai(f"[red]AI error: {e}[/]")

    def action_duplicates(self):
        panel = self.query_one(f"#{self.active_panel}-panel")
        self._show_ai("[bold]Поиск дубликатов...[/]")
        dupes = find_duplicates(panel.current_path)
        if dupes:
            lines = [f"❌ {d['duplicate'].name} (копия {d['original'].name})" for d in dupes[:10]]
            self._show_ai(f"Найдено дубликатов: {len(dupes)}\n" + "\n".join(lines))
        else:
            self._show_ai("✅ Дубликатов не найдено")

    async def on_input_submitted(self, event: Input.Submitted):
        command = event.value.strip()
        if not command:
            return
        event.value = ""

        panel = self.query_one(f"#{self.active_panel}-panel")

        if command.startswith("ai "):
            self._show_ai("[bold]AI думает...[/]")
            try:
                context = await asyncio.to_thread(scan_directory, panel.current_path)
                response = await asyncio.to_thread(ask_ai, command[3:], context)
                self._show_ai(f"🤖 {response}")
            except Exception as e:
                self._show_ai(f"[red]AI error: {e}[/]")

        elif command.startswith("cd "):
            path = command[3:].strip()
            new_path = panel.current_path / path
            if new_path.is_dir():
                panel.current_path = new_path.resolve()
                panel.load_files()
                self._show_ai(f"📁 {new_path}")
            else:
                self._show_ai(f"[red]Папка не найдена: {path}[/]")

        elif command.startswith("mkdir "):
            name = command[6:].strip()
            result = create_dir(panel.current_path, name)
            self._show_ai(result)
            panel.load_files()

        elif command.startswith("stats"):
            stats = file_stats(panel.current_path)
            exts = ", ".join(f"{k}: {v}" for k, v in stats["by_extension"].items())
            self._show_ai(
                f"📊 Статистика:\n"
                f"Файлов: {stats['files']}, Папок: {stats['dirs']}\n"
                f"Размер: {self._fmt_size(stats['total_size'])}\n"
                f"Типы: {exts}"
            )

        elif command.startswith("old "):
            days = int(command[4:].strip()) if command[4:].strip().isdigit() else 30
            old = find_old_files(panel.current_path, days)
            if old:
                lines = []
                for f in old[:15]:
                    try:
                        mtime = f.stat().st_mtime
                        lines.append(f"  {f.name} ({mtime:.0f})")
                    except Exception:
                        lines.append(f"  {f.name} (access error)")
                self._show_ai(f"Старые файлы (>{days} дней): {len(old)}\n" + "\n".join(lines))
            else:
                self._show_ai(f"✅ Нет файлов старше {days} дней")

        else:
            self._show_ai(f"[yellow]Команды: cd, mkdir, stats, old, ai <prompt>[/]")

    def _show_ai(self, text: str):
        self.query_one("#ai-output").update(text)

    def _fmt_size(self, size: int) -> str:
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024:
                return f"{size:.1f}{unit}"
            size /= 1024
        return f"{size:.1f}TB"


if __name__ == "__main__":
    app = FileManagerApp()
    app.run()
