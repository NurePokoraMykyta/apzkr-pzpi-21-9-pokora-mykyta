import React, { useState, useEffect } from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, TextField, Button, Box } from '@mui/material';
import { TimePicker } from '@mui/x-date-pickers/TimePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { useTranslation } from 'react-i18next';

const FeedingScheduleForm = ({ open, onClose, onSubmit, schedule }) => {
    const { t } = useTranslation();
    const [foodType, setFoodType] = useState('');
    const [scheduledTime, setScheduledTime] = useState(null);

    useEffect(() => {
        if (schedule) {
            setFoodType(schedule.food_type);
            setScheduledTime(new Date(`2000-01-01T${schedule.scheduled_time}`));
        } else {
            setFoodType('');
            setScheduledTime(null);
        }
    }, [schedule]);

    const handleSubmit = () => {
        onSubmit({
            food_type: foodType,
            scheduled_time: scheduledTime.toTimeString().slice(0, 5),
        });
        onClose();
    };

    return (
        <Dialog open={open} onClose={onClose}>
            <DialogTitle>{schedule ? t('editFeedingSchedule') : t('addFeedingSchedule')}</DialogTitle>
            <DialogContent>
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
                    <TextField
                        label={t('foodType')}
                        value={foodType}
                        onChange={(e) => setFoodType(e.target.value)}
                        fullWidth
                    />
                    <LocalizationProvider dateAdapter={AdapterDateFns}>
                        <TimePicker
                            label={t('scheduledTime')}
                            value={scheduledTime}
                            onChange={setScheduledTime}
                            renderInput={(params) => <TextField {...params} fullWidth />}
                        />
                    </LocalizationProvider>
                </Box>
            </DialogContent>
            <DialogActions>
                <Button onClick={onClose}>{t('cancel')}</Button>
                <Button onClick={handleSubmit} color="primary">{t('save')}</Button>
            </DialogActions>
        </Dialog>
    );
};

export default FeedingScheduleForm;