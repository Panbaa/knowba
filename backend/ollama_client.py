from ollama import ChatResponse, chat

chat_model = "llama3:8b"
embedding_model = "qwen3-embedding"


def prompt_ollama(messages):
    response: ChatResponse = chat(model="llama3:8b", messages=messages)
    return response

def get_embedding(input_text: [str]):
    response = ollama.embed(
        model=embedding_model,
        input=input_text
    )
    return response['embeddings']

# get_embedding(["hello world", "how are you?"])