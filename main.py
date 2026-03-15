from agent import chat 
#this is the main chat loop
print("Assistant is ready! Type 'quit' to exit.")
print("------------------------")

while True:
    user_input = input("You: ")

    if user_input.lower() =="quit":
        print("Goodbye!")
        break

    response = chat(user_input)
    print(f"Assistant: {response}")
    print()