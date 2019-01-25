const express = require('express')
const app = express()
const port = 3010
var csv = require("fast-csv");
var formidable = require('formidable');
app.use(express.static('public'));
var obj = csv();
const passport = require('passport');
var path = require('path')
var fs = require('fs');
var router = express.Router();
const config = require('./config/database');
//Express Session middleware
var session = require('express-session');
app.use(session({
    secret: 'keyboard cat',
    resave: true,
    saveUninitialized: true
}));
var features = [];
var dataframe = [];
var dataset = [];
var msg = [];

var bodyParser = require('body-parser')
// parse application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: false }))

// parse application/json
app.use(bodyParser.json())

var { PythonShell } = require('python-shell');


app.set('view engine', 'ejs');
//Express messages middleware
var flash = require('connect-flash');
app.use(require('connect-flash')());
app.use(function (req, res, next) {
    res.locals.messages = require('express-messages')(req, res);
    next();
});

// Express validator midlleware
var expressValidator = require('express-validator')
app.use(expressValidator({
    errorFormatter: function (param, msg, value) {
        var namespace = param.split('.'),
            root = namespace.shift(),
            formParam = root;

        while (namespace.length) {
            formParam += '[' + namespace.shift() + ']';
        }
        return {
            param: formParam,
            msg: msg,
            value: value
        };
    }
}));

require('./config/passport')(passport);
app.use(passport.initialize());
app.use(passport.session());

var mongoose = require('mongoose');
mongoose.connect(config.database, {
    useNewUrlParser: true
});
var db = mongoose.connection;

// if we're not connected yet
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', function () {
    // we're connected!
    console.log("Database Connected!")
});


let User = require('./models/user');

app.get('*', function (req, res, next) {
    res.locals.user = req.user || null;
    next();
});




app.get('/file', (req, res) => res.render('upload'));
app.get('/csv', (req, res) => res.render('fromcsv'));
app.get('/', (req, res) => res.render('landingpage'));

app.post('/file', function (req, res) {
    var form = new formidable.IncomingForm();
    features = [];
    dataframe = [];
    dataset = [];
    form.parse(req);

    form.on('fileBegin', function (name, file) {
        file.name = 'data.csv';
        file.path = __dirname + '/public/uploads/' + file.name;
    });

    form.on('file', function (name, file) {
        console.log('Uploaded ' + file.name);

        csv
            .fromPath("./public/uploads/data.csv")
            .on("data", function (data) {
                dataset.push(data);
            })
            .on("end", function () {
                console.log("done");
                for (var j = 0; j < dataset[0].length; j++) {
                    features.push(dataset[0][j]);
                }
            });
    });
});




let users = require('./routes/users');
app.use('/users', users);

app.listen(port, () => console.log(`visualbox listening on port ${port}!`))