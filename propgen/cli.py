"""Explicit operation CLI; JSON output may contain private CRM data."""

import json
from pathlib import Path

import typer

from .client import METHODS, Client, PropGenError, specification

app = typer.Typer(no_args_is_help=True)


@app.command()
def capabilities():
    """List all pinned documented operations without credentials."""
    for path, ops in specification()["paths"].items():
        for method, op in ops.items():
            if method in METHODS:
                typer.echo(f"{method.upper()} {path} — {op.get('summary', '')}")


@app.command()
def call(
    method: str,
    path: str,
    path_params: str = "{}",
    query: str = "{}",
    body_file: Path | None = None,
    headers: str = "{}",
    authorize_write: bool = False,
    confirm: bool = False,
    output: Path | None = None,
):
    """Call an exact documented template. Supply typed parameters as JSON objects."""
    try:
        with Client() as client:
            response = client.request(
                method,
                path,
                path_params=json.loads(path_params),
                query=json.loads(query),
                body=json.loads(body_file.read_text()) if body_file else None,
                headers=json.loads(headers),
                authorize_write=authorize_write,
                confirm=confirm,
            )
            if output:
                output.write_bytes(response.content)
                typer.echo("Response saved")
            else:
                typer.echo(response.text)
    except (PropGenError, ValueError, OSError):
        typer.echo(
            "Request failed. Check configuration, documented inputs, permissions and confirmation.",
            err=True,
        )
        raise typer.Exit(1) from None


@app.command()
def check_connection():
    """One read-only account request. Suppresses private response data."""
    try:
        with Client() as client:
            response = client.request("get", "/account")
            typer.echo(
                f"Account read authenticated and schema validated: HTTP {response.status_code}"
            )
    except PropGenError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(1) from None


if __name__ == "__main__":
    app()
