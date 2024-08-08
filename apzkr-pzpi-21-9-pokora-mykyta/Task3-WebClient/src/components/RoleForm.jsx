import React, { useState, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, TextField, Button, Checkbox, FormControlLabel } from '@mui/material';
import { useTranslation } from 'react-i18next';

const RoleForm = ({ open, onClose, onSubmit, role }) => {
    const { t } = useTranslation();
    const [formData, setFormData] = useState({
        name: '',
        description: '',
        permissions: [],
    });

    useEffect(() => {
        if (role) {
            setFormData(role);
        } else {
            setFormData({ name: '', description: '', permissions: [] });
        }
    }, [role]);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handlePermissionChange = (permission) => {
        const newPermissions = formData.permissions.includes(permission)
            ? formData.permissions.filter(p => p !== permission)
            : [...formData.permissions, permission];
        setFormData({ ...formData, permissions: newPermissions });
    };

    const handleSubmit = () => {
        onSubmit(formData);
        onClose();
    };

    const permissions = ['manage_devices', 'view_company', 'manage_aquariums', 'manage_feeders'];

    return (
        <Dialog open={open} onClose={onClose}>
            <DialogTitle>{role ? t('editRole') : t('createRole')}</DialogTitle>
            <DialogContent>
                <TextField
                    autoFocus
                    margin="dense"
                    name="name"
                    label={t('roleName')}
                    type="text"
                    fullWidth
                    value={formData.name}
                    onChange={handleChange}
                />
                <TextField
                    margin="dense"
                    name="description"
                    label={t('roleDescription')}
                    type="text"
                    fullWidth
                    value={formData.description}
                    onChange={handleChange}
                />
                {permissions.map((permission) => (
                    <FormControlLabel
                        key={permission}
                        control={
                            <Checkbox
                                checked={formData.permissions.includes(permission)}
                                onChange={() => handlePermissionChange(permission)}
                                name={permission}
                            />
                        }
                        label={t(permission)}
                    />
                ))}
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>{t('cancel')}</Button>
                <Button onClick={handleSubmit} color="primary">{t('save')}</Button>
            </DialogActions>
        </Dialog>
    );
};

export default RoleForm;