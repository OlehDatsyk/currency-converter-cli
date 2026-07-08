"""
main.py
=======
Entry point for the Currency Converter CLI application.

Responsibilities of this module ONLY:
    - Render a friendly terminal UI (via Rich)
    - Collect and validate user input
    - Delegate the actual conversion work to `CurrencyService`
    - Translate errors into readable, non-scary messages

Run with:
    python main.py
"""

from __future__ import annotations

import sys

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from config import ConfigurationError, load_settings
from currency_service import (
    APIError,
    CurrencyService,
    CurrencyServiceError,
    InvalidCurrencyError,
    NetworkError,
    RateLimitError,
)
from utils import ValidationError, format_money, normalize_currency_code, parse_amount

console = Console()

APP_TITLE = "💱  Currency Converter CLI"
APP_SUBTITLE = "Live exchange rates, right in your terminal"


def print_header() -> None:
    """Render the application banner."""
    console.print(
        Panel.fit(
            f"[bold cyan]{APP_TITLE}[/bold cyan]\n[dim]{APP_SUBTITLE}[/dim]",
            border_style="cyan",
        )
    )


def prompt_for_currency(label: str) -> str:
    """
    Repeatedly prompt the user for a currency code until a valid one
    (structurally: 3 letters) is entered.

    Args:
        label: Human-readable label shown in the prompt, e.g. "source".

    Returns:
        A normalized, uppercase 3-letter currency code.
    """
    while True:
        raw_value = Prompt.ask(f"[bold]Enter the {label} currency code[/bold] (e.g. USD)")
        try:
            return normalize_currency_code(raw_value)
        except ValidationError as exc:
            console.print(f"[bold red]✗[/bold red] {exc}")


def prompt_for_amount() -> float:
    """
    Repeatedly prompt the user for a positive numeric amount until valid.

    Returns:
        The validated amount as a float.
    """
    while True:
        raw_value = Prompt.ask("[bold]Enter the amount to convert[/bold]")
        try:
            return parse_amount(raw_value)
        except ValidationError as exc:
            console.print(f"[bold red]✗[/bold red] {exc}")


def render_result(result) -> None:  # type: ignore[no-untyped-def]
    """Render a ConversionResult as a formatted Rich table."""
    table = Table(title="Conversion Result", show_header=False, border_style="green")
    table.add_column("Field", style="bold")
    table.add_column("Value")

    table.add_row("Source Currency", result.source_currency)
    table.add_row("Target Currency", result.target_currency)
    table.add_row("Amount", format_money(result.amount))
    table.add_row("Exchange Rate", f"{result.exchange_rate:.6f}")
    table.add_row(
        "Converted Amount",
        f"[bold green]{format_money(result.converted_amount)} {result.target_currency}[/bold green]",
    )
    table.add_row("Last Updated", result.last_updated)

    console.print(table)


def run_conversion_flow(service: CurrencyService) -> None:
    """Collect input from the user and perform one conversion."""
    source_currency = prompt_for_currency("source")
    target_currency = prompt_for_currency("target")
    amount = prompt_for_amount()

    with console.status("[bold cyan]Fetching live exchange rate...[/bold cyan]"):
        result = service.convert(source_currency, target_currency, amount)

    render_result(result)


def main() -> int:
    """
    Application entry point.

    Returns:
        Process exit code (0 = success, 1 = error).
    """
    print_header()

    try:
        settings = load_settings()
    except ConfigurationError as exc:
        console.print(f"[bold red]Configuration error:[/bold red] {exc}")
        return 1

    service = CurrencyService(settings)

    try:
        run_conversion_flow(service)
    except InvalidCurrencyError as exc:
        console.print(f"[bold red]Invalid currency:[/bold red] {exc}")
        return 1
    except RateLimitError as exc:
        console.print(f"[bold red]Rate limit exceeded:[/bold red] {exc}")
        return 1
    except NetworkError as exc:
        console.print(f"[bold red]Network error:[/bold red] {exc}")
        return 1
    except APIError as exc:
        console.print(f"[bold red]API error:[/bold red] {exc}")
        return 1
    except CurrencyServiceError as exc:
        console.print(f"[bold red]Unexpected service error:[/bold red] {exc}")
        return 1
    except KeyboardInterrupt:
        console.print("\n[yellow]Cancelled by user.[/yellow]")
        return 130

    return 0


if __name__ == "__main__":
    sys.exit(main())
