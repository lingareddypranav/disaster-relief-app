// frontend/src/services/apiService.js
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/';

export const getHurricanes = () => axios.get(`${API_URL}hurricanes/`);
export const getVehicles = () => axios.get(`${API_URL}vehicles/`);
export const getResourceNeeds = () => axios.get(`${API_URL}resource-needs/`);

// Function to dispatch resources
export const dispatchResources = (adjustedNeeds) => {
  return axios.post(`${API_URL}dispatch-resources/`, adjustedNeeds);
};
