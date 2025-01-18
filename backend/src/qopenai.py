import os
from openai import OpenAI
import requests
import qlogs
from consts import DATA_DIR, IMG_DIR

from dotenv import load_dotenv
load_dotenv()

KEY_OPENAI = os.getenv("KEY_OPENAI")

client = OpenAI(api_key=KEY_OPENAI)

# Read personality from file
BASE_KNOW_PATH = os.path.join(DATA_DIR, "txt/base-knowledge.txt")
if os.path.isfile(BASE_KNOW_PATH):
    personality = "BASE KNOWLEDGE : " + open(BASE_KNOW_PATH, "r").read()
else:
    personality = "BASE KNOWLEDGE : None"
    #create the file
    with open(BASE_KNOW_PATH, "w") as doc:
        doc.write("")

# Read emoji from file
BASE_KNOW_PATH = os.path.join(DATA_DIR, "txt/emoji.txt")
if os.path.isfile(BASE_KNOW_PATH):
    emoji = open(BASE_KNOW_PATH, "r").read()
else:
    emoji = ""
    with open(BASE_KNOW_PATH, "w") as doc:
        doc.write("")

# Read memory from file
memory_file_path = os.path.join(DATA_DIR, "txt/memory.txt")
if os.path.isfile(memory_file_path):
    memory = open(memory_file_path, "r").read()
else:
    memory = ""
    #create the file
    with open(memory_file_path, "w") as doc:
        doc.write("")

# Read interactions from file
interactions_file_path = os.path.join(DATA_DIR, "txt/interactions.txt")
if os.path.isfile(interactions_file_path):
    with open(interactions_file_path, mode="r", encoding="utf-8") as doc:
        interactions = doc.readlines()
else:
    #create the file
    with open(memory_file_path, "w") as doc:
        doc.write("")
    interactions = []

def generation(messages):
    global client

    qlogs.info(f"- Requesting generation from OpenAI")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    
    response_content = response.choices[0].message.content
    response_content = response_content[:1000]

    return response_content

def img_generation(user, prompt):
    global client

    user = user[:1000]

    qlogs.info(f"- Requesting Image generation from OpenAI")
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024",
        user = user,
    )

    return response.data[0].url

def generate_response(prompt, user):
    global personality, emoji, memory, interactions
    
    messages=[
        {"role": "system", "content": personality},
        {"role": "system", "content": emoji},
        {"role": "system", "content": memory},
        {"role": "system", "content": "".join(interactions)},
        {"role": "system", "content": f"Message sent by {user}"},
        {"role": "system", "content": "Language : French"},
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
    
    with open(interactions_file_path, mode="w", encoding='utf-8') as interactions_file:
        interactions_file.writelines(interactions)

def update_memory_summary():
    global personality, memory, interactions, memory_file_path
    
    memory = "MEMORY : " + memory

    prompt = "Based on the Memory provided and Interactions with user, write 10 bullet points of what Quackers needs to remember. Different from the Base Knowledge."
    
    messages=[
        {"role": "system", "content": personality},
        {"role": "system", "content": memory},
        {"role": "system", "content": "".join(interactions)},
        {"role": "system", "content": "Language : French"},
        {"role": "user", "content": prompt}
    ]
    
    summary = generation(messages)
    
    with open(memory_file_path, "w") as memory_file:
        memory_file.write(summary)

    memory = summary

def welcome(presentation):
    global personality, emoji, memory, interactions
    
    messages=[
        {"role": "system", "content": personality},
        {"role": "system", "content": emoji},
        {"role": "system", "content": "User answered question about themselves, write from the given information a presentation for the user to the other member of the server. Use bullet points. Make it Discord formatted."},
        {"role": "system", "content": "Language : French"},
        {"role": "user", "content": presentation}
    ]
    
    response_content = generation(messages)

    return response_content

def imagine(user, prompt):
    url = img_generation(user, prompt)

    img_data = requests.get(url).content
    img_path = os.path.join(IMG_DIR, f"tmp_gen.png")
    with open(img_path, 'wb') as handler:
        handler.write(img_data)

    return img_path