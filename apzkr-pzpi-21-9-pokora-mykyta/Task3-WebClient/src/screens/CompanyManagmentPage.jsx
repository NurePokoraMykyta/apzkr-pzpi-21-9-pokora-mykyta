// screens/CompanyManagementPage.jsx
import React, { useState, useEffect } from 'react';
import {Container, Typography, TextField, Button, Box, Tabs, Tab, Snackbar, Alert, Paper, Grid} from '@mui/material';
import { useTranslation } from 'react-i18next';
import { useCompany } from '../contexts/CompanyContext';
import { companyApi, rolesApi } from '../api';
import RoleForm from '../components/RoleForm';
import UserTable from '../components/UserTable';
import AddUserDialog from "../components/AddUserForm";

const CompanyManagementPage = () => {
    const { t } = useTranslation();
    const { selectedCompany, updateSelectedCompany  } = useCompany();
    const [companyName, setCompanyName] = useState('');
    const [companyDescription, setCompanyDescription] = useState('');
    const [users, setUsers] = useState([]);
    const [roles, setRoles] = useState([]);
    const [openRoleForm, setOpenRoleForm] = useState(false);
    const [currentRole, setCurrentRole] = useState(null);
    const [tabValue, setTabValue] = useState(0);
    const [openAddUserDialog, setOpenAddUserDialog] = useState(false);
    const [alert, setAlert] = useState({ open: false, severity: 'success', message: '' });

    useEffect(() => {
        if (selectedCompany) {
            setCompanyName(selectedCompany.name);
            setCompanyDescription(selectedCompany.description);
            fetchUsers();
            fetchRoles();
        }
    }, [selectedCompany]);

    const fetchUsers = async () => {
        try {
            const response = await companyApi.getCompanyUsers(selectedCompany.id);
            setUsers(response.data);
        } catch (error) {
            showAlert('error', t('errorFetchingUsers'));
        }
    };

    const fetchRoles = async () => {
        try {
            const response = await rolesApi.getCompanyRoles(selectedCompany.id);
            setRoles(response.data);
        } catch (error) {
            showAlert('error', t('errorFetchingRoles'));
        }
    };

    const handleUpdateCompany = async () => {
        try {
            const updatedCompany = await companyApi.updateCompany(selectedCompany.id, { name: companyName, description: companyDescription });
            updateSelectedCompany(updatedCompany);
            setCompanyName(updatedCompany.name);
            setCompanyDescription(updatedCompany.description);
            showAlert('success', t('companyUpdated'));
        } catch (error) {
            showAlert('error', t('errorUpdatingCompany'));
        }
    };

    const handleDeleteCompany = async () => {
        if (window.confirm(t('confirmDeleteCompany'))) {
            try {
                await companyApi.deleteCompany(selectedCompany.id);
                updateSelectedCompany(null);
                showAlert('success', t('companyDeleted'));
            } catch (error) {
                showAlert('error', t('errorDeletingCompany'));
            }
        }
    };

    const handleRemoveUser = async (email) => {
        try {
            await companyApi.removeUserFromCompany(selectedCompany.id, email);
            fetchUsers();
            showAlert('success', t('userRemoved'));
        } catch (error) {
            showAlert('error', t('errorRemovingUser'));
        }
    };

    const handleAddUser = async (email, roleId) => {
        try {
            await companyApi.addUserToCompany(selectedCompany.id, email, roleId);
            fetchUsers();
            setOpenAddUserDialog(false);
            showAlert('success', t('userAdded'));
        } catch (error) {
            showAlert('error', t('errorAddingUser'));
        }
    };

    const handleAssignRole = async (userUid, roleId) => {
        try {
            await rolesApi.assignRole(roleId, userUid, selectedCompany.id);
            fetchUsers();
            showAlert('success', t('roleAssigned'));
        } catch (error) {
            showAlert('error', t('errorAssigningRole'));
        }
    };

    const handleSubmitRole = async (roleData) => {
        try {
            if (currentRole) {
                await rolesApi.updateRole(currentRole.id, { ...roleData, company_id: selectedCompany.id }, selectedCompany.id);
                showAlert('success', t('roleUpdated'));
            } else {
                await rolesApi.createRole({ ...roleData, company_id: selectedCompany.id });
                showAlert('success', t('roleCreated'));
            }
            fetchRoles();
        } catch (error) {
            showAlert('error', t('errorSavingRole'));
        }
    };

    const showAlert = (severity, message) => {
        setAlert({ open: true, severity, message });
    };

    if (!selectedCompany) {
        return <Typography>{t('noCompanySelected')}</Typography>;
    }

    return (
        <Container maxWidth="lg">
            <Typography variant="h4" align="center" gutterBottom sx={{ my: 4 }}>
                {t('companyManagement')}
            </Typography>

            <Paper elevation={3} sx={{ p: 3, mb: 4 }}>
                <Tabs
                    value={tabValue}
                    onChange={(e, newValue) => setTabValue(newValue)}
                    variant="fullWidth"
                    indicatorColor="primary"
                    textColor="primary"
                >
                    <Tab label={t('companyInfo')} />
                    <Tab label={t('users')} />
                    <Tab label={t('roles')} />
                </Tabs>
            </Paper>

            {tabValue === 0 && (
                <Paper elevation={3} sx={{ p: 4 }}>
                    <Typography variant="h5" gutterBottom>{t('companyInfo')}</Typography>
                    <TextField
                        fullWidth
                        label={t('companyName')}
                        value={companyName}
                        onChange={(e) => setCompanyName(e.target.value)}
                        margin="normal"
                        variant="outlined"
                    />
                    <TextField
                        fullWidth
                        label={t('companyDescription')}
                        value={companyDescription}
                        onChange={(e) => setCompanyDescription(e.target.value)}
                        margin="normal"
                        multiline
                        rows={4}
                        variant="outlined"
                    />
                    <Box sx={{ mt: 3, display: 'flex', justifyContent: 'space-between' }}>
                        <Button variant="contained" color="primary" onClick={handleUpdateCompany}>
                            {t('updateCompany')}
                        </Button>
                        <Button variant="outlined" color="error" onClick={handleDeleteCompany}>
                            {t('deleteCompany')}
                        </Button>
                    </Box>
                </Paper>
            )}

            {tabValue === 1 && (
                <Paper elevation={3} sx={{ p: 4 }}>
                    <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
                        <Typography variant="h5">{t('companyUsers')}</Typography>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={() => setOpenAddUserDialog(true)}
                        >
                            {t('addUser')}
                        </Button>
                    </Box>
                    <UserTable
                        users={users}
                        roles={roles}
                        onRemoveUser={handleRemoveUser}
                        onAssignRole={handleAssignRole}
                    />
                </Paper>
            )}

            {tabValue === 2 && (
                <Paper elevation={3} sx={{ p: 4 }}>
                    <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
                        <Typography variant="h5">{t('roles')}</Typography>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={() => {
                                setCurrentRole(null);
                                setOpenRoleForm(true);
                            }}
                        >
                            {t('createRole')}
                        </Button>
                    </Box>
                    <Grid container spacing={3}>
                        {roles.map((role) => (
                            <Grid item xs={12} sm={6} md={4} key={role.id}>
                                <Paper elevation={2} sx={{ p: 2 }}>
                                    <Typography variant="subtitle1" gutterBottom>{role.name}</Typography>
                                    <Typography variant="body2" sx={{ mb: 2 }}>{role.description}</Typography>
                                    <Button
                                        variant="outlined"
                                        fullWidth
                                        onClick={() => {
                                            setCurrentRole(role);
                                            setOpenRoleForm(true);
                                        }}
                                    >
                                        {t('edit')}
                                    </Button>
                                </Paper>
                            </Grid>
                        ))}
                    </Grid>
                </Paper>
            )}

            <AddUserDialog
                open={openAddUserDialog}
                onClose={() => setOpenAddUserDialog(false)}
                onAddUser={handleAddUser}
                roles={roles}
            />

            <RoleForm
                open={openRoleForm}
                onClose={() => setOpenRoleForm(false)}
                onSubmit={handleSubmitRole}
                role={currentRole}
            />

            <Snackbar
                open={alert.open}
                autoHideDuration={6000}
                onClose={() => setAlert({ ...alert, open: false })}
            >
                <Alert onClose={() => setAlert({ ...alert, open: false })} severity={alert.severity} sx={{ width: '100%' }}>
                    {alert.message}
                </Alert>
            </Snackbar>
        </Container>
    );
};

export default CompanyManagementPage;