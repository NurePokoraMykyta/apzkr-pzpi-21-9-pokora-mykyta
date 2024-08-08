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
    if (!config.url.startsWith('/auth/') || config.url === '/auth/logout' || config.url === '/auth/me') {
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
    getCurrentUser: () => api.get('/auth/me'),
    updateProfile: (userData) => api.put('/auth/me', userData),
    deleteAccount: () => api.delete('/auth/me'),
};

export const rolesApi = {
    createRole: (roleData) => api.post('/roles', roleData),
    getCompanyRoles: (companyId) => api.get(`/roles/company/${companyId}`),
    getCompanyRole: (companyId, roleId) => api.get(`/roles/company/${companyId}/role/${roleId}`),
    updateRole: (roleId, roleData, companyId) => api.put(`/roles/company/${companyId}/role/${roleId}`, roleData),
    assignRole: (roleId, userId, companyId) => api.post(`/roles/${roleId}/assign?user_id=${userId}&company_id=${companyId}`),
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
    updateFish: (aquariumId, fishId, fishData, companyId) => api.put(`/aquariums/${aquariumId}/fish/${fishId}`, {
        fish_data: {
            species: fishData.species,
            quantity: fishData.quantity
        },
        company_id: companyId
    }),
    removeFish: (aquariumId, fishId, companyId, quantity = null) =>
        api.delete(`/aquariums/${aquariumId}/fish/${fishId}`, {
            params: {
                company_id: companyId,
                ...(quantity !== null && { quantity })
            }
        }),
    getFish: (aquariumId) => api.get(`/aquariums/${aquariumId}/fish`),
    getCompanyUsers: (companyId) => api.get(`/companies/${companyId}/users`),
};

export const deviceApi = {
    setupDevice: (aquariumId, deviceData) => api.post(`/devices/${aquariumId}`, deviceData),
    getDevice: (aquariumId) => api.get(`/devices/${aquariumId}`),
    updateDevice: (aquariumId, deviceData) => api.put(`/devices/${aquariumId}`, deviceData),
    activateDevice: (aquariumId) => api.post(`/devices/${aquariumId}/activate`),
    deactivateDevice: (aquariumId) => api.post(`/devices/${aquariumId}/deactivate`),
    fillFoodPatch: (aquariumId, foodPatchData) => api.post(`/devices/${aquariumId}/food-patch`, foodPatchData),
    deleteFoodPatch: (aquariumId) => api.delete(`/devices/${aquariumId}/food-patch`),
};

export const feedingScheduleApi = {
    getAquariumFeedingSchedules: (aquariumId) => api.get(`/aquariums/${aquariumId}/feeding-schedules`),
    addFeedingSchedule: (aquariumId, scheduleData) => api.post(`/aquariums/${aquariumId}/feeding-schedules`, scheduleData),
    getFeedingSchedule: (scheduleId) => api.get(`/feeding-schedules/${scheduleId}`),
    updateFeedingSchedule: (scheduleId, scheduleData) => api.put(`/feeding-schedules/${scheduleId}`, scheduleData),
    deleteFeedingSchedule: (scheduleId) => api.delete(`/feeding-schedules/${scheduleId}`),
};

export default api;