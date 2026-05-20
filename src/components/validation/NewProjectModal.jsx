import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import './NewProjectModal.css';

export default function NewProjectModal({ isOpen, onClose, onProjectCreated }) {
  const navigate = useNavigate();
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm();

  const [apiError, setApiError] = useState('');

  const onSubmit = async (data) => {
    setApiError('');
    try {
      const response = await fetch('/api/projects', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: data.name,
          description: data.description,
          targetMarket: data.targetMarket,
        }),
      });
      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.message || 'Failed to create project');
      }
      const newProject = await response.json();
      onProjectCreated?.(newProject);
      onClose();
      navigate(`/workflow/${newProject.id}/step/1`);
    } catch (err) {
      setApiError(err.message);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <h2>Create New Validation Project</h2>
        <form onSubmit={handleSubmit(onSubmit)} noValidate>
          <div className="form-group">
            <label htmlFor="name">Project Name</label>
            <input
              id="name"
              type="text"
              maxLength={100}
              {...register('name', { required: true, maxLength: 100 })}
            />
            {errors.name && <span className="error">Name is required (max 100 chars)</span>}
          </div>

          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              maxLength={100}
              {...register('description', { required: true, maxLength: 100 })}
            />
            {errors.description && <span className="error">Description is required (max 100 chars)</span>}
          </div>

          <div className="form-group">
            <label htmlFor="targetMarket">Target Market</label>
            <input
              id="targetMarket"
              type="text"
              maxLength={100}
              {...register('targetMarket', { required: true, maxLength: 100 })}
            />
            {errors.targetMarket && <span className="error">Target Market is required (max 100 chars)</span>}
          </div>

          {apiError && <div className="api-error">{apiError}</div>}

          <div className="modal-actions">
            <button type="button" onClick={onClose} disabled={isSubmitting}>
              Cancel
            </button>
            <button type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Creating...' : 'Create Project'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}