from .document_service import get_vector_index
from storage.db import save_message, get_history
#from llama_index.core.response_synthesizers import ResponseSynthesizer

async def answer_question(question: str, user_id: str) -> str:
    try:
        index = get_vector_index(user_id)
        query_engine = index.as_query_engine(similarity_top_k=3)
        context = query_engine.query(question)

        answer_text = str(context.response) if hasattr(context, "response") else str(context)
        if not answer_text.strip():
            answer_text = "I don’t know the answer."

        save_message(user_id, "user", question)
        save_message(user_id, "bot", answer_text)

        return answer_text
    except Exception as e:
        return f"Error while querying: {str(e)}"

def get_chat_history(user_id: str):
    return get_history(user_id)
