import React from 'react';
import ServiceSelector from './components/ServiceSelector';
import ServiceConfigurator from './components/ServiceConfigurator';

const App = () => {
  const [selectedService, setSelectedService] = useState(null);

  const handleServiceSelect = (service) => {
    setSelectedService(service);
  };

  return (
    <div>
      <ServiceSelector onServiceSelect={handleServiceSelect} />
      {selectedService && <ServiceConfigurator selectedService={selectedService} />}
    </div>
  );
};

export default App;