import axios from 'axios';

const BASE_URL = "http://localhost:8090";

// ==================== AUTH ====================
export const signupUser = (data) =>
  axios.post(`${BASE_URL}/auth/registration/`, data);

export const loginUser = (data) =>
  axios.post(`${BASE_URL}/auth/jwt/login/`, data);

// ==================== PROFILE ====================
export const completeProfile = (data, token) =>
  axios.post(`${BASE_URL}/api/profile/complete/`, data, {
    headers: { Authorization: `Bearer ${token}` },
  });

// ==================== APPOINTMENTS ====================
export const addAppointment = async (data, token = null) => {
  try {
    const res = await axios.post(`${BASE_URL}/api/appointments/book/`, data, {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
      },
    });

    return { success: true, appointment: res.data };
  } catch (err) {
    console.error('Appointment booking error:', err.response || err.message);
    
    const message = err.response?.data
      ? JSON.stringify(err.response.data)
      : 'Network error. Please try again.';
      
    return { success: false, error: message };
  }
};

export const fetchAppointments = async (token = null) => {
  try {
    const res = await axios.get(`${BASE_URL}/api/appointments/`, {
      headers: {
        ...(token && { Authorization: `Bearer ${token}` }),
      },
    });
    return { success: true, appointments: res.data };
  } catch (err) {
    console.error('Fetching appointments error:', err.response || err.message);
    
    const message = err.response?.data
      ? JSON.stringify(err.response.data)
      : 'Network error. Please try again.';
      
    return { success: false, error: message };
  }
};

export const cancelAppointment = async (appointmentId, token = null) => {
  try {
    const res = await axios.post(
      `${BASE_URL}/api/appointments/cancel/${appointmentId}/`,
      {},
      {
        headers: {
          ...(token && { Authorization: `Bearer ${token}` }),
        },
      }
    );
    return { success: true, data: res.data };
  } catch (err) {
    console.error('Cancel appointment error:', err.response || err.message);
    return { success: false, error: err.response?.data || err.message };
  }
};

// ==================== HOSPITALS/PROVIDERS ====================
export const searchHospitals = async (lat, lon, query = "hospital") => {
  try {
    const res = await axios.get(
      `${BASE_URL}/api/hospitals/search/`,
      {
        params: { lat, lon, query },
      }
    );
    return { success: true, hospitals: res.data };
  } catch (err) {
    console.error('Hospital search error:', err.response || err.message);
    return { success: false, error: err.response?.data || err.message };
  }
};

// ==================== SYMPTOM CHECKER ====================
export const checkSymptoms = async (symptoms) => {
  try {
    const res = await axios.post(`${BASE_URL}/api/symptoms/check/`, {
      symptoms: symptoms,
    });
    return { success: true, diagnosis: res.data };
  } catch (err) {
    console.error('Symptom check error:', err.response || err.message);
    
    const message = err.response?.data?.error || 
                    err.response?.data ||
                    'Failed to analyze symptoms. Please try again.';
    
    return { success: false, error: message };
  }
};

// ==================== PRESCRIPTION READER ====================
export const uploadPrescription = async (file) => {
  try {
    const formData = new FormData();
    formData.append('file', file);

    const res = await axios.post(
      `${BASE_URL}/api/upload-prescription/`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return { success: true, medicines: res.data };
  } catch (err) {
    console.error('Prescription upload error:', err.response || err.message);
    
    const message = err.response?.data?.error || 
                    err.response?.data ||
                    'Failed to process prescription. Please try again.';
    
    return { success: false, error: message };
  }
};

// ==================== REMINDERS ====================
export const listReminders = async (token = null) => {
  try {
    const res = await axios.get(`${BASE_URL}/api/reminders/list/`, {
      headers: {
        ...(token && { Authorization: `Bearer ${token}` }),
      },
    });
    return { success: true, reminders: res.data };
  } catch (err) {
    console.error('Fetch reminders error:', err.response || err.message);
    return { success: false, error: err.response?.data || err.message };
  }
};

export const createPrescriptionReminders = async () => {
  try {
    const res = await axios.post(
      `${BASE_URL}/api/prescription/reminders/create/`
    );
    return { success: true, reminders: res.data };
  } catch (err) {
    console.error('Create reminders error:', err.response || err.message);
    return { success: false, error: err.response?.data || err.message };
  }
};

// ==================== FORUM ====================
export const fetchPosts = async () => {
  try {
    const res = await axios.get(`${BASE_URL}/api/forum/posts/`);
    return { success: true, posts: res.data };
  } catch (err) {
    console.error('Fetch posts error:', err.response || err.message);
    return { success: false, error: err.response?.data || err.message };
  }
};

export const createPost = async (postData) => {
  try {
    const res = await axios.post(`${BASE_URL}/api/forum/posts/`, postData);
    return { success: true, post: res.data };
  } catch (err) {
    console.error('Create post error:', err.response || err.message);
    return { success: false, error: err.response?.data || err.message };
  }
};

export const fetchPostDetail = async (postId) => {
  try {
    const res = await axios.get(`${BASE_URL}/api/forum/posts/${postId}/`);
    return { success: true, post: res.data };
  } catch (err) {
    console.error('Fetch post detail error:', err.response || err.message);
    return { success: false, error: err.response?.data || err.message };
  }
};

export const addComment = async (postId, commentData) => {
  try {
    const res = await axios.post(
      `${BASE_URL}/api/forum/posts/${postId}/`,
      commentData
    );
    return { success: true, comment: res.data };
  } catch (err) {
    console.error('Add comment error:', err.response || err.message);
    return { success: false, error: err.response?.data || err.message };
  }
};

export const votePost = async (postId, action) => {
  try {
    const res = await axios.post(
      `${BASE_URL}/api/forum/posts/${postId}/${action}/`
    );
    return { success: true, result: res.data };
  } catch (err) {
    console.error('Vote post error:', err.response || err.message);
    return { success: false, error: err.response?.data || err.message };
  }
};
