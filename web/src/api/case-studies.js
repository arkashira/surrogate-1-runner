import axios from 'axios';

const API_URL = '/api/case-studies';

export const submitCaseStudy = async (caseStudyData) => {
  try {
    const response = await axios.post(API_URL, caseStudyData);
    return response.data;
  } catch (error) {
    throw new Error('Failed to submit case study');
  }
};