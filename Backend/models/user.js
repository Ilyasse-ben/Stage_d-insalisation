const mongoos=require('mongoose')
// crée schema 
const userSchema=new mongoos.Schema({
    email:String,
    password:String,
})
module.exports=mongoos.model('user',userSchema)