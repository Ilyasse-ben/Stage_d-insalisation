const express=require('express')
const rout=express.Router()
const match_controller=require('../Controller/matchController')
rout.get('/',match_controller.get_all_match)
rout.get('/:id',match_controller.get_match)
module.exports=rout