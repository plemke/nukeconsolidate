
	Author    : Pmg Lemmen
	Company   : Dutchdevelopers
	email     : peter@dutchdevelopers.nl
	Date      : 13/12/12
	Copyright : Peter Mg Lemmen All rights reserved



    Consolidate tool for Foundry Nuke.

    rename the pyton file to dutchdevscripts.py 
    and copy it in the plugins directory
    
    
    
    Paste the followin items in menu.py at the end

    #Collect Files Menu Node
      collectMenu = nuke.menu("Nodes").addMenu("plemkes consolidator")
      collectMenu.addCommand('make backup ', 'dutchdevscripts.dutchdevscripts()')
      collectMenu.addCommand('Help', 'dutchdevscripts.Help()')
      collectMenu.addCommand('Manual', 'dutchdevscripts.Manual()')

    add the following line to init.py
    import dutchdevscripts
