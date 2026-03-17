// src/components/Layout/Navbar.jsx
import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box
} from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';
import {
  Home,
  List,
  Dashboard,
  Chat
} from '@mui/icons-material';

const Navbar = () => {
  const navigate = useNavigate();

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography 
          variant="h6" 
          component="div" 
          sx={{ flexGrow: 1, cursor: 'pointer' }}
          onClick={() => navigate('/')}
        >
          Emploi Sénégal
        </Typography>
        
        <Box>
          <Button color="inherit" component={Link} to="/" startIcon={<Home />}>
            Accueil
          </Button>
          <Button color="inherit" component={Link} to="/offres" startIcon={<List />}>
            Offres
          </Button>
          <Button color="inherit" component={Link} to="/dashboard" startIcon={<Dashboard />}>
            Dashboard
          </Button>
          <Button color="inherit" component={Link} to="/assistant" startIcon={<Chat />}>
            Assistant
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;