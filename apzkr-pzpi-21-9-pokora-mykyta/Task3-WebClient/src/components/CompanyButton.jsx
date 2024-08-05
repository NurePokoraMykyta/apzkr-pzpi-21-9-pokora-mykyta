import React, { useState } from 'react';
import { Button, Menu, MenuItem, Dialog } from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import { useCompany } from '../contexts/CompanyContext';
import { LoginModal, RegisterModal } from './AuthModals';
import CompanyList from './CompanyList';
import CreateCompanyForm from './CreateCompanyForm';
import { useTranslation } from "react-i18next";

const CompanyButton = () => {
    const { user } = useAuth();
    const { selectedCompany } = useCompany();
    const { t } = useTranslation();
    const [open, setOpen] = useState(null);
    const [openLoginModal, setOpenLoginModal] = useState(false);
    const [openRegisterModal, setOpenRegisterModal] = useState(false);
    const [openCompanyListDialog, setOpenCompanyListDialog] = useState(false);
    const [openCreateCompanyDialog, setOpenCreateCompanyDialog] = useState(false);

    const handleClick = (event) => {
        if (user) {
            setOpen(event.currentTarget);
        } else {
            setOpenLoginModal(true);
        }
    };

    const handleClose = () => {
        setOpen(null);
    };

    const handleCompanyList = () => {
        handleClose();
        setOpenCompanyListDialog(true);
    };

    const handleCreateCompany = () => {
        handleClose();
        setOpenCreateCompanyDialog(true);
    };

    const handleSwitchToRegister = () => {
        setOpenLoginModal(false);
        setOpenRegisterModal(true);
    };

    const handleSwitchToLogin = () => {
        setOpenRegisterModal(false);
        setOpenLoginModal(true);
    };

    return (
        <>
            <Button
                variant="contained"
                color="primary"
                onClick={handleClick}
                sx={{ mr: 2 }}
            >
                {selectedCompany ? selectedCompany.name : t('company')}
            </Button>
            {user && (
                <Menu
                    anchorEl={open}
                    open={Boolean(open)}
                    onClose={handleClose}
                >
                    <MenuItem onClick={handleCompanyList}>{t('myCompanies')}</MenuItem>
                    <MenuItem onClick={handleCreateCompany}>{t('createCompany')}</MenuItem>
                </Menu>
            )}
            <LoginModal
                open={openLoginModal}
                onClose={() => setOpenLoginModal(false)}
                onSwitchToRegister={handleSwitchToRegister}
            />
            <RegisterModal
                open={openRegisterModal}
                onClose={() => setOpenRegisterModal(false)}
                onSwitchToLogin={handleSwitchToLogin}
            />
            <Dialog open={openCompanyListDialog} onClose={() => setOpenCompanyListDialog(false)}>
                <CompanyList onClose={() => setOpenCompanyListDialog(false)} />
            </Dialog>
            <Dialog open={openCreateCompanyDialog} onClose={() => setOpenCreateCompanyDialog(false)}>
                <CreateCompanyForm onSuccess={() => setOpenCreateCompanyDialog(false)} />
            </Dialog>
        </>
    );
};

export default CompanyButton;