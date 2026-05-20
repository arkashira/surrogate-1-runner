import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ServiceSelector = () => {
  const [services, setServices] = useState([]);
  const [selectedService, setSelectedService] = useState(null);

  useEffect(() => {
    axios.get('/api/aws/services')
      .then(response => {
        setServices(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  }, []);

  const handleServiceSelect = (service) => {
    setSelectedService(service);
  };

  return (
    <div>
      <h2>Service Selector</h2>
      <ul>
        {services.map((service) => (
          <li key={service.id}>
            <input
              type="radio"
              name="service"
              value={service.id}
              checked={selectedService === service}
              onChange={() => handleServiceSelect(service)}
            />
            <span>{service.name}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ServiceSelector;