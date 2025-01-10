import os
from openai import OpenAI

ENV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "secret.env")
with open(ENV, 'r') as env_file:
    env_data = env_file.readlines()
    KEY_OPENAI = env_data[0].strip()
    KEY_DISCORD = env_data[1].strip()

client = OpenAI(api_key=KEY_OPENAI)

# Read personality from file
docu = "txt/base-knowledge.txt"
if os.path.isfile(docu):
    personality = "BASE KNOWLEDGE : " + open(docu, "r").read()
else:
    personality = "BASE KNOWLEDGE : None"
    #create the file
    with open(docu, "w") as doc:
        doc.write("")

# Read emoji from file
docu = "txt/emoji.txt"
if os.path.isfile(docu):
    emoji = open(docu, "r").read()
else:
    emoji = ""
    with open(docu, "w") as doc:
        doc.write("")

# Read memory from file
memory_file_path = "txt/memory.txt"
if os.path.isfile(memory_file_path):
    memory = open(memory_file_path, "r").read()
else:
    memory = ""
    #create the file
    with open(memory_file_path, "w") as doc:
        doc.write("")

# Read interactions from file
interactions_file_path = "txt/interactions.txt"
if os.path.isfile(interactions_file_path):
    interactions = open(interactions_file_path, "r").readlines()
else:
    #create the file
    with open(memory_file_path, "w") as doc:
        doc.write("")
    interactions = []

def generation(messages):
    global client

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    
    response_content = response.choices[0].message['content']

    return response_content

def generate_response(prompt, user):
    global personality, emoji, memory, interactions
    
    messages=[
        {"role": "system", "content": personality},
        {"role": "system", "content": emoji},
        {"role": "system", "content": memory},
        {"role": "system", "content": interactions},
        {"role": "system", "content": f"Message sent by {user}"},
        {"role": "user", "content": prompt}
    ]

    response_content = generation(messages)
    
    # Update memory file
    interaction_update(prompt, response_content)
    
    return response_content

def interaction_update(prompt, response_content):
    global interactions, interactions_file_path

    # Append new interaction
    interactions.append(f"User: {prompt}\n")
    interactions.append(f"Assistant: {response_content}\n")
    
    # Keep only the last 10 interactions
    if len(interactions) > 20:
        interactions = interactions[-20:]
    
    with open(interactions_file_path, "w") as interactions_file:
        interactions_file.writelines(interactions)

def update_memory_summary():
    global personality, memory, interactions, memory_file_path
    
    memory = "MEMORY : " + memory

    prompt = "Based on the Memory provided and Interactions with user, write 10 bullet points of what Quackers needs to remember. Different from the Base Knowledge."
    
    messages=[
        {"role": "system", "content": personality},
        {"role": "system", "content": memory},
        {"role": "system", "content": "".join(interactions)},
        {"role": "user", "content": prompt}
    ]
    
    summary = generation(messages)
    
    with open(memory_file_path, "w") as memory_file:
        memory_file.write(summary)

    memory = summary