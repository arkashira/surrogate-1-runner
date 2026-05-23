import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const DashboardLandingPage: React.FC = () => {
  const { currentUser } = useAuth();
  const navigate = useNavigate();

  React.useEffect(() => {
    if (!currentUser) {
      navigate('/login');
    }
  }, [currentUser, navigate]);

  return (
    <div className="dashboard-container">
      <h1>Welcome to Your Dashboard</h1>
      <p>Here you can find tailored marketing guidance and manage your account.</p>
      {/* Add more dashboard content here */}
    </div>
  );
};

export default DashboardLandingPage;