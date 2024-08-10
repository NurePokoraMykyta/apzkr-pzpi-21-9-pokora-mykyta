import React from 'react';
import { Card, CardContent, Typography, Button, Box, Chip } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import PowerSettingsNewIcon from '@mui/icons-material/PowerSettingsNew';
import RestaurantIcon from '@mui/icons-material/Restaurant';
import { useTranslation } from 'react-i18next';
import {useNavigate} from "react-router-dom";

const DeviceCard = ({ device, aquarium, onEdit, onToggleActive, onManageFood }) => {
    const { t } = useTranslation();
    const navigate = useNavigate();
    console.log(device);
    console.log("Аквариум");
    return (
        <Card elevation={3}
              onClick={(e) => {
                  if (!e.target.closest('button')) {
                      navigate(`/devices/aquarium/${aquarium.id}`);
                  }
              }}
              sx={{
                  cursor: 'pointer',
                  '&:hover': {
                      boxShadow: 6,
                  },
              }}>
            <CardContent>
                <Typography variant="h6" gutterBottom>{device.unique_address}</Typography>
                <Box display="flex" alignItems="center" mb={2}>
                    <Chip
                        label={device.is_active ? t('active') : t('inactive')}
                        color={device.is_active ? 'success' : 'error'}
                        size="small"
                    />
                    <Typography variant="body2" color="textSecondary" ml={1}>
                        {t('aquarium')}: {aquarium.name}
                    </Typography>
                </Box>
                <Box display="flex" justifyContent="space-between">
                    <Button startIcon={<EditIcon />} onClick={() => onEdit(device)}>
                        {t('edit')}
                    </Button>
                    <Button
                        startIcon={<PowerSettingsNewIcon />}
                        color={device.is_active ? 'warning' : 'success'}
                        onClick={() => onToggleActive(device)}
                    >
                        {device.is_active ? t('deactivate') : t('activate')}
                    </Button>
                </Box>
                <Box mt={2}>
                    <Button
                        startIcon={<RestaurantIcon />}
                        color="primary"
                        onClick={() => onManageFood(device)}
                        fullWidth
                    >
                        {t('manageFood')}
                    </Button>
                </Box>
            </CardContent>
        </Card>
    );
};

export default DeviceCard;