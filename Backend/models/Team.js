const mongoose = require('mongoose');

// Création du schéma
const TeamSchema = new mongoose.Schema({
    logo: String,
    name: String,
    description: String,
    etat: Number, // entier
    players: mongoose.Schema.Types.Mixed, // tableau de chaînes (à adapter selon ton besoin)
    coaching: mongoose.Schema.Types.Mixed,  // tableau de chaînes
    group: mongoose.Schema.Types.Mixed // type libre
}, {
    collection: 'Team' // si ta collection existe déjà dans MongoDB
});

// Export du modèle
module.exports = mongoose.model('Team', TeamSchema);
