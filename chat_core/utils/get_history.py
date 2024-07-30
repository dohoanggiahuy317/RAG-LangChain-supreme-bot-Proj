from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import ConfigurableFieldSpec


def get_session_history(user_id, conversation_id):
    return SQLChatMessageHistory(f"{user_id}--{conversation_id}", "sqlite:///chat_core/database/memory.db")



def get_runnable_history(runnable):
    runnable_with_history = RunnableWithMessageHistory(
        runnable,
        get_session_history,
        input_messages_key="question",
        history_messages_key="history",
        history_factory_config=[
            ConfigurableFieldSpec(
                id="user_id",
                annotation=str,
                name="User ID",
                description="Unique identifier for the user.",
                default="",
                is_shared=True,
            ),
            ConfigurableFieldSpec(
                id="conversation_id",
                annotation=str,
                name="Conversation ID",
                description="Unique identifier for the conversation.",
                default="",
                is_shared=True,
            ),
        ],
    )

    return runnable_with_history