import React from 'react';
import { Box, Grid, Typography, Button } from '@mui/material';
import { useTranslation } from "react-i18next";

const AwardLogo = ({ src, alt }) => (
    <img src={src} alt={alt} style={{ height: 'auto', width: '100%', maxWidth: '150px' }} />
);

const Awards = () => {
    const { t } = useTranslation();
    return (
        <Box sx={{ flexGrow: 1, padding: 4, textAlign: 'center'}}>
            <Typography color='primary' variant="h4" component="h2" gutterBottom sx={{ marginBottom: 4 }}>
                {t('latestAwards')}
            </Typography>
            <Grid container justifyContent="center" spacing={4} sx={{ mb: 4 }}>
                <Grid item xs={6} sm={3}>
                    <AwardLogo src="https://www.surepetcare.com/images/misc/awards/IOT_Awards_Frame.png" alt="CES Innovation Award" />
                </Grid>
                <Grid item xs={6} sm={3}>
                    <AwardLogo src="https://media.surepetcare.com/website/images/awards/dogster.png" alt="Dogster Approved" />
                </Grid>
                <Grid item xs={6} sm={3}>
                    <AwardLogo src="https://media.surepetcare.com/website/images/awards/readers.png" alt="Editor's Choice" />
                </Grid>
                <Grid item xs={6} sm={3}>
                    <AwardLogo src="https://media.surepetcare.com/website/images/awards/ces.png" alt="CES Innovation Award" />
                </Grid>
            </Grid>
            <Button variant="outlined" color="primary" sx={{
                borderColor: '#00a0e9',
                color: '#00a0e9',
                '&:hover': {
                    borderColor: '#008bc7',
                    backgroundColor: 'rgba(0, 160, 233, 0.04)'
                }
            }}>
                {t('mentionsInMedia')}
            </Button>
        </Box>
    );
};

export default Awards;