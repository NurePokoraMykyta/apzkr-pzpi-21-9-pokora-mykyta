// src/components/CompanyRequiredWrapper.js
import React from 'react';
import { useCompany } from '../contexts/CompanyContext';
import {
    Box,
    Typography,
    Paper,
    Container,
    Grid,
    Tooltip,
    Card,
    CardContent,
    CardActionArea,
    Avatar
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import { styled } from '@mui/material/styles';
import BusinessIcon from '@mui/icons-material/Business';
import InfoOutlinedIcon from '@mui/icons-material/InfoOutlined';

const StyledCard = styled(Card)(({ theme }) => ({
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
    transition: 'transform 0.3s, box-shadow 0.3s',
    '&:hover': {
        transform: 'translateY(-5px)',
        boxShadow: theme.shadows[8],
    },
}));

const IconAvatar = styled(Avatar)(({ theme }) => ({
    backgroundColor: theme.palette.primary.main,
    width: 56,
    height: 56,
    margin: '0 auto 16px',
}));

const CompanyRequiredWrapper = ({ children, pageIcon, pageTitle, pageDescription }) => {
    const { selectedCompany } = useCompany();
    const { t } = useTranslation();

    if (!selectedCompany) {
        return (
            <Container maxWidth="md">
                <Paper elevation={3} sx={{ mt: 4, p: 4, borderRadius: 2, backgroundColor: 'background.default' }}>
                    <Grid container spacing={3} alignItems="center" justifyContent="center">
                        <Grid item xs={12} textAlign="center">
                            <IconAvatar>
                                <BusinessIcon fontSize="large" />
                            </IconAvatar>
                            <Typography variant="h4" gutterBottom fontWeight="bold">
                                {t('noCompanySelected')}
                            </Typography>
                            <Typography variant="subtitle1" color="text.secondary" paragraph>
                                {t('pleaseSelectCompanyHeader')}
                            </Typography>
                        </Grid>
                        <Grid item xs={12} sm={6} md={4}>
                            <StyledCard>
                                <CardActionArea>
                                    <CardContent>
                                        <IconAvatar>
                                            {pageIcon}
                                        </IconAvatar>
                                        <Typography variant="h6" component="div" gutterBottom>
                                            {pageTitle}
                                        </Typography>
                                        <Typography variant="body2" color="text.secondary">
                                            {pageDescription}
                                        </Typography>
                                    </CardContent>
                                </CardActionArea>
                            </StyledCard>
                        </Grid>
                        <Grid item xs={12} textAlign="center" sx={{ mt: 4 }}>
                            <Tooltip title={t('companySelectionHelp')} arrow>
                                <Box display="flex" alignItems="center" justifyContent="center">
                                    <InfoOutlinedIcon color="primary" sx={{ mr: 1 }} />
                                    <Typography variant="body2" color="text.secondary">
                                        {t('useCompanyButtonToSelect')}
                                    </Typography>
                                </Box>
                            </Tooltip>
                        </Grid>
                    </Grid>
                </Paper>
            </Container>
        );
    }

    return children;
};

export default CompanyRequiredWrapper;