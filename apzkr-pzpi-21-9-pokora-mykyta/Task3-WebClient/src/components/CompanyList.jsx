import React, { useState, useEffect } from 'react';
import { List, ListItem, ListItemText, Typography, CircularProgress, Box } from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import { useCompany } from '../contexts/CompanyContext';
import { companyApi } from '../api';

const CompanyList = ({ onClose }) => {
    const { user } = useAuth();
    const { setSelectedCompany } = useCompany();
    const [companies, setCompanies] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchCompanies = async () => {
            try {
                const response = await companyApi.getUserCompanies();
                setCompanies(response.data);
            } catch (error) {
                console.error('Error fetching companies:', error);
            } finally {
                setLoading(false);
            }
        };

        if (user) {
            fetchCompanies();
        }
    }, [user]);

    const handleCompanySelect = (company) => {
        setSelectedCompany(company);
        onClose();
    };

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" height="200px">
                <CircularProgress />
            </Box>
        );
    }

    if (companies.length === 0) {
        return (
            <Typography variant="body1" textAlign="center" py={2}>
                У вас пока нет компаний
            </Typography>
        );
    }

    return (
        <List>
            {companies.map((company) => (
                <ListItem key={company.id} button onClick={() => handleCompanySelect(company)}>
                    <ListItemText
                        primary={company.name}
                        secondary={company.description || 'Без описания'}
                    />
                </ListItem>
            ))}
        </List>
    );
};

export default CompanyList;