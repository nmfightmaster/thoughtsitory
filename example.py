#!/usr/bin/env python3
"""
Example script demonstrating Thoughtsitory usage.
"""

from thoughtsitory.models import ThoughtNode, MessageType
from thoughtsitory.utils import save_thought_node, print_node_summary, print_success_message

def main():
    """Demonstrate creating and managing ThoughtNodes programmatically."""
    
    # Create a new ThoughtNode
    node = ThoughtNode(title="Example AI Conversation")
    node.add_tag("example")
    node.add_tag("demo")
    
    # Add some conversation messages
    node.add_message(MessageType.USER, "What is the best way to learn Python?")
    node.add_message(MessageType.AI, "The best way to learn Python is to start with the basics and practice regularly. Here are some tips:\n\n1. Start with Python's official tutorial\n2. Work on small projects\n3. Use interactive platforms like Jupyter notebooks\n4. Join coding communities")
    node.add_message(MessageType.USER, "What about data science libraries?")
    node.add_message(MessageType.AI, "For data science in Python, focus on these key libraries:\n\n- NumPy: For numerical computing\n- Pandas: For data manipulation and analysis\n- Matplotlib/Seaborn: For data visualization\n- Scikit-learn: For machine learning\n\nStart with Pandas as it's most commonly used.")
    
    # Add a summary
    node.summary = "Discussion about learning Python and data science libraries, covering best practices and recommended tools."
    
    # Save the node
    file_path = save_thought_node(node)
    print_success_message(f"Example ThoughtNode created and saved!")
    print(f"File: {file_path}")
    
    # Show the summary
    print_node_summary(node)
    
    print("\n" + "="*50)
    print("You can now use the CLI to view this node:")
    print(f"python thoughts.py view {node.id}")
    print("="*50)

if __name__ == "__main__":
    main() 