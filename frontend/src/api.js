/**
 * API service for communicating with the backend Flask application
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Default headers for authentication
const getDefaultHeaders = () => ({
  'Content-Type': 'application/json',
  'X-User-ID': 'admin-user-id', // Default user ID - customize based on your auth system
  'X-User-Role': 'admin', // Default role - customize based on your auth system
});

/**
 * Create a full interview workflow (JD Enhancement + Interview Generation)
 * @param {Object} formData - Form data with job description and WORK methodology inputs
 * @returns {Promise} API response
 */
export const createInterview = async (formData) => {
  const response = await fetch(`${API_BASE_URL}/api/interview/workflow/full`, {
    method: 'POST',
    headers: getDefaultHeaders(),
    body: JSON.stringify({
      req_id: formData.req_id,
      basic_title: formData.basic_title,
      basic_description: formData.basic_description,
      basic_department: formData.basic_department || '',
      basic_level: formData.basic_level || '',
      work_output: formData.work_output || '',
      work_role: formData.work_role || '',
      work_knowledge: formData.work_knowledge || '',
      work_competencies: formData.work_competencies || '',
      interview_name: formData.interview_name || `${formData.basic_title} Interview`,
    }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || `HTTP error! status: ${response.status}`);
  }

  return response.json();
};

/**
 * Get interview by ID
 * @param {number} interviewId - Interview ID
 * @returns {Promise} API response
 */
export const getInterview = async (interviewId) => {
  const response = await fetch(`${API_BASE_URL}/api/interview/${interviewId}`, {
    method: 'GET',
    headers: getDefaultHeaders(),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || `HTTP error! status: ${response.status}`);
  }

  return response.json();
};

/**
 * Health check
 * @returns {Promise} API response
 */
export const healthCheck = async () => {
  const response = await fetch(`${API_BASE_URL}/health`, {
    method: 'GET',
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
};