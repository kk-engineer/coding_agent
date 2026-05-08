from rich.panel import Panel
from rich.markdown import Markdown

from utils.console import console


def print_markdown_panel(
    content: str,
    title: str,
    border_style: str = "blue"
):

    markdown = Markdown(content)

    panel = Panel(
        markdown,
        title=f"[bold]{title}[/bold]",
        border_style=border_style,
        padding=(1, 2)
    )

    console.print(panel)