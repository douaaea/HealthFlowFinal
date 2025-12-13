 
import {
  Card,
  CardContent,
  Typography,
  Chip,
  Box,
  Divider,
} from '@mui/material';
import {
  Person,
  Cake,
  FitnessCenter,
  Favorite,
  Warning,
} from '@mui/icons-material';

function PatientCard({ patient }) {
  const getRiskColor = (category) => {
    switch (category) {
      case 'low':
        return 'success';
      case 'moderate':
        return 'warning';
      case 'high':
        return 'error';
      default:
        return 'default';
    }
  };

  const demographics = patient.demographics || {};
  const vitals = patient.vitals || {};
  const labs = patient.labs || {};
  const prediction = patient.prediction || {};

  return (
    <Card>
      <CardContent>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h6" component="div" noWrap>
            <Person sx={{ mr: 1, verticalAlign: 'middle' }} />
            {patient.patient_id.substring(0, 8)}...
          </Typography>
          {prediction.risk_category && (
            <Chip
              label={prediction.risk_category.toUpperCase()}
              color={getRiskColor(prediction.risk_category)}
              size="small"
            />
          )}
        </Box>

        <Divider sx={{ mb: 2 }} />

        <Box sx={{ mb: 1 }}>
          <Typography variant="body2" color="text.secondary">
            <Cake sx={{ fontSize: 16, mr: 1, verticalAlign: 'middle' }} />
            Age: {demographics.age || 'N/A'} | Gender: {demographics.gender || 'N/A'}
          </Typography>
        </Box>

        <Box sx={{ mb: 1 }}>
          <Typography variant="body2" color="text.secondary">
            <FitnessCenter sx={{ fontSize: 16, mr: 1, verticalAlign: 'middle' }} />
            BMI: {vitals.bmi?.toFixed(1) || 'N/A'} | BP: {vitals.avg_systolic_bp?.toFixed(0) || 'N/A'}/{vitals.avg_diastolic_bp?.toFixed(0) || 'N/A'}
          </Typography>
        </Box>

        <Box sx={{ mb: 1 }}>
          <Typography variant="body2" color="text.secondary">
            <Favorite sx={{ fontSize: 16, mr: 1, verticalAlign: 'middle' }} />
            Cholesterol: {labs.avg_cholesterol?.toFixed(0) || 'N/A'} | HDL: {labs.avg_hdl?.toFixed(0) || 'N/A'}
          </Typography>
        </Box>

        {prediction.framingham_score !== undefined && (
          <Box sx={{ mt: 2, p: 1, bgcolor: 'grey.100', borderRadius: 1 }}>
            <Typography variant="body2" fontWeight="bold">
              <Warning sx={{ fontSize: 16, mr: 1, verticalAlign: 'middle', color: 'warning.main' }} />
              Framingham Risk: {prediction.framingham_score}%
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
}

export default PatientCard;
