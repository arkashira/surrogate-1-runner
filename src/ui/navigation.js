import React from 'react';
import { Link } from 'react-router-dom';

const Navigation = () => {
  const navItems = [
    { label: 'Home', path: '/' },
    { label: 'Marketing Framework', path: '/framework' }, // Direct top-level access
    { label: 'Resources', path: '/resources' },
  ];

  return (
    <nav className="bg-white shadow-md p-4">
      <div className="container mx-auto flex justify-between items-center">
        <div className="text-xl font-bold text-indigo-600">Axentx SaaS</div>
        <div className="flex space-x-4">
          {navItems.map(item => (
            <Link
              key={item.path}
              to={item.path}
              className="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded transition"
            >
              {item.label}
            </Link>
          ))}
        </div>
      </div>
    </nav>
  );
};

export default Navigation;