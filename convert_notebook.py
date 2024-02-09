import nbformat
from nbconvert.preprocessors import Preprocessor
from nbconvert import MarkdownExporter
import re
import argparse
import base64
from pathlib import Path

class DocsPreprocessor(Preprocessor):
    def __init__(self, notebook_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notebook_name = Path(notebook_path).stem
        # Directory for saving images and audio files
        self.assets_dir = f'static/documentation/notebooks/{self.notebook_name}/assets'
        Path(self.assets_dir).mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

    def preprocess(self, nb, resources):
        # Set the correct path for the output files
        resources['output_files_dir'] = self.assets_dir
        return super().preprocess(nb, resources)

    def preprocess_cell(self, cell, resources, index):
        if cell.cell_type == 'markdown':
            cell.source = self.modify_links(cell.source)
        elif cell.cell_type == 'code':
            cell.source = self.indent_code_blocks_in_code(cell.source)
            cell = self.handle_image_outputs(cell, resources, index)
            cell = self.handle_audio_outputs(cell, resources, index)  # Handle audio outputs
        return cell, resources

    def modify_links(self, text):
        # Function to modify links in markdown cells
        return text

    def indent_code_blocks_in_code(self, text):
        # Function to indent code blocks within code cells
        return text

    def handle_image_outputs(self, cell, resources, cell_index):
        if 'outputs' in cell:
            for output_index, output in enumerate(cell['outputs']):
                if output.output_type in ['display_data', 'execute_result']:
                    for mime_type, data in output.data.items():
                        if mime_type.startswith('image/'):
                            image_data = base64.b64decode(data)
                            image_filename = f'output_{cell_index}_{output_index}.{mime_type.split("/")[-1]}'
                            image_filepath = Path(self.assets_dir) / image_filename
                            with open(image_filepath, 'wb') as img_file:
                                img_file.write(image_data)
                            output.data[mime_type] = f'![image](/{image_filepath})'
        return cell

    def handle_audio_outputs(self, cell, resources, cell_index):
        if 'outputs' in cell:
            for output_index, output in enumerate(cell['outputs']):
                if output.output_type in ['display_data', 'execute_result']:
                    for mime_type, data in output.data.items():
                        print("found", mime_type)
                        if mime_type.startswith('audio/'):
                            audio_data = base64.b64decode(data)
                            audio_filename = f'output_{cell_index}_{output_index}.{mime_type.split("/")[-1]}'
                            audio_filepath = Path(self.assets_dir) / audio_filename
                            with open(audio_filepath, 'wb') as audio_file:
                                audio_file.write(audio_data)
                            output.data[mime_type] = f'<audio controls><source src="/{audio_filepath}" type="{mime_type}"></audio>'
        return cell

def convert_notebook(notebook_path):
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)

    resources = {
        'output_files_dir': f'static/documentation/notebooks/{Path(notebook_path).stem}/assets'
    }

    exporter = MarkdownExporter()
    exporter.register_preprocessor(DocsPreprocessor(notebook_path), True)

    body, resources = exporter.from_notebook_node(nb, resources)

    # Replace '(static' with '(/workers-ai/static' in the Markdown content
    body = body.replace('(static', '(/workers-ai/static')

    # Write the converted Markdown
    md_path = Path(notebook_path).with_suffix('.md')
    with open(md_path, 'w') as f:
        f.write(body)
    print(f"Converted notebook saved to {md_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert an IPython Notebook to Markdown with custom processing for images and audio.")
    parser.add_argument("notebook", help="The path to the IPython notebook to convert.")
    args = parser.parse_args()

    convert_notebook(args.notebook)
