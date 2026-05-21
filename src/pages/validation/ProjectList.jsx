import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ProgressBar, Badge } from 'react-bootstrap';
import axios from 'axios';
import './ProjectList.css';

/**
 * ProjectList Component
 *
 * Displays a list of validation projects fetched from the backend.
 * Each project shows its name, creation date, progress bar, and completion status.
 * Clicking a project navigates to its detail page.
 *
 * Polls for updates every 10 seconds.
 */
const ProjectList = () => {
  const [projects, setProjects] = useState([]);
  const navigate = useNavigate();

  const fetchProjects = async () => {
    try {
      const { data } = await axios.get('/api/validation/projects');
      setProjects(data);
    } catch (err) {
      console.error('Failed to fetch projects:', err);
    }
  };

  useEffect(() => {
    fetchProjects();
    const interval = setInterval(fetchProjects, 10000); // Poll every 10s
    return () => clearInterval(interval);
  }, []);

  const handleProjectClick = (projectId) => {
    navigate(`/validation/project/${projectId}`);
  };

  return (
    <div className="project-list-container">
      <h2>Validation Projects</h2>
      <ul className="project-list">
        {projects.map((project) => (
          <li
            key={project.id}
            className="project-item"
            onClick={() => handleProjectClick(project.id)}
          >
            <div className="project-header">
              <span className="project-name">{project.name}</span>
              <span className="project-date">
                {new Date(project.created_at).toLocaleDateString()}
              </span>
              {project.status === 'Completed' && (
                <Badge bg="success" className="completed-badge">
                  ✓
                </Badge>
              )}
            </div>
            <ProgressBar now={project.progress} label={`${project.progress}%`} />
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ProjectList;