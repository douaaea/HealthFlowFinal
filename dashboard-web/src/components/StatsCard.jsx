 
import { Card, CardContent, Typography } from '@mui/material';

function StatsCard({ title, value, color = 'primary' }) {
  return (
    <Card sx={{ bgcolor: `${color}.light`, color: `${color}.contrastText` }}>
      <CardContent>
        <Typography variant="h6" component="div">
          {title}
        </Typography>
        <Typography variant="h4" component="div" sx={{ mt: 2 }}>
          {value}
        </Typography>
      </CardContent>
    </Card>
  );
}

export default StatsCard;
