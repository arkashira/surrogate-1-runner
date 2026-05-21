import React from 'react';

interface ServiceFilterProps {
  onChange: (serviceType: string) => void;
}

const ServiceFilter: React.FC<ServiceFilterProps> = ({ onChange }) => {
  const handleChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    onChange(event.target.value);
  };

  return (
    <div className="service-filter">
      <select onChange={handleChange}>
        <option value="">All Services</option>
        <option value="compute">Compute</option>
        <option value="storage">Storage</option>
        <option value="networking">Networking</option>
      </select>
    </div>
  );
};

export default ServiceFilter;