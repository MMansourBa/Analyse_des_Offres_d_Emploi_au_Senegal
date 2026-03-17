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

// Endpoints existants
export const getOffres = (params = {}) => api.get('/offres/', { params });
export const getOffre = (id) => api.get(`/offres/${id}/`);
export const getStats = () => api.get('/stats/');
export const getTopEntreprises = () => api.get('/entreprises/top/');
export const getEvolution = () => api.get('/evolution/');

// Version avec vrai appel API (à décommenter quand le backend est prêt)
//export const sendChat = (message) => {
  //return api.post('/chat/', { message });
//};

// Nouvel endpoint pour l'assistant
export const sendChat = (message) => {
  // Version temporaire qui simule une réponse
  // À remplacer plus tard par un vrai appel API
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: {
          response: getSimulatedResponse(message)
        }
      });
    }, 1000);
  });
};

// Fonction pour simuler des réponses (à supprimer quand le vrai backend sera prêt)
function getSimulatedResponse(message) {
  const msg = message.toLowerCase();
  
  if (msg.includes('secteur') || msg.includes('recrute')) {
    return "Actuellement, le secteur qui recrute le plus est l'Informatique / IT, suivi par la Logistique et le Commerce.";
  }
  else if (msg.includes('compétence') || msg.includes('skill')) {
    return "Les compétences les plus demandées à Dakar sont : gestion de projet, communication, leadership, et maîtrise des outils bureautiques.";
  }
  else if (msg.includes('cdi')) {
    return "Ce mois-ci, nous avons environ 25 offres en CDI, principalement dans les secteurs de l'IT et de l'administration.";
  }
  else if (msg.includes('ville') || msg.includes('dakar') || msg.includes('thies')) {
    return "Dakar concentre plus de 70% des offres, suivie de Thiès et Saint-Louis. Pour l'IT spécifiquement, Dakar est la ville leader avec 85% des opportunités.";
  }
  else {
    return "Je suis votre assistant pour analyser le marché de l'emploi sénégalais. Vous pouvez me poser des questions sur les secteurs, les compétences, les villes, ou les types de contrats !";
  }
}

export default api;