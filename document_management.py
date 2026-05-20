class DocumentManager:
    def __init__(self):
        self.documents = {}

    def create_document(self, doc_id, content):
        """
        Create a new document with the given ID and content.
        """
        if doc_id in self.documents:
            raise ValueError("Document already exists")
        self.documents[doc_id] = {'content': content, 'versions': [content]}

    def edit_document(self, doc_id, new_content):
        """
        Edit an existing document with the given ID and new content.
        """
        if doc_id not in self.documents:
            raise ValueError("Document does not exist")
        self.documents[doc_id]['content'] = new_content
        self.documents[doc_id]['versions'].append(new_content)

    def delete_document(self, doc_id):
        """
        Delete an existing document with the given ID.
        """
        if doc_id not in self.documents:
            raise ValueError("Document does not exist")
        del self.documents[doc_id]

    def get_version_history(self, doc_id):
        """
        Get the version history of a document with the given ID.
        """
        if doc_id not in self.documents:
            raise ValueError("Document does not exist")
        return self.documents[doc_id]['versions']

    def revert_to_previous_version(self, doc_id, version_index):
        """
        Revert a document to a previous version specified by the index.
        """
        if doc_id not in self.documents:
            raise ValueError("Document does not exist")
        if version_index < 0 or version_index >= len(self.documents[doc_id]['versions']):
            raise ValueError("Invalid version index")
        self.documents[doc_id]['content'] = self.documents[doc_id]['versions'][version_index]