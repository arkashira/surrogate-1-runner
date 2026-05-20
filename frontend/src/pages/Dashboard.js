import React from 'react';
import UpdateButton from '../components/UpdateButton';

const Dashboard = () => {
  const supportedServices = ['service1', 'service2', 'service3']; // Example services

  return (
    <div>
      <h1>Dashboard</h1>
      {supportedServices.map((service) => (
        <div key={service}>
          <h2>{service}</h2>
          <UpdateButton serviceName={service} />
        </div>
      ))}
    </div>
  );
};

export default Dashboard;