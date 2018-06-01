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
            
                            
               if action == "GETGENRE":
                  
                  genre=params.get("genre",None)
                  if genre: genre = genre[0]  
                 
                  genretype=params.get("genretype",None)
                  if genretype: genretype = genretype[0]
                  origtitle=params.get("title",None)
                  if origtitle: origtitle = origtitle[0]    
                  #if origtitle and genre and genretype:
                  utils.getGenre(genre,genretype,origtitle)  
                  
               if action == "WIDGETGETNEXT":
                  Id=params.get("id",None)
                  if Id: Id = Id[0] 
                  Episodes=utils.GetNextEpisodesKodi()  
                  if Episodes:
                      xbmcplugin.addDirectoryItems(int(sys.argv[1]), Episodes)
                      if SETTING("iconmixdebug")=="true":
                          logMsg("Plugin  : WIDGETGETNEXT (%s)" %(Prochain))
                  xbmcplugin.endOfDirectory(int(sys.argv[1]))  
               
               if action == "GETALLNEXTEPISODES":
                  Id=params.get("id",None)
                  if Id: Id = Id[0] 
                  dbtype=params.get("dbtype",None)
                  if dbtype: dbtype = dbtype[0] 
                  Episodes=utils.getallnextepisodes(str(Id),None,str(dbtype),True)  
                  if Episodes:
                      xbmcplugin.addDirectoryItems(int(sys.argv[1]), Episodes)                      
                  xbmcplugin.endOfDirectory(int(sys.argv[1]))  
               
             
               
               if action == "GETCAST":
                  Id=params.get("id",None)
                  if Id: Id = Id[0] 
                  castingtype=params.get("casttype",None)
                  if castingtype: castingtype = castingtype[0]
                  utils.getCasting(castingtype,Id)   
               
               if action == "GETEPISODESKODI":
                  Id=params.get("id",None)
                  if Id: Id = Id[0] 
                  Episodes,Prochain=utils.GetEpisodesKodi(Id,False)  
                  if Episodes:
                      xbmcplugin.addDirectoryItems(int(sys.argv[1]), Episodes)
                      self.windowhome.setProperty('IconmixProchainEpisode',str(Prochain))
                      if SETTING("iconmixdebug")=="true":
                          logMsg("Plugin  : GetEpisodesKodi (%s)" %(Prochain))
                  xbmcplugin.endOfDirectory(int(sys.argv[1])) 
                  OldTvShowId=self.windowhome.getProperty('IconmixFlagPanelEpisode')
                  if OldTvShowId!=Id:
                    self.windowhome.clearProperty('IconmixFlagPanelEpisode')
                  
                             
               if action == "GETARTISTEART":
                  Id=params.get("id",None)
                  if Id: Id = Id[0] 
                  castingtype=params.get("casttype",None)
                  if castingtype: castingtype = castingtype[0]
                  Id=xbmc.getInfoLabel("ListItem.DBID")              
                  utils.getArtisteArt(castingtype,Id)  
               
                  
               if action == "GETMENUVIEW":
                  if  (len(sys.argv)>1 and sys.argv[1]):
                    content_type = utils.VueActuelle()
                    if not content_type:
                          content_type = "files"
                    current_view = xbmc.getInfoLabel("Container.Viewmode").decode("utf-8")
                    
                    ListeVues=utils.ModeVuesMenu(content_type, current_view)
                    if ListeVues:
                      #logMsg("ListeVues ok (%s)" %(ListeVues))
                      xbmcplugin.addDirectoryItems(int(sys.argv[1]), ListeVues)
                    xbmcplugin.endOfDirectory(int(sys.argv[1])) 
               return
               
               
        except:
          params= {}
        
        try:
            params = dict( arg.split( '=' ) for arg in sys.argv[ 1 ].split( '&' ) )
        except:
            params = {}
        logMsg("Appel Plugin sans action : %s" %(params),0)     
        self.trailer = params.get( 'trailer', False )
        self.trailerTypeVideo=params.get( 'dbtype', None )
        self.trailerTitre=params.get( 'label', None )
        self.trailerAnnee=params.get( 'year', None )
        self.trailerKODIID=params.get( 'dbid', None )
        self.trailerIMDBID=params.get( 'imdbnumber', None )
        self.trailerTMDBID=params.get( 'tmdbnumber', None )
          
          
        self.setview = params.get( 'setview', False )
        self.setviewmenu = params.get( 'setviewmenu', False )
        if self.setviewmenu:
          self.idview=params.get( 'id', None )
          #logMsg("On y est !!! (%s)(%s)" %(self.idview,params))
          
        self.videcache = params.get( 'videcache', False )
        self.addplaylist = params.get( 'addplaylist', False )
        self.supplaylist = params.get( 'supplaylist', False )
        self.updateallmusic = params.get( 'updateallmusic', False )
        self.mettreajour = params.get( 'mettreajour', False )
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
        
        
        if self.togglewatchedepisode and self.itemidkodiepisode:
          #dialog=xbmcgui.Dialog() 
          self.windowhome.clearProperty('IconmixProchainEpisode')
          if self.togglewatched=="True":
           json_result = utils.setJSON('VideoLibrary.SetEpisodeDetails', '{ "episodeid":%d,"resume":{"position":0,"total":0},"playcount":1 }' %(int(self.itemidkodiepisode)))                          
          else:
           json_result = utils.setJSON('VideoLibrary.SetEpisodeDetails', '{ "episodeid":%d,"resume":{"position":0,"total":0},"playcount":0 }' %(int(self.itemidkodiepisode)))                          
          self.windowhome.setProperty('IconMixUpdateEpisodes','1')
          #dialog.notification('IconMixTools', "TOGGLEEEEEEEEEEEEEEEEEEEEEE (%s)(%s)" %(str(self.itemidkodiepisode),self.togglewatched), ADDON_ICON,500)
        
        
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
            """
            logMsg("item (%s)" %(item))
            logMsg("TvShowItem (%s)"  %(TvShowItem))
            logMsg("TvShowLinkPath (%s)"  %(TvShowLinkPath))
            logMsg("TvShowPath (%s)"  %(TvShowPath))
            """
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
                    
            #-------------BANDES ANNONCES-------------             
            if self.trailer :  
                self.GetTrailer()
                    
            #-------------CHOIX DE LA VUE-------------             
            if self.setview:
                self.SelectionneVue()
            
            if self.setviewmenu and self.idview:
               xbmc.executebuiltin("Container.SetViewMode(%s)"  % self.idview)
             
           #     self.SelectionneVueMenu()

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
          
    def GetTrailer(self):
      #xbmc.executebuiltin( "ActivateWindow(busydialog)" ) 
      self.windowhome.setProperty('FenetreListeChoix','1')
      dialog=xbmcgui.Dialog()                
      self.TrailerType=""
      self.ListeTrailer=[]
      ContainerID=None
      Saison=None
      TMDBID='' 
      TMDBIDListe=[]
      PanneauActeur=None 
      TMDBIDListeAllocine=[]
      self.TrailerType=""
      
      
      
      if self.trailerTitre:
          TypeVideo=self.trailerTypeVideo
          PanneauActeur=True
          Titre=self.trailerTitre
          Annee=self.trailerAnnee
          KODIID=self.trailerKODIID
          IMDBID=self.trailerIMDBID
          TMDBID=self.trailerTMDBID
          self.TrailerType="dialogplus"
          if not TMDBID:
                   TMDBID=utils.get_externalID(IMDBID,TypeVideo) 
      else:    
          TypeVideo=xbmc.getInfoLabel("ListItem.DBType")
          Annee=xbmc.getInfoLabel("ListItem.Year")
          Titre=xbmc.getInfoLabel("ListItem.Label").decode('utf-8','ignore')
          Saison=None 
          if self.windowhome.getProperty('IconmixShowInfo')=="1":
            ContainerID=1990
          else:
             if self.windowhome.getProperty('IconmixShowInfo')=="2":
               if not xbmc.getCondVisibility("ControlGroup(7003).HasFocus"):
                  ContainerID=5051
               else:
                  ContainerID=1990
             else:
                  ContainerID=None
          
          if TypeVideo=="episode":     
                Saison=str(xbmc.getInfoLabel("ListItem.Season"))                      
             
          
          if TypeVideo=="set":
            self.TrailerType="videonavsaga"
         
          
          if xbmc.getCondVisibility("Control.HasFocus(7779)"):
              PanneauActeur=True
              TypeVideo=xbmc.getInfoLabel("Container(5051).ListItem.Property(dbtype)")
              Titre=xbmc.getInfoLabel("Container(5051).ListItem.Label").decode('utf-8','ignore')
              Annee=xbmc.getInfoLabel("Container(5051).ListItem.Year")
              KODIID=xbmc.getInfoLabel("Container(5051).ListItem.DBID")
              self.TrailerType="Roles"
          
          if xbmc.getCondVisibility("Control.HasFocus(2999)"): #myvideonav elements (saga,acteurs,realisateurs)
              TypeVideo=xbmc.getInfoLabel("Container(1999).ListItem.DBType")
              Titre=xbmc.getInfoLabel("Container(1999).ListItem.Label").decode('utf-8','ignore')
              Annee=xbmc.getInfoLabel("Container(1999).ListItem.Year")
              self.TrailerType="videonav"
              
          if xbmc.getCondVisibility("Control.HasFocus(2008)"): #dialogvideoinfo
              TypeVideo='movie'
              Titre=xbmc.getInfoLabel("Container(5002).ListItem.Label").decode('utf-8','ignore')
              Annee=xbmc.getInfoLabel("Container(5002).ListItem.Year")
              self.TrailerType="saga"
          if xbmc.getCondVisibility("ControlGroup(442).HasFocus"): #dialogvideoinfo cherche trailer
              logMsg("ContainerID (%s)" %(ContainerID))
              TypeVideo=xbmc.getInfoLabel("Container(%d).ListItem.DBTYPE" %(ContainerID)) if ContainerID else xbmc.getInfoLabel("ListItem.DBTYPE")
              Titre=xbmc.getInfoLabel("Container(%d).ListItem.Label" %(ContainerID)) if ContainerID else xbmc.getInfoLabel("ListItem.Label")
              Titre=Titre.decode('utf-8','ignore')
              Annee=xbmc.getInfoLabel("Container(%d).ListItem.Year" %(ContainerID)) if ContainerID else xbmc.getInfoLabel("ListItem.Year")
              self.TrailerType="videoinfo7003"
          if xbmc.getCondVisibility("Control.HasFocus(7778)"): #dialogvideoinfo realisateur
              TypeVideo=xbmc.getInfoLabel("Container(5052).ListItem.DBTYPE" )
              Titre=xbmc.getInfoLabel("Container(5052).ListItem.Label" )
              Titre=Titre.decode('utf-8','ignore')
              Annee=xbmc.getInfoLabel("Container(5052).ListItem.Year" )    
              self.TrailerType="realisateur"

           
           
          if self.TrailerType=="Roles" :
               #acteurs  
               IMDBID=xbmc.getInfoLabel("Container(5051).ListItem.Property(IMDBNumber)")
               TMDBID=xbmc.getInfoLabel("Container(5051).ListItem.Property(TMDBNumber)")
              
               if not TMDBID:
                   TMDBID=utils.get_externalID(IMDBID,TypeVideo)
                 
                 
          if self.TrailerType=="realisateur" :
               #realisateur
               IMDBID=xbmc.getInfoLabel("Container(5052).ListItem.Property(IMDBNumber)")
               TMDBID=xbmc.getInfoLabel("Container(5052).ListItem.Property(TMDBNumber)")
               KODIID=xbmc.getInfoLabel("Container(5052).ListItem.DBID")
               PanneauActeur=True
               if not TMDBID:
                     TMDBID=utils.get_externalID(IMDBID,TypeVideo)
                  
          if self.TrailerType=="videonav":
               #VideoNav
               IMDBID=xbmc.getInfoLabel("Container(1999).ListItem.Property(IMDBNumber)")
               TMDBID=xbmc.getInfoLabel("Container(1999).ListItem.Property(TMDBNumber)")
               KODIID=xbmc.getInfoLabel("Container(1999).ListItem.DBID")
               if not TMDBID and not IMDBID:
                   json_result = utils.getJSON('VideoLibrary.Get%sDetails' %(TypeVideo), '{ "%sid":%d,"properties":["imdbnumber"] }' %(TypeVideo,int(xbmc.getInfoLabel("Container(1999).ListItem.DBID"))))                         
                   IMDBID=json_result.get("imdbnumber")                 
               if TMDBID=='' and IMDBID:
                   TMDBID=utils.get_externalID(IMDBID,TypeVideo)
                   
          if self.TrailerType=="videonavsaga":
               #VideoNav
                 TypeVideo="movie"
                 nbitem=xbmc.getInfoLabel("Container(1999).NumItems")
                 #logMsg("NbItems (%s)(%s)" %(nbitem,xbmc.getInfoLabel("Control.GetLabel(3333)")))
                 if nbitem:
             
                     zz=int(nbitem)
                     compteur=0
                     
                     for compteur in range(0,zz): 
                       #SagaItem=ListeSaga.getListItem(cpt)
                       #IMDBID=SagaItem.getProperty(IMDBNumber)
                       #TMDBID=SagaItem.getProperty(TMDBNumber)
                       #DBID=SagaItem.getProperty(DBID)
                       
                       IMDBID=xbmc.getInfoLabel("Container(1999).ListItemAbsolute(%d).Property(IMDBNumber)" %(compteur))
                       TMDBID=xbmc.getInfoLabel("Container(1999).ListItemAbsolute(%d).Property(TMDBNumber)" %(compteur))
                       DBID=xbmc.getInfoLabel("Container(1999).ListItemAbsolute(%d).Property(DBID)" %(compteur))
                       LABEL=xbmc.getInfoLabel("Container(1999).ListItemAbsolute(%d).Label" %(compteur))
                       YEAR=xbmc.getInfoLabel("Container(1999).ListItemAbsolute(%d).Year" %(compteur))
                       TMDBIDListeAllocine.append({"Titre":LABEL,"Annee":YEAR})
                       
                       #logMsg("Allocine (%d)(%s)(%s)(%s)(%s)(%s)" %(compteur,LABEL,YEAR,IMDBID,TMDBID,DBID),0)
                       if DBID:
                         if not TMDBID and not IMDBID:
                             json_result = utils.getJSON('VideoLibrary.GetMovieDetails', '{ "movieid":%d,"properties":["imdbnumber"] }' %(int(DBID)))                         
                             IMDBID=json_result.get("imdbnumber")                 
                       if TMDBID or IMDBID:
                            TMDBIDListe.append({"tmdbid":TMDBID,"imdbid":IMDBID})
                   
                   
                 
                   
          if self.TrailerType=="saga" :
               #SAGA
               IMDBID=xbmc.getInfoLabel("Container(5002).ListItem.Property(IMDBNumber)")
               TMDBID=xbmc.getInfoLabel("Container(5002).ListItem.Property(TMDBNumber)")
               KODIID=xbmc.getInfoLabel("Container(5002).ListItem.DBID")
               if not TMDBID and not IMDBID:
                   json_result = utils.getJSON('VideoLibrary.GetMovieDetails', '{ "movieid":%d,"properties":["imdbnumber"] }' %(int(xbmc.getInfoLabel("Container(5002).ListItem.DBID"))))                         
                   IMDBID=json_result.get("imdbnumber")
               
               else: 
                 if not TMDBID:
                   TMDBID=utils.get_externalID(IMDBID,'movie')
             
          
          if self.TrailerType=="videoinfo7003" or self.TrailerType=="":
               #acteurs videoinfo   
               KODIID=xbmc.getInfoLabel("Container(%d).ListItem.DBID" %(ContainerID)) if ContainerID else xbmc.getInfoLabel("ListItem.DBID")
               TMDBID=xbmc.getInfoLabel("Container(%d).ListItem.Property(TMDBNumber)" %(ContainerID)) if ContainerID else xbmc.getInfoLabel("ListItem.Property(TMDBNumber)")
               if TypeVideo!="episode":
                 IMDBNUMBER=xbmc.getInfoLabel("Container(%d).ListItem.IMDBNumber" %(ContainerID)) if ContainerID else xbmc.getInfoLabel("ListItem.IMDBNumber")
               else:
                 IMDBNUMBER=xbmc.getInfoLabel("Container(%d).ListItem.TVShowTitle" %(ContainerID)) if ContainerID else xbmc.getInfoLabel("ListItem.TVShowTitle")
                 Titre=IMDBNUMBER
               if not TMDBID:             
                   TMDBID=utils.get_externalID(IMDBNUMBER,TypeVideo)
      #logMsg("self.TrailerType (%s)(%s) : (%s)(%s)" %(self.TrailerType,Titre,TypeVideo,TMDBID))
      dialog.notification('IconMixTools', __language__( 32508 ), ADDON_ICON,500)   
      if TMDBID!='' or len(TMDBIDListe)>0 or len(TMDBIDListeAllocine)>0:
           xbmc.executebuiltin( "ActivateWindow(busydialog)" )   
           #logMsg("self.TrailerType (%s) : (%s)(%s)(%s)(%s)(%s)" %(self.TrailerType,Titre,TypeVideo,TMDBID,ContainerID,KODIID))
           if len(TMDBIDListe)>0:
             #start_time = time.time() 
             if SETTING('allocineactif')=="true" :
                self.ListeTrailer=self.ListeTrailer+utils.GetSagaTrailersAllocine(TMDBIDListeAllocine)
             if SETTING('youtubeactif')=="true" :
                self.ListeTrailer=self.ListeTrailer+utils.GetSagaTrailers(TMDBIDListe) 
     
           else:
            
             self.ListeTrailer=utils.getTrailer(TMDBID,TypeVideo,Saison)
             if not self.ListeTrailer:
               self.ListeTrailer=[]
             self.GetAllocineTrailer(Titre,Annee,TypeVideo,PanneauActeur)
           
                
           if self.TrailerType=="videonav" and KODIID!="": 
              self.ListeTrailer.append({"id":xbmc.getInfoLabel("Container(1999).ListItem.FilenameAndPath"),"position":"0","iso_639_1":"","iso_3166_1":"","key":"KODI","name":__skin_string__( 208 )+"[I]"+"[COLOR=LightGrey] "+xbmc.getInfoLabel("Container(1999).ListItem.Label").decode("utf8")+" [/I][/COLOR]","site":"YouTube","size":xbmc.getInfoLabel("Container(1999).ListItem.VideoResolution"),"type":"","landscape":xbmc.getInfoLabel("Container(1999).ListItem.Art(thumb)")})
           if self.TrailerType=="saga" and KODIID!="": 
              self.ListeTrailer.append({"id":xbmc.getInfoLabel("Container(5002).ListItem.FilenameAndPath"),"position":"0","iso_639_1":"","iso_3166_1":"","key":"KODI","name":__skin_string__( 208 )+"[I]"+"[COLOR=LightGrey] "+xbmc.getInfoLabel("Container(5002).ListItem.Label").decode("utf8")+" [/I][/COLOR]","site":"YouTube","size":xbmc.getInfoLabel("Container(5002).ListItem.VideoResolution"),"type":"","landscape":xbmc.getInfoLabel("Container(5002).ListItem.Art(thumb)")})
           if self.TrailerType=="videoinfo7003" and ContainerID and KODIID!="":
              self.ListeTrailer.append({"id":xbmc.getInfoLabel("Container(%d).ListItem.FilenameAndPath" %(ContainerID)),"position":"0","iso_639_1":"","iso_3166_1":"","key":"KODI","name":__skin_string__( 208 )+"[I]"+"[COLOR=LightGrey] "+xbmc.getInfoLabel("Container(%d).ListItem.Label" %(ContainerID)).decode("utf8")+" [/I][/COLOR]","site":"YouTube","size":xbmc.getInfoLabel("Container(%d).ListItem.VideoResolution" %(ContainerID)),"type":"","landscape":xbmc.getInfoLabel("Container(%d).ListItem.Art(thumb)"%(ContainerID))})
           if self.TrailerType=="videoinfo7003" and not ContainerID and  KODIID!="":
              self.ListeTrailer.append({"id":xbmc.getInfoLabel("ListItem.FilenameAndPath" ),"position":"0","iso_639_1":"","iso_3166_1":"","key":"KODI","name":__skin_string__( 208 )+"[I]"+"[COLOR=LightGrey] "+xbmc.getInfoLabel("ListItem.Label" ).decode("utf8")+" [/I][/COLOR]","site":"YouTube","size":xbmc.getInfoLabel("ListItem.VideoResolution" ),"type":"","landscape":xbmc.getInfoLabel("ListItem.Art(thumb)")})
           if self.TrailerType=="Roles" and KODIID!="": 
              self.ListeTrailer.append({"id":xbmc.getInfoLabel("Container(5051).ListItem.FilenameAndPath"),"position":"0","iso_639_1":"","iso_3166_1":"","key":"KODI","name":__skin_string__( 208 )+"[I]"+"[COLOR=LightGrey] "+xbmc.getInfoLabel("Container(5051).ListItem.Label").decode("utf8")+" [/I][/COLOR]","site":"YouTube","size":xbmc.getInfoLabel("Container(5051).ListItem.VideoResolution"),"type":"","landscape":xbmc.getInfoLabel("Container(5051).ListItem.Art(thumb)")})
           if self.TrailerType=="realisateur" and KODIID!="": 
              self.ListeTrailer.append({"id":xbmc.getInfoLabel("ListItem.FilenameAndPath"),"position":"0","iso_639_1":"","iso_3166_1":"","key":"KODI","name":__skin_string__( 208 )+"[I]"+"[COLOR=LightGrey] "+xbmc.getInfoLabel("ListItem.Label").decode("utf8")+" [/I][/COLOR]","site":"YouTube","size":xbmc.getInfoLabel("ListItem.VideoResolution"),"type":"","landscape":xbmc.getInfoLabel("ListItem.Art(thumb)")})
           
        
           xbmc.executebuiltin( "Dialog.Close(busydialog)" ) 
      if len(self.ListeTrailer)>0:
          ListeNomTrailer=[]
          Image=""
          for Item in  self.ListeTrailer:
               NomTrailer=None                        
              
               try:
                  Image=urllib.unquote(Item.get("landscape").replace("image://",""))
               except:
                  Image=""
                  logMsg("erreur : %s" %(Item),0)                      
                
               try: 
                    NomTrailer=utils.try_decode(Item["name"])+" ["+utils.try_decode(Item["type"])+" - "+str(Item["size"])+"p - "+utils.try_decode(Item["iso_3166_1"]+"]")
               except:
                    NomTrailer=utils.try_decode(Item["type"])+' ['+str(Item.get("size"))+'p - '+utils.try_decode(Item["iso_3166_1"])+']'
                    
               Elements = xbmcgui.ListItem(label=NomTrailer, iconImage=str(Image),label2="selectionnevue")
               Elements.setProperty("Icon", Image)
               Elements.setProperty("Source", Item["key"])
               ListeNomTrailer.append(Elements)
                    
          if len(ListeNomTrailer)>0: 
                
                self.ui = MainService.dialog_select_UI('choix.xml', ADDON_PATH, 'default','1080i',listing=ListeNomTrailer,trailers=self.ListeTrailer,ItemId=xbmc.getInfoLabel("ListItem.DBID"))
                self.windowhome.setProperty("IconMixTrailer","1")
                ret=self.ui.doModal()
                del self.ui                          
                self.windowhome.clearProperty('IconMixTrailer')
                  
                      
      else: 
          # 
          dialog=xbmcgui.Dialog()
          dialog.notification('IconMixTools', Titre+": "+__language__( 32506 ), "acteurs/arfffff.png", 500)
      self.windowhome.setProperty('FenetreListeChoix','')
      #retour au focus précédent
      retour={"":2008,"videonav":2999,"realisateur":7778,"videoinfo7003":7003,"dialogplus":7003,"videonavsaga":2008,"Roles":7779}
      xbmc.executebuiltin("SetFocus(%d)" %(retour[self.TrailerType]))   
           
    
    def GetAllocineTrailer(self,Titre=None,Annee=None,TypeVideo=None,PanneauActeur=None):
      if SETTING('allocineactif')=="true":
        start_time = time.time() 
        AllocineBA=None
        #logMsg("recherche Trailer allocine %s/%s/%s/%s" %(Titre,TypeVideo,Annee,PanneauActeur),0)
        #Annee=xbmc.getInfoLabel("ListItem.Year")
        if TypeVideo=="movie":
          AllocineBA=utils.Allocine_BandeAnnonce(Titre.lower(),TypeVideo,None,None,Annee)
          #

        else:
          if not PanneauActeur:
            Titre=xbmc.getInfoLabel("ListItem.TVShowTitle")
          Episode=None              
          if TypeVideo=="tvshow":
            Saison=None                                        
          else:
            Saison=str(xbmc.getInfoLabel("ListItem.Season"))
            
          if TypeVideo=="episode"  :
            Episode=str(xbmc.getInfoLabel("ListItem.Episode"))
            Annee=None
            
          AllocineBA=utils.Allocine_BandeAnnonce(Titre.lower(),TypeVideo,Saison,Episode,Annee)
          #logMsg("recherche Trailer allocine %s/%s/%s/%s/%s" %(Titre,TypeVideo,Annee,Saison,Episode),0)

            #interval = time.time() - start_time 
            #logMsg("Total time in seconds (%s): %s" %(xbmc.getInfoLabel("ListItem.Season"),str(interval)),0) 
        if AllocineBA:
            if not self.ListeTrailer:
              self.ListeTrailer=[]
            cpt=len(AllocineBA)-1
            while cpt>=0:                
                self.ListeTrailer.insert(0,AllocineBA[cpt])
                cpt=cpt-1
            
                   
                 
    
    def MiseAJour(self):
      saga=""
      DBTYPEX=xbmc.getInfoLabel("ListItem.DBTYPE")
      if xbmc.getCondVisibility("Container.Content(artists)"): 
               DBTYPEX="artist"
      if ( DBTYPEX=="set" or DBTYPEX=="movie" or DBTYPEX=="tvshow" or DBTYPEX=="artist" or DBTYPEX=="season" or saga!=""):
             if saga=="":
               Unique="ok"
             else:
               Unique=""
             
             if DBTYPEX!="season": 
               dialog = xbmcgui.Dialog()
               if DBTYPEX=="movie": 
                Titre=__skin_string__( 342 )
               if DBTYPEX=="set": 
                Titre=__skin_string__( 20434 )
               if DBTYPEX=="tvshow": 
                Titre=__skin_string__( 20343 )
               if DBTYPEX=="artist": 
                Titre=__skin_string__( 36917 )
                
               if DBTYPEX!="movie":
                 Choix=[__language__( 32502 )+Titre, __language__( 32503 )+Titre]
               else :
                 Choix=[__language__( 32510 )]
               if Unique and xbmc.getInfoLabel("ListItem.DBID") and not DBTYPEX=="movie": 
                 Choix.append(__language__( 32507 )+" [COLOR=yellow]"+utils.try_decode(xbmc.getInfoLabel("ListItem.Label"))+"[/COLOR]")
                 
               if DBTYPEX=="set"  or DBTYPEX=="movie" or DBTYPEX=="tvshow":
                   Choix.append(__language__( 32514 )+" [COLOR=yellow]"+utils.try_decode(xbmc.getInfoLabel("ListItem.Label"))+"[/COLOR]")
               if DBTYPEX=="tvshow":
                 Choix.append(__language__( 32511 ))
               
               ret=dialog.select(Titre, Choix)
             else:
              ret=0
             if ret==0: #tous
              if DBTYPEX=="set": utils.UpdateSagas(0,1)
              if DBTYPEX=="tvshow": utils.UpdateSeries(0,1)
              if DBTYPEX=="movie": utils.updateartworkall("Movies")
              if DBTYPEX=="artist": utils.UpdateArtistes(None,1)
             if ret==1: #que les nouveaux ou film unique
              if DBTYPEX=="set": utils.UpdateSagas()
              if DBTYPEX=="movie": utils.updatemovieartwork(xbmc.getInfoLabel("ListItem.DBID"))
              if DBTYPEX=="tvshow": utils.UpdateSeries()
              if DBTYPEX=="artist": utils.UpdateArtistes()
             if ret==2 and Unique: #item en cours
              if DBTYPEX=="set": utils.UpdateSagas(xbmc.getInfoLabel("ListItem.DBID"))
              if DBTYPEX=="tvshow": utils.UpdateSeries(xbmc.getInfoLabel("ListItem.DBID"))                    
              if DBTYPEX=="artist": utils.UpdateArtistes(xbmc.getInfoLabel("ListItem.DBID"))
             if ret==3 and Unique: #ArtWorks
              if DBTYPEX=="set": utils.UpdateSagas(xbmc.getInfoLabel("ListItem.DBID"),None,True)                    
              if DBTYPEX=="tvshow": utils.updatetvartwork(xbmc.getInfoLabel("ListItem.DBID"))
             if ret==4 and Unique: #ArtWorks
              if DBTYPEX=="tvshow": utils.updateartworkall("TvShows")
    
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
