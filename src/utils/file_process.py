from fastapi import HTTPException
from fastapi import UploadFile
from langchain.document_loaders import UnstructuredPDFLoader


def file_processing(file: UploadFile):
    file_location = f"/tmp/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(file.file.read())  # Save the uploaded file to the /tmp directory
    try:
        loader = UnstructuredPDFLoader(file_path=file_location)
        data = loader.load()  # Load the PDF file
        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
