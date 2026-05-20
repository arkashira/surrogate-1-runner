import axios from "axios";

/**
 * Fetch all versions for a given summary.
 * @param {string} summaryId
 * @returns {Promise<Array>} array of version objects
 */
export const getSummaryVersions = async (summaryId) => {
  const { data } = await axios.get(`/api/summaries/${summaryId}/versions`);
  return data;
};

/**
 * Restore a specific version.
 * @param {string} summaryId
 * @param {string} versionId
 * @returns {Promise<void>}
 */
export const restoreSummaryVersion = async (summaryId, versionId) => {
  await axios.put(
    `/api/summaries/${summaryId}/versions/${versionId}/restore`
  );
};