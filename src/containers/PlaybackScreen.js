import React, { useEffect, useState } from 'react';
import AudioPlayer from '../components/AudioPlayer';

const PlaybackScreen = ({ recording }) => {
  const [metadata, setMetadata] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMetadata = async () => {
      try {
        // Construct the API endpoint URL
        const response = await fetch(`/api/recordings/${recording.id}/metadata`);

        // Check if the response is successful
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Parse the JSON response
        const data = await response.json();
        setMetadata(data);
      } catch (error) {
        console.error('Failed to fetch metadata:', error);
        // Set an error state to display a user-friendly message
        setError('Failed to load recording metadata. Please try again later.');
      }
    };

    fetchMetadata();
  }, [recording.id]); // Re-run effect if recording ID changes

  // Show error message if an error occurred
  if (error) {
    return <div className="error-message">{error}</div>;
  }

  // Show loading state if metadata is still being fetched
  if (!metadata) {
    return <div>Loading...</div>;
  }

  // Render the AudioPlayer with the fetched metadata
  return <AudioPlayer metadata={metadata} />;
};

export default PlaybackScreen;