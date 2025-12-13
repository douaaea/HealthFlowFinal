import { useEffect, useState } from 'react';
import { Grid, Card, CardContent, Typography, Button, CircularProgress } from '@mui/material';
import { getFeatureStats, getPredictionStats, extractFeatures, predictRisks } from '../services/api';
import StatsCard from './StatsCard';
import RiskChart from './RiskChart';

function Dashboard() {
  const [featureStats, setFeatureStats] = useState(null);
  const [predictionStats, setPredictionStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const [features, predictions] = await Promise.all([
        getFeatureStats(),
        getPredictionStats(),
      ]);
      setFeatureStats(features);
      setPredictionStats(predictions);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleExtractFeatures = async () => {
    setProcessing(true);
    try {
      await extractFeatures();
      alert('Features extracted successfully!');
      loadData();
    } catch (error) {
      alert('Error extracting features');
    } finally {
      setProcessing(false);
    }
  };

  const handlePredictRisks = async () => {
    setProcessing(true);
    try {
      await predictRisks();
      alert('Risks predicted successfully!');
      loadData();
    } catch (error) {
      alert('Error predicting risks');
    } finally {
      setProcessing(false);
    }
  };

  if (loading) {
    return <CircularProgress />;
  }

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        HealthFlow Dashboard
      </Typography>

      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={6}>
          <Button
            variant="contained"
            fullWidth
            onClick={handleExtractFeatures}
            disabled={processing}
          >
            Extract Features
          </Button>
        </Grid>
        <Grid item xs={12} md={6}>
          <Button
            variant="contained"
            color="secondary"
            fullWidth
            onClick={handlePredictRisks}
            disabled={processing}
          >
            Predict Risks
          </Button>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <StatsCard
            title="Total Patients"
            value={featureStats?.total_patients || 0}
            color="primary"
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <StatsCard
            title="Average Age"
            value={featureStats?.average_age || 'N/A'}
            color="info"
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <StatsCard
            title="Average BMI"
            value={featureStats?.average_bmi?.toFixed(2) || 'N/A'}
            color="warning"
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <StatsCard
            title="Avg Cholesterol"
            value={featureStats?.average_cholesterol?.toFixed(1) || 'N/A'}
            color="success"
          />
        </Grid>
      </Grid>

      <Grid container spacing={3} sx={{ mt: 3 }}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Risk Distribution
              </Typography>
              <RiskChart data={predictionStats?.risk_distribution || {}} />
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Prediction Statistics
              </Typography>
              <Typography>
                Total Predictions: {predictionStats?.total_predictions || 0}
              </Typography>
              <Typography>
                Avg Framingham Score: {predictionStats?.average_framingham_score?.toFixed(2) || 'N/A'}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </div>
  );
}

export default Dashboard;
 
