from typing import List, Optional
from fastapi import HTTPException, status
from .models import User, DocumentLock

def check_permission(user: User, doc_id: str, required_role: str = 'owner') -> bool:
    """
    Checks if the user has the required role to access the document locks.
    
    Args:
        user (User): The user object.
        doc_id (str): The document ID.
        required_role (str): The required role ('owner' or 'admin').
        
    Returns:
        bool: True if the user has the required role, False otherwise.
        
    Raises:
        HTTPException: If the user does not have the required role.
    """
    if user.role == required_role or user.role == 'admin':
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have the required permissions to view the locks."
        )

def get_active_locks_with_permissions(user: User, doc_id: str) -> List[DocumentLock]:
    """
    Retrieves active locks for a document while respecting user permissions.
    
    Args:
        user (User): The user object.
        doc_id (str): The document ID.
        
    Returns:
        List[DocumentLock]: A list of active locks.
    """
    if check_permission(user, doc_id):
        # Assuming there's a method to fetch active locks based on doc_id
        active_locks = DocumentLock.get_active_locks(doc_id)
        return active_locks
    return []

# Example usage:
# user = User(role='owner')
# doc_id = 'example_doc_id'
# locks = get_active_locks_with_permissions(user, doc_id)