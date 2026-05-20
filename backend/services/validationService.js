const db = require('../db');

class ValidationService {
  async getProjects() {
    const { rows } = await db.query(
      `SELECT id, name, created_at, progress, status
       FROM projects
       ORDER BY created_at DESC`
    );
    return rows.map(this.formatProject);
  }

  async createProject(name) {
    const { rows } = await db.query(
      `INSERT INTO projects (name, created_at, progress, status)
       VALUES ($1, NOW(), 0, 'InProgress')
       RETURNING id, name, created_at, progress, status`,
      [name]
    );
    return this.formatProject(rows[0]);
  }

  formatProject(p) {
    return {
      id: p.id,
      name: p.name,
      createdAt: p.created_at.toISOString(),
      progress: p.progress,
      status: p.status,
    };
  }
}

module.exports = new ValidationService();