from fastapi import UploadFile
from typing import List
from pathlib import Path
import uuid
import logging

logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

async def salvar_pdfs_temporarios(files: List[UploadFile]) -> List[str]:
    """
    Salva PDFs no servidor temporariamente e retorna caminhos
    """
    pdf_paths = []
    
    for file in files:
        if not file.filename.lower().endswith('.pdf'):
            raise ValueError(f"Arquivo {file.filename} não é PDF")
        
        unique_name = f"{uuid.uuid4()}_{file.filename}"
        file_path = UPLOAD_DIR / unique_name
        
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        pdf_paths.append(str(file_path))
        logger.info(f"[AdapterUpload] ✅ Salvo: {file.filename} -> {file_path}")
    
    return pdf_paths