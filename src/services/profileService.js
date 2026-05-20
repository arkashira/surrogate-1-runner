const BASE_URL = process.env.REACT_APP_API_BASE_URL ?? '';

const handleResponse = async (response) => {
  const text = await response.text();
  if (!response.ok) {
    const error = new Error(`API error ${response.status}: ${text}`);
    error.status = response.status;
    throw error;
  }
  // If the body is empty (204) return null
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    return text; // fallback to raw text
  }
};

export const profileService = {
  async saveCompanyProfile(profile) {
    const res = await fetch(`${BASE_URL}/api/company-profile`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(profile),
    });
    return handleResponse(res);
  },

  async getCompanyProfile() {
    const res = await fetch(`${BASE_URL}/api/company-profile`, {
      method: 'GET',
      headers: { Accept: 'application/json' },
    });
    if (res.status === 404) return null;
    return handleResponse(res);
  },
};