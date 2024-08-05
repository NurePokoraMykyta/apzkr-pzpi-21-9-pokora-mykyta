// src/components/FishForm.jsx
import React, { useState, useEffect } from 'react';
import {
    TextField,
    Button,
    Box,
    Typography
} from '@mui/material';
import { useTranslation } from 'react-i18next';

const FishForm = ({ onSubmit, initialData = {}, aquariumCapacity }) => {
    const { t } = useTranslation();
    const [species, setSpecies] = useState(initialData.species || '');
    const [quantity, setQuantity] = useState(initialData.quantity || '');
    const [error, setError] = useState('');

    useEffect(() => {
        setSpecies(initialData.species || '');
        setQuantity(initialData.quantity || '');
    }, [initialData]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!species.trim()) {
            setError(t('speciesRequired'));
            return;
        }
        if (quantity <= 0) {
            setError(t('quantityMustBePositive'));
            return;
        }
        if (aquariumCapacity && quantity > aquariumCapacity) {
            setError(t('quantityExceedsCapacity'));
            return;
        }
        onSubmit({ species, quantity: Number(quantity) });
    };

    return (
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
            <Typography variant="h6" gutterBottom>
                {initialData.id ? t('editFish') : t('addFish')}
            </Typography>

            <TextField
                fullWidth
                label={t('fishSpecies')}
                value={species}
                onChange={(e) => setSpecies(e.target.value)}
                margin="normal"
                required
            />

            <TextField
                fullWidth
                label={t('quantity')}
                type="number"
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
                margin="normal"
                required
                inputProps={{ min: 1 }}
            />

            {error && (
                <Typography color="error" sx={{ mt: 1 }}>
                    {error}
                </Typography>
            )}

            <Button
                type="submit"
                variant="contained"
                color="primary"
                sx={{ mt: 2 }}
            >
                {initialData.id ? t('update') : t('add')}
            </Button>
        </Box>
    );
};

export default FishForm;