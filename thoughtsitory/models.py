from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid
from enum import Enum


class MessageType(Enum):
    USER = "user"
    AI = "ai"


@dataclass
class Message:
    """Represents a single message in a conversation."""
    type: MessageType
    text: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            "text": self.text,
            "timestamp": self.timestamp
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        return cls(
            type=MessageType(data["type"]),
            text=data["text"],
            timestamp=data["timestamp"]
        )


@dataclass
class ThoughtNode:
    """Represents a modular AI conversation node."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    content: List[Message] = field(default_factory=list)
    links: Dict[str, List[str]] = field(default_factory=lambda: {
        "parents": [],
        "forks": [],
        "related": []
    })
    versions: List[Dict[str, Any]] = field(default_factory=list)
    summary: str = ""
    
    def add_message(self, message_type: MessageType, text: str) -> None:
        """Add a new message to the conversation."""
        message = Message(type=message_type, text=text)
        self.content.append(message)
        self.updated_at = datetime.utcnow().isoformat()
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the node."""
        if tag not in self.tags:
            self.tags.append(tag)
            self.updated_at = datetime.utcnow().isoformat()
    
    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the node."""
        if tag in self.tags:
            self.tags.remove(tag)
            self.updated_at = datetime.utcnow().isoformat()
    
    def add_parent(self, parent_id: str) -> None:
        """Add a parent node link."""
        if parent_id not in self.links["parents"]:
            self.links["parents"].append(parent_id)
            self.updated_at = datetime.utcnow().isoformat()
    
    def add_fork(self, fork_id: str) -> None:
        """Add a fork node link."""
        if fork_id not in self.links["forks"]:
            self.links["forks"].append(fork_id)
            self.updated_at = datetime.utcnow().isoformat()
    
    def add_related(self, related_id: str) -> None:
        """Add a related node link."""
        if related_id not in self.links["related"]:
            self.links["related"].append(related_id)
            self.updated_at = datetime.utcnow().isoformat()
    
    def create_version(self, description: str = "") -> None:
        """Create a new version snapshot."""
        version = {
            "id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "description": description,
            "content": [msg.to_dict() for msg in self.content],
            "summary": self.summary
        }
        self.versions.append(version)
        self.updated_at = datetime.utcnow().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the ThoughtNode to a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "content": [msg.to_dict() for msg in self.content],
            "links": self.links,
            "versions": self.versions,
            "summary": self.summary
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ThoughtNode':
        """Create a ThoughtNode from a dictionary."""
        node = cls(
            id=data["id"],
            title=data["title"],
            tags=data["tags"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            links=data["links"],
            versions=data["versions"],
            summary=data["summary"]
        )
        
        # Convert content back to Message objects
        for msg_data in data["content"]:
            node.content.append(Message.from_dict(msg_data))
        
        return node 