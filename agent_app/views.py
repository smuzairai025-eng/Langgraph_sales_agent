from django.shortcuts import render
from rest_framework.decorators import api_view
from Ai_engine.graph import agent
from rest_framework.response import Response
from langchain_core.messages import HumanMessage
# Create your views here.

Memory={}
# @api_view(['GET'])
def chat_ui(request):
    return render(request,"home.html")

@api_view(['POST'])
def chat_endpoint(request):
    user_message=request.data.get("message")
    thread_id=request.data.get("thread_id")

    if not user_message:
        return Response({"error":"No message found in request"},status=400)
    
    current_state=Memory.get(thread_id,{
        "messages":[],
        "profile": {"industry":None ,"website":None, "customer_size":None},
        "intent": "inquiry"
    })

    inputs = {
        "messages": current_state["messages"] + [HumanMessage(content=user_message)],
        "profile": current_state["profile"]
    }

    result = agent.invoke(inputs)

    Memory[thread_id]={
        "messages":result["messages"],
        "profile":result.get("profile",{})
    }

    last_ai_msg = result["messages"][-1].content

    return Response({
        "response": last_ai_msg,
        "thread_id": thread_id
    })


