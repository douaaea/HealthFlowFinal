 
import { useEffect, useState } from 'react';
import {
  Grid,
  Typography,
  CircularProgress,
  Alert,
} from '@mui/material';
import { getFeatures, getPredictions } from '../services/api';
import PatientCard from './PatientCard';

function PatientList() {
  const [patients, setPatients] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadPatients();
  }, []);

  const loadPatients = async () => {
    setLoading(true);
    try {
      const [featuresData, predictionsData] = await Promise.all([
        getFeatures(),
        getPredictions(),
      ]);

      // Combiner les features et les prédictions
      const featuresMap = new Map(
        featuresData.features.map(f => [f.patient_id, f])
      );
      const predictionsMap = new Map(
        predictionsData.predictions.map(p => [p.patient_id, p])
      );

      const combinedPatients = featuresData.features.map(feature => ({
        ...feature,
        prediction: predictionsMap.get(feature.patient_id),
      }));

      setPatients(combinedPatients);
    } catch (err) {
      setError('Error loading patients');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <CircularProgress />;
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Patient List ({patients.length})
      </Typography>

      <Grid container spacing={3}>
        {patients.map((patient) => (
          <Grid item xs={12} md={6} lg={4} key={patient.patient_id}>
            <PatientCard patient={patient} />
          </Grid>
        ))}
      </Grid>

      {patients.length === 0 && (
        <Alert severity="info">No patients found. Extract features first.</Alert>
      )}
    </div>
  );
}

export default PatientList;
