import json
import os
from pathlib import Path
from typing import Optional, List
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .models import ThoughtNode

console = Console()


def ensure_data_directory() -> Path:
    """Ensure the data directory exists and return its path."""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    return data_dir


def save_thought_node(node: ThoughtNode) -> str:
    """Save a ThoughtNode to a JSON file in the data directory."""
    data_dir = ensure_data_directory()
    file_path = data_dir / f"{node.id}.json"
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(node.to_dict(), f, indent=2, ensure_ascii=False)
    
    return str(file_path)


def load_thought_node(node_id: str) -> Optional[ThoughtNode]:
    """Load a ThoughtNode from a JSON file by its ID."""
    data_dir = ensure_data_directory()
    file_path = data_dir / f"{node_id}.json"
    
    if not file_path.exists():
        return None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return ThoughtNode.from_dict(data)
    except (json.JSONDecodeError, KeyError) as e:
        console.print(f"[red]Error loading node {node_id}: {e}[/red]")
        return None


def list_thought_nodes() -> List[ThoughtNode]:
    """List all ThoughtNodes in the data directory."""
    data_dir = ensure_data_directory()
    nodes = []
    
    for json_file in data_dir.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            node = ThoughtNode.from_dict(data)
            nodes.append(node)
        except (json.JSONDecodeError, KeyError) as e:
            console.print(f"[red]Error loading {json_file.name}: {e}[/red]")
    
    return nodes


def delete_thought_node(node_id: str) -> bool:
    """Delete a ThoughtNode file by its ID."""
    data_dir = ensure_data_directory()
    file_path = data_dir / f"{node_id}.json"
    
    if file_path.exists():
        file_path.unlink()
        return True
    return False


def print_node_summary(node: ThoughtNode) -> None:
    """Print a formatted summary of a ThoughtNode."""
    # Create a rich panel with node information
    content = Text()
    content.append(f"ID: {node.id}\n", style="bold blue")
    content.append(f"Title: {node.title}\n", style="bold")
    content.append(f"Created: {node.created_at}\n", style="dim")
    content.append(f"Updated: {node.updated_at}\n", style="dim")
    
    if node.tags:
        content.append(f"Tags: {', '.join(node.tags)}\n", style="green")
    
    if node.summary:
        content.append(f"Summary: {node.summary}\n", style="italic")
    
    content.append(f"Messages: {len(node.content)}\n", style="yellow")
    content.append(f"Versions: {len(node.versions)}\n", style="yellow")
    
    # Links summary
    links_info = []
    if node.links["parents"]:
        links_info.append(f"Parents: {len(node.links['parents'])}")
    if node.links["forks"]:
        links_info.append(f"Forks: {len(node.links['forks'])}")
    if node.links["related"]:
        links_info.append(f"Related: {len(node.links['related'])}")
    
    if links_info:
        content.append(f"Links: {', '.join(links_info)}", style="cyan")
    
    panel = Panel(content, title="ThoughtNode Summary", border_style="blue")
    console.print(panel)


def print_success_message(message: str) -> None:
    """Print a success message with rich formatting."""
    console.print(f"[green]✓ {message}[/green]")


def print_error_message(message: str) -> None:
    """Print an error message with rich formatting."""
    console.print(f"[red]✗ {message}[/red]")


def print_info_message(message: str) -> None:
    """Print an info message with rich formatting."""
    console.print(f"[blue]ℹ {message}[/blue]") 