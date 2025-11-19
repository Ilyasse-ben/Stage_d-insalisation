const mongoose = require('mongoose');

// création de Schéma
const macheSchema= new mongoose.Schema({
        // ici tu peux définir les champs si besoin
        team1: mongoose.Schema.Types.ObjectId,
        team2: mongoose.Schema.Types.ObjectId,
        date: Date,
        stade: String
},{
   collection: 'Match'
})
module.exports=mongoose.model('Match',macheSchema)