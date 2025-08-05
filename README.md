# Thoughtsitory

A Python CLI tool for managing modular AI conversation nodes called **ThoughtNodes**.

## Features

- **Modular Conversation Management**: Create, view, and manage AI conversation nodes
- **Rich CLI Interface**: Beautiful console output with rich formatting
- **Flexible Data Model**: Support for messages, tags, links, and versioning
- **JSON Storage**: Simple file-based storage in JSON format
- **Extensible Architecture**: Easy to extend with new commands and features

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd thoughtsitory
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Commands

#### Create a new ThoughtNode
```bash
# Interactive mode
python thoughts.py create

# With title and tags
python thoughts.py create --title "My AI Conversation" --tags "ai,conversation,ideas"
```

#### List all ThoughtNodes
```bash
python thoughts.py list
```

#### View a specific ThoughtNode
```bash
python thoughts.py view <node-id>
```

#### Add a message to a ThoughtNode
```bash
# Interactive mode
python thoughts.py add-message <node-id> --type user

# With message text
python thoughts.py add-message <node-id> --type ai --text "Hello, how can I help you?"
```

#### Add a tag to a ThoughtNode
```bash
python thoughts.py add-tag <node-id> <tag>
```

### Data Model

Each **ThoughtNode** contains:

- **ID**: Unique UUID identifier
- **Title**: Human-readable title
- **Tags**: List of tags for categorization
- **Timestamps**: Created and updated timestamps
- **Content**: List of messages (user/AI conversations)
- **Links**: Relationships to other nodes (parents, forks, related)
- **Versions**: Version history snapshots
- **Summary**: Optional summary text

### Message Types

- **User Messages**: Human input in conversations
- **AI Messages**: AI responses in conversations

### File Structure

```
thoughtsitory/
├── thoughts.py              # Main CLI entrypoint
├── requirements.txt         # Python dependencies
├── README.md              # This file
├── thoughtsitory/         # Package directory
│   ├── __init__.py       # Package initialization
│   ├── models.py         # Data models (ThoughtNode, Message)
│   └── utils.py          # Utility functions
└── data/                 # Storage directory (created automatically)
    └── *.json           # ThoughtNode JSON files
```

## Development

### Project Structure

The project is organized for easy expansion:

- **`thoughtsitory/models.py`**: Core data models
- **`thoughtsitory/utils.py`**: File I/O and utility functions
- **`thoughts.py`**: CLI commands and user interface

### Adding New Commands

To add new commands, extend the `app` object in `thoughts.py`:

```python
@app.command()
def new_command():
    """Description of the new command."""
    # Implementation here
```

### Dependencies

- **typer**: Modern CLI framework
- **rich**: Beautiful terminal output
- **uuid**: UUID generation (built-in)

## Future Enhancements

Planned features for future versions:

- **Forking**: Create branches of conversations
- **Search**: Find nodes by content or tags
- **Export**: Export conversations in various formats
- **Import**: Import from other conversation formats
- **Graph Visualization**: Visualize node relationships
- **AI Integration**: Direct AI API integration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

---

**Thoughtsitory** - Organize your AI conversations, one thought at a time.
