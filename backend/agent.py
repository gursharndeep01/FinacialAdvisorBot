from langchain.messages import SystemMessage
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from rag import get_relevant_chunks
from tools import calculate_sip, calculate_emi, calculate_cagr, calculate_fd
from memory import get_memory
from config import GROQ_API_KEY, MODEL_NAME


llm = ChatGroq(api_key=GROQ_API_KEY, model=MODEL_NAME)

SYSTEM_PROMPT = """ You are a helpful Indian financial advisor chatbot.
You help users with: 
- Mutual funds, SIP, EMI, FD, CAGR calculations
- Tax saving advice
- Investment planning
Always give answer in simple terms.
If calculation is needed, use the tools provided to you.
If unsure , say so honestly.
"""

def chat(query: str, session_id: str = "default"):
    chunks= get_relevant_chunks(query, k=4)
    context = "\n".join([c.page_content for c in chunks])
    memory = get_memory(session_id)
    calc_result= None
    q= query.lower()
    if "sip" in q and any (char.isdigit() for char in q):
        nums = [int(s) for s in q.split() if s.isdigit()]
        if len(nums) >= 3:
            calc_result = calculate_sip(nums[0], nums[1], nums[2])
    elif "emi" in q and any (char.isdigit() for char in q):
        nums = [int(s) for s in q.split() if s.isdigit()]
        if len(nums) >= 3:
            calc_result = calculate_emi(nums[0], nums[1], nums[2])
    elif "cagr" in q and any (char.isdigit() for char in q):
        nums = [int(s) for s in q.split() if s.isdigit()]
        if len(nums) >= 3:
            calc_result = calculate_cagr(nums[0], nums[1], nums[2])
    elif "fd" in q and any (char.isdigit() for char in q):
        nums = [int(s) for s in q.split() if s.isdigit()]
        if len(nums) >= 3:
            calc_result = calculate_fd(nums[0], nums[1], nums[2])
    messages = [SystemMessage(content=SYSTEM_PROMPT)]
    
    for msg in memory.messages:
        messages.append(msg)
    user_context= f""" 
    context from documents: {context}
    {f'calculation result: {calc_result}' if calc_result else ''}
    user question : {query}
    """
    messages.append(HumanMessage(content=user_context))
    response = llm.invoke(messages)
    answer = response.content
    memory.add_user_message(query)
    memory.add_ai_message(answer)
    
    return answer