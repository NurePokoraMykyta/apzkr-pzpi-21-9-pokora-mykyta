import React, { useState } from 'react';
import { TextField, Button, Box, Typography } from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import { companyApi } from '../api';

const CreateCompanyForm = ({ onSuccess }) => {
    const [name, setName] = useState('');
    const [description, setDescription] = useState('');
    const [error, setError] = useState('');
    const { setSuccessMessage } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await companyApi.createCompany({ name, description });
            setSuccessMessage('Компания успешно создана');
            onSuccess();
        } catch (error) {
            setError(error.response?.data?.detail);
        }
    };

    return (
        <Box component="form" onSubmit={handleSubmit} sx={{ p: 3, maxWidth: 400 }}>
            {error && (
                <Typography color="error" sx={{ mb: 2 }}>
                    {error}
                </Typography>
            )}
            <TextField
                fullWidth
                label="Назва компанії"
                value={name}
                onChange={(e) => setName(e.target.value)}
                margin="normal"
                required
            />
            <TextField
                fullWidth
                label="Опис"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                margin="normal"
                multiline
                rows={3}
            />
            <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }}>
                Створити компанії
            </Button>
        </Box>
    );
};

export default CreateCompanyForm;