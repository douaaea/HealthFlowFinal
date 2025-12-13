 
import { useEffect, useState } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Chip,
  Box,
  CircularProgress,
} from '@mui/material';
import { CheckCircle, Error } from '@mui/icons-material';
import { checkHealth } from '../services/api';

function HealthStatus() {
  const [statuses, setStatuses] = useState({
    fhir: null,
    deid: null,
    features: null,
    predictions: null,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHealthStatus();
    const interval = setInterval(loadHealthStatus, 30000); // Refresh every 30s
    return () => clearInterval(interval);
  }, []);

  const loadHealthStatus = async () => {
    const services = ['fhir', 'deid', 'features', 'predictions'];
    const results = {};

    for (const service of services) {
      try {
        const response = await checkHealth(service);
        results[service] = { status: 'UP', data: response };
      } catch (error) {
        results[service] = { status: 'DOWN', error: error.message };
      }
    }

    setStatuses(results);
    setLoading(false);
  };

  if (loading) {
    return <CircularProgress />;
  }

  const ServiceCard = ({ name, displayName, status }) => (
    <Card>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="h6">{displayName}</Typography>
          <Chip
            icon={status?.status === 'UP' ? <CheckCircle /> : <Error />}
            label={status?.status || 'UNKNOWN'}
            color={status?.status === 'UP' ? 'success' : 'error'}
          />
        </Box>
        {status?.data && (
          <Box sx={{ mt: 2 }}>
            <Typography variant="body2" color="text.secondary">
              {JSON.stringify(status.data, null, 2)}
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Microservices Health Status
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <ServiceCard
            name="fhir"
            displayName="ProxyFHIR Service"
            status={statuses.fhir}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <ServiceCard
            name="deid"
            displayName="DeID Service"
            status={statuses.deid}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <ServiceCard
            name="features"
            displayName="Featurizer Service"
            status={statuses.features}
          />
        </Grid>
        <Grid item xs={12} md={6}>
          <ServiceCard
            name="predictions"
            displayName="ML Predictor Service"
            status={statuses.predictions}
          />
        </Grid>
      </Grid>
    </div>
  );
}

export default HealthStatus;
