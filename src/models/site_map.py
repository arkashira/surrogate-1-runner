from typing import List, Dict, Any, Optional
from pydantic import BaseModel, validator, ValidationError

class SiteMapNode(BaseModel):
    title: str
    url: str
    children: Optional[List['SiteMapNode']] = []

    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Title cannot be empty')
        return v.strip()

    @validator('url')
    def url_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('URL cannot be empty')
        return v.strip()

    @validator('url')
    def url_must_be_unique(cls, v, values, **kwargs):
        # This validator will be called during full tree validation
        return v

class SiteMap(BaseModel):
    root: SiteMapNode

    @validator('root')
    def check_unique_urls(cls, root, values, **kwargs):
        urls = set()
        stack = [root]
        
        while stack:
            node = stack.pop()
            if node.url in urls:
                raise ValueError(f'Duplicate URL found: {node.url}')
            urls.add(node.url)
            if node.children:
                stack.extend(node.children)
        
        return root

    @classmethod
    def validate_json(cls, data: Dict[str, Any]) -> 'SiteMap':
        try:
            return cls(**data)
        except ValidationError as e:
            raise ValueError(f'Validation error: {e}')
        except Exception as e:
            raise ValueError(f'Invalid site map structure: {str(e)}')