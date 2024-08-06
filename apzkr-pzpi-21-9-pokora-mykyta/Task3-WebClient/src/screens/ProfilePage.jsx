import React, { useState, useEffect } from 'react';
import {
    Container,
    Typography,
    TextField,
    Button,
    Grid,
    Paper,
    Box,
    Divider,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    Snackbar,
    Alert,
    CircularProgress
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import { useAuth } from '../contexts/AuthContext';
import { authApi } from '../api';

const ProfilePage = () => {
    const { t } = useTranslation();
    const { user, logout } = useAuth();
    const [profileData, setProfileData] = useState({
        id: '',
        display_name: '',
        email: '',
        phone_number: '',
        status: '',
        created_at: '',
        updated_at: ''
    });
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [openDeleteDialog, setOpenDeleteDialog] = useState(false);

    useEffect(() => {
        fetchUserData();
    }, []);

    const fetchUserData = async () => {
        try {
            const response = await authApi.getCurrentUser();
            setProfileData({
                id: response.data.id,
                display_name: response.data.display_name,
                email: response.data.email || '',
                phone_number: response.data.phone_number || '',
                status: response.data.status,
                created_at: response.data.created_at,
                updated_at: response.data.updated_at
            });
        } catch (err) {
            setError(t('errorFetchingProfile'));
        } finally {
            setIsLoading(false);
        }
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setProfileData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await authApi.updateProfile(profileData);
            setSuccess(t('profileUpdateSuccess'));
            fetchUserData();
        } catch (err) {
            setError(t('profileUpdateError'));
        }
    };

    const handleDeleteAccount = async () => {
        try {
            await authApi.deleteAccount();
            logout();
            // Потім додам редірект на головну сторінку
        } catch (err) {
            setError(t('accountDeleteError'));
        } finally {
            setOpenDeleteDialog(false);
        }
    };

    if (isLoading) {
        return (
            <Container sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
                <CircularProgress />
            </Container>
        );
    }

    return (
        <Container component="main" maxWidth="md" sx={{ mt: 4, mb: 4 }}>
            <Paper elevation={3} sx={{ p: 4 }}>
                <Grid container spacing={4}>
                    <Grid item xs={12} md={6}>
                        <Typography variant="h5" gutterBottom>
                            {t('profile')}
                        </Typography>
                        <form onSubmit={handleSubmit}>
                            <TextField
                                fullWidth
                                margin="normal"
                                label={t('displayName')}
                                name="display_name"
                                value={profileData.display_name}
                                onChange={handleInputChange}
                            />
                            <TextField
                                fullWidth
                                margin="normal"
                                label={t('email')}
                                name="email"
                                value={profileData.email}
                                onChange={handleInputChange}
                                type="email"
                            />
                            <TextField
                                fullWidth
                                margin="normal"
                                label={t('phoneNumber')}
                                name="phone_number"
                                value={profileData.phone_number}
                                onChange={handleInputChange}
                            />
                            <Button
                                type="submit"
                                variant="contained"
                                color="primary"
                                sx={{ mt: 2 }}
                            >
                                {t('updateProfile')}
                            </Button>
                        </form>
                    </Grid>

                    <Grid item xs={12} md={6} sx={{ display: 'flex', flexDirection: 'column' }}>
                        <Box sx={{ pl: { md: 4 }, borderLeft: { md: 1 }, borderColor: 'divider', height: '100%' }}>
                            <Typography variant="h5" gutterBottom>
                                {t('accountInfo')}
                            </Typography>
                            <Box sx={{ mt: 2 }}>
                                <Typography variant="body1" gutterBottom>
                                    <strong>{t('id')}:</strong> {profileData?.id}
                                </Typography>
                                <Typography variant="body1" gutterBottom>
                                    <strong>{t('email')}:</strong> {profileData?.email}
                                </Typography>
                                <Typography variant="body1" gutterBottom>
                                    <strong>{t('status')}:</strong> {profileData?.status}
                                </Typography>
                                <Typography variant="body1" gutterBottom>
                                    <strong>{t('createdAt')}:</strong> {new Date(profileData?.created_at).toLocaleString()}
                                </Typography>
                                {user?.updated_at && (
                                    <Typography variant="body1" gutterBottom>
                                        <strong>{t('lastUpdated')}:</strong> {new Date(profileData.updated_at).toLocaleString()}
                                    </Typography>
                                )}
                            </Box>
                            <Button
                                variant="outlined"
                                color="error"
                                sx={{ mt: 4 }}
                                onClick={() => setOpenDeleteDialog(true)}
                            >
                                {t('deleteAccount')}
                            </Button>
                        </Box>
                    </Grid>
                </Grid>
            </Paper>

            <Dialog
                open={openDeleteDialog}
                onClose={() => setOpenDeleteDialog(false)}
            >
                <DialogTitle>{t('deleteAccount')}</DialogTitle>
                <DialogContent>
                    <DialogContentText>
                        {t('deleteAccountConfirmation')}
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setOpenDeleteDialog(false)}>{t('cancel')}</Button>
                    <Button onClick={handleDeleteAccount} color="error">
                        {t('confirm')}
                    </Button>
                </DialogActions>
            </Dialog>

            <Snackbar
                open={!!error || !!success}
                autoHideDuration={6000}
                onClose={() => {
                    setError('');
                    setSuccess('');
                }}
            >
                <Alert
                    onClose={() => {
                        setError('');
                        setSuccess('');
                    }}
                    severity={error ? "error" : "success"}
                    sx={{ width: '100%' }}
                >
                    {error || success}
                </Alert>
            </Snackbar>
        </Container>
    );
};

export default ProfilePage;