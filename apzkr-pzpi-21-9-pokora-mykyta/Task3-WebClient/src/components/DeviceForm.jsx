import React, { useState, useEffect } from 'react';
import { TextField, Button, Dialog, DialogActions, DialogContent, DialogTitle, MenuItem } from '@mui/material';
import { useTranslation } from 'react-i18next';

const DeviceForm = ({ open, onClose, onSubmit, device, aquariums }) => {
    const { t } = useTranslation();
    const [formData, setFormData] = useState({
        unique_address: '',
        aquarium_id: ''
    });

    useEffect(() => {
        if (device) {
            setFormData({
                unique_address: device.unique_address,
                aquarium_id: device.aquarium_id
            });
        } else {
            setFormData({
                unique_address: '',
                aquarium_id: ''
            });
        }
    }, [device]);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = () => {
        onSubmit(formData);
        onClose();
    };

    return (
        <Dialog open={open} onClose={onClose}>
            <DialogTitle>{device ? t('editDevice') : t('addDevice')}</DialogTitle>
            <DialogContent>
                <TextField
                    autoFocus
                    margin="dense"
                    name="unique_address"
                    label={t('uniqueAddress')}
                    type="text"
                    fullWidth
                    value={formData.unique_address}
                    onChange={handleChange}
                />
                <TextField
                    select
                    margin="dense"
                    name="aquarium_id"
                    label={t('aquarium')}
                    fullWidth
                    value={formData.aquarium_id}
                    onChange={handleChange}
                >
                    {aquariums.map((aquarium) => (
                        <MenuItem key={aquarium.id} value={aquarium.id}>
                            {aquarium.name}
                        </MenuItem>
                    ))}
                </TextField>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>{t('cancel')}</Button>
                <Button onClick={handleSubmit} color="primary">{t('submit')}</Button>
            </DialogActions>
        </Dialog>
    );
};

export default DeviceForm;