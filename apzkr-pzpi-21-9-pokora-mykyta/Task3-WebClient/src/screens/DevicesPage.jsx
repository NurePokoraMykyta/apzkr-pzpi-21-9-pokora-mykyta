import React, { useState, useEffect } from 'react';
import {Container, Typography, Grid, Button, Snackbar, Alert, CircularProgress, Box} from '@mui/material';
import { useTranslation } from 'react-i18next';
import DeviceCard from '../components/DeviceCard';
import DeviceForm from '../components/DeviceForm';
import FoodPatchForm from '../components/FoodPatchForm';
import { deviceApi, companyApi } from '../api';
import { useCompany } from '../contexts/CompanyContext';

const DevicesPage = () => {
    const { t } = useTranslation();
    const { selectedCompany } = useCompany();
    const [devices, setDevices] = useState([]);
    const [aquariums, setAquariums] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [openDeviceForm, setOpenDeviceForm] = useState(false);
    const [openFoodPatchForm, setOpenFoodPatchForm] = useState(false);
    const [currentDevice, setCurrentDevice] = useState(null);
    const [currentFoodPatch, setCurrentFoodPatch] = useState(null);
    const [alert, setAlert] = useState({ open: false, severity: 'success', message: '' });

    useEffect(() => {
        if (selectedCompany) {
            fetchAquariums();
        }
    }, [selectedCompany]);

    const fetchAquariums = async () => {
        try {
            const response = await companyApi.getCompanyAquariums(selectedCompany.id);
            setAquariums(response.data);
            fetchDevices(response.data);
        } catch (error) {
            showAlert('error', t('errorFetchingAquariums'));
        } finally {
            setIsLoading(false);
        }
    };

    const fetchDevices = async (aquariumsList) => {
        const devicesList = [];
        for (const aquarium of aquariumsList) {
            try {
                const response = await deviceApi.getDevice(aquarium.id);
                devicesList.push(response.data);
            } catch (error) {
                if (error.response && error.response.status === 404) {
                    console.log(`No device found for aquarium ${aquarium.id}`);
                } else {
                    console.error(`Error fetching device for aquarium ${aquarium.id}:`, error);
                }
            }
        }
        setDevices(devicesList);
    };

    const handleAddDevice = () => {
        setCurrentDevice(null);
        setOpenDeviceForm(true);
    };

    const handleEditDevice = (device) => {
        setCurrentDevice(device);
        setOpenDeviceForm(true);
    };

    const handleToggleActive = async (device) => {
        const updatedDevices = devices.map(d =>
            d.id === device.id ? { ...d, is_active: !d.is_active } : d
        );
        setDevices(updatedDevices);

        try {
            let updatedDevice;
            if (device.is_active) {
                updatedDevice = await deviceApi.deactivateDevice(device.aquarium_id);
            } else {
                updatedDevice = await deviceApi.activateDevice(device.aquarium_id);
            }
            setDevices(prevDevices =>
                prevDevices.map(d => (d.id === updatedDevice.id ? updatedDevice : d))
            );
            showAlert(
                'success',
                updatedDevices.find(d => d.id === device.id).is_active
                    ? t('deviceActivated')
                    : t('deviceDeactivated')
            );
        } catch (error) {
            setDevices(devices);
            showAlert('error', t('errorTogglingDevice'));
        }
    };

    const handleManageFood = (device) => {
        setCurrentDevice(device);
        setCurrentFoodPatch(null);
        setOpenFoodPatchForm(true);
    };

    const handleSubmitDevice = async (deviceData) => {
        try {
            let updatedDevice;
            if (currentDevice) {
                updatedDevice = await deviceApi.updateDevice(deviceData.aquarium_id, deviceData);
                setDevices(devices.map(d => d.id === updatedDevice.id ? updatedDevice : d));
            } else {
                updatedDevice = await deviceApi.setupDevice(deviceData.aquarium_id, deviceData);
                setDevices([...devices, updatedDevice]);
            }
            showAlert('success', currentDevice ? t('deviceUpdated') : t('deviceAdded'));
            setOpenDeviceForm(false);
        } catch (error) {
            showAlert('error', t('errorSavingDevice'));
        }
    };

    const handleSubmitFoodPatch = async (foodPatchData) => {
        try {
            const updatedDevice = await deviceApi.fillFoodPatch(currentDevice.aquarium_id, foodPatchData);
            setDevices(devices.map(d => d.id === updatedDevice.id ? updatedDevice : d));
            showAlert('success', t('foodPatchAdded'));
            setOpenFoodPatchForm(false);
        } catch (error) {
            showAlert('error', t('errorSavingFoodPatch'));
        }
    };

    const handleDeleteFoodPatch = async () => {
        try {
            await deviceApi.deleteFoodPatch(currentDevice.aquarium_id);
            const updatedDevice = { ...currentDevice, food_patch: null };
            setDevices(devices.map(d => d.id === updatedDevice.id ? updatedDevice : d));
            showAlert('success', t('foodPatchDeleted'));
            setOpenFoodPatchForm(false);
        } catch (error) {
            showAlert('error', t('errorDeletingFoodPatch'));
        }
    };

    const showAlert = (severity, message) => {
        setAlert({ open: true, severity, message });
    };

    if (isLoading) {
        return (
            <Container sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
                <CircularProgress />
            </Container>
        );
    }

    return (
        <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', mb: 4 }}>
                <Typography variant="h4" align="center" gutterBottom>
                    {t('devices')}
                </Typography>
                <Button variant="contained" color="primary" onClick={handleAddDevice} sx={{ mt: 2 }}>
                    {t('addDevice')}
                </Button>
            </Box>
            <Grid container spacing={3}>
                {devices.map((device) => {
                    const aquarium = aquariums.find(a => a.id === device.aquarium_id);
                    return (
                        <Grid item xs={12} sm={6} md={4} key={device.id}>
                            <DeviceCard
                                device={device}
                                aquarium={aquarium}
                                onEdit={handleEditDevice}
                                onToggleActive={handleToggleActive}
                                onManageFood={handleManageFood}
                            />
                        </Grid>
                    );
                })}
            </Grid>
            {devices.length === 0 && (
                <Typography variant="body1" sx={{ mt: 2 }}>
                    {t('noDevicesFound')}
                </Typography>
            )}
            <DeviceForm
                open={openDeviceForm}
                onClose={() => setOpenDeviceForm(false)}
                onSubmit={handleSubmitDevice}
                device={currentDevice}
                aquariums={aquariums}
            />
            <FoodPatchForm
                open={openFoodPatchForm}
                onClose={() => setOpenFoodPatchForm(false)}
                onSubmit={handleSubmitFoodPatch}
                onDelete={handleDeleteFoodPatch}
                currentFoodPatch={currentDevice?.food_patch}
            />
            <Snackbar
                open={alert.open}
                autoHideDuration={6000}
                onClose={() => setAlert({ ...alert, open: false })}
            >
                <Alert onClose={() => setAlert({ ...alert, open: false })} severity={alert.severity} sx={{ width: '100%' }}>
                    {alert.message}
                </Alert>
            </Snackbar>
        </Container>
    );
};

export default DevicesPage;