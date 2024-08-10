import React from 'react';
import { useTranslation } from 'react-i18next';
import AquariumsPage from './screens/AquariumsPage';
import FeedersPage from "./screens/FeedersPage";
import DevicesPage from "./screens/DevicesPage";
import ProfilePage from "./screens/ProfilePage";
import DeviceDetailPage from "./screens/DeviceDetailPage"; // Импортируем новую страницу

import CompanyRequiredWrapper from './components/CompanyRequiredWrapper';
import AquariumIcon from '@mui/icons-material/SetMeal';
import DevicesIcon from '@mui/icons-material/DevicesOther';
import FeederIcon from '@mui/icons-material/Restaurant';
import CompanyManagementPage from "./screens/CompanyManagmentPage";
import BusinessIcon from "@mui/icons-material/Business";

const RouteWrapper = ({ children, pageIcon, translationKey }) => {
    const { t } = useTranslation();
    return (
        <CompanyRequiredWrapper
            pageIcon={pageIcon}
            pageTitle={t(translationKey)}
            pageDescription={t(`${translationKey}Description`)}
        >
            {children}
        </CompanyRequiredWrapper>
    );
};

export const routes = [
    {
        name: 'aquariums',
        path: '/aquariums',
        component: () => (
            <RouteWrapper pageIcon={<AquariumIcon />} translationKey="aquariums">
                <AquariumsPage />
            </RouteWrapper>
        ),
        showInNavigation: true
    },
    {
        name: 'devices',
        path: '/devices',
        component: () => (
            <RouteWrapper pageIcon={<DevicesIcon />} translationKey="devices">
                <DevicesPage />
            </RouteWrapper>
        ),
        showInNavigation: true
    },
    {
        name: 'deviceDetail',
        path: '/devices/aquarium/:aquariumId',
        component: () => (
            <RouteWrapper pageIcon={<DevicesIcon />} translationKey="deviceDetail">
                <DeviceDetailPage />
            </RouteWrapper>
        ),
        showInNavigation: false
    },
    {
        name: 'feeders',
        path: '/feeders',
        component: () => (
            <RouteWrapper pageIcon={<FeederIcon />} translationKey="feeders">
                <FeedersPage />
            </RouteWrapper>
        ),
        showInNavigation: true
    },
    {
        name: 'companyManagement',
        path: '/company-management',
        component: () => (
            <RouteWrapper pageIcon={<BusinessIcon />} translationKey="companyManagement">
                <CompanyManagementPage />
            </RouteWrapper>
        ),
        showInNavigation: true
    },
    { name: 'profile', path: '/profile', component: ProfilePage, showInNavigation: true },
];