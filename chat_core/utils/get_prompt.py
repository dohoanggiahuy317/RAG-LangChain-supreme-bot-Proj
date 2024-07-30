from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def prompt_template():
    
    template = """You help everyone by answering questions, and improve your answers from previous answer in History.
    Don't try to make up an answer, if you don't know just say that you don't know.
    Answer in the same language the question was asked.
    Answer in a way that is easy to understand.
    Do not say "Based on the information you provided, ..." or "I think the answer is...". Just answer the question directly in detail.
    Use only the following pieces of context and chat history to answer the question at the end.

    Context: {context}

    Question: {question}

    Answer:"""

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", template),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ]
    )

    return prompt