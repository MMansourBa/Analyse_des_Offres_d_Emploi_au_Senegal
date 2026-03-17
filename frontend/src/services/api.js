// src/services/api.js
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Intercepteur pour gérer les erreurs
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// ============================================
// ENDPOINTS EXISTANTS
// ============================================

// Offres
export const getOffres = (params = {}) => api.get('/offres/', { params });
export const getOffre = (id) => api.get(`/offres/${id}/`);

// Statistiques générales
export const getStats = () => api.get('/stats/');
export const getTopEntreprises = () => api.get('/entreprises/top/');
export const getEvolution = () => api.get('/evolution/');

// Assistant
export const sendChat = (message) => api.post('/chat/', { message });

// ============================================
// NOUVEAUX ENDPOINTS POUR LE DASHBOARD
// ============================================

/**
 * Récupère le top des compétences
 * GET /api/competences/
 */
export const getCompetences = () => api.get('/competences/');

/**
 * Récupère la répartition des offres par secteur
 * GET /api/secteurs/
 */
export const getSecteurs = () => api.get('/secteurs/');

/**
 * Récupère la répartition des offres par ville
 * GET /api/villes/
 */
export const getVilles = () => api.get('/villes/');

/**
 * Récupère la répartition des offres par type de contrat
 * GET /api/contrats/
 */
export const getContrats = () => api.get('/contrats/');

/**
 * Récupère toutes les valeurs disponibles pour les filtres
 * GET /api/filtres/
 */
export const getFiltres = () => api.get('/filtres/');

// ============================================
// VÉRIFICATION DE LA CONNEXION API
// ============================================

/**
 * Vérifie si l'API répond
 */
export const checkApiHealth = () => api.get('/');

export default api;