"""
Base document generation agent.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from app.models.tabletop import Tabletop
from app.models.document import DocumentType


@dataclass
class DocumentContent:
    """Generated document content structure."""
    title: str
    description: str
    content: str
    learning_goals: str


class BaseDocumentAgent(ABC):
    """
    Base class for document generation agents.

    Each agent specializes in creating a specific type of document
    for tabletop exercises. The agent follows a structured approach:
    1. Generate document description
    2. Create main content
    3. Define learning goals
    """

    def __init__(self):
        self.name = self.__class__.__name__

    @property
    @abstractmethod
    def document_type(self) -> DocumentType:
        """The type of document this agent generates."""
        pass

    @property
    @abstractmethod
    def role_description(self) -> str:
        """Description of the agent's role/persona."""
        pass

    @property
    @abstractmethod
    def document_purpose(self) -> str:
        """Description of the document's purpose."""
        pass

    def build_context(self, tabletop: Tabletop) -> str:
        """Build context from tabletop data for the LLM."""
        context_parts = [
            f"# Tabletop Exercise: {tabletop.title}",
            "",
        ]

        if tabletop.description:
            context_parts.extend([
                "## Description",
                tabletop.description,
                "",
            ])

        if tabletop.story_prompt:
            context_parts.extend([
                "## Initial Story Prompt",
                tabletop.story_prompt,
                "",
            ])

        # Add questions and answers
        for question in tabletop.questions:
            if question.answer:
                context_parts.extend([
                    f"## {question.question_type.value.replace('_', ' ').title()}",
                    f"**Question:** {question.question_text}",
                    "",
                    f"**Answer:** {question.answer}",
                    "",
                ])

        return "\n".join(context_parts)

    def generate_description_prompt(self, tabletop: Tabletop) -> str:
        """Generate prompt for creating document description."""
        context = self.build_context(tabletop)
        return f"""
{self.role_description}

Based on the following tabletop exercise information, write a brief description
(2-3 sentences) of what this {self.document_purpose} will contain and how it
will be used.

{context}

Write ONLY the description, nothing else.
"""

    def generate_content_prompt(self, tabletop: Tabletop) -> str:
        """Generate prompt for creating main document content."""
        context = self.build_context(tabletop)
        return f"""
{self.role_description}

Based on the following tabletop exercise information, create the main content
for a {self.document_purpose}.

{context}

{self.get_content_guidelines()}

Create comprehensive, well-structured content. Use markdown formatting.
"""

    def generate_learning_goals_prompt(self, tabletop: Tabletop) -> str:
        """Generate prompt for creating learning goals."""
        context = self.build_context(tabletop)
        return f"""
{self.role_description}

Based on the following tabletop exercise information, create a list of
learning goals for this {self.document_purpose}.

{context}

Create 4-6 specific, measurable learning objectives. Format as a numbered list.
Each goal should describe what participants will learn, understand, or be able to do.
"""

    @abstractmethod
    def get_content_guidelines(self) -> str:
        """Get specific content guidelines for this document type."""
        pass

    async def generate(
        self,
        tabletop: Tabletop,
        llm_service: "LLMService"
    ) -> DocumentContent:
        """
        Generate all document content sections.

        Args:
            tabletop: The tabletop exercise to generate content for
            llm_service: The LLM service for generating content

        Returns:
            DocumentContent with all sections populated
        """
        # Generate title
        title = self.generate_title(tabletop)

        # Generate description
        description_prompt = self.generate_description_prompt(tabletop)
        description = await llm_service.generate(description_prompt)

        # Generate main content
        content_prompt = self.generate_content_prompt(tabletop)
        content = await llm_service.generate(content_prompt)

        # Generate learning goals
        goals_prompt = self.generate_learning_goals_prompt(tabletop)
        learning_goals = await llm_service.generate(goals_prompt)

        return DocumentContent(
            title=title,
            description=description,
            content=content,
            learning_goals=learning_goals,
        )

    def generate_title(self, tabletop: Tabletop) -> str:
        """Generate document title based on tabletop and document type."""
        doc_type_name = self.document_type.value.replace("_", " ").title()
        return f"{tabletop.title} - {doc_type_name}"
