// src/pages/Dashboard.jsx
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
  Divider,
  Alert
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
import {
  getStats,
  getTopEntreprises,
  getEvolution,
  getCompetences,
  getSecteurs,
  getVilles,
  getContrats
} from '../services/api';

// Correction pour les icônes Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82ca9d', '#ffc658', '#8dd1e1'];

const KPICard = ({ title, value, subtitle, color }) => (
  <Card sx={{ height: '100%', background: `linear-gradient(135deg, ${color} 30%, ${color}dd 90%)`, color: 'white' }}>
    <CardContent>
      <Typography variant="h6" gutterBottom>{title}</Typography>
      <Typography variant="h3" component="div">{value}</Typography>
      {subtitle && <Typography variant="body2">{subtitle}</Typography>}
    </CardContent>
  </Card>
);

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // États pour les données
  const [stats, setStats] = useState(null);
  const [entreprises, setEntreprises] = useState([]);
  const [evolution, setEvolution] = useState([]);
  const [competences, setCompetences] = useState([]);
  const [secteurs, setSecteurs] = useState([]);
  const [villes, setVilles] = useState([]);
  const [contrats, setContrats] = useState([]);
  
  const [timeRange, setTimeRange] = useState('6mois');

  // Coordonnées approximatives des villes sénégalaises
  const villesCoords = {
    'Dakar': [14.7167, -17.4677],
    'Thiès': [14.7833, -16.9167],
    'Saint-Louis': [16.0333, -16.5],
    'Ziguinchor': [12.5833, -16.2667],
    'Kaolack': [14.0167, -16.25],
    'Mbour': [14.4167, -16.9667],
    'Louga': [15.6167, -16.2167],
    'Tambacounda': [13.7667, -13.6667],
    'Kolda': [12.8833, -14.95],
    'Matam': [15.6167, -13.3167],
    'Kédougou': [12.55, -12.1833],
    'Sédhiou': [12.7, -15.55],
    'Diourbel': [14.65, -16.2333],
    'Fatick': [14.3333, -16.4167],
    'Kaffrine': [14.1, -15.55]
  };

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      console.log('Chargement des données du dashboard...');
      
      // Lancer toutes les requêtes en parallèle
      const [
        statsRes,
        entreprisesRes,
        evolutionRes,
        competencesRes,
        secteursRes,
        villesRes,
        contratsRes
      ] = await Promise.allSettled([
        getStats(),
        getTopEntreprises(),
        getEvolution(),
        getCompetences(),
        getSecteurs(),
        getVilles(),
        getContrats()
      ]);

      // Traiter les résultats
      if (statsRes.status === 'fulfilled') {
        console.log('Stats reçues:', statsRes.value.data);
        setStats(statsRes.value.data);
      } else {
        console.error('Erreur stats:', statsRes.reason);
      }

      if (entreprisesRes.status === 'fulfilled') {
        console.log('Entreprises reçues:', entreprisesRes.value.data);
        setEntreprises(entreprisesRes.value.data);
      }

      if (evolutionRes.status === 'fulfilled') {
        console.log('Evolution reçue:', evolutionRes.value.data);
        setEvolution(evolutionRes.value.data);
      }

      if (competencesRes.status === 'fulfilled') {
        console.log('Compétences reçues:', competencesRes.value.data);
        // Prendre les compétences structurées ou libres selon ce qui est disponible
        const data = competencesRes.value.data;
        if (data.competences_structurees) {
          setCompetences(data.competences_structurees);
        } else if (Array.isArray(data)) {
          setCompetences(data);
        }
      }

      if (secteursRes.status === 'fulfilled') {
        console.log('Secteurs reçus:', secteursRes.value.data);
        setSecteurs(secteursRes.value.data);
      }

      if (villesRes.status === 'fulfilled') {
        console.log('Villes reçues:', villesRes.value.data);
        setVilles(villesRes.value.data);
      }

      if (contratsRes.status === 'fulfilled') {
        console.log('Contrats reçus:', contratsRes.value.data);
        setContrats(contratsRes.value.data);
      }

    } catch (error) {
      console.error('Erreur globale:', error);
      setError('Erreur lors du chargement des données');
    } finally {
      setLoading(false);
    }
  };

  const filterEvolutionData = () => {
    if (!evolution || evolution.length === 0) return [];
    
    const months = timeRange === '3mois' ? 3 : timeRange === '6mois' ? 6 : 12;
    return evolution.slice(-months);
  };

  // Préparer les données pour les graphiques
  const prepareSecteursData = () => {
    if (!secteurs || secteurs.length === 0) return [];
    return secteurs.slice(0, 8).map(s => ({
      nom: s.secteur || 'Non spécifié',
      offres: s.count || 0
    }));
  };

  const prepareContratsData = () => {
    if (!contrats || contrats.length === 0) return [];
    return contrats.map(c => ({
      nom: c.type_contrat || 'Non spécifié',
      valeur: c.count || 0
    }));
  };

  const prepareVillesData = () => {
    if (!villes || villes.length === 0) return [];
    return villes.slice(0, 10).map(v => ({
      nom: v.ville || 'Non spécifié',
      offres: v.count || 0,
      lat: villesCoords[v.ville] ? villesCoords[v.ville][0] : 14.7167,
      lng: villesCoords[v.ville] ? villesCoords[v.ville][1] : -17.4677
    }));
  };

  const prepareCompetencesData = () => {
    if (!competences || competences.length === 0) return [];
    return competences.slice(0, 10).map(c => ({
      nom: c.nom || c.competence || 'Non spécifié',
      count: c.count || 0
    }));
  };

  const prepareEntreprisesData = () => {
    if (!entreprises || entreprises.length === 0) return [];
    return entreprises.slice(0, 5);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  const secteursData = prepareSecteursData();
  const contratsData = prepareContratsData();
  const villesData = prepareVillesData();
  const competencesData = prepareCompetencesData();
  const entreprisesData = prepareEntreprisesData();
  const evolutionData = filterEvolutionData();

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold' }}>
        📊 Tableau de Bord - Analyse du Marché de l'Emploi
      </Typography>
      <Typography variant="subtitle1" color="textSecondary" gutterBottom>
        Sénégal • Données mises à jour quotidiennement
      </Typography>
      <Divider sx={{ mb: 4 }} />

      {/* KPIs avec vraies données */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="Total Offres"
            value={stats?.total_offres?.toLocaleString() || '0'}
            subtitle="Offres analysées"
            color="#1976d2"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="Secteur Leader"
            value={stats?.secteur_dominant?.secteur || 'N/A'}
            subtitle={stats?.secteur_dominant ? `${stats.secteur_dominant.count} offres` : 'Aucune donnée'}
            color="#2e7d32"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="Ville Leader"
            value={stats?.ville_top?.ville || 'N/A'}
            subtitle={stats?.ville_top ? `${stats.ville_top.count} offres` : 'Aucune donnée'}
            color="#ed6c02"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="Croissance"
            value={`${stats?.croissance_mensuelle > 0 ? '+' : ''}${stats?.croissance_mensuelle || 0}%`}
            subtitle="vs mois précédent"
            color="#9c27b0"
          />
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
            {competencesData.length > 0 ? (
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
            ) : (
              <Typography color="textSecondary" align="center" sx={{ py: 10 }}>
                Aucune donnée de compétences disponible
              </Typography>
            )}
          </Paper>
        </Grid>

        {/* Top entreprises */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Top Entreprises qui Recrutent
            </Typography>
            {entreprisesData.length > 0 ? (
              <Box sx={{ mt: 2 }}>
                {entreprisesData.map((entreprise, index) => (
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
                ))}
              </Box>
            ) : (
              <Typography color="textSecondary" align="center" sx={{ py: 10 }}>
                Aucune donnée d'entreprises disponible
              </Typography>
            )}
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
            {villesData.length > 0 ? (
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
            ) : (
              <Typography color="textSecondary" align="center" sx={{ py: 10 }}>
                Aucune donnée géographique disponible
              </Typography>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;