var util = require('util'),
	querystring = require('querystring'),
	request = require('request'),
	cheerio = require('cheerio');

var loginInfos = {
	username: process.argv[2],
	password: process.argv[3]
}

var cookieJar = request.jar();

var modulesNotes = [];

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
    	$('table.tableBulletin').each(function(moduleI, moduleEl) {
    		var $moduleEl = $(this);

    		var moduleName = $moduleEl.prev().text().replace(/\(.+\)/gi, '').trim();
    		console.log('----------------------------------------------');
    		console.log(' '+ moduleName);
    		console.log('----------------------------------------------');

    		modulesNotes[moduleI] = {
				module: moduleName,
				units: []
			};

    		// Loop over each units
    		var unitI = 0;
    		$moduleEl.find('tr').each(function(i, unitEl) {
    			var $unitEl = $(this);

    			// Is it a unit ?
    			var unitName = $unitEl.find('td.nomUnite').text().trim();
    			if(unitName != '') {

    				console.log('   '+ unitName);

    				// Unit structure
    				modulesNotes[moduleI].units[unitI] = {
						unit: unitName,
						coeff: 0,
						year: {
							notes: [],

							coeff: 0
						},
						exa: {
							note: 0,
							coeff: 0
						}
					};

    				// Get notes
		    		var $unitNotes = $unitEl.find('td.noteTest');
		    		var nbNotes = $unitNotes.length - 1;

		    		$unitNotes.each(function(noteI, noteEl) {
		    			var $noteEl = $(this);

		    			// Get & parse note
		    			var note = $noteEl.text().trim();
		    			if(note == '&nbsp;' || note == '') {
		    				note = '';
		    			} else {
		    				note = parseFloat(note);
		    			}

		    			// Get & parse coeff
		    			var $coeffEl = $noteEl.next();
		    			var coeff = parseFloat($coeffEl.text().replace('%', '').trim()) / 100;

		    			// Notes
		    			if(noteI <= nbNotes - 3) {
		    				modulesNotes[moduleI].units[unitI].year.notes.push({
		    					note: note,
		    					coeff: coeff
		    				});

		    			// Year coeff
		    			} else if(noteI == nbNotes - 2) {
		    				modulesNotes[moduleI].units[unitI].year.coeff = coeff;

		    			// Exa
		    			} else if(noteI == nbNotes - 1) {
		    				modulesNotes[moduleI].units[unitI].exa = {
		    					note: note,
		    					coeff: coeff
		    				};

		    			// Final unit coeff
		    			} else if(noteI == nbNotes) {
		    				modulesNotes[moduleI].units[unitI].coeff = coeff;
		    			}
		    			
		    		});

    				unitI++;

		    		console.log('');
    			}
    		});
    	});

		callback(moduleNotes);
    });
}

var writeOutput = function(notes) {
	
}

login(function(error) {
	if(error) { console.log(error); return; }

	getNotes(function(notes) {

	});
});

var notesExample = [
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
				},

				exa: {
					note: 5,
					coeff: 0.5
				}
			}
		]
	}
];
