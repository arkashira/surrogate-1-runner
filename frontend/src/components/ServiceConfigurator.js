import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ServiceConfigurator = ({ selectedService }) => {
  const [config, setConfig] = useState({});

  useEffect(() => {
    if (selectedService) {
      axios.get(`/api/aws/services/${selectedService.id}/config`)
        .then(response => {
          setConfig(response.data);
        })
        .catch(error => {
          console.error(error);
        });
    }
  }, [selectedService]);

  const handleConfigChange = (event) => {
    setConfig({ ...config, [event.target.name]: event.target.value });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    axios.post(`/api/aws/services/${selectedService.id}/config`, config)
      .then(response => {
        console.log(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  };

  return (
    <div>
      <h2>Service Configurator</h2>
      <form onSubmit={handleSubmit}>
        {Object.keys(config).map((key) => (
          <div key={key}>
            <label>{key}</label>
            <input
              type="text"
              name={key}
              value={config[key]}
              onChange={handleConfigChange}
            />
          </div>
        ))}
        <button type="submit">Save Config</button>
      </form>
    </div>
  );
};

export default ServiceConfigurator;