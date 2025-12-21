import React, { useState } from 'react';
import {
    Box,
    Typography,
    Grid,
    Paper,
    Card,
    CardContent,
    Button,
    Chip,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    LinearProgress,
} from '@mui/material';
import {
    ResponsiveContainer,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    RadarChart,
    PolarGrid,
    PolarAngleAxis,
    PolarRadiusAxis,
    Radar,
} from 'recharts';
import { Gavel, CheckCircle, Warning, Info } from '@mui/icons-material';

// Mock Data
const overallFairnessScore = 92;

const demographicData = [
    { group: 'Male', approvalRate: 85, errorRate: 15 },
    { group: 'Female', approvalRate: 83, errorRate: 17 },
    { group: 'Other', approvalRate: 80, errorRate: 20 },
];

const ageGroupData = [
    { group: '18-30', approvalRate: 88, errorRate: 12 },
    { group: '31-50', approvalRate: 86, errorRate: 14 },
    { group: '51-70', approvalRate: 82, errorRate: 18 },
    { group: '71+', approvalRate: 78, errorRate: 22 },
];

const biasMetrics = [
    { metric: 'Demographic Parity', value: 0.95, threshold: 0.9, status: 'pass' },
    { metric: 'Equal Opportunity', value: 0.92, threshold: 0.9, status: 'pass' },
    { metric: 'Predictive Parity', value: 0.88, threshold: 0.9, status: 'warning' },
    { metric: 'False Positive Rate Parity', value: 0.96, threshold: 0.9, status: 'pass' },
    { metric: 'Disparate Impact', value: 0.91, threshold: 0.8, status: 'pass' },
];

const radarData = [
    { subject: 'Accuracy', A: 120, B: 110, fullMark: 150 },
    { subject: 'Fairness', A: 98, B: 130, fullMark: 150 },
    { subject: 'Robustness', A: 86, B: 130, fullMark: 150 },
    { subject: 'Explainability', A: 99, B: 100, fullMark: 150 },
    { subject: 'Privacy', A: 85, B: 90, fullMark: 150 },
    { subject: 'Efficiency', A: 65, B: 85, fullMark: 150 },
];

export default function AuditFairness() {
    return (
        <Box className="fade-in">
            <Box mb={4} display="flex" justifyContent="space-between" alignItems="center">
                <Box>
                    <Typography variant="h4" fontWeight={700} gutterBottom>
                        Audit Fairness
                    </Typography>
                    <Typography variant="body1" color="text.secondary">
                        Comprehensive AI Fairness and Bias Analysis
                    </Typography>
                </Box>
                <Button variant="outlined" startIcon={<Gavel />}>
                    Generate Report
                </Button>
            </Box>

            {/* Top Cards */}
            <Grid container spacing={3} mb={4}>
                <Grid item xs={12} md={4}>
                    <Card sx={{ height: '100%', background: 'linear-gradient(135deg, #0066CC 0%, #004C99 100%)', color: 'white' }}>
                        <CardContent>
                            <Typography variant="subtitle2" sx={{ opacity: 0.8 }}>Overall Fairness Score</Typography>
                            <Typography variant="h2" fontWeight={700}>{overallFairnessScore}%</Typography>
                            <Box mt={2} display="flex" alignItems="center" gap={1}>
                                <CheckCircle sx={{ fontSize: 20 }} />
                                <Typography variant="body2">Model is compliant with regulations</Typography>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={12} md={8}>
                    <Card sx={{ height: '100%' }}>
                        <CardContent>
                            <Typography variant="h6" fontWeight={600} mb={2}>Key Fairness Metrics</Typography>
                            <TableContainer>
                                <Table size="small">
                                    <TableHead>
                                        <TableRow>
                                            <TableCell>Metric</TableCell>
                                            <TableCell align="right">Value</TableCell>
                                            <TableCell align="right">Threshold</TableCell>
                                            <TableCell align="center">Status</TableCell>
                                        </TableRow>
                                    </TableHead>
                                    <TableBody>
                                        {biasMetrics.map((row) => (
                                            <TableRow key={row.metric} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                                <TableCell component="th" scope="row">{row.metric}</TableCell>
                                                <TableCell align="right">{row.value}</TableCell>
                                                <TableCell align="right">{row.threshold}</TableCell>
                                                <TableCell align="center">
                                                    <Chip 
                                                        label={row.status.toUpperCase()} 
                                                        color={row.status === 'pass' ? 'success' : row.status === 'warning' ? 'warning' : 'error'} 
                                                        size="small" 
                                                        sx={{ fontWeight: 600, minWidth: 80 }}
                                                    />
                                                </TableCell>
                                            </TableRow>
                                        ))}
                                    </TableBody>
                                </Table>
                            </TableContainer>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            {/* Charts Section */}
            <Grid container spacing={3} mb={4}>
                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 3, borderRadius: 2, height: 400 }}>
                        <Typography variant="h6" fontWeight={600} mb={3}>Demographic Analysis (Gender)</Typography>
                        <ResponsiveContainer width="100%" height="90%">
                            <BarChart data={demographicData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis dataKey="group" />
                                <YAxis />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey="approvalRate" name="Approval Rate (%)" fill="#0088FE" />
                                <Bar dataKey="errorRate" name="Error Rate (%)" fill="#FF8042" />
                            </BarChart>
                        </ResponsiveContainer>
                    </Paper>
                </Grid>
                <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 3, borderRadius: 2, height: 400 }}>
                        <Typography variant="h6" fontWeight={600} mb={3}>Age Group Disparity</Typography>
                        <ResponsiveContainer width="100%" height="90%">
                            <BarChart data={ageGroupData} layout="vertical" margin={{ top: 20, right: 30, left: 40, bottom: 5 }}>
                                <CartesianGrid strokeDasharray="3 3" />
                                <XAxis type="number" />
                                <YAxis dataKey="group" type="category" />
                                <Tooltip />
                                <Legend />
                                <Bar dataKey="approvalRate" name="Approval Rate (%)" fill="#82ca9d" />
                            </BarChart>
                        </ResponsiveContainer>
                    </Paper>
                </Grid>
            </Grid>

            {/* Detailed Analysis */}
            <Grid container spacing={3}>
                 <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 3, borderRadius: 2, height: 400 }}>
                        <Typography variant="h6" fontWeight={600} mb={3}>Model Evaluation Dimensions</Typography>
                         <ResponsiveContainer width="100%" height="90%">
                            <RadarChart outerRadius={90} width={730} height={250} data={radarData}>
                              <PolarGrid />
                              <PolarAngleAxis dataKey="subject" />
                              <PolarRadiusAxis angle={30} domain={[0, 150]} />
                              <Radar name="Current Model" dataKey="B" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
                              <Radar name="Baseline" dataKey="A" stroke="#82ca9d" fill="#82ca9d" fillOpacity={0.6} />
                              <Legend />
                            </RadarChart>
                          </ResponsiveContainer>
                    </Paper>
                 </Grid>
                 <Grid item xs={12} md={6}>
                    <Paper sx={{ p: 3, borderRadius: 2, height: 400, display: 'flex', flexDirection: 'column', gap: 2 }}>
                        <Typography variant="h6" fontWeight={600}>Fairness Recommendations</Typography>
                        
                        <Alert severity="warning" icon={<Warning />}>
                             <strong>Predictive Parity Warning:</strong> The model shows a slight disparity in predictive accuracy for the '51-70' age group. Consider re-balancing the training dataset.
                        </Alert>
                         <Alert severity="info" icon={<Info />}>
                             <strong>Data Augmentation:</strong> Increasing the sample size for minority groups improved the Disparate Impact score by 5% in the last iteration.
                        </Alert>
                         <Alert severity="success" icon={<CheckCircle />}>
                             <strong>Gender Bias:</strong> No significant gender bias detected across all metrics.
                        </Alert>
                         
                         <Box mt="auto">
                             <Button variant="contained" fullWidth>Run Automated Remediation</Button>
                         </Box>
                    </Paper>
                 </Grid>
            </Grid>
            
        </Box>
    );
}

function Alert(props) {
    return <Box sx={{ p: 2, borderRadius: 1, border: '1px solid', borderColor: props.severity === 'warning' ? '#ff9800' : props.severity === 'info' ? '#2196f3' : '#4caf50', bgcolor: props.severity === 'warning' ? '#fff3e0' : props.severity === 'info' ? '#e3f2fd' : '#e8f5e9', color: props.severity === 'warning' ? '#e65100' : props.severity === 'info' ? '#0d47a1' : '#1b5e20', display: 'flex', gap: 2, alignItems: 'center' }}>{props.icon}<Box>{props.children}</Box></Box>
}
