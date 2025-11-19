const User=require('../models/user.js');
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");
const SECRET_KEY = "Mrocco_2025_CAF";

exports.login=async (req,res)=>{
    const {email,password}=req.body;
    const user=await User.findOne({'email':email});
    if(user){
        if(await bcrypt.compare(password, user.password)){
            const token = jwt.sign(
            { id: user.id, email: user.email },
            SECRET_KEY,
            { expiresIn: "1h" });
            return res.status(200).json({'message':'this personne existe',token});
        }
        return res.status(200).json({'message':'this personne not existe'});
    }
    return res.status(200).json({'message':'this personne not existe'})
}
exports.iscrire=async (req,res)=>{
    const {email,password}=req.body;
    const user=await User.findOne({'email':email});
    console.log(await bcrypt.hash(password, 10));
    if(user){
        return res.status(201).json({'messag':'email ou password incoritct'})
    }
    User.insertOne({email:email,password:await bcrypt.hash(password,10)})
    return res.status(201).json({'messag':'inscription bien fait'})
}