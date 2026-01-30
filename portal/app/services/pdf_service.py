"""
PDF generation service for creating document files.
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.config import settings


class PDFService:
    """
    Service for generating PDF documents from content.

    Uses ReportLab for PDF generation with support for:
    - Markdown-like formatting
    - Multiple sections
    - Professional styling
    """

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or settings.PDF_OUTPUT_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_pdf(
        self,
        title: str,
        description: str,
        content: str,
        learning_goals: str,
        filename: Optional[str] = None,
    ) -> str:
        """
        Generate a PDF document with the provided content.

        Args:
            title: Document title
            description: Document description
            content: Main content (markdown supported)
            learning_goals: Learning goals section
            filename: Optional custom filename

        Returns:
            Path to the generated PDF file
        """
        try:
            from reportlab.lib import colors
            from reportlab.lib.pagesizes import letter
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch
            from reportlab.platypus import (
                SimpleDocTemplate,
                Paragraph,
                Spacer,
                Table,
                TableStyle,
                PageBreak,
            )
        except ImportError:
            raise ImportError("reportlab package not installed. Run: pip install reportlab")

        # Generate filename if not provided
        if not filename:
            safe_title = "".join(c if c.isalnum() or c in " -_" else "" for c in title)
            safe_title = safe_title.replace(" ", "_")[:50]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_title}_{timestamp}.pdf"

        filepath = self.output_dir / filename

        # Create document
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72,
        )

        # Styles
        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.HexColor("#1a1a2e"),
        )

        heading_style = ParagraphStyle(
            "CustomHeading",
            parent=styles["Heading2"],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=12,
            textColor=colors.HexColor("#16213e"),
        )

        subheading_style = ParagraphStyle(
            "CustomSubheading",
            parent=styles["Heading3"],
            fontSize=14,
            spaceBefore=15,
            spaceAfter=8,
            textColor=colors.HexColor("#0f3460"),
        )

        body_style = ParagraphStyle(
            "CustomBody",
            parent=styles["Normal"],
            fontSize=11,
            leading=16,
            spaceAfter=12,
        )

        description_style = ParagraphStyle(
            "Description",
            parent=styles["Normal"],
            fontSize=12,
            leading=18,
            spaceAfter=20,
            textColor=colors.HexColor("#4a4a4a"),
            borderColor=colors.HexColor("#e0e0e0"),
            borderWidth=1,
            borderPadding=10,
            backColor=colors.HexColor("#f8f9fa"),
        )

        # Build document content
        story = []

        # Title
        story.append(Paragraph(self._escape_html(title), title_style))
        story.append(Spacer(1, 0.25 * inch))

        # Description box
        story.append(Paragraph("Overview", heading_style))
        story.append(Paragraph(self._escape_html(description), description_style))
        story.append(Spacer(1, 0.25 * inch))

        # Learning Goals
        story.append(Paragraph("Learning Goals", heading_style))
        goals_content = self._markdown_to_paragraphs(learning_goals, body_style)
        story.extend(goals_content)
        story.append(Spacer(1, 0.25 * inch))

        # Main Content
        story.append(PageBreak())
        story.append(Paragraph("Document Content", heading_style))
        story.append(Spacer(1, 0.15 * inch))

        content_paragraphs = self._markdown_to_paragraphs(
            content, body_style, heading_style, subheading_style
        )
        story.extend(content_paragraphs)

        # Footer info
        story.append(Spacer(1, 0.5 * inch))
        footer_style = ParagraphStyle(
            "Footer",
            parent=styles["Normal"],
            fontSize=9,
            textColor=colors.HexColor("#888888"),
        )
        story.append(Paragraph(
            f"Generated by OWASP Zombies on Fire Tabletop Portal | {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            footer_style
        ))

        # Build PDF
        doc.build(story)

        return str(filepath)

    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    def _markdown_to_paragraphs(
        self,
        content: str,
        body_style,
        heading_style=None,
        subheading_style=None,
    ) -> list:
        """
        Convert markdown-like content to ReportLab paragraphs.

        Handles:
        - ## Headings
        - ### Subheadings
        - **bold** text
        - *italic* text
        - - Bullet points
        - Numbered lists
        """
        from reportlab.platypus import Paragraph, Spacer, ListFlowable, ListItem
        from reportlab.lib.units import inch

        elements = []
        lines = content.split("\n")
        current_list = []
        in_list = False

        for line in lines:
            line = line.strip()

            if not line:
                if in_list and current_list:
                    elements.append(self._create_list(current_list, body_style))
                    current_list = []
                    in_list = False
                elements.append(Spacer(1, 0.1 * inch))
                continue

            # Headings
            if line.startswith("### ") and subheading_style:
                if in_list and current_list:
                    elements.append(self._create_list(current_list, body_style))
                    current_list = []
                    in_list = False
                elements.append(Paragraph(self._escape_html(line[4:]), subheading_style))
                continue

            if line.startswith("## ") and heading_style:
                if in_list and current_list:
                    elements.append(self._create_list(current_list, body_style))
                    current_list = []
                    in_list = False
                elements.append(Paragraph(self._escape_html(line[3:]), heading_style))
                continue

            if line.startswith("# ") and heading_style:
                if in_list and current_list:
                    elements.append(self._create_list(current_list, body_style))
                    current_list = []
                    in_list = False
                elements.append(Paragraph(self._escape_html(line[2:]), heading_style))
                continue

            # Bullet points
            if line.startswith("- ") or line.startswith("* "):
                in_list = True
                current_list.append(("bullet", line[2:]))
                continue

            # Numbered lists
            if len(line) > 2 and line[0].isdigit() and line[1] in ".)":
                in_list = True
                current_list.append(("number", line[2:].strip()))
                continue

            # Regular paragraph
            if in_list and current_list:
                elements.append(self._create_list(current_list, body_style))
                current_list = []
                in_list = False

            # Process inline formatting
            formatted_line = self._process_inline_formatting(line)
            elements.append(Paragraph(formatted_line, body_style))

        # Handle any remaining list
        if current_list:
            elements.append(self._create_list(current_list, body_style))

        return elements

    def _create_list(self, items: list, style) -> "ListFlowable":
        """Create a list flowable from items."""
        from reportlab.platypus import ListFlowable, ListItem, Paragraph

        list_items = []
        for item_type, text in items:
            formatted = self._process_inline_formatting(text)
            list_items.append(ListItem(Paragraph(formatted, style)))

        bullet_type = "bullet" if items[0][0] == "bullet" else "1"
        return ListFlowable(list_items, bulletType=bullet_type, leftIndent=20)

    def _process_inline_formatting(self, text: str) -> str:
        """Process inline markdown formatting."""
        import re

        # Escape HTML first
        text = self._escape_html(text)

        # Bold: **text** -> <b>text</b>
        text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)

        # Italic: *text* -> <i>text</i>
        text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)

        # Code: `text` -> <font face="Courier">text</font>
        text = re.sub(r"`(.+?)`", r'<font face="Courier">\1</font>', text)

        return text


def get_pdf_service() -> PDFService:
    """Get the PDF service instance."""
    return PDFService()
