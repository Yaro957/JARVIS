import csv
import sqlite3

conn = sqlite3.connect('jarvis.db')
cursor = conn.cursor()

# # Create table
# query = "CREATE TABLE IF NOT EXISTS SYS_COMMAND(id integer primary key, name varchar(100), path varchar(1000))"
# cursor.execute(query)

# # Insert all applications
# applications = [
#     ('android studio','C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Android Studio\\Android Studio.lnk'),
#     ('brave browser', 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe'),
#     ('calculator', 'C:\\Windows\\System32\\calc.exe'),
#     ('capcut', 'C:\\Users\\omjum\\AppData\\Local\\CapCut\\CapCut.exe'),
#     ('clock', 'ms-clock:'),
#     ('command prompt', 'C:\\WINDOWS\\system32\\cmd.exe'),
#     ('discord', 'C:\\ProgramData\\omjum\\Discord\\Update.exe'),
#     ('excel', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE'),
#     ('google chrome', 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'),
#     ('grand theft auto v', 'E:\\Games\\Grand Theft Auto V\\GTAVLauncher.exe'),
#     ('harmony music', 'C:\\Users\\omjum\\AppData\\Local\\Programs\\harmonymusic\\harmonymusic.exe'),
#     ('microsoft edge', 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'),
#     ('mozilla firefox', 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'),
#     ('notepad', 'C:\\Windows\\System32\\notepad.exe'),
#     ('postman', 'C:\\Users\\omjum\\AppData\\Local\\Postman\\Postman.exe'),
#     ('powerpoint', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE'),
#     ('teams', 'C:\\Users\\omjum\\AppData\\Local\\Microsoft\\Teams\\current\\Teams.exe'),
#     ('visual studio code', 'C:\\Users\\omjum\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'),
#     ('watch dogs 2', 'E:\\Games\\Watch Dogs 2\\bin\\WatchDogs2.exe'),
#     ('whatsapp', 'C:\\Users\\omjum\\AppData\\Local\\WhatsApp\\WhatsApp.exe'),
#     ('word', 'C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE'),
#     ('zoom', 'C:\\Users\\omjum\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe')
# ]

# # Insert all applications using executemany for efficiency
# query = "INSERT INTO SYS_COMMAND (name, path) VALUES (?, ?)"
# cursor.executemany(query, applications)

# conn.commit()
# conn.close()

# print("Database created and applications inserted successfully!")


# Create WEBCOMMAND table
# query = "CREATE TABLE IF NOT EXISTS WEBCOMMAND(id integer primary key, name varchar(100), url varchar(1000))"
# cursor.execute(query)

# List of commonly used websites
# websites = [
#     ('amazon', 'https://www.amazon.com'),
#     ('chatgpt', 'https://chat.openai.com'),
#     ('claude', 'https://claude.ai'),
#     ('discord', 'https://discord.com'),
#     ('facebook', 'https://www.facebook.com'),
#     ('gemini', 'https://gemini.google.com'),
#     ('github', 'https://github.com'),
#     ('gmail', 'https://mail.google.com'),
#     ('google', 'https://www.google.com'),
#     ('instagram', 'https://www.instagram.com'),
#     ('linkedin', 'https://www.linkedin.com'),
#     ('netflix', 'https://www.netflix.com'),
#     ('reddit', 'https://www.reddit.com'),
#     ('spotify', 'https://open.spotify.com'),
#     ('stack overflow', 'https://stackoverflow.com'),
#     ('twitter', 'https://twitter.com'),
#     ('whatsapp web', 'https://web.whatsapp.com'),
#     ('x', 'https://x.com'),
#     ('youtube', 'https://www.youtube.com'),
#     ('youtube music', 'https://music.youtube.com')
# ]

# # Insert all websites
# query = "INSERT INTO WEBCOMMAND (name, url) VALUES (?, ?)"
# cursor.executemany(query, websites)

# conn.commit()
# conn.close()

# print("WEBCOMMAND table created and websites inserted successfully!")

# creating table for contacts
cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')

# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
desired_columns_indices = [0,1,2]

# Read data from CSV and insert into SQLite table for the desired columns
with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    for row in csvreader:
        if len(row) < 2:
            continue  # skip empty or invalid rows
        elif len(row) == 2:
            row.append(None)  # add a placeholder for missing email 
        selected_data = [row[i] for i in desired_columns_indices]
        cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no','email') VALUES (null, ?, ?,?);''', tuple(selected_data))

# Commit changes and close connection
# cursor.execute("DELETE FROM  contacts")
# query = 'om jumde'
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()
# print(results[0][0])

conn.commit()
conn.close()