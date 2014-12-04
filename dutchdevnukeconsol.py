#===============================================================================
#
#	Author  : Pmg Lemmen
#	Company : Dutchdevelopers
#	email   : peter@dutchdevelopers.nl
#	Date    : 13/12/12
#	Mod     : 4/12/14
#
#    
#    Paste the followin items in menu.py
#
#    #Collect Files Menu Node
#    collectMenu = nuke.menu("Nodes").addMenu("Consolidator")
#    collectMenu.addCommand('make backup ', 'dutchdevscripts.dutchdevscripts()')
#    collectMenu.addCommand('Help', 'dutchdevscripts.Help()')
#    collectMenu.addCommand('Manual', 'dutchdevscripts.Manual()')
#
#    add import dutchdevnukeconsol to init.py
#
#
#
#
#===============================================================================


import nuke
import os
import sys
import shutil
import re
import threading
import time
import webbrowser



##############################################################
##
##  Prepare system for writing slashes etc.
##
##############################################################

plemke_version     = "v1.0.12 2012 "
only_enabled_nodes = False
slash = '/'
project_file_name = ""
project_file_dir  = ""
backup_root_dir  	= "e:/backup/"
backup_project_dir  	= "backup1"
handlesize	  	= 0
errorcnt 		= 0;




def SetWindows():
    global slash
    slash = '/'

def SetLinux():
    global slash
    slash = '/'

def SetMac():
    global slash
    slash = '/'

def open_log_file( projectname ):
	global backup_root_dir
	global backup_project_dir

	node_dir = backup_root_dir + '/' + backup_project_dir + '/backup_info.txt'

	myfile = open( node_dir, "w" ) 

	myfile.write( "#################################################################################\n");
	myfile.write( "#    \n" );
	myfile.write( "#    Version    : " + plemke_version + "\n");
	myfile.write( "#    Author     : Pmg Lemmen \n");
	myfile.write( "#    project    : " + projectname + "\n" );
	myfile.write( "#    \n" );
	myfile.write( "#################################################################################\n");
	myfile.close()

def write_log_file( text ):
	global backup_root_dir
	global backup_project_dir

	node_dir = backup_root_dir + '/'+ backup_project_dir + '/backup_info.txt'
	myfile = open( node_dir , "a" ) 
	myfile.write( text+"\n");
	myfile.close()



##############################################################

def SystemInit():
    global platform
    global root




    platform = os.name

  
    if platform == "nt":
	SetWindows()
 
    if platform == "mac":
	SetMac()
    
    if platform == "linux":
	SetLinux()




##############################################################

def Help():
    url = 'http://www.dutchdevelopers.nl/'
    webbrowser.open_new(url)


##############################################################

def Manual():
    url = 'http://www.dutchdevelopers.nl/nukemanual'
    webbrowser.open_new(url)

##############################################################

def collectPanel():
    colPanel = nuke.Panel("Consolidator")
    colPanel.addFilenameSearch("Output Path:", "")
    colPanel.addButton("Cancel")
    colPanel.addButton("OK")

    retVar 	= colPanel.show()
    pathVar 	= colPanel.value("Output Path:")

    return (retVar, pathVar)




##############################################################

def convert_file_to_relative( inname ):
    nuke.message( inname )



##############################################################
#

def prepare_current_project():
    global globalprogress
    global project_file_name
    global project_file_dir
    global backup_root_dir
    global backup_project_dir 
    global backup_project_name 

    nuke.selectAll();

    errorcnt 		= 0;

    backup_project_name = backup_root_dir + '/' + backup_project_dir 


    if os.path.lexists( backup_root_dir ) == False:
	os.mkdir( backup_root_dir )

    if os.path.lexists( backup_project_name ) == False:
	os.mkdir( backup_project_name )



    project_fps       = nuke.Root()['fps'].value()
    project_file_name = nuke.Root()['name'].value()
    project_file_dir  = nuke.root()['project_directory'].value() ;

    
    if  project_file_dir != "" :
        project_file_dir  = nuke.root()['project_directory'].value() + '/';
#//	+ '/'


    globalprogress = nuke.ProgressTask("Plemkes consolidator")
    globalprogress.setProgress(0)

    return 0


def ok_to_backup( anode ):
    global only_enabled_nodes


    if only_enabled_nodes == False:
	return True

    if anode['disable'].value() == True:
        return False

    return True





def make_node_dir( inode ):
	global plemke_version
	global backup_root_dir
	global backup_project_name 

	node_name = inode['name'].value()

	node_dir = backup_root_dir + '/' +  backup_project_dir + '/'+ node_name
	
        if os.path.lexists( node_dir ) == False:
	   os.mkdir( node_dir )

	myfile = open( node_dir+'/'+node_name+'_info.txt', "w" ) 
	myfile.write( "#################################################################################\n");
	myfile.write( "#    \n" );
	myfile.write( "#    Version    : " + plemke_version + "\n");
	myfile.write( "#    Author     : Pmg Lemmen \n");
	myfile.write( "#    nodename   : " + node_name + "\n" );
	myfile.write( "#    Org path   : " + inode['file'].value()+ "\n"  );
	myfile.write( "#    \n" );
	myfile.write( "#################################################################################\n");
	myfile.close()

	return node_dir



def backup_image_sequence( inode ):
	global errorcnt
	global handlesize
	dest = make_node_dir( inode )

	first = inode['first'].value() - int( handlesize );
	last  = inode['last'].value() + int( handlesize );
	total = last-first

	deler = 1.0/total


	frame_range = range( first , last )

	filename = inode['file'].value();

        globalprogress.setMessage( "backup Node : "+inode['name'].value() + " "+str(total ) + " Frames \n")


	for frame in frame_range :

            globalprogress.setMessage( "Frame "+str(frame-first) + " from " +str(total ) + " Frames \n")
	    if globalprogress.isCancelled():
		break

	    newfilename = filename % frame
   	    source_file = project_file_dir + newfilename 

            if os.path.lexists( source_file ) == False:
	       errorcnt = errorcnt + 1
	       write_log_file( "Missing source in sequence : "+source_file )
	    else:
               if os.path.lexists( dest+'/'+ os.path.basename( newfilename ) ) == False:
	          shutil.copy(  source_file , dest )
		  a=0
            
	    pos = 100.0 * deler * ( frame - first )
	    globalprogress.setProgress( int( pos ) )

	file_name = os.path.basename( filename )
	new_path = inode.knob('name').value() + slash + file_name
	inode.knob('file').setValue( new_path );


def backup_image_file( inode ):
	global errorcnt
	dest 	  = make_node_dir( inode )
	filename  = inode['file'].value();


        globalprogress.setMessage( "backup Node : "+inode['name'].value() )

   	source_file = project_file_dir + filename 
        if os.path.lexists( source_file ) == False:
	   errorcnt = errorcnt + 1
	   write_log_file( "Missing source : "+source_file )
	else:
	   shutil.copy(  source_file , dest )

	file_name = os.path.basename( filename )
	new_path = inode.knob('name').value() + slash + file_name
	inode.knob('file').setValue( new_path );

def backup_audio_file( inode ):
	global errorcnt
	dest 	  = make_node_dir( inode )
	filename  = inode['file'].value();


        globalprogress.setMessage( "backup Node : "+inode['name'].value() )

   	source_file = project_file_dir + filename 
        if os.path.lexists( source_file ) == False:
	   errorcnt = errorcnt + 1
	   write_log_file( "Missing source : "+source_file )
	else:
	   shutil.copy(  source_file , dest )

	file_name = os.path.basename( filename )
	new_path = inode.knob('name').value() + slash + file_name
	inode.knob('file').setValue( new_path );


def backup_geo_file( inode ):
	global errorcnt
	dest 	  = make_node_dir( inode )
	filename  = inode['file'].value();


        globalprogress.setMessage( "backup Node : "+inode['name'].value() )

   	source_file = project_file_dir + filename 
        if os.path.lexists( source_file ) == False:
	   errorcnt = errorcnt + 1
	   write_log_file( "Missing source : "+source_file )
	else:
	   shutil.copy(  source_file , dest )

	file_name = os.path.basename( filename )
	new_path = inode.knob('name').value() + slash + file_name
	inode.knob('file').setValue( new_path );




def backup_movie_file( mnode ):
	global errorcnt
	dest 	  = make_node_dir( mnode )
	filename  = mnode['file'].value();

   	source_file = project_file_dir + filename 

        globalprogress.setMessage( "backup movie Node : "+mnode['name'].value() )

	nuke.message( source_file )

        if os.path.lexists( source_file ) == False:
	   errorcnt = errorcnt + 1
	   write_log_file( "Missing source : "+source_file )
	else:
	   shutil.copy(  source_file , dest )

	file_name = os.path.basename( filename )
	new_path = mnode.knob('name').value() + slash + file_name
	mnode.knob('file').setValue( new_path );






def read_root_item( items ):
	nuke.message( items['name'].value() )









def read_graphic_node( items ):

        if ok_to_backup( items ) == False :
	   return False


	chars = set('%#')
	first = items['first'].value();
	last  = items['last'].value();
	total = last - first

	media_type = "unknown"

	if total > 0 :
		filename = items['file'].value()

		if any( (c in chars ) for c in filename  ):
			backup_image_sequence( items )
		else:
			backup_movie_file( items )
	else:
		backup_image_file( items )








def read_viewer_node( vnode ):
    global	only_enabled_nodes







def read_audio_node( anode ):
    global	only_enabled_nodes

    if ok_to_backup( anode ) == True :
       backup_audio_file( anode )








def read_geo2_node( anode ):
    global	only_enabled_nodes

    if ok_to_backup( anode ) == True :
       backup_geo_file( anode )




def read_node( nodename , node ):

    if nodename == 'Root':
        read_root_node( node )
    elif nodename == 'Viewer':
        read_viewer_node( node )
    elif nodename == 'ReadGeo':
        read_geo2_node( node )
    elif nodename == 'ReadGeo2':
        read_geo2_node( node )
    elif nodename == 'AudioRead':
        read_audio_node( node )
    elif nodename == 'Read':
        read_graphic_node( node )


##############################################################
# Parent Function

def dutchdevscripts():
    global  globalprogress
    global  only_enabled_nodes
    global  backup_project_dir
    global  backup_root_dir
    global  handlesize
    global  plemke_version

    dpan = nuke.Panel( "Where to save?");
    dpan.setWidth( 300 );
    dpan.setTitle( "plemkes consolidator  "+plemke_version );
    dpan.addBooleanCheckBox( "backup enabled nodes only" , False );
    dpan.addSingleLineInput( "Handle size" , str( handlesize ) );
    dpan.addFilenameSearch( "Folder Path" , "Select backup folder" );
    dpan.addSingleLineInput( "Backup name" , "NKBK_0001" );


    if dpan.show() == 1 :
        backup_root_dir  	= dpan.value('Folder Path' )
        backup_project_dir  	= dpan.value('Backup name' )
    else:
	nuke.message('You have to select a backup directory ')
	return 0

    only_enabled_nodes = dpan.value('backup enabled nodes only' )
    handlesize = dpan.value('Handle size' )

    prepare_current_project()

    backup_project_name = 'backup_'+ os.path.basename( project_file_name ) 

    open_log_file( backup_project_name  )


    for items in nuke.allNodes():
	bla = items.Class()

	read_node( bla , items )


#### for some strange reasons it skipped reads


    new_project_directory = backup_root_dir+'/'+backup_project_dir

    setting_proj_dir = nuke.root()['project_directory']
    setting_proj_dir.setValue( new_project_directory )


    out_name = backup_root_dir + '/'+ backup_project_dir + '/' + backup_project_name

    nuke.scriptSave( out_name )

    node_dir = backup_root_dir + '/' + backup_project_dir + '/backup_info.txt'
    nuke.message( "Backup Done\nThere are "+ str( errorcnt ) + " Errors \nErrors are mostly missing source files\nOpen "+node_dir + " to check the errors ")

    del globalprogress

    return 1

##############################################################
#

SystemInit()
