import axios from 'axios';

/**
 * Fetches metadata for a given stream URL
 * @param {string} streamUrl - The URL of the stream to fetch metadata from
 * @returns {Promise<Object>} - Promise resolving to stream metadata object
 */
export async function fetchStreamMetadata(streamUrl) {
  try {
    // In a real implementation, this would make an HTTP request to fetch
    // stream metadata from the source. For now, we simulate with mock data.
    const response = await axios.get(`${streamUrl}/metadata`);
    return response.data;
  } catch (error) {
    console.error('Failed to fetch stream metadata:', error);
    // Return default fallback values in case of failure
    return {
      title: 'Unknown Program',
      description: 'No description available'
    };
  }
}

/**
 * Gets program title and description for a recording
 * @param {Object} recording - Recording object containing stream information
 * @returns {Promise<Object>} - Promise resolving to program metadata
 */
export async function getProgramMetadata(recording) {
  if (!recording || !recording.streamUrl) {
    return {
      title: 'Unknown Program',
      description: 'No description available'
    };
  }

  try {
    const metadata = await fetchStreamMetadata(recording.streamUrl);
    return {
      title: metadata.title || 'Unknown Program',
      description: metadata.description || 'No description available'
    };
  } catch (error) {
    console.error('Error getting program metadata:', error);
    return {
      title: 'Unknown Program',
      description: 'No description available'
    };
  }
}