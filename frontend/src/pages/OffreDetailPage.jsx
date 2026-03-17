// src/pages/OffreDetailPage.jsx
import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  Chip,
  Divider,
  Button,
  CircularProgress,
  Grid
} from '@mui/material';
import {
  ArrowBack,
  Business,
  LocationOn,
  CalendarToday,
  Work,
  Category
} from '@mui/icons-material';
import { useParams, useNavigate } from 'react-router-dom';
import { getOffre } from '../services/api';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';

const OffreDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [offre, setOffre] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchOffre();
  }, [id]);

  const fetchOffre = async () => {
    try {
      const response = await getOffre(id);
      setOffre(response.data);
    } catch (error) {
      console.error('Erreur chargement offre:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Date non spécifiée';
    try {
      const date = new Date(dateString);
      return format(date, 'dd MMMM yyyy', { locale: fr });
    } catch {
      return dateString;
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  if (!offre) {
    return (
      <Container>
        <Typography>Offre non trouvée</Typography>
        <Button startIcon={<ArrowBack />} onClick={() => navigate('/offres')}>
          Retour aux offres
        </Button>
      </Container>
    );
  }

  return (
    <Container maxWidth="md" sx={{ mt: 4, mb: 4 }}>
      <Button 
        startIcon={<ArrowBack />} 
        onClick={() => navigate('/offres')}
        sx={{ mb: 2 }}
      >
        Retour aux offres
      </Button>

      <Paper sx={{ p: 4 }}>
        {/* En-tête */}
        <Typography variant="h4" gutterBottom>
          {offre.intitule}
        </Typography>
        
        <Box display="flex" gap={2} flexWrap="wrap" mb={3}>
          <Chip 
            icon={<Business />} 
            label={offre.entreprise || 'Non spécifié'} 
            variant="outlined"
          />
          <Chip 
            icon={<LocationOn />} 
            label={offre.ville || 'Non spécifié'} 
            variant="outlined"
          />
          <Chip 
            icon={<Work />} 
            label={offre.type_contrat || 'Non spécifié'} 
            color="primary"
          />
          <Chip 
            icon={<CalendarToday />} 
            label={formatDate(offre.date_publication)} 
            variant="outlined"
          />
          {offre.secteur && (
            <Chip 
              icon={<Category />} 
              label={offre.secteur} 
              variant="outlined"
            />
          )}
        </Box>

        <Divider sx={{ my: 3 }} />

        {/* Compétences */}
        {offre.competences && (
          <>
            <Typography variant="h6" gutterBottom>
              Compétences requises
            </Typography>
            <Typography paragraph>
              {offre.competences}
            </Typography>
            <Divider sx={{ my: 3 }} />
          </>
        )}

        {/* Informations supplémentaires si disponibles */}
        <Grid container spacing={2}>
          {offre.mention_salaire && (
            <Grid item xs={12}>
              <Typography variant="subtitle2" color="textSecondary">
                Salaire
              </Typography>
              <Typography>
                {offre.salaire_texte || 'Non spécifié'}
              </Typography>
            </Grid>
          )}
        </Grid>
      </Paper>
    </Container>
  );
};

export default OffreDetailPage;