import React, { createContext, useState, useContext, useEffect } from 'react';
import { authApi } from '../api';
import { useTranslation } from "react-i18next";
import {jwtDecode} from 'jwt-decode';
import {useNavigate} from "react-router-dom";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [error, setError] = useState(null);
    const [successMessage, setSuccessMessage] = useState(null);
    const { t } = useTranslation();
    const navigator = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        if (token) {
            if (isTokenExpired(token)) {
                handleLogout();
            } else {
                setUser({ token });
            }
        }

        const handleLogoutEvent = () => {
            handleLogout();
        };

        window.addEventListener('logout', handleLogoutEvent);

        return () => {
            window.removeEventListener('logout', handleLogoutEvent);
        };
    }, []);

    const isTokenExpired = (token) => {
        try {
            const decoded = jwtDecode(token);
            return decoded.exp < Date.now() / 1000;
        } catch (e) {
            return true;
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('token_type');
        setUser(null);
        setError(null);
        window.dispatchEvent(new CustomEvent('userLoggedOut'));
        navigator('/');
    };

    const login = async (email, password) => {
        try {
            const response = await authApi.login({ email, password });
            const { access_token, token_type } = response.data;
            localStorage.setItem('access_token', access_token);
            localStorage.setItem('token_type', token_type);
            setUser({ token: access_token });
            setError(null);
            return true;
        } catch (err) {
            setError(err.response?.data?.detail);
            return false;
        }
    };

    const register = async (email, password, displayName) => {
        try {
            await authApi.register({ email, password, display_name: displayName });
            setSuccessMessage(t('registrationSuccess'));
            setError(null);
            return true;
        } catch (err) {
            setError(err.response?.data?.detail);
            return false;
        }
    };

    const logout = async () => {
        try {
            await authApi.logout();
        } catch (err) {
            console.error(err);
        } finally {
            handleLogout();
        }
    };

    return (
        <AuthContext.Provider value={{ user, error, successMessage, login, register, logout, setError, setSuccessMessage }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);