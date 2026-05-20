import React from 'react';
import MarkdownModal from './MarkdownModal';

interface DashboardProps {
  playbooks: Array<{ title: string; date: string; excerpt: string; content: string }>;
}

const Dashboard: React.FC<DashboardProps> = ({ playbooks }) => {
  const [selectedPlaybook, setSelectedPlaybook] = useState<string | null>(null);

  const openModal = (content: string) => {
    setSelectedPlaybook(content);
  };

  const closeModal = () => {
    setSelectedPlaybook(null);
  };

  return (
    <div className="dashboard">
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Date</th>
            <th>Excerpt</th>
          </tr>
        </thead>
        <tbody>
          {playbooks.map((playbook) => (
            <tr key={playbook.title} onClick={() => openModal(playbook.content)}>
              <td>{playbook.title}</td>
              <td>{playbook.date}</td>
              <td>{playbook.excerpt}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <MarkdownModal isOpen={!!selectedPlaybook} onRequestClose={closeModal} markdownContent={selectedPlaybook || ''} />
    </div>
  );
};

export default Dashboard;