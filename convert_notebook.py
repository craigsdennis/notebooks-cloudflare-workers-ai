import argparse
import os
import re

import nbformat
from nbconvert import MarkdownExporter
from nbconvert.preprocessors import Preprocessor


class DocsPreprocessor(Preprocessor):
    def preprocess_cell(self, cell, resources, cell_index):
        if cell.cell_type == 'markdown':
            cell.source = self.modify_links(cell.source)
        elif cell.cell_type == 'code':
            cell.source = self.indent_code_blocks_in_code(cell.source)
        return cell, resources

    def modify_links(self, text):
        # Modify links to be absolute paths without the 'https://' prefix
        def replace_link(match):
            url = match.group(3)  # The URL part of the markdown link
            # Check if the URL is from developers.cloudflare.com
            if 'developers.cloudflare.com' in url:
                # Extract the path part of the URL and convert it to an absolute path
                path = url.split('developers.cloudflare.com')[-1]
                return f'[{match.group(1)}]({path})'
            return match.group(0)

        return re.sub(r'\[([^\]]+)\]\((http[s]?://)?([^\)]+)\)', replace_link, text)

    def indent_code_blocks_in_code(self, text):
        # Indent every line in code blocks fenced by triple backticks
        in_code_block = False
        indented_lines = []
        for line in text.split('\n'):
            if line.startswith('```'):
                in_code_block = not in_code_block
                # Indent the fence line as well
                indented_lines.append('    ' + line)
            elif in_code_block:
                # Indent the line by 4 spaces if it's inside a code block
                indented_lines.append('    ' + line)
            else:
                # Add the line without indentation if it's outside a code block
                indented_lines.append(line)
        return '\n'.join(indented_lines)

def convert_notebook(notebook_path):
    # Load the notebook
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)

    # Create a MarkdownExporter and use the DocsPreprocessor
    exporter = MarkdownExporter()
    exporter.register_preprocessor(DocsPreprocessor(), True)

    # Convert the notebook to Markdown
    body, resources = exporter.from_notebook_node(nb)

    # Determine the path for the output Markdown file
    md_path = os.path.splitext(notebook_path)[0] + '.md'

    # Save the Markdown
    with open(md_path, 'w') as f:
        f.write(body)
    print(f"Converted notebook saved to {md_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert an IPython Notebook to Markdown with custom processing for links and code blocks within code cells.")
    parser.add_argument("notebook", help="The path to the IPython notebook to convert.")
    args = parser.parse_args()

    convert_notebook(args.notebook)
