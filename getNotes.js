var request = require('request'),
	cheerio = require('cheerio'),
	querystring = require('querystring');

var loginInfos = {
	username: process.argv[2],
	password: process.argv[3]
}

var cookieJar = request.jar();

var login = function(callback) {
	request.post({
	    uri: 'https://fee.heig-vd.ch/etudiants/index.php',
	    headers: {'content-type': 'application/x-www-form-urlencoded'},
	    body: querystring.stringify(loginInfos),
	    jar: cookieJar
    },
    function(err, res, body) {
    	var $ = cheerio.load(body);

    	if($('a[href="/etudiants/index.php?delog=true"]').length > 0) {
    		callback(null);
    	} else {
    		callback('Error while loggin in. Please check your credentials.');
    	}
    });
}

var getNotes = function(callback) {
	request.get({
	    uri: 'https://fee.heig-vd.ch/etudiants/bulletinNotes.php',
	    jar: cookieJar
    },
    function(err, res, body) {
    	var $ = cheerio.load(body);

    	// Loop over each modules
    	$('table.tableBulletin').each(function(i, torrentEl) {
    		
    	});
    });
}

var notes = [
	{
		module: '',
		units: [
			{
				unit: '',
				year: {
					notes: [
						{
							note: 5,
							coeff: 0.5
						}
					],

					coeff: 0.5
				}

				exa: {
					note: 5,
					coeff: 0.5
				}
			}
		]
	}
];
