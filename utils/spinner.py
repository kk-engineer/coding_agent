import time

from rich.status import Status

from utils.console import console


class AgentSpinner:

    def __init__(
        self,
        message: str,
        spinner: str = "dots"
    ):

        self.message = message

        self.spinner = spinner

        self.start_time = None

        self.status = None

    def __enter__(self):

        self.start_time = time.time()

        self.status = console.status(
            f"[bold cyan]{self.message}[/bold cyan]",
            spinner=self.spinner
        )

        self.status.start()

        return self

    def __exit__(
        self,
        exc_type,
        exc_val,
        exc_tb
    ):

        self.status.stop()

        elapsed = (
            time.time()
            - self.start_time
        )

        console.print(
            f"[green]✓[/green] "
            f"{self.message} "
            f"[dim]({elapsed:.2f}s)[/dim]"
        )