// src/screens/AquariumsPage.jsx
import React, { useState, useEffect } from 'react';
import {
    Container,
    Typography,
    Grid,
    Button,
    Dialog,
    DialogTitle,
    DialogContent,
    Snackbar,
    Alert,
    CircularProgress, Box
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import { useCompany } from '../contexts/CompanyContext';
import AquariumCard from '../components/AquariumCard';
import AquariumForm from '../components/AquariumForm';
import FishForm from '../components/FishForm';
import { companyApi } from '../api';

const AquariumsPage = () => {
    const { t } = useTranslation();
    const { selectedCompany } = useCompany();
    const [aquariums, setAquariums] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isAquariumFormOpen, setIsAquariumFormOpen] = useState(false);
    const [isFishFormOpen, setIsFishFormOpen] = useState(false);
    const [currentAquarium, setCurrentAquarium] = useState(null);
    const [currentFish, setCurrentFish] = useState({});
    const [alert, setAlert] = useState({ open: false, severity: 'success', message: '' });

    useEffect(() => {
        if (selectedCompany) {
            fetchAquariums();
        }
    }, [selectedCompany]);

    const fetchAquariums = async () => {
        setIsLoading(true);
        try {
            const response = await companyApi.getCompanyAquariums(selectedCompany.id);
            setAquariums(response.data);
        } catch (error) {
            showAlert('error', error?.response?.data?.detail || t('errorFetchingAquariums'));
        } finally {
            setIsLoading(false);
        }
    };

    const handleFeedNow = async (aquariumId) => {
        try {
            await companyApi.feedNow(aquariumId);
            showAlert('success', t('feedingSuccessful'));
        } catch (error) {
            showAlert('error',error.response?.data?.detail || t('errorFeeding'));
        }
    };

    const handleAddFish = (aquariumId) => {
        setCurrentAquarium(aquariumId);
        setCurrentFish({});
        setIsFishFormOpen(true);
    };
    const handleEditFish = (aquariumId, fish) => {
        setCurrentAquarium(aquariumId);
        setCurrentFish(fish);
        setIsFishFormOpen(true);
    };

    const handleRemoveFish = async (aquariumId, fishId, quantity = null) => {
        try {
            const response = await companyApi.removeFish(aquariumId, fishId, selectedCompany.id, quantity);
            setAquariums(prevAquariums =>
                prevAquariums.map(aquarium =>
                    aquarium.id === aquariumId
                        ? {
                            ...aquarium,
                            fish: aquarium.fish.map(fish => {
                                if (fish.id === fishId) {
                                    if (quantity === null || quantity >= fish.quantity) {
                                        return null;
                                    } else {
                                        return { ...fish, quantity: fish.quantity - quantity };
                                    }
                                }
                                return fish;
                            }).filter(Boolean)
                        }
                        : aquarium
                )
            );
            showAlert('success', response.data.message);
        } catch (error) {
            showAlert('error', error.response?.data?.detail || t('errorRemovingFish'));
        }
    };

    const handleSubmitFish = async (fishData) => {
        try {
            let updatedFish;
            if (currentFish && currentFish.id) {
                const response = await companyApi.updateFish(
                    currentAquarium,
                    currentFish.id,
                    { species: fishData.species, quantity: fishData.quantity },
                    selectedCompany.id
                );
                updatedFish = response.data;
            } else {
                const response = await companyApi.addFish(currentAquarium, {
                    ...fishData,
                    company_id: selectedCompany.id
                });
                updatedFish = response.data;
            }
            setIsFishFormOpen(false);
            setAquariums(prevAquariums =>
                prevAquariums.map(aquarium =>
                    aquarium.id === currentAquarium
                        ? {
                            ...aquarium,
                            fish: currentFish.id
                                ? aquarium.fish.map(fish => fish.id === currentFish.id ? updatedFish : fish)
                                : [...aquarium.fish, updatedFish]
                        }
                        : aquarium
                )
            );
            showAlert('success', currentFish.id ? t('fishUpdated') : t('fishAdded'));
        } catch (error) {
            showAlert('error', error.response?.data?.detail || t('errorSavingFish'));
        }
    };

    const handleAddAquarium = () => {
        setCurrentAquarium({});
        setIsAquariumFormOpen(true);
    };

    const handleEditAquarium = (aquarium) => {
        setCurrentAquarium(aquarium);
        setIsAquariumFormOpen(true);
    };

    const handleDeleteAquarium = async (aquariumId) => {
        try {
            await companyApi.deleteAquarium(selectedCompany.id, aquariumId);
            fetchAquariums();
            showAlert('success', t('aquariumDeleted'));
        } catch (error) {
            showAlert('error', error.response?.data?.detail || t('errorDeletingAquarium'));
        }
    };

    const handleSubmitAquarium = async (aquariumData) => {
        try {
            if (currentAquarium && currentAquarium.id) {
                await companyApi.updateAquarium(selectedCompany.id, currentAquarium.id, aquariumData);
            } else {
                await companyApi.createAquarium(selectedCompany.id, aquariumData);
            }
            setIsAquariumFormOpen(false);
            fetchAquariums();
            showAlert('success', currentAquarium ? t('aquariumUpdated') : t('aquariumCreated'));
        } catch (error) {
            showAlert('error', error.response?.data?.detail || t('errorSavingAquarium'));
        }
    };

    const showAlert = (severity, message) => {
        setAlert({ open: true, severity, message });
    };

    if (!selectedCompany) {
        return (
            <Container>
                <Typography variant="h4" gutterBottom>{t('pleaseSelectCompany')}</Typography>
            </Container>
        );
    }

    if (isLoading) {
        return (
            <Container sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
                <CircularProgress />
            </Container>
        );
    }

    return (
        <Container maxWidth="lg" sx={{mt: 4}}>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 4 }}>
                <Typography variant="h4" align="center" gutterBottom>
                    {t('aquariums')}
                </Typography>
                <Button variant="contained" color="primary" onClick={handleAddAquarium} sx={{ mt: 2 }}>
                    {t('createAquarium')}
                </Button>
            </Box>
            <Grid container spacing={4} sx={{ display: 'flex', justifyContent: 'center'}}>
                {aquariums.map((aquarium) => (
                    <Grid item xs={12} sm={6} md={4} key={aquarium.id} sx={{ display: 'flex' }}>
                        <AquariumCard
                            aquarium={aquarium}
                            onFeedNow={handleFeedNow}
                            onAddFish={() => handleAddFish(aquarium.id)}
                            onEditFish={(fish) => handleEditFish(aquarium.id, fish)}
                            onRemoveFish={(fishId) => handleRemoveFish(aquarium.id, fishId)}
                            onEdit={() => handleEditAquarium(aquarium)}
                            onDelete={() => handleDeleteAquarium(aquarium.id)}
                        />
                    </Grid>
                ))}
            </Grid>

            <Dialog open={isAquariumFormOpen} onClose={() => setIsAquariumFormOpen(false)}>
                <DialogTitle>{currentAquarium ? t('editAquarium') : t('createAquarium')}</DialogTitle>
                <DialogContent>
                    <AquariumForm onSubmit={handleSubmitAquarium} initialData={currentAquarium} />
                </DialogContent>
            </Dialog>

            <Dialog open={isFishFormOpen} onClose={() => setIsFishFormOpen(false)}>
                <DialogTitle>{currentFish.id ? t('editFish') : t('addFish')}</DialogTitle>
                <DialogContent>
                    <FishForm
                        onSubmit={handleSubmitFish}
                        initialData={currentFish}
                        aquariumCapacity={aquariums.find(a => a.id === currentAquarium)?.capacity}
                    />
                </DialogContent>
            </Dialog>

            <Snackbar open={alert.open} autoHideDuration={6000} onClose={() => setAlert({ ...alert, open: false })}>
                <Alert onClose={() => setAlert({ ...alert, open: false })} severity={alert.severity} sx={{ width: '100%' }}>
                    {alert.message}
                </Alert>
            </Snackbar>
        </Container>
    );
};

export default AquariumsPage;