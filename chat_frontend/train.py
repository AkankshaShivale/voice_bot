from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot = ChatBot(
    "MyBot",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    database_uri="sqlite:///db.sqlite3",  # Fresh DB
    read_only=False,  # Allow training (but we control it)
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "maximum_similarity_threshold": 0.90,
            
        }
    ]
)

trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train("./greetings.yml", "./conversations.yml")  # Only your files

import sqlite3

# Step 1: Extract '--' lines from both YAML files
def extract_lines_from_file(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()
    return [
        line.strip()[4:]  # Remove the '- -' prefix
        for line in lines
        if line.strip().startswith('- - ')
    ]

# Extract lines from both YAML files
lines_from_greetings = extract_lines_from_file("greetings.yml")
lines_from_conversations = extract_lines_from_file("conversations.yml")

# Combine both lists
all_clean_lines = lines_from_greetings + lines_from_conversations

# Step 2: Connect to ChatterBot's SQLite DB
conn = sqlite3.connect("db.sqlite3")  # ChatterBot's DB
cursor = conn.cursor()
print("Connected to the database.")  # Debug: Connection status

# Step 3: Delete rows from Statement table where text matches any clean line
for line in all_clean_lines:
    print(f"Checking for statement: '{line}'")  # Debug: Currently checking statement
    cursor.execute("SELECT id, text FROM statement WHERE LOWER(text) = LOWER(?)", (line,))
    statement_ids = cursor.fetchall()
    
    if statement_ids:
        print(f"Found {len(statement_ids)} matching rows for: '{line}'")  # Debug: Found matching rows
    else:
        print(f"No matching rows found for: '{line}'")  # Debug: No match for current line

    for statement_id in statement_ids:
        # Debug: Deleting associated rows
        print(f"Deleting associated rows for statement ID: {statement_id[0]}")  
        
        # First, delete from the tag_association table where statement_id matches
        cursor.execute("DELETE FROM tag_association WHERE statement_id = ?", (statement_id[0],))
        
        # Then, delete the statement itself
        cursor.execute("DELETE FROM statement WHERE id = ?", (statement_id[0],))

# Step 4: Commit changes
conn.commit()
print("Changes committed to the database.")  # Debug: Committing changes

# Step 5: Close the connection
conn.close()
print("Database connection closed.")  # Debug: Closing connection

print("Matching rows deleted from Statement and related entries removed from tag_association.")
