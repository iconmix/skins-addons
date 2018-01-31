# coding: utf-8
#from __future__ import unicode_literals
import resources.lib.Utils as utils
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
#containers :
#1998 : Acteurs
#1999 : éléments des sagas, des acteurs et réalisateurs, et artistes (musique)


# Script constantes
ADDON = xbmcaddon.Addon()
__addonid__    = ADDON.getAddonInfo('id')
__version__    = ADDON.getAddonInfo('version')
__language__   = ADDON.getLocalizedString
__cwd__        = ADDON.getAddonInfo('path')  
ADDON_ID = ADDON.getAddonInfo('id').decode("utf8")
ADDON_ICON = ADDON.getAddonInfo('icon').decode("utf8")
ADDON_NAME = ADDON.getAddonInfo('name').decode("utf8")
ADDON_PATH = ADDON.getAddonInfo('path').decode("utf8")
ADDON_VERSION = ADDON.getAddonInfo('version').decode("utf8")
ADDON_DATA_PATH = xbmc.translatePath("special://profile/addon_data/%s" % ADDON_ID).decode("utf8")
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
              #utils.logMsg("Plugin : %s" %(params),0)       
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
             
               
               if action == "GETCAST":
                  Id=params.get("id",None)
                  if Id: Id = Id[0] 
                  castingtype=params.get("casttype",None)
                  if castingtype: castingtype = castingtype[0]
                  utils.getCasting(castingtype,Id)              
               
              
               if action == "GETARTISTEART":
                  Id=params.get("id",None)
                  if Id: Id = Id[0] 
                  castingtype=params.get("casttype",None)
                  if castingtype: castingtype = castingtype[0]
                  Id=xbmc.getInfoLabel("ListItem.DBID")              
                  utils.getArtisteArt(castingtype,Id)  
               """   
               if action == "SETMENUVIEW":
                  vue=params.get("id",None)
                  if Id:
                    xbmc.executebuiltin("Container.SetViewMode(%s)" % vue)
               """   
                  
               if action == "GETMENUVIEW":
                  if  (len(sys.argv)>1 and sys.argv[1]):
                    content_type = utils.VueActuelle()
                    if not content_type:
                          content_type = "files"
                    current_view = xbmc.getInfoLabel("Container.Viewmode").decode("utf-8")
                    
                    ListeVues=utils.ModeVuesMenu(content_type, current_view)
                    if ListeVues:
                      utils.logMsg("ListeVues ok (%s)" %(ListeVues))
                      xbmcplugin.addDirectoryItems(int(sys.argv[1]), ListeVues)
                    xbmcplugin.endOfDirectory(int(sys.argv[1]))       
                 
        except:
           params= {}
        
        try:
            params = dict( arg.split( '=' ) for arg in sys.argv[ 1 ].split( '&' ) )
        except:
            params = {}
            
        self.trailer = params.get( 'trailer', False )
        self.setview = params.get( 'setview', False )
        self.setviewmenu = params.get( 'setviewmenu', False )
        if self.setviewmenu:
          self.idview=params.get( 'id', None )
          #utils.logMsg("On y est !!! (%s)(%s)" %(self.idview,params))
          
        self.videcache = params.get( 'videcache', False )
        self.addplaylist = params.get( 'addplaylist', False )
        self.supplaylist = params.get( 'supplaylist', False )
        self.updateallmusic = params.get( 'updateallmusic', False )
        self.mettreajour = params.get( 'mettreajour', False )
        self.backend = params.get( 'backend', False )
        
        
        if self.videcache:
           self.quelcache = params.get( 'cache', False )
           dialogC = xbmcgui.Dialog()
           ret=dialogC.yesno("ICONMIXTOOLS CACHE !!!", __language__( 32602 )," ",str(self.quelcache).upper()) #-- Show a dialog 'YES/NO'.
           if ret>0:
             utils.vidercache(self.quelcache)
 
        else:
        
          if not action :
            saga=""   
            #------ lancer mode serveur ----------- 
            if self.backend and xbmc.getCondVisibility("String.IsEmpty(Window(home).Property(IconMixToolsbackend))"):                
                MainService.MainService()
            
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
      TrailerType=""
      self.ListeTrailer=[]
      TMDBID='' 
      TMDBIDListe=[]
      
      TMDBIDListeAllocine=[]
      TrailerType=""
      TypeVideo=xbmc.getInfoLabel("ListItem.DBType")
      Annee=xbmc.getInfoLabel("ListItem.Year")
      Titre=xbmc.getInfoLabel("ListItem.Label").decode('utf-8','ignore')
      Saison=None 
      if TypeVideo=="episode":     
            Saison=str(xbmc.getInfoLabel("ListItem.Season"))                      
         
      
      if TypeVideo=="set":
        TrailerType="videonavsaga"
     
      
      if xbmc.getCondVisibility("Control.HasFocus(7779)"):
          TypeVideo=xbmc.getInfoLabel("Container(5051).ListItem.Property(dbtype)")
          Titre=xbmc.getInfoLabel("Container(5051).ListItem.Label").decode('utf-8','ignore')
          Annee=xbmc.getInfoLabel("Container(5051).ListItem.Year")
          TrailerType="Roles"
      
      if xbmc.getCondVisibility("Control.HasFocus(2999)"): #myvideonav elements (saga,acteurs,realisateurs)
          TypeVideo=xbmc.getInfoLabel("Container(1999).ListItem.DBType")
          Titre=xbmc.getInfoLabel("Container(1999).ListItem.Label").decode('utf-8','ignore')
          Annee=xbmc.getInfoLabel("Container(1999).ListItem.Year")
          TrailerType="videonav"
      if xbmc.getCondVisibility("Control.HasFocus(2008)"): #dialogvideoinfo
          TypeVideo='movie'
          Titre=xbmc.getInfoLabel("Container(5002).ListItem.Label").decode('utf-8','ignore')
          Annee=xbmc.getInfoLabel("Container(5002).ListItem.Year")
          TrailerType="saga"
      if xbmc.getCondVisibility("ControlGroup(7003).HasFocus"): #dialogvideoinfo cherche trailer
          TypeVideo=xbmc.getInfoLabel("ListItem.DBTYPE")
          Titre=xbmc.getInfoLabel("ListItem.Label").decode('utf-8','ignore')
          Annee=xbmc.getInfoLabel("ListItem.Year")
          TrailerType="videoinfo7003"
      if xbmc.getCondVisibility("Control.HasFocus(7778)"): #dialogvideoinfo realisateur
          TypeVideo=xbmc.getInfoLabel("ListItem.Property(dbtype)")
          Titre=xbmc.getInfoLabel("ListItem.Label").decode('utf-8','ignore')
          Annee=xbmc.getInfoLabel("ListItem.Year")
          TrailerType="realisateur"
      dialog.notification('IconMixTools', __language__( 32508 )+": [COLOR=Yellow] "+Titre+"[/COLOR]", ADDON_ICON,1000) 
      xbmc.executebuiltin( "ActivateWindow(busydialog)" )    
      if TrailerType=="Roles" :
           #acteurs  
           if not xbmc.getInfoLabel("Container(5051).ListItem.Property(IMDBNumber)"):
             #pas local
             Trailer5051=xbmc.getInfoLabel("Container(5051).ListItem.Trailer")
             
             self.ListeTrailer=utils.getTrailer(Trailer5051,TypeVideo) 
             self.GetAllocineTrailer(Titre,Annee,TypeVideo,None)
            
             #utils.logMsg("recherche Trailer (%s)(%s)(%s)" %(Titre,Annee,TypeVideo),0)
           else:
             #local
             TMDBID=utils.get_externalID(xbmc.getInfoLabel("Container(5051).ListItem.Property(IMDBNumber)"),TypeVideo)
             
      if TrailerType=="realisateur" :
           #realisateur
           if not xbmc.getInfoLabel("ListItem.Property(IMDBNumber)"):
             #pas local
             self.ListeTrailer=utils.getTrailer(xbmc.getInfoLabel("ListItem.Trailer"),TypeVideo) 
             self.GetAllocineTrailer(xbmc.getInfoLabel("ListItem.Label"),xbmc.getInfoLabel("ListItem.Year"),xbmc.getInfoLabel("ListItem.Property(dbtype)"),None)
           else:
             #local
             TMDBID=utils.get_externalID(xbmc.getInfoLabel("ListItem.Property(IMDBNumber)"),TypeVideo)
              
      if TrailerType=="videonav":
           #VideoNav
           IMDBID=xbmc.getInfoLabel("Container(1999).ListItem.Property(IMDBNumber)")
           TMDBID=xbmc.getInfoLabel("Container(1999).ListItem.Property(TMDBNumber)")
           if not TMDBID and not IMDBID:
               json_result = utils.getJSON('VideoLibrary.Get%sDetails' %(TypeVideo), '{ "%sid":%d,"properties":["imdbnumber"] }' %(TypeVideo,int(xbmc.getInfoLabel("Container(1999).ListItem.DBID"))))                         
               IMDBID=json_result.get("imdbnumber")                 
           if TMDBID=='' and IMDBID:
               TMDBID=utils.get_externalID(IMDBID,TypeVideo)
               
      if TrailerType=="videonavsaga":
           #VideoNav
             TypeVideo="movie"
           
          
             zz=int(xbmc.getInfoLabel("Container(1999).NumItems"))
             #utils.logMsg("SagaType (%s)(%s)" %(zz,xbmc.getInfoLabel("Container(1999).NumItems")),0)
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
               
               #utils.logMsg("Allocine (%d)(%s)(%s)(%s)(%s)(%s)" %(compteur,LABEL,YEAR,IMDBID,TMDBID,DBID),0)
               if DBID:
                 if not TMDBID and not IMDBID:
                     json_result = utils.getJSON('VideoLibrary.GetMovieDetails', '{ "movieid":%d,"properties":["imdbnumber"] }' %(int(DBID)))                         
                     IMDBID=json_result.get("imdbnumber")                 
                 if TMDBID or IMDBID:
                    TMDBIDListe.append({"tmdbid":TMDBID,"imdbid":IMDBID})
               
               
             
               
      if TrailerType=="saga" :
           #SAGA
           IMDBID=xbmc.getInfoLabel("Container(5002).ListItem.Property(IMDBNumber)")
           TMDBID=xbmc.getInfoLabel("Container(5002).ListItem.Property(TMDBNumber)")
           if not TMDBID and not IMDBID:
               json_result = utils.getJSON('VideoLibrary.GetMovieDetails', '{ "movieid":%d,"properties":["imdbnumber"] }' %(int(xbmc.getInfoLabel("Container(5002).ListItem.DBID"))))                         
               IMDBID=json_result.get("imdbnumber")
           
           if TMDBID=='' and IMDBID:
               TMDBID=utils.get_externalID(IMDBID,'movie')
         
      
      if TrailerType=="videoinfo7003" or TrailerType=="":
           #acteurs videoinfo                     
           if TypeVideo!="episode":
             IMDBNUMBER=xbmc.getInfoLabel("ListItem.IMDBNumber")
           else:
             IMDBNUMBER=xbmc.getInfoLabel("ListItem.TVShowTitle")
             Titre=IMDBNUMBER
           
           if not IMDBNUMBER:
             self.ListeTrailer=utils.getTrailer(xbmc.getInfoLabel("ListItem.Trailer"),TypeVideo) 
           else:
             TMDBID=utils.get_externalID(IMDBNUMBER,TypeVideo)
           #utils.logMsg("Trailertype (%s) : (%s)(%s)(%s)" %(Titre,IMDBNUMBER,TypeVideo,TMDBID))
       
      if TMDBID!='' or len(TMDBIDListe)>0:
           if len(TMDBIDListe)>0:
             #utils.logMsg("SagaType TMDBIDListe %s" %(TMDBIDListe),0)
             #start_time = time.time() 
             if ADDON.getSetting('allocineactif')=="true" :
                self.ListeTrailer=self.ListeTrailer+utils.GetSagaTrailersAllocine(TMDBIDListeAllocine)
             if ADDON.getSetting('youtubeactif')=="true" :
                self.ListeTrailer=self.ListeTrailer+utils.GetSagaTrailers(TMDBIDListe) 
             
            
           else:
            
             self.ListeTrailer=utils.getTrailer(TMDBID,TypeVideo,Saison)
             #utils.logMsg("recherche Trailer (%s)(%s)(%s)" %(Titre,Annee,TypeVideo),0)
             if not self.ListeTrailer:
               self.ListeTrailer=[]
             self.GetAllocineTrailer(Titre,Annee,TypeVideo,None)
             #utils.logMsg("self.ListeTrailer (%d)(%s)" %(len(self.ListeTrailer),self.ListeTrailer),0)
           
                
           if TrailerType=="videonav" and str(xbmc.getInfoLabel("Container(1999).ListItem.Property(DBID)"))!="": 
              self.ListeTrailer.append({"id":xbmc.getInfoLabel("Container(1999).ListItem.FilenameAndPath"),"position":"0","iso_639_1":"","iso_3166_1":"","key":"KODI","name":xbmc.getLocalizedString( 208 )+"[I]"+"[COLOR=LightGrey] "+xbmc.getInfoLabel("Container(1999).ListItem.Label").decode("utf8")+" [/I][/COLOR]","site":"YouTube","size":xbmc.getInfoLabel("Container(1999).ListItem.VideoResolution"),"type":"","landscape":xbmc.getInfoLabel("Container(1999).ListItem.Art(thumb)")})
           if TrailerType=="saga" and str(xbmc.getInfoLabel("Container(5002).ListItem.Property(DBID)"))!="": 
              self.ListeTrailer.append({"id":xbmc.getInfoLabel("Container(5002).ListItem.FilenameAndPath"),"position":"0","iso_639_1":"","iso_3166_1":"","key":"KODI","name":xbmc.getLocalizedString( 208 )+"[I]"+"[COLOR=LightGrey] "+xbmc.getInfoLabel("Container(5002).ListItem.Label").decode("utf8")+" [/I][/COLOR]","site":"YouTube","size":xbmc.getInfoLabel("Container(5002).ListItem.VideoResolution"),"type":"","landscape":xbmc.getInfoLabel("Container(5002).ListItem.Art(thumb)")})
           if (TrailerType=="videoinfo7003" or TrailerType=="videoinfo7003") and str(xbmc.getInfoLabel("ListItem.DBID"))!="":
              self.ListeTrailer.append({"id":xbmc.getInfoLabel("ListItem.FilenameAndPath"),"position":"0","iso_639_1":"","iso_3166_1":"","key":"KODI","name":xbmc.getLocalizedString( 208 )+"[I]"+"[COLOR=LightGrey] "+xbmc.getInfoLabel("ListItem.Label").decode("utf8")+" [/I][/COLOR]","site":"YouTube","size":xbmc.getInfoLabel("ListItem.VideoResolution"),"type":"","landscape":xbmc.getInfoLabel("ListItem.Art(thumb)")})
           if TrailerType=="Roles" and str(xbmc.getInfoLabel("Container(5051).ListItem.Property(DBID)"))!="": 
              self.ListeTrailer.append({"id":xbmc.getInfoLabel("Container(5051).ListItem.FilenameAndPath"),"position":"0","iso_639_1":"","iso_3166_1":"","key":"KODI","name":xbmc.getLocalizedString( 208 )+"[I]"+"[COLOR=LightGrey] "+xbmc.getInfoLabel("Container(5051).ListItem.Label").decode("utf8")+" [/I][/COLOR]","site":"YouTube","size":xbmc.getInfoLabel("Container(5051).ListItem.VideoResolution"),"type":"","landscape":xbmc.getInfoLabel("Container(5051).ListItem.Art(thumb)")})
           if TrailerType=="realisateur" and str(xbmc.getInfoLabel("ListItem.Property(DBID)"))!="": 
              self.ListeTrailer.append({"id":xbmc.getInfoLabel("ListItem.FilenameAndPath"),"position":"0","iso_639_1":"","iso_3166_1":"","key":"KODI","name":xbmc.getLocalizedString( 208 )+"[I]"+"[COLOR=LightGrey] "+xbmc.getInfoLabel("ListItem.Label").decode("utf8")+" [/I][/COLOR]","site":"YouTube","size":xbmc.getInfoLabel("ListItem.VideoResolution"),"type":"","landscape":xbmc.getInfoLabel("ListItem.Art(thumb)")})
           
      
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
                  utils.logMsg("erreur : %s" %(Item),0)                      
                
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
          dialog.notification('IconMixTools', Titre+": "+__language__( 32506 ), "acteurs/arfffff.png", 3000)
      self.windowhome.setProperty('FenetreListeChoix','')
      #retour au focus précédent
      if  TrailerType=="Roles" :  
                     #self.windowhome.setProperty('ActeurVideoReset','')
                     xbmc.executebuiltin("SetFocus(7779)")
      else :
           if  TrailerType=="videonav" : 
                xbmc.executebuiltin("SetFocus(2999)")                             
           else:
                if  TrailerType=="realisateur" :
                  xbmc.executebuiltin("SetFocus(7778)")
                if  TrailerType=="videoinfo7003" :
                  xbmc.executebuiltin("SetFocus(7003)")
                else:
                  if TrailerType=="videonavsaga":
                    xbmc.executebuiltin("SetFocus(2008)")
                  else:    
                    xbmc.executebuiltin("SetFocus(2008)")
    
    def GetAllocineTrailer(self,Titre=None,Annee=None,TypeVideo=None,PanneauActeur=None):
      if ADDON.getSetting('allocineactif')=="true":
        start_time = time.time() 
        AllocineBA=None
        
        #Annee=xbmc.getInfoLabel("ListItem.Year")
        if TypeVideo=="movie":
          AllocineBA=utils.Allocine_BandeAnnonce(Titre.lower(),TypeVideo,None,None,Annee)
          #utils.logMsg("recherche Trailer allocine %s/%s/%s" %(Titre,TypeVideo,Annee),0)

        else:
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
          #utils.logMsg("recherche Trailer allocine %s/%s/%s/%s/%s" %(Titre,TypeVideo,Annee,Saison,Episode),0)

            #interval = time.time() - start_time 
            #utils.logMsg("Total time in seconds (%s): %s" %(xbmc.getInfoLabel("ListItem.Season"),str(interval)),0) 
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
                Titre=xbmc.getLocalizedString( 342 )
               if DBTYPEX=="set": 
                Titre=xbmc.getLocalizedString( 20434 )
               if DBTYPEX=="tvshow": 
                Titre=xbmc.getLocalizedString( 20343 )
               if DBTYPEX=="artist": 
                Titre=xbmc.getLocalizedString( 36917 )
                
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
    #utils.logMsg('appel plugin termine...')
