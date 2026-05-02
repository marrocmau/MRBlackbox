from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.bar import Bar
from pathlib import Path
import json
from mr_blackbox.i18n import i18n

console = Console()

class DashboardRenderer:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.ledger_path = project_root / ".mr-blackbox" / "ledger.json"

    def _load_ledger(self):
        if not self.ledger_path.exists():
            return None
        with open(self.ledger_path, "r") as f:
            return json.load(f)

    def render_costview(self):
        data = self._load_ledger()
        if not data:
            console.print(f"[bold red]{i18n.t('error')}[/bold red] Ledger not found. Run 'mr ingest' first.")
            return

        totals = data.get("totals", {})
        sessions = data.get("sessions", [])
        
        content = (
            f"Project: [cyan]{self.project_root.name}[/cyan]\n"
            f"{i18n.t('sessions_tracked')} {len(sessions)}\n\n"
            f"[bold]{i18n.t('total_cost')}[/bold]\n"
            f"USD: [green]${totals.get('usd', 0):.2f}[/green]\n"
            f"EUR: [blue]€{totals.get('eur', 0):.2f}[/blue]\n"
            f"{i18n.t('tokens')} {totals.get('tokens', 0):,}\n"
        )
        
        console.print(Panel(content, title="MR CostView", expand=False))

    def render_usage(self):
        data = self._load_ledger()
        if not data:
            console.print(f"[bold red]{i18n.t('error')}[/bold red] Ledger not found.")
            return

        totals = data.get("totals", {})
        sessions = data.get("sessions", [])
        
        # Header
        console.print(Panel(
            Text.from_markup(f"MR/  ▁ ▁ ▃ ▃ ▄ ▇ █ ▇ ▅ ▄ ▁          $\n"
                             f"usage\n"
                             f"{self.project_root.name}"),
            style="bold blue"
        ))

        # Project Cost Table
        table = Table(title=f"💰 {i18n.t('total_cost').upper()}", show_header=False, box=None)
        table.add_row("Total USD:", f"[green]${totals.get('usd', 0):.2f}[/green]")
        table.add_row("Total EUR:", f"[blue]€{totals.get('eur', 0):.2f}[/blue]")
        console.print(table)

        # Token Tier breakdown (simplified for MVP)
        tier_table = Table(title="🧩 COST BY TOKEN TIER")
        tier_table.add_column(i18n.t('tier'))
        tier_table.add_column("USD", justify="right")
        tier_table.add_column(i18n.t('tokens'), justify="right")
        
        # Aggregate tiers from all sessions
        tiers = {"Input": 0, "Output": 0, "Cache": 0}
        for s in sessions:
            u = s.get("usage", {})
            tiers["Input"] += u.get("input_tokens", 0)
            tiers["Output"] += u.get("output_tokens", 0)
            tiers["Cache"] += u.get("cache_read_tokens", 0) + u.get("cache_write_tokens", 0)
            
        # For simplicity, we assume a fixed rate for visualization in MVP
        for tier, tokens in tiers.items():
            tier_table.add_row(tier, f"${(tokens/1000000)*3:.2f}", f"{tokens:,}")
            
        # Aggregate providers
        providers = {}
        for s in sessions:
            p = s["session"].get("provider", "unknown")
            providers[p] = providers.get(p, 0.0) + s["cost"].get("total_usd", 0.0)

        prov_table = Table(title=f"🤖 COST BY {i18n.t('provider').upper()}")
        prov_table.add_column(i18n.t('provider'))
        prov_table.add_column("USD", justify="right")
        prov_table.add_column("%", justify="right")
        prov_table.add_column("Reliability", justify="center")
        
        for prov, cost in providers.items():
            pct = (cost / totals.get("usd", 1) * 100) if totals.get("usd", 0) > 0 else 0
            # Get reliability for this provider (heuristic: lowest reliability among sessions)
            modes = [s["cost"].get("calculation_mode", "exact") for s in sessions if s["session"].get("provider") == prov]
            rel = "exact"
            if "estimated" in modes: rel = "[bold red]estimated[/bold red]"
            elif "derived" in modes: rel = "[yellow]derived[/yellow]"
            
            prov_table.add_row(prov, f"${cost:.2f}", f"{pct:.1f}%", rel)
        
        console.print(prov_table)

        # Summary
        console.print(Panel(
            f"Sessions: {len(sessions)}    Last session: {sessions[-1]['session']['session_id'] if sessions else 'N/A'}",
            title="📋 SUMMARY"
        ))
