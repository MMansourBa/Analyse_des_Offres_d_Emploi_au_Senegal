// src/pages/Accueil.jsx - Correction de l'affichage des compétences
import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  CircularProgress,
  Divider,
  Button,
  Alert,
  Chip
} from '@mui/material';
import {
  TrendingUp,
  Business,
  LocationOn,
  Work,
  EmojiEvents,
  ArrowForward,
  Code,
  Psychology,
  Language
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { getStats, getTopEntreprises, getCompetences } from '../services/api';

const StatCard = ({ title, value, icon, color, subtitle }) => {
  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box display="flex" alignItems="center" mb={2}>
          <Box sx={{ 
            backgroundColor: color + '20',
            borderRadius: '50%',
            width: 48,
            height: 48,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            mr: 2
          }}>
            {icon}
          </Box>
          <Typography variant="h6" color="textSecondary">
            {title}
          </Typography>
        </Box>
        <Typography variant="h3" component="div" gutterBottom>
          {value}
        </Typography>
        {subtitle && (
          <Typography variant="body2" color="textSecondary">
            {subtitle}
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};

const CompetenceCard = ({ competence, count, index }) => {
  const getColor = (index) => {
    const colors = ['#1976d2', '#2e7d32', '#ed6c02', '#9c27b0', '#d32f2f'];
    return colors[index % colors.length];
  };

  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        mb: 2,
        p: 2,
        borderRadius: 2,
        bgcolor: '#f8f9fa',
        '&:hover': {
          bgcolor: '#e9ecef',
          transform: 'translateX(5px)',
          transition: 'all 0.3s'
        }
      }}
    >
      <Box
        sx={{
          width: 40,
          height: 40,
          borderRadius: '50%',
          bgcolor: getColor(index) + '20',
          color: getColor(index),
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontWeight: 'bold',
          mr: 2
        }}
      >
        #{index + 1}
      </Box>
      <Box sx={{ flex: 1 }}>
        <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
          {competence}
        </Typography>
        <Box display="flex" alignItems="center">
          <Work sx={{ fontSize: 16, mr: 0.5, color: 'text.secondary' }} />
          <Typography variant="body2" color="textSecondary">
            {count} offres
          </Typography>
        </Box>
      </Box>
      <Chip
        label={`${Math.round((count / 500) * 100)}%`}
        size="small"
        sx={{ bgcolor: getColor(index), color: 'white' }}
      />
    </Box>
  );
};

const Accueil = () => {
  const [stats, setStats] = useState(null);
  const [topEntreprises, setTopEntreprises] = useState([]);
  const [competences, setCompetences] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const [statsRes, entreprisesRes, competencesRes] = await Promise.all([
          getStats(),
          getTopEntreprises(),
          getCompetences()
        ]);
        
        console.log('Stats reçues:', statsRes.data);
        console.log('Entreprises reçues:', entreprisesRes.data);
        console.log('Compétences reçues:', competencesRes.data);
        
        setStats(statsRes.data);
        setTopEntreprises(entreprisesRes.data || []);
        
        // Traiter les compétences - prendre les compétences structurées
        if (competencesRes.data && competencesRes.data.competences_structurees) {
          setCompetences(competencesRes.data.competences_structurees.slice(0, 10));
        } else if (Array.isArray(competencesRes.data)) {
          setCompetences(competencesRes.data.slice(0, 10));
        }
        
      } catch (error) {
        console.error('Erreur chargement données:', error);
        setError('Impossible de charger les données. Vérifiez que le backend est bien lancé sur http://localhost:8000');
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

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
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <Typography variant="h5" gutterBottom>
            🔌 Backend non accessible
          </Typography>
          <Typography paragraph>
            Assurez-vous que le serveur Django est lancé sur http://localhost:8000
          </Typography>
          <Button 
            variant="contained" 
            onClick={() => window.location.reload()}
          >
            Réessayer
          </Button>
        </Paper>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* En-tête */}
      <Box mb={4}>
        <Typography variant="h3" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
          Analyse du Marché de l'Emploi
        </Typography>
        <Typography variant="h5" color="textSecondary" gutterBottom>
          Sénégal • Données mises à jour en temps réel
        </Typography>
        <Divider sx={{ my: 2 }} />
      </Box>

      {/* KPIs */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Offres"
            value={stats?.total_offres?.toLocaleString() || '0'}
            icon={<Work sx={{ color: '#1976d2' }} />}
            color="#1976d2"
            subtitle="Offres d'emploi analysées"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Secteur Leader"
            value={stats?.secteur_dominant?.secteur || 'N/A'}
            icon={<Business sx={{ color: '#2e7d32' }} />}
            color="#2e7d32"
            subtitle={stats?.secteur_dominant ? `${stats.secteur_dominant.count} offres` : 'Aucune donnée'}
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Ville Leader"
            value={stats?.ville_top?.ville || 'N/A'}
            icon={<LocationOn sx={{ color: '#ed6c02' }} />}
            color="#ed6c02"
            subtitle={stats?.ville_top ? `${stats.ville_top.count} offres` : 'Aucune donnée'}
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Croissance"
            value={`${stats?.croissance_mensuelle > 0 ? '+' : ''}${stats?.croissance_mensuelle || 0}%`}
            icon={<TrendingUp sx={{ color: stats?.croissance_mensuelle >= 0 ? '#4caf50' : '#f44336' }} />}
            color={stats?.croissance_mensuelle >= 0 ? '#4caf50' : '#f44336'}
            subtitle="vs mois précédent"
          />
        </Grid>
      </Grid>

      {/* Message si pas de données */}
      {(!stats?.total_offres || stats.total_offres === 0) && (
        <Alert severity="info" sx={{ mb: 4 }}>
          Aucune offre d'emploi trouvée dans la base de données. 
          Vérifiez que vos données sont bien importées dans Django.
        </Alert>
      )}

      {/* Section principale */}
      <Grid container spacing={4}>
        {/* Top Compétences */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Box display="flex" alignItems="center" mb={3}>
              <EmojiEvents sx={{ fontSize: 40, color: '#ed6c02', mr: 2 }} />
              <Box>
                <Typography variant="h5" gutterBottom>
                  Top 10 Compétences Recherchées
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Basé sur l'analyse des offres d'emploi
                </Typography>
              </Box>
            </Box>
            
            {competences.length > 0 ? (
              <Box>
                {competences.map((comp, index) => (
                  <CompetenceCard
                    key={index}
                    competence={comp.nom || comp.competence}
                    count={comp.count || 0}
                    index={index}
                  />
                ))}
              </Box>
            ) : (
              <Box textAlign="center" py={4}>
                <Psychology sx={{ fontSize: 60, color: '#ccc', mb: 2 }} />
                <Typography color="textSecondary">
                  Aucune donnée de compétences disponible
                </Typography>
              </Box>
            )}
          </Paper>
        </Grid>

        {/* Top Entreprises et autres infos */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Box display="flex" alignItems="center" mb={3}>
              <Business sx={{ fontSize: 40, color: '#1976d2', mr: 2 }} />
              <Box>
                <Typography variant="h5" gutterBottom>
                  Top Entreprises qui Recrutent
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Les employeurs les plus actifs
                </Typography>
              </Box>
            </Box>
            
            {topEntreprises.length > 0 ? (
              <Box>
                {topEntreprises.slice(0, 5).map((entreprise, index) => (
                  <Box
                    key={index}
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      mb: 2,
                      p: 2,
                      borderRadius: 2,
                      bgcolor: '#f8f9fa',
                      '&:hover': { bgcolor: '#e9ecef' }
                    }}
                  >
                    <Typography
                      variant="h6"
                      sx={{
                        minWidth: 40,
                        color: index < 3 ? '#1976d2' : 'text.secondary',
                        fontWeight: 'bold'
                      }}
                    >
                      #{index + 1}
                    </Typography>
                    <Typography variant="body1" sx={{ flex: 1, fontWeight: 'bold' }}>
                      {entreprise.entreprise}
                    </Typography>
                    <Chip
                      label={`${entreprise.count} offres`}
                      size="small"
                      color={index < 3 ? 'primary' : 'default'}
                    />
                  </Box>
                ))}
              </Box>
            ) : (
              <Typography color="textSecondary" align="center" py={4}>
                Aucune donnée d'entreprises disponible
              </Typography>
            )}
          </Paper>

          {/* Répartition par contrat (optionnel) */}
          <Paper sx={{ p: 3 }}>
            <Box display="flex" alignItems="center" mb={2}>
              <Language sx={{ color: '#2e7d32', mr: 1 }} />
              <Typography variant="h6">
                Type de contrat dominant
              </Typography>
            </Box>
            <Typography variant="h4" color="primary" gutterBottom>
              {stats?.contrat_dominant?.type_contrat || 'Non spécifié'}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              {stats?.contrat_dominant?.count || 0} offres disponibles
            </Typography>
          </Paper>
        </Grid>
      </Grid>

      {/* Call to Action */}
      <Paper 
        sx={{ 
          mt: 4, 
          p: 4, 
          textAlign: 'center',
          background: 'linear-gradient(135deg, #1976d2 0%, #9c27b0 100%)',
          color: 'white',
          borderRadius: 2
        }}
      >
        <Typography variant="h4" gutterBottom>
          Explorez toutes les opportunités
        </Typography>
        <Typography variant="body1" paragraph sx={{ opacity: 0.9 }}>
          {stats?.total_offres ? 
            `Parcourez notre base de données de ${stats.total_offres} offres d'emploi` :
            'Découvrez les offres disponibles'
          }
        </Typography>
        <Button 
          variant="contained" 
          size="large"
          onClick={() => navigate('/offres')}
          sx={{ 
            bgcolor: 'white', 
            color: '#1976d2',
            '&:hover': { bgcolor: '#f5f5f5' },
            px: 4,
            py: 1.5
          }}
        >
          Voir les offres
          <ArrowForward sx={{ ml: 1 }} />
        </Button>
      </Paper>
    </Container>
  );
};

export default Accueil;