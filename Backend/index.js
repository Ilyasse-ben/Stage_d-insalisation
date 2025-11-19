const express=require('express');
const cors = require("cors");
const app=express()
const mongoose=require('mongoose');
const team_route=require('./routes/route_teams.js');
const stadium_rote=require('./routes/route_stadiums.js');
const matche_route=require('./routes/route_matche.js')
const user_route=require('./routes/route_user.js');
// Autoriser toutes les origines (développement seulement)
app.use(cors());

// ================== connextion a la basse de donne 
mongoose.connect('mongodb://localhost:27017/CAF').then(()=>{
    console.log("connextion sucsseflye")
}).catch((e)=>{
    console.log("he hasse a errer: "+e)
})
// pour encoder les json
app.use(express.urlencoded({ extended: true }));

app.use(express.json())
app.use("/team",team_route)
app.use("/stadium",stadium_rote)
app.use("/match",matche_route)
app.use("/",user_route)
app.listen(3000,()=>{
    console.log("i'am listen in http://localhost:3000")
})