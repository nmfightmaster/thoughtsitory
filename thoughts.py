#!/usr/bin/env python3
"""
Thoughtsitory - A CLI tool for managing modular AI conversation nodes.
"""

import typer
from datetime import datetime, timezone
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.text import Text

from thoughtsitory.models import ThoughtNode, MessageType
from thoughtsitory.utils import save_thought_node, print_node_summary, print_success_message, print_error_message

app = typer.Typer(
    name="thoughts",
    help="Thoughtsitory - Manage modular AI conversation nodes",
    add_completion=False
)
console = Console()


@app.command()
def create(
    title: str = typer.Option(None, "--title", "-t", help="Title for the new thought node"),
    tags: str = typer.Option(None, "--tags", help="Comma-separated tags for the node")
):
    """Create a new ThoughtNode."""
    console.print(Panel.fit("Creating New ThoughtNode", style="bold blue"))
    
    # Get title if not provided
    if not title:
        title = Prompt.ask("Enter a title for your thought node")
    
    if not title.strip():
        print_error_message("Title cannot be empty")
        raise typer.Exit(1)
    
    # Get tags if not provided
    tag_list = []
    if tags:
        tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
    else:
        tags_input = Prompt.ask("Enter tags (comma-separated, optional)", default="")
        if tags_input.strip():
            tag_list = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
    
    # Create the ThoughtNode
    node = ThoughtNode(title=title.strip())
    
    # Add tags
    for tag in tag_list:
        node.add_tag(tag)
    
    # Save the node
    try:
        file_path = save_thought_node(node)
        print_success_message(f"ThoughtNode created successfully!")
        console.print(f"Saved to: {file_path}")
        
        # Show summary
        print_node_summary(node)
        
    except Exception as e:
        print_error_message(f"Failed to create ThoughtNode: {e}")
        raise typer.Exit(1)


@app.command()
def list():
    """List all ThoughtNodes."""
    from thoughtsitory.utils import list_thought_nodes
    
    console.print(Panel.fit("Listing ThoughtNodes", style="bold blue"))
    
    nodes = list_thought_nodes()
    
    if not nodes:
        console.print("[yellow]No ThoughtNodes found. Create one with 'thoughts create'[/yellow]")
        return
    
    for i, node in enumerate(nodes, 1):
        console.print(f"\n[bold]{i}.[/bold] {node.title}")
        console.print(f"   ID: {node.id}")
        console.print(f"   Tags: {', '.join(node.tags) if node.tags else 'None'}")
        console.print(f"   Messages: {len(node.content)}")
        console.print(f"   Updated: {node.updated_at}")


@app.command()
def view(
    node_id: str = typer.Argument(..., help="ID of the ThoughtNode to view")
):
    """View a specific ThoughtNode."""
    from thoughtsitory.utils import load_thought_node
    
    console.print(Panel.fit("Viewing ThoughtNode", style="bold blue"))
    
    node = load_thought_node(node_id)
    if not node:
        print_error_message(f"ThoughtNode with ID '{node_id}' not found")
        raise typer.Exit(1)
    
    print_node_summary(node)
    
    # Show conversation content
    if node.content:
        console.print("\n[bold]Conversation:[/bold]")
        for i, message in enumerate(node.content, 1):
            role = "User" if message.type == MessageType.USER else "AI"
            console.print(f"{i}. [{role}] {message.text}")
    else:
        console.print("\n[yellow]No messages yet. Add some with 'thoughts add-message'[/yellow]")


@app.command()
def add_message(
    node_id: str = typer.Argument(..., help="ID of the ThoughtNode"),
    message_type: str = typer.Option(..., "--type", "-t", help="Message type: user or ai"),
    text: str = typer.Option(None, "--text", help="Message text")
):
    """Add a message to a ThoughtNode."""
    from thoughtsitory.utils import load_thought_node, save_thought_node
    
    console.print(Panel.fit("Adding Message", style="bold blue"))
    
    # Validate message type
    try:
        msg_type = MessageType(message_type.lower())
    except ValueError:
        print_error_message("Message type must be 'user' or 'ai'")
        raise typer.Exit(1)
    
    # Load the node
    node = load_thought_node(node_id)
    if not node:
        print_error_message(f"ThoughtNode with ID '{node_id}' not found")
        raise typer.Exit(1)
    
    # Get message text if not provided
    if not text:
        text = Prompt.ask(f"Enter {message_type} message")
    
    if not text.strip():
        print_error_message("Message text cannot be empty")
        raise typer.Exit(1)
    
    # Add the message
    node.add_message(msg_type, text.strip())
    
    # Save the updated node
    try:
        save_thought_node(node)
        print_success_message(f"Message added to '{node.title}'")
        
    except Exception as e:
        print_error_message(f"Failed to save ThoughtNode: {e}")
        raise typer.Exit(1)


@app.command()
def add_tag(
    node_id: str = typer.Argument(..., help="ID of the ThoughtNode"),
    tag: str = typer.Argument(..., help="Tag to add")
):
    """Add a tag to a ThoughtNode."""
    from thoughtsitory.utils import load_thought_node, save_thought_node
    
    console.print(Panel.fit("Adding Tag", style="bold blue"))
    
    node = load_thought_node(node_id)
    if not node:
        print_error_message(f"ThoughtNode with ID '{node_id}' not found")
        raise typer.Exit(1)
    
    node.add_tag(tag)
    
    try:
        save_thought_node(node)
        print_success_message(f"Tag '{tag}' added to '{node.title}'")
        
    except Exception as e:
        print_error_message(f"Failed to save ThoughtNode: {e}")
        raise typer.Exit(1)


@app.command()
def fork(
    node_id: str = typer.Argument(..., help="ID of the ThoughtNode to fork"),
    title: str = typer.Option(None, "--title", "-t", help="Title for the forked node"),
    notes: str = typer.Option(None, "--notes", "-n", help="Notes explaining the fork reason")
):
    """Fork (duplicate) an existing ThoughtNode with a new ID and title."""
    from thoughtsitory.utils import load_thought_node, save_thought_node
    
    console.print(Panel.fit("Forking ThoughtNode", style="bold blue"))
    
    # Load the original node
    original_node = load_thought_node(node_id)
    if not original_node:
        print_error_message(f"ThoughtNode with ID '{node_id}' not found")
        raise typer.Exit(1)
    
    # Get title for the forked node
    if not title:
        title = Prompt.ask("Enter a title for the forked node")
    
    if not title.strip():
        print_error_message("Title cannot be empty")
        raise typer.Exit(1)
    
    # Create the forked node
    forked_node = ThoughtNode(title=title.strip())
    
    # Copy content from original node
    forked_node.content = original_node.content.copy()
    
    # Copy tags from original node
    forked_node.tags = original_node.tags.copy()
    
    # Copy summary from original node
    forked_node.summary = original_node.summary
    
    # Add the original node as a parent
    forked_node.add_parent(original_node.id)
    
    # Add notes/reason if provided
    if notes:
        forked_node.summary = f"Forked from {original_node.title}. Reason: {notes}"
    else:
        # Get notes interactively if not provided
        notes_input = Prompt.ask("Add notes explaining the fork reason (optional)", default="")
        if notes_input.strip():
            forked_node.summary = f"Forked from {original_node.title}. Reason: {notes_input.strip()}"
        else:
            forked_node.summary = f"Forked from {original_node.title}"
    
    # Add the forked node to the original node's forks
    original_node.add_fork(forked_node.id)
    
    # Save both nodes
    try:
        original_file_path = save_thought_node(original_node)
        forked_file_path = save_thought_node(forked_node)
        
        print_success_message(f"ThoughtNode forked successfully!")
        
        # Show summary of both nodes
        console.print("\n[bold]Original Node:[/bold]")
        print_node_summary(original_node)
        
        console.print("\n[bold]Forked Node:[/bold]")
        print_node_summary(forked_node)
        
        console.print(f"\n[green]Original saved to: {original_file_path}[/green]")
        console.print(f"[green]Forked saved to: {forked_file_path}[/green]")
        
    except Exception as e:
        print_error_message(f"Failed to fork ThoughtNode: {e}")
        raise typer.Exit(1)


@app.command()
def snapshot(
    node_id: str = typer.Argument(..., help="ID of the ThoughtNode to snapshot"),
    summary: str = typer.Option(None, "--summary", "-s", help="Summary label for this version"),
    notes: str = typer.Option(None, "--notes", "-n", help="Notes explaining this version's purpose")
):
    """Create a snapshot version of a ThoughtNode's current state."""
    from thoughtsitory.utils import load_thought_node, save_thought_node
    
    console.print(Panel.fit("Creating Snapshot", style="bold blue"))
    
    # Load the node
    node = load_thought_node(node_id)
    if not node:
        print_error_message(f"ThoughtNode with ID '{node_id}' not found")
        raise typer.Exit(1)
    
    # Get summary if not provided
    if not summary:
        summary = Prompt.ask("Enter a summary label for this version")
    
    if not summary.strip():
        print_error_message("Summary cannot be empty")
        raise typer.Exit(1)
    
    # Get notes if not provided
    if not notes:
        notes_input = Prompt.ask("Enter notes explaining this version's purpose (optional)", default="")
        notes = notes_input.strip()
    
    # Create the snapshot
    try:
        version_number = node.create_snapshot(summary.strip(), notes)
        
        # Save the updated node
        file_path = save_thought_node(node)
        
        print_success_message(f"Snapshot created successfully!")
        
        # Display snapshot details
        console.print(f"\n[bold]Node:[/bold] {node.title}")
        console.print(f"[bold]Version:[/bold] {version_number}")
        console.print(f"[bold]Timestamp:[/bold] {datetime.now(timezone.utc).isoformat()}")
        console.print(f"[bold]Summary:[/bold] {summary.strip()}")
        if notes:
            console.print(f"[bold]Notes:[/bold] {notes}")
        console.print(f"[bold]Messages in snapshot:[/bold] {len(node.content)}")
        console.print(f"[green]Saved to: {file_path}[/green]")
        
    except Exception as e:
        print_error_message(f"Failed to create snapshot: {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app() 