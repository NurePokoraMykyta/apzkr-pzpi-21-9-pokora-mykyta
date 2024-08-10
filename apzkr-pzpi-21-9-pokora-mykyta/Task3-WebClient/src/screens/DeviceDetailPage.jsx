import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
    Container, Typography, Box, CircularProgress, Paper, Button,
    Table, TableBody, TableCell, TableContainer, TableHead, TableRow,
    Grid, TextField
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { useTranslation } from 'react-i18next';
import { deviceApi } from '../api';
import { format, parseISO, subDays } from 'date-fns';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const DeviceDetailPage = () => {
    const { aquariumId } = useParams();
    const navigate = useNavigate();
    const { t } = useTranslation();
    const [device, setDevice] = useState(null);
    const [waterParameters, setWaterParameters] = useState([]);
    const [loading, setLoading] = useState(true);
    const [startDate, setStartDate] = useState(subDays(new Date(), 7));
    const [endDate, setEndDate] = useState(new Date());

    useEffect(() => {
        fetchDeviceAndParameters();
    }, [aquariumId, startDate, endDate]);

    const fetchDeviceAndParameters = async () => {
        setLoading(true);
        try {
            const deviceResponse = await deviceApi.getDevice(aquariumId);
            setDevice(deviceResponse.data);

            const parametersResponse = await deviceApi.getWaterParameters(
                deviceResponse.data.aquarium_id,
                startDate.toISOString(),
                endDate.toISOString()
            );

            setWaterParameters(parametersResponse.data);
        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
                <CircularProgress />
            </Box>
        );
    }

    if (!device) {
        return (
            <Container>
                <Typography variant="h4">{t('deviceNotFound')}</Typography>
            </Container>
        );
    }

    return (
        <Container maxWidth="lg">
            <Button
                startIcon={<ArrowBackIcon />}
                onClick={() => navigate(-1)}
                sx={{ mt: 2, mb: 2 }}
            >
                {t('back')}
            </Button>
            <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
                <Typography variant="h4" gutterBottom>{t('deviceDetails')}</Typography>
                <Typography variant="h6">{t('deviceAddress')}: {device.unique_address}</Typography>
                <Typography>{t('status')}: {device.is_active ? t('active') : t('inactive')}</Typography>
            </Paper>

            <Paper elevation={3} sx={{ mt: 3, p: 3 }}>
                <Typography variant="h5" gutterBottom>{t('waterParameters')}</Typography>
                <LocalizationProvider dateAdapter={AdapterDateFns}>
                    <Grid container spacing={2} sx={{ mb: 3 }}>
                        <Grid item xs={12} sm={6}>
                            <DatePicker
                                label={t('startDate')}
                                value={startDate}
                                onChange={(newValue) => setStartDate(newValue)}
                                renderInput={(params) => <TextField {...params} fullWidth />}
                            />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <DatePicker
                                label={t('endDate')}
                                value={endDate}
                                onChange={(newValue) => setEndDate(newValue)}
                                renderInput={(params) => <TextField {...params} fullWidth />}
                            />
                        </Grid>
                    </Grid>
                </LocalizationProvider>

                <TableContainer>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>{t('dateTime')}</TableCell>
                                <TableCell>{t('ph')}</TableCell>
                                <TableCell>{t('temperature')}</TableCell>
                                <TableCell>{t('salinity')}</TableCell>
                                <TableCell>{t('oxygenLevel')}</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {waterParameters.map((param) => (
                                <TableRow key={param.id}>
                                    <TableCell>{format(parseISO(param.measured_at), 'yyyy-MM-dd HH:mm:ss')}</TableCell>
                                    <TableCell>{param.ph}</TableCell>
                                    <TableCell>{param.temperature}°C</TableCell>
                                    <TableCell>{param.salinity}‰</TableCell>
                                    <TableCell>{param.oxygen_level} mg/L</TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </Paper>
        </Container>
    );
};

export default DeviceDetailPage;