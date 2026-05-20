
import React, { useState } from 'react';
import { useQuery } from '@apollo/client';
import GET_PLAYBOOKS from './queries/GetPlaybooks.graphql';
import PlaybookModal from './PlaybookModal';

const Playbooks = () => {
  const { loading, error, data } = useQuery(GET_PLAYBOOKS);
  const [selectedPlaybook, setSelectedPlaybook] = useState(null);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error :(</div>;

  return (
    <div>
      {data.playbooks.map((playbook) => (
        <div key={playbook.id} onClick={() => setSelectedPlaybook(playbook)}>
          <h3>{playbook.title}</h3>
          <p>{playbook.excerpt}</p>
          <small>{new Date(playbook.createdAt).toLocaleDateString()}</small>
        </div>
      ))}
      {selectedPlaybook && <PlaybookModal playbook={selectedPlaybook} />}
    </div>
  );
};

export default Playbooks;

// src/queries/GetPlaybooks.graphql

query GetPlaybooks {
  playbooks {
    id
    title
    excerpt
    createdAt
  }
}

// src/components/PlaybookModal.tsx

import React from 'react';
import { useState } from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@apollo/client';
import GET_PLAYBOOK_BY_ID from './queries/GetPlaybookById.graphql';

const PlaybookModal = ({ playbook }) => {
  const { id } = useParams();

  const { loading, error, data } = useQuery(GET_PLAYBOOK_BY_ID, {
    variables: { id: id || playbook.id },
  });

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error :(</div>;

  return (
    <div>
      <h1>{data.playbook.title}</h1>
      <div dangerouslySetInnerHTML={{ __html: data.playbook.content }} />
    </div>
  );
};

export default PlaybookModal;

// src/queries/GetPlaybookById.graphql

query GetPlaybookById($id: ID!) {
  playbook(id: $id) {
    id
    title
    content
  }
}