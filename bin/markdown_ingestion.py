import os
import markdown
import sqlite3
from typing import List, Tuple

def parse_markdown(file_path: str) -> List[Tuple[str, str]]:
    with open(file_path, 'r') as file:
        text = file.read()
    html = markdown.markdown(text)
    # Simple parsing to extract questions and answers
    # This is a placeholder and should be replaced with a more sophisticated parser
    qa_pairs = []
    lines = html.split('\n')
    for i in range(len(lines) - 1):
        if lines[i].startswith('<h1>') and lines[i+1].startswith('<p>'):
            question = lines[i].replace('<h1>', '').replace('</h1>', '')
            answer = lines[i+1].replace('<p>', '').replace('</p>', '')
            qa_pairs.append((question, answer))
    return qa_pairs

def store_qa_pairs(qa_pairs: List[Tuple[str, str]], db_path: str) -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS qa_pairs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    ''')
    cursor.executemany('INSERT INTO qa_pairs (question, answer) VALUES (?, ?)', qa_pairs)
    conn.commit()
    conn.close()

def main():
    markdown_file_path = 'path/to/markdown/file.md'
    db_path = 'path/to/surrogate-1/database.db'
    qa_pairs = parse_markdown(markdown_file_path)
    store_qa_pairs(qa_pairs, db_path)

if __name__ == '__main__':
    main()