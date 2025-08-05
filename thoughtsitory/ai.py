"""
AI integration module for Thoughtsitory CLI.
Handles OpenAI API interactions for AI chat functionality.
"""

import os
import json
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from openai import OpenAI
from openai import AuthenticationError, RateLimitError, APIError
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from dotenv import load_dotenv

from .models import ThoughtNode, Message, MessageType

# Load environment variables from .env file
load_dotenv()

console = Console()


@dataclass
class AIConfig:
    """Configuration for AI integration."""
    api_key: str
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 1000
    temperature: float = 0.7
    context_messages: int = 10  # Number of recent messages to include as context


class AIService:
    """Service class for handling AI interactions."""
    
    def __init__(self, config: Optional[AIConfig] = None):
        """Initialize the AI service with configuration."""
        if config is None:
            config = self._load_config()
        
        self.config = config
        self._setup_openai()
    
    def _load_config(self) -> AIConfig:
        """Load AI configuration from environment variables."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required. "
                "Please set it with your OpenAI API key."
            )
        
        return AIConfig(
            api_key=api_key,
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "1000")),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
            context_messages=int(os.getenv("OPENAI_CONTEXT_MESSAGES", "10"))
        )
    
    def _setup_openai(self) -> None:
        """Setup OpenAI client with API key."""
        self.client = OpenAI(api_key=self.config.api_key)
    
    def _build_context_prompt(self, node: ThoughtNode) -> str:
        """Build a context prompt from the ThoughtNode's recent messages."""
        if not node.content:
            return f"This is a new conversation about: {node.title}"
        
        # Get recent messages for context
        recent_messages = node.content[-self.config.context_messages:]
        
        context_parts = [f"Conversation Title: {node.title}"]
        
        if node.tags:
            context_parts.append(f"Tags: {', '.join(node.tags)}")
        
        if node.summary:
            context_parts.append(f"Summary: {node.summary}")
        
        context_parts.append("\nRecent conversation:")
        
        for message in recent_messages:
            role = "User" if message.type == MessageType.USER else "AI"
            context_parts.append(f"{role}: {message.text}")
        
        return "\n".join(context_parts)
    
    def _build_system_prompt(self, node: ThoughtNode) -> str:
        """Build a system prompt for the AI."""
        system_prompt = """You are a helpful AI assistant participating in a conversation. 
Your responses should be:
- Relevant to the conversation context
- Helpful and informative
- Conversational and engaging
- Appropriate in length (not too long unless detailed explanation is needed)

The conversation context includes the title, tags, summary, and recent messages."""
        
        return system_prompt
    
    def chat_with_node(self, node: ThoughtNode, user_message: str) -> str:
        """
        Send a user message to the AI and get a response.
        
        Args:
            node: The ThoughtNode containing conversation context
            user_message: The user's message to send to the AI
            
        Returns:
            The AI's response as a string
            
        Raises:
            Exception: If there's an error with the API call
        """
        try:
            # Build the conversation context
            context_prompt = self._build_context_prompt(node)
            system_prompt = self._build_system_prompt(node)
            
            # Prepare messages for OpenAI API
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{context_prompt}\n\nUser: {user_message}"}
            ]
            
            # Make the API call
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature
            )
            
            # Extract the AI response
            ai_response = response.choices[0].message.content.strip()
            
            return ai_response
            
        except AuthenticationError:
            raise Exception("Invalid API key. Please check your OPENAI_API_KEY environment variable.")
        except RateLimitError:
            raise Exception("Rate limit exceeded. Please try again later.")
        except APIError as e:
            raise Exception(f"OpenAI API error: {e}")
        except Exception as e:
            raise Exception(f"Unexpected error during AI chat: {e}")
    
    def test_connection(self) -> bool:
        """Test the AI service connection."""
        try:
            # Make a simple test call
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            return True
        except AuthenticationError:
            raise Exception("Invalid API key. Please check your OPENAI_API_KEY.")
        except RateLimitError:
            raise Exception("Rate limit exceeded. Please try again later.")
        except APIError as e:
            raise Exception(f"OpenAI API error: {e}")
        except Exception as e:
            raise Exception(f"Connection error: {e}")


def print_ai_response(response: str, node_title: str) -> None:
    """Print the AI response with rich formatting."""
    content = Text()
    content.append("AI Response", style="bold green")
    content.append(f"\nNode: {node_title}\n", style="dim")
    content.append(response, style="white")
    
    panel = Panel(content, title="🤖 AI Reply", border_style="green")
    console.print(panel)


def print_ai_error(error: str) -> None:
    """Print AI error with rich formatting."""
    content = Text()
    content.append("AI Error", style="bold red")
    content.append(f"\n{error}", style="red")
    
    panel = Panel(content, title="❌ AI Error", border_style="red")
    console.print(panel)


def validate_ai_setup() -> bool:
    """Validate that AI integration is properly configured."""
    try:
        # Check if API key is set
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            console.print("[red]Error: OPENAI_API_KEY environment variable is not set.[/red]")
            console.print("[yellow]Please set it with: export OPENAI_API_KEY='your-api-key'[/yellow]")
            return False
        
        # Test the connection
        service = AIService()
        service.test_connection()
        console.print("[green]✓ AI integration is properly configured[/green]")
        return True
            
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return False 