import { useState } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import {
  AppBar,
  Toolbar,
  Typography,
  Container,
  Box,
  Tabs,
  Tab,
} from '@mui/material';
import Dashboard from './components/Dashboard';
import PatientList from './components/PatientList';
import HealthStatus from './components/HealthStatus';
import Pipeline from './components/Pipeline';  // NOUVEAU

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function TabPanel({ children, value, index }) {
  return (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

function App() {
  const [activeTab, setActiveTab] = useState(0);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            HealthFlow - Dashboard
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ mt: 4 }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={activeTab} onChange={handleTabChange}>
            <Tab label="Dashboard" />
            <Tab label="Patients" />
            <Tab label="Pipeline" />      {/* NOUVEAU */}
            <Tab label="Health Status" />
          </Tabs>
        </Box>

        <TabPanel value={activeTab} index={0}>
          <Dashboard />
        </TabPanel>
        <TabPanel value={activeTab} index={1}>
          <PatientList />
        </TabPanel>
        <TabPanel value={activeTab} index={2}>
          <Pipeline />                    {/* NOUVEAU */}
        </TabPanel>
        <TabPanel value={activeTab} index={3}>
          <HealthStatus />
        </TabPanel>
      </Container>
    </ThemeProvider>
  );
}

export default App;
