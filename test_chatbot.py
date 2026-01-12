#!/usr/bin/env python3
"""
Simple test script for the chatbot
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if API key is set
api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key == "your_openai_api_key_here":
    print("❌ ERROR: OPENAI_API_KEY not set or still contains placeholder!")
    print("Please update the .env file with your actual OpenAI API key")
    sys.exit(1)

print("✅ API key found!")
print("\nTesting chatbot...\n")

try:
    from app.chain import chat
    
    # Test 1: Basic conversation
    test_message = "Hello! What is 2+2?"
    print(f"User: {test_message}")
    
    response = chat(test_message)
    print(f"Chatbot: {response}\n")
    
    # Test 2: Another message to verify memory
    test_message2 = "What about 3+3?"
    print(f"User: {test_message2}")
    
    response2 = chat(test_message2)
    print(f"Chatbot: {response2}\n")
    
    # Test 3: Weather query
    test_message3 = "What's the weather like in Madrid?"
    print(f"User: {test_message3}")
    
    response3 = chat(test_message3)
    print(f"Chatbot: {response3}\n")
    
    # Test 4: Another weather query
    test_message4 = "How about in London?"
    print(f"User: {test_message4}")
    
    response4 = chat(test_message4)
    print(f"Chatbot: {response4}\n")
    
    print("✅ Chatbot test successful!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
