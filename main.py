from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import fitz  # PyMuPDF
import tempfile
import uuid
import os

app = FastAPI()

@app.post("/convert/")
async def convert_pdf_to_images(file: UploadFile = File(...)):
    """Convierte un PDF a imágenes y devuelve las rutas."""
    suffix = file.filename.split(".")[-1]
    if suffix.lower() != "pdf":
        return {"error": "Solo se aceptan PDFs"}

    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp_pdf.write(await file.read())
    temp_pdf.close()

    pdf_doc = fitz.open(temp_pdf.name)
    output_files = []

    for page_number in range(len(pdf_doc)):
        page = pdf_doc.load_page(page_number)
        pix = page.get_pixmap(dpi=150)  # resolución moderada
        image_filename = f"/tmp/{uuid.uuid4()}.jpg"
        pix.save(image_filename)
        output_files.append(image_filename)

    pdf_doc.close()
    os.remove(temp_pdf.name)

    # Devolver solo la primera imagen o todas
    return {"images": output_files}
