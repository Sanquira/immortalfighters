"""Module for markdown extensions."""
from markdown.extensions import Extension


class EscapeHtml(Extension):
    """
    EscapeHtml extension. Disable user inserted html tags.
    """
    def extendMarkdown(self, md):
        md.preprocessors.deregister('html_block')
        md.inlinePatterns.deregister('html')
