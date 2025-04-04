from Frontend.GUI import (
    main, SetAssistantStatus,
    ShowTextToScreen, TempDirectoryPath,
    SetMicrophoneStatus, AnswerModifier,
    QueryModifier, GetMicrophoneStatus,
    GetAssistantStatus
)
from Backend.Model import FirstLayerDMM
from Backend.RealTimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")

# Default welcome message
DefaultMessage = f'''{Username}: Hello {Assistantname}, How are you?
{Assistantname}: Welcome {Username}. I am doing well. How may I help you?'''

# List of supported function commands
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

# Track subprocesses
subprocesses = []

def ShowDefaultChatIfNoChats():
    """Initialize chat log with default message if empty"""
    with open(r'Data\ChatLog.json', "r", encoding='utf-8') as file:
        if len(file.read()) < 5:
            with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as db_file:
                db_file.write("")
            with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as resp_file:
                resp_file.write(DefaultMessage)

def ReadChatLogJson():
    """Read and return chat log data"""
    with open(r'Data\ChatLog.json', 'r', encoding='utf-8') as file:
        return json.load(file)

def ChatLogIntegration():
    """Format chat log data and save to database file"""
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"{Username}: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"{Assistantname}: {entry['content']}\n"
    
    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

def ShowChatsOnGUI():
    """Display chat history in GUI"""
    with open(TempDirectoryPath('Database.data'), "r", encoding='utf-8') as file:
        data = file.read()
        if len(str(data)) > 0:
            lines = data.split('\n')
            result = '\n'.join(lines)
            with open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8') as resp_file:
                resp_file.write(result)

def InitialExecution():
    """Initialize the application state"""
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()

def MainExecution():
    """Main execution loop for processing user input"""
    task_execution = False
    image_execution = False
    image_generation_query = ""

    SetAssistantStatus("Listening...")
    query = SpeechRecognition()
    ShowTextToScreen(f"{Username}: {query}")
    SetAssistantStatus("Thinking...")

    decision = FirstLayerDMM(query)
    print(f"\nDecision: {decision}\n")

    # Check for general and realtime queries
    has_general = any(i.startswith("general") for i in decision)
    has_realtime = any(i.startswith("realtime") for i in decision)
    
    merged_query = " and ".join(
        [" ".join(i.split()[1:]) for i in decision 
         if i.startswith("general") or i.startswith("realtime")]
    )

    # Handle image generation
    for queries in decision:
        if "generate" in queries:
            image_generation_query = str(queries)
            image_execution = True

    # Handle automation tasks
    for queries in decision:
        if not task_execution:
            if any(queries.startswith(func) for func in Functions):
                run(Automation(list(decision)))
                task_execution = True

    # Process image generation
    if image_execution:
        with open(r"Frontend\Files\ImageGeneration.data", "w") as file:
            file.write(f"{image_generation_query}, True")
        try:
            p1 = subprocess.Popen(
                ['python', r'Backend\ImageGeneration.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                shell=False
            )
            subprocesses.append(p1)
        except Exception as e:
            print(f"Error starting ImageGeneration.py: {e}")

    # Handle realtime and general queries
    if has_general and has_realtime or has_realtime:
        SetAssistantStatus("Searching...")
        answer = RealtimeSearchEngine(QueryModifier(merged_query))
        ShowTextToScreen(f"{Assistantname}: {answer}")
        SetAssistantStatus("Answering...")
        TextToSpeech(answer)
        return True
    else:
        for queries in decision:
            if "general" in queries:
                SetAssistantStatus("Thinking...")
                query_final = queries.replace("general", "")
                answer = ChatBot(QueryModifier(query_final))
                ShowTextToScreen(f"{Assistantname}: {answer}")
                SetAssistantStatus("Answering...")
                TextToSpeech(answer)
                return True
            elif "realtime" in queries:
                SetAssistantStatus("Searching...")
                query_final = queries.replace("realtime", "")
                answer = RealtimeSearchEngine(QueryModifier(query_final))
                ShowTextToScreen(f"{Assistantname}: {answer}")
                SetAssistantStatus("Answering...")
                TextToSpeech(answer)
                return True
            elif "exit" in queries:
                query_final = "Okay, Bye!"
                answer = ChatBot(QueryModifier(query_final))
                ShowTextToScreen(f"{Assistantname}: {answer}")
                SetAssistantStatus("Answering...")
                TextToSpeech(answer)
                SetAssistantStatus("Answering...")
                os._exit(1)

def FirstThread():
    """Main processing thread"""
    while True:
        current_status = GetMicrophoneStatus()
        if current_status == "True":
            MainExecution()
        else:
            ai_status = GetAssistantStatus()
            if "Available..." in ai_status:
                sleep(0.1)
            else:
                SetAssistantStatus("Available...")

def SecondThread():
    """GUI thread"""
    main()

if __name__ == "__main__":
    # Initialize the application
    InitialExecution()
    
    # Start the main processing thread
    thread2 = threading.Thread(target=FirstThread, daemon=True)
    thread2.start()
    
    # Start the GUI thread
    SecondThread()