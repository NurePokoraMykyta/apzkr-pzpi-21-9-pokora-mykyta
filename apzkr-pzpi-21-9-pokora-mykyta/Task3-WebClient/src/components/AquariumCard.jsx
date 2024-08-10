// src/components/AquariumCard.jsx
import React from 'react';
import {
    Card,
    CardContent,
    CardActions,
    Typography,
    Button,
    List,
    ListItem,
    ListItemText,
    IconButton,
    Box,
    Divider
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import RestaurantIcon from '@mui/icons-material/Restaurant';
import AddIcon from '@mui/icons-material/Add';


const AquariumCard = ({ aquarium, onFeedNow, onAddFish, onEditFish, onRemoveFish, onEdit, onDelete }) => {
    const { t } = useTranslation();

    return (
        <Card elevation={3} sx={{ display: 'flex', flexDirection: 'column', height: '100%', maxWidth: '100%' }}>
            <CardContent sx={{ flexGrow: 1 }}>
                <Typography variant="h5" component="div" gutterBottom>
                    {aquarium.name}
                </Typography>
                <Typography color="textSecondary" gutterBottom>
                    {t('capacity')}: {aquarium.capacity} {t('liters')}
                </Typography>
                <Typography variant="body2" paragraph>
                    {aquarium.description}
                </Typography>

                <Divider sx={{ my: 2 }} />

                <Typography variant="subtitle1" gutterBottom>
                    {t('fish')}:
                </Typography>
                <Box sx={{ maxHeight: 200, overflow: 'auto', mb: 2 }}>
                    {aquarium.fish && aquarium.fish.length > 0 ? (
                        <List dense>
                            {aquarium.fish.map((fish) => (
                                <ListItem
                                    key={fish.id}
                                    secondaryAction={
                                        <Box>
                                            <IconButton edge="end" aria-label="edit" onClick={() => onEditFish(fish)}>
                                                <EditIcon />
                                            </IconButton>
                                            <IconButton edge="end" aria-label="delete" onClick={() => onRemoveFish(fish.id)}>
                                                <DeleteIcon />
                                            </IconButton>
                                        </Box>
                                    }
                                >
                                    <ListItemText
                                        primary={`${fish.species}`}
                                        secondary={`${t('quantity')}: ${fish.quantity}`}
                                    />
                                </ListItem>
                            ))}
                        </List>
                    ) : (
                        <Typography variant="body2" color="textSecondary">
                            {t('noFishInAquarium')}
                        </Typography>
                    )}
                </Box>
            </CardContent>

            <CardActions>
                <Button
                    size="small"
                    startIcon={<RestaurantIcon />}
                    onClick={() => onFeedNow(aquarium.id)}
                >
                    {t('feedNow')}
                </Button>
                <Button
                    size="small"
                    startIcon={<AddIcon />}
                    onClick={() => onAddFish(aquarium.id)}
                >
                    {t('addFish')}
                </Button>
                <Button
                    size="small"
                    startIcon={<EditIcon />}
                    onClick={() => onEdit(aquarium)}
                >
                    {t('edit')}
                </Button>
                <Button
                    size="small"
                    color="error"
                    startIcon={<DeleteIcon />}
                    onClick={() => onDelete(aquarium.id)}
                >
                    {t('delete')}
                </Button>
            </CardActions>
        </Card>
    );
};

export default AquariumCard;