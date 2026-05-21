import React, { useState } from 'react';
import './styles/console.css';

// Configuration for available services
const services = [
  { id: 'ec2', name: 'EC2', description: 'Virtual Servers in the Cloud' },
  { id: 's3', name: 'S3', description: 'Scalable Storage in the Cloud' },
  { id: 'lambda', name: 'Lambda', description: 'Run Code without Thinking about Servers' },
  { id: 'dynamodb', name: 'DynamoDB', description: 'Fast and Flexible NoSQL Database' },
  { id: 'cloudwatch', name: 'CloudWatch', description: 'Monitor Resources and Applications' },
];

const AWSConsole = () => {
  const [activeServiceId, setActiveServiceId] = useState(services[0].id);

  // Dynamic content renderer
  const renderContent = () => {
    const service = services.find(s => s.id === activeServiceId);
    return (
      <div className="service-dashboard">
        <h2>{service.name} Dashboard</h2>
        <div className="placeholder-box">
          <p><strong>Sandbox Mode:</strong> Interacting with {service.name} resources is simulated.</p>
          <p className="description">{service.description}</p>
          <button className="mock-action-btn">Launch {service.name} Instance</button>
        </div>
      </div>
    );
  };

  return (
    <div className="aws-console-container">
      {/* Sidebar Navigation */}
      <aside className="aws-sidebar">
        <div className="sidebar-header">
          <h1>AWS</h1>
        </div>
        <nav>
          <ul className="service-nav-list">
            {services.map((service) => (
              <li 
                key={service.id}
                className={service.id === activeServiceId ? 'active' : ''}
                onClick={() => setActiveServiceId(service.id)}
              >
                {service.name}
              </li>
            ))}
          </ul>
        </nav>
      </aside>

      {/* Main Content Area */}
      <main className="aws-main-content">
        <header className="content-header">
          <h3>{services.find(s => s.id === activeServiceId).name} Management Console</h3>
          <div className="user-profile">Admin User</div>
        </header>
        <div className="content-body">
          {renderContent()}
        </div>
      </main>
    </div>
  );
};

export default AWSConsole;