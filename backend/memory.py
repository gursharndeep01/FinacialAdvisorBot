from langchain_community.chat_message_histories import ChatMessageHistory

sessions= {}
def get_memory(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = ChatMessageHistory()
    return sessions[session_id]

def clear_memory(session_id: str):
   if session_id in sessions:
       del sessions[session_id]
       return True
   return False

def get_all_sessions():
    return list(sessions.keys())
