-- 创建完整数据库结构
DROP TABLE IF EXISTS docs_metadata;
DROP TABLE IF EXISTS docs_search;

CREATE TABLE IF NOT EXISTS docs_metadata (
    doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    tags TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE VIRTUAL TABLE IF NOT EXISTS docs_search
USING fts5(
    title,
    content,
    tags,
    tokenize = 'porter unicode61'
);