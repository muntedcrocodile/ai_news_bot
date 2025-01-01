import os
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import CharacterTextSplitter

# Load the summarization model locally
model_id = "Falconsai/text_summarization"
summarization_model = HuggingFacePipeline.from_model_id(model_id, task='summarization')


# Define the map step: summarize each chunk
def map_summarize(doc):
    return summarization_model.invoke(doc, max_length=50)


def summarize_text(text):
    # Split the text into smaller chunks
    text_splitter = CharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    split_docs = text_splitter.split_text(text)

    # Apply the map step to each chunk
    mapped_summaries = [map_summarize(doc) for doc in split_docs]

    # Reduce step: consolidate the summaries into a final summary
    final_summary = " ".join(mapped_summaries)
    return final_summary
