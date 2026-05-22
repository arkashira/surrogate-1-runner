import React, { useState } from 'react';
import { Search } from './Search';
import { GuideContent } from './GuideContent';
import './TroubleshootingGuide.css';

const TroubleshootingGuide = () => {
  const [searchTerm, setSearchTerm] = useState('');

  return (
    <div className="troubleshooting-guide">
      <h2>Troubleshooting Guide</h2>
      <Search onSearch={setSearchTerm} />
      <GuideContent searchTerm={searchTerm} />
    </div>
  );
};

export default TroubleshootingGuide;