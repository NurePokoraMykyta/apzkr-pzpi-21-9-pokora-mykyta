import React, { useState } from 'react';
import { Modal, Box, Typography, TextField, Button, IconButton, Alert } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import { useAuth } from '../contexts/AuthContext';
import { useTranslation } from 'react-i18next';

const modalStyle = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    boxShadow: 24,
    p: 4,
    borderRadius: 2,
};

export const LoginModal = ({ open, onClose, onSwitchToRegister }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { login, error, setError } = useAuth();
    const { t } = useTranslation();

    const handleSubmit = async (e) => {
        e.preventDefault();
        await login(email, password);
        if (!error) onClose();
    };

    return (
        <Modal open={open} onClose={onClose}>
            <Box sx={modalStyle}>
                <IconButton
                    aria-label="close"
                    onClick={onClose}
                    sx={{
                        position: 'absolute',
                        right: 8,
                        top: 8,
                    }}
                >
                    <CloseIcon />
                </IconButton>
                <Typography variant="h6" component="h2" gutterBottom>
                    {t('login')}
                </Typography>
                {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
                <form onSubmit={handleSubmit}>
                    <TextField
                        fullWidth
                        label={t('email')}
                        variant="outlined"
                        margin="normal"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                    <TextField
                        fullWidth
                        label={t('password')}
                        type="password"
                        variant="outlined"
                        margin="normal"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        color="primary"
                        sx={{ mt: 2 }}
                    >
                        {t('login')}
                    </Button>
                </form>
                <Button
                    onClick={() => {
                        setError(null);
                        onSwitchToRegister();
                    }}
                    fullWidth
                    sx={{ mt: 2 }}
                >
                    {t('noAccount')}
                </Button>
            </Box>
        </Modal>
    );
};

export const RegisterModal = ({ open, onClose, onSwitchToLogin }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [displayName, setDisplayName] = useState('');
    const { register, error, setError } = useAuth();
    const { t } = useTranslation();

    const handleSubmit = async (e) => {
        e.preventDefault();
        await register(email, password, displayName);
        if (!error) onClose();
    };

    return (
        <Modal open={open} onClose={onClose}>
            <Box sx={modalStyle}>
                <IconButton
                    aria-label="close"
                    onClick={onClose}
                    sx={{
                        position: 'absolute',
                        right: 8,
                        top: 8,
                    }}
                >
                    <CloseIcon />
                </IconButton>
                <Typography variant="h6" component="h2" gutterBottom>
                    {t('register')}
                </Typography>
                {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
                <form onSubmit={handleSubmit}>
                    <TextField
                        fullWidth
                        label={t('email')}
                        variant="outlined"
                        margin="normal"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                    />
                    <TextField
                        fullWidth
                        label={t('password')}
                        type="password"
                        variant="outlined"
                        margin="normal"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                    <TextField
                        fullWidth
                        label={t('displayName')}
                        variant="outlined"
                        margin="normal"
                        value={displayName}
                        onChange={(e) => setDisplayName(e.target.value)}
                    />
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        color="primary"
                        sx={{ mt: 2 }}
                    >
                        {t('register')}
                    </Button>
                </form>
                <Button
                    onClick={() => {
                        setError(null);
                        onSwitchToLogin();
                    }}
                    fullWidth
                    sx={{ mt: 2 }}
                >
                    {t('haveAccount')}
                </Button>
            </Box>
        </Modal>
    );
};