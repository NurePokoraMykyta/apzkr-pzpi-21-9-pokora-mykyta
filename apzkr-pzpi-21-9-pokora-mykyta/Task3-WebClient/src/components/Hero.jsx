import React from 'react';
import { Grid, Box, Typography } from '@mui/material';
import { styled } from '@mui/material/styles';
import IoTImage from '../img.png';
import {useTranslation} from "react-i18next";

const HeroBox = styled(Box)({
    position: 'relative',
    height: 0,
    paddingTop: '56.25%',
    backgroundSize: 'cover',
    backgroundPosition: 'center',
});

const TextBox = styled(Box)({
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    padding: '40px 0px 20px 0px',
    textAlign: 'center',
});

const HeroText = styled(Typography)({
    color: '#fff',
    fontSize: 24,
});

const HeroImage = ({ src, title }) => (
    <HeroBox
        sx={{
            backgroundImage: `
        linear-gradient(
          rgba(255, 255, 255, 0),
          rgba(0, 0, 0, 0.0),
          rgba(0, 0, 0, 0.7)
        ),
        url('${src}')
      `,
        }}
    >
        <TextBox>
            <HeroText>{title}</HeroText>
        </TextBox>
    </HeroBox>
);

const Hero = () => {
    const { t, i18n } = useTranslation();

    return (
        <Box sx={{ flexGrow: 1, p: 2 }}>
            <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                    <HeroImage
                        src="https://cdn.britannica.com/29/121829-050-911F77EC/freshwater-aquarium.jpg"
                        title={t('aquariums')}
                    />
                </Grid>
                <Grid item xs={12} md={6}>
                    <HeroImage
                        src="https://fbi.cults3d.com/uploaders/17010591/illustration-file/437ad06d-af28-4e5e-ab3e-9f27ec000910/bild_2.jpg"
                        title={t('feeders')}
                    />
                </Grid>
                <Grid item xs={12} sm={4}>
                    <HeroImage
                        src={IoTImage}
                        title={t('IoT')}
                    />
                </Grid>
                <Grid item xs={12} sm={4}>
                    <HeroImage
                        src="https://media.istockphoto.com/id/887987150/photo/blogging-woman-reading-blog.jpg?s=612x612&w=0&k=20&c=7SScR_Y4n7U3k5kBviYm3VwEmW4vmbngDUa0we429GA="
                        title={t('blog')}
                    />
                </Grid>
                <Grid item xs={12} sm={4}>
                    <HeroImage
                        src="https://st.depositphotos.com/1011643/3244/i/450/depositphotos_32445073-Male-customer-support-operator-with-headset.jpg"
                        title={t('support')}
                    />
                </Grid>
            </Grid>
        </Box>
    );
};

export default Hero;