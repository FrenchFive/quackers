import os
import random
import re
from openai import OpenAI
import requests
import qlogs
import json
import qquiz
from consts import DATA_DIR, IMG_DIR

from dotenv import load_dotenv
load_dotenv()

KEY_OPENAI = os.getenv("KEY_OPENAI")

if KEY_OPENAI == None:
    print("Error: There is currently no 'KEY_OPENAI' environment variable. Please create a .env with the required values.")
    exit(1)
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

def _parse_question(raw: str):
    parts = [p.strip() for p in raw.split("//")]
    if len(parts) != 6:
        return None
    try:
        qtext = parts[0].replace("Q:", "").strip()
        optA = parts[1][2:].strip() if parts[1].startswith("A") else parts[1]
        optB = parts[2][2:].strip() if parts[2].startswith("B") else parts[2]
        optC = parts[3][2:].strip() if parts[3].startswith("C") else parts[3]
        optD = parts[4][2:].strip() if parts[4].startswith("D") else parts[4]
        ans = parts[5].split(":")[-1].strip().upper()[0]
    except Exception:
        return None
    return {"q": qtext, "A": optA, "B": optB, "C": optC, "D": optD, "answer": ans}


def _generate_single_question(category: str, difficulty: str):
    prompt = (
        f"Generate one {difficulty} multiple choice question about {category}. "
        "Respond on a single line exactly formatted as: "
        "Q: question ? // A) choice1 // B) choice2 // C) choice3 // D) choice4 // ANSWER: <A/B/C/D>"
    )
    messages = [{"role": "user", "content": prompt}]
    return generation(messages)


def _originality_score(question: str, others):
    if not others:
        return 10
    lines = "\n".join(others)
    prompt = (
        "On a scale from 1 to 10, how different is the following question from the list provided?\n"
        f"Question: {question}\nList:{lines}\nRespond with only the number."
    )
    messages = [{"role": "user", "content": prompt}]
    resp = generation(messages)
    match = re.search(r"(\d+)", resp)
    if not match:
        return 10
    return int(match.group(1))


def generate_quiz(guild: int):
    """Generate a list of 10 unique questions for the given guild."""
    cat_path = os.path.join(DATA_DIR, "txt/quiz_categories.txt")
    with open(cat_path, "r", encoding="utf-8") as f:
        categories = [l.strip() for l in f if l.strip()]
    difficulties = ["easy"] * 2 + ["medium"] * 4 + ["hard"] * 4
    questions = []
    for i in range(10):
        category = random.choice(categories)
        diff = difficulties[i]
        while True:
            raw = _generate_single_question(category, diff)
            q = _parse_question(raw)
            if not q:
                continue
            q["category"] = category
            q["difficulty"] = diff
            existing_global = qquiz.get_questions_by_category(category)
            existing_guild = qquiz.get_questions_by_category(category, guild)
            if q["q"] in existing_global or q["q"] in existing_guild:
                continue
            score = _originality_score(q["q"], existing_global)
            if score < 6:
                continue
            questions.append(q)
            break
    return questions

