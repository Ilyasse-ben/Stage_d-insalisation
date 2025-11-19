const Matchs=require('../models/Match.js')
const Tema=require('../models/Team.js')

// ========================
// Récupérer TOUS les matches
// ========================
exports.get_all_match=async (req,res)=>{
    try {
        // --- Si on reçoit une date dans la requête ---
        if (req.query.Date) {
            const dateToFind = new Date(req.query.Date);

            // Début et fin de journée (UTC pour éviter le décalage de fuseau horaire)
            const startOfDay = new Date(Date.UTC(
                dateToFind.getUTCFullYear(),
                dateToFind.getUTCMonth(),
                dateToFind.getUTCDate(),
                0, 0, 0, 0
            ));
            const endOfDay = new Date(Date.UTC(
                dateToFind.getUTCFullYear(),
                dateToFind.getUTCMonth(),
                dateToFind.getUTCDate(),
                23, 59, 59, 999
            ));

            // Recherche des matchs ce jour-là
            const matchs = await Matchs.find({
                date: { $gte: startOfDay, $lte: endOfDay }
            });

            if (!matchs.length) {
                return res.status(404).json({ message: 'Aucun élément trouvé' });
            }
            return res.status(200).json(matchs);
        }
        // Récupérer un match par name
        if(req.query.name){
            const name=req.query.name
            const team_name=await Tema.find({'name':name})
            const idTeam=team_name[0].id
            const  match=await Matchs.find({$or:[{'team1':idTeam},{'team2':idTeam}]})
            return  res.status(200).json(match);
        }
        const matchs=await Matchs.find().sort({'date':1})
        res.status(200).json(matchs);
    } catch (err) {
        res.status(500).json({
            message: "Erreur lors de la récupération des matchs",
            erreur: err
        });
    }
}

// ========================
// Récupérer un match par id
// ========================
exports.get_match=async (req,res)=>{
    try{
        
        const id=req.params.id
        console.log(id)
        const match=await Matchs.findById(id)
        res.status(200).json(match)
    }catch(err){
        res.status(500).json({'message':'he hase a erre','errer':err})
    }
}
// ========================
// ========================