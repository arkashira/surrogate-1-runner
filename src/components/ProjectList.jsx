import React, { useState, useEffect } from 'react';
import { getProjects, deleteProject, cancelIngestion } from '../api/projects';

const ProjectList = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const response = await getProjects();
      setProjects(response.data);
    } catch (err) {
      setError('Failed to load projects');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (projectId) => {
    if (window.confirm('Are you sure you want to delete this project?')) {
      try {
        await deleteProject(projectId);
        setProjects(projects.filter(p => p.id !== projectId));
      } catch (err) {
        setError('Failed to delete project');
      }
    }
  };

  const handleCancelIngestion = async (projectId) => {
    try {
      await cancelIngestion(projectId);
      setProjects(projects.map(p => 
        p.id === projectId ? { ...p, ingestionStatus: 'cancelled' } : p
      ));
    } catch (err) {
      setError('Failed to cancel ingestion');
    }
  };

  if (loading) return <div>Loading projects...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div className="project-list">
      <h2>Projects</h2>
      {projects.length === 0 ? (
        <p>No projects found</p>
      ) : (
        <ul>
          {projects.map(project => (
            <li key={project.id} className="project-item">
              <div className="project-info">
                <h3>{project.name}</h3>
                <p>Status: {project.ingestionStatus || 'Not started'}</p>
              </div>
              <div className="project-actions">
                {project.ingestionStatus === 'running' && (
                  <button 
                    onClick={() => handleCancelIngestion(project.id)}
                    className="cancel-btn"
                  >
                    Cancel Ingestion
                  </button>
                )}
                <button 
                  onClick={() => handleDelete(project.id)}
                  className="delete-btn"
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default ProjectList;