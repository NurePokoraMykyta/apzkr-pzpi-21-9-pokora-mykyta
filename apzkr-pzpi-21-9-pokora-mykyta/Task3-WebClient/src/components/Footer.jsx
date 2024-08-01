import React from 'react';
import { Box, Container, Grid, Typography, Link, TextField, Button, IconButton } from '@mui/material';
import FacebookIcon from '@mui/icons-material/Facebook';
import TwitterIcon from '@mui/icons-material/Twitter';
import InstagramIcon from '@mui/icons-material/Instagram';
import YouTubeIcon from '@mui/icons-material/YouTube';
import {useTranslation} from "react-i18next";

const Footer = () => {
    const { t, i18n } = useTranslation();
    return (
        <Box component="footer" sx={{ bgcolor: 'background.paper', py: 6 }}>
            <Container maxWidth="lg">
                <Grid container spacing={4} justifyContent="space-evenly">
                    <Grid item xs={12} sm={4} md={3}>
                        <Typography variant="h6" color="text.primary" gutterBottom>
                            {t('aboutUs')}
                        </Typography>
                        <Link href="#" color="text.secondary" display="block">{t('aboutCompany')}</Link>
                        <Link href="#" color="text.secondary" display="block">{t('contacts')}</Link>
                        <Link href="#" color="text.secondary" display="block">{t('warranty')}</Link>
                        <Link href="#" color="text.secondary" display="block">{t('partners')}</Link>
                    </Grid>
                    <Grid item xs={12} sm={4} md={3}>
                        <Typography variant="h6" color="text.primary" gutterBottom>
                            {t('products')}
                        </Typography>
                        <Link href="#" color="text.secondary" display="block">{t('aquariums')}</Link>
                        <Link href="#" color="text.secondary" display="block">{t('IoT')}</Link>
                        <Link href="#" color="text.secondary" display="block">{t('feeders')}</Link>
                        <Link href="#" color="text.secondary" display="block">{t('accessories')}</Link>
                    </Grid>
                    <Grid item xs={12} sm={4} md={3}>
                        <Typography variant="h6" color="text.primary" gutterBottom>
                            {t('subscribeToNews')}
                        </Typography>
                        <TextField
                            label={t('email')}
                            variant="outlined"
                            fullWidth
                            margin="normal"
                        />
                        <Button variant="contained" color="primary" sx={{ mt: 1 }}>
                            {t('subscribe')}
                        </Button>
                    </Grid>
                </Grid>
                <Box mt={5}>
                    <Typography variant="body2" color="text.secondary" align="center">
                        {'© '}
                        <Link color="inherit" href="http://localhost:3000/">
                            FinFare
                        </Link>{' '}
                        2024
                    </Typography>
                </Box>
                <Box mt={2} display="flex" justifyContent="center">
                    <IconButton aria-label="facebook" color="primary">
                        <FacebookIcon />
                    </IconButton>
                    <IconButton aria-label="twitter" color="primary">
                        <TwitterIcon />
                    </IconButton>
                    <IconButton aria-label="instagram" color="primary">
                        <InstagramIcon />
                    </IconButton>
                    <IconButton aria-label="youtube" color="primary">
                        <YouTubeIcon />
                    </IconButton>
                </Box>
            </Container>
        </Box>
    );
};

export default Footer;