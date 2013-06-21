#!/usr/bin/env python

# -*- coding: UTF-8 -*-

import sys
import re
import requests
from bs4 import BeautifulSoup
from xlsxwriter.workbook import Workbook

# Login in the intranet
def login(username, password):
	r = requests.post('https://fee.heig-vd.ch/etudiants/index.php', data={'username': username, 'password': password})

	if r.status_code == 200:
		soup = BeautifulSoup(r.text)

		if soup.find('a', {'href': '/etudiants/index.php?delog=true'}) != None:
			return r
		else:
			return False

# Get & parse notes from the intranet
def getNotes(prevR):

	r = requests.get('https://fee.heig-vd.ch/etudiants/bulletinNotes.php', cookies=prevR.cookies)

	soup = BeautifulSoup(r.text)

	notes = []

	# Parse modules names
	for moduleName in soup.find_all('h3'):
		notes.append({
			'moduleName': re.sub(r'\(.+\)', '', moduleName.get_text()).strip(),
			'units': []
		})

	# Parse all modules data
	moduleI = 0
	for moduleEl in soup.find_all('table', {'class': 'tableBulletin'}):

		unitI = 0
		for lineEl in moduleEl.find_all('tr'):
			unitEl = lineEl.find('td', {'class': 'nomUnite'})

			if unitEl != None:

				unitName = unitEl.get_text().strip()

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

				# Parse notes
				noteI = 0
				for noteEl in unitNotes:
					note = noteEl.get_text().strip()

					if note == '&nbsp;' or note == '':
						note = 0
					else:
						note = float(note)

					# "Normal" note
					if noteI <= nbNotes - 3:
						notes[moduleI]['units'][unitI]['year']['notes'].append({
	    					'note': note,
	    					'coeff': 0
	    				});

	    			# Exa note
					elif noteI == nbNotes - 1:
						notes[moduleI]['units'][unitI]['exa']['note'] = note

					noteI += 1

				# Parse coefs.
				noteI = 0
				for coeffEl in lineEl.find_all('td', {'class': 'coefficient'}):
					coeff = coeffEl.get_text().strip()
					coeff = float(coeff.replace('%', '')) / 100

					# "Normal" note coef.
					if noteI <= nbNotes - 3:
						notes[moduleI]['units'][unitI]['year']['notes'][noteI]['coeff'] = coeff

					# Year moy coef.
					elif noteI == nbNotes - 2:
						notes[moduleI]['units'][unitI]['year']['coeff'] = coeff

					# Exa coef.
					elif noteI == nbNotes - 1:
						notes[moduleI]['units'][unitI]['exa']['coeff'] = coeff

					# Unit moy coef.
					elif noteI == nbNotes:
						notes[moduleI]['units'][unitI]['coeff'] = coeff

					noteI += 1

				unitI += 1

		moduleI += 1

	return notes

# Get the max number of notes in all units
def getMaxNbNotes(notes):
	maxNbNotes = 0

	for module in notes:
		for unit in module['units']:
			nbNotes = len(unit['year']['notes'])

			if nbNotes > maxNbNotes:
				maxNbNotes = nbNotes

	return maxNbNotes

# Generate excel formula for a given row
def getRowFormula(startCol, nbNotes, row):
	formula = ''

	for col in range(startCol, startCol+(nbNotes*2), 2):
		if formula == '':
			formula += '='
		else:
			formula += '+'

		formula += chr(ord('a') + col) + row
		formula += '*'+ chr(ord('a') + col+1) + row

	return formula

# Generate excel formula for a given col
def getColFormula(startRow, nbRows, col):
	formula = ''

	colNote = chr(ord('a') + col)
	colCoef = chr(ord('a') + col+1)

	for row in range(startRow, startRow+nbRows):
		if formula == '':
			formula += '='
		else:
			formula += '+'

		formula += colNote + str(row)
		formula += '*'+ colCoef + str(row)

	return formula

# Write XLSX file
def writeXlsx(notes):
	workbook = Workbook('Notes.xlsx')
	worksheet = workbook.add_worksheet()

	# Hide 0 in cells values
	worksheet.hide_zero()

	# Set width & height for first line & column
	worksheet.set_column(0, 0, 5)
	worksheet.set_row(0, 10)
	worksheet.set_column(1, 1, 50)

	# Define cell formats
	moduleNameFormat = workbook.add_format({'bold': 1})

	coeffFormat = workbook.add_format()
	coeffFormat.set_num_format('0.00%')
	coeffFormat.set_font_size(8)
	coeffFormat.set_align('center')

	noteFormat = workbook.add_format()
	noteFormat.set_align('center')
	noteFormat.set_border(1)
	noteFormat.set_locked(False)

	notesToDisplay = getMaxNbNotes(notes)

	# Write header row
	headerRow = [u'Nom de module/unité']
	for note in range(1, notesToDisplay+1):
		headerRow.extend(['Note '+ str(note), 'Coef.'])
	headerRow.extend([u'Année', 'Coef.', 'Exa', 'Coef.', 'Moy.', 'Coef.'])
	worksheet.write_row(1, 1, headerRow)

	xlsxRow = 3

	for module in notes:
		# Write module name, moy. formula and module coef.
		worksheet.write_string(xlsxRow, 1, module['moduleName'], moduleNameFormat)
		worksheet.write_formula(xlsxRow, 8+(notesToDisplay*2), getColFormula(xlsxRow+2, len(module['units']), 6+(notesToDisplay*2)), noteFormat)
		worksheet.write_number(xlsxRow, 9+(notesToDisplay*2), 1.0/len(notes), coeffFormat)

		xlsxRow += 1

		for unit in module['units']:
			worksheet.write_string(xlsxRow, 1, unit['name'])

			nbNotes = len(unit['year']['notes'])

			xlsxCol = 2
			for noteI in range(0, notesToDisplay):
				if noteI <= nbNotes - 1:
					worksheet.write_number(xlsxRow, xlsxCol, unit['year']['notes'][noteI]['note'], noteFormat)
					worksheet.write_number(xlsxRow, xlsxCol+1, unit['year']['notes'][noteI]['coeff'], coeffFormat)
				else:
					worksheet.write_blank(xlsxRow, xlsxCol, '')
					worksheet.write_blank(xlsxRow, xlsxCol+1, '')
				
				xlsxCol += 2

			xlsxCol -= 2

			rowN = str(xlsxRow+1)

			# Write year formula & coef.
			worksheet.write_formula(xlsxRow, xlsxCol + 2, getRowFormula(xlsxCol-notesToDisplay-1, notesToDisplay, rowN), noteFormat)
			worksheet.write_number(xlsxRow, xlsxCol + 3, unit['year']['coeff'], coeffFormat)

			# Write exa note & coef.
			worksheet.write_number(xlsxRow, xlsxCol + 4, unit['exa']['note'], noteFormat)
			worksheet.write_number(xlsxRow, xlsxCol + 5, unit['exa']['coeff'], coeffFormat)

			# Write moy formula & coef.
			worksheet.write_formula(xlsxRow, xlsxCol + 6, getRowFormula(xlsxCol+2, 2, rowN), noteFormat)
			worksheet.write_number(xlsxRow, xlsxCol + 7, unit['coeff'], coeffFormat)

			xlsxRow += 1

		xlsxRow += 1

	# Write general year formula
	worksheet.write_formula(xlsxRow, xlsxCol + 6, getColFormula(3, xlsxRow-2, xlsxCol + 8), noteFormat)

	worksheet.protect()

	workbook.close()


# MAIN
r = login(sys.argv[1], sys.argv[2])

# Check if login succeeded
if r != False:
	print "Login successfull"

	notes = getNotes(r)

	writeXlsx(notes)
else:
	print "Error while loggin in. Please check your credentials."
