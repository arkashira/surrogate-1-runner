"""
轻量级Markdown文档全文搜索系统，使用SQLite FTS5实现高效搜索。
支持文档索引、动态更新和全文检索，包含完整的错误处理和类型注解。
"""

import os
import sqlite3
from pathlib import Path
from typing import Iterable, List, Dict, Optional, Union

__all__ = ["init_db", "index_docs", "search", "DocumentMetadata"]


class DocumentMetadata:
    """存储文档元数据（可选，用于扩展功能）"""
    def __init__(self, doc_id: int, title: str, content: str, tags: List[str] = None):
        self.doc_id = doc_id
        self.title = title
        self.content = content
        self.tags = tags or []


def init_db(db_path: Union[str, Path]) -> None:
    """
    初始化SQLite数据库，创建FTS5虚拟表和元数据表。
    
    参数:
        db_path: 数据库文件路径
    """
    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建元数据表（可选，用于存储扩展信息）
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS docs_metadata (
            doc_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 创建FTS5虚拟表用于搜索
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS docs_search
        USING fts5(
            title,
            content,
            tags,
            tokenize = 'porter unicode61'
        );
    """)
    
    conn.commit()
    conn.close()


def _extract_title_and_content(md_path: Path) -> Optional[Dict[str, str]]:
    """
    从Markdown文件中提取标题和内容。
    
    参数:
        md_path: Markdown文件路径
        
    返回:
        包含'title'和'content'的字典，或None（文件无效）
    """
    try:
        text = md_path.read_text(encoding="utf-8")
    except Exception as e:
        return None
    
    lines = text.splitlines()
    title = None
    content_lines = []
    
    for line in lines:
        if title is None and line.startswith("#"):
            # 移除标题符号和空格
            title = line.lstrip("#").strip()
        else:
            content_lines.append(line)
    
    if not title:
        title = md_path.stem
    
    return {
        "title": title,
        "content": "\n".join(content_lines)
    }


def index_docs(docs_dir: Union[str, Path], db_path: Union[str, Path]) -> None:
    """
    索引目录中的Markdown文件（追加模式，不删除现有数据）。
    
    参数:
        docs_dir: 包含Markdown文件的目录
        db_path: 数据库文件路径
    """
    docs_dir = Path(docs_dir)
    db_path = Path(db_path)
    
    if not docs_dir.is_dir():
        raise ValueError(f"文档目录 {docs_dir} 不存在或不是目录")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 索引所有Markdown文件
    for md_file in docs_dir.rglob("*.md"):
        data = _extract_title_and_content(md_file)
        if not data:
            continue
        
        # 插入元数据
        cursor.execute("""
            INSERT INTO docs_metadata (title, content, tags)
            VALUES (?, ?, ?)
        """, (data["title"], data["content"], str(data.get("tags", []))))
        
        # 插入搜索表
        cursor.execute("""
            INSERT INTO docs_search (title, content, tags)
            VALUES (?, ?, ?)
        """, (data["title"], data["content"], str(data.get("tags", []))))
    
    conn.commit()
    conn.close()


def search(query: str, db_path: Union[str, Path], limit: int = 10) -> List[Dict[str, str]]:
    """
    执行全文搜索并返回片段。
    
    参数:
        query: 搜索字符串（支持FTS5语法）
        db_path: 数据库文件路径
        limit: 返回结果数量
        
    返回:
        包含{id, title, snippet}的字典列表
    """
    db_path = Path(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 使用snippet()函数获取搜索片段
    cursor.execute("""
        SELECT rowid, title, snippet(docs_search, -1, '[', ']', '...', 20)
        FROM docs_search
        WHERE docs_search MATCH ?
        ORDER BY rank
        LIMIT ?
    """, (query, limit))
    
    results = []
    for rowid, title, snippet in cursor.fetchall():
        results.append({
            "id": rowid,
            "title": title,
            "snippet": snippet
        })
    
    conn.close()
    return results