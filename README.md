# Simple docuquery AI

## Características

- **Procesamiento de Documentos**: Carga y procesa documentos en formato PDF.
- **Integración con OpenAI**: Utiliza los modelos de OpenAI para generar embeddings y realizar consultas.
- **Almacenamiento y Recuperación**: Utiliza Pinecone para almacenar y recuperar embeddings de documentos.

## Instalación

### Requisitos Previos

- Docker
- Clave API de Pinecone
- Clave API de OpenAI

### Paso a Paso

1. Clona el repositorio:

    ```bash
    git clone https://github.com/joaquinreyero/simple-docuquery-ai.git
    cd docuai
    ```

2. Crea un archivo `.env` en la raíz del proyecto con tus claves API:

    ```env
    OPENAI_API_KEY=tu-clave-openai
    PINECONE_API_KEY=tu-clave-pinecone
    ```

3. Construye y ejecuta los contenedores Docker utilizando Docker Compose:

    ```bash
    docker-compose up --build
    ```

## Uso

1. Abre tu navegador web y navega a `http://localhost:8001/docs`.
2. Carga un archivo PDF a través del endpoint `/upload-pdf/`.

    ```bash
    curl -X POST "http://localhost:8001/upload-pdf/" -F "file=@/ruta/a/tu/archivo.pdf"
    ```

3. Realiza preguntas sobre el contenido del documento cargado.

## API Endpoints

### `/upload-pdf/`

- **Método**: `POST`
- **Descripción**: Carga un archivo PDF y procesa su contenido.
- **Parámetros**: `file` (archivo PDF)
- **Respuesta**: JSON con estadísticas del índice de Pinecone.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o un pull request en el repositorio para discutir cualquier cambio que desees realizar.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para obtener más información.
