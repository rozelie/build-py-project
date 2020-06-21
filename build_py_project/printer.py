from rich import print


def print_err(err: str):
    print_err(f"[red]{err}[/red]")


def print_info(info: str):
    print(info)


def print_green(title: str):
    print(f"[green]{title}[/green]")
