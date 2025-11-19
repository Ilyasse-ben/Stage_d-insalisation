const exprese=require("express");
const rout=exprese.Router();
const teams_Controller=require("../Controller/teamController")
const verifyToken = require("../middlewares/authMiddleware");

rout.get('/',teams_Controller.get_Teams)
rout.get('/:id',teams_Controller.get_Team)

module.exports = rout;