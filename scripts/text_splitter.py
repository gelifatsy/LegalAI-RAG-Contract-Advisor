from langchain.text_splitter import RecursiveCharacterTextSplitter


def text_splitter(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        separators = ["\n\n", "\n", " ", ""],    
        chunk_size = 1600,
        chunk_overlap= 200
    )
    chunks = text_splitter.split_documents(documents=documents)
    return chunks 

# # Text splitting
# chunks = text_splitter.split_documents(documents=documents)