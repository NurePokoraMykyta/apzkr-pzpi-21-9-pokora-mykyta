import axios from 'axios';
import {jwtDecode} from 'jwt-decode';

const API_URL = 'http://localhost:8000/api';

export const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

const isTokenExpired = (token) => {
    try {
        const decoded = jwtDecode(token);
        return decoded.exp < Date.now() / 1000;
    } catch (e) {
        return true;
    }
};

api.interceptors.request.use((config) => {
    if (!config.url.startsWith('/auth/') || config.url === '/auth/logout') {
        const token = localStorage.getItem('access_token');
        if (token) {
            if (isTokenExpired(token)) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('token_type');
                window.dispatchEvent(new Event('logout'));
                return Promise.reject('Token expired');
            }
            config.headers['Authorization'] = `Bearer ${token}`;
        }
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

export const authApi = {
    register: (userData) => api.post('/auth/register', userData),
    login: (credentials) => api.post('/auth/login', credentials),
    logout: () => api.post('/auth/logout'),
};

export const companyApi = {
    createCompany: (companyData) => api.post('/companies', companyData),
    getUserCompanies: () => api.get('/companies'),
    getCompany: (id) => api.get(`/companies/${id}`),
    updateCompany: (id, companyData) => api.put(`/companies/${id}`, companyData),
    deleteCompany: (id) => api.delete(`/companies/${id}`),
    addUserToCompany: (companyId, email, roleId) =>
        api.post(`/companies/${companyId}/users`, null, { params: { email, role_id: roleId } }),
    removeUserFromCompany: (companyId, email) =>
        api.delete(`/companies/${companyId}/users/${email}`),
    getCompanyAquariums: (companyId) => api.get(`/companies/${companyId}/aquariums`),
    createAquarium: (companyId, aquariumData) => api.post(`/companies/${companyId}/aquariums`, aquariumData),
    updateAquarium: (companyId, aquariumId, aquariumData) => api.put(`/companies/${companyId}/aquariums/${aquariumId}`, aquariumData),
    deleteAquarium: (companyId, aquariumId) => api.delete(`/companies/${companyId}/aquariums/${aquariumId}`),
    feedNow: (aquariumId) => api.post(`/aquariums/${aquariumId}/feed-now`),
    addFish: (aquariumId, fishData) => api.post(`/aquariums/${aquariumId}/fish`, fishData),
    updateFish: (aquariumId, fishId, fishData) => api.put(`/aquariums/${aquariumId}/fish/${fishId}`, fishData),
    removeFish: (aquariumId, fishId, quantity) => api.delete(`/aquariums/${aquariumId}/fish/${fishId}`, { params: { quantity } }),
    getFish: (aquariumId) => api.get(`/aquariums/${aquariumId}/fish`),
};

export default api;