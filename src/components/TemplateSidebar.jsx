import React from 'react';
import PropTypes from 'prop-types';
import { templates } from '../templates';
import './TemplateSidebar.css';

/**
 * TemplateSidebar renders a list of curated templates in the sidebar.
 *
 * Props:
 * - onUseTemplate: function(template) => void
 *   Called when the user clicks the "Use" button for a template.
 */
const TemplateSidebar = ({ onUseTemplate }) => {
  return (
    <aside className="template-sidebar">
      <h2 className="sidebar-title">Templates</h2>
      <ul className="template-list">
        {templates.map((tpl) => (
          <li key={tpl.id} className="template-item">
            <div className="template-header">
              <span className="template-name">{tpl.name}</span>
              <button
                className="use-button"
                onClick={() => onUseTemplate(tpl)}
                aria-label={`Use ${tpl.name}`}
              >
                Use
              </button>
            </div>
            <p className="template-description">{tpl.description}</p>
            {tpl.parameters && tpl.parameters.length > 0 && (
              <ul className="template-params">
                {tpl.parameters.map((param) => (
                  <li key={param} className="template-param">
                    {param}
                  </li>
                ))}
              </ul>
            )}
          </li>
        ))}
      </ul>
    </aside>
  );
};

TemplateSidebar.propTypes = {
  onUseTemplate: PropTypes.func.isRequired,
};

export default TemplateSidebar;