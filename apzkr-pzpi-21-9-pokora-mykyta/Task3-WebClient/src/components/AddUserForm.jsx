import React, { useState } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, TextField, Button, Select, MenuItem } from '@mui/material';
import { useTranslation } from 'react-i18next';

const AddUserDialog = ({ open, onClose, onAddUser, roles }) => {
    const { t } = useTranslation();
    const [email, setEmail] = useState('');
    const [roleId, setRoleId] = useState('');

    const handleSubmit = () => {
        onAddUser(email, roleId);
        setEmail('');
        setRoleId('');
    };

    return (
        <Dialog open={open} onClose={onClose}>
            <DialogTitle>{t('addUserToCompany')}</DialogTitle>
            <DialogContent>
                <TextField
                    autoFocus
                    margin="dense"
                    label={t('email')}
                    type="email"
                    fullWidth
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                />
                <Select
                    fullWidth
                    value={roleId}
                    onChange={(e) => setRoleId(e.target.value)}
                    sx={{ mt: 2 }}
                    displayEmpty
                >
                    <MenuItem value="" disabled>{t('selectRole')}</MenuItem>
                    {roles.map((role) => (
                        <MenuItem key={role.id} value={role.id}>{role.name}</MenuItem>
                    ))}
                </Select>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>{t('cancel')}</Button>
                <Button onClick={handleSubmit} color="primary" disabled={!email || !roleId}>
                    {t('add')}
                </Button>
            </DialogActions>
        </Dialog>
    );
};

export default AddUserDialog;