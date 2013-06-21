#!/usr/bin/env python

import sys
import re
import requests
from bs4 import BeautifulSoup
from xlsxwriter.workbook import Workbook

def login(username, password):
	r = requests.post('https://fee.heig-vd.ch/etudiants/index.php', data={'username': username, 'password': password})

	soup = BeautifulSoup(r.text)

	if soup.find('a', {'href': '/etudiants/index.php?delog=true'}) != None:
		return r
	else:
		return False

def getNotes(prevR):

	r = requests.get('https://fee.heig-vd.ch/etudiants/bulletinNotes.php', cookies=prevR.cookies)

	soup = BeautifulSoup(r.text)

	notes = []

	for moduleName in soup.find_all('h3'):
		notes.append({
			'moduleName': re.sub(r'\(.+\)', '', moduleName.get_text()).strip(),
			'units': []
		})

	moduleI = 0
	for moduleEl in soup.find_all('table', {'class': 'tableBulletin'}):

		print "----------------------------------------------"
		print " "+ notes[moduleI]['moduleName']
		print "----------------------------------------------"

		unitI = 0
		for lineEl in moduleEl.find_all('tr'):
			unitEl = lineEl.find('td', {'class': 'nomUnite'})

			if unitEl != None:

				unitName = unitEl.get_text().strip()

				print "   "+ unitName

				notes[moduleI]['units'].append({
					'name': unitName,
					'coeff': 0,
					'year': {
						'notes': [],
						'coeff': 0
					},
					'exa': {
						'note': 0,
						'coeff': 0
					}
				})

				unitNotes = lineEl.find_all('td', {'class': 'noteTest'})
				nbNotes = len(unitNotes) - 1

				noteI = 0
				for noteEl in unitNotes:
					note = noteEl.get_text().strip()

					if note == '&nbsp;' or note == '':
						note = 0
					else:
						note = float(note)

					if noteI <= nbNotes - 3:
						notes[moduleI]['units'][unitI]['year']['notes'].append({
	    					'note': note,
	    					'coeff': 0
	    				});
					elif noteI == nbNotes - 1:
						notes[moduleI]['units'][unitI]['exa']['note'] = note

					noteI += 1

				noteI = 0
				for coeffEl in lineEl.find_all('td', {'class': 'coefficient'}):
					coeff = coeffEl.get_text().strip()
					coeff = float(coeff.replace('%', '')) / 100

					if noteI <= nbNotes - 3:
						notes[moduleI]['units'][unitI]['year']['notes'][noteI]['coeff'] = coeff
					elif noteI == nbNotes - 2:
						notes[moduleI]['units'][unitI]['year']['coeff'] = coeff
					elif noteI == nbNotes - 1:
						notes[moduleI]['units'][unitI]['exa']['coeff'] = coeff
					elif noteI == nbNotes:
						notes[moduleI]['units'][unitI]['coeff'] = coeff

					noteI += 1


				print ""

				unitI += 1

		moduleI += 1

	return notes

def writeXlsx(notes):
	workbook = Workbook('Notes.xlsx')
	worksheet = workbook.add_worksheet()

	xlsxRow = 0

	for module in notes:
		worksheet.write_string(xlsxRow, 0, module['moduleName'])
		
		xlsxRow += 1

		for unit in module['units']:
			worksheet.write_string(xlsxRow, 0, unit['name'])

			nbNotes = len(unit['year']['notes'])

			xlsxCol = 1
			for noteI in range(0, 4):
				if noteI <= nbNotes - 1:
					worksheet.write_number(xlsxRow, xlsxCol, unit['year']['notes'][noteI]['note'])
					worksheet.write_number(xlsxRow, xlsxCol+1, unit['year']['notes'][noteI]['coeff'])
				else:
					worksheet.write_blank(xlsxRow, xlsxCol, '')
					worksheet.write_blank(xlsxRow, xlsxCol+1, '')
				
				xlsxCol += 2

			rowN = str(xlsxRow+1)

			worksheet.write_formula(xlsxRow, xlsxCol + 2, '=B'+rowN+'*C'+rowN +'+D'+rowN+'*E'+rowN +'+F'+rowN+'*G'+rowN +'+H'+rowN+'*I'+rowN +'+J'+rowN+'*K'+rowN)
			worksheet.write_number(xlsxRow, xlsxCol + 3, unit['year']['coeff'])

			worksheet.write_number(xlsxRow, xlsxCol + 4, unit['exa']['note'])
			worksheet.write_number(xlsxRow, xlsxCol + 5, unit['exa']['coeff'])

			worksheet.write_formula(xlsxRow, xlsxCol + 6, '=L'+rowN+'*M'+rowN +'+N'+rowN+'*O'+rowN)
			worksheet.write_number(xlsxRow, xlsxCol + 7, unit['coeff'])

			xlsxRow += 1

	workbook.close()


r = login(sys.argv[1], sys.argv[2])

if r != False:
	print "Login successfull"

	notes = getNotes(r)

	writeXlsx(notes)
else:
	print "Error while loggin in. Please check your credentials."