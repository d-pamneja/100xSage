from src.instances import openAI_client

# OpenAI Instances
ticket_creation_thread = openAI_client.beta.threads.create()