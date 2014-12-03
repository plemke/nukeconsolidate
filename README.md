
	Author  : Pmg Lemmen
	Company : Dutchdevelopers
	email   : peter@dutchdevelopers.nl
	Date    : 13/12/12


    Paste the followin items in menu.py

    Collect Files Menu Node
    collectMenu = nuke.menu("Nodes").addMenu("plemkes bud")
    collectMenu.addCommand('make backup ', 'dutchdevscripts.dutchdevscripts()')
    collectMenu.addCommand('Help', 'dutchdevscripts.Help()')
    collectMenu.addCommand('Manual', 'dutchdevscripts.Manual()')

    add import dutchdevscripts to init.py
