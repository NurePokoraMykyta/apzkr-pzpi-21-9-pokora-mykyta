import React, { useState, useEffect } from 'react';
import {
    AppBar,
    Toolbar,
    Button,
    Box,
    Typography,
    Menu,
    MenuItem,
    Snackbar,
    Alert,
    CircularProgress
} from '@mui/material';
import { styled } from '@mui/material/styles';
import { useTranslation } from 'react-i18next';
import UaFlag from '../ua.png';
import EnFlag from '../en.png';
import { useAuth } from '../contexts/AuthContext';
import {LoginModal, RegisterModal} from "./AuthModals";
import {routes} from "../routes";
import {NavLink, Link} from "react-router-dom";
import CompanyButton from "./CompanyButton";

const StyledToolbar = styled(Toolbar)({
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    transition: 'all 0.3s',
});

const NavContainer = styled(Box)(({ theme }) => ({
    display: 'flex',
    justifyContent: 'center',
    padding: '8px 0',
    borderTop: '1px solid #e0e0e0',
    backgroundColor: theme.palette.background.paper,
    position: 'sticky',
    top: 0,
    zIndex: theme.zIndex.appBar,
}));

const StyledNavLink = styled(NavLink)(({ theme }) => ({
    textDecoration: 'none',
    color: theme.palette.text.primary,
    padding: '6px 16px',
    borderRadius: '4px',
    '&:hover': {
        backgroundColor: 'rgba(0, 0, 0, 0.04)',
    },
    '&.active': {
        backgroundColor: theme.palette.primary.main,
        color: theme.palette.common.white,
        '&:hover': {
            backgroundColor: theme.palette.primary.dark,
        },
    },
}));

const FlagIcon = styled('img')({
    width: 24,
    height: 24,
    borderRadius: '50%',
    objectFit: 'cover',
    cursor: 'pointer',
});
const Header = () => {
    const [isTopVisible, setIsTopVisible] = useState(true);
    const [isOpen, setOpen] = useState(null);
    const { t, i18n } = useTranslation();
    const { user,  logout, successMessage, setSuccessMessage } = useAuth();
    const [loginModalOpen, setLoginModalOpen] = useState(false);
    const [registerModalOpen, setRegisterModalOpen] = useState(false);

    const handleLoginClick = () => {
        setLoginModalOpen(true);
    };

    const handleRegisterClick = () => {
        setRegisterModalOpen(true);
    };

    const handleLogout = async () => {
        await logout();
    };


    useEffect(() => {
        const handleScroll = () => {
            const currentScrollPos = window.pageYOffset;
            setIsTopVisible(currentScrollPos < 50);
        };

        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const handleLanguageMenuOpen = (event) => {
        setOpen(event.currentTarget);
    };

    const handleLanguageMenuClose = () => {
        setOpen(null);
    };

    const changeLanguage = (lang) => {
        i18n.changeLanguage(lang).then(() => {
            handleLanguageMenuClose();
        });
    };

    return (
        <>
            <AppBar position="static" color="transparent" elevation={0} sx={{
                transition: 'all 0.3s',
                height: isTopVisible ? 'auto' : 0,
                overflow: 'hidden',
                visibility: isTopVisible ? 'visible' : 'hidden',
            }}>
                <StyledToolbar>
                    <Typography variant="h6" component="div" sx={{ visibility: 'hidden' }}>
                        FinFare
                    </Typography>
                    <Typography
                        variant="h6"
                        component={Link}
                        to="/"
                        sx={{
                            position: 'absolute',
                            left: '50%',
                            transform: 'translateX(-50%)',
                            textDecoration: 'none',
                            color: 'inherit',
                            '&:hover': {
                                textDecoration: 'none',
                            },
                        }}
                    >
                        FinFare
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <CompanyButton />
                        {user ? (
                            <Button variant="outlined" color="primary" onClick={handleLogout} sx={{ mr: 2 }}>{t('logout')}</Button>
                        ) : (
                            <Button variant="outlined" color="primary" onClick={handleLoginClick} sx={{ mr: 2 }}>{t('login')}</Button>
                        )}
                        <FlagIcon
                            src={i18n.language === 'ua' ? UaFlag : EnFlag}
                            alt={i18n.language === 'ua' ? 'Ukrainian' : 'English'}
                            onClick={handleLanguageMenuOpen}
                        />
                        <Menu
                            anchorEl={isOpen}
                            open={Boolean(isOpen)}
                            onClose={handleLanguageMenuClose}
                        >
                            <MenuItem onClick={() => changeLanguage('ua')}>
                                <FlagIcon src={UaFlag} alt="Ukrainian" sx={{ mr: 1 }} />
                                Українська
                            </MenuItem>
                            <MenuItem onClick={() => changeLanguage('en')}>
                                <FlagIcon src={EnFlag} alt="English" sx={{ mr: 1 }} />
                                English
                            </MenuItem>
                        </Menu>
                    </Box>
                </StyledToolbar>
            </AppBar>
            {user && (
                <NavContainer>
                    {routes.filter(route => route.showInNavigation).map(route => (
                        <StyledNavLink key={route.path} to={route.path}>
                            {t(route.name)}
                        </StyledNavLink>
                    ))}
                </NavContainer>
            )}
            <LoginModal
                open={loginModalOpen}
                onClose={() => setLoginModalOpen(false)}
                onSwitchToRegister={() => {
                    setLoginModalOpen(false);
                    setRegisterModalOpen(true);
                }}
            />
            <RegisterModal
                open={registerModalOpen}
                onClose={() => setRegisterModalOpen(false)}
                onSwitchToLogin={() => {
                    setRegisterModalOpen(false);
                    setLoginModalOpen(true);
                }}
            />
            <Snackbar
                open={!!successMessage}
                autoHideDuration={6000}
                onClose={() => setSuccessMessage(null)}
                anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
            >
                <Alert onClose={() => setSuccessMessage(null)} severity="success" sx={{ width: '100%' }}>
                    {successMessage}
                </Alert>
            </Snackbar>
        </>
    );
};

export default Header;