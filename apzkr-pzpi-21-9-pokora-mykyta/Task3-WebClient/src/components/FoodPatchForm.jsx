import React, { useState, useEffect } from 'react';
import { TextField, Button, Dialog, DialogActions, DialogContent, DialogTitle } from '@mui/material';
import { useTranslation } from 'react-i18next';

const FoodPatchForm = ({ open, onClose, onSubmit, onDelete, currentFoodPatch }) => {
    const { t } = useTranslation();
    const [formData, setFormData] = useState({
        name: '',
        food_type: '',
        quantity: 1
    });

    useEffect(() => {
        if (currentFoodPatch) {
            setFormData(currentFoodPatch);
        } else {
            setFormData({ name: '', food_type: '', quantity: 1 });
        }
    }, [currentFoodPatch]);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = () => {
        onSubmit(formData);
    };

    return (
        <Dialog open={open} onClose={onClose}>
            <DialogTitle>{currentFoodPatch ? t('editFoodPatch') : t('addFoodPatch')}</DialogTitle>
            <DialogContent>
                <TextField
                    autoFocus
                    margin="dense"
                    name="name"
                    label={t('name')}
                    type="text"
                    fullWidth
                    value={formData.name}
                    onChange={handleChange}
                />
                <TextField
                    margin="dense"
                    name="food_type"
                    label={t('foodType')}
                    type="text"
                    fullWidth
                    value={formData.food_type}
                    onChange={handleChange}
                />
                <TextField
                    margin="dense"
                    name="quantity"
                    label={t('quantity')}
                    type="number"
                    fullWidth
                    value={formData.quantity}
                    onChange={handleChange}
                />
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>{t('cancel')}</Button>
                {currentFoodPatch && (
                    <Button onClick={onDelete} color="error">
                        {t('delete')}
                    </Button>
                )}
                <Button onClick={handleSubmit} color="primary">
                    {t('submit')}
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default FoodPatchForm;