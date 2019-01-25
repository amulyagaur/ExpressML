var express = require('express');

var router = express.Router();
var bcrypt = require('bcryptjs');
let User = require('../models/user');
const passport = require('passport');

router.get('/login', function (req, res) {
    res.render('login', { title: 'Login' });
});

router.get('/register', function (req, res) {
    res.render('register', { title: 'Register' });
});



router.post('/register', function (req, res) {

    const name = req.body.name;
    const email = req.body.email;
    const username = req.body.username;
    const password = req.body.password;
    const password2 = req.body.password2;

    console.log(req.body.name);
    console.log(req.body.email);
    console.log(req.body.username);
    console.log(req.body.password);
    console.log(req.body.password2);

    req.checkBody('name', 'Name is required').notEmpty();
    req.checkBody('email', 'Email is required').notEmpty();
    req.checkBody('email', 'Email is not valid').isEmail();
    req.checkBody('username', 'Username is required').notEmpty();
    req.checkBody('password', 'Password is required').notEmpty();
    req.checkBody('password2', 'Passwords do not match').equals(req.body.password);

    let errors = req.validationErrors();

    if (errors) {
        console.log(errors);
        res.render('register', {
            title: 'Register',
            errors: errors
        });
    }
    else {
        let newUser = new User({
            name: name,
            email: email,
            username: username,
            password: password
        });
        bcrypt.genSalt(10, function (err, salt) {
            bcrypt.hash(newUser.password, salt, function (err, hash) {
                if (err) {
                    console.log(err);
                    return;
                }
                else {
                    newUser.password = hash;
                    newUser.save(function (err) {
                        if (err)
                            console.log(err);
                        else {
                            req.flash('success', 'Successfully Registered! Please Login.');
                            res.redirect('/users/login');
                        }
                    });
                }
            });
        });

    }
});

router.post('/login', function (req, res, next) {

    passport.authenticate('local', {
        successFlash: 'Welcome!',
        successRedirect: '/mainpage',
        failureRedirect: '/users/login',
        failureFlash: true
    })(req, res, next);

});

router.get('/logout', function (req, res) {
    req.logout();
    req.flash('success', 'You are logged out!');
    res.redirect('/users/login');
});

module.exports = router