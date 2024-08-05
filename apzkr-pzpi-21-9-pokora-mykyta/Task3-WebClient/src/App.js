import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import Header from './components/Header';
import LandingPage from './screens/LandingPage';
import { routes } from './routes';
import theme from "./theme";
import {ThemeProvider} from "@mui/material";
import {CompanyProvider} from "./contexts/CompanyContext";

function App() {
    return (
        <Router>
            <AuthProvider>
                <CompanyProvider>
                    <ThemeProvider theme={theme}>
                        <Header />
                        <Routes>
                            <Route path="/" element={<LandingPage />} />
                            {routes.map((route) => (
                                <Route key={route.path} path={route.path} element={<route.component />} />
                            ))}
                        </Routes>
                    </ThemeProvider>
                </CompanyProvider>
            </AuthProvider>

        </Router>
    );
}

export default App;