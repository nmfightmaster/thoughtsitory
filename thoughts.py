#!/usr/bin/env python3
"""
Thoughtsitory - A CLI tool for managing modular AI conversation nodes.
"""

import typer
from datetime import datetime, timezone
from typing import List
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


@app.command()
def revert(
    node_id: str = typer.Argument(..., help="ID of the ThoughtNode to revert"),
    version: int = typer.Argument(..., help="Version number to revert to"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt"),
    list_versions: bool = typer.Option(False, "--list", "-l", help="List available versions before reverting")
):
    """Revert a ThoughtNode's content to a previously saved version."""
    from thoughtsitory.utils import load_thought_node, save_thought_node
    
    console.print(Panel.fit("Reverting ThoughtNode", style="bold blue"))
    
    # Load the node
    node = load_thought_node(node_id)
    if not node:
        print_error_message(f"ThoughtNode with ID '{node_id}' not found")
        raise typer.Exit(1)
    
    # List versions if requested
    if list_versions:
        console.print(f"\n[bold]Available versions for '{node.title}':[/bold]")
        if not node.versions:
            console.print("[yellow]No versions found. Create a snapshot first with 'thoughts snapshot'[/yellow]")
            return
        
        for version_info in node.versions:
            console.print(f"  Version {version_info['version']}: {version_info['summary']}")
            console.print(f"    Timestamp: {version_info['timestamp']}")
            if version_info.get('notes'):
                console.print(f"    Notes: {version_info['notes']}")
            console.print()
    
    # Validate version number
    if not node.versions:
        print_error_message("No versions found. Create a snapshot first with 'thoughts snapshot'")
        raise typer.Exit(1)
    
    # Find the specified version
    target_version = None
    for version_info in node.versions:
        if version_info['version'] == version:
            target_version = version_info
            break
    
    if not target_version:
        available_versions = [v['version'] for v in node.versions]
        print_error_message(f"Version {version} not found. Available versions: {available_versions}")
        raise typer.Exit(1)
    
    # Show revert details
    console.print(f"[bold]Node:[/bold] {node.title}")
    console.print(f"[bold]Current messages:[/bold] {len(node.content)}")
    console.print(f"[bold]Reverting to version:[/bold] {version}")
    console.print(f"[bold]Version summary:[/bold] {target_version['summary']}")
    if target_version.get('notes'):
        console.print(f"[bold]Version notes:[/bold] {target_version['notes']}")
    console.print(f"[bold]Version timestamp:[/bold] {target_version['timestamp']}")
    console.print(f"[bold]Messages in version:[/bold] {len(target_version['content_snapshot'])}")
    
    # Confirm revert unless --yes flag is used
    if not yes:
        if not Confirm.ask("Are you sure you want to revert? This will create a snapshot of the current state first."):
            console.print("[yellow]Revert cancelled.[/yellow]")
            return
    
    try:
        # Create a snapshot of current state before reverting
        pre_revert_summary = "Pre-revert snapshot"
        pre_revert_notes = f"Auto-created before reverting to version {version}"
        
        # Create the pre-revert snapshot
        pre_revert_version = node.create_snapshot(pre_revert_summary, pre_revert_notes)
        
        # Replace content with the target version's content
        node.content = []
        for msg_data in target_version['content_snapshot']:
            from thoughtsitory.models import Message
            node.content.append(Message.from_dict(msg_data))
        
        # Update timestamp
        node.updated_at = datetime.now(timezone.utc).isoformat()
        
        # Save the updated node
        file_path = save_thought_node(node)
        
        print_success_message(f"Successfully reverted to version {version}!")
        
        # Display confirmation details
        console.print(f"\n[bold]Revert completed:[/bold]")
        console.print(f"  Node: {node.title}")
        console.print(f"  Reverted to version: {version}")
        console.print(f"  Version timestamp: {target_version['timestamp']}")
        console.print(f"  Messages restored: {len(node.content)}")
        console.print(f"  Pre-revert snapshot created: Version {pre_revert_version}")
        console.print(f"[green]Saved to: {file_path}[/green]")
        
    except Exception as e:
        print_error_message(f"Failed to revert ThoughtNode: {e}")
        raise typer.Exit(1)


@app.command()
def compare(
    node_id: str = typer.Argument(..., help="ID of the ThoughtNode to compare"),
    version_a: int = typer.Argument(..., help="First version number to compare"),
    version_b: int = typer.Argument(..., help="Second version number to compare"),
    summaries: bool = typer.Option(False, "--summaries", "-s", help="Compare summaries instead of full content"),
    brief: bool = typer.Option(False, "--brief", "-b", help="Only show number of changes")
):
    """Compare two versions of a ThoughtNode to see content changes."""
    from thoughtsitory.utils import load_thought_node
    import difflib
    
    console.print(Panel.fit("Comparing ThoughtNode Versions", style="bold blue"))
    
    # Load the node
    node = load_thought_node(node_id)
    if not node:
        print_error_message(f"ThoughtNode with ID '{node_id}' not found")
        raise typer.Exit(1)
    
    # Validate that versions exist
    if not node.versions:
        print_error_message("No versions found. Create snapshots first with 'thoughts snapshot'")
        raise typer.Exit(1)
    
    # Find the specified versions
    version_a_data = None
    version_b_data = None
    
    for version_info in node.versions:
        if version_info['version'] == version_a:
            version_a_data = version_info
        if version_info['version'] == version_b:
            version_b_data = version_info
    
    if not version_a_data:
        available_versions = [v['version'] for v in node.versions]
        print_error_message(f"Version {version_a} not found. Available versions: {available_versions}")
        raise typer.Exit(1)
    
    if not version_b_data:
        available_versions = [v['version'] for v in node.versions]
        print_error_message(f"Version {version_b} not found. Available versions: {available_versions}")
        raise typer.Exit(1)
    
    # Display version information
    console.print(f"\n[bold]Node:[/bold] {node.title}")
    console.print(f"[bold]Comparing:[/bold] Version {version_a} vs Version {version_b}")
    console.print(f"[bold]Version {version_a}:[/bold] {version_a_data['summary']} ({version_a_data['timestamp']})")
    console.print(f"[bold]Version {version_b}:[/bold] {version_b_data['summary']} ({version_b_data['timestamp']})")
    
    # Extract content to compare
    if summaries:
        content_a = [version_a_data.get('summary', '')]
        content_b = [version_b_data.get('summary', '')]
        content_type = "summaries"
    else:
        # Extract message content from content_snapshot
        content_a = [msg['text'] for msg in version_a_data['content_snapshot']]
        content_b = [msg['text'] for msg in version_b_data['content_snapshot']]
        content_type = "messages"
    
    # Check if versions are identical
    if content_a == content_b:
        console.print(f"\n[green]✓ No changes found between versions {version_a} and {version_b}[/green]")
        return
    
    # Create diff
    if brief:
        # Count changes using a simpler approach
        added_lines = len(content_b) - len(content_a)
        removed_lines = 0
        
        # For more accurate counting, we'd need to do a proper diff analysis
        # For now, just show the difference in message count
        if added_lines > 0:
            console.print(f"\n[bold]Summary of changes:[/bold]")
            console.print(f"  Added {content_type}: {added_lines}")
            console.print(f"  Total changes: {added_lines}")
        elif added_lines < 0:
            console.print(f"\n[bold]Summary of changes:[/bold]")
            console.print(f"  Removed {content_type}: {abs(added_lines)}")
            console.print(f"  Total changes: {abs(added_lines)}")
        else:
            console.print(f"\n[bold]Summary of changes:[/bold]")
            console.print(f"  No changes in {content_type} count")
            console.print(f"  Total changes: 0")
        
    else:
        # Show detailed diff
        console.print(f"\n[bold]Detailed diff ({content_type}):[/bold]")
        
        if summaries:
            # For summaries, show a simple before/after
            console.print(f"\n[bold]Summary Comparison:[/bold]")
            console.print(f"[bold red]Version {version_a}:[/bold red] {content_a[0] if content_a else '(empty)'}")
            console.print(f"[bold green]Version {version_b}:[/bold green] {content_b[0] if content_b else '(empty)'}")
        else:
            # For messages, create a detailed diff
            diff = difflib.unified_diff(content_a, content_b, 
                                      fromfile=f"Version {version_a}", 
                                      tofile=f"Version {version_b}",
                                      lineterm='')
            
            diff_text = '\n'.join(diff)
            
            if diff_text.strip():
                # Format the diff with colors
                lines = diff_text.split('\n')
                for line in lines:
                    if line.startswith('+') and not line.startswith('+++'):
                        console.print(f"[green]{line}[/green]")
                    elif line.startswith('-') and not line.startswith('---'):
                        console.print(f"[red]{line}[/red]")
                    elif line.startswith('@'):
                        console.print(f"[blue]{line}[/blue]")
                    elif line.startswith('+++') or line.startswith('---'):
                        console.print(f"[dim]{line}[/dim]")
                    else:
                        console.print(line)
            else:
                console.print("[yellow]No differences found in content[/yellow]")


@app.command()
def search(
    title: str = typer.Option(None, "--title", "-t", help="Substring to match in node titles (case-insensitive)"),
    tag: List[str] = typer.Option(None, "--tag", "-g", help="Tag to search for (can be used multiple times)"),
    message: str = typer.Option(None, "--message", "-m", help="Substring to match in message content (case-insensitive)"),
    limit: int = typer.Option(10, "--limit", "-l", help="Maximum number of results to show")
):
    """Search ThoughtNodes by title, tags, or message content."""
    from thoughtsitory.utils import list_thought_nodes
    from rich.table import Table
    
    console.print(Panel.fit("Searching ThoughtNodes", style="bold blue"))
    
    # Load all nodes
    nodes = list_thought_nodes()
    
    if not nodes:
        console.print("[yellow]No ThoughtNodes found. Create some with 'thoughts create'[/yellow]")
        return
    
    # Filter nodes based on criteria
    filtered_nodes = []
    
    for node in nodes:
        matches = []
        node_matches = True
        
        # Check title filter
        if title:
            if title.lower() in node.title.lower():
                matches.append(f"Title contains '{title}'")
            else:
                node_matches = False
        
        # Check tag filter
        if tag:
            node_tags_lower = [t.lower() for t in node.tags]
            search_tags_lower = [t.lower() for t in tag]
            
            # Check if node has ALL of the search tags (AND logic)
            has_all_tags = all(search_tag in node_tags_lower for search_tag in search_tags_lower)
            if has_all_tags:
                matches.append(f"Has tags: {', '.join(tag)}")
            else:
                node_matches = False
        
        # Check message filter
        if message:
            message_found = False
            for msg in node.content:
                if message.lower() in msg.text.lower():
                    message_found = True
                    break
            
            if message_found:
                matches.append(f"Message contains '{message}'")
            else:
                node_matches = False
        
        # If no filters provided, include all nodes
        if not title and not tag and not message:
            node_matches = True
            matches.append("No filters applied")
        
        if node_matches:
            # Add match reasons to the node for display
            node.match_reasons = matches
            filtered_nodes.append(node)
    
    # Sort by updated_at (descending)
    filtered_nodes.sort(key=lambda x: x.updated_at, reverse=True)
    
    # Apply limit
    if limit > 0:
        filtered_nodes = filtered_nodes[:limit]
    
    # Display results
    if not filtered_nodes:
        console.print("[yellow]No ThoughtNodes match your search criteria.[/yellow]")
        console.print("\n[dim]Try:[/dim]")
        console.print("  • Use fewer or different search terms")
        console.print("  • Check spelling of tags")
        console.print("  • Use 'thoughts list' to see all available nodes")
        return
    
    # Create results table
    table = Table(title=f"Search Results ({len(filtered_nodes)} found)")
    table.add_column("Title", style="bold", width=30)
    table.add_column("ID", style="dim", width=36)
    table.add_column("Tags", style="green", width=20)
    table.add_column("Updated", style="cyan", width=20)
    table.add_column("Messages", style="yellow", width=10)
    table.add_column("Matches", style="blue", width=30)
    
    for node in filtered_nodes:
        # Truncate title if too long
        display_title = node.title[:27] + "..." if len(node.title) > 30 else node.title
        
        # Format tags
        tags_str = ", ".join(node.tags[:3])  # Show first 3 tags
        if len(node.tags) > 3:
            tags_str += f" (+{len(node.tags) - 3})"
        
        # Format updated date
        updated_date = node.updated_at.split("T")[0]  # Just the date part
        
        # Format match reasons
        match_reasons = "; ".join(node.match_reasons)
        if len(match_reasons) > 27:
            match_reasons = match_reasons[:24] + "..."
        
        table.add_row(
            display_title,
            node.id,
            tags_str,
            updated_date,
            str(len(node.content)),
            match_reasons
        )
    
    console.print(table)
    
    # Show summary
    if len(filtered_nodes) == limit and len(nodes) > limit:
        console.print(f"\n[dim]Showing first {limit} results. Use --limit to see more.[/dim]")


if __name__ == "__main__":
    app() 