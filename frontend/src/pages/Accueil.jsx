// src/pages/Accueil.jsx - Version avec compétences statiques
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
  Psychology
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { getStats, getTopEntreprises, getCompetences } from '../services/api';

// ============================================
// DONNÉES STATIQUES DES COMPÉTENCES (basées sur vos résultats)
// ============================================
const COMPETENCES_STATIQUES = [
  { nom: 'anglais', count: 1829, percentage: 54.9 },
  { nom: 'gestion', count: 656, percentage: 19.7 },
  { nom: 'organisation', count: 271, percentage: 8.1 },
  { nom: 'communication', count: 204, percentage: 6.1 },
  { nom: 'sécurité', count: 200, percentage: 6.0 },
  { nom: 'sens du service', count: 143, percentage: 4.3 },
  { nom: 'résolution de problèmes', count: 103, percentage: 3.1 },
  { nom: 'travail en équipe', count: 100, percentage: 3.0 },
  { nom: 'logistique', count: 84, percentage: 2.5 },
  { nom: 'français', count: 81, percentage: 2.4 }
];

const TOTAL_OFFRES = 3332;

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

// ✅ COMPOSANT COMPETENCE CARD MIS À JOUR AVEC LES BONNES DONNÉES
const CompetenceCard = ({ competence, count, percentage, index }) => {
  const getColor = (index) => {
    const colors = ['#1976d2', '#2e7d32', '#ed6c02', '#9c27b0', '#d32f2f', '#388e3c', '#f57c00', '#7b1fa2', '#0288d1', '#5e35b1'];
    return colors[index % colors.length];
  };

  const color = getColor(index);
  
  // Créer une barre de progression visuelle
  const barreLength = Math.round(percentage * 1.8); // Pour que 54.9% donne ~100 caractères
  const barre = '█'.repeat(barreLength);

  return (
    <Box
      sx={{
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
      <Box display="flex" alignItems="center" mb={1}>
        <Box
          sx={{
            width: 40,
            height: 40,
            borderRadius: '50%',
            bgcolor: color + '20',
            color: color,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontWeight: 'bold',
            mr: 2
          }}
        >
          #{index + 1}
        </Box>
        <Typography variant="h6" sx={{ fontWeight: 'bold', flex: 1 }}>
          {competence}
        </Typography>
        <Box textAlign="right">
          <Typography variant="body1" sx={{ fontWeight: 'bold', color: color }}>
            {percentage}%
          </Typography>
          <Typography variant="caption" color="textSecondary">
            {count.toLocaleString()} offres
          </Typography>
        </Box>
      </Box>
      
      {/* Barre de progression */}
      <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
        <Box
          sx={{
            height: 24,
            bgcolor: color + '30',
            borderRadius: 1,
            mr: 1,
            fontFamily: 'monospace',
            fontSize: '14px',
            lineHeight: '24px',
            px: 1,
            color: color,
            fontWeight: 'bold',
            width: `${percentage * 1.8}%`,
            minWidth: '50px',
            maxWidth: '100%',
            overflow: 'hidden',
            whiteSpace: 'nowrap'
          }}
        >
          {barre}
        </Box>
        <Typography variant="body2" color="textSecondary" sx={{ minWidth: 60 }}>
          {percentage}%
        </Typography>
      </Box>
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
        
        // On garde les appels API pour les stats et entreprises
        const [statsRes, entreprisesRes] = await Promise.all([
          getStats(),
          getTopEntreprises()
        ]);
        
        console.log('Stats reçues:', statsRes.data);
        console.log('Entreprises reçues:', entreprisesRes.data);
        
        setStats(statsRes.data);
        setTopEntreprises(entreprisesRes.data || []);
        
        // ✅ ON UTILISE LES COMPÉTENCES STATIQUES
        setCompetences(COMPETENCES_STATIQUES);
        
      } catch (error) {
        console.error('Erreur chargement données:', error);
        // Même en cas d'erreur, on garde les compétences statiques
        setCompetences(COMPETENCES_STATIQUES);
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
            Mais les compétences affichées sont correctes (données statiques)
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
        <Grid item xs={12} sm={6} md={4}>
          <StatCard
            title="Total Offres"
            value={stats?.total_offres?.toLocaleString() || TOTAL_OFFRES.toLocaleString()}
            icon={<Work sx={{ color: '#1976d2', fontSize: 40 }} />}
            color="#1976d2"
            subtitle="Offres d'emploi analysées"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={4}>
          <StatCard
            title="Secteur Leader"
            value={stats?.secteur_dominant?.secteur || 'Informatique / IT'}
            icon={<Business sx={{ color: '#2e7d32', fontSize: 40 }} />}
            color="#2e7d32"
            subtitle={stats?.secteur_dominant ? `${stats.secteur_dominant.count} offres` : '2895 offres'}
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={4}>
          <StatCard
            title="Ville Leader"
            value={stats?.ville_top?.ville || 'Dakar'}
            icon={<LocationOn sx={{ color: '#ed6c02', fontSize: 40 }} />}
            color="#ed6c02"
            subtitle={stats?.ville_top ? `${stats.ville_top.count} offres` : '3209 offres'}
          />
        </Grid>
      </Grid>

      {/* Message si pas de données backend */}
      {(!stats?.total_offres || stats.total_offres === 0) && (
        <Alert severity="info" sx={{ mb: 4 }}>
          Utilisation de données statiques pour les compétences en attendant la correction du backend.
        </Alert>
      )}

      {/* Section principale */}
      <Grid container spacing={4}>
        {/* Top Compétences - VERSION STATIQUE AVEC BONNES DONNÉES */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Box display="flex" alignItems="center" mb={3}>
              <EmojiEvents sx={{ fontSize: 40, color: '#ed6c02', mr: 2 }} />
              <Box>
                <Typography variant="h5" gutterBottom>
                  Top 10 Compétences Recherchées
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Basé sur l'analyse textuelle des offres d'emploi
                </Typography>
              </Box>
            </Box>
            
            {competences.length > 0 ? (
              <Box>
                {competences.map((comp, index) => (
                  <CompetenceCard
                    key={index}
                    competence={comp.nom}
                    count={comp.count}
                    percentage={comp.percentage}
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

        {/* Top Entreprises */}
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
                      {entreprise.entreprise || 'Entreprise non spécifiée'}
                    </Typography>
                    <Chip
                      label={`${entreprise.count || 0} offres`}
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

          {/* Petit résumé de la compétence #1 */}
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              💡 Compétence la plus demandée
            </Typography>
            <Box>
              <Typography variant="h4" color="primary" gutterBottom>
                {competences[0]?.nom || 'Anglais'}
              </Typography>
              <Typography variant="body2" color="textSecondary">
                Présent dans {competences[0]?.count || 1829} offres soit {' '}
                {competences[0]?.percentage || 54.9}% des offres
              </Typography>
            </Box>
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
            `Parcourez notre base de données de ${stats.total_offres.toLocaleString()} offres d'emploi` :
            'Parcourez notre base de données de 3 332 offres d\'emploi'
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