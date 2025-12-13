import axios from 'axios';

const API_BASE_URL = 'http://localhost:8080/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Health checks
export const checkHealth = async (service) => {
  const endpoints = {
    fhir: '/fhir/health',
    deid: '/deid/health',
    features: '/features/health',
    predictions: '/predictions/health',
  };
  const response = await api.get(endpoints[service]);
  return response.data;
};

// Features API
export const getFeatures = async () => {
  const response = await api.get('/features/features');
  return response.data;
};

export const getFeatureStats = async () => {
  const response = await api.get('/features/stats');
  return response.data;
};

export const extractFeatures = async () => {
  const response = await api.post('/features/extract/all');
  return response.data;
};

// Predictions API
export const getPredictions = async () => {
  const response = await api.get('/predictions/predictions');
  return response.data;
};

export const getPredictionStats = async () => {
  const response = await api.get('/predictions/stats');
  return response.data;
};

export const getHighRiskPatients = async () => {
  const response = await api.get('/predictions/high-risk');
  return response.data;
};

export const predictRisks = async () => {
  const response = await api.post('/predictions/predict/all');
  return response.data;
};

// Get patient details
export const getPatientFeatures = async (patientId) => {
  const response = await api.get(`/features/features/${patientId}`);
  return response.data;
};

export const getPatientPrediction = async (patientId) => {
  const response = await api.get(`/predictions/risk/${patientId}`);
  return response.data;
};

export default api;
