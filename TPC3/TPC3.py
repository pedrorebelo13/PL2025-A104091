import re

def transform_markdown_to_html(markdown_content):
    """Convert a Markdown string into HTML, supporting headers, lists, and inline elements."""
    # Initialize output list and list state
    output_html = []
    inside_numbered_list = False
    
    # Split content into lines for processing
    for line in markdown_content.split('\n'):
        line = line.strip()
        if not line:  # Skip empty lines
            continue
            
        # Handle headers starting with #
        if match := re.match(r'^#\s*(.+)$', line):
            output_html.append(f'<h1>{match.group(1)}</h1>')
            continue
            
        # Handle ordered list items (e.g., "1. Item")
        if match := re.match(r'^\d+\.\s+(.+)$', line):
            if not inside_numbered_list:
                output_html.append('<ol>')
                inside_numbered_list = True
            output_html.append(f'    <li>{match.group(1)}</li>')
            continue
        elif inside_numbered_list:
            output_html.append('</ol>')
            inside_numbered_list = False
            
        # Process inline Markdown elements
        converted_text = line
        
        # Convert images: ![alt](url)
        converted_text = re.sub(
            r'!\[(.+?)\]\((https?://.+?)\)',
            r'<img src="\2" alt="\1" />',
            converted_text
        )
        
        # Convert links: [text](url)
        converted_text = re.sub(
            r'\[(.+?)\]\((https?://.+?)\)',
            r'<a href="\2">\1</a>',
            converted_text
        )
        
        # Convert italic: *text*
        converted_text = re.sub(
            r'\*(.+?)\*',
            r'<i>\1</i>',
            converted_text
        )
        
        # Convert bold: **text**
        converted_text = re.sub(
            r'\*\*(.+?)\*\*',
            r'<b>\1</b>',
            converted_text
        )
        
        if converted_text and not inside_numbered_list:
            output_html.append(converted_text)
    
    # Ensure any open ordered list is closed
    if inside_numbered_list:
        output_html.append('</ol>')
        
    return '\n'.join(output_html)

# Test the conversion with a sample Markdown text
if __name__ == "__main__":
    sample_markdown = """
# Introduction
This is a *test* with **emphasis** on details...
1. Step one
2. Step two
3. Step three
Learn more at [official site](https://www.example.com)
See the image: ![cute puppy](https://www.puppy.com/image.jpg)
"""
    result = transform_markdown_to_html(sample_markdown)
    print(result)