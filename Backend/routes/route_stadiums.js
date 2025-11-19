const exprese=require("express");
const rout=exprese.Router();
const stadium_Controller=require("../Controller/stadiumController")

rout.get('/',stadium_Controller.get_all_stadium)
rout.get('/:id',stadium_Controller.get_stadium)
module.exports = rout;