import datetime
import logging
from typing import List

class DigestService:
    def __init__(self, updates: List[dict]):
        self.updates = updates

    def identify_important_updates(self) -> List[dict]:
        # Define predefined criteria to identify important updates
        important_updates = []
        for update in self.updates:
            if update['priority'] == 'high' or update['category'] == 'critical':
                important_updates.append(update)
        return important_updates

    def generate_daily_digest(self) -> str:
        important_updates = self.identify_important_updates()
        digest = 'Daily Digest:\n'
        for update in important_updates:
            digest += f"- {update['title']}: {update['description']}\n"
        return digest

    def send_daily_digest(self, team_members: List[dict]) -> None:
        digest = self.generate_daily_digest()
        for member in team_members:
            # Automatically translate the digest into the team member's preferred language
            translated_digest = self.translate_digest(digest, member['language'])
            # Send the translated digest to the team member
            self.send_email(member['email'], translated_digest)

    def translate_digest(self, digest: str, language: str) -> str:
        # Implement translation logic here
        # For demonstration purposes, assume a simple translation function
        translations = {
            'en': digest,
            'fr': 'Digeste quotidien:\n' + digest.replace('Daily Digest:', '').replace('high', 'élevé').replace('critical', 'critique'),
            # Add more languages as needed
        }
        return translations.get(language, digest)

    def send_email(self, email: str, digest: str) -> None:
        # Implement email sending logic here
        # For demonstration purposes, assume a simple email sending function
        logging.info(f'Sending email to {email} with digest: {digest}')

# Example usage
if __name__ == '__main__':
    updates = [
        {'title': 'Update 1', 'description': 'This is update 1', 'priority': 'high', 'category': 'critical'},
        {'title': 'Update 2', 'description': 'This is update 2', 'priority': 'low', 'category': 'info'},
        {'title': 'Update 3', 'description': 'This is update 3', 'priority': 'high', 'category': 'critical'},
    ]
    team_members = [
        {'email': 'member1@example.com', 'language': 'en'},
        {'email': 'member2@example.com', 'language': 'fr'},
    ]
    digest_service = DigestService(updates)
    digest_service.send_daily_digest(team_members)