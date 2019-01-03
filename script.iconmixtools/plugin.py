# coding: utf-8
#from __future__ import unicode_literals
import resources.lib.Utils as utils
from resources.lib.Utils import logMsg
import resources.lib.mainservice as MainService
from unidecode import unidecode
from datetime import datetime,timedelta
import _strptime
import urlparse,urllib
import time
from time import sleep
import unicodedata
import os
import xbmc,xbmcgui,xbmcaddon,xbmcplugin
import random
import MonAutoCompletion
import shutil

#containers :
#1998 : Acteurs
#1999 : éléments des sagas, des acteurs et réalisateurs, et artistes (musique)


# Script constantes
ADDON = xbmcaddon.Addon()
__addonid__    = ADDON.getAddonInfo('id')
__version__    = ADDON.getAddonInfo('version')
__language__   = ADDON.getLocalizedString
__skin_string__ = xbmc.getLocalizedString
__cwd__        = ADDON.getAddonInfo('path')  
ADDON_ID = ADDON.getAddonInfo('id').decode("utf8")
ADDON_ICON = ADDON.getAddonInfo('icon').decode("utf8")
ADDON_NAME = ADDON.getAddonInfo('name').decode("utf8")
ADDON_PATH = ADDON.getAddonInfo('path').decode("utf8")
ADDON_VERSION = ADDON.getAddonInfo('version').decode("utf8")
ADDON_DATA_PATH = xbmc.translatePath("special://profile/addon_data/%s" % ADDON_ID).decode("utf8")
SETTING = ADDON.getSetting
KODI_VERSION  = int(xbmc.getInfoLabel( "System.BuildVersion" ).split(".")[0])
ACTION_PREVIOUS_MENU = (9, 10, 92, 216, 247, 257, 275, 61467, 61448)

class Main:
    def __init__( self ):
        
        self._init_vars()
        self.ui=None
        self.windowhome.setProperty("IconMixDataPath",ADDON_DATA_PATH)
        
      
        #get params
        action = None
        try:
           params = urlparse.parse_qs(sys.argv[2][1:].decode("utf-8"))
          
           if params: 
              #logMsg("Appel Plugin : %s" %(params),0)       
              path=params.get("path",None)
              if path: path = path[0]
              limit=params.get("limit",None)
              if limit: limit = int(limit[0])
              else: limit = 25
              action=params.get("action",None)
              if action: action = action[0].upper()
              
          
           if action: 
            
               
               
               if action == "ICONMIXNEXTAIRED":
                   try:
                      windowhome = xbmcgui.Window(10000)  
                   except:
                      windowhome=None               
                   if windowhome:
                     cpt=0
                     while cpt<50:
                        if windowhome.getProperty('MonNextAired.Actif')!='oui':
                          Episodes=utils.GetNextEpisodesKodi()  
                          if Episodes:
                              xbmcplugin.addDirectoryItems(int(sys.argv[1]), Episodes)
                          xbmcplugin.endOfDirectory(int(sys.argv[1]))  
                          cpt=50
                        else:
                          xbmc.sleep(500)
                        cpt=cpt+1
               if action == "ICONMIXMOVIEPROGRESS":                  
                          Liste=utils.GetProgress("movie")  
                          if Liste:
                              xbmcplugin.addDirectoryItems(int(sys.argv[1]), Liste)
                          xbmcplugin.endOfDirectory(int(sys.argv[1]))  
                          
               if action == "ICONMIXTVPROGRESS":                  
                          Liste=utils.GetProgress("tvshow")  
                          if Liste:
                              xbmcplugin.addDirectoryItems(int(sys.argv[1]), Liste)
                          xbmcplugin.endOfDirectory(int(sys.argv[1]))
               if action == "ICONMIXEPISODEPROGRESS":                  
                          Liste=utils.GetProgress("episode")  
                          if Liste:
                              xbmcplugin.addDirectoryItems(int(sys.argv[1]), Liste)
                          xbmcplugin.endOfDirectory(int(sys.argv[1]))   
                  
               if action == "GETGENRELIST":
                  Id=params.get("id",None)
                  if Id: Id = Id[0] 
                  genretype=params.get("genretype",None)
                  if genretype: genretype = genretype[0]
                  utils.getGenreListe(Id,genretype)
            
              
                  
                             
               
                  
               
               
               
        except:
          params= {}
        
        try:
            params = dict( arg.split( '=' ) for arg in sys.argv[ 1 ].split( '&' ) )
        except:
            params = {}
        
          
        self.setview = params.get( 'setview', False )
        self.setviewmenu = params.get( 'setviewmenu', False )
        if self.setviewmenu:
          self.idview=params.get( 'id', None )
          
        self.videcache = params.get( 'videcache', False )
        self.addplaylist = params.get( 'addplaylist', False )
        self.supplaylist = params.get( 'supplaylist', False )
        self.updateallmusic = params.get( 'updateallmusic', False )
        self.mettreajour = params.get( 'mettreajour', False )
        if self.mettreajour:
           self.mettreajourID = params.get( 'id', False )
           self.mettreajourLABEL = params.get( 'label', False )
           self.mettreajourTYPE = params.get( 'type', False )
        self.backend = params.get( 'backend', False )
        self.updateacteursinf = params.get( 'updateacteursinf', False )
        if self.updateacteursinf:
          self.itemidkodi=params.get( 'idkodi', None )
          self.itemidtmdb=params.get( 'idtmb', None )
        self.togglewatchedepisode = params.get( 'togglewatchedepisode', None )
        self.itemidkodiepisode=params.get( 'idepisode', None )
        self.togglewatched=params.get('togglewatched',False)
        self.showinfo = params.get( 'showinfo', False )
        self.PurgeDatabase =  params.get( 'purgedatabase', False )
        self.PurgeDatabaseManuel =  params.get( 'purgedatabasemanuel', False )
        
        self.Positionnement = params.get( 'position', None )
        
        if self.Positionnement :
         
          self.ui = MainService.dialog_SelectPosition('position.xml', ADDON_PATH, 'default','1080i')
          ret=self.ui.doModal()
          del self.ui 
          
        
        
        if self.togglewatchedepisode and self.itemidkodiepisode:
          self.windowhome.clearProperty('IconmixProchainEpisode')
          if self.togglewatched=="True":
           json_result = utils.setJSON('VideoLibrary.SetEpisodeDetails', '{ "episodeid":%d,"resume":{"position":0,"total":0},"playcount":1 }' %(int(self.itemidkodiepisode)))                          
          else:
           json_result = utils.setJSON('VideoLibrary.SetEpisodeDetails', '{ "episodeid":%d,"resume":{"position":0,"total":0},"playcount":0 }' %(int(self.itemidkodiepisode)))                          
          self.windowhome.setProperty('IconMixUpdateEpisodes','1')
        
        
        #purge des series orphelines sans épisodes.....
        if self.PurgeDatabase and (SETTING("autopurge")=="true" or self.PurgeDatabaseManuel):
          
          try:
           from sqlite3 import dbapi2 as sqlite
          
          except:
              from pysqlite2 import dbapi2 as sqlite

          DB = os.path.join(xbmc.translatePath("special://database"), 'MyVideos107.db')
          db = sqlite.connect(DB)
          db.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])
          rows = db.execute('SELECT idShow,totalCount FROM tvshowcounts WHERE totalCount is NULL') 
          items=rows.fetchall()
          dialog=xbmcgui.Dialog() 
          Choix=["Toutes"]
          DelListe=[{"idShow":None,"idPath":None,"path":None}]
          for item in items:
            rows = db.execute('SELECT idShow,c00 FROM tvshow WHERE idShow="%s"' %(item["idShow"])) 
            TvShowItem=rows.fetchone()
            rows = db.execute('SELECT idShow,idPath FROM tvshowlinkpath WHERE idShow="%s"' %(item["idShow"])) 
            TvShowLinkPath=rows.fetchone()
            rows = db.execute('SELECT idPath,strPath FROM path WHERE idPath="%s"' %(TvShowLinkPath["idPath"])) 
            TvShowPath=rows.fetchone()
           
            Choix.append("%s=%s" %(TvShowItem["c00"],TvShowPath["strPath"]))
            DelListe.append({"idShow":item["idShow"],"idPath":TvShowLinkPath["idPath"],"path":TvShowPath["strPath"]})
            
          if len(Choix)>1:
            if self.PurgeDatabaseManuel:
               ret=dialog.multiselect("Series orphelines", Choix)
            else:
               ret=[0]
            if ret and len(ret)>0:
              if ret[0]==0:    
                for item in range(1,len(DelListe)):                
                  db.execute('DELETE FROM tvshowlinkpath WHERE idShow = "%s"' %(DelListe[item]["idShow"]))
                  db.execute('DELETE FROM path WHERE idPath = "%s"' %(DelListe[item]["idPath"])) 
                  db.execute('DELETE FROM tvshow WHERE idShow = "%s"' %(DelListe[item]["idShow"])) 
                  db.commit() 
              else:    
                for item in ret:
                  db.execute('DELETE FROM tvshowlinkpath WHERE idShow = "%s"' %(DelListe[item]["idShow"]))
                  db.execute('DELETE FROM path WHERE idPath = "%s"' %(DelListe[item]["idPath"])) 
                  db.execute('DELETE FROM tvshow WHERE idShow = "%s"' %(DelListe[item]["idShow"])) 
                  db.commit() 
              #shutil.rmtree(DelListe[item]["path"])
              xbmc.executebuiltin('Container.Refresh')
              dialog.notification('IconMixTools', __language__( 32860 ), ADDON_ICON,500)
          else:
            if self.PurgeDatabaseManuel:
              dialog.notification('IconMixTools', __language__( 32861 ), ADDON_ICON,500)
              
              
          
          
       
        
        if self.videcache :
           self.quelcache = params.get( 'cache', False )
           dialogC = xbmcgui.Dialog()
           ret=dialogC.yesno("ICONMIXTOOLS CACHE !!!", __language__( 32602 )," ",str(self.quelcache).upper()) #-- Show a dialog 'YES/NO'.
           if ret>0:
             utils.vidercache(self.quelcache)
 
        else:
        
          if not action :
            saga=""   
            #------ lancer mode serveur ----------- 
            if self.backend :
              return
            # and xbmc.getCondVisibility("String.IsEmpty(Window(home).Property(IconMixToolsbackend))"):                
            #    MainService.MainService()
            
            #-------------METTRE A JOUR SAGA ou SERIE-------------
            if self.mettreajour:
                self.MiseAJour()
                    
            
            #-------------CHOIX DE LA VUE-------------             
            if self.setview:
                self.SelectionneVue()
            
            if self.setviewmenu and self.idview:
               xbmc.executebuiltin("Container.SetViewMode(%s)"  % self.idview)
             

            #{"jsonrpc":"2.0","method":"Playlist.Add","id":-2067158130,"params":{"playlistid":0,"item":{"directory":"special://profile/playlists/music/Long Tracks.xsp"}}}
            #{"jsonrpc":"2.0","method":"Player.Open","id":1877953368,"params":{"options":{"shuffled":true},"item":{"playlistid":0,"position":0}}}  
            #-------------AJOUTER A UNE PLAYLIST-------------                              
            if self.addplaylist:                     
                  utils.AddToPlayList()
            #-------------SUPPRIMER D'UNE PLAYLIST-------------                              
            if self.supplaylist:
                  utils.DelFromPlayList()
                  
            if self.updateacteursinf and self.windowhome.getProperty('IconmixShowInfo')=="1":
              ListeActeurs=self.GetControl(self.windowvideoinf,1998)                                 
              #ACTEURS  ------------------------------------------------                                 
              if ListeActeurs:
                ListeItemx=utils.getCasting("movie",self.itemidkodi,1,self.itemidtmdb)
                ListeActeurs.reset()
                if ListeItemx:
                     #logMsg("Acteursinf.....")
                     for itemX in ListeItemx:
                          ListeActeurs.addItem(itemX) 
                                                         
                status=""
              
   
            
           
    
    
    def GetControl(self,Window=None,Id=None):
          ControlId=None          
          try:
               ControlId=Window.getControl(Id)  
          except:
               ControlId=None
          return ControlId
          
        
                 
    
    def MiseAJour(self):
     
      saga=""
      logMsg("1 : %s - %s -%s" %(self.mettreajourID,self.mettreajourTYPE,self.mettreajourLABEL))
      if not self.mettreajourID:
        self.mettreajourID=xbmc.getInfoLabel("ListItem.DBID")
      if not self.mettreajourLABEL:
        self.mettreajourLABEL=xbmc.getInfoLabel("ListItem.Label")
      if not self.mettreajourTYPE:
        self.mettreajourTYPE=xbmc.getInfoLabel("ListItem.DBTYPE")
      logMsg("2: %s - %s -%s" %(self.mettreajourID,self.mettreajourTYPE,self.mettreajourLABEL))
      if xbmc.getCondVisibility("Container.Content(artists)"): 
               self.mettreajourTYPE="artist"
      if ( self.mettreajourTYPE=="set" or self.mettreajourTYPE=="movie" or self.mettreajourTYPE=="tvshow" or self.mettreajourTYPE=="artist" or self.mettreajourTYPE=="season" or saga!=""):
             if saga=="":
               Unique="ok"
             else:
               Unique=""
             
             if self.mettreajourTYPE!="season": 
               dialog = xbmcgui.Dialog()
               if self.mettreajourTYPE=="movie": 
                Titre=__skin_string__( 342 )
               if self.mettreajourTYPE=="set": 
                Titre=__skin_string__( 20434 )
               if self.mettreajourTYPE=="tvshow": 
                Titre=__skin_string__( 20343 )
               if self.mettreajourTYPE=="artist": 
                Titre=__skin_string__( 36917 )
                
               if self.mettreajourTYPE!="movie":
                 Choix=[__language__( 32502 )+Titre, __language__( 32503 )+Titre]
               else :
                 Choix=[__language__( 32510 )]
               if Unique and self.mettreajourID and not self.mettreajourTYPE=="movie": 
                 Choix.append(__language__( 32507 )+" [COLOR=yellow]"+utils.try_decode(self.mettreajourLABEL)+"[/COLOR]")
                 
               if self.mettreajourTYPE=="set"  or self.mettreajourTYPE=="movie" or self.mettreajourTYPE=="tvshow":
                   Choix.append(__language__( 32514 )+" [COLOR=yellow]"+utils.try_decode(self.mettreajourLABEL)+"[/COLOR]")
               if self.mettreajourTYPE=="tvshow":
                 Choix.append(__language__( 32511 ))
               
               ret=dialog.select(Titre, Choix)
             else:
              ret=0
             if (ret>=0):
              self.windowhome.setProperty("IconMixArt","ok")
             if ret==0: #tous
              if self.mettreajourTYPE=="set": utils.UpdateSagas(0,1)
              if self.mettreajourTYPE=="tvshow": utils.UpdateSeries(0,1)
              if self.mettreajourTYPE=="movie": utils.updateartworkall("Movies")
              if self.mettreajourTYPE=="artist": utils.UpdateArtistes(None,1)
             if ret==1: #que les nouveaux ou film unique
              if self.mettreajourTYPE=="set": utils.UpdateSagas()
              if self.mettreajourTYPE=="movie": utils.updatemovieartwork(self.mettreajourID)
              if self.mettreajourTYPE=="tvshow": utils.UpdateSeries()
              if self.mettreajourTYPE=="artist": utils.UpdateArtistes()
             if ret==2 and Unique: #item en cours
              if self.mettreajourTYPE=="set": utils.UpdateSagas(self.mettreajourID)
              if self.mettreajourTYPE=="tvshow": utils.UpdateSeries(self.mettreajourID)                    
              if self.mettreajourTYPE=="artist": utils.UpdateArtistes(self.mettreajourID)
             if ret==3 and Unique: #ArtWorks
              if self.mettreajourTYPE=="set": utils.UpdateSagas(self.mettreajourID,None,True)                    
              if self.mettreajourTYPE=="tvshow": utils.updatetvartwork(self.mettreajourID)
             if ret==4 and Unique: #ArtWorks
              if self.mettreajourTYPE=="tvshow": utils.updateartworkall("TvShows")
                
             self.windowhome.clearProperty("IconMixArt")
    
    def SelectionneVue(self):
      content_type = utils.VueActuelle()
      if not content_type:
            content_type = "files"
      current_view = xbmc.getInfoLabel("Container.Viewmode").decode("utf-8")
      utils.ModeVues(content_type, current_view)
      
    
    
    def _init_vars(self):
          self.windowhome = xbmcgui.Window(10000) # Home.xml 
          self.windowvideonav = xbmcgui.Window(10025) # myvideonav.xml           
          self.windowvideoinf = xbmcgui.Window(12003) # dialogvideoinfo.xml 
          self.windowvideoplayer = xbmcgui.Window(12901) # videoOSD.xml 
          self.windowvideoplayerinfo = xbmcgui.Window(10142) # DialogFullScreenInfo.xml
          self.ListeTrailer=[]
          
 


if (__name__ == "__main__"):
    Main()
    #logMsg('appel plugin termine...')
