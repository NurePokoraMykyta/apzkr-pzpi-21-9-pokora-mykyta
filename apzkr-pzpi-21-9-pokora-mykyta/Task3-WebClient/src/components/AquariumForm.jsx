// src/components/AquariumForm.jsx
import React, { useState } from 'react';
import { TextField, Button, Box } from '@mui/material';
import { useTranslation } from 'react-i18next';

const AquariumForm = ({ onSubmit, initialData}) => {
    const initialValues = initialData || {};
    const [name, setName] = useState(initialValues.name || '');
    const [capacity, setCapacity] = useState(initialValues.capacity || '');
    const [description, setDescription] = useState(initialValues.description || '');
    const { t } = useTranslation();

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({ name, capacity: Number(capacity), description });
    };

    return (
        <Box component="form" onSubmit={handleSubmit}>
            <TextField
                fullWidth
                label={t('aquariumName')}
                value={name}
                onChange={(e) => setName(e.target.value)}
                margin="normal"
                required
            />
            <TextField
                fullWidth
                label={t('capacity')}
                type="number"
                value={capacity}
                onChange={(e) => setCapacity(e.target.value)}
                margin="normal"
                required
            />
            <TextField
                fullWidth
                label={t('description')}
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                margin="normal"
                multiline
                rows={3}
            />
            <Button type="submit" variant="contained" color="primary">
                {initialData.id ? t('update') : t('create')}
            </Button>
        </Box>
    );
};

export default AquariumForm;