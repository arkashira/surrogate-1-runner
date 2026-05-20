import csv
import sqlite3

class VocabularyDB:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vocabulary (
                id INTEGER PRIMARY KEY,
                term TEXT NOT NULL,
                definition TEXT NOT NULL,
                topic TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add_vocabulary(self, term, definition, topic):
        self.cursor.execute("""
            INSERT INTO vocabulary (term, definition, topic)
            VALUES (?, ?, ?)
        """, (term, definition, topic))
        self.conn.commit()

    def get_vocabulary_by_topic(self, topic):
        self.cursor.execute("""
            SELECT * FROM vocabulary
            WHERE topic = ?
        """, (topic,))
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

# src/vocabulary_data.csv
term,definition,topic
Network Switch,Device that connects multiple computers together,Networking
Router,Device that directs traffic between networks,Networking
Firewall,Device that blocks unauthorized access to a network,Networking
Cloud Computing,Delivery of computing services over the internet,Cloud
Containerization,Method of deploying applications in containers,Cloud
Microservices,Architecture pattern that structures applications as services,Cloud
API Gateway,Component that manages API requests and responses,Cloud
Load Balancer,Device that distributes traffic across multiple servers,Cloud