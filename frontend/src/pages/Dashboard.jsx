import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  CircularProgress,
  Card,
  CardContent,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Divider
} from '@mui/material';
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell,
  Area,
  AreaChart
} from 'recharts';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import { getStats, getTopEntreprises, getEvolution } from '../services/api';

// Correction pour les icônes Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82ca9d', '#ffc658', '#8dd1e1'];

const KPICard = ({ title, value, subtitle, color }) => (
  <Card sx={{ height: '100%', background: `linear-gradient(135deg, ${color} 0%, ${color}dd 100%)`, color: 'white' }}>
    <CardContent>
      <Typography variant="h6" gutterBottom>{title}</Typography>
      <Typography variant="h3" component="div">{value}</Typography>
      {subtitle && <Typography variant="body2">{subtitle}</Typography>}
    </CardContent>
  </Card>
);

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState(null);
  const [entreprises, setEntreprises] = useState([]);
  const [evolution, setEvolution] = useState([]);
  const [timeRange, setTimeRange] = useState('6mois');

  // Données simulées pour les graphiques (à remplacer par les vraies données API)
  const [secteursData, setSecteursData] = useState([]);
  const [contratsData, setContratsData] = useState([]);
  const [villesData, setVillesData] = useState([]);
  const [competencesData, setCompetencesData] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [statsRes, entreprisesRes, evolutionRes] = await Promise.all([
        getStats(),
        getTopEntreprises(),
        getEvolution()
      ]);

      setStats(statsRes.data);
      setEntreprises(entreprisesRes.data || []);
      setEvolution(evolutionRes.data || []);

      // Données simulées en attendant les vraies APIs
      setSecteursData([
        { nom: 'Informatique / IT', offres: 145 },
        { nom: 'Logistique / Transport', offres: 98 },
        { nom: 'Commercial / Vente', offres: 87 },
        { nom: 'RH / Administration', offres: 65 },
        { nom: 'Marketing / Communication', offres: 54 },
        { nom: 'Finance / Comptabilité', offres: 43 },
        { nom: 'Ingénierie', offres: 38 },
        { nom: 'Santé', offres: 22 }
      ]);

      setContratsData([
        { nom: 'CDI', valeur: 45 },
        { nom: 'CDD', valeur: 38 },
        { nom: 'Stage', valeur: 12 },
        { nom: 'Freelance', valeur: 5 }
      ]);

      setVillesData([
        { nom: 'Dakar', offres: 320, lat: 14.7167, lng: -17.4677 },
        { nom: 'Thiès', offres: 85, lat: 14.7833, lng: -16.9167 },
        { nom: 'Saint-Louis', offres: 42, lat: 16.0333, lng: -16.5 },
        { nom: 'Ziguinchor', offres: 28, lat: 12.5833, lng: -16.2667 },
        { nom: 'Kaolack', offres: 25, lat: 14.0167, lng: -16.25 },
        { nom: 'Mbour', offres: 23, lat: 14.4167, lng: -16.9667 }
      ]);

      setCompetencesData([
        { nom: 'Gestion de projet', count: 156 },
        { nom: 'Communication', count: 142 },
        { nom: 'Leadership', count: 128 },
        { nom: 'Anglais', count: 115 },
        { nom: 'Bureautique', count: 98 },
        { nom: 'Analyse de données', count: 87 },
        { nom: 'Service client', count: 76 },
        { nom: 'Travail d\'équipe', count: 72 },
        { nom: 'Rigueur', count: 68 },
        { nom: 'Résolution de problèmes', count: 65 }
      ]);

    } catch (error) {
      console.error('Erreur chargement données:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterEvolutionData = () => {
    if (!evolution.length) return [];
    const months = timeRange === '3mois' ? 3 : timeRange === '6mois' ? 6 : 12;
    return evolution.slice(-months);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold' }}>
        📊 Tableau de Bord - Analyse du Marché de l'Emploi
      </Typography>
      <Typography variant="subtitle1" color="textSecondary" gutterBottom>
        Sénégal • Données mises à jour quotidiennement
      </Typography>
      <Divider sx={{ mb: 4 }} />

      {/* KPIs */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="Total Offres"
            value={stats?.total_offres || 523}
            subtitle="Offres analysées"
            color="#1976d2"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="Secteur Leader"
            value="Informatique"
            subtitle="145 offres"
            color="#2e7d32"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="Ville Leader"
            value="Dakar"
            subtitle="320 offres"
            color="#ed6c02"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="Croissance"
            value="+12.5%"
            subtitle="vs mois dernier"
            color="#9c27b0"
          />
        </Grid>
      </Grid>

      {/* Première ligne de graphiques */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {/* Offres par secteur */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Offres par Secteur d'Activité
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={secteursData} layout="vertical" margin={{ left: 100 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="nom" type="category" width={100} />
                <Tooltip />
                <Bar dataKey="offres" fill="#1976d2">
                  {secteursData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Répartition par type de contrat */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Répartition par Type de Contrat
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={contratsData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ nom, percent }) => `${nom} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="valeur"
                >
                  {contratsData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>

      {/* Deuxième ligne - Évolution */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
              <Typography variant="h6">
                Évolution du Nombre d'Offres
              </Typography>
              <FormControl size="small" sx={{ minWidth: 120 }}>
                <InputLabel>Période</InputLabel>
                <Select
                  value={timeRange}
                  label="Période"
                  onChange={(e) => setTimeRange(e.target.value)}
                >
                  <MenuItem value="3mois">3 derniers mois</MenuItem>
                  <MenuItem value="6mois">6 derniers mois</MenuItem>
                  <MenuItem value="12mois">12 derniers mois</MenuItem>
                </Select>
              </FormControl>
            </Box>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={evolution.length ? filterEvolutionData() : [
                { mois: 'Jan', offres: 65 },
                { mois: 'Fév', offres: 78 },
                { mois: 'Mar', offres: 82 },
                { mois: 'Avr', offres: 95 },
                { mois: 'Mai', offres: 88 },
                { mois: 'Juin', offres: 102 }
              ]}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="mois" />
                <YAxis />
                <Tooltip />
                <Area type="monotone" dataKey="offres" stroke="#1976d2" fill="#1976d250" />
              </AreaChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
      </Grid>

      {/* Troisième ligne - Compétences et Villes */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {/* Top compétences */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Top 10 Compétences Demandées
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={competencesData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="nom" angle={-45} textAnchor="end" height={80} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#2e7d32">
                  {competencesData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={`hsl(${index * 35}, 70%, 50%)`} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>

        {/* Top entreprises */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Top Entreprises qui Recrutent
            </Typography>
            <Box sx={{ mt: 2 }}>
              {entreprises.length > 0 ? entreprises.map((entreprise, index) => (
                <Box
                  key={index}
                  sx={{
                    display: 'flex',
                    alignItems: 'center',
                    mb: 2,
                    p: 1,
                    borderRadius: 1,
                    '&:hover': { backgroundColor: '#f5f5f5' }
                  }}
                >
                  <Typography
                    variant="body1"
                    sx={{
                      minWidth: 30,
                      fontWeight: 'bold',
                      color: index < 3 ? '#ed6c02' : 'text.secondary'
                    }}
                  >
                    #{index + 1}
                  </Typography>
                  <Typography variant="body1" sx={{ flex: 1 }}>
                    {entreprise.entreprise}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    {entreprise.count} offres
                  </Typography>
                </Box>
              )) : (
                // Données simulées si pas de données réelles
                [
                  { entreprise: 'La Laiterie du Berger', count: 8 },
                  { entreprise: 'GBG', count: 6 },
                  { entreprise: 'Maersk', count: 5 },
                  { entreprise: 'UNICEF', count: 4 },
                  { entreprise: 'AnyVan', count: 3 }
                ].map((entreprise, index) => (
                  <Box
                    key={index}
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      mb: 2,
                      p: 1,
                      borderRadius: 1,
                      '&:hover': { backgroundColor: '#f5f5f5' }
                    }}
                  >
                    <Typography
                      variant="body1"
                      sx={{
                        minWidth: 30,
                        fontWeight: 'bold',
                        color: index < 3 ? '#ed6c02' : 'text.secondary'
                      }}
                    >
                      #{index + 1}
                    </Typography>
                    <Typography variant="body1" sx={{ flex: 1 }}>
                      {entreprise.entreprise}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      {entreprise.count} offres
                    </Typography>
                  </Box>
                ))
              )}
            </Box>
          </Paper>
        </Grid>
      </Grid>

      {/* Carte géographique */}
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Répartition Géographique des Offres
            </Typography>
            <Box sx={{ height: 400, width: '100%', borderRadius: 2, overflow: 'hidden' }}>
              <MapContainer
                center={[14.7167, -17.4677]}
                zoom={7}
                style={{ height: '100%', width: '100%' }}
              >
                <TileLayer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                />
                {villesData.map((ville, index) => (
                  <Marker
                    key={index}
                    position={[ville.lat, ville.lng]}
                  >
                    <Popup>
                      <strong>{ville.nom}</strong><br />
                      {ville.offres} offres d'emploi
                    </Popup>
                  </Marker>
                ))}
              </MapContainer>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;