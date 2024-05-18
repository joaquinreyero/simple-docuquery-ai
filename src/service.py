from langchain.text_splitter import RecursiveCharacterTextSplitter

from pinecone import Pinecone
from langchain.chains.question_answering import load_qa_chain

from fastapi import UploadFile, HTTPException

from langchain.vectorstores import Pinecone

from src.config import instance_pinecone, instance_embeddings, instance_llm, verify_pinecone_index
from src.utils.file_process import file_processing


def upload_pdf(file: UploadFile):
    """ Upload a PDF file into Pinecone"""
    try:
        """ Process the uploaded PDF file and extract the text """
        data = file_processing(file)

        """ Split the text into chunks of 500 characters with an overlap of 50 characters """
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        texts = text_splitter.split_documents(data)

        """ Embed the text using OpenAI's GPT-3 model """
        embeddings_list = [instance_embeddings().embed_documents(t.page_content) for t in texts]

        verify_pinecone_index()  # Verify if the Pinecone index exists

        """ Create a Pinecone index and upsert the embeddings """
        vectors = [{"id": str(i), "values": embedding[0], "metadata": {"text": t.page_content}} for i, (embedding, t) in
                   enumerate(zip(embeddings_list, texts))]  # Create a list of dictionaries with the embeddings and
        # metadata
        instance_pinecone().upsert(vectors=vectors)

        """ Return the Pinecone index stats """
        stats = instance_pinecone().describe_index_stats()
        return {
            "dimension": stats["dimension"],
            "index_fullness": stats["index_fullness"],
            "total_vector_count": stats["total_vector_count"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def ask(question: str):
    """ Search for similar documents in Pinecone using the question """
    try:
        vectorstore = Pinecone(instance_pinecone(), instance_embeddings(), "text")  # Create a Pinecone vectorstore
        docs = vectorstore.similarity_search(question)  # Search for similar documents in Pinecone using the question

        """ Construct a question-answering chain and run the chain on the documents and question """
        chain = load_qa_chain(instance_llm(), chain_type="stuff")
        response = chain.run(input_documents=docs, question=question)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
