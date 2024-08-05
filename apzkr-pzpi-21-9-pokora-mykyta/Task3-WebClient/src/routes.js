import React from 'react';
import { useTranslation } from 'react-i18next';
import AquariumsPage from './screens/AquariumsPage';
import FeedersPage from "./screens/FeedersPage";
import DevicesPage from "./screens/DevicesPage";
import BlogPage from "./screens/BlogPage";
import ProfilePage from "./screens/ProfilePage";

import CompanyRequiredWrapper from './components/CompanyRequiredWrapper';
import AquariumIcon from '@mui/icons-material/SetMeal';
import DevicesIcon from '@mui/icons-material/DevicesOther';
import FeederIcon from '@mui/icons-material/Restaurant';

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
        )
    },
    {
        name: 'devices',
        path: '/devices',
        component: () => (
            <RouteWrapper pageIcon={<DevicesIcon />} translationKey="devices">
                <DevicesPage />
            </RouteWrapper>
        )
    },
    {
        name: 'feeders',
        path: '/feeders',
        component: () => (
            <RouteWrapper pageIcon={<FeederIcon />} translationKey="feeders">
                <FeedersPage />
            </RouteWrapper>
        )
    },
    { name: 'blog', path: '/blog', component: BlogPage },
    { name: 'profile', path: '/profile', component: ProfilePage },
];