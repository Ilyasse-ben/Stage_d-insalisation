const userControler=require('../Controller/userController.js')
const exprese=require("express");
const rout=exprese.Router();
rout.post('/login',userControler.login);
rout.post('/inscrir',userControler.iscrire);

module.exports = rout;