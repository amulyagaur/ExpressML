const express = require('express')
const app = express()
const port = 3050
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
var filename;

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
app.get('/mainpage', function (req, res) {
    if (req.user) {
        res.render('index');
    }
    else {
        req.flash('error', "Please Login");
        res.redirect('/users/login');
    }
});

app.get('/visualize', function (req, res) {
    if (req.user) {
        res.render('visual', {
            features: features
        });
    }
    else {
        req.flash('error', "Please Login");
        res.redirect('/users/login');
    }
});

app.get('/analyze', function (req, res) {

    if (req.user) {
        res.render('analyze', {
            features: features,
                    traintime: '',
                    accuracy: '',
                    type: '',
                    flag: 0,
                    flag1: 0,
                    hp: '',
                    user: req.user,
                    bestf:'',
                    xyz:''
        });
        
    }
    else {
        req.flash('error', "Please Login");
        res.redirect('/users/login');
    }
});
app.post('/predict', function (req, res) {
    var msg = [];
    var MyData = [];
    var label = req.body.predictLabel;
    for (var i = 0; i < features.length; i++)
        if (features[i] != label)
            MyData.push(features[i]);

    if (MyData.length == features.length) {
        req.flash('error', 'Enter a valid label');
        res.redirect('/analyze');
    }
    var value = req.body.predict;
    if (value >= features.length) {
        req.flash('error', 'Enter a valid value (< no. of features)');
        res.redirect('/analyze');
    }
    console.log(value);

    var scriptfile = 'scripts/script_SelectKBest.py';
    var str = JSON.stringify(MyData);
    console.log(filename)
    str = str + "\n" + label + "\n" + filename + "\n" + value;
    console.log(str)
    var pyshell = new PythonShell(scriptfile);
    pyshell.send(str);

    pyshell.on('message', function (message) {
        // received a message sent from the Python script (a simple "print" statement)
        //console.log(message);
        msg.push(message);
    });

    // end the input stream and allow the process to exit
    pyshell.end(function (err, code, signal) {
        if (err)
            throw err;
        console.log('finished');
        console.log(msg);
        for( var i=0; i< msg.length ; i++)
            console.log(msg[i]);
        var x1 = msg[1];
        x1 = x1.substr(1,x1.length-2);
        var select=[];
        for( var i=0;i<x1.length;i++)
            {
                select.push(MyData[x1[i]]);
            }
        res.render('analyze', {
         features: features,
                    traintime: '',
                    accuracy: '',
                    type: '',
                    flag: 1,
                    flag1: '',
                    hp: '',
                    user: req.user,
                    bestf:select,
                    xyz:'Selected Features'
                });
    });
     
    
});

app.post('/analyze', function (req, res) {
    var msg = [];
    var MyData = req.body.feature;
    var label = req.body.label;
    var type = req.body.type;
    var classifier, regressor;

    console.log(type);
    if (type == 'on') {
        
        msg.push("regression");
        type = "checked";
        regressor = req.body.regressor;
    }
    else {
        msg.push("classification");
        type = "unchecked";
        classifier = req.body.classifier;
    }
    console.log(classifier);
    console.log(regressor);
    var scriptfile;
    if ((typeof classifier == undefined) && (typeof regressor == undefined)) {
        req.flash('error', 'Select a model first');
        res.redirect('/analyze');
    }

    else
        if (MyData.length == 0) {
            req.flash('error', 'Select atleast one feature');
            res.redirect('/analyze');
        }
        else {
            str = JSON.stringify(MyData);
            console.log(filename)
            str = str + "\n" + label + "\n" + filename;
            console.log(str);
            if (type == "checked")
                scriptfile = regressor;
            else
                scriptfile = classifier;
            if (type == "unchecked")
                scriptfile = 'scripts/classifiers/' + scriptfile + '.py';
            else
                scriptfile = 'scripts/regressors/' + scriptfile + '.py';

            var pyshell = new PythonShell(scriptfile);
            pyshell.send(str);

            pyshell.on('message', function (message) {
                // received a message sent from the Python script (a simple "print" statement)
                //console.log(message);
                msg.push(message);
            });

            // end the input stream and allow the process to exit
            pyshell.end(function (err, code, signal) {
                if (err)
                    throw err;
                console.log('finished');
                console.log(msg);

                for (var i = 0; i < msg.length; i++) {
                    console.log(i);
                    console.log("\n");
                    console.log(msg[i]);
                    console.log("\n");
                }
                var acc = msg[1];
                var f1 = 0;
                if (classifier == "SBC" || regressor=="SBR") {
                    acc = acc.substr(1, acc.length - 2);

                    acc = acc.replace(/\(/g, '');

                    acc = acc.replace(/\)/g, '');

                    acc = acc.split(',');
                    f1 = 1;
                }

                var t_time = msg[3];
                if (classifier == "SBC" || regressor=="SBR") {
                    t_time = t_time.substr(1, t_time.length - 2);
                    t_time = t_time.split(',');
                }
                res.render('analyze', {
                    features: features,
                    traintime: t_time,
                    accuracy: acc,
                    type: type,
                    flag: 1,
                    flag1: f1,
                    hp: msg[2],
                    user: req.user,
                    bestf:'',
                    xyz:classifier || regressor
                });

            });
        }
});

app.post('/file', function (req, res) {
    var form = new formidable.IncomingForm();
    features = [];
    dataframe = [];
    dataset = [];
    form.parse(req);

    form.on('fileBegin', function (name, file) {
        file.name = req.user.username + '.csv';
        file.path = __dirname + '/public/uploads/' + file.name;
        filename = file.path;
    });

    form.on('file', function (name, file) {
        console.log('Uploaded ' + file.name);

        csv
            .fromPath("./public/uploads/" + req.user.username + ".csv")
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