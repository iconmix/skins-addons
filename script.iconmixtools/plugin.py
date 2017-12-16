# coding: utf-8
#from __future__ import unicode_literals
import resources.lib.Utils as utils
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


class dialog_select_UI(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)
        self.listing = kwargs.get('listing')
        self.ListeTrailer = kwargs.get('trailers')

    def onInit(self):
        self.img_list = self.getControl(6)            
            

        if self.img_list:
          for item in self.listing:           
              self.img_list.addItem(item)
          self.setFocus(self.img_list)
          self.BAF=0
          if xbmc.getCondVisibility("Skin.HasSetting(BAfenetre)"):
            self.BAF=1
        else:
          self.close()
        #utils.logMsg("Courant ID : %d" %(xbmcgui.getCurrentWindowDialogId()),0)

    def onAction(self, action):
        if action in ACTION_PREVIOUS_MENU:
            if xbmc.Player().isPlaying():
               xbmc.Player().stop()
            self.close()
        #else:  utils.logMsg("Action : %s" %(action.getId()),0)
# Action : 3 haut
#Action : 4 bas
# Action : 2 droite
# Action : 1 gauche

    def onClick(self, controlID):
        if controlID == 6 or controlID == 3: 
            ret = self.img_list.getSelectedPosition()
            
            if self.BAF==0: 
                xbmc.executebuiltin('Dialog.Close(all,true)')
            self.previousitem=""
            self.previousLABEL1999 = ""
            self.previousitemPlayer=""
            if str(self.ListeTrailer[ret]["key"])!="KODI": 
              
               xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id=%s,%d)' %(self.ListeTrailer[ret]["key"],self.BAF))
              
            else:
                xbmc.executebuiltin('PlayMedia("'+self.ListeTrailer[ret]["id"]+'",%d)' %(self.BAF) )
                #self.close()

    def onFocus(self, controlID):
        pass
        

def in_hours_and_min(minutes_string):
    try:
        full_minutes = int(minutes_string)
        minutes = full_minutes % 60
        hours   = full_minutes // 60
        return str(hours) + 'h' + str(minutes).zfill(2)
    except:
        return ''

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
             """   
             if action == "GETSAGA":
                Id=params.get("id",None)
                if Id: Id = Id[0]  
                utils.CheckSaga(Id)
                return  
             
             
                
             if action == "GETSAGAFANART":  
                Id=params.get("id",None)
                if Id: Id = Id[0]   
                utils.getSagaFanarts()
                return  
                              
             if action == "GETTRAILER":
                
                Id=params.get("id",None)
                if Id: Id = Id[0] 
                trailertype=params.get("trailertype",None)
                if trailertype: trailertype = trailertype[0] 
                utils.getTrailer(Id,trailertype)        
             """
             
             if action == "GETCAST":
                Id=params.get("id",None)
                if Id: Id = Id[0] 
                castingtype=params.get("casttype",None)
                if castingtype: castingtype = castingtype[0]
                utils.getCasting(castingtype,Id)
                
             
                
             if action == "GETTVFILMACTEUR":
                Id=params.get("id",None)
                if Id: 
                  Id = Id[0] 
                  infotype=params.get("infotype",None)
                  if infotype: infotype = infotype[0]
                  KodiLocal=params.get("local",None)
                  Acteur=utils.try_decode(Id.encode('utf8')) 
                  if not KodiLocal: 
                      utils.ActeurFilmsTvTMDB(infotype,Acteur.split(" (")[0])
                  else:                  
                      utils.ActeurFilmsTvKODI(infotype,Id.encode('utf8').split(" (")[0])

             if action == "GETARTISTEART":
                Id=params.get("id",None)
                if Id: Id = Id[0] 
                castingtype=params.get("casttype",None)
                if castingtype: castingtype = castingtype[0]
                Id=xbmc.getInfoLabel("ListItem.DBID")              
                utils.getArtisteArt(castingtype,Id)       
                
                
             if action == "TVDIFFUSION":
                TvSe=xbmc.getInfoLabel("ListItem.Season")
                TvId=xbmc.getInfoLabel("ListItem.DBID")
                TvType=xbmc.getInfoLabel("ListItem.DBTYPE")
                utils.getDiffusionTV(TvId,TvSe,TvType)
             
             
                     
                     
        except:
           params= {}
        
        try:
            params = dict( arg.split( '=' ) for arg in sys.argv[ 1 ].split( '&' ) )
        except:
            params = {}
            
        self.backend = params.get( 'backend', False )
        self.trailer = params.get( 'trailer', False )
        self.setview = params.get( 'setview', False )
        self.videcache = params.get( 'videcache', False )
        self.addplaylist = params.get( 'addplaylist', False )
        self.supplaylist = params.get( 'supplaylist', False )
        self.updateallmusic = params.get( 'updateallmusic', False )
        self.mettreajour = params.get( 'mettreajour', False )
        
        
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
                xbmc.executebuiltin("SetProperty(IconMixToolsbackend,true,home)")
                self.run_backend()
                
            #-------------METTRE A JOUR SAGA ou SERIE-------------
            DBTYPEX=xbmc.getInfoLabel("ListItem.DBTYPE")
            if xbmc.getCondVisibility("Container.Content(artists)"): 
                     DBTYPEX="artist"
            if self.mettreajour and ( DBTYPEX=="set" or DBTYPEX=="movie" or DBTYPEX=="tvshow" or DBTYPEX=="artist" or saga!=""):
                   if saga=="":
                     Unique="ok"
                   else:
                     Unique=""
                   
                 
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
                     Choix.append(__language__( 32507 )+" [COLOR=yellow]["+utils.try_decode(xbmc.getInfoLabel("ListItem.Label"))+"][/COLOR]")
                     
                   if DBTYPEX=="set"  or DBTYPEX=="movie" or DBTYPEX=="tvshow":
                       Choix.append(__language__( 32514 )+" [COLOR=yellow]"+utils.try_decode(xbmc.getInfoLabel("ListItem.Label"))+"[/COLOR]")
                   if DBTYPEX=="tvshow":
                     Choix.append(__language__( 32511 ))
                   
                   ret=dialog.select(Titre, Choix)
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
                    if DBTYPEX=="tvshow": utils.UpdateSeries(xbmc.getInfoLabel("ListItem.IMDBNumber"))                    
                    if DBTYPEX=="artist": utils.UpdateArtistes(xbmc.getInfoLabel("ListItem.DBID"))
                   if ret==3 and Unique: #ArtWorks
                    if DBTYPEX=="set": utils.UpdateSagas(xbmc.getInfoLabel("ListItem.DBID"),None,True)                    
                    if DBTYPEX=="tvshow": utils.updatetvartwork(xbmc.getInfoLabel("ListItem.DBID"))
                   if ret==4 and Unique: #ArtWorks
                    if DBTYPEX=="tvshow": utils.updateartworkall("TvShows")
                    
            #-------------BANDES ANNONCES-------------             
            if self.trailer :                
                self.windowhome.setProperty('FenetreListeChoix','1')
                dialog=xbmcgui.Dialog()                
                TrailerType=""
                ListeTrailer=[]
                TMDBID=''
                TypeVideo=xbmc.getInfoLabel("Container(5051).ListItem.Property(dbtype)")
                Titre=xbmc.getInfoLabel("Container(5051).ListItem.Label").decode('utf-8','ignore')
                if xbmc.getCondVisibility("Control.HasFocus(2999)"): #myvideonav
                    TypeVideo=xbmc.getInfoLabel("Container(1999).ListItem.DBType")
                    Titre=xbmc.getInfoLabel("Container(1999).ListItem.Label").decode('utf-8','ignore')
                    TrailerType="videonav"
                if xbmc.getCondVisibility("Control.HasFocus(2008)"): #dialogvideoinfo
                    TypeVideo='movie'
                    Titre=xbmc.getInfoLabel("Container(5002).ListItem.Label").decode('utf-8','ignore')
                    TrailerType="saga"
                if xbmc.getCondVisibility("ControlGroup(7003).HasFocus"): #dialogvideoinfo cherche trailer
                    TypeVideo=xbmc.getInfoLabel("ListItem.DBTYPE")
                    Titre=xbmc.getInfoLabel("ListItem.Label").decode('utf-8','ignore')
                    TrailerType="videoinfo7003"
                if xbmc.getCondVisibility("Control.HasFocus(7778)"): #dialogvideoinfo realisateur
                    TypeVideo=xbmc.getInfoLabel("Container(5052).ListItem.Property(dbtype)")
                    Titre=xbmc.getInfoLabel("Container(5052).ListItem.Label").decode('utf-8','ignore')
                    TrailerType="realisateur"
                dialog.notification('IconMixTools', __language__( 32508 )+": [COLOR=Yellow] "+Titre+"[/COLOR]", ADDON_ICON,1000)     
                if TrailerType=="" :
                     #acteurs  
                     if not xbmc.getInfoLabel("Container(5051).ListItem.Property(IMDBNumber)"):
                       #pas local
                       ListeTrailer=utils.getTrailer(xbmc.getInfoLabel("Container(5051).ListItem.Trailer"),TypeVideo) 
                     else:
                       #local
                       TMDBID=utils.get_externalID(xbmc.getInfoLabel("Container(5051).ListItem.Property(IMDBNumber)"),TypeVideo)
                       
                if TrailerType=="realisateur" :
                     #realisateur
                     if not xbmc.getInfoLabel("Container(5052).ListItem.Property(IMDBNumber)"):
                       #pas local
                       ListeTrailer=utils.getTrailer(xbmc.getInfoLabel("Container(5052).ListItem.Trailer"),TypeVideo) 
                     else:
                       #local
                       TMDBID=utils.get_externalID(xbmc.getInfoLabel("Container(5052).ListItem.Property(IMDBNumber)"),TypeVideo)
                        
                if TrailerType=="videonav" :
                     #VideoNav
                     IMDBID=xbmc.getInfoLabel("Container(1999).ListItem.Property(IMDBNumber)")
                     TMDBID=xbmc.getInfoLabel("Container(1999).ListItem.Property(TMDBNumber)")
                     if not TMDBID and not IMDBID:
                         json_result = utils.getJSON('VideoLibrary.Get%sDetails' %(TypeVideo), '{ "%sid":%d,"properties":["imdbnumber"] }' %(TypeVideo,int(xbmc.getInfoLabel("Container(1999).ListItem.DBID"))))                         
                         IMDBID=json_result.get("imdbnumber")                 
                     if TMDBID=='' and IMDBID:
                         TMDBID=utils.get_externalID(IMDBID,TypeVideo)
                         
                if TrailerType=="saga" :
                     #SAGA
                     IMDBID=xbmc.getInfoLabel("Container(5002).ListItem.Property(IMDBNumber)")
                     TMDBID=xbmc.getInfoLabel("Container(5002).ListItem.Property(TMDBNumber)")
                     if not TMDBID and not IMDBID:
                         json_result = utils.getJSON('VideoLibrary.GetMovieDetails', '{ "movieid":%d,"properties":["imdbnumber"] }' %(int(xbmc.getInfoLabel("Container(5002).ListItem.DBID"))))                         
                         IMDBID=json_result.get("imdbnumber")
                     
                     if TMDBID=='' and IMDBID:
                         TMDBID=utils.get_externalID(IMDBID,'movie')
                   
                
                if TrailerType=="videoinfo7003" :
                     #acteurs videoinfo                     
                     if TypeVideo!="episode":
                       IMDBNUMBER=xbmc.getInfoLabel("ListItem.IMDBNumber")
                     else:
                       IMDBNUMBER=xbmc.getInfoLabel("ListItem.TVShowTitle")
                       Titre=IMDBNUMBER
                     
                     if not IMDBNUMBER:
                       ListeTrailer=utils.getTrailer(xbmc.getInfoLabel("ListItem.Trailer"),TypeVideo) 
                     else:
                       TMDBID=utils.get_externalID(IMDBNUMBER,TypeVideo)
                 
                if TMDBID!='' :                    
                     ListeTrailer=utils.getTrailer(TMDBID,TypeVideo)
                     if TrailerType=="videonav" and str(xbmc.getInfoLabel("Container(1999).ListItem.Property(DBID)"))!="": 
                        ListeTrailer.append({"id":xbmc.getInfoLabel("Container(1999).ListItem.FilenameAndPath"),"position":"0","iso_639_1":"","iso_3166_1":"","key":"KODI","name":xbmc.getLocalizedString( 208 )+"[I]"+"[COLOR=LightGrey] "+xbmc.getInfoLabel("Container(1999).ListItem.Label").decode("utf8")+" [/I][/COLOR]","site":"YouTube","size":xbmc.getInfoLabel("Container(1999).ListItem.VideoResolution"),"type":"","landscape":xbmc.getInfoLabel("Container(1999).ListItem.Art(thumb)")})
                     if TrailerType=="saga" and str(xbmc.getInfoLabel("Container(5002).ListItem.Property(DBID)"))!="": 
                        ListeTrailer.append({"id":xbmc.getInfoLabel("Container(5002).ListItem.FilenameAndPath"),"position":"0","iso_639_1":"","iso_3166_1":"","key":"KODI","name":xbmc.getLocalizedString( 208 )+"[I]"+"[COLOR=LightGrey] "+xbmc.getInfoLabel("Container(5002).ListItem.Label").decode("utf8")+" [/I][/COLOR]","site":"YouTube","size":xbmc.getInfoLabel("Container(5002).ListItem.VideoResolution"),"type":"","landscape":xbmc.getInfoLabel("Container(5002).ListItem.Art(thumb)")})
                     if TrailerType=="videoinfo7003" and str(xbmc.getInfoLabel("ListItem.DBID"))!="":
                        ListeTrailer.append({"id":xbmc.getInfoLabel("ListItem.FilenameAndPath"),"position":"0","iso_639_1":"","iso_3166_1":"","key":"KODI","name":xbmc.getLocalizedString( 208 )+"[I]"+"[COLOR=LightGrey] "+xbmc.getInfoLabel("ListItem.Label").decode("utf8")+" [/I][/COLOR]","site":"YouTube","size":xbmc.getInfoLabel("ListItem.VideoResolution"),"type":"","landscape":xbmc.getInfoLabel("ListItem.Art(thumb)")})
                     if TrailerType=="" and str(xbmc.getInfoLabel("Container(5051).ListItem.Property(DBID)"))!="": 
                        ListeTrailer.append({"id":xbmc.getInfoLabel("Container(5051).ListItem.FilenameAndPath"),"position":"0","iso_639_1":"","iso_3166_1":"","key":"KODI","name":xbmc.getLocalizedString( 208 )+"[I]"+"[COLOR=LightGrey] "+xbmc.getInfoLabel("Container(5051).ListItem.Label").decode("utf8")+" [/I][/COLOR]","site":"YouTube","size":xbmc.getInfoLabel("Container(5051).ListItem.VideoResolution"),"type":"","landscape":xbmc.getInfoLabel("Container(5051).ListItem.Art(thumb)")})
                     if TrailerType=="realisateur" and str(xbmc.getInfoLabel("Container(5052).ListItem.Property(DBID)"))!="": 
                        ListeTrailer.append({"id":xbmc.getInfoLabel("Container(5052).ListItem.FilenameAndPath"),"position":"0","iso_639_1":"","iso_3166_1":"","key":"KODI","name":xbmc.getLocalizedString( 208 )+"[I]"+"[COLOR=LightGrey] "+xbmc.getInfoLabel("Container(5052).ListItem.Label").decode("utf8")+" [/I][/COLOR]","site":"YouTube","size":xbmc.getInfoLabel("Container(5052).ListItem.VideoResolution"),"type":"","landscape":xbmc.getInfoLabel("Container(5052).ListItem.Art(thumb)")})
                     
                
                
                if ListeTrailer:
                    ListeNomTrailer=[]
                    Image=""
                    for Item in  ListeTrailer:
                         NomTrailer=None
                        
                         if Item.get("key")!="KODI": 
                          Image="http://img.youtube.com/vi/%s/hqdefault.jpg" %(Item.get("key"))
                         else:
                          Image=urllib.unquote(Item.get("landscape").replace("image://",""))
                          utils.logMsg("Land :%s" %(Image,),0)
                         try: 
                              NomTrailer=utils.try_decode(Item["name"])+" ["+str(Item["type"])+" - "+str(Item["size"])+" - "+str(Item["iso_3166_1"]+"]")
                         except:
                              NomTrailer=str(Item["type"])+" ("+Item.get("size")+")"+" "+str(Item["iso_3166_1"])
                         Elements = xbmcgui.ListItem(label=NomTrailer, iconImage=str(Image),label2="selectionnevue")
                         Elements.setProperty("Icon", Image)
                         ListeNomTrailer.append(Elements)
                              
                    if len(ListeNomTrailer)>0:
                          #dialogC = xbmcgui.Dialog()
                          
                          
                          self.ui = dialog_select_UI('choix.xml', ADDON_PATH, 'default','1080i',listing=ListeNomTrailer,trailers=ListeTrailer)
                          self.windowhome.setProperty("IconMixTrailer","1")
                          ret=self.ui.doModal()
                          del self.ui                          
                          self.windowhome.clearProperty('IconMixTrailer')
                          
                              
                else: 
                    dialog=xbmcgui.Dialog()
                    dialog.notification('IconMixTools', Titre+": "+__language__( 32506 ), "acteurs/arfffff.png", 3000)
                self.windowhome.setProperty('FenetreListeChoix','')
                if  TrailerType=="" :  
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
                            xbmc.executebuiltin("SetFocus(2008)")
                    
            #-------------CHOIX DE LA VUE-------------             
            if self.setview:
                 content_type = utils.VueActuelle()
                 if not content_type:
                        content_type = "files"
                 current_view = xbmc.getInfoLabel("Container.Viewmode").decode("utf-8")
                 utils.ModeVues(content_type, current_view)

  		      #{"jsonrpc":"2.0","method":"Playlist.Add","id":-2067158130,"params":{"playlistid":0,"item":{"directory":"special://profile/playlists/music/Long Tracks.xsp"}}}
            #{"jsonrpc":"2.0","method":"Player.Open","id":1877953368,"params":{"options":{"shuffled":true},"item":{"playlistid":0,"position":0}}}  
            #-------------AJOUTER A UNE PLAYLIST-------------                              
       	    if self.addplaylist:           	        
                  utils.AddToPlayList()
            #-------------SUPPRIMER D'UNE PLAYLIST-------------                              
            if self.supplaylist:
                  utils.DelFromPlayList()
           
			    

    def _init_vars(self):
          self.windowhome = xbmcgui.Window(10000) # Home.xml 
          self.windowvideonav = xbmcgui.Window(10025) # myvideonav.xml           
          self.windowvideoinf = xbmcgui.Window(12003) # dialogvideoinfo.xml 
          self.windowvideoplayer = xbmcgui.Window(12901) # videoOSD.xml 
          self.windowvideoplayerinfo = xbmcgui.Window(10142) # DialogFullScreenInfo.xml
          
        
    def GetControl(self,Window=None,Id=None):
          ControlId=None          
          try:
               ControlId=Window.getControl(Id)  
          except:
               ControlId=None
          return ControlId
          
    def SetArtisteHomeVar(self,ArtisteData=None):
      if ArtisteData:
        self.windowhome.setProperty("ArtistBio",ArtisteData.get("ArtistBio"))
        self.windowhome.setProperty("ArtistThumb",ArtisteData.get("ArtistThumb"))
        self.windowhome.setProperty("ArtistLogo",ArtisteData.get("ArtistLogo"))
        self.windowhome.setProperty("ArtistBanner",ArtisteData.get("ArtistBanner"))
        self.windowhome.setProperty("ArtistFanart",ArtisteData.get("ArtistFanart"))
        self.windowhome.setProperty("ArtistFanart2",ArtisteData.get("ArtistFanart2"))
        self.windowhome.setProperty("ArtistFanart3",ArtisteData.get("ArtistFanart3"))   


   
                
        


    def run_backend(self):
        self.previousitem = ""
        self.previousitem8889 = ""
        self.previousitem1998 = ""
        self.previousLABEL1999 = ""
        self.previousitem1998local = ""
        self.previousitemMusic = ""
        self.previousitemPlayer= ""
        self.PreviousWindowActiveID= ""
        self.PreviousPlayerActiveID= ""
        self.DBTYPEOK = False
        self.DBTYPE= ""
        self.duration=""
        self.TvShow=""
        self.TvSeason=""
        status=""
        TvSe="o"
        TvSh="o"
        self.EpSa=0
        self.precedenttype=None
        self.windowhome.clearProperty('DurationTools')                   
        self.windowhome.clearProperty('DurationToolsEnd')
        self.windowhome.clearProperty('IconMixExtraFanart') 
        self.windowhome.clearProperty('IconMixEpSa')
        self.windowhome.clearProperty('IconMixSaga')
        self.windowhome.clearProperty('IconMixDirector')
        self.windowhome.clearProperty('IconMixActor')
        self.windowhome.clearProperty('IconMixTrailer')
        
        
        
        utils.logMsg('Version : %s - Service en cours..' %(ADDON_VERSION),0)
        while not xbmc.abortRequested: 
            #-------------------------- MUSIQUE EN LECTURE---------------------------------
            #-------------------------- 
            if xbmc.getCondVisibility("Player.HasAudio"):
                self.selecteditemAlbumPlayer = xbmc.getInfoLabel("MusicPlayer.Album")
                self.windowmusicvisID=None
                self.windowmusicvis=None
                if xbmc.getCondVisibility("Window.IsVisible(12006)"): self.windowmusicvisID = 12006 # musicvis.xml
                if xbmc.getCondVisibility("Window.IsVisible(10000)"): self.windowmusicvisID = 10000 
                if self.windowmusicvisID and not str(self.selecteditemAlbumPlayer)=="" and (self.previousitemPlayer != self.selecteditemAlbumPlayer or (self.windowmusicvisID and self.PreviousWindowActiveID!=self.windowmusicvisID)):
                  self.previousitemPlayer = self.selecteditemAlbumPlayer
                  self.selecteditemArtistPlayer = xbmc.getInfoLabel("MusicPlayer.Artist")
                  if self.windowmusicvisID: self.windowmusicvis = xbmcgui.Window(self.windowmusicvisID) # musicvis.xml
                  self.PreviousWindowActiveID=self.windowmusicvisID
                  if self.windowmusicvis: 
                    ListeFanarts=self.GetControl(self.windowmusicvis,2996)
                  self.vide_artisteplayer()
                  self.vide_albumplayer()
                  try:
                       AlbumData,ArtisteData=utils.GetMusicFicheAlbum(None,None,1,1,None)
                       if AlbumData:
                           if AlbumData.get("AlbumCover"): self.windowhome.setProperty("AlbumCoverPlayer",AlbumData.get("AlbumCover"))
                           if AlbumData.get("AlbumBack"): self.windowhome.setProperty("AlbumBackPlayer",AlbumData.get("AlbumBack"))
                           if AlbumData.get("AlbumCd"):
                              self.windowhome.setProperty("AlbumCdPlayer",AlbumData.get("AlbumCd"))
                           
                           if AlbumData.get("AlbumInfo"): self.windowhome.setProperty("AlbumInfoPlayer",AlbumData.get("AlbumInfo"))
                       if ArtisteData:
                            if ListeFanarts:
                                ListeFanarts.reset()
                                Fanarts=ArtisteData.get("fanarts")
                                if Fanarts:
                                  Fanarts2=new_array = random.sample( Fanarts, len(Fanarts) )
                                TabFanarts=[]
                                if Fanarts:
                                    for Item in Fanarts2:
                                           ItemListe=xbmcgui.ListItem(label="extrafanart",iconImage=Item)
                                           ItemListe.setInfo("pictures", {"title": "extrafanart","picturepath": Item}) 
                                           TabFanarts.append(ItemListe)
                                    
                                    ListeFanarts.addItems(TabFanarts) 
                            if ArtisteData.get("ArtistBio"): self.windowhome.setProperty("ArtistBioPlayer",ArtisteData.get("ArtistBio"))
                            if ArtisteData.get("ArtistThumb"): self.windowhome.setProperty("ArtistThumbPlayer",ArtisteData.get("ArtistThumb"))
                            if ArtisteData.get("ArtistLogo"): self.windowhome.setProperty("ArtistLogoPlayer",ArtisteData.get("ArtistLogo"))
                            if ArtisteData.get("ArtistBanner"): self.windowhome.setProperty("ArtistBannerPlayer",ArtisteData.get("ArtistBanner"))
                            if ArtisteData.get("ArtistFanart"): self.windowhome.setProperty("ArtistFanartPlayer",ArtisteData.get("ArtistFanart"))
                            if ArtisteData.get("ArtistFanart2"): self.windowhome.setProperty("ArtistFanart2Player",ArtisteData.get("ArtistFanart2"))
                            if ArtisteData.get("ArtistFanart3"): self.windowhome.setProperty("ArtistFanart3Player",ArtisteData.get("ArtistFanart3"))  
                  except:
                       utils.logMsg("Probleme : AlbumData,ArtisteData=utils.GetMusicFicheAlbum(None,None,1,1)",0)  
                
            #-------------------------- #VUES MUSIQUES ------------------------------------------
            if xbmc.getCondVisibility("Window.IsVisible(10502)"):
              ContainerGenre=0
              self.selecteditemMusic = xbmc.getInfoLabel("ListItem.DBID")
              LabelMusic = xbmc.getInfoLabel("ListItem.Label")
              Cover=xbmc.getInfoLabel("Container.ListItem.Icon")
                
              if self.selecteditemMusic==-1 or str(self.selecteditemMusic)=="" :
                 self.vide_album()
                 self.windowhome.clearProperty("iconmixExtraFanart")
                 self.windowhome.clearProperty('DurationToolsEnd')
                 self.windowhome.clearProperty('DurationTools')
                
              if self.selecteditemMusic>-1 and not str(self.selecteditemMusic)=="" and self.previousitemMusic != self.selecteditemMusic:
                self.previousitemMusic = self.selecteditemMusic
                #self.DBTYPE=xbmc.getInfoLabel("ListItem.DBTYPE")
                self.DBTYPE=xbmc.getInfoLabel("Container.Content")
                self.windowmusicnav = xbmcgui.Window(10502) # mymusicnav.xml
                ListeSaga=self.GetControl(self.windowmusicnav,1999)
                ListeFanarts=self.GetControl(self.windowmusicnav,2998)
                
                
                #if ((self.DBTYPE=="artist" or xbmc.getCondVisibility("Container.Content(artists)")) and Music1999==0) :
                if (self.DBTYPE=="artists" or self.DBTYPE=="genres"):
                #or (xbmc.getCondVisibility("Container.Content(genres)") and Music1999==1): #mise à jour artiste complete
                    if xbmc.getCondVisibility("Container.Content(genres)"): 
                       Music1999=0
                    ArtisteData=[]
                    self.vide_artiste()
                                     
                    #ArtisteData=utils.GetMusicFicheArtiste(LabelMusic,self.selecteditemMusic)
                    
                    
                    
                    ArtisteId=self.selecteditemMusic
                    ListeItemx=[] 
                    if ListeSaga:
                      ListeSaga.reset()
                      try:
                        if self.DBTYPE=="artists":
                           ListeItemx,ArtisteData=utils.CheckArtisteAlbums(ArtisteId,None,1)
                        if self.DBTYPE=="genres":
                           ListeItemx=utils.CheckGenres(LabelMusic)
                      except:
                        ListeItemx=None                      
                      if ListeItemx:
                           ListeSaga.addItems(ListeItemx)
                           
                    if ArtisteData:
                        if ListeFanarts:
                          ListeFanarts.reset()
                          Fanarts=ArtisteData.get("fanarts")
                          TabFanarts=[]
                          if Fanarts:
                              for Item in Fanarts:
                                     ItemListe=xbmcgui.ListItem(label="extrafanart",iconImage=Item)
                                     ItemListe.setInfo("pictures", {"title": "extrafanart","picturepath": Item}) 
                                     TabFanarts.append(ItemListe)
                              ListeFanarts.addItems(TabFanarts)  
                        
                        self.SetArtisteHomeVar(ArtisteData)       
                                                            
                           
                    
                   
                #if self.DBTYPE=="album" or xbmc.getCondVisibility("Container.Content(albums)") or self.DBTYPE=="song" or xbmc.getCondVisibility("Container.Content(songs)"): 
                if self.DBTYPE=="albums"  or self.DBTYPE=="songs": 
                   self.vide_album()
                   ListeSaga=self.GetControl(self.windowmusicnav,1999)
                   if ListeSaga:
                      ListeSaga.reset()
                   try:
                       if self.DBTYPE=="songs":
                                              
                         AlbumData,ArtisteData=utils.GetMusicFicheAlbum(self.selecteditemMusic,Cover,1,None,1,None)
                       else:
                         AlbumData,ArtisteData=utils.GetMusicFicheAlbum(self.selecteditemMusic,Cover,1,None,None,None)
                         
                       self.windowhome.clearProperty('DurationTools')                   
                       self.windowhome.clearProperty('DurationToolsEnd')
                       self.duration = xbmc.getInfoLabel("ListItem.Duration") 
                       self.display_duration() 
                         
                       if AlbumData:
                           self.windowhome.setProperty("AlbumCover",AlbumData.get("AlbumCover"))
                           self.windowhome.setProperty("AlbumBack",AlbumData.get("AlbumBack"))
                           if AlbumData.get("AlbumCd"):
                              self.windowhome.setProperty("AlbumCd",AlbumData.get("AlbumCd"))
                           else:
                              self.windowhome.setProperty("AlbumCd","")
                           self.windowhome.setProperty("AlbumInfo",AlbumData.get("AlbumInfo"))
                       if ArtisteData:
                          if ListeFanarts:
                              ListeFanarts.reset()
                              Fanarts=ArtisteData.get("fanarts")
                              TabFanarts=[]
                              if Fanarts:
                                  for Item in Fanarts:
                                         ItemListe=xbmcgui.ListItem(label="extrafanart",iconImage=Item)
                                         ItemListe.setInfo("pictures", {"title": "extrafanart","picturepath": Item}) 
                                         TabFanarts.append(ItemListe)
                                  ListeFanarts.addItems(TabFanarts) 
                          self.SetArtisteHomeVar(ArtisteData)  
                   except:
                       utils.logMsg("Probleme : AlbumData,ArtisteData=utils.GetMusicFicheAlbum(self.selecteditemMusic,Cover,None)",0)  
                
              
          
            #-------------------------- FILMS/SERIES/ACTEURS --------------------------
            #if not self.ui:
            if (self.windowhome.getProperty('IconMixTrailer')!="1") and (xbmc.getCondVisibility("Window.IsVisible(10025)") or xbmc.getCondVisibility("Window.IsVisible(12901)") or xbmc.getCondVisibility("Window.IsVisible(10142)") or xbmc.getCondVisibility("Window.IsVisible(12003)")) and not xbmc.getCondVisibility("Container.Scrolling") and not xbmc.getCondVisibility("Window.IsVisible(12000)"):
                
                MiseAjour=""
                TMDBNUMBER=None
               
                #-------------------------- ACTEURS : Roles/Bio---------------------------------
                if xbmc.getCondVisibility("Control.HasFocus(8889)") or xbmc.getCondVisibility("Control.HasFocus(1998)") or xbmc.getCondVisibility("Control.HasFocus(7779)") or xbmc.getCondVisibility("Control.HasFocus(7777)") or xbmc.getCondVisibility("Control.HasFocus(7778)"):
                    F8889=xbmc.getCondVisibility("Control.HasFocus(8889)")
                    F1998=xbmc.getCondVisibility("Control.HasFocus(1998)")
                    F7779=xbmc.getCondVisibility("Control.HasFocus(7779)")
                    F7777=xbmc.getCondVisibility("Control.HasFocus(7777)") or xbmc.getCondVisibility("Control.HasFocus(7778)")
                    if F8889 | F1998 | F7779 |F7777:
                      if not F8889:
                          ActeurRealisateur="acteurs"
                          if not F7777:
                             self.selecteditem1998 = xbmc.getInfoLabel("Container(1998).ListItem.Label").split(" (")[0]  
                          else:
                             self.selecteditem1998 = xbmc.getInfoLabel("ListItem.Director").split(" (")[0] 
                             ActeurRealisateur="director"             
                          
                          KodiLocal=self.windowhome.getProperty('ActeurVideoLocal')
                          if (self.previousitem1998 != self.selecteditem1998 and not str(self.selecteditem1998)=="") or ( self.previousitem1998local!=KodiLocal):
                            self.previousitem1998 = self.selecteditem1998
                            self.previousitem1998local=KodiLocal
                            if xbmc.getCondVisibility("Window.IsVisible(10025)"):
                               #ACTEURS VIDEONAV
                               ListeRole=self.GetControl(self.windowvideonav,5051)
                               
                            if xbmc.getCondVisibility("Window.IsVisible(12003)"):
                               #ACTEURS VIDEOINFO
                               if not F7777:
                                ListeRole=self.GetControl(self.windowvideoinf,5051)
                               else:
                                ListeRole=self.GetControl(self.windowvideoinf,5052)
                               
                            if xbmc.getCondVisibility("Window.IsVisible(12901)"):
                               #ACTEURS VideoPlayer
                               ListeRole=self.GetControl(self.windowvideoplayer,5051)
                               
                            if xbmc.getCondVisibility("Window.IsVisible(10142)"):
                               #ACTEURS VideoPlayer
                               ListeRole=self.GetControl(self.windowvideoplayerinfo,5051)                              
                               
                             
                            if ListeRole:
                             #Acteur=utils.try_decode(self.selecteditem1998.encode('utf8'))
                             #https://api.themoviedb.org/3/search/person?api_key=67158e2af1624020e34fd893c881b019&language=en-US&query=Rafael%20L%C3%B3pez&page=1&include_adult=false
                              Acteur=self.selecteditem1998.decode("utf8") 
                              if not KodiLocal: 
                                     ListeItemx=utils.ActeurFilmsTvTMDB(ActeurRealisateur,utils.try_decode(Acteur.encode("utf8")),1) 
                              else:
                                     ListeItemx=utils.ActeurFilmsTvKODI(ActeurRealisateur,self.selecteditem1998.split(" (")[0],1)
                                   
                              ListeRole.reset()
                              if ListeItemx: 
                                   for itemX in ListeItemx:
                                        ListeRole.addItem(itemX) 
                              else:
                                 ItemVide = xbmcgui.ListItem(label="******",iconImage="DefaultTVShows.png",label2="*******") 
                                 ItemVide.setProperty("dbtype","movie")
                                 ItemVide.setInfo("video", {"title": "oooo","year": "1970","originaltitle": "original_title","trailer":"id"}) 
                                 ListeRole.addItem(ItemVide)                                 
                              status=""
                      if not F1998:
                          ActiF7779="non"
                          if F7779  or F7777:
                              if F7779:
                                 self.selecteditem8889 = xbmc.getInfoLabel("Container(1998).ListItem.Label")
                              else:
                                 self.selecteditem8889 = xbmc.getInfoLabel("ListItem.Director") 
                          else:
                              if not xbmc.getCondVisibility("Player.HasVideo"):
                                  self.selecteditem8889 = xbmc.getInfoLabel("ListItem.DBID")
                              else:
                                  self.selecteditem8889 = xbmc.getInfoLabel("VideoPlayer.DBID")                   
                              
                          self.previousitem = ""
                          self.previousitemMusic = ""
                          if self.previousitem8889 != self.selecteditem8889 and not str(self.selecteditem8889)=="":
                              if F7779 or F7777:
                                ActiF7779="oui"
                                if not F7777:
                                    self.LABEL8889=xbmc.getInfoLabel("Container(1998).ListItem.Label").split(" (")[0].decode("utf8")
                                    self.DBTYPE=xbmc.getInfoLabel("Container(1998).ListItem.DBTYPE")
                                   
                                else:
                                    self.LABEL8889=xbmc.getInfoLabel("ListItem.Director").split(" (")[0].decode("utf8")
                                    self.DBTYPE="director"
                              else: 
                                self.LABEL8889=xbmc.getInfoLabel("ListItem.Label").split(" (")[0].decode("utf8")
                                self.DBTYPE=xbmc.getInfoLabel("ListItem.DBTYPE")
                                
                              self.previousitem8889 = self.selecteditem8889
                              self.windowhome.clearProperty('Actorbiographie')
                              self.windowhome.clearProperty('Actornaissance')
                              self.windowhome.clearProperty('Actordeces')                                                 
                              self.windowhome.clearProperty('Actorlieunaissance')
                              self.windowhome.clearProperty('ActorAge')
                              self.windowhome.clearProperty('ActorNomReel')
                              InfoDate=None
                              Lieu=None
                              if ActiF7779!="oui": 
                                 xbmc.executebuiltin( "ActivateWindow(busydialog)" ) 
                              if not Lieu:                   
                                  InfoSup=utils.GetActeurInfo(utils.try_decode(self.LABEL8889.encode("utf8")),self.DBTYPE)
                                  
                                  if InfoSup : 
                                      self.windowhome.setProperty('Actorbiographie',InfoSup.get("biographie"))
                                      Lieu=InfoSup.get("lieunaissance")
                                      self.windowhome.setProperty('Actorlieunaissance',InfoSup.get("lieunaissance"))  
                                      self.windowhome.setProperty('ActorNomReel',InfoSup.get("nomreel"))

                                      InfoDate= InfoSup.get("naissance")

                                      if InfoDate:                         
                                          XBRegion=str(xbmc.getRegion('dateshort'))
                                          if XBRegion=="%d/%m/%Y":                             
                                           self.windowhome.setProperty('Actornaissance',str(InfoDate[8:10]+"/"+InfoDate[5:7]+"/"+InfoDate[0:4])) 
                                          else:                             
                                           self.windowhome.setProperty('Actornaissance',str(InfoDate))                                                             
                                          InfoDate= InfoSup.get("deces")                   
                                          if InfoDate:
                                              XBRegion=str(xbmc.getRegion('dateshort'))
                                              if XBRegion=="%d/%m/%Y":                             
                                               self.windowhome.setProperty('Actordeces',str(InfoDate[8:10]+"/"+InfoDate[5:7]+"/"+InfoDate[0:4])) 
                                              else:                             
                                               self.windowhome.setProperty('Actordeces',str(InfoDate))
                                              Age=""
                                          else:
                                              Age =  str(int(datetime.now().date().year) - int(InfoSup.get("naissance")[0:4])) 
                                              self.windowhome.setProperty('Actorage',Age) 
                              if ActiF7779!="oui": 
                                  xbmc.executebuiltin( "Dialog.Close(busydialog)" )
                              
                              if not InfoDate and not Lieu:
                                       if ActiF7779!="oui": 
                                           dialog=xbmcgui.Dialog()
                                           dialog.notification('IconMixTools', __language__( 32584 )+self.LABEL8889, "acteurs/arfffff.png", 3000)
                                           xbmc.executebuiltin("SetFocus(55)")                                 
                #-------------------------- FILMS/SERIES ---------------------------------   
                #roles  ------------------------------------------------
                else:
                    self.previousitem8889 = ""  
                    self.previousitemMusic = ""
                        
                    if xbmc.getCondVisibility("Control.HasFocus(2999)"): #focus sur SAGA
                        self.LABEL1999=xbmc.getInfoLabel("Container(1999).ListItem.Label")
                        TMDBNUMBER=xbmc.getInfoLabel("Container(1999).ListItem.property(TMDBNUMBER)")
                        if not TMDBNUMBER :
                         self.selecteditem = xbmc.getInfoLabel("Container(1999).ListItem.DBID")
                        else:
                         self.selecteditem = TMDBNUMBER
                        self.DBTYPE=xbmc.getInfoLabel("Container(1999).ListItem.DBTYPE")  
                        if (self.previousitem != self.selecteditem) or (self.LABEL1999!=self.previousLABEL1999)  :
                             self.previousitem = self.selecteditem
                             self.previousLABEL1999=self.LABEL1999
                             MiseAjour="1"                   
                    else : 
                        if not xbmc.getCondVisibility("Window.IsVisible(12901)") and  not xbmc.getCondVisibility("Window.IsVisible(10142)"):
                            self.selecteditem = xbmc.getInfoLabel("ListItem.DBID")
                            self.DBTYPE=xbmc.getInfoLabel("ListItem.DBTYPE")
                            self.previousitemPlayer=""
                        else: #videoplayer
                            self.selecteditem = xbmc.getInfoLabel("VideoPlayer.DBID")
                            if xbmc.getCondVisibility("Window.IsVisible(12901)"):
                              self.PlayerActiveID=1
                            if xbmc.getCondVisibility("Window.IsVisible(10142)"):
                              self.PlayerActiveID=2
                            
                            
                            if self.PreviousPlayerActiveID!=self.PlayerActiveID:
                              self.PreviousPlayerActiveID=self.PlayerActiveID
                              self.previousitemPlayer=""                         
                            
                            if self.previousitemPlayer != self.selecteditem :
                               self.previousitem=""
                            if xbmc.getCondVisibility("!String.IsEmpty(VideoPlayer.TVShowTitle)"):
                               self.DBTYPE="episode"
                            else:
                               self.DBTYPE="movie"                            
                         
                        if (self.previousitem != self.selecteditem)  or (self.windowhome.getProperty('IconMixUpdateSagas')=="1") :
                             self.previousitem = self.selecteditem
                             MiseAjour="1"
                             if xbmc.getCondVisibility("Window.IsVisible(12901)"): #videoplayer
                                MiseAjour="3"
                                self.previousitemPlayer = self.selecteditem
                             if xbmc.getCondVisibility("Window.IsVisible(10142)") :#videoplayer
                                MiseAjour="4"
                                self.previousitemPlayer = self.selecteditem
                                 
                             if xbmc.getCondVisibility("Window.IsVisible(12003)") :#videoinfo
                                  MiseAjour="2" 
                             self.windowhome.clearProperty('IconMixUpdateSagas')
                                        
                    if not self.selecteditem :
                        self.windowhome.clearProperty('IconMixExtraFanart')
                        
                    if MiseAjour!="" : #liste des acteurs
                        self.windowhome.setProperty('IconMixUpdating','1')                     
                        self.DBTYPEOK= (self.DBTYPE!="set" and self.DBTYPE!="tvshow" and self.DBTYPE!="season" and self.DBTYPE!="addon" and self.DBTYPE!="artist") or (xbmc.getCondVisibility("Control.HasFocus(2999)"))
                        
                        self.windowhome.clearProperty('DurationTools')                   
                        self.windowhome.clearProperty('DurationToolsEnd')
                        self.windowhome.clearProperty('IconMixExtraFanart') 
                        #self.windowhome.clearProperty("ItemCountry1")
                        self.windowhome.clearProperty("ItemCountry2")
                        self.windowhome.clearProperty("ItemCountry3")
                        self.windowhome.clearProperty("ItemCountry4")
                        
                        #focus 2999 (saga) panneau acteurs
                        if xbmc.getCondVisibility("Control.HasFocus(2999)"):
                            if self.selecteditem > -1 and not str(self.selecteditem)=="":                          
                              if self.DBTYPEOK:
                                    ListeActeurs=self.GetControl(self.windowvideonav,1998)
                                    #ACTEURS  ------------------------------------------------                                 
                                    if ListeActeurs:
                                      ListeItemx=utils.getCasting(self.DBTYPE,self.selecteditem,1,TMDBNUMBER)
                                      ListeActeurs.reset()
                                      if ListeItemx: 
                                           for itemX in ListeItemx:
                                                ListeActeurs.addItem(itemX) 
                                                                               
                                      status=""
                                
                                    self.windowhome.setProperty('IconMixExtraFanart',utils.CheckItemExtrafanartPath(xbmc.getInfoLabel("Container(1999).ListItem.Path")))   
                                    self.duration = xbmc.getInfoLabel("Container(1999).ListItem.Duration") 
                                    self.display_duration()
                        
                        else:
                          
                          if self.selecteditem > -1 and not str(self.selecteditem)=="": #liste des acteurs
                              self.windowhome.clearProperty('IconMixSagaClearArt')  
                              self.windowhome.clearProperty('IconMixSagaClearLogo')
                              self.windowhome.clearProperty('IconMixSagaBackGround')
                              self.windowhome.clearProperty('IconMixSagaBanner')
                              self.windowhome.clearProperty('IconMixSagaDiscArt')
                              self.windowhome.clearProperty('IconMixSagaPoster')
                              self.windowhome.clearProperty('IconMixSagaThumb') 
                              
                              ListeItemx=[]
                              ResetDirector=True                         
                              #if not self.DBTYPE=="set" and not status=="1":
                              if not status=="1":
                                status="1"
                                if MiseAjour=="1":
                                   #ACTEURS VIDEONAV
                                   ListeActeurs=self.GetControl(self.windowvideonav,1998)
                                   
                                if MiseAjour=="2":
                                   #ACTEURS VIDEOINFO
                                   ListeActeurs=self.GetControl(self.windowvideoinf,1998)
                                   
                                if MiseAjour=="3":
                                   #ACTEURS VideoPlayer
                                   ListeActeurs=self.GetControl(self.windowvideoplayer,1998)
                                if MiseAjour=="4":
                                   #ACTEURS VideoPlayer
                                   ListeActeurs=self.GetControl(self.windowvideoplayerinfo,1998)
                                   
                                #ACTEURS  ------------------------------------------------                                 
                                if ListeActeurs:
                                  ListeItemx=utils.getCasting(self.DBTYPE,self.selecteditem,1,TMDBNUMBER)
                                  ListeActeurs.reset()
                                  if ListeItemx: 
                                       for itemX in ListeItemx:
                                            ListeActeurs.addItem(itemX)                                   
                                       self.windowhome.setProperty('IconMixDirector',str(utils.getRealisateur('realisateur',self.selecteditem,realisateur=xbmc.getInfoLabel("ListItem.Director"))))
                                       ResetDirector=False
                                  status=""
                                  
                              #SAGAS ------------------------------------------------
                              if not xbmc.getCondVisibility("Window.IsVisible(12901)") and not xbmc.getCondVisibility("Window.IsVisible(10142)") : #pas en lecture visible
                                  if (self.DBTYPE=="set" or MiseAjour=="2") and not status=="1": #mise à jour saga (videonav ou videoinfo)
                                    status="1"
                                    if not MiseAjour=="2":
                                       ListeSaga=self.GetControl(self.windowvideonav,1999)
                                       ListeFanarts=self.GetControl(self.windowvideonav,5555)                                       
                                       SetID=self.selecteditem
                                    else:
                                       ListeSaga=self.GetControl(self.windowvideoinf,5002)
                                       ListeFanarts=None
                                       SetID=xbmc.getInfoLabel("ListItem.SetId")
                                       
                                    if ListeSaga and SetID:
                                      NbItems=ListeSaga.size()
                                      FileTab=[]
                                      try:
                                        ListeItemx,FileTab =utils.CheckSaga(SetID,1)
                                      except:
                                        ListeItemx=None
                                      ListeSaga.reset()
                                      if ListeItemx:
                                           ListeSaga.addItems(ListeItemx)                                       
                                           if FileTab and ListeFanarts:
                                             ListeFanarts.reset()                                         
                                             for index in FileTab:                                             
                                                 Liste=utils.getSagaFanartsV2(index)
                                                 if Liste:                                                
                                                    ListeFanarts.addItems(Liste)
                                           #ListeSaga.selectItem(1)         
                                           #utils.getSagaItemPath()
                                                                           
                                    status=""
                                    
                                  if self.DBTYPEOK or self.DBTYPE=="tvshow":
                                     self.windowhome.setProperty('IconMixExtraFanart',utils.CheckItemExtrafanartPath(xbmc.getInfoLabel("ListItem.Path")))
                                     #self.windowhome.setProperty('IconMixTvShowCountry',utils.GetTvShowCountry(self.selecteditem))
                                     if self.DBTYPE!="tvshow":                                    
                                       #self.windowhome.setProperty('IconMixExtraFanart',utils.CheckItemExtrafanartPath(self.DBTYPE,self.selecteditem))
                                       self.duration = xbmc.getInfoLabel("ListItem.Duration") 
                                       self.display_duration()
                                     else:
                                       utils.getepisodes(int(self.selecteditem),None,self.DBTYPE,None)
                                       
                                  if self.DBTYPE=="episode" and xbmc.getCondVisibility("Skin.HasSetting(CheckSeries)"):
                                       TvSh=xbmc.getInfoLabel("ListItem.TVShowTitle") 
                                       TvSe=xbmc.getInfoLabel("ListItem.Season")
                                       TvId=self.selecteditem
                                       
                                       TvNbKodi=xbmc.getInfoLabel("Container.NumItems")
                                       if TvId and TvSe and TvSh :
                                         if TvSe!=self.TvSeason or TvSh!=self.TvShow : 
                                           self.windowhome.clearProperty('IconMixEpSa')      
                                           self.EpSa=utils.getepisodes(int(TvId),int(TvSe),self.DBTYPE,TvNbKodi)                                           
                                           if self.EpSa>=0:                                     
                                             self.windowhome.setProperty('IconMixEpSa',str(self.EpSa))                                       
                                             self.TvShow=TvSh
                                             self.TvSeason=TvSe
                                           else:                                     
                                             self.windowhome.clearProperty('IconMixEpSa')
                                             self.TvShow=""
                                             self.TvSeason=""                                      
                                       else : self.windowhome.clearProperty('IconMixEpSa')
                                  if (self.DBTYPE=="director" or self.DBTYPE=="actor") and "Default" in xbmc.getInfoLabel("ListItem.Icon") :
                                       if self.DBTYPE=="director":
                                           self.windowhome.setProperty('IconMixDirector',str(utils.getRealisateur('realisateur',self.selecteditem,realisateur=xbmc.getInfoLabel("ListItem.label"))))
                                       else:
                                           self.windowhome.setProperty('IconMixDirector',str(utils.getRealisateur('acteur',xbmc.getInfoLabel("ListItem.DBID"),realisateur=xbmc.getInfoLabel("ListItem.label"))))
                                      
                                  else :                                       
                                      if ResetDirector:
                                          self.windowhome.clearProperty('IconMixDirector')
                                  self.duration = xbmc.getInfoLabel("ListItem.Duration") 
                                  self.display_duration()
                              else : 
                                self.windowhome.clearProperty('IconMixEpSa')
                                self.TvShow=""
                                self.TvSeason=""        
                          else : 
                             ListeActeurs=self.GetControl(self.windowvideonav,1998)
                                    #ACTEURS  ------------------------------------------------                                 
                             if ListeActeurs:                              
                              ListeActeurs.reset()
                             self.windowhome.clearProperty('IconMixEpSa')
                             self.TvShow=""
                             self.TvSeason=""
                    self.windowhome.clearProperty('IconMixUpdating') 
                               
            xbmc.sleep(200)
        utils.logMsg("Astalavista baby ;)")
            
    def vide_artiste(self):
        self.windowhome.clearProperty("ArtistBio")
        self.windowhome.clearProperty("ArtistThumb")
        self.windowhome.clearProperty("ArtistLogo")
        self.windowhome.clearProperty("ArtistBanner")
        self.windowhome.clearProperty("ArtistFanart")
        self.windowhome.clearProperty("ArtistFanart2")
        self.windowhome.clearProperty("ArtistFanart3") 
        
    def vide_album(self):
       self.windowhome.clearProperty("AlbumCover")
       self.windowhome.clearProperty("AlbumBack")
       self.windowhome.clearProperty("AlbumCd")
       self.windowhome.clearProperty("AlbumInfo")
       
    def vide_artisteplayer(self):
        self.windowhome.clearProperty("ArtistBioPlayer")
        self.windowhome.clearProperty("ArtistThumbPlayer")
        self.windowhome.clearProperty("ArtistLogoPlayer")
        self.windowhome.clearProperty("ArtistBannerPlayer")
        self.windowhome.clearProperty("ArtistFanartPlayer")
        self.windowhome.clearProperty("ArtistFanart2Player")
        self.windowhome.clearProperty("ArtistFanart3Player") 
        
    def vide_albumplayer(self):
       self.windowhome.clearProperty("AlbumCoverPlayer")
       self.windowhome.clearProperty("AlbumBackPlayer")
       self.windowhome.clearProperty("AlbumCdPlayer")
       self.windowhome.clearProperty("AlbumInfoPlayer")
           

    def display_duration(self):
        Traduction={"île de l’ascension":"ascension island",
"andorre":"andorra",
"émirats arabes unis":"united arab emirates",
"afghanistan":"afghanistan",
"antigua-et-barbuda":"antigua & barbuda",
"anguilla":"anguilla",
"angleterre":"united kingdom",
"albanie":"albania",
"arménie":"armenia",
"angola":"angola",
"antarctique":"antarctica",
"argentine":"argentina",
"samoa américaines":"american samoa",
"autriche":"austria",
"australie":"australia",
"aruba":"aruba",
"îles åland":"åland islands",
"azerbaïdjan":"azerbaijan",
"bosnie-herzégovine":"bosnia & herzegovina",
"barbade":"barbados",
"bangladesh":"bangladesh",
"belgique":"belgium",
"burkina faso":"burkina faso",
"bulgarie":"bulgaria",
"bahreïn":"bahrain",
"burundi":"burundi",
"bénin":"benin",
"saint-barthélemy":"st. barthélemy",
"bermudes":"bermuda",
"brunéi darussalam":"brunei",
"bolivie":"bolivia",
"pays-bas caribéens":"caribbean netherlands",
"brésil":"brazil",
"bahamas":"bahamas",
"bhoutan":"bhutan",
"botswana":"botswana",
"biélorussie":"belarus",
"belize":"belize",
"canada":"canada",
"îles cocos":"cocos (keeling) islands",
"congo-kinshasa":"congo - kinshasa",
"république centrafricaine":"central african republic",
"congo-brazzaville":"congo - brazzaville",
"suisse":"switzerland",
"côte d’ivoire":"côte d’ivoire",
"îles cook":"cook islands",
"chili":"chile",
"cameroun":"cameroon",
"chine":"china",
"colombie":"colombia",
"costa rica":"costa rica",
"cuba":"cuba",
"cap-vert":"cape verde",
"curaçao":"curaçao",
"île christmas":"christmas island",
"chypre":"cyprus",
"république tchèque":"czech republic",
"allemagne":"germany",
"diego garcia":"diego garcia",
"djibouti":"djibouti",
"danemark":"denmark",
"dominique":"dominica",
"république dominicaine":"dominican republic",
"algérie":"algeria",
"ceuta et melilla":"ceuta & melilla",
"équateur":"ecuador",
"estonie":"estonia",
"égypte":"egypt",
"sahara occidental":"western sahara",
"érythrée":"eritrea",
"espagne":"spain",
"éthiopie":"ethiopia",
"finlande":"finland",
"fidji":"fiji",
"îles malouines":"falkland islands",
"états fédérés de micronésie":"micronesia",
"îles féroé":"faroe islands",
"france":"france",
"gabon":"gabon",
"royaume-uni":"united kingdom",
"royaume uni":"united kingdom",
"grenade":"grenada",
"géorgie":"georgia",
"guyane française":"french guiana",
"guernesey":"guernsey",
"ghana":"ghana",
"gibraltar":"gibraltar",
"groenland":"greenland",
"gambie":"gambia",
"guinée":"guinea",
"guadeloupe":"guadeloupe",
"guinée équatoriale":"equatorial guinea",
"grèce":"greece",
"îles géorgie du sud et sandwich du sud":"south georgia & south sandwich islands",
"guatemala":"guatemala",
"guam":"guam",
"guinée-bissau":"guinea-bissau",
"guyana":"guyana",
"r.a.s. chinoise de hong kong":"hong kong sar china",
"honduras":"honduras",
"croatie":"croatia",
"haïti":"haiti",
"hongrie":"hungary",
"îles canaries":"canary islands",
"indonésie":"indonesia",
"irlande":"ireland",
"israël":"israel",
"île de man":"isle of man",
"inde":"india",
"territoire britannique de l’océan indien":"british indian ocean territory",
"irak":"iraq",
"iran":"iran",
"islande":"iceland",
"italie":"italy",
"jersey":"jersey",
"jamaïque":"jamaica",
"jordanie":"jordan",
"japon":"japan",
"kenya":"kenya",
"kirghizistan":"kyrgyzstan",
"cambodge":"cambodia",
"kiribati":"kiribati",
"comores":"comoros",
"saint-christophe-et-niévès":"st. kitts & nevis",
"corée du nord":"north korea",
"corée du sud":"south korea",
"koweït":"kuwait",
"îles caïmans":"cayman islands",
"kazakhstan":"kazakhstan",
"laos":"laos",
"liban":"lebanon",
"sainte-lucie":"st. lucia",
"liechtenstein":"liechtenstein",
"sri lanka":"sri lanka",
"libéria":"liberia",
"lesotho":"lesotho",
"lituanie":"lithuania",
"luxembourg":"luxembourg",
"lettonie":"latvia",
"libye":"libya",
"maroc":"morocco",
"monaco":"monaco",
"moldavie":"moldova",
"monténégro":"montenegro",
"saint-martin (partie française)":"st. martin",
"madagascar":"madagascar",
"îles marshall":"marshall islands",
"macédoine":"macedonia",
"mali":"mali",
"myanmar":"myanmar (burma)",
"mongolie":"mongolia",
"r.a.s. chinoise de macao":"macau sar china",
"îles mariannes du nord":"northern mariana islands",
"martinique":"martinique",
"mauritanie":"mauritania",
"montserrat":"montserrat",
"malte":"malta",
"maurice":"mauritius",
"maldives":"maldives",
"malawi":"malawi",
"mexique":"mexico",
"malaisie":"malaysia",
"mozambique":"mozambique",
"namibie":"namibia",
"nouvelle-calédonie":"new caledonia",
"niger":"niger",
"île norfolk":"norfolk island",
"nigéria":"nigeria",
"nicaragua":"nicaragua",
"pays-bas":"netherlands",
"norvège":"norway",
"népal":"nepal",
"nauru":"nauru",
"niue":"niue",
"nouvelle-zélande":"new zealand",
"oman":"oman",
"panama":"panama",
"pérou":"peru",
"polynésie française":"french polynesia",
"papouasie-nouvelle-guinée":"papua new guinea",
"philippines":"philippines",
"pakistan":"pakistan",
"pologne":"poland",
"saint-pierre-et-miquelon":"st. pierre & miquelon",
"pitcairn":"pitcairn islands",
"porto rico":"puerto rico",
"territoires palestiniens":"palestinian territories",
"portugal":"portugal",
"palaos":"palau",
"paraguay":"paraguay",
"qatar":"qatar",
"la réunion":"réunion",
"roumanie":"romania",
"serbie":"serbia",
"russie":"russia",
"rwanda":"rwanda",
"arabie saoudite":"saudi arabia",
"îles salomon":"solomon islands",
"seychelles":"seychelles",
"soudan":"sudan",
"suède":"sweden",
"singapour":"singapore",
"sainte-hélène":"st. helena",
"slovénie":"slovenia",
"svalbard et jan mayen":"svalbard & jan mayen",
"slovaquie":"slovakia",
"sierra leone":"sierra leone",
"saint-marin":"san marino",
"sénégal":"senegal",
"somalie":"somalia",
"suriname":"suriname",
"soudan du sud":"south sudan",
"sao tomé-et-principe":"são tomé & príncipe",
"el salvador":"el salvador",
"saint-martin":"sint maarten",
"syrie":"syria",
"swaziland":"swaziland",
"tristan da cunha":"tristan da cunha",
"îles turques-et-caïques":"turks & caicos islands",
"tchad":"chad",
"terres australes françaises":"french southern territories",
"togo":"togo",
"thaïlande":"thailand",
"tadjikistan":"tajikistan",
"tokelau":"tokelau",
"timor oriental":"timor-leste",
"turkménistan":"turkmenistan",
"tunisie":"tunisia",
"tonga":"tonga",
"turquie":"turkey",
"trinité-et-tobago":"trinidad & tobago",
"tuvalu":"tuvalu",
"taïwan":"taiwan",
"tanzanie":"tanzania",
"ukraine":"ukraine",
"ouganda":"uganda",
"îles mineures éloignées des états-unis":"u.s. outlying islands",
"états-unis":"united states of america",
"uruguay":"uruguay",
"ouzbékistan":"uzbekistan",
"état de la cité du vatican":"vatican city",
"saint-vincent-et-les-grenadines":"st. vincent & grenadines",
"venezuela":"venezuela",
"îles vierges britanniques":"british virgin islands",
"îles vierges des états-unis":"u.s. virgin islands",
"vietnam":"vietnam",
"vanuatu":"vanuatu",
"wallis-et-futuna":"wallis & futuna",
"samoa":"samoa",
"kosovo":"kosovo",
"yémen":"yemen",
"mayotte":"mayotte",
"afrique du sud":"south africa",
"zambie":"zambia",
"zimbabwe":"zimbabwe"}
        xxx="null"
        
        #self.windowhome.setProperty('ItemUniqueGenre',xbmc.getInfoLabel( "ListItem.Genre" ).replace(" /",", "))
        
        if self.DBTYPE=="movie":
          CountryList=xbmc.getInfoLabel( "ListItem.Country" ).replace("/",",")
          CountryList=CountryList.split(",")
          if not CountryList:
            CountryList.append(xbmc.getInfoLabel( "ListItem.Country" ))
          idx=1
          for country in CountryList:
             Pays=country.strip()
             TradFrEn=Traduction.get(country.strip().lower())
             if TradFrEn:
               Pays=TradFrEn
             self.windowhome.setProperty('ItemCountry%d' %(idx),Pays)
             
             idx=idx+1
       
        if self.duration :
        #else :
         if self.duration.find(':')!=-1: #KODI LEIA
            TT=self.duration.rsplit(':')
            XX=0
            if len(TT)==3:
              XX=XX+int(TT[0])*60
              XX=XX+int(TT[1])
            if len(TT)==2:
              XX=int(TT[0])
            if len(TT)>1:
             self.duration=str(XX)
        
         if self.duration.find(':')==-1:
            readable_duration = in_hours_and_min(self.duration)
            self.windowhome.setProperty('DurationTools', readable_duration)
            if int(self.duration)>0:
              now = datetime.now()
              now_plus_10 = now + timedelta(minutes = int(self.duration))
              xxx = format(now_plus_10, '%Hh%M')
              self.windowhome.setProperty('DurationToolsEnd', xxx)
            else:
              self.windowhome.clearProperty('DurationToolsEnd')
              self.windowhome.clearProperty('DurationTools')
         else:
           self.windowhome.setProperty('DurationTools', self.duration)
         

          		   

if (__name__ == "__main__"):
    Main()
    #utils.logMsg('script finished.')
