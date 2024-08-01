import React from 'react';
import { Grid, Card, CardContent, Typography, Box } from '@mui/material';
import HeadsetMicIcon from '@mui/icons-material/HeadsetMic';
import SetMealIcon from '@mui/icons-material/SetMeal';
import VerifiedUserIcon from '@mui/icons-material/VerifiedUser';
import {useTranslation} from "react-i18next";

const FeatureCard = ({ Icon, title, description }) => (
    <Card>
        <CardContent>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center' }}>
                <Icon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
                <Typography gutterBottom variant="h5" component="div">
                    {title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                    {description}
                </Typography>
            </Box>
        </CardContent>
    </Card>
);

const Features = () => {
    const { t, i18n } = useTranslation();
    return (
        <Box sx={{ flexGrow: 1, padding: 4, backgroundColor: 'grey.100' }}>
            <Grid container spacing={4}>
                <Grid item xs={12} md={4}>
                    <FeatureCard
                        Icon={HeadsetMicIcon}
                        title={t('excellentCustomerService')}
                        description={t('excellentCustomerServiceDesc')}
                    />
                </Grid>
                <Grid item xs={12} md={4}>
                    <FeatureCard
                        Icon={SetMealIcon}
                        title={t('perfectAquariumSelection')}
                        description={t('perfectAquariumSelectionDesc')}
                    />
                </Grid>
                <Grid item xs={12} md={4}>
                    <FeatureCard
                        Icon={VerifiedUserIcon}
                        title={t('qualityGuarantee')}
                        description={t('qualityGuaranteeDesc')}
                    />
                </Grid>
            </Grid>
        </Box>
    );
};

export default Features;