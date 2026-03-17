from ollama import ChatResponse, chat


def prompt_ollama(messages):
    response: ChatResponse = chat(model="llama3:8b", messages=messages)
    return response
