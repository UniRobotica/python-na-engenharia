import json
import base64
import os

# Caminho do notebook
notebook_path = "notebooks/Pratica1_20261_PythonBasicoFuncoes.ipynb"

# Pasta onde salvar as imagens
output_dir = "imagens_extraidas"
os.makedirs(output_dir, exist_ok=True)

# Abrir notebook
with open(notebook_path, "r", encoding="utf-8") as f:
    notebook = json.load(f)

contador = 1
for cell_index, cell in enumerate(notebook["cells"]):
    if cell["cell_type"] == "markdown" and "attachments" in cell:
        for name, attachment in cell["attachments"].items():
            for mime, b64data in attachment.items():
                image_bytes = base64.b64decode(b64data)
                # Nome único
                filename = f"image_cell{cell_index}_{contador}.png"
                path = os.path.join(output_dir, filename)
                with open(path, "wb") as img_file:
                    img_file.write(image_bytes)
                print(f"Salvo: {path}")
                contador += 1