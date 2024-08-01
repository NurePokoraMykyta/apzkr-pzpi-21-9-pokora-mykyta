import { createTheme } from '@mui/material/styles';

const theme = createTheme({
    palette: {
        primary: {
            main: '#0099a8',
        },
        secondary: {
            main: '#ffffff',
        },
        background: {
            default: '#ffffff',
            paper: '#f5f5f5',
        },
        text: {
            primary: '#333333',
            secondary: '#666666',
        },
    },
    typography: {
        fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
        h1: {
            fontWeight: 700,
        },
        h2: {
            fontWeight: 700,
        },
        h3: {
            fontWeight: 600,
        },
        button: {
            textTransform: 'none',
        },
    },
    components: {
        MuiButton: {
            styleOverrides: {
                root: {
                    borderRadius: 20,
                    padding: '6px 16px',
                },
                contained: {
                    boxShadow: 'none',
                },
            },
        },
        MuiAppBar: {
            styleOverrides: {
                root: {
                    backgroundColor: '#ffffff',
                    color: '#333333',
                    boxShadow: 'none',
                    borderBottom: '1px solid #e0e0e0',
                },
            },
        },
        MuiCard: {
            styleOverrides: {
                root: {
                    boxShadow: 'none',
                    border: '1px solid #e0e0e0',
                },
            },
        },
    },
});

export default theme;