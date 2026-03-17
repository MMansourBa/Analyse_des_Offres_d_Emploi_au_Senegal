// src/components/Layout/Footer.jsx
import React from 'react';
import { Box, Container, Typography, Link, Grid, IconButton } from '@mui/material';
import { Facebook, Twitter, LinkedIn, GitHub } from '@mui/icons-material';

const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        px: 2,
        mt: 'auto',
        backgroundColor: (theme) => theme.palette.grey[200],
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={3}>
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" color="text.primary" gutterBottom>
              Emploi Sénégal
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Analyse des offres d'emploi au Sénégal
              <br />
              Données mises à jour quotidiennement
            </Typography>
          </Grid>
          
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" color="text.primary" gutterBottom>
              Liens utiles
            </Typography>
            <Link href="/" color="inherit" display="block" sx={{ mb: 1 }}>
              Accueil
            </Link>
            <Link href="/offres" color="inherit" display="block" sx={{ mb: 1 }}>
              Offres d'emploi
            </Link>
            <Link href="/dashboard" color="inherit" display="block" sx={{ mb: 1 }}>
              Dashboard
            </Link>
            <Link href="/assistant" color="inherit" display="block">
              Assistant IA
            </Link>
          </Grid>
          
          <Grid item xs={12} sm={4}>
            <Typography variant="h6" color="text.primary" gutterBottom>
              Suivez-nous
            </Typography>
            <Box>
              <IconButton color="primary" aria-label="facebook">
                <Facebook />
              </IconButton>
              <IconButton color="primary" aria-label="twitter">
                <Twitter />
              </IconButton>
              <IconButton color="primary" aria-label="linkedin">
                <LinkedIn />
              </IconButton>
              <IconButton color="primary" aria-label="github">
                <GitHub />
              </IconButton>
            </Box>
            <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
              © {new Date().getFullYear()} Emploi Sénégal
              <br />
              Tous droits réservés
            </Typography>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default Footer;