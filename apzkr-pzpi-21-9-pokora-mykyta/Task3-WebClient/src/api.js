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

export default api;