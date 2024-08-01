import React, { createContext, useState, useContext } from 'react';
import { authApi } from '../api';


const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [error, setError] = useState(null);

    const login = async (email, password) => {
        try {
            const response = await authApi.login({ email, password });
            setUser(response.data);
            setError(null);
        } catch (err) {
            setError(err.response?.data?.detail);
        }
    };

    const register = async (email, password, displayName) => {
        try {
            const response = await authApi.register({ email, password, display_name: displayName });
            setUser(response.data);
            setError(null);
        } catch (err) {
            setError(err.response?.data?.detail);
        }
    };

    const logout = async () => {
        try {
            await authApi.logout();
            setUser(null);
            setError(null);
        } catch (err) {
            setError(err.response?.data?.detail);
        }
    };

    return (
        <AuthContext.Provider value={{ user, error, login, register, logout, setError }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);