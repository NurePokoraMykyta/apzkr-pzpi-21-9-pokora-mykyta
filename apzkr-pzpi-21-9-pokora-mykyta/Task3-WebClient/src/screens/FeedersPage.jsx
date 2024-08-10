import React, { useState, useEffect } from 'react';
import {
    Container,
    Typography,
    Button,
    Box,
    Snackbar,
    Alert,
    CircularProgress,
    Paper,
    Grid,
    List,
    ListItemSecondaryAction, IconButton, ListItemText, ListItem, Chip
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import { useCompany } from '../contexts/CompanyContext';
import { feedingScheduleApi, companyApi } from '../api';
import FeedingScheduleForm from '../components/FeedingScheduleForm';
import FeedingScheduleList from '../components/FeedingScheduleList';
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";

const FeedersPage = () => {
    const { t } = useTranslation();
    const { selectedCompany } = useCompany();
    const [aquariums, setAquariums] = useState([]);
    const [selectedAquarium, setSelectedAquarium] = useState(null);
    const [schedules, setSchedules] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [openForm, setOpenForm] = useState(false);
    const [currentSchedule, setCurrentSchedule] = useState(null);
    const [alert, setAlert] = useState({ open: false, severity: 'success', message: '' });

    useEffect(() => {
        if (selectedCompany) {
            fetchAquariums();
        }
    }, [selectedCompany]);

    useEffect(() => {
        if (selectedAquarium) {
            fetchFeedingSchedules();
        }
    }, [selectedAquarium]);

    const fetchAquariums = async () => {
        try {
            const response = await companyApi.getCompanyAquariums(selectedCompany.id);
            setAquariums(response.data);
            if (response.data.length > 0) {
                setSelectedAquarium(response.data[0]);
            }
        } catch (error) {
            showAlert('error', t('errorFetchingAquariums'));
        } finally {
            setIsLoading(false);
        }
    };

    const fetchFeedingSchedules = async () => {
        try {
            const response = await feedingScheduleApi.getAquariumFeedingSchedules(selectedAquarium.id);
            setSchedules(response.data);
        } catch (error) {
            showAlert('error', t('errorFetchingFeedingSchedules'));
        }
    };

    const handleAddSchedule = () => {
        setCurrentSchedule(null);
        setOpenForm(true);
    };

    const handleEditSchedule = (schedule) => {
        setCurrentSchedule(schedule);
        setOpenForm(true);
    };

    const handleDeleteSchedule = async (scheduleId) => {
        try {
            await feedingScheduleApi.deleteFeedingSchedule(scheduleId);
            setSchedules(schedules.filter(s => s.id !== scheduleId));
            showAlert('success', t('feedingScheduleDeleted'));
        } catch (error) {
            showAlert('error', t('errorDeletingFeedingSchedule'));
        }
    };

    const handleSubmitSchedule = async (scheduleData) => {
        try {
            if (currentSchedule) {
                const updatedSchedule = await feedingScheduleApi.updateFeedingSchedule(currentSchedule.id, scheduleData);
                setSchedules(schedules.map(s => s.id === updatedSchedule.id ? updatedSchedule : s));
                showAlert('success', t('feedingScheduleUpdated'));
            } else {
                const newSchedule = await feedingScheduleApi.addFeedingSchedule(selectedAquarium.id, scheduleData);
                setSchedules([...schedules, newSchedule]);
                showAlert('success', t('feedingScheduleAdded'));
            }
            setOpenForm(false);
        } catch (error) {
            showAlert('error', t('errorSavingFeedingSchedule'));
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
            <Typography variant="h4" align="center" gutterBottom sx={{ mb: 4 }}>
                {t('feeders')}
            </Typography>

            <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
                <Typography variant="h6" gutterBottom>{t('selectAquarium')}</Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    {aquariums.map((aquarium) => (
                        <Chip
                            key={aquarium.id}
                            label={aquarium.name}
                            onClick={() => setSelectedAquarium(aquarium)}
                            color={selectedAquarium?.id === aquarium.id ? "primary" : "default"}
                        />
                    ))}
                </Box>
            </Paper>

            {selectedAquarium && (
                <Paper elevation={3} sx={{ p: 3 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                        <Typography variant="h5">{t('feedingSchedules')}</Typography>
                        <Button variant="contained" color="primary" onClick={handleAddSchedule}>
                            {t('addFeedingSchedule')}
                        </Button>
                    </Box>
                    {schedules.length > 0 ? (
                        <List>
                            {schedules.map((schedule) => (
                                <ListItem key={schedule.id} divider>
                                    <ListItemText
                                        primary={schedule.food_type}
                                        secondary={`${t('scheduledTime')}: ${schedule.scheduled_time}`}
                                    />
                                    <ListItemSecondaryAction>
                                        <IconButton edge="end" aria-label="edit" onClick={() => handleEditSchedule(schedule)}>
                                            <EditIcon />
                                        </IconButton>
                                        <IconButton edge="end" aria-label="delete" onClick={() => handleDeleteSchedule(schedule.id)}>
                                            <DeleteIcon />
                                        </IconButton>
                                    </ListItemSecondaryAction>
                                </ListItem>
                            ))}
                        </List>
                    ) : (
                        <Typography variant="body1" align="center">
                            {t('noFeedingSchedules')}
                        </Typography>
                    )}
                </Paper>
            )}

            <FeedingScheduleForm
                open={openForm}
                onClose={() => setOpenForm(false)}
                onSubmit={handleSubmitSchedule}
                schedule={currentSchedule}
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

export default FeedersPage;