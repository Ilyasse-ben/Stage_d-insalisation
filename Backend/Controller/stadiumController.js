const Stadium = require('../models/Stadiums');

// ========================
// Récupérer TOUS les stades (avec option de filtrage par nom)
// ========================
exports.get_all_stadium = async (req, res) => {
    try {
        const filtre = {};

        // Si un nom est passé dans la query (?name=)
        if (req.query.name) {
            // Utilisation de $regex pour recherche partielle insensible à la casse
            filtre.name = { $regex: req.query.name, $options: "i" };
        }

        // Recherche dans la base
        const stadiums = await Stadium.find(filtre);

        // Renvoi de la liste des stades
        res.json(stadiums);
    } catch (error) {
        // Gestion des erreurs
        res.status(500).json({ message: "Error retrieving stadiums", error: error.message });
    }
};

// ========================
// Récupérer UN stade par son ID
// ========================
exports.get_stadium = async (req, res) => {
    try {
        const id = req.params.id; // On récupère l'ID passé dans l'URL
        const stadium = await Stadium.findById(id); // Recherche dans MongoDB

        if (stadium) {
            res.json(stadium); // Stade trouvé → on renvoie les données
        } else {
            // Stade non trouvé
            res.status(404).json({ message: 'Stadium not found' });
        }
    } catch (error) {
        // Erreur serveur ou ID invalide
        res.status(500).json({ message: "Error retrieving stadium", error: error.message });
    }
};
