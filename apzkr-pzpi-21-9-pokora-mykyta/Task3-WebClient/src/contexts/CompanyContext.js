import React, {createContext, useState, useContext, useEffect, useCallback} from 'react';
import { useAuth } from './AuthContext';

const CompanyContext = createContext();

export const CompanyProvider = ({ children }) => {
    const [selectedCompany, setSelectedCompany] = useState(() => {
        const storedCompany = localStorage.getItem('selectedCompany');
        return storedCompany ? JSON.parse(storedCompany) : null;
    });
    const { user } = useAuth();

    useEffect(() => {
        if (selectedCompany) {
            localStorage.setItem('selectedCompany', JSON.stringify(selectedCompany));
        } else {
            localStorage.removeItem('selectedCompany');
        }
    }, [selectedCompany]);

    const clearSelectedCompany = useCallback(() => {
        setSelectedCompany(null);
        localStorage.removeItem('selectedCompany');
    }, []);

    useEffect(() => {
        const handleUserLoggedOut = () => {
            clearSelectedCompany();
        };

        window.addEventListener('userLoggedOut', handleUserLoggedOut);
        return () => {
            window.removeEventListener('userLoggedOut', handleUserLoggedOut);
        };
    }, [clearSelectedCompany]);

    const updateSelectedCompany = useCallback((updatedCompany) => {
        setSelectedCompany(prevCompany => ({
            ...prevCompany,
            ...updatedCompany
        }));
    }, []);

    return (
        <CompanyContext.Provider value={{ selectedCompany, setSelectedCompany, clearSelectedCompany, updateSelectedCompany }}>
            {children}
        </CompanyContext.Provider>
    );
};

export const useCompany = () => useContext(CompanyContext);