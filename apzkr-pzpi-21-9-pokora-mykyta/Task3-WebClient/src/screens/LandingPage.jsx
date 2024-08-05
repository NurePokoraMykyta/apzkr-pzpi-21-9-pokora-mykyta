import React from 'react';
import { ThemeProvider, CssBaseline } from '@mui/material';
import Header from "../components/Header";
import Hero from "../components/Hero";
import Features from "../components/Features";
import Awards from "../components/Awards";
import Footer from "../components/Footer";
import theme from "../theme";


const LandingPage = () => {
    return (
        <>
            <CssBaseline />
            <Hero />
            <Features />
            <Awards />
            <Footer />
        </>
    );
};

export default LandingPage;