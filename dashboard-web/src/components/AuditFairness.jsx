import { useState, useEffect } from 'react';
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
    Skeleton,
    Alert as MuiAlert,
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
import { Gavel, CheckCircle, Warning, Info, Refresh } from '@mui/icons-material';
import { getAuditMetrics, generateFairnessReport } from '../services/api';

export default function AuditFairness() {
    const [metrics, setMetrics] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [generating, setGenerating] = useState(false);

    useEffect(() => {
        loadMetrics();
    }, []);

    const loadMetrics = async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await getAuditMetrics();
            setMetrics(data);
        } catch (err) {
            console.error('Failed to load audit metrics:', err);
            setError('AuditFairness service unavailable. Please ensure the service is running on port 5004.');
        } finally {
            setLoading(false);
        }
    };

    const handleGenerateReport = async () => {
        setGenerating(true);
        try {
            await generateFairnessReport();
            await loadMetrics();
        } catch (err) {
            setError('Failed to generate report');
        } finally {
            setGenerating(false);
        }
    };

    // Fallback data if service unavailable
    const overallFairnessScore = metrics?.overall_score ?? 0;
    const demographicData = metrics?.demographic_analysis ?? [];
    const ageGroupData = metrics?.age_group_analysis ?? [];
    const biasMetrics = metrics?.bias_metrics ?? [];
    const radarData = metrics?.model_dimensions ?? [];
    const recommendations = metrics?.recommendations ?? [];

    if (loading) {
        return (
            <Box>
                <Skeleton variant="text" width={300} height={50} sx={{ mb: 3 }} />
                <Grid container spacing={3}>
                    {[1, 2, 3].map((i) => (
                        <Grid item xs={12} md={4} key={i}>
                            <Skeleton variant="rounded" height={180} sx={{ borderRadius: 4 }} />
                        </Grid>
                    ))}
                </Grid>
            </Box>
        );
    }

    return (
        <Box className="fade-in">
            <Box mb={4} display="flex" justifyContent="space-between" alignItems="center">
                <Box>
                    <Typography variant="h4" fontWeight={700} gutterBottom>
                        Audit Fairness
                    </Typography>
                    <Typography variant="body1" color="text.secondary">
                        AI Fairness and Bias Analysis from EvidentlyAI
                    </Typography>
                </Box>
                <Box display="flex" gap={2}>
                    <Button variant="outlined" startIcon={<Refresh />} onClick={loadMetrics} disabled={loading}>
                        Refresh
                    </Button>
                    <Button 
                        variant="contained" 
                        startIcon={<Gavel />} 
                        onClick={handleGenerateReport}
                        disabled={generating || !!error}
                    >
                        {generating ? 'Generating...' : 'Generate Report'}
                    </Button>
                </Box>
            </Box>

            {error && (
                <MuiAlert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
                    {error}
                </MuiAlert>
            )}

            {!error && metrics && (
                <>
                    {/* Top Cards */}
                    <Grid container spacing={3} mb={4}>
                        <Grid item xs={12} md={4}>
                            <Card sx={{ height: '100%', background: 'linear-gradient(135deg, #0066CC 0%, #004C99 100%)', color: 'white' }}>
                                <CardContent>
                                    <Typography variant="subtitle2" sx={{ opacity: 0.8 }}>Overall Fairness Score</Typography>
                                    <Typography variant="h2" fontWeight={700}>{overallFairnessScore}%</Typography>
                                    <Box mt={2} display="flex" alignItems="center" gap={1}>
                                        <CheckCircle sx={{ fontSize: 20 }} />
                                        <Typography variant="body2">
                                            {overallFairnessScore >= 90 ? 'Model is compliant with regulations' : 'Review recommended'}
                                        </Typography>
                                    </Box>
                                </CardContent>
                            </Card>
                        </Grid>
                        <Grid item xs={12} md={8}>
                            <Card sx={{ height: '100%' }}>
                                <CardContent>
                                    <Typography variant="h6" fontWeight={600} mb={2}>Key Fairness Metrics</Typography>
                                    {biasMetrics.length > 0 ? (
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
                                                        <TableRow key={row.metric}>
                                                            <TableCell>{row.metric}</TableCell>
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
                                    ) : (
                                        <Typography color="text.secondary">No metrics available</Typography>
                                    )}
                                </CardContent>
                            </Card>
                        </Grid>
                    </Grid>

                    {/* Charts Section */}
                    <Grid container spacing={3} mb={4}>
                        <Grid item xs={12} md={6}>
                            <Paper sx={{ p: 3, borderRadius: 2, height: 400 }}>
                                <Typography variant="h6" fontWeight={600} mb={3}>Demographic Analysis (Gender)</Typography>
                                {demographicData.length > 0 ? (
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
                                ) : (
                                    <Box display="flex" alignItems="center" justifyContent="center" height="80%">
                                        <Typography color="text.secondary">No demographic data available</Typography>
                                    </Box>
                                )}
                            </Paper>
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <Paper sx={{ p: 3, borderRadius: 2, height: 400 }}>
                                <Typography variant="h6" fontWeight={600} mb={3}>Age Group Disparity</Typography>
                                {ageGroupData.length > 0 ? (
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
                                ) : (
                                    <Box display="flex" alignItems="center" justifyContent="center" height="80%">
                                        <Typography color="text.secondary">No age group data available</Typography>
                                    </Box>
                                )}
                            </Paper>
                        </Grid>
                    </Grid>

                    {/* Detailed Analysis */}
                    <Grid container spacing={3}>
                        <Grid item xs={12} md={6}>
                            <Paper sx={{ p: 3, borderRadius: 2, height: 400 }}>
                                <Typography variant="h6" fontWeight={600} mb={3}>Model Evaluation Dimensions</Typography>
                                {radarData.length > 0 ? (
                                    <ResponsiveContainer width="100%" height="90%">
                                        <RadarChart outerRadius={90} data={radarData}>
                                            <PolarGrid />
                                            <PolarAngleAxis dataKey="subject" />
                                            <PolarRadiusAxis angle={30} domain={[0, 150]} />
                                            <Radar name="Current Model" dataKey="B" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
                                            <Radar name="Baseline" dataKey="A" stroke="#82ca9d" fill="#82ca9d" fillOpacity={0.6} />
                                            <Legend />
                                        </RadarChart>
                                    </ResponsiveContainer>
                                ) : (
                                    <Box display="flex" alignItems="center" justifyContent="center" height="80%">
                                        <Typography color="text.secondary">No evaluation data available</Typography>
                                    </Box>
                                )}
                            </Paper>
                        </Grid>
                        <Grid item xs={12} md={6}>
                            <Paper sx={{ p: 3, borderRadius: 2, height: 400, display: 'flex', flexDirection: 'column', gap: 2 }}>
                                <Typography variant="h6" fontWeight={600}>Fairness Recommendations</Typography>
                                
                                {recommendations.length > 0 ? (
                                    recommendations.map((rec, idx) => (
                                        <Alert key={idx} severity={rec.severity} icon={rec.severity === 'warning' ? <Warning /> : rec.severity === 'info' ? <Info /> : <CheckCircle />}>
                                            <strong>{rec.title}:</strong> {rec.message}
                                        </Alert>
                                    ))
                                ) : (
                                    <Typography color="text.secondary">No recommendations available</Typography>
                                )}
                                 
                                <Box mt="auto">
                                    <Button variant="contained" fullWidth disabled={!!error}>Run Automated Remediation</Button>
                                </Box>
                            </Paper>
                        </Grid>
                    </Grid>
                </>
            )}

            {error && !metrics && (
                <Box textAlign="center" py={8}>
                    <Typography variant="h6" color="text.secondary" gutterBottom>
                        AuditFairness Service Unavailable
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                        Please ensure the audit-fairness microservice is running on port 5004
                    </Typography>
                    <Button variant="contained" onClick={loadMetrics}>
                        Retry Connection
                    </Button>
                </Box>
            )}
        </Box>
    );
}

function Alert(props) {
    return (
        <Box 
            sx={{ 
                p: 2, 
                borderRadius: 1, 
                border: '1px solid', 
                borderColor: props.severity === 'warning' ? '#ff9800' : props.severity === 'info' ? '#2196f3' : '#4caf50', 
                bgcolor: props.severity === 'warning' ? '#fff3e0' : props.severity === 'info' ? '#e3f2fd' : '#e8f5e9', 
                color: props.severity === 'warning' ? '#e65100' : props.severity === 'info' ? '#0d47a1' : '#1b5e20', 
                display: 'flex', 
                gap: 2, 
                alignItems: 'center' 
            }}
        >
            {props.icon}
            <Box>{props.children}</Box>
        </Box>
    );
}
