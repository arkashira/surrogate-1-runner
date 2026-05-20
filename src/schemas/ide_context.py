from typing import Optional, List, Dict, Any

class IdeContext:
    def __init__(self, user: str, selection: Optional[Dict[str, List[int]]] = None, cursor: Optional[Dict[str, int]] = None):
        self.user = user
        self.selection = selection
        self.cursor = cursor

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the IdeContext object to a dictionary for JSON serialization.
        
        Returns:
            Dict[str, Any]: A dictionary representation of the IdeContext object.
        """
        return {
            'user': self.user,
            'selection': self.selection if self.selection is not None else {},
            'cursor': self.cursor if self.cursor is not None else {}
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IdeContext':
        """
        Creates an IdeContext object from a dictionary.
        
        Args:
            data (Dict[str, Any]): A dictionary containing the necessary fields to create an IdeContext object.
            
        Returns:
            IdeContext: An instance of IdeContext created from the provided dictionary.
        """
        return cls(
            user=data.get('user', ''),
            selection=data.get('selection'),
            cursor=data.get('cursor')
        )