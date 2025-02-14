from src.dependencies import * 

# OpenAI Embedding Instances
openAI_client = OpenAI(api_key=OPENAI_API_KEY)
embedding_model = openAI_client.embeddings

# Pinecone Initialisation
pc = Pinecone(api_key = PINECONE_API_KEY, environment = PINECONE_API_ENV)


