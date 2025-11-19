const Team = require('../models/Team.js');

// ========================
// Récupérer UNE équipe par son ID
// ========================
exports.get_Team = async (req, res) => {
    try {
        const id = req.params.id; // On récupère l'ID passé dans l'URL
        const team = await Team.findById(id); // Recherche dans MongoDB par _id

        if (!team) {
            // Si aucune équipe trouvée, on renvoie un statut 404 (Not Found)
            return res.status(404).json({ message: 'Team not found' });
        }

        // Si trouvée, on renvoie l'objet JSON
        res.json(team);
    } catch (err) {
        // Si erreur serveur, on renvoie un statut 500 et le message d'erreur
        res.status(500).json({ error: err.message });
    }
}

// ========================
// Récupérer TOUTES les équipes ou filtrer par nom
// ========================
exports.get_Teams = async (req, res) => {
    try {
        const filter = {}; // Objet vide pour construire le filtre de recherche dynamiquement

        // Si on passe un paramètre ?name= dans l'URL
        if (req.query.name) {
            // Recherche partielle (contient le texte) et insensible à la casse (option 'i')
            filter.name = { $regex: req.query.name, $options: 'i' };
        }

        // Recherche dans la base avec ou sans filtre
        const teams = await Team.find(filter);

        // Retourne la liste au format JSON
        res.json(teams);
    } catch (err) {
        // Gestion des erreurs serveur
        res.status(500).json({ error: err.message });
    }
}
