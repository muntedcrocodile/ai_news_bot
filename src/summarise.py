import os
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import CharacterTextSplitter

# Load the summarization model locally
model_id = "Falconsai/text_summarization"
summarization_model = HuggingFacePipeline.from_model_id(model_id, task='summarization')


# Define the map step: summarise each chunk
def map_summarise(doc):
    return summarization_model.invoke(doc, max_length=50)


def summarise_text(text):
    # Split the text into smaller chunks
    text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=0, separator=". ", is_separator_regex=False, length_function=len)
    split_docs = text_splitter.split_text(text)

    # Apply the map step to each chunk
    mapped_summaries = [map_summarise(doc) for doc in split_docs]

    # Reduce step: consolidate the summaries into a final summary
    final_summary = " ".join(mapped_summaries)
    return final_summary
