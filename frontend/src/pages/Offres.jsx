// src/pages/Offres.jsx
import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  Box,
  Pagination,
  Card,
  CardContent,
  CardActions,
  Chip,
  CircularProgress,
  InputAdornment,
  IconButton
} from '@mui/material';
import {
  Search,
  LocationOn,
  Business,
  CalendarToday,
  Clear
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { getOffres } from '../services/api';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';

const Offres = () => {
  const [offres, setOffres] = useState([]);
  const [loading, setLoading] = useState(true);
  const [pagination, setPagination] = useState({
    count: 0,
    next: null,
    previous: null,
    currentPage: 1,
    totalPages: 1
  });
  
  const [filters, setFilters] = useState({
    recherche: '',
    ville: '',
    secteur: '',
    contrat: '',
    page: 1
  });

  const [filtresDisponibles, setFiltresDisponibles] = useState({
    villes: [],
    secteurs: [],
    contrats: []
  });

  const navigate = useNavigate();

  useEffect(() => {
    fetchOffres();
  }, [filters]);

  const fetchOffres = async () => {
    setLoading(true);
    try {
      const params = {
        page: filters.page,
        page_size: 12
      };
      
      if (filters.recherche) params.recherche = filters.recherche;
      if (filters.ville) params.ville = filters.ville;
      if (filters.secteur) params.secteur = filters.secteur;
      if (filters.contrat) params.contrat = filters.contrat;
      
      const response = await getOffres(params);
      
      setOffres(response.data.results);
      
      // Extraire les filtres disponibles depuis les résultats
      const villes = [...new Set(response.data.results.map(o => o.ville).filter(Boolean))];
      const secteurs = [...new Set(response.data.results.map(o => o.secteur).filter(Boolean))];
      const contrats = [...new Set(response.data.results.map(o => o.type_contrat).filter(Boolean))];
      
      setFiltresDisponibles({ villes, secteurs, contrats });
      
      // Calculer la pagination
      setPagination({
        count: response.data.count,
        next: response.data.next,
        previous: response.data.previous,
        currentPage: filters.page,
        totalPages: Math.ceil(response.data.count / 12)
      });
      
    } catch (error) {
      console.error('Erreur chargement offres:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    setFilters(prev => ({ ...prev, [name]: value, page: 1 }));
  };

  const handlePageChange = (event, value) => {
    setFilters(prev => ({ ...prev, page: value }));
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const clearFilters = () => {
    setFilters({
      recherche: '',
      ville: '',
      secteur: '',
      contrat: '',
      page: 1
    });
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

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Offres d'Emploi au Sénégal
      </Typography>
      <Typography variant="subtitle1" color="textSecondary" gutterBottom>
        {pagination.count} offres disponibles
      </Typography>

      {/* Filtres */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={4}>
            <TextField
              fullWidth
              label="Rechercher"
              name="recherche"
              value={filters.recherche}
              onChange={handleFilterChange}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <Search />
                  </InputAdornment>
                )
              }}
              placeholder="Titre, entreprise, compétences..."
            />
          </Grid>
          
          <Grid item xs={12} md={2}>
            <FormControl fullWidth>
              <InputLabel>Ville</InputLabel>
              <Select
                name="ville"
                value={filters.ville}
                onChange={handleFilterChange}
                label="Ville"
              >
                <MenuItem value="">Toutes</MenuItem>
                {filtresDisponibles.villes.map(ville => (
                  <MenuItem key={ville} value={ville}>{ville}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12} md={2}>
            <FormControl fullWidth>
              <InputLabel>Secteur</InputLabel>
              <Select
                name="secteur"
                value={filters.secteur}
                onChange={handleFilterChange}
                label="Secteur"
              >
                <MenuItem value="">Tous</MenuItem>
                {filtresDisponibles.secteurs.map(secteur => (
                  <MenuItem key={secteur} value={secteur}>{secteur}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12} md={2}>
            <FormControl fullWidth>
              <InputLabel>Contrat</InputLabel>
              <Select
                name="contrat"
                value={filters.contrat}
                onChange={handleFilterChange}
                label="Contrat"
              >
                <MenuItem value="">Tous</MenuItem>
                {filtresDisponibles.contrats.map(contrat => (
                  <MenuItem key={contrat} value={contrat}>{contrat}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12} md={2}>
            <Button
              fullWidth
              variant="outlined"
              onClick={clearFilters}
              startIcon={<Clear />}
            >
              Effacer
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {/* Liste des offres */}
      {loading ? (
        <Box display="flex" justifyContent="center" py={4}>
          <CircularProgress />
        </Box>
      ) : (
        <>
          <Grid container spacing={3}>
            {offres.map((offre) => (
              <Grid item xs={12} md={6} lg={4} key={offre.id}>
                <Card 
                  sx={{ 
                    height: '100%', 
                    display: 'flex', 
                    flexDirection: 'column',
                    transition: 'transform 0.2s',
                    '&:hover': {
                      transform: 'translateY(-4px)',
                      boxShadow: 4,
                      cursor: 'pointer'
                    }
                  }}
                  onClick={() => navigate(`/offres/${offre.id}`)}
                >
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Typography variant="h6" gutterBottom noWrap>
                      {offre.intitule}
                    </Typography>
                    
                    <Box display="flex" alignItems="center" mb={1}>
                      <Business sx={{ fontSize: 18, mr: 1, color: 'text.secondary' }} />
                      <Typography variant="body2" color="textSecondary">
                        {offre.entreprise || 'Entreprise non spécifiée'}
                      </Typography>
                    </Box>
                    
                    <Box display="flex" alignItems="center" mb={1}>
                      <LocationOn sx={{ fontSize: 18, mr: 1, color: 'text.secondary' }} />
                      <Typography variant="body2" color="textSecondary">
                        {offre.ville || 'Ville non spécifiée'}
                      </Typography>
                    </Box>
                    
                    <Box display="flex" alignItems="center" mb={2}>
                      <CalendarToday sx={{ fontSize: 18, mr: 1, color: 'text.secondary' }} />
                      <Typography variant="body2" color="textSecondary">
                        {formatDate(offre.date_publication)}
                      </Typography>
                    </Box>
                    
                    <Box display="flex" gap={1} flexWrap="wrap">
                      <Chip 
                        label={offre.type_contrat || 'Non spécifié'} 
                        size="small"
                        color="primary"
                        variant="outlined"
                      />
                      {offre.secteur && (
                        <Chip 
                          label={offre.secteur} 
                          size="small"
                          variant="outlined"
                        />
                      )}
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>

          {/* Pagination */}
          {pagination.totalPages > 1 && (
            <Box display="flex" justifyContent="center" mt={4}>
              <Pagination
                count={pagination.totalPages}
                page={filters.page}
                onChange={handlePageChange}
                color="primary"
                size="large"
              />
            </Box>
          )}
        </>
      )}
    </Container>
  );
};

export default Offres;