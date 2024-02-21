

text_splitter = RecursiveCharacterTextSplitter(
    separators = ["\n\n", "\n", " ", ""],    
    chunk_size = 1600,
    chunk_overlap= 200
)

# Text splitting
chunks = text_splitter.split_documents(documents=documents)