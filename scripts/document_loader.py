import logging
from langchain_community.document_loaders import DirectoryLoader, Docx2txtLoader




def langchain_document_loader(TMP_DIR):
    """
    Load documents from the temporary directory (TMP_DIR).
    Files can be in txt, pdf, CSV or docx format.

    Logs information and errors to respective files.
    """

    logging.basicConfig(
        filename="../logs/error.log",  # Specify error log file path
        level=logging.ERROR,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    info_logger = logging.getLogger("info_logger")
    info_logger.setLevel(logging.INFO)
    info_handler = logging.FileHandler("../logs/info.log")  # Specify info log file path
    info_handler.setLevel(logging.INFO)
    # info_handler.setFormatter(info_logger.formatter)
    info_logger.addHandler(info_handler)

    documents = []

    info_logger.info(f"Starting document loading from {TMP_DIR}")

    try:
        doc_loader = DirectoryLoader(
            TMP_DIR.as_posix(),
            glob="**/*.docx",
            loader_cls=Docx2txtLoader,
            show_progress=True,
        )
        documents.extend(doc_loader.load())
        info_logger.info(f"Loaded {len(doc_loader.loaded_count)} DOCX files.")
    except Exception as e:
        logging.error("Error loading DOCX files: %s", e)
    
    try:
        txt_loader = DirectoryLoader(
            TMP_DIR.as_posix(), glob="**/*.txt", loader_cls=TextLoader, show_progress=True
        )
        documents.extend(txt_loader.load())
        info_logger.info(f"Loaded {len(txt_loader.loaded_count)} TXT files.")
    except Exception as e:
        logging.error("Error loading TXT files: %s", e)

    try:
        pdf_loader = DirectoryLoader(
            TMP_DIR.as_posix(), glob="**/*.pdf", loader_cls=PyPDFLoader, show_progress=True
        )
        documents.extend(pdf_loader.load())
        info_logger.info(f"Loaded {len(pdf_loader.loaded_count)} PDF files.")
    except Exception as e:
        logging.error("Error loading PDF files: %s", e)

    try:
        csv_loader = DirectoryLoader(
            TMP_DIR.as_posix(), glob="**/*.csv", loader_cls=CSVLoader, show_progress=True,
            loader_kwargs={"encoding":"utf8" }
        )
        documents.extend(csv_loader.load())
        info_logger.info(f"Loaded {len(csv_loader.loaded_count)} CSV files.")
    except Exception as e:
        logging.error("Error loading CSV files: %s", e)

    info_logger.info(f"Successfully loaded {len(documents)} documents.")

    return documents
