import sqlite3

# Connect to the SQLite database (if it doesn't exist, it will be created)
conn = sqlite3.connect('knowledge.db')
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS knowledge (
                    question TEXT PRIMARY KEY,
                    answer TEXT
                )''')
conn.commit()


# Function to get a response from the database
def get_response_from_db(question):
    # Apply strip() and lower() to normalize the input
    question = question.strip().lower()
    cursor.execute("SELECT answer FROM knowledge WHERE question=?", (question,))
    result = cursor.fetchone()
    return result[0] if result else None


# Function to learn a new response
def learn_new_knowledge_db(question, answer):
    # Apply strip() and lower() to normalize the question
    question = question.strip().lower()
    cursor.execute("INSERT OR REPLACE INTO knowledge (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()

# Function to list all stored knowledge
def list_all_knowledge():
    cursor.execute("SELECT * FROM knowledge")
    results = cursor.fetchall()
    if results:
        for row in results:
            print(f"Question: {row[0]}, Answer: {row[1]}")
    else:
        print("There is no knowledge stored in the database.")

# Interaction with the user
def chat():
    while True:
        user_input = input("Tell Me: ").strip().lower()  # Normalize the input from the user

        # If the user wants to see all stored knowledge
        if user_input == "show all":
            list_all_knowledge()
            continue

        response = get_response_from_db(user_input)

        if response:
            print(f"Bot: {response}")
        else:
            print("I don't understand what you're saying. Would you like to teach me a new response?")
            should_learn = input("Would you like to teach me? (yes/no): ").strip().lower()
            if should_learn.lower() == "yes":
                new_question = user_input  # Use the normalized input as the new question
                new_answer = input("Please, tell me the correct answer: ").strip()
                learn_new_knowledge_db(new_question, new_answer)
                print(f"Thank you! I've learned something new: {new_question} -> {new_answer}")


# Load initial knowledge into the database
def load_initial_knowledge():
    # Initial knowledge base
    initial_knowledge = {
        "hello": "Hello! How are you?",
        "how are you?": "I'm doing well, thank you for asking.",
        "what would you like to talk about?": "I can talk about many topics. Ask me anything!"
    }

    for question, answer in initial_knowledge.items():
        learn_new_knowledge_db(question, answer)


# Load initial knowledge into the database only if it doesn't exist
def check_and_load_initial_knowledge():
    cursor.execute("SELECT count(*) FROM knowledge")
    result = cursor.fetchone()[0]
    if result == 0:
        load_initial_knowledge()


# Check if initial knowledge needs to be loaded
check_and_load_initial_knowledge()

# Start the interaction with the user
chat()
