import os
from langchain_unstructured import UnstructuredLoader

os.environ["UNSTRUCTURED_INFERENCE_CPU"] = "True"

local_api_url = "http://localhost:9500/general/v0/general"  # Replace with your local API endpoint
loader = UnstructuredLoader("samples/sampleManufactures.pdf", url=local_api_url) 

docs = loader.load()

print(docs[0].page_content)
