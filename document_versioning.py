class DocumentVersioning:
    def __init__(self, document_id):
        self.document_id = document_id
        self.versions = []

    def create_version(self, content):
        version_id = len(self.versions) + 1
        version = {
            'id': version_id,
            'content': content,
            'timestamp': datetime.now()
        }
        self.versions.append(version)
        return version_id

    def get_version_history(self):
        return self.versions

    def revert_to_version(self, version_id):
        for version in self.versions:
            if version['id'] == version_id:
                self.versions[-1] = version
                return True
        return False


def main():
    # Example usage
    doc_versioning = DocumentVersioning('doc1')
    doc_versioning.create_version('Initial content')
    doc_versioning.create_version('Updated content')
    print(doc_versioning.get_version_history())
    doc_versioning.revert_to_version(1)
    print(doc_versioning.get_version_history())


if __name__ == "__main__":
    main()