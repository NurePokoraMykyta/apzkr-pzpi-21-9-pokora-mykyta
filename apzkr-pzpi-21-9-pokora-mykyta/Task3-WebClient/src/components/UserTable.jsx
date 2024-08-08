import React from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button, Select, MenuItem } from '@mui/material';
import { useTranslation } from 'react-i18next';

const UserTable = ({ users, roles, onRemoveUser, onAssignRole }) => {
    const { t } = useTranslation();

    return (
        <TableContainer component={Paper}>
            <Table>
                <TableHead>
                    <TableRow>
                        <TableCell>{t('email')}</TableCell>
                        <TableCell>{t('role')}</TableCell>
                        <TableCell>{t('actions')}</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {users.map((user) => (
                        <TableRow key={user.id}>
                            <TableCell>{user.email}</TableCell>
                            <TableCell>
                                <Select
                                    value={user.role_id || ''}
                                    onChange={(e) => onAssignRole(user.id, e.target.value)}
                                >
                                    {roles.map((role) => (
                                        <MenuItem key={role.id} value={role.id}>{role.name}</MenuItem>
                                    ))}
                                </Select>
                            </TableCell>
                            <TableCell>
                                <Button onClick={() => onRemoveUser(user.email)} color="error">
                                    {t('remove')}
                                </Button>
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};

export default UserTable;