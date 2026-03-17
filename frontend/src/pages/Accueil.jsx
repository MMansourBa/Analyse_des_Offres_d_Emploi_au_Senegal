// src/pages/Accueil.jsx
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
  useTheme
} from '@mui/material';
import {
  TrendingUp,
  Business,
  LocationOn,
  Work,
  EmojiEvents,
  ArrowForward
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { getStats, getTopEntreprises } from '../services/api';

const StatCard = ({ title, value, icon, color, subtitle }) => {
  const theme = useTheme();
  
  return (
    <Card 
      sx={{ 
        height: '100%',
        transition: 'transform 0.2s',
        '&:hover': {
          transform: 'translateY(-4px)',
          boxShadow: theme.shadows[8]
        }
      }}
    >
      <CardContent>
        <Box display="flex" alignItems="center" mb={2}>
          <Box 
            sx={{ 
              backgroundColor: color + '20',
              borderRadius: '50%',
              width: 48,
              height: 48,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              mr: 2
            }}
          >
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

const Accueil = () => {
  const [stats, setStats] = useState(null);
  const [topEntreprises, setTopEntreprises] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const theme = useTheme();

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, entreprisesRes] = await Promise.all([
          getStats(),
          getTopEntreprises()
        ]);
        setStats(statsRes.data);
        setTopEntreprises(entreprisesRes.data);
      } catch (error) {
        console.error('Erreur chargement données:', error);
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
            value={stats?.total_offres || 0}
            icon={<Work sx={{ color: theme.palette.primary.main }} />}
            color={theme.palette.primary.main}
            subtitle="Offres d'emploi analysées"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Secteur Dominant"
            value={stats?.secteur_dominant?.secteur || 'N/A'}
            icon={<Business sx={{ color: theme.palette.success.main }} />}
            color={theme.palette.success.main}
            subtitle={`${stats?.secteur_dominant?.count || 0} offres`}
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Ville Leader"
            value={stats?.ville_top?.ville || 'N/A'}
            icon={<LocationOn sx={{ color: theme.palette.warning.main }} />}
            color={theme.palette.warning.main}
            subtitle={`${stats?.ville_top?.count || 0} opportunités`}
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

      {/* Top Compétences */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <EmojiEvents sx={{ mr: 1, color: theme.palette.warning.main }} />
              Top 10 Compétences Recherchées
            </Typography>
            <Box mt={2}>
              {stats?.top_competences?.map((comp, index) => (
                <Box 
                  key={index}
                  sx={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    mb: 1,
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
                      color: index < 3 ? theme.palette.warning.main : 'text.secondary'
                    }}
                  >
                    #{index + 1}
                  </Typography>
                  <Typography variant="body1" sx={{ flex: 1 }}>
                    {comp.nom}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    {comp.count} offres
                  </Typography>
                  <Box 
                    sx={{ 
                      width: 100, 
                      height: 8, 
                      bgcolor: '#e0e0e0', 
                      borderRadius: 4,
                      ml: 2,
                      position: 'relative'
                    }}
                  >
                    <Box 
                      sx={{ 
                        width: `${(comp.count / stats.top_competences[0].count) * 100}%`,
                        height: '100%',
                        bgcolor: index < 3 ? theme.palette.warning.main : theme.palette.primary.main,
                        borderRadius: 4
                      }}
                    />
                  </Box>
                </Box>
              ))}
            </Box>
          </Paper>
        </Grid>

        {/* Top Entreprises */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <Business sx={{ mr: 1, color: theme.palette.info.main }} />
              Top Entreprises qui Recrutent
            </Typography>
            <Box mt={2}>
              {topEntreprises.map((entreprise, index) => (
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
                      color: index < 3 ? theme.palette.info.main : 'text.secondary'
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
            
            <Button 
              variant="outlined" 
              endIcon={<ArrowForward />}
              onClick={() => navigate('/offres')}
              sx={{ mt: 2 }}
              fullWidth
            >
              Voir toutes les offres
            </Button>
          </Paper>
        </Grid>
      </Grid>

      {/* Call to Action */}
      <Paper 
        sx={{ 
          p: 4, 
          textAlign: 'center',
          background: `linear-gradient(45deg, ${theme.palette.primary.main} 30%, ${theme.palette.secondary.main} 90%)`,
          color: 'white'
        }}
      >
        <Typography variant="h4" gutterBottom>
          Explorez toutes les opportunités
        </Typography>
        <Typography variant="body1" paragraph>
          Parcourez notre base de données de {stats?.total_offres || 0} offres d'emploi
        </Typography>
        <Button 
          variant="contained" 
          size="large"
          onClick={() => navigate('/offres')}
          sx={{ 
            bgcolor: 'white', 
            color: theme.palette.primary.main,
            '&:hover': { bgcolor: '#f5f5f5' }
          }}
        >
          Voir les offres
        </Button>
      </Paper>
    </Container>
  );
};

export default Accueil;