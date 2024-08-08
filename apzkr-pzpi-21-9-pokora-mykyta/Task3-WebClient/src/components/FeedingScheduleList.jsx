import React from 'react';
import { List, ListItem, ListItemText, ListItemSecondaryAction, IconButton, Typography } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import { useTranslation } from 'react-i18next';

const FeedingScheduleList = ({ schedules, onEdit, onDelete }) => {
    const { t } = useTranslation();

    return (
        <List>
            {schedules.length === 0 ? (
                <Typography variant="body1">{t('noFeedingSchedules')}</Typography>
            ) : (
                schedules.map((schedule) => (
                    <ListItem key={schedule.id}>
                        <ListItemText
                            primary={schedule.food_type}
                            secondary={`${t('scheduledTime')}: ${schedule.scheduled_time}`}
                        />
                        <ListItemSecondaryAction>
                            <IconButton edge="end" aria-label="edit" onClick={() => onEdit(schedule)}>
                                <EditIcon />
                            </IconButton>
                            <IconButton edge="end" aria-label="delete" onClick={() => onDelete(schedule.id)}>
                                <DeleteIcon />
                            </IconButton>
                        </ListItemSecondaryAction>
                    </ListItem>
                ))
            )}
        </List>
    );
};

export default FeedingScheduleList;