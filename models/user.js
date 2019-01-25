let mongoose = require('mongoose');
var findOrCreate = require('mongoose-findorcreate')

let userSchema = mongoose.Schema({
    name: {
        type: String,
        required: true
    },
    email: {
        type: String,
        required: true
    },
    username: {
        type: Number,
        required: true
    },
    password: {
        type: String,
        required: true
    }
});

userSchema.plugin(findOrCreate);

let User = module.exports = mongoose.model('User', userSchema);
