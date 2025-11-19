const mongoose = require('mongoose');

// Création du schéma
const TeamSchema = new mongoose.Schema({
    logo: String,
    name: String,
    description: String,
    City: String, // entier
    capacity:String
}, {
    collection: 'Stadium' // si ta collection existe déjà dans MongoDB
});

// Export du modèle
module.exports = mongoose.model('stadium', TeamSchema);