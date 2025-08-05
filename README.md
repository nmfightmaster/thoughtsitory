# Thoughtsitory

A Python CLI tool for managing modular AI conversation nodes called **ThoughtNodes**.

## Features

- **Modular Conversation Management**: Create, view, and manage AI conversation nodes
- **AI Integration**: Direct OpenAI API integration for AI-powered conversations
- **Node Forking**: Duplicate and branch conversations while preserving relationships
- **Version Control**: Create snapshots and revert to previous versions with automatic backup
- **Powerful Search**: Find nodes by title, tags, or message content with AND logic
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

### AI Integration Setup

To use the AI chat functionality, you need to set up OpenAI API access:

1. **Get an OpenAI API Key**:
   - Sign up at [OpenAI](https://platform.openai.com/)
   - Navigate to API Keys section
   - Create a new API key

2. **Set the API Key**:
   ```bash
   # On Linux/macOS
   export OPENAI_API_KEY="your-api-key-here"
   
   # On Windows (PowerShell)
   $env:OPENAI_API_KEY="your-api-key-here"
   
   # On Windows (Command Prompt)
   set OPENAI_API_KEY=your-api-key-here
   ```

3. **Optional Environment Variables**:
   ```bash
   # Model to use (default: gpt-3.5-turbo)
   export OPENAI_MODEL="gpt-4"
   
   # Maximum tokens per response (default: 1000)
   export OPENAI_MAX_TOKENS="1500"
   
   # Temperature for response creativity (default: 0.7)
   export OPENAI_TEMPERATURE="0.8"
   
   # Number of recent messages to include as context (default: 10)
   export OPENAI_CONTEXT_MESSAGES="15"
   ```

4. **Test the Setup**:
   ```bash
   python thoughts.py ai-chat <node-id> --message "Hello"
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

#### Chat with AI using a ThoughtNode as context
```bash
# Interactive mode - prompts for message
python thoughts.py ai-chat <node-id>

# With message provided
python thoughts.py ai-chat <node-id> --message "What do you think about this topic?"

# Fork the node before chatting to preserve original
python thoughts.py ai-chat <node-id> --fork --message "Let's explore this further"

# Interactive mode with forking
python thoughts.py ai-chat <node-id> --fork
```

**AI Chat Features:**
- **Context Awareness**: AI receives the ThoughtNode's title, tags, summary, and recent conversation history
- **Automatic Versioning**: Creates a snapshot after each AI interaction
- **Fork Protection**: Use `--fork` flag to create a copy before chatting, preserving the original
- **Rich Output**: Beautiful formatting for AI responses with node context
- **Error Handling**: Comprehensive error handling for API issues, invalid keys, etc.
- **Environment Configuration**: Supports configurable models, tokens, and temperature via environment variables

**AI Chat Workflow:**
```bash
# 1. Create a conversation node
python thoughts.py create --title "Project Discussion" --tags "project,planning"
python thoughts.py add-message <node-id> --type user --text "Let's discuss the project scope"

# 2. Chat with AI (preserves original)
python thoughts.py ai-chat <node-id> --fork --message "What are the key considerations for this project?"

# 3. Continue the conversation
python thoughts.py ai-chat <node-id> --message "How should we prioritize the features?"

# 4. View the conversation
python thoughts.py view <node-id>
```

**Environment Variables for AI Configuration:**
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: Model to use (default: gpt-3.5-turbo)
- `OPENAI_MAX_TOKENS`: Maximum response length (default: 1000)
- `OPENAI_TEMPERATURE`: Response creativity (default: 0.7)
- `OPENAI_CONTEXT_MESSAGES`: Number of recent messages to include (default: 10)

#### Fork (duplicate) a ThoughtNode
```bash
# Interactive mode - prompts for title and notes
python thoughts.py fork <node-id>

# With title and notes
python thoughts.py fork <node-id> --title "Forked Conversation" --notes "Creating a new branch for testing"

# With just title (notes will be prompted)
python thoughts.py fork <node-id> --title "My Forked Node"
```

**Forking Features:**
- Creates a new ThoughtNode with a unique UUID
- Preserves all original content (messages, tags, metadata)
- Establishes parent-child relationships between original and forked nodes
- Allows adding explanatory notes about the fork reason
- Updates both nodes' link metadata automatically

**Example Fork Workflow:**
```bash
# 1. Create a conversation
python thoughts.py create --title "AI Project Discussion" --tags "project,ai,planning"

# 2. Add some messages
python thoughts.py add-message <node-id> --type user --text "Let's discuss the AI project scope"
python thoughts.py add-message <node-id> --type ai --text "I can help you plan the AI project..."

# 3. Fork the conversation for a different approach
python thoughts.py fork <node-id> --title "Alternative AI Approach" --notes "Exploring different implementation strategy"

# 4. Both nodes now have proper links and can be developed independently
```

#### Create a snapshot version of a ThoughtNode
```bash
# Interactive mode - prompts for summary and notes
python thoughts.py snapshot <node-id>

# With summary and notes
python thoughts.py snapshot <node-id> --summary "Version 1.0" --notes "Initial stable version"

# With just summary (notes will be prompted)
python thoughts.py snapshot <node-id> --summary "Before major changes"
```

**Snapshot Features:**
- Creates a versioned snapshot of the current conversation state
- Auto-increments version numbers (1, 2, 3, etc.)
- Preserves all messages in the `content_snapshot` field
- Allows adding summary labels and explanatory notes
- Updates the node's timestamp automatically
- Maintains version history in the node's `versions` array

**Example Snapshot Workflow:**
```bash
# 1. Create and populate a conversation
python thoughts.py create --title "Project Planning" --tags "planning,meeting"
python thoughts.py add-message <node-id> --type user --text "Let's plan the project timeline"
python thoughts.py add-message <node-id> --type ai --text "Here's a suggested timeline..."

# 2. Create a snapshot before making changes
python thoughts.py snapshot <node-id> --summary "Initial Plan" --notes "Baseline version before modifications"

# 3. Continue working on the conversation
python thoughts.py add-message <node-id> --type user --text "What about the budget?"

# 4. Create another snapshot
python thoughts.py snapshot <node-id> --summary "With Budget Discussion" --notes "Added budget considerations"
```

#### Revert a ThoughtNode to a previous version
```bash
# Interactive mode - prompts for confirmation
python thoughts.py revert <node-id> <version>

# Skip confirmation prompt
python thoughts.py revert <node-id> <version> --yes

# List available versions before reverting
python thoughts.py revert <node-id> <version> --list

# Combine options
python thoughts.py revert <node-id> <version> --list --yes
```

**Revert Features:**
- Restores a ThoughtNode's content to a previously saved version
- Automatically creates a "Pre-revert snapshot" of current state before reverting
- Validates version numbers and provides helpful error messages
- Shows detailed information about the target version before reverting
- Confirms action with user unless `--yes` flag is used
- Lists available versions with `--list` flag for easy reference

**Example Revert Workflow:**
```bash
# 1. Create snapshots during development
python thoughts.py create --title "Feature Development" --tags "development,feature"
python thoughts.py add-message <node-id> --type user --text "Let's implement user authentication"
python thoughts.py snapshot <node-id> --summary "Auth Start" --notes "Beginning authentication implementation"

# 2. Continue development
python thoughts.py add-message <node-id> --type ai --text "I'll help you implement OAuth2..."
python thoughts.py add-message <node-id> --type user --text "Actually, let's use JWT instead"
python thoughts.py snapshot <node-id> --summary "JWT Approach" --notes "Switched to JWT authentication"

# 3. List available versions
python thoughts.py revert <node-id> 1 --list

# 4. Revert to earlier version
python thoughts.py revert <node-id> 1 --yes
# This creates a pre-revert snapshot and restores the original content
```

#### Compare two versions of a ThoughtNode
```bash
# Compare full content between versions
python thoughts.py compare <node-id> <version-a> <version-b>

# Compare just the summaries
python thoughts.py compare <node-id> <version-a> <version-b> --summaries

# Show only a brief summary of changes
python thoughts.py compare <node-id> <version-a> <version-b> --brief

# Combine options
python thoughts.py compare <node-id> <version-a> <version-b> --summaries --brief
```

**Compare Features:**
- **Content Comparison**: Shows detailed diff of message content between versions
- **Summary Comparison**: Compare just the version summaries with `--summaries` flag
- **Brief Mode**: Show only change counts with `--brief` flag
- **Color-coded Output**: Added lines in green, removed lines in red
- **Version Validation**: Checks that both versions exist before comparing
- **Identical Detection**: Shows "No changes" message when versions are identical
- **Rich Display**: Shows version metadata (timestamps, summaries) before diff

**Example Compare Workflow:**
```bash
# 1. Create a conversation with multiple versions
python thoughts.py create --title "Project Planning" --tags "planning,meeting"
python thoughts.py add-message <node-id> --type user --text "Let's plan the project timeline"
python thoughts.py add-message <node-id> --type ai --text "Here's a suggested timeline..."
python thoughts.py snapshot <node-id> --summary "Initial Plan" --notes "Baseline version"

# 2. Add more content and create another version
python thoughts.py add-message <node-id> --type user --text "What about the budget?"
python thoughts.py add-message <node-id> --type ai --text "Budget considerations..."
python thoughts.py snapshot <node-id> --summary "With Budget" --notes "Added budget discussion"

# 3. Compare the versions
python thoughts.py compare <node-id> 1 2                    # Full content diff
python thoughts.py compare <node-id> 1 2 --brief           # Just change counts
python thoughts.py compare <node-id> 1 2 --summaries       # Compare summaries only
```

#### Search ThoughtNodes by title, tags, or message content
```bash
# Search by title (case-insensitive)
python thoughts.py search --title "boss fight"

# Search by tags (can use multiple --tag flags)
python thoughts.py search --tag design --tag combat

# Search by message content (case-insensitive)
python thoughts.py search --message "summarize"

# Combine search criteria (AND logic)
python thoughts.py search --title "combat" --tag enemy --message "range"

# Limit results
python thoughts.py search --tag game --limit 5
```

**Search Features:**
- **AND Logic**: All provided criteria must match (title AND tags AND message)
- **Case-insensitive**: Searches are not case-sensitive
- **Tag Matching**: Can search for multiple tags (node must have ALL specified tags)
- **Message Search**: Searches through all message content in conversations
- **Result Limiting**: Control number of results with `--limit` (default: 10)
- **Rich Display**: Shows results in a formatted table with match reasons
- **Helpful Errors**: Provides suggestions when no results are found

**Example Search Workflow:**
```bash
# 1. Create nodes with different content
python thoughts.py create --title "Game Design Discussion" --tags "game,design,combat"
python thoughts.py add-message <node-id> --type user --text "Let's discuss the boss fight mechanics"

python thoughts.py create --title "AI Project Planning" --tags "ai,planning,research"
python thoughts.py add-message <node-id> --type user --text "We need to summarize the research findings"

# 2. Search by different criteria
python thoughts.py search --title "Game"                    # Finds Game Design Discussion
python thoughts.py search --message "summarize"             # Finds AI Project Planning
python thoughts.py search --tag design --tag combat         # Finds Game Design Discussion
python thoughts.py search --title "Game" --tag design       # Finds Game Design Discussion
python thoughts.py search --title "Game" --tag research     # No results (AND logic)
```

#### Export ThoughtNodes as a graph
```bash
# Export all ThoughtNodes as a graph JSON file
python thoughts.py export

# Alternative short form
python thoughts.py export -g
```

**Export Features:**
- **Graph Format**: Exports ThoughtNodes as a JSON graph with nodes and edges
- **Relationship Mapping**: Converts ThoughtNode links to graph edges with types
- **Duplicate Prevention**: Avoids duplicate edges (e.g., if A links to B and B links to A)
- **Summary Truncation**: Truncates summaries over 150 characters for readability
- **Existing Node Validation**: Only includes edges that point to existing nodes
- **Rich Output**: Shows success message with output path and statistics

**Graph Structure:**
The exported `data/graph.json` file contains:
- **nodes**: Array of ThoughtNode data with id, title, and summary
- **edges**: Array of relationship data with source, target, and type

**Edge Types:**
- **parent**: Links from child to parent nodes (from `links["parents"]`)
- **fork**: Links from original to forked nodes (from `links["forks"]`)
- **related**: Links between related nodes (from `links["related"]`)

**Example Export Workflow:**
```bash
# 1. Create a network of related nodes
python thoughts.py create --title "Main Project Discussion" --tags "project,main"
python thoughts.py add-message <node-id-1> --type user --text "Let's start the main project"

# 2. Fork the main discussion
python thoughts.py fork <node-id-1> --title "UI Design Branch" --notes "Exploring UI design options"
python thoughts.py add-message <node-id-2> --type user --text "What about the user interface?"

# 3. Create a related discussion
python thoughts.py create --title "Backend Architecture" --tags "backend,architecture"
python thoughts.py add-message <node-id-3> --type user --text "Let's discuss the backend design"

# 4. Export the graph
python thoughts.py export
# Output: data/graph.json with nodes and edges
```

**Graph JSON Example:**
```json
{
  "nodes": [
    {
      "id": "1234abcd-5678-efgh-ijkl-mnopqrstuvwx",
      "title": "Main Project Discussion",
      "summary": "Initial project planning discussion"
    },
    {
      "id": "5678efgh-9abc-def0-ghij-klmnopqrstuv",
      "title": "UI Design Branch",
      "summary": "Forked from Main Project Discussion. Reason: Exploring UI design options"
    }
  ],
  "edges": [
    {
      "source": "5678efgh-9abc-def0-ghij-klmnopqrstuv",
      "target": "1234abcd-5678-efgh-ijkl-mnopqrstuvwx",
      "type": "parent"
    },
    {
      "source": "1234abcd-5678-efgh-ijkl-mnopqrstuvwx",
      "target": "5678efgh-9abc-def0-ghij-klmnopqrstuv",
      "type": "fork"
    }
  ]
}
```

#### Visualize ThoughtNodes and their relationships
```bash
# Show forest of all top-level nodes (nodes without parents)
python thoughts.py visualize

# Show subtree rooted at a specific node
python thoughts.py visualize --node-id 1234abcd

# Alternative short form
python thoughts.py visualize -n 1234abcd
```

**Visualize Features:**
- **Hierarchical Tree View**: Displays nodes in a tree structure using `rich.tree`
- **Relationship Types**: Different icons and colors for parents (📤), forks (🌿), and related nodes (🔗)
- **Forest Mode**: Shows all top-level nodes when no `--node-id` is provided
- **Subtree Mode**: Shows the complete subtree when a specific node ID is given
- **Cycle Detection**: Handles circular references gracefully with cycle detection
- **Missing Node Handling**: Shows warnings for broken links to non-existent nodes
- **Summary Statistics**: Displays counts of total nodes and relationship types
- **Truncated Display**: Long titles are truncated for better readability
- **Short IDs**: Shows first 8 characters of UUIDs for compact display

**Tree Output Features:**
- **Node Labels**: Title (truncated if needed), short ID, and tags
- **Color Coding**: Different colors for different relationship types
- **Icons**: Visual indicators for parents (📤), forks (🌿), and related nodes (🔗)
- **Depth Limiting**: Prevents infinite recursion with maximum depth protection
- **Cycle Detection**: Shows cycle warnings to prevent infinite loops

**Example Visualize Workflow:**
```bash
# 1. Create a network of related nodes
python thoughts.py create --title "Main Project Discussion" --tags "project,main"
python thoughts.py add-message <node-id-1> --type user --text "Let's start the main project"

# 2. Fork the main discussion
python thoughts.py fork <node-id-1> --title "UI Design Branch" --notes "Exploring UI design options"
python thoughts.py add-message <node-id-2> --type user --text "What about the user interface?"

# 3. Create a related discussion
python thoughts.py create --title "Backend Architecture" --tags "backend,architecture"
python thoughts.py add-message <node-id-3> --type user --text "Let's discuss the backend design"

# 4. Visualize the entire network
python thoughts.py visualize                    # Shows forest of all top-level nodes
python thoughts.py visualize -n <node-id-1>   # Shows subtree from main project
python thoughts.py visualize -n <node-id-2>   # Shows subtree from UI branch
```

**Tree Output Example:**
```
🌲 ThoughtNodes Forest
├── 📤 Parents:
│   └── 🌳 Main Project Discussion (1234abcd) [project,main]
│       └── 🌿 Forks:
│           └── 🌳 UI Design Branch (5678efgh) [project,main]
└── 🌳 Backend Architecture (9abcdef0) [backend,architecture]
```

### Data Model

Each **ThoughtNode** contains:

- **ID**: Unique UUID identifier
- **Title**: Human-readable title
- **Tags**: List of tags for categorization
- **Timestamps**: Created and updated timestamps
- **Content**: List of messages (user/AI conversations)
- **Links**: Relationships to other nodes
  - **Parents**: Original nodes that this node was forked from
  - **Forks**: Nodes that were forked from this node
  - **Related**: Other related nodes
- **Versions**: Version history snapshots with auto-incremented version numbers
- **Summary**: Optional summary text

### Message Types

- **User Messages**: Human input in conversations
- **AI Messages**: AI responses in conversations

### Version Structure

Each version snapshot contains:
- **version**: Auto-incremented integer (1, 2, 3, etc.)
- **timestamp**: ISO format UTC timestamp when snapshot was created
- **summary**: Short label describing the version
- **notes**: Optional explanation of the version's purpose
- **content_snapshot**: Deep copy of all messages at the time of snapshot

**Important Note**: When using the `revert` command, a "Pre-revert snapshot" is automatically created before restoring the target version. This ensures you can always recover the state that existed before the revert operation.

### Versioning Workflow

The versioning system provides a complete workflow for managing conversation history:

1. **Create Snapshots**: Use `snapshot` to save the current state with a summary and notes
2. **Compare Versions**: Use `compare` to see differences between any two versions
3. **Revert Changes**: Use `revert` to restore a previous version (with automatic backup)

**Example Versioning Workflow:**
```bash
# 1. Create and develop a conversation
python thoughts.py create --title "Feature Planning" --tags "planning,feature"
python thoughts.py add-message <node-id> --type user --text "Let's plan the user interface"
python thoughts.py add-message <node-id> --type ai --text "I suggest a clean, minimal design..."
python thoughts.py snapshot <node-id> --summary "Initial UI Plan" --notes "First draft of UI design"

# 2. Continue development
python thoughts.py add-message <node-id> --type user --text "What about mobile responsiveness?"
python thoughts.py add-message <node-id> --type ai --text "Mobile-first design is essential..."
python thoughts.py snapshot <node-id> --summary "Mobile Considerations" --notes "Added mobile design requirements"

# 3. Compare the versions to see what changed
python thoughts.py compare <node-id> 1 2

# 4. If needed, revert to the earlier version
python thoughts.py revert <node-id> 1 --yes
```

### File Structure

```
thoughtsitory/
├── thoughts.py              # Main CLI entrypoint
├── requirements.txt         # Python dependencies
├── README.md              # This file
├── thoughtsitory/         # Package directory
│   ├── __init__.py       # Package initialization
│   ├── models.py         # Data models (ThoughtNode, Message)
│   ├── ai.py             # AI integration (OpenAI API)
│   └── utils.py          # Utility functions
└── data/                 # Storage directory (created automatically)
    └── *.json           # ThoughtNode JSON files
```

## Development

### Project Structure

The project is organized for easy expansion:

- **`thoughtsitory/models.py`**: Core data models
- **`thoughtsitory/ai.py`**: AI integration and OpenAI API handling
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
- **openai**: OpenAI API integration
- **uuid**: UUID generation (built-in)

## Future Enhancements

Planned features for future versions:

- **Search**: Find nodes by content or tags
- **Export**: Export conversations in various formats
- **Import**: Import from other conversation formats
- **Graph Visualization**: Visualize node relationships
- **Version Management**: Advanced version control for ThoughtNodes
- **Collaboration**: Multi-user support and sharing

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
