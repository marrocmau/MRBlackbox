import typer
import subprocess
import os
import signal
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.panel import Panel
from mr_blackbox.storage.manager import StorageManager
from mr_blackbox.i18n import i18n

app = typer.Typer(name="mr", help="MR Blackbox — AI Coding Cost Observability")
console = Console()

def get_worker_pid(root: Path) -> int:
    pid_file = root / ".mr-blackbox" / "runtime" / "worker.pid"
    if pid_file.exists():
        try:
            return int(pid_file.read_text().strip())
        except ValueError:
            return -1
    return -1

@app.command()
def init(
    name: str = typer.Option(..., "--name", "-n", help="Project name"),
    project_type: str = typer.Option("other", "--type", "-t", help="Project type (e.g., saas, webapp, ios_app)")
):
    """Initializes a new MR Blackbox project in the current directory."""
    storage = StorageManager(Path.cwd())
    if storage.init_project(name, project_type):
        console.print(Panel(f"[bold green]{i18n.t('success')}[/bold green] {i18n.t('project_init', name=name)}", title="MR Blackbox"))
    else:
        console.print(f"[bold red]{i18n.t('error')}[/bold red] {i18n.t('project_exists')}")

@app.command()
def on():
    """Starts the MR Blackbox background worker for the current project."""
    root = StorageManager.find_project_root(Path.cwd())
    if not root:
        console.print(f"[bold red]{i18n.t('error')}[/bold red] {i18n.t('not_project')}")
        return

    pid = get_worker_pid(root)
    if pid > 0:
        # Check if process is actually running
        try:
            os.kill(pid, 0)
            console.print(f"[bold yellow]{i18n.t('warning')}[/bold yellow] {i18n.t('tracing_already_on')}")
            return
        except OSError:
            pass

    # Start worker in background
    import sys
    script_path = Path(__file__).parent.parent / "worker" / "main.py"
    
    # We use nohup-like behavior
    process = subprocess.Popen(
        [sys.executable, str(script_path), str(root)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True
    )
    
    console.print(Panel(f"[bold green]{i18n.t('tracing_on')}[/bold green]\n{i18n.t('tracing_project', name=root.name)}", title="MR Blackbox"))

@app.command()
def off():
    """Stops the MR Blackbox background worker."""
    root = StorageManager.find_project_root(Path.cwd())
    if not root:
        console.print(f"[bold red]{i18n.t('error')}[/bold red] {i18n.t('not_project')}")
        return

    pid = get_worker_pid(root)
    if pid <= 0:
        console.print(f"[bold yellow]{i18n.t('warning')}[/bold yellow] {i18n.t('tracing_already_off')}")
        return

    try:
        os.kill(pid, signal.SIGTERM)
        pid_file = root / ".mr-blackbox" / "runtime" / "worker.pid"
        if pid_file.exists():
            pid_file.unlink()
        console.print(Panel(f"[bold yellow]{i18n.t('tracing_off')}[/bold yellow]", title="MR Blackbox"))
    except OSError:
        console.print(f"[bold red]{i18n.t('error')}[/bold red] Could not stop worker process.")

@app.command()
def ingest(
    provider: str = typer.Option("claude", "--provider", "-p", help="AI provider (claude, gemini, codex)"),
    session_id: Optional[str] = typer.Option(None, "--session", "-s", help="Specific session ID to ingest"),
    model: str = typer.Option("claude-3-5-sonnet", "--model", "-m", help="Model used in the session")
):
    """Ingests AI coding sessions into the project ledger."""
    root = StorageManager.find_project_root(Path.cwd())
    if not root:
        console.print("[bold red]Error:[/bold red] Not an MR Blackbox project.")
        return

    storage = StorageManager(root)
    
    if provider == "claude":
        from mr_blackbox.adapters.claude import ClaudeAdapter
        from mr_blackbox.engine.cost_engine import CostEngine
        from datetime import datetime
        
        adapter = ClaudeAdapter()
        engine = CostEngine(root)
        
        if not session_id:
            session_id = adapter.get_latest_session_id(root)
            if not session_id:
                console.print("[bold yellow]Warning:[/bold yellow] No Claude sessions found.")
                return
        
        usage = adapter.ingest_session(session_id, root)
        if not usage:
            console.print(f"[bold red]Error:[/bold red] Could not ingest Claude session [cyan]{session_id}[/cyan].")
            return
            
        cost = engine.calculate_cost(usage, "claude_code", model)
        provider_name = "claude_code"
    
    elif provider == "gemini":
        from mr_blackbox.adapters.gemini import GeminiAdapter
        from mr_blackbox.engine.cost_engine import CostEngine
        from datetime import datetime
        
        adapter = GeminiAdapter()
        engine = CostEngine(root)
        
        if not session_id:
            session_id = adapter.get_latest_session_id(root)
            if not session_id:
                console.print("[bold yellow]Warning:[/bold yellow] No Gemini sessions found.")
                return

        usage = adapter.ingest_session(session_id, root)
        if not usage:
            console.print(f"[bold red]Error:[/bold red] Could not ingest Gemini session [cyan]{session_id}[/cyan].")
            return
            
        cost = engine.calculate_cost(usage, "gemini_cli", model, mode="derived")
        provider_name = "gemini_cli"
        reliability = "derived"
    
    elif provider == "codex":
        from mr_blackbox.adapters.codex import CodexAdapter
        from mr_blackbox.engine.cost_engine import CostEngine
        
        adapter = CodexAdapter()
        engine = CostEngine(root)
        
        if not session_id:
            session_id = adapter.get_latest_session_id(root)
            
        usage = adapter.ingest_session(session_id, root)
        if not usage:
            console.print(f"[bold red]{i18n.t('error')}[/bold red] Could not ingest Codex session.")
            return
            
        # Codex is always estimated in Phase 3
        cost = engine.calculate_cost(usage, "codex_cli", "codex-base", mode="estimated")
        provider_name = "codex_cli"
        reliability = "estimated"
    else:
        console.print(f"[bold red]{i18n.t('error')}[/bold red] Provider {provider} not supported.")
        return

    # Create session metadata
    from mr_blackbox.engine.models import Session
    from datetime import datetime
    session_meta = Session(
        session_id=session_id,
        project_id=root.name,
        provider=provider_name,
        started_at=datetime.now(),
        cwd=str(root),
        calculation_mode=reliability
    )
    
    if storage.add_session_to_ledger(session_meta.dict(), usage.dict(), cost.dict()):
        console.print(Panel(
            f"Ingested session: [cyan]{session_id}[/cyan] ({provider_name})\n"
            f"Tokens: {usage.total_tokens:,}\n"
            f"Cost: [green]${cost.total_usd:.4f}[/green] / [blue]€{cost.total_eur:.4f}[/blue]",
            title="MR Ingest"
        ))
    else:
        console.print(f"[bold yellow]Warning:[/bold yellow] Session [cyan]{session_id}[/cyan] already exists.")

@app.command()
def cache():
    """Shows cache efficiency and savings."""
    root = StorageManager.find_project_root(Path.cwd())
    if not root:
        console.print("[bold red]Error:[/bold red] Not an MR Blackbox project.")
        return
    
    # Load ledger
    import json
    ledger_path = root / ".mr-blackbox" / "ledger.json"
    if not ledger_path.exists():
        console.print("[bold red]Error:[/bold red] Ledger not found.")
        return
        
    with open(ledger_path, "r") as f:
        data = json.load(f)
        
    sessions = data.get("sessions", [])
    total_read = sum(s["usage"].get("cache_read_tokens", 0) for s in sessions)
    total_write = sum(s["usage"].get("cache_write_tokens", 0) for s in sessions)
    total_input = sum(s["usage"].get("input_tokens", 0) for s in sessions)
    
    total_potential = total_read + total_input
    efficiency = (total_read / total_potential * 100) if total_potential > 0 else 0
    
    # Savings estimation (using average Claude pricing for now)
    savings_usd = (total_read / 1_000_000) * 2.70 # (3.00 fresh - 0.30 read)
    
    from rich.table import Table
    table = Table(title="MR Cache Inspector")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Cache Efficiency", f"{efficiency:.1f}%")
    table.add_row("Cache Read Tokens", f"{total_read:,}")
    table.add_row("Cache Write Tokens", f"{total_write:,}")
    table.add_row("Estimated Savings", f"${savings_usd:.2f}")
    
    console.print(table)

@app.command()
def costview():
    """Shows a quick summary of project costs."""
    root = StorageManager.find_project_root(Path.cwd())
    if not root:
        console.print("[bold red]Error:[/bold red] Not an MR Blackbox project.")
        return
    
    from mr_blackbox.cli.dashboard import DashboardRenderer
    renderer = DashboardRenderer(root)
    renderer.render_costview()

@app.command()
def usage():
    """Shows a detailed dashboard of AI usage and costs."""
    root = StorageManager.find_project_root(Path.cwd())
    if not root:
        console.print("[bold red]Error:[/bold red] Not an MR Blackbox project.")
        return
    
    from mr_blackbox.cli.dashboard import DashboardRenderer
    renderer = DashboardRenderer(root)
    renderer.render_usage()

@app.command()
def status():
    """Shows the current project status."""
    root = StorageManager.find_project_root(Path.cwd())
    if not root:
        console.print("[bold yellow]Warning:[/bold yellow] No MR Blackbox project found in this directory or its parents.")
        return
    
    # Read project.json
    import json
    with open(root / ".mr-blackbox" / "project.json", "r") as f:
        project = json.load(f)
    
    pid = get_worker_pid(root)
    tracing_status = "[bold green]ON[/bold green]" if pid > 0 else "[bold red]OFF[/bold red]"
    
    console.print(Panel(
        f"Project: [cyan]{project['name']}[/cyan]\n"
        f"Type: {project['type']}\n"
        f"Tracing: {tracing_status}\n"
        f"Root: {root}",
        title="MR Blackbox Status"
    ))

if __name__ == "__main__":
    app()
