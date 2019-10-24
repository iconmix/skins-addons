# coding: utf-8
#from __future__ import unicode_literals
import locale
import resources.lib.Utils as utils
from resources.lib.Utils import logMsg
import resources.lib.pays as pays
from unidecode import unidecode
from datetime import datetime,timedelta
import _strptime
import urlparse,urllib
import time
from time import sleep
import unicodedata
import os,io
import xbmc,xbmcgui,xbmcaddon,xbmcplugin,xbmcvfs
import random
import MonAutoCompletion
import youturl
import threading
#from multiprocessing import Process
#containers :
#1998 : Acteurs
#1999 : éléments des sagas, des acteurs et réalisateurs, et artistes (musique)
#5555 : fanarts 
#5051 : liste roles acteur
#5052: liste films/series realisateur

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
SETTING = ADDON.getSetting
KODI_VERSION  = int(xbmc.getInfoLabel( "System.BuildVersion" ).split(".")[0])
ACTION_PREVIOUS_MENU = (9, 10, 92, 216, 247, 257, 275, 61467, 61448)
__skin_string__ = xbmc.getLocalizedString
KODILANGCODE = xbmc.getLanguage(xbmc.ISO_639_1).lower()



class myMonitor(xbmc.Monitor):
  
  #------------------------------------------------------------------------------------------------------------------
  def __init__(self):
    self.updatesetting()
    self.ScanFinished=None
    self.previousitem=None
    # != self.selecteditem or self.windowhome.getProperty('IconMixUpdateEpisodes')=='1':                    
    self.precedenttvshow=None
    xbmc.Monitor.__init__(self)
    
  #------------------------------------------------------------------------------------------------------------------
  def updatesetting(self):
    self.ADDON = xbmcaddon.Addon()
    try:
     self.tempsannonce=int(self.ADDON.getSetting('tempsannonce'))
    except:
     self.tempsannonce=0
    if self.tempsannonce<=0: 
      xbmc.executebuiltin('SetProperty(IconmixBAAuto,"OK",10000)')
    else:
      xbmc.executebuiltin("ClearProperty(IconmixBAAuto,home)")
    self.annoncefull=self.ADDON.getSetting('annoncefull')
    self.allocinefirst=self.ADDON.getSetting('allocinefirst')
    self.allocineactif=self.ADDON.getSetting('allocineactif')
    self.youtubeactif=self.ADDON.getSetting('youtubeactif')
    self.annoncefilm=self.ADDON.getSetting('annoncefilm')
    self.annonceserie=self.ADDON.getSetting('annonceserie')
    self.noterfilm=self.ADDON.getSetting('noterfilm')
    self.noterserie=self.ADDON.getSetting('noterserie')
    self.annoncetoutes=self.ADDON.getSetting('annoncetoutes')
    xbmc.executebuiltin("SetProperty(AutoCompletionProvider,%s,home)" %xbmc.getInfoLabel("Skin.String(AutoCompleteProvider)"))
  
  #------------------------------------------------------------------------------------------------------------------
  def onScanFinished(self,library=None):
    self.ScanFinished=True
    
  
  #------------------------------------------------------------------------------------------------------------------
  def onCleanFinished(self,library=None):
    self.ScanFinished=True
  
  #------------------------------------------------------------------------------------------------------------------
  def onSettingsChanged(self):
    self.updatesetting()
  

#--------------------------------------------------------------------------------------------------
   
class Player(xbmc.Player):

  #------------------------------------------------------------------------------------------------------------------
  def play(self, item='', listitem=None, windowed=False, sublist=None,VolumeBA=None):
      self.Volume=VolumeBA
      super(Player, self).play(item, listitem, windowed)  
   

  #------------------------------------------------------------------------------------------------------------------
  def __init__(self):
      self.windowhome = xbmcgui.Window(10000)
      self.windowvideo = xbmcgui.Window(10025)
      self.DureeTotale=None
      self.Volume=None
      self.PositionLecture=0
      self.ItemID=None      
      self.ItemType=None
      self.noterfilm=None
      self.noterserie=None
      self.currentepisode=None
      xbmc.Player.__init__(self,0)

  #------------------------------------------------------------------------------------------------------------------
  def onPlayBackStarted(self):   
      self.PreviousprogressPosition=None   
      self.PreviousprogressWindow=None
      logMsg("Volume avant Lecture=%s" %utils.GetVolume())
      if self.Volume:
           xbmc.executebuiltin("SetVolume(%d,true)" %self.Volume)
      
      try:
        self.DureeTotale = int(self.getTotalTime())
      except:
        self.DureeTotale=None
      try:
        self.checkProgressPlay()
      except:
        A=None
          
   
  #------------------------------------------------------------------------------------------------------------------
  def Notation(self):
      Annonce=self.windowhome.getProperty('annonceencours')
      try:
        self.DureeLue=int(self.PositionLecture)
      except:
        self.DureeLue=0
      if self.DureeTotale and self.DureeLue:
          if ((self.DureeTotale-20)<=self.DureeLue):
            if (self.ItemType=="Movie" and self.noterfilm=="false") or (self.ItemType=="Episode" and self.noterserie=="false") :
              self.ItemID=None
            if Annonce!="":
              xbmc.PlayList().clear()  
            if self.ItemID:
               self.ui = dialog_Notation('notation.xml', ADDON_PATH, 'default','1080i',dbid=self.ItemID,TypeVideo=self.ItemType)
               ret=self.ui.doModal()
               del self.ui 
      self.windowhome.clearProperty('annonceencours')
      self.windowhome.clearProperty('IconMixTrailer')
      self.PositionLecture=0
      self.ItemID=None
      self.ItemNotation=None
      self.ItemType=None       

  #------------------------------------------------------------------------------------------------------------------
  def onPlayBackStopped(self):
      self.PreviousprogressPosition=None
      self.PreviousprogressWindow=None
      logMsg("Volume apres Lecture=%s" %utils.GetVolume())
      if self.Volume:
           xbmc.executebuiltin("SetVolume(100)")
      logMsg("Volume apres retablissement=%s" %utils.GetVolume())
      self.Notation()
      
      

  #------------------------------------------------------------------------------------------------------------------
  def onPlayBackEnded(self):
      self.PreviousprogressPosition=None
      self.PreviousprogressWindow=None
      self.Notation()
      
  #------------------------------------------------------------------------------------------------------------------
  def onPlayBackSeekChapter(self):
      try:
        self.checkProgressPlay()
      except:
        A=None

#--------------------------------------------------------------------------------------------------
      
class dialog_ShowInfo(xbmcgui.WindowXMLDialog):
    #------------------------------------------------------------------------------------------------------------------
  def __init__(self, *args, **kwargs):
        self.retourpath=None
        self.dontshow=True
        self.windowhome = xbmcgui.Window(10000)
        xbmcgui.WindowXMLDialog.__init__(self)
        self.listitem = kwargs.get('listitem')
        self.acteurs = kwargs.get('acteurs')
        self.mainservice = kwargs.get('mainservice')
        self.dbid=kwargs.get('dbid')
        self.dbtype=kwargs.get('dbtype')
        self.Genre5001=None
        
        self.IconmixShowInfo=self.windowhome.getProperty('IconmixShowInfo')
        

    #------------------------------------------------------------------------------------------------------------------
  def onInit(self):
        self.Ajour=None
        self.Local=None
        
        self.img_list = self.getControl(1990)
        if self.img_list:
          self.img_list.reset()
         
          self.img_list.addItem(self.listitem)
          image=self.listitem.getProperty("Poster")
          if not image:
            image=self.listitem.getArt("poster")
          if not image:
            image=self.listitem.getArt("thumb")
          if not image:
            image=self.listitem.getArt("icon")
          if not image: 
            image="DefaultThumb.png"
          self.getControl(2000).setImage(image, False)  
          
          extrafanart=xbmcgui.Window(10000).getProperty('IconMixExtraFanart')
          if not extrafanart:
            extrafanart=self.listitem.getArt("fanart")
            if not extrafanart:
              extrafanart=self.listitem.getArt("tvshow.fanart")
            if extrafanart:
              xbmcgui.Window(10000).setProperty('IconMixExtraFanart',extrafanart)
          self.ListeActeurs=self.getControl(1998)
          if self.acteurs and self.ListeActeurs:
            self.ListeActeurs.reset()
            
            for item in self.acteurs:
              self.ListeActeurs.addItem(item)
          pays.ConversionPays(None,1990)    
          genrecontrol=self.getControl(5001)
          if genrecontrol:
            Liste=utils.getGenreListe2(self.listitem.getVideoInfoTag().getGenre())
            #Liste=None
            #logMsg("GENRES : %s" %self.listitem.getVideoInfoTag().getGenre())
            if Liste:                     
              genrecontrol.addItems(Liste) 
        else:
          self.close()

    #------------------------------------------------------------------------------------------------------------------
  def onAction(self, action):
      # Action : 3 haut
      # Action : 4 bas
      # Action : 2 droite
      # Action : 1 gauche  
      # 11 touche "info" 
      # 163 : "m"
      # 117 : "c"
     
      if action.getId()==11 or action in ACTION_PREVIOUS_MENU:         
          self.close()
      else:
        if action in (1,2,4) or not self.Ajour:
          F8889=xbmc.getCondVisibility("Control.HasFocus(8889)")
          F7781=xbmc.getCondVisibility("Control.HasFocus(7781)") if self.Ajour else 1 #<!-- controle acteurs -->
          F7779=xbmc.getCondVisibility("Control.HasFocus(7779)") #acteurs <!-- controle roles -->
          F7778=xbmc.getCondVisibility("Control.HasFocus(7778)") #directors
          F7777=xbmc.getCondVisibility("Control.HasFocus(7777)") or F7778
          if F8889 | F7781 | F7779 |F7777:
                  self.CompteurTemps=0
                  KodiLocal=self.windowhome.getProperty('ActeurVideoLocal')
                  if (action.getId()==4 and (F7779 or F7778) and self.Local!=KodiLocal) or (action in (1,2) and F7781) or not self.Ajour:
                     self.mainservice.CheckActeursRoles(F8889, F7781, F7779,F7777,1)
                     self.Ajour=True                      
                     self.Local=KodiLocal
 
    #------------------------------------------------------------------------------------------------------------------
  def onClick(self, controlID):
        if controlID == 6 or controlID == 3:             
            Trailer=None
        if controlID==600:
          self.close()
        if controlID==8: #play
          Path=self.listitem.getPath()
          if len(Path)>3: 
             self.close()
             xbmc.executebuiltin("Dialog.Close(all,True])")
             xbmc.Player().play(Path)
        if controlID==7777:
          self.mainservice.CheckActeursRoles(False, False, False,True,1)
          self.Local=self.windowhome.getProperty('ActeurVideoLocal')
        if controlID==500:
          self.dontshow=None          
          self.close()
        if controlID==5001:
          self.Genre5001=xbmc.getInfoLabel("Container(5001).ListItem.Label2")          
          self.dontshow=None          
          self.close()           
        if controlID==1000 or controlID==1001 :
          mtitle=xbmc.getInfoLabel("Container(1990).ListItem.Title")
          dbtype=xbmc.getInfoLabel("Container(1990).ListItem.DBTYPE")
          label=xbmc.getInfoLabel("Container(1990).ListItem.Label")
          year=xbmc.getInfoLabel("Container(1990).ListItem.Year")
          dbid=xbmc.getInfoLabel("Container(1990).ListItem.DBID")
          imdbnumber=xbmc.getInfoLabel("Container(1990).ListItem.Property(IMDBNumber)")
          tmdbnumber=xbmc.getInfoLabel("Container(1990).ListItem.Property(TMDBNumber)")
          Commande='label:%s*dbtype:%s*label:%s*year:%s*dbid:%s*imdbnumber:%s*tmdbnumber:%s' %(mtitle,dbtype,label,year,dbid,imdbnumber,tmdbnumber)
          self.mainservice.GetTrailer(Commande)         
            
        
                

    #------------------------------------------------------------------------------------------------------------------
  def onFocus(self, controlID):
        pass

#--------------------------------------------------------------------------------------------------
        
class dialog_ShowGuide(xbmcgui.WindowXMLDialog):
    #------------------------------------------------------------------------------------------------------------------
  def __init__(self, *args, **kwargs):
        self.windowhome = xbmcgui.Window(10000)
        xbmcgui.WindowXMLDialog.__init__(self)
        self.calendrier = None #kwargs.get('Calendrier')
       
        self.GlobalCalendrier=kwargs.get('GlobalCalendrier')
        self.retour=None
        self.IdEncours=None
        self.ShowBetaSerieInfo=False
        self.CalendrierMode=1
        self.NoAction=None
        self.NoActionP=None
        #1 : series KODI
        #0 : toutes
        #2 : a venir
              

    #------------------------------------------------------------------------------------------------------------------
  def onInit(self):    
        self.List=[]
        self.Container=[]
        self.IndexContainer=0
        self.debut=1
        self.Position=None
        self.RetourUpdate=None
        try:
          self.InfoCtrl=self.getControl(1881)
          self.InfoCtrl.setVisible(False)
        except:
          self.InfoCtrl=None
        
        cpt=1780
        while (cpt<1794):          
         self.List.append(self.getControl(cpt))
         cpt=cpt+1
        self.BACtrl=self.getControl(1670)
        
        self.Focus=None
        
        
        self.ChangeCalendrier()        
        self.windowhome.setProperty("IconmixGuideShowBetaSerieSemaine","%s" %self.debut)
        
        
        
          
    #------------------------------------------------------------------------------------------------------------------
  def SetHeader(self):
        id0=self.CalendrierMode-1
        if id0<0:
          id0=2
        id2=self.CalendrierMode+1
        if id2>2:
          id2=0    
      
        Header=self.getControl(1878)          
        Header.setLabel(__language__(32867+id0)) 
        Header=self.getControl(1883)          
        Header.setLabel(__language__(32867+self.CalendrierMode))
        Header.setEnabled(False)
        Header=self.getControl(1879)          
        Header.setLabel(__language__(32867+id2))
    #fenetre principale   
    #1990 à 1996 : les 7 containers des épisodes affichés
    #1878/1879 : si focus 1879, on passe à la 2ème page etc.... 
    #1883 : mode actuel
    #1800 à 1806 : Dates entêtes affichées
    #1897 : Synopis de l'épisode
    #1895 : Fanart de fond d'écran
    #1896 : Poster de la série
    #1894 : Banniere de la serie
    
    #boite info
    #1888 : Nb saisons/episodes
    #1887 : Histoire de la série
    #1889 : Titre de la série
    #1882 : Nom du studio
    #1885 : Image du studio
    #1886 : Poster de la série
    #1884 : Image logo Kodi si dans Kodi
    
    
        
          
    #------------------------------------------------------------------------------------------------------------------
  def onClick(self, controlID):
      TvDbId=None
      if controlID>=1780 and controlID<=1793 :
        if self.ShowBetaSerieInfo==True:
          KodiId=None
          if self.CalendrierMode==1:
            KodiId=xbmc.getInfoLabel("Container(%d).ListItem.DBID" %controlID)
          else:
            TvDbId=xbmc.getInfoLabel("Container(%d).ListItem.Property(tvdbid)" %controlID)
            if self.GlobalCalendrier[0].get(TvDbId):
              try:
               KodiId=self.GlobalCalendrier[0][TvDbId].get("KodiId")
              except:
               KodiId=None
          if KodiId:    
            self.retour=KodiId              
            self.windowhome.clearProperty("IconmixGuideShowBetaSerieInfo")
            self.close()
          else:
            if TvDbId:
              self.GetTrailer(TvDbId,xbmc.getInfoLabel("Container(%d).ListItem.Title" %controlID),self.AnneeActuelle)
        else:
         if self.RetourUpdate: 
           self.ShowBetaSerieInfo=True
           self.windowhome.setProperty("IconmixGuideShowBetaSerieInfo","show") 
      
      #bascule entre calendriers
      if controlID==1878 or controlID==1879:
        if controlID==1878:
          self.CalendrierMode=self.CalendrierMode-1
          if self.CalendrierMode<0:
            self.CalendrierMode=2
        if controlID==1879:
          self.CalendrierMode=self.CalendrierMode+1
          if self.CalendrierMode>2:
            self.CalendrierMode=0
        self.ChangeCalendrier()
        
      
    #------------------------------------------------------------------------------------------------------------------
  def ChangeCalendrier(self):
      if self.CalendrierMode==1:
        self.calendrier=utils.Diffusion2Semaines(self.GlobalCalendrier)
      if self.CalendrierMode==0:
        #self.calendrier=utils.GetCalendrierSemaine()
        self.calendrier=utils.GetCalendrier2SemaineTvMaze()
      if self.CalendrierMode==2:
        #self.calendrier=utils.GetCalendrierSemaine(True)
        self.calendrier=utils.GetCalendrier2SemaineTvMaze(None,True)
      
      #xbmc.sleep(400)
      self.UpdateContainer()
           
      
      self.SetHeader()
      if self.IndexContainer>=0:        
        self.setFocusId(self.Container[self.IndexContainer])
      else:
        self.setFocusId(1878)      
    
    #------------------------------------------------------------------------------------------------------------------
  def GetTrailer(self,tvdbid=None,Titre=None,Annee=None):
      self.unique={"tvdb":tvdbid}
      xbmc.executebuiltin( "ActivateWindow(busydialog)" )
      TMDBNUMBER=utils.get_TMDBID(DbType="tvshow",KodiId=None,UniqueId=self.unique)
      self.ListeTrailer=utils.getTrailer(TMDBNUMBER,"tvshow",None)
      AllocineBA=utils.Allocine_BandeAnnonce(Titre.lower(),"tvshow",None,None,Annee)
      if AllocineBA:
            if not self.ListeTrailer:
              self.ListeTrailer=[]
            cpt=len(AllocineBA)-1
            while cpt>=0:                
                self.ListeTrailer.insert(0,AllocineBA[cpt])
                cpt=cpt-1
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
                
                self.ui = dialog_select_UI('choix.xml', ADDON_PATH, 'default','1080i',listing=ListeNomTrailer,trailers=self.ListeTrailer,ItemId=xbmc.getInfoLabel("ListItem.DBID"),Window=True)
                self.windowhome.setProperty("IconMixTrailer","1")
                ret=self.ui.doModal()
                del self.ui                          
                self.windowhome.clearProperty('IconMixTrailer')
                  
                      
      else: 
          dialog=xbmcgui.Dialog()
          dialog.notification('IconMixTools', Titre+": "+__language__( 32506 ), "acteurs/arfffff.png", 500)
         
    #------------------------------------------------------------------------------------------------------------------
  def UpdateContainer(self):
      indexcontainer=0
      cpt=0
      self.IndexContainer=-1
      self.Container=[]
      TvDbInit=None
      self.NoActionP=None
      
      for DateItem in self.calendrier:
          if indexcontainer<14:
            self.List[indexcontainer].reset()
            if len(DateItem)>0:
              self.Container.append(1780+indexcontainer)
              if self.IndexContainer<0:
                  self.IndexContainer=0
                
              ListeNextEpisodes=[]
              for Item in DateItem:
                  #code : S01E02
                  #title : titre de l'episode
                  #TitreSerie : titre de la serie
                 Code=Item.get("next").get("code")
                 Elements = xbmcgui.ListItem(label=Item.get("next").get("title"), label2=Code)
                 Elements.setArt({"poster":Item.get("poster"),"banner":Item.get("banner"),"fanart":Item.get("fanart"),"clearart":Item.get("clearart")})
                 Elements.setProperty("TitreSerie",Item.get("TitreSerie"))
                 TvDbId=Item.get("tvdbid")
                 
                 KodiId=None
                 
                 #NetWork="resource://resource.images.studios.white"+str(Item.get("next").get("network")).lower()+".png"
                 NetWork="resource://resource.images.studios.white/"+str(Item.get("next").get("network")).lower()+".png"
                 #NetWork=str(Item.get("next").get("network"))+".png"
                 #NetWork="resource://resource.images.studios.white/nbc.png"
                 if self.CalendrierMode!=1 and self.GlobalCalendrier[0].get(str(Item.get("tvdbid"))):
                       NetWork="acteurs/local.png"
                       KodiId=self.GlobalCalendrier[0].get(str(Item.get("tvdbid"))).get("KodiId")
                       logMsg("Network kodi (%s)(%s)" %(TvDbId,KodiId))
                 Elements.setProperty("Network",NetWork)
                 Elements.setInfo("video", {"dbid": str(Item.get("KodiId")),"mediatype": "tvshow","title": Item.get("TitreSerie"),"plot":Item.get("next").get("description")})
                 Elements.setProperty("KodiId",str(KodiId))
                 Elements.setProperty("tvdbid",str(Item.get("tvdbid")))
                 Elements.setProperty("plot",Item.get("next").get("description"))
                 try:
                  
                   Saison=int(Code.split("E")[0].replace("S",""))
                   Episode=int(Code.split("E")[1].replace("E",""))
                   NbEpisodes=int(Item.get("Saisons").get(str(Saison)))
                   logMsg("Saison (%s) Episode (%s) NbEpisodes (%s)" %(Saison,Episode,NbEpisodes))
                   if Episode==NbEpisodes:
                      Elements.setProperty('IsFinal',"   >>"+__skin_string__(31795))
                   
                 except:
                   Saison=None
                   Episode=None
                 
                 
                 ListeNextEpisodes.append(Elements)
                 if TvDbId and not TvDbInit:
                   TvDbInit=TvDbId
                  
              self.List[indexcontainer].addItems(ListeNextEpisodes)
                 
              indexcontainer=indexcontainer+1
            else:
              indexcontainer=indexcontainer+1
          cpt=cpt+1
      if TvDbInit:
         self.UpdateInfoBetaSerie(TvDbInit)
       
      loc = locale.getlocale(locale.LC_ALL)
      locale.setlocale(locale.LC_ALL, xbmc.getLanguage(xbmc.ISO_639_1))
      for i in range(1800,1814): 
        Date=(datetime.today() + timedelta(i-1800)).strftime("%A %d/%m/%Y") 
        if i==1800:
          Date=__skin_string__(33006)+'[CR][COLOR=yellow][I]'+Date+'[/I][/COLOR]'          
        self.getControl(i).setLabel(Date)
      
      try:  
        locale.setlocale(locale.LC_ALL, loc)
      except:
        i=0
     
    #------------------------------------------------------------------------------------------------------------------
  def UpdatePlot(self):
          
           Space="                                                            "
           self.IdEncours=self.Container[self.IndexContainer]               
           if self.IdEncours and (self.IdEncours>=1780 and self.IdEncours<=1793):
             ContainerCtrl=self.getControl(self.IdEncours)    
             ItemSelect=ContainerCtrl.getSelectedItem()
             PlotLabel=self.getControl(1897)
             PlotLabel.setLabel("")
             Description=ItemSelect.getProperty('plot')
             logMsg("description (%s)" %Description)
              
             
             if len(Description)>1:
               if len(Description)>130:
                Description=Space+Description
               PlotLabel.setLabel(Description.replace("\n"," ").replace("<p>","").replace("</p>",""))
             
             TitreEpisodeCtrl=self.getControl(1898)
             TitreEpisodeCtrl.setLabel("[COLOR=yellow]"+xbmc.getInfoLabel("Container(%s).ListItem.Title" %(self.IdEncours))+" [/COLOR] ("+xbmc.getInfoLabel("Container(%s).ListItem.Label2" %(self.IdEncours))+") : [COLOR=FFFFD966]"+xbmc.getInfoLabel("Container(%s).ListItem.Label" %(self.IdEncours))+"[/COLOR]")
            
                 
    #------------------------------------------------------------------------------------------------------------------
  def WaitScroll(self):
      cpt=0
      self.NoActionP=True
      self.NoAction=None
      while cpt<3 and not self.NoAction:
        xbmc.sleep(300)
        cpt=cpt+1
       
      if not self.NoAction:
          self.RetourUpdate=self.UpdateInfoBetaSerie()
      self.NoActionP=None  
      
           
           
           
    #------------------------------------------------------------------------------------------------------------------
  def UpdateInfoBetaSerie(self,MyTvDbId=None):
         Retour=None
         zz=None
         Banner=""
         Poster=""
         Fanart=None
         self.IdEncours=self.Container[self.IndexContainer] 
         ContainerCtrl=self.getControl(self.IdEncours)    
         ItemSelect=ContainerCtrl.getSelectedItem()          
         if not self.Position:
          self.Position=0
         if self.IdEncours and (self.IdEncours>=1780 and self.IdEncours<=1793):
           Fanart=xbmc.getInfoLabel("Container(%s).ListItem.Art(fanart)" %(self.IdEncours))
           Poster=xbmc.getInfoLabel("Container(%s).ListItem.Art(poster)" %(self.IdEncours))
           Code=xbmc.getInfoLabel("Container(%s).ListItem.Label2" %(self.IdEncours))
           FinalCtrl=self.getControl(1890)
           FinalCtrl.setVisible(False)
           try:
             Saison=int(Code.split("E")[0].replace("S",""))
             Episode=int(Code.split("E")[1].replace("E",""))
           except:
              Saison=None
              Episode=None
           
           if MyTvDbId:
             TvDbId=MyTvDbId
           else: 
             TvDbId=ItemSelect.getProperty('tvdbid')
           KodiCtrl=self.getControl(1884)
           try:
              zz=int(ItemSelect.getProperty('KodiId'))
              KodiCtrl.setImage("acteurs/local.png")
           except:
              KodiCtrl.setImage("") 
           Network=ItemSelect.getProperty("network")             
           if zz or self.CalendrierMode==1 :
             self.BACtrl.setLabel(__language__(32870))
           else:   
             self.BACtrl.setLabel(__language__(32508))

           if TvDbId :    
             
                 if MyTvDbId:
                    TvDbId=MyTvDbId
                 else: 
                    ContainerCtrl=self.getControl(self.IdEncours)    
                    ItemSelect=ContainerCtrl.getSelectedItem()
                    TvDbId=ItemSelect.getProperty('tvdbid')
                    
                 try:
                  TvDbId=int(TvDbId)
                 except:
                  TvDbId=None
                 if TvDbId and TvDbId!=None:
                   query_url = "https://api.betaseries.com/shows/display?key=46be59b5b866&thetvdb_id=%s" % (TvDbId) 
                   json_data = utils.requestUrlJson(query_url)
                   if json_data:
                       DetailsSerie=json_data.get("show")
                       if DetailsSerie:
                           Titre=DetailsSerie.get("title")
                           if not Network:
                             Network=DetailsSerie.get("network")                 
                           Status=DetailsSerie.get("status")
                           NbSaisons=DetailsSerie.get("seasons")
                           NbEpisodes=DetailsSerie.get("episodes")
                           SeasonDetails=DetailsSerie.get("seasons_details")
                           for saisonN in SeasonDetails:
                             if int(saisonN.get("number"))==Saison:
                              if int(saisonN.get("episodes"))==Episode:
                                FinalCtrl.setVisible(True)
                                break
                           
                            
                           
                           
                           Annee=DetailsSerie.get("creation")
                           self.AnneeActuelle=Annee
                           Description=DetailsSerie.get("description")
                           Images=DetailsSerie.get("images")
                           if Images:
                              if not Poster or Poster=="":                                
                                Poster=Images.get("poster")
                              Banner=Images.get("banner")
                              if not Fanart or Fanart=="":
                                logMsg("Fanart (%s) (%s)" %(Fanart,Images.get("show")))
                                Fanart=Images.get("show")
                         
                           Retour=True
                   else:
                    UniqueId={"tvdb":str(TvDbId)}
                    TMDBID=utils.get_TMDBID("tvshow",None,UniqueId)
                    if TMDBID:
                      query_url = "%stv/%s?api_key=67158e2af1624020e34fd893c881b019&language=en" % (utils.BaseUrlTMDB,TMDBID)
                      json_data = utils.requestUrlJson(query_url)
                      if json_data:
                        Annee=json_data.get("first_air_date").split("-")[0]
                        Titre=json_data.get("name")
                        NbEpisodes=json_data.get("number_of_episodes")
                        NbSaisons=json_data.get("number_of_seasons")
                        try:
                          NetWork=json_data.get("networks")[0].get("name")
                        except:
                          NetWork=""
                        Description=json_data.get("overview")
                        Fanart=json_data.get("backdrop_path")
                        Poster=json_data.get("poster_path")
                        if Fanart:
                           Fanart="http://image.tmdb.org/t/p/original"+Fanart
                        if Poster:
                          Poster="http://image.tmdb.org/t/p/original"+Poster
                        Retour=True  
                          
                        
                    
                   if Retour==True:
                           NbEpSaCtrl=self.getControl(1888) 
                           NbEpSaCtrl.setLabel("%s %s / %s %s / %s: %s" %(NbSaisons,__skin_string__(36905),NbEpisodes,__skin_string__(36907),__skin_string__(20416),Annee))   
                           
                           PlotLabel=self.getControl(1887)
                           if not Description:
                            Description=""
                           PlotLabel.setText(Description.replace("\n"," ")) 
                           TitreCtrl=self.getControl(1889)
                           TitreCtrl.setLabel(Titre)                          
                           TNetworkCtrl=self.getControl(1882)
                           NetWorkCtrl=self.getControl(1885) 
                           if not xbmcvfs.exists(Network) and not xbmcvfs.exists("resource://resource.images.studios.white%s.png" %Network):
                            NetWorkCtrl.setImage("")
                            TNetworkCtrl.setLabel(Network)
                           else:
                            TNetworkCtrl.setLabel("")
                            try:
                               if "resource:" in Network:
                                 NetWorkCtrl.setImage(Network)
                               else:
                                 NetWorkCtrl.setImage("resource://resource.images.studios.white%s.png" %Network)
                            except:
                              NetWorkCtrl.setImage("") 
                   
             
           PosterCtrl=self.getControl(1886)
           if not Poster:
              Poster="DefaultTVShows.png"
           PosterCtrl.setImage(Poster)
           FanartCtrl=self.getControl(1895)
           if not Fanart:
            Fanart=""
           FanartCtrl.setImage(Fanart)
           logMsg("--->(%s),(%s),(%s)" %(Banner,Fanart,Poster)) 
         else:
           logMsg("(%s) self.IdEncours and (self.IdEncours>=1780 and self.IdEncours<=1793)" %self.IdEncours)
         self.RetourUpdate=Retour
        
         if self.RetourUpdate:
          self.InfoCtrl.setVisible(True)
         else:
          self.InfoCtrl.setVisible(False)
        
         return Retour  
           

    #------------------------------------------------------------------------------------------------------------------
  def onAction(self, action):
      # 3 haut
      # 4 bas
      # 2 droite
      # 1 gauche  
      # 5 PagePrec
      # 6 PageSuiv
      # 11 touche "info" 
      # 163 : "m"
      # 117 : "c"
      #159 Home
      #160 End
      
     
      if action in ACTION_PREVIOUS_MENU: 
        if self.ShowBetaSerieInfo==False:
          self.windowhome.clearProperty("IconmixGuideShowBetaSerieInfo")
          self.close()
        else:
          self.ShowBetaSerieInfo=False
          self.windowhome.clearProperty("IconmixGuideShowBetaSerieInfo")
      else:
        CodeAction=action.getId()
        logMsg("actionid perm (%s)" %CodeAction)
        try:
          currentfocus=int(xbmc.getInfoLabel("System.CurrentControlID"))
        except:
          currentfocus=0
        if (currentfocus>=1780 and currentfocus<=1793):
        
          if CodeAction in (1,2,3,4,5,6,159,160):
            self.NoAction=None
           
            self.IdEncours=self.Container[self.IndexContainer]               
            if self.IdEncours and (self.IdEncours>=1780 and self.IdEncours<=1793):
              self.Position=int(xbmc.getInfoLabel("Container(%s).Position" %self.IdEncours))
              if CodeAction==2: #droite
                self.IndexContainer=self.IndexContainer+1
                if self.IndexContainer>=len(self.Container):
                  self.IndexContainer=0            
                
                #ContainerCtrl=self.getControl()
                xbmc.executebuiltin("Control.SetFocus(%s,%s)" %(self.Container[self.IndexContainer],self.Position))
                #xbmc.sleep(500)
                  
              if CodeAction==1: #gauche
                self.IndexContainer=self.IndexContainer-1
                if self.IndexContainer<0:
                  self.IndexContainer=len(self.Container)-1            
                
                xbmc.executebuiltin("Control.SetFocus(%s,%s)" %(self.Container[self.IndexContainer],self.Position))
                        
              #logMsg("Action (%s)" %action.getId())           
              
              

              self.UpdatePlot()
              if not self.NoActionP:
                 self.NoAction=True
                 self.WaitScroll()
                 self.NoAction=None
          else:
            logMsg("actionid (%s)" %CodeAction)    
              
          if CodeAction==11: # and self.RetourUpdate:
            #info betaserie
            if self.ShowBetaSerieInfo!=True:
              self.RetourUpdate=self.UpdateInfoBetaSerie()                         
              if self.RetourUpdate==True:
                self.ShowBetaSerieInfo=True
                self.windowhome.setProperty("IconmixGuideShowBetaSerieInfo","show")
              else:
                #dialog=xbmcgui.Dialog()
                #dialog.notification('IconMixTools', __language__( 32584 ), "acteurs/arfffff.png", 1500)                               
                self.ShowBetaSerieInfo=False
                self.windowhome.clearProperty("IconmixGuideShowBetaSerieInfo")
            else:
              self.ShowBetaSerieInfo=False
              self.windowhome.clearProperty("IconmixGuideShowBetaSerieInfo")
        if currentfocus==1878 or currentfocus==1879  :
          if CodeAction==2 or CodeAction==1:
            if currentfocus==1878:
              self.setFocusId(1879)
            else:
              self.setFocusId(1878)
   
   
    #------------------------------------------------------------------------------------------------------------------
  def onFocus(self, controlID):
        self.Focus=controlID       
        
        if controlID>=1780 and controlID<=1793:
          if controlID>=1780 and controlID<=1786:
              self.windowhome.setProperty("IconmixGuideShowBetaSerieSemaine","1" )
              #self.UpdateContainer(self.debut)
              
          
          if controlID>=1787 and controlID<=1793:
              self.windowhome.setProperty("IconmixGuideShowBetaSerieSemaine","2" )
              #self.UpdateContainer(self.debut) 
          logMsg("OnFocus %s" %controlID)
          #self.UpdateInfoBetaSerie()     
          self.UpdatePlot()
          if not self.NoActionP:
                 self.WaitScroll()
        
          
       
        
#--------------------------------------------------------------------------------------------------            
          
class dialog_select_UI(xbmcgui.WindowXMLDialog):
    #------------------------------------------------------------------------------------------------------------------
  def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)
        self.listing = kwargs.get('listing')
        self.ListeTrailer = kwargs.get('trailers')
        self.ItemId = kwargs.get('ItemId')
        self.kodi_player = Player()
        self.BAF=kwargs.get('Window')

    #------------------------------------------------------------------------------------------------------------------
  def onInit(self):
        self.img_list = self.getControl(6)            

        if self.img_list:
          for item in self.listing:           
              self.img_list.addItem(item)
          self.setFocus(self.img_list)
          if not self.BAF:
            self.BAF=0
            if xbmc.getCondVisibility("Skin.HasSetting(BAfenetre)"):
              self.BAF=1
          else:
            self.BAF=1
        else:
          self.close()

    #------------------------------------------------------------------------------------------------------------------
  def onAction(self, action):
      # Action : 3 haut
      # Action : 4 bas
      # Action : 2 droite
      # Action : 1 gauche  
      # 11 touche "info"      
      if action in ACTION_PREVIOUS_MENU:
          if self.kodi_player and self.kodi_player.isPlaying():
             self.kodi_player.stop()
             xbmc.executebuiltin("SetProperty(annonceencours,,home)")
          self.close()
      

    #------------------------------------------------------------------------------------------------------------------
  def onClick(self, controlID):
        if controlID == 6 or controlID == 3: 
            ret = self.img_list.getSelectedPosition()
            titre=self.img_list.getSelectedItem().getLabel()
            self.Titre = self.getControl(8)
            Trailer=None
            if self.Titre:
              self.Titre.setLabel(titre)
            self.Windowed=True
            try:
              Trailer=self.ListeTrailer[ret]["id"]
              
              if "cineserie" in Trailer:
                #logMsg("Traduction de lien %s" %Trailer)
                Trailer=utils.BACineSeriesGetVideo(Trailer,self.ListeTrailer[ret].get("size"))
              
              if "youtube" in Trailer:
                idyoutube=Trailer.split('video_id=')[1]
                if idyoutube:
                  urlyoutube=youturl.getyoutubeurl(idyoutube)
                  Trailer=urlyoutube
              
            except:
              Trailer=None
                 
            if xbmc.getCondVisibility("Player.HasMedia"):
                dialogC = xbmcgui.Dialog()
                retx= dialogC.yesno("ICONMIXTOOLS !!!", __language__( 32615 )," ", __language__( 32613 )) #-- Show a dialog 'YES/NO'.
                if retx<=0:                  
                  Trailer=None
            if self.kodi_player and Trailer:
                self.previousitem=""
                self.previousLABEL1999 = ""
                self.previousitemPlayer=""
                if self.BAF==0: 
                  xbmc.executebuiltin('Dialog.Close(all,true)')
                  xbmcgui.Window(10000).setProperty('annonceencours','full')
                  self.Windowed=False
                else:
                  xbmcgui.Window(10000).setProperty('annonceencours','window')
                xbmc.executebuiltin("SetProperty(BAprecedenteInf,%s,home)" %(self.ItemId))
                Elements = xbmcgui.ListItem(label=titre, iconImage=self.img_list.getSelectedItem().getProperty("Icon"))
                Elements.setInfo("video", {"title": titre,"mediatype": "movie"})
                Elements.setArt({"poster":self.img_list.getSelectedItem().getProperty("Icon")})
                self.kodi_player.play(Trailer,listitem=Elements,windowed=self.Windowed,VolumeBA=100)
                

    #------------------------------------------------------------------------------------------------------------------
  def onFocus(self, controlID):
        pass
 
#-------------------------------------------------------------------------------------------------- 
        
class dialog_Notation(xbmcgui.WindowXMLDialog):
    #------------------------------------------------------------------------------------------------------------------
  def __init__(self, *args, **kwargs):
        self.DBID = kwargs.get('dbid')
        self.ItemNotation = None
        self.ItemType=kwargs.get('TypeVideo')
        xbmcgui.WindowXMLDialog.__init__(self)
        
        
    #------------------------------------------------------------------------------------------------------------------
  def onInit(self):
       
        self.img_list = self.getControl(6)            
        if self.img_list:
          Compteur=1
          Elements = xbmcgui.ListItem(label="-")            
          self.img_list.addItem(Elements)
          while Compteur<11:
            Elements = xbmcgui.ListItem(label=str(Compteur))            
            self.img_list.addItem(Elements)
            Compteur=Compteur+1
          logMsg("NOTATION")
          
          try:
               json_result = utils.getJSON('VideoLibrary.Get%sDetails' %(self.ItemType), '{ "%sid":%s,"properties":["userrating","art"] }' %(self.ItemType.lower(),self.DBID))
          except:
               logMsg("VideoLibrary.Get%sDetails : %s impossible = " %(self.ItemType,self.DBID) ,0 )
               
          if json_result:
             try:
              self.ItemNotation=int(json_result.get("userrating"))
             except:
              self.ItemNotation=0
             try:
              logMsg("IMAGE NOTATION=%s" %json_result.get("art").get("poster"))
              self.getControl(99).setImage(json_result.get("art").get("poster"))
             except:
              self.ItemPoster=None
             
          try:
           self.setFocus(self.img_list)
           self.img_list.selectItem(self.ItemNotation) 
          except:
           self.setFocus(self.img_list) 
          self.Titre = self.getControl(1)
          if self.Titre:
              self.Titre.setLabel(__language__(32707))         
        else:
          self.close()

    #------------------------------------------------------------------------------------------------------------------
  def onAction(self, action):
      # Action : 3 haut
      #Action : 4 bas
      # Action : 2 droite
      # Action : 1 gauche        
      if action in ACTION_PREVIOUS_MENU:         
          self.close()
      #else:  logMsg("Action : %s" %(action.getId()),0)


    #------------------------------------------------------------------------------------------------------------------
  def onClick(self, controlID):
        if controlID == 6: 
            ret = self.img_list.getSelectedPosition()
            if ret>=0:
              try:
               json_result = utils.setJSON('VideoLibrary.Set%sDetails' %(self.ItemType), '{ "%sid":%s,"userrating":%s }' %(self.ItemType.lower(),self.DBID,str(ret)))
              except:
                logMsg("VideoLibrary.Set%sDetails : %s impossible = " %(self.ItemType.lower(),self.DBID) ,0 )            
              #logMsg("Notation : (%s)(%s)(%d)" %(self.DBID,self.ItemType,ret),0)
            self.close()
           

    #------------------------------------------------------------------------------------------------------------------
  def onFocus(self, controlID):
        pass

#--------------------------------------------------------------------------------------------------

class dialog_SelectPosition(xbmcgui.WindowXMLDialog):
    #------------------------------------------------------------------------------------------------------------------
  def __init__(self, *args, **kwargs):
        self.DBID = kwargs.get('dbid')
        xbmcgui.Window(10000).setProperty('iconmixtoolsseekosd','1')
        xbmcgui.WindowXMLDialog.__init__(self)
     
     
    #------------------------------------------------------------------------------------------------------------------
  def SecToHMS(self,Temps=None)   :
      if Temps:
        Temps=int(Temps)
        H=Temps//3600
        Mr=Temps%3600
        
        M=Mr//60
        
        S=Mr%60
        return str(H) if H>9 else '0'+str(H),str(M) if M>9 else '0'+str(M),str(S) if S>9 else '0'+str(S)
      else:
         return None,None,None
    
    #------------------------------------------------------------------------------------------------------------------
  def HMSToSec(self,H=None,M=None,S=None):
      Temps=(int(H)*3600)+(int(M)*60)+int(S)
      return Temps
    
       
    #------------------------------------------------------------------------------------------------------------------
  def onInit(self):
        if not xbmc.getCondVisibility("Player.Paused"):
          xbmc.Player().pause()
        PlayerTime=xbmc.Player().getTime()
        self.PlayerMaxTime=xbmc.Player().getTotalTime()
        H,M,S=self.SecToHMS(self.PlayerMaxTime)
        self.H,self.M,self.S=self.SecToHMS(PlayerTime)
        self.PH,self.PM,self.PS=self.SecToHMS(PlayerTime)
        self.getControl(3000).setLabel(self.H)
        self.getControl(3001).setLabel(self.M)
        self.getControl(3002).setLabel(self.S)
        logMsg("self.PH (%s)" %H)
        if H=="00":
          self.getControl(3000).setVisible(False)
          self.getControl(3300).setWidth(325)

    #------------------------------------------------------------------------------------------------------------------
  def Max60(self,Compteur=None):
      
        if Compteur>59:
          Compteur=Compteur-60
        if Compteur<0:
          Compteur=60-abs(Compteur)
          
          
        if Compteur>9:
          return str(Compteur)
        else:
          return '0'+str(Compteur)  
          
    #------------------------------------------------------------------------------------------------------------------
  def Max24(self,Compteur=None):
      
        if Compteur>23:
          Compteur=Compteur-24
        if Compteur<0:
          Compteur=24-abs(Compteur)
        if Compteur>9:
          return str(Compteur)
        else:
          return '0'+str(Compteur)

    #------------------------------------------------------------------------------------------------------------------
  def onAction(self, action):
      # Action : 3 haut
      #Action : 4 bas
      # Action : 2 droite
      # Action : 1 gauche 
      # ACTION_PAGE_DOWN = 6
      # ACTION_PAGE_UP = 5
      #ACTION_FIRST_PAGE = 159
      #ACTION_LAST_PAGE = 160
      BoutonVal={"3000":self.getControl(3000).getLabel(),"3001":self.getControl(3001).getLabel(),"3002":self.getControl(3002).getLabel()}
      if action in ACTION_PREVIOUS_MENU or not xbmc.Player().isPlayingVideo(): 
          TempsActuel=self.HMSToSec(self.PH,self.PM,self.PS)
          if xbmc.Player().isPlayingVideo():
            xbmc.Player().seekTime(TempsActuel)  
            if xbmc.getCondVisibility("Player.Paused"):
              xbmc.Player().pause()
          xbmcgui.Window(10000).clearProperty('iconmixtoolsseekosd')      
          self.close()
      Bouton=self.getFocusId()
      
      ActionId=action.getId()
      
      
      if ActionId in (3,4,5,6,159,160):
        Avance=0
        if ActionId==3:
          Avance=int(self.getControl(Bouton).getLabel())+1
        if ActionId==4:
          Avance=int(self.getControl(Bouton).getLabel())-1
        if ActionId==5 and Bouton!=3000:
          Avance=int(self.getControl(Bouton).getLabel())+10
        if ActionId==6 and Bouton!=3000:
          Avance=int(self.getControl(Bouton).getLabel())-10
        if Bouton!=3000:
          BoutonVal[str(Bouton)]=self.Max60(Avance)
        else:
          BoutonVal[str(Bouton)]=self.Max24(Avance)
        if ActionId==159:
          BoutonVal={"3000":"00","3001":"00","3002":"00"}
        if ActionId==160:
          H,M,S=self.SecToHMS(self.PlayerMaxTime)
          BoutonVal={"3000":H,"3001":M,"3002":S}
        
        TempsActuel=self.HMSToSec(BoutonVal["3000"],BoutonVal["3001"],BoutonVal["3002"])
        if TempsActuel<=self.PlayerMaxTime:
          
          self.getControl(3000).setLabel(BoutonVal["3000"])
          self.getControl(3001).setLabel(BoutonVal["3001"])
          self.getControl(3002).setLabel(BoutonVal["3002"])
          xbmc.Player().seekTime(TempsActuel)
          
      if ActionId in (1,2):
        if ActionId==2:
          Bouton=Bouton+1
          if Bouton>3002:
            Bouton=3000
        if ActionId==1:
          Bouton=Bouton-1
          if Bouton<3000:
            Bouton=3002
        self.setFocusId(Bouton)
          
        
      
      #logMsg("Bouton (%s) Action : (%s)" %(Bouton,ActionId),0)


    #------------------------------------------------------------------------------------------------------------------
  def onClick(self, controlID):
        TempsActuel=self.HMSToSec(self.H,self.M,self.S)
        if TempsActuel<=self.PlayerMaxTime:
          #logMsg("SEEK (%d)" %(TempsActuel))
          if xbmc.getCondVisibility("Player.Paused"):
             xbmc.Player().pause()
          xbmcgui.Window(10000).clearProperty('iconmixtoolsseekosd')   
          self.close()
           
#--------------------------------------------------------------------------------------------------
        

class dialog_BandeAnnonce(xbmcgui.WindowXMLDialog):
    #------------------------------------------------------------------------------------------------------------------
  def __init__(self, *args, **kwargs):
        self.PlayList = kwargs.get('PlayListItem')
        self.VolumeBA = kwargs.get('VolumeBA')
        
        self.kodi_player = Player()
        xbmcgui.WindowXMLDialog.__init__(self) 
        self.Lecture()         
   
    #------------------------------------------------------------------------------------------------------------------
  def onAction(self, action):
      if action.getId()==2:
        #prochain
        self.kodi_player.playnext()
      else :
        if action.getId()==1:
          #precedent
          self.kodi_player.playprevious()
        else:
          self.kodi_player.stop()  
          xbmcgui.Window(10000).clearProperty('annonceencours')
          xbmcgui.Window(10000).clearProperty('IconMixTrailer')        
          self.close()   
 
    
    #------------------------------------------------------------------------------------------------------------------
  def Lecture(self):       
      if self.kodi_player and self.PlayList:         
        self.kodi_player.play(self.PlayList,VolumeBA=self.VolumeBA, windowed=True, sublist=None)        
      else:
        xbmcgui.Window(10000).clearProperty('annonceencours')
        xbmcgui.Window(10000).clearProperty('IconMixTrailer')
        self.close()
 
#--------------------------------------------------------------------------------------------------        

class MainService:
  
    #------------------------------------------------------------------------------------------------------------------
  def __init__(self):         
      
      self.CompteurTemps=0
      
      TvSe="o"
      TvSh="o"
      
      self._init_vars()
      self._start_time = time.time()
      self.RandomTime=0
      self.Recherche=None
      self.SelectedItemPath=None
      self.AutoCompletionProvider=None
      MonAutoCompletion.InitKodiSearch()
      self.windowhome.setProperty("AutoCompletionProvider",SETTING("autocomplete_provider"))
      self.ListeEpisodes=None
      self.GlobalAnnonces=[]
      self.GlobalAnnoncesThread=[]
      self.HomeMenuItem=None
      self.IdWidgetContainer=None
      self.IdWidgetContainerPos=None
      lGlobalAnnonces=0
      self.AllocineIDPrec=None
      lGlobalAnnoncesThread=0
      self.firstidduration=None
      #utils.GetMissingMovies()
      #logMsg("GlobalGenre %s" %utils.GetTMDBGenres())
       
      if xbmcvfs.exists(ADDON_DATA_PATH+"/series/planningnextV2"):
        os.remove(ADDON_DATA_PATH+"/series/planningnextV2")
        
      
      if self.windowhome:
         cpt=0
         while cpt<50:
            if self.windowhome.getProperty('MonNextAired.Actif')!='oui':
              self.GlobalCalendrier=utils.Charge_Calendrier()
              cpt=50
            else:
              xbmc.sleep(500)
            cpt=cpt+1
      
      utils.GetCalendrier2SemaineTvMaze(None)
      
      logMsg('Version : %s - Chemin : %s - Service en cours..' %(ADDON_VERSION,ADDON_PATH),0)
      
      
      while not self.kodimonitor.abortRequested(): # and xbmc.getCondVisibility("!String.IsEmpty(Window(home).Property(IconMixToolsbackend))"): 
        
          if self.kodimonitor.ScanFinished:
            self.kodimonitor.ScanFinished=None
            self.windowhome.setProperty('IconMixUpdateEpisodes','1')
            self.previousitem=None
            
          self.windowhome.clearProperty("IconMixToolsbackend")
          
          #-------------------------- 
          self.CheckListeVues()
          self.GetTrailer()
                      
          #recherche
          self.AutoRecherche()
          #-------------------------- MUSIQUE EN LECTURE---------------------------------
          self.LectureMusique() 
          #-------------------------- #VUES MUSIQUES ------------------------------------------
          self.DetailsVuesMusique()
          #-------------------------- FILMS/SERIES/ACTEURS --------------------------
          self.ShowIconmixInfo()
          self.ShowIconmixGuide()
          #self.getAllDuration()
          
          if not self.windowhome.getProperty('annonceencours')=="full" and (self.windowhome.getProperty('IconMixTrailer')!="1") and (self.windowhome.getProperty('IconmixShowInfo')=="1" or xbmc.getCondVisibility("Window.IsVisible(10025)") or xbmc.getCondVisibility("Window.IsVisible(12901)") or xbmc.getCondVisibility("Window.IsVisible(10142)") or xbmc.getCondVisibility("Window.IsVisible(12003)")) and not xbmc.getCondVisibility("Container.Scrolling") and not xbmc.getCondVisibility("Window.IsVisible(12000)"):
              
              MiseAjour=""
              TMDBNUMBER=None
              
             
              F8889=xbmc.getCondVisibility("Control.HasFocus(8889)")
              F7781=xbmc.getCondVisibility("Control.HasFocus(7781)")
              F7779=xbmc.getCondVisibility("Control.HasFocus(7779)") or xbmc.getCondVisibility("Control.HasFocus(5051)")
              F7777=xbmc.getCondVisibility("Control.HasFocus(7777)") or xbmc.getCondVisibility("Control.HasFocus(7778)")
             
              #-------------------------- ACTEURS : Roles/Bio---------------------------------
                  
              if F8889 | F7781 | F7779 |F7777:
                self.CompteurTemps=0
                self.CheckActeursRoles(F8889, F7781, F7779,F7777)                                
              #-------------------------- FILMS/SERIES ---------------------------------   
              else:
                  self.previousitem8889 = ""  
                  self.previousitemMusic = ""
                  
                      
                  if xbmc.getCondVisibility("Control.HasFocus(2999)"): #
                      self.CompteurTemps=0
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
                          self.PlayerActiveID=None
                          
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
                      if self.selecteditem:   
                        self.SelectedItemPath=None        
                              
                        #Liste episodes       
                        if (xbmc.getCondVisibility("Control.HasFocus(2666)") or xbmc.getCondVisibility("Control.HasFocus(2998)")) and self.DBTYPE=="tvshow" and not xbmc.getCondVisibility("Skin.HasSetting(DisableTvList)") and not xbmc.getCondVisibility("Skin.HasSetting(DisableFocusTvList)"):
                          try:
                           Prochain=int(self.windowhome.getProperty('IconmixProchainEpisode'))
                          except:
                           Prochain=0
                          
                          if Prochain>0 :                           
                             xbmc.executebuiltin("Action(FirstPage)")
                             xbmc.executebuiltin("Control.Move(2666,%d)"  %(Prochain))
                             self.windowhome.clearProperty('IconmixProchainEpisode')
                           
                                                                      
                        
                        if (self.previousitem != self.selecteditem)  or (self.windowhome.getProperty('IconMixUpdateSagas')=="1") or self.windowhome.getProperty('IconMixUpdateEpisodes')=='1': 
                             #Bande-annonce en cours, on stoppe
                             if self.DBTYPE=="tvshow" or self.DBTYPE=="movie":
                                if self.DBTYPE=="movie":
                                  KodiTitre=xbmc.getInfoLabel("ListItem.Label").lower()
                                else:
                                  KodiTitre=xbmc.getInfoLabel("ListItem.TVShowTitle").lower()
                                Annee=xbmc.getInfoLabel("ListItem.Year")
                                utils.Annonces(self.selecteditem,self.DBTYPE,KodiTitre,Annee,self.GlobalAnnonces,self.GlobalAnnoncesThread,None).start()
                              
                             if self.kodi_player and self.kodi_player.isPlayingVideo() and (self.windowhome.getProperty('annonceencours') or self.AnnonceNetflix):
                                self.AnnonceNetflix=None
                                self.kodi_player.stop()
                                self.windowhome.clearProperty('annonceencours')
                             if self.selecteditem!=self.windowhome.getProperty('BAprecedenteInf'):
                                self.windowhome.clearProperty('BAprecedenteInf')
                             #--------------------------------------
                             self.previousitem = self.selecteditem
                             self.CompteurTemps=0
                             self.PreviousBAnnonce=0
                             MiseAjour="1"
                             
                                                      
                             
                             if xbmc.getCondVisibility("Window.IsVisible(12901)"): #videoplayer <videoosd.xml>
                                MiseAjour="3"                              
                                self.previousitemPlayer = self.selecteditem
                                pays.ConversionPays(True,None)
                                
                             if xbmc.getCondVisibility("Window.IsVisible(10142)") :#videoplayer <DialogFullScreenInfo.xml>
                                MiseAjour="4"
                                pays.ConversionPays(True,None)
                                self.previousitemPlayer = self.selecteditem
                                 
                             if xbmc.getCondVisibility("Window.IsVisible(12003)") :#videoinfo
                                  MiseAjour="2" 
                                  pays.ConversionPays(None,None) 
                               
                             self.windowhome.clearProperty('IconMixUpdateSagas')
                             
                             if self.previousitem != self.selecteditem or self.windowhome.getProperty('IconMixUpdateEpisodes')=='1':                    
                                self.windowhome.clearProperty('IconMixUpdateEpisodes')
                             
                             
                        else:                          
                            
                          #---------------------------- BANDE ANNONCE AUTOMATIQUE-------------------------------------
                         self.BandeAnnonceAutomatique()
                      else:
                        if self.SelectedItemPath!=xbmc.getInfoLabel("ListItem.FolderPath"):
                          self.SelectedItemPath=xbmc.getInfoLabel("ListItem.FolderPath")
                          self.duration = xbmc.getInfoLabel("ListItem.Duration") 
                          self.display_duration(self.selecteditem,self.DBTYPE)         
                              
                          
                                          
                  if not self.selecteditem :
                      self.windowhome.clearProperty('IconMixExtraFanart')
                      utils.ClearNextEpisode()
                      self.precedenttvshow=None
                      self.previousitem=None
                      self.windowhome.clearProperty("ItemCountry1")
                      self.windowhome.clearProperty("ItemCountry2")
                      self.windowhome.clearProperty("ItemCountry3")
                      self.windowhome.clearProperty("ItemCountry4")
                      
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
                      if self.DBTYPE!="tvshow" and self.DBTYPE!="episode" and self.DBTYPE!="season":
                          utils.ClearNextEpisode()
                          self.windowhome.clearProperty('IconMixTvStatus')
                          self.windowhome.clearProperty('IconMixTvNetwork')
                          self.windowhome.clearProperty('IconMixTvCharacter') 
                      
                      #ACTEURS ELEMENT DE SAGA ------------------------------------------------ 
                      if xbmc.getCondVisibility("Control.HasFocus(2999)"):
                          if self.selecteditem > -1 and not str(self.selecteditem)=="":
                            pays.ConversionPays(None,1999)                          
                            if self.DBTYPEOK:
                                  try:
                                     ListeActeurs=self.GetControl(self.windowvideonav,1998)
                                  except:
                                    ListeActeurs=None
                                 
                                                                  
                                  if ListeActeurs:
                                    ListeItemx=utils.getCasting(self.DBTYPE,self.selecteditem,1,TMDBNUMBER)
                                    ListeActeurs.reset()
                                    if ListeItemx:
                                         for itemX in ListeItemx:
                                              ListeActeurs.addItem(itemX)                                                               
                                    
                                  
                                  extrafanart=utils.CheckItemExtrafanartPath(xbmc.getInfoLabel("Container(1999).ListItem.Path"))
                              
                                  self.windowhome.setProperty('IconMixExtraFanart',extrafanart)   
                                  self.duration = xbmc.getInfoLabel("Container(1999).ListItem.Duration") 
                                  self.display_duration(self.selecteditem,self.DBTYPE)
                      
                      else:
                        #liste des acteurs 'normaux'
                        if (self.selecteditem > -1 and not str(self.selecteditem)==""): 
                            self.windowhome.clearProperty('IconMixSagaClearArt')  
                            self.windowhome.clearProperty('IconMixSagaClearLogo')
                            self.windowhome.clearProperty('IconMixSagaBackGround')
                            self.windowhome.clearProperty('IconMixSagaBanner')
                            self.windowhome.clearProperty('IconMixSagaDiscArt')
                            self.windowhome.clearProperty('IconMixSagaPoster')
                            self.windowhome.clearProperty('IconMixSagaThumb') 
                            ListeItemx=[]
                            ResetDirector=True  
                            ListeActeursInf=None 
                            self.duration = xbmc.getInfoLabel("ListItem.Duration") 
                            self.display_duration(self.selecteditem,self.DBTYPE)
                            if MiseAjour=="1":
                               #ACTEURS VIDEONAV
                               pays.ConversionPays(None,None)
                               try:
                                 ListeActeurs=self.GetControl(self.windowvideonav,1998)
                               except:
                                 ListeActeurs=None
                               
                            if MiseAjour=="2":
                               #ACTEURS VIDEOINFO
                               try:
                                 Window = xbmcgui.Window(12003)
                               except:
                                 Window=None
                               if Window:
                                 ListeActeurs=self.GetControl(Window,1998)
                                 
                                 self.ListeDiffusion=self.GetControl(Window,8888)
                                 if self.ListeDiffusion:
                                   self.ListeDiffusion.reset()
                                   
                                   self.Episodes=utils.getallnextepisodes(self.selecteditem,None,self.DBTYPE,self.GlobalCalendrier)
                                   if self.Episodes:
                                      self.ListeDiffusion.addItems(self.Episodes)
                                   else:
                                      self.Episodes=[]
                                      self.ListeDiffusion.addItems(self.Episodes)
                                 #ListeActeursInf=self.GetControl(self.windowvideoinf,5007)
                                 
                            if MiseAjour=="3":
                               #ACTEURS VideoPlayer
                               try:
                                  ListeActeurs=self.GetControl(self.windowvideoplayer,1998)
                               except:
                                  ListeActeurs
                            if MiseAjour=="4":
                               #ACTEURS VideoPlayer
                               if not self.windowvideoplayerinfo:
                                self.windowvideoplayerinfo = xbmcgui.Window(10142)
                               try:
                                 ListeActeurs=self.GetControl(self.windowvideoplayerinfo,1998)
                               except:
                                 ListeActeurs=None
                            #ACTEURS  ------------------------------------------------                                 
                            if ListeActeurs:
                               
                              ListeItemx=utils.getCasting(self.DBTYPE,self.selecteditem,1,TMDBNUMBER)
                              ListeActeurs.reset()
                              if ListeActeursInf:
                                ListeActeursInf.reset()
                     
                              if ListeItemx: 
                                   for itemX in ListeItemx:
                                        ListeActeurs.addItem(itemX)  
                                        if ListeActeursInf:
                                            ListeActeursInf.addItem(itemX)  
                                   Realisateur=utils.Remove_Separator(xbmc.getInfoLabel("ListItem.Director").split(" (")[0].decode("utf8"))
                                   if Realisateur:
                                     self.windowhome.setProperty('IconMixDirector',utils.GetPhotoRealisateur('realisateurs',realisateur=Realisateur))                                                                        
                                   ResetDirector=False
                              
                                
                            #FENETRE MYVIDEONAV (10025) ------------------------------------------------
                            if xbmc.getCondVisibility("Window.IsVisible(10025)"):
                              
                                #mise à jour saga (videonav ou videoinfo)
                                try:
                                  ListeFanarts=self.GetControl(self.windowvideonav,5555) 
                                  ListeFanarts.reset()
                                except:
                                  ListeFanarts=None
                                
                                
                                if (self.DBTYPE=="set" or MiseAjour=="2") :
                                  self.windowhome.setProperty('IconMixUpdate1999',"on") 
                                  if not MiseAjour=="2":
                                   
                                    ListeSaga=self.GetControl(self.windowvideonav,1999)
                                    ListeFanarts=self.GetControl(self.windowvideonav,5555) 
                                    SetID=self.selecteditem
                                  else:
                                     ListeSaga=self.GetControl(self.windowvideoinf,1999)
                                     ListeFanarts=None
                                     SetID=xbmc.getInfoLabel("ListItem.SetId")
                                     
                                  if ListeSaga and SetID:
                                    
                                    FileTab=[]
                                    
                                    try:
                                      if not xbmcvfs.exists(ADDON_DATA_PATH+"/collections/"):
                                        utils.UpdateSagas(0,1,None," - Initialisation...")
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
                                  self.windowhome.clearProperty('IconMixUpdate1999')
                                #elif ListeFanarts and (self.DBTYPE=="tvshow" or self.DBTYPE=="movie"):                                  
                                #  Liste=utils.getMovieTvFanarts(self.selecteditem,self.DBTYPE)
                                #  if Liste:                                                
                                #     ListeFanarts.addItems(Liste) 
                                  
                                if self.DBTYPEOK or self.DBTYPE=="tvshow" or self.DBTYPE=="season":
                                   
                                   self.windowhome.setProperty('IconMixExtraFanart',utils.CheckItemExtrafanartPath(xbmc.getInfoLabel("ListItem.Path")))
                                   if self.DBTYPE!="tvshow" and self.DBTYPE!="season":
                                     if self.DBTYPE=="episode":                                      
                                        utils.getnextepisode(self.selecteditem,None,self.DBTYPE,self.GlobalCalendrier,self.precedenttvshow)       
                                   else:
                                      self.TvSeason=""
                                      if self.selecteditem!=self.precedenttvshow:
                                       
                                        #-------------------------- affichage des episodes de la série ------------------
                                        if not xbmc.getCondVisibility("Skin.HasSetting(DisableTvList)"):
                                          utils.getnextepisode(self.selecteditem,None,self.DBTYPE,self.GlobalCalendrier,self.precedenttvshow)
                                          self.UpdateListeEpisodes()
                                           
                                        else :
                                          utils.getepisodes(self.selecteditem,None,self.DBTYPE)
                                          self.precedenttvshow=self.selecteditem  
                                     
                                    #--------------------------------------------------------------------------------
                                if not xbmc.getCondVisibility("Skin.HasSetting(CheckSeries)"):
                                      self.windowhome.clearProperty('IconMixTv')
                                      self.windowhome.clearProperty('IconMixTvKodi')   
                                     
                                if self.DBTYPE=="episode" and xbmc.getCondVisibility("Skin.HasSetting(CheckSeries)"):
                                     TvSh=xbmc.getInfoLabel("ListItem.TVShowTitle") 
                                     TvSe=xbmc.getInfoLabel("ListItem.Season")
                                     TvId=self.selecteditem                                       
                                     if TvId and TvSe and TvSh:
                                       if TvSe!=self.TvSeason or TvSh!=self.TvShow : 
                                         self.windowhome.clearProperty('IconMixTv')
                                         self.windowhome.clearProperty('IconMixTvKodi')        
                                         self.EpSa,self.EpSaKodi,Poster=utils.getepisodes(int(TvId),int(TvSe),self.DBTYPE)  
                                         logMsg("utils.getepisodes(%s %d-%d-%s) = (%s)(%s)" %(TvSh,int(TvId),int(TvSe),self.DBTYPE,self.EpSa,self.EpSaKodi))                                         
                                         if self.EpSa>=0:                                     
                                           self.windowhome.setProperty('IconMixTv',str(self.EpSa)) 
                                           self.windowhome.setProperty('IconMixTvKodi',str(self.EpSaKodi))                                      
                                           self.TvShow=TvSh
                                           self.TvSeason=TvSe
                                         else:                                     
                                           self.TvShow=""
                                           self.TvSeason=""  
                                         
                                     else : 
                                      self.windowhome.clearProperty('IconMixTv')
                                      self.windowhome.clearProperty('IconMixTvKodi') 
                                      
                                if (self.DBTYPE=="director" or self.DBTYPE=="actor"):
                                  ActeurRealisateur=xbmc.getInfoLabel("ListItem.label")
                                  ActeurIcon=xbmc.getInfoLabel("ListItem.Icon")
                                  
                                  if "Default" in  ActeurIcon: #recherche photo
                                    
                                     Recherche=ActeurRealisateur.split(" (")[0].decode("utf8")                                
                                     HttpIcon=utils.GetPhotoRealisateur(self.DBTYPE,Recherche) 
                                     if HttpIcon:
                                        self.windowhome.setProperty('IconMixDirector',HttpIcon)
                                        ActeurIcon=HttpIcon
                                  
                                  self.windowhome.setProperty('IconMixActor',ActeurRealisateur) 
                                  if "Default" in ActeurIcon:
                                       ActeurIcon="frames/acteurvide.png"
                                  self.windowhome.setProperty('IconMixActorIcon',ActeurIcon) 
                                  ListeFilmographie=self.GetControl(self.windowvideonav,1999)
                                  if ListeFilmographie:
                                   try:
                                     ListeItemx =utils.ActeurFilmsTvKODI(self.DBTYPE,xbmc.getInfoLabel("ListItem.Label").split(" (")[0],1)
                                   except:
                                     ListeItemx=None
                                   ListeFilmographie.reset()
                                   if ListeItemx:
                                        ListeFilmographie.addItems(ListeItemx)  
                                     
                                    
                                else : 
                                    FolderPath=xbmc.getInfoLabel("Container.FolderPath")
                                    if (not "/actors" in FolderPath) and (not "actorid" in FolderPath) and (not "/directors" in FolderPath) and (not "directorid" in FolderPath):
                                      self.windowhome.clearProperty('IconMixActor')  
                                      self.windowhome.clearProperty('IconMixActorIcon')                                      
                                    if ResetDirector:
                                        self.windowhome.clearProperty('IconMixDirector')
                                #self.duration = xbmc.getInfoLabel("ListItem.Duration") 
                                #self.display_duration()
                            else : 
                              self.windowhome.clearProperty('IconMixTv')
                              self.windowhome.clearProperty('IconMixTvKodi') 
                             
                              self.TvShow=""
                              self.TvSeason=""        
                        else :                            
                           self.windowhome.clearProperty('IconMixTv')
                             
                           self.TvShow=""
                           self.TvSeason=""
                           try:
                            ListeActeurs=self.GetControl(self.windowvideonav,1998)
                           except:
                            ListeActeurs=None
                           if ListeActeurs:
                            ListeActeurs.reset()
                  self.windowhome.clearProperty('IconMixUpdating') 
          else:
            if xbmc.getCondVisibility("Window.IsVisible(10000)"):
              try:
                tt=xbmc.getInfoLabel( "Container(9000).ListItem.Property(background)")
                widgetback=int(tt.replace("WDF","").replace(".jpg",""))
                if widgetback>2:
                  widgetback=None
              except:
                widgetback=None
              if widgetback:
                HomeItem=xbmc.getInfoLabel( "Container(9000).CurrentItem" )
                if self.HomeMenuItem!=HomeItem:                  
                  self.HomeMenuItem=HomeItem                                   
                  self.IdWidgetContainerPos=None
                else:
                  HomeItemPos=xbmc.getInfoLabel( "Container(80%s1%s).CurrentItem" %(widgetback,HomeItem)) 
                  self.IdWidgetContainer=None
                  if self.IdWidgetContainerPos!=HomeItemPos:
                    self.IdWidgetContainerPos=HomeItemPos
                    fanartwd=xbmc.getInfoLabel("$INFO[Container(80%s1%s).ListItem.Art(fanart)]"%(widgetback,HomeItem )) 
                    self.windowhome.setProperty("iconmixwidgetfanart",fanartwd)  
               
                
            
            if self.kodi_player:
              #arret si lecture mais fenetre VideoNav pas visible
              if self.kodi_player.isPlayingVideo() and not xbmc.getCondVisibility("Window.IsVisible(10025)")  and ((self.windowhome.getProperty('annonceencours')!="" and self.windowhome.getProperty('annonceencours')!="full") or self.AnnonceNetflix):
                if not xbmc.getCondVisibility("Window.IsActive(12005)") and (not xbmc.getCondVisibility("Window.IsVisible(10000)") or self.AnnonceNetflix): 
                   self.kodi_player.stop() 
                   self.NetFlixBA=[]
                   self.AnnonceNetflix=None
                   self.windowhome.clearProperty('annonceencours')
                   
          #arret si lecture en plein écran mais fenetre videofullscreen pas visible
          if  self.kodi_player.isPlayingVideo() and not xbmc.getCondVisibility("Window.IsActive(12005)")  and (self.windowhome.getProperty('annonceencours')=="full" and not self.AnnonceNetflix):
                 xbmc.sleep(2000)
                 if not xbmc.getCondVisibility("Window.IsActive(12005)") and (not xbmc.getCondVisibility("Window.IsVisible(10000)") or self.AnnonceNetflix):
                   self.CompteurTemps=0 
                   self.AnnonceNetflix=None
                   self.kodi_player.stop()                   
                   self.windowhome.clearProperty('annonceencours')
          #lecture d'un film,serie,...etc..de Kodi pas la bande annonce donc recuperation des infos pour la notation en fin de lecture       
          if  self.kodi_player.isPlayingVideo() and self.windowhome.getProperty('annonceencours')=="":
                self.kodi_player.PositionLecture=self.kodi_player.getTime() 
                if not self.kodi_player.ItemID:
                  self.kodi_player.ItemID=xbmc.getInfoLabel("VideoPlayer.DBID")   
                  self.kodi_player.noterfilm=self.kodimonitor.noterfilm
                  self.kodi_player.noterserie=self.kodimonitor.noterserie        
                  if xbmc.getInfoLabel("VideoPlayer.Episode"):
                     self.kodi_player.ItemType="Episode"
                  else:
                     self.kodi_player.ItemType="Movie"
          try:
            self.checkProgressPlay()
          except:
            A=None               
               
          if not xbmc.getCondVisibility("Player.HasMedia"):
             self.CompteurTemps=self.CompteurTemps+400              
          else:
             self.CompteurTemps=0
             if xbmc.getCondVisibility("Window.IsVisible(12901)") or  xbmc.getCondVisibility("Window.IsVisible(12005)") or  xbmc.getCondVisibility("Window.IsVisible(10142)"):
               self.precedenttvshow=None
               logMsg("self.precedenttvshow=None Lecture")
               self.windowhome.clearProperty('IconmixProchainEpisode') 
          if xbmc.getCondVisibility("Window.IsActive(10000)") and not xbmc.getCondVisibility("Window.IsVisible(12003)"):
              self.RandomTime=self.RandomTime+400
              if self.precedenttvshow:
                self.precedenttvshow=None
                logMsg("self.precedenttvshow=None3")
              if self.previousitem:
                self.previousitem =None
              
          else:
              self.RandomTime=0
          if self.RandomTime>=15000:
            try:
              Cpt=int(xbmc.getInfoLabel( "Container(8080).NumItems" ))
            except:
              Cpt=0
            if Cpt>5 :
               xbmc.executebuiltin( "Control.Move(8080,%d)" %(random.randint(5,Cpt)) )
               
               self.RandomTime=0 
          
          #debug
          if len(self.GlobalAnnonces)>0:
            if len(self.GlobalAnnonces[0])!=lGlobalAnnonces:
              lGlobalAnnonces=len(self.GlobalAnnonces[0])
              #logMsg("self.GlobalAnnonces (%d) - %s" %(lGlobalAnnonces,self.GlobalAnnonces))
              
          if len(self.GlobalAnnoncesThread)!=lGlobalAnnoncesThread:
            lGlobalAnnoncesThread=len(self.GlobalAnnoncesThread)
            logMsg("self.GlobalAnnoncesThread (%d) - %s" %(lGlobalAnnoncesThread,self.GlobalAnnoncesThread))
          
          self.windowhome.setProperty("IconMixToolsbackend","en cours")
          xbmc.sleep(400)
          
            
      logMsg('Arret en cours...', 0)
      logMsg("sauvegarde calendrier")
      utils.SaveBandeAnnoncesFull(self.GlobalAnnonces)
      utils.Sauvegarde_Calendrier(self.GlobalCalendrier)
      del self.kodi_player
      del self.kodimonitor
      self.windowhome.clearProperty("IconMixToolsbackend")
            
      logMsg("Astalavista baby ;)")  
  
  def getAllDuration(self):
    if xbmc.getCondVisibility("Window.IsVisible(10025)"):
      id=xbmc.getInfoLabel("Container.ListItem(0).DBID")
      if id and id!=self.firstidduration:
        i=0
        self.firstidduration=id
        idcont=int(xbmc.getInfoLabel("System.CurrentControlID"))
        
        containeractif=xbmcgui.Window(10025).getControl(idcont) 
        
        #if containeractif:
        monlistitem=containeractif.getSelectedItem()
        logMsg("CONTAINER ACTIF = %s / %s" %(idcont,containeractif))
        label=monlistitem.getLabel()
        logMsg("-----> %s / %s" %(monlistitem,label))
        # self.windowhome.clearProperty('IconmixProchainEpisode')
        # self.firstidduration
    else:
      self.firstidduration=None
  
  def GetTrailer(self,commande=None):
      #xbmc.executebuiltin( "ActivateWindow(busydialog)" )
      if not commande:
         commande=self.windowhome.getProperty("iconmixgettrailer")
         
      
      self.windowhome.clearProperty("iconmixgettrailer")
      itemcommande={}
      if commande:
        commande=commande.split('*')
        for item in commande:
          
          itemcommande[str(item.split(":")[0])]=item.split(":")[1] 
        
      else:
        return
        
      
      trailerTypeVideo=itemcommande.get('dbtype')
      trailerTitre=itemcommande.get('label')
      trailerAnnee=itemcommande.get('year')
      trailerKODIID=itemcommande.get('dbid')
      trailerIMDBID=itemcommande.get('imdbnumber')
      trailerTMDBID=itemcommande.get('tmdbnumber')
      
      self.windowhome.setProperty('FenetreListeChoix','1')
      dialog=xbmcgui.Dialog()                
      TrailerType=""
      ListeTrailer=[]
      ContainerID=None
      Saison=None
      TMDBID='' 
      TMDBIDListe=[]
      PanneauActeur=None 
      TMDBIDListeAllocine=[]
      SAGAITEMID=[]
      TrailerType=""     
      
      if trailerTitre:
          TypeVideo=trailerTypeVideo
          PanneauActeur=True
          Titre=trailerTitre
          Annee=trailerAnnee
          KODIID=trailerKODIID
          IMDBID=trailerIMDBID
          TMDBID=trailerTMDBID
          TrailerType="dialogplus"
          if not TMDBID:
                   #TMDBID=utils.get_externalID(IMDBID,TypeVideo) 
                   TMDBID=utils.get_TMDBID(TypeVideo,KODIID,None)
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
            TrailerType="videonavsaga"
         
          
          if xbmc.getCondVisibility("Control.HasFocus(7779)"):
              PanneauActeur=True
              TypeVideo=xbmc.getInfoLabel("Container(5051).ListItem.Property(dbtype)")
              Titre=xbmc.getInfoLabel("Container(5051).ListItem.Label").decode('utf-8','ignore')
              Annee=xbmc.getInfoLabel("Container(5051).ListItem.Year")
              KODIID=xbmc.getInfoLabel("Container(5051).ListItem.DBID")
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
          if xbmc.getCondVisibility("ControlGroup(442).HasFocus"): #dialogvideoinfo cherche trailer
              #logMsg("ContainerID (%s)" %(ContainerID))
              TypeVideo=xbmc.getInfoLabel("Container(%d).ListItem.DBTYPE" %(ContainerID)) if ContainerID else xbmc.getInfoLabel("ListItem.DBTYPE")
              Titre=xbmc.getInfoLabel("Container(%d).ListItem.Label" %(ContainerID)) if ContainerID else xbmc.getInfoLabel("ListItem.Label")
              Titre=Titre.decode('utf-8','ignore')
              Annee=xbmc.getInfoLabel("Container(%d).ListItem.Year" %(ContainerID)) if ContainerID else xbmc.getInfoLabel("ListItem.Year")
              TrailerType="videoinfo7003"
          if xbmc.getCondVisibility("Control.HasFocus(7778)"): #dialogvideoinfo realisateur
              TypeVideo=xbmc.getInfoLabel("Container(5052).ListItem.DBTYPE" )
              Titre=xbmc.getInfoLabel("Container(5052).ListItem.Label" )
              Titre=Titre.decode('utf-8','ignore')
              Annee=xbmc.getInfoLabel("Container(5052).ListItem.Year" )    
              TrailerType="realisateur"

           
           
          if TrailerType=="Roles" :
               #acteurs  
               IMDBID=xbmc.getInfoLabel("Container(5051).ListItem.Property(IMDBNumber)")
               TMDBID=xbmc.getInfoLabel("Container(5051).ListItem.Property(TMDBNumber)")
               KODIID=xbmc.getInfoLabel("Container(5051).ListItem.DBID")
               if not TMDBID:
                   #TMDBID=utils.get_externalID(IMDBID,TypeVideo)
                   TMDBID=utils.get_TMDBID(TypeVideo,KODIID,None)
                   
                 
                 
          if TrailerType=="realisateur" :
               #realisateur
               IMDBID=xbmc.getInfoLabel("Container(5052).ListItem.Property(IMDBNumber)")
               TMDBID=xbmc.getInfoLabel("Container(5052).ListItem.Property(TMDBNumber)")
               KODIID=xbmc.getInfoLabel("Container(5052).ListItem.DBID")
               PanneauActeur=True
               if not TMDBID:
                     #TMDBID=utils.get_externalID(IMDBID,TypeVideo)
                     TMDBID=utils.get_TMDBID(TypeVideo,KODIID,None)
                  
          if TrailerType=="videonav":
               #VideoNav
               IMDBID=xbmc.getInfoLabel("Container(1999).ListItem.Property(IMDBNumber)")
               TMDBID=xbmc.getInfoLabel("Container(1999).ListItem.Property(TMDBNumber)")
               KODIID=xbmc.getInfoLabel("Container(1999).ListItem.DBID")
               if not TMDBID and not IMDBID:
                   json_result = utils.getJSON('VideoLibrary.Get%sDetails' %(TypeVideo), '{ "%sid":%d,"properties":["imdbnumber"] }' %(TypeVideo,int(xbmc.getInfoLabel("Container(1999).ListItem.DBID"))))                         
                   IMDBID=json_result.get("imdbnumber")                 
               if TMDBID=='' and IMDBID:
                   #TMDBID=utils.get_externalID(IMDBID,TypeVideo)
                   TMDBID=utils.get_TMDBID(TypeVideo,KODIID,None)
                   
          if TrailerType=="videonavsaga":
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
                       if DBID:
                        SAGAITEMID.append(DBID)                       
                       TMDBIDListeAllocine.append({"Titre":LABEL,"Annee":YEAR,"kodiid":DBID})
                       
                       #logMsg("Allocine (%d)(%s)(%s)(%s)(%s)(%s)" %(compteur,LABEL,YEAR,IMDBID,TMDBID,DBID),0)
                       if DBID:
                         if not TMDBID and not IMDBID:
                             json_result = utils.getJSON('VideoLibrary.GetMovieDetails', '{ "movieid":%d,"properties":["imdbnumber"] }' %(int(DBID)))                         
                             IMDBID=json_result.get("imdbnumber")                 
                       if TMDBID or IMDBID:
                            TMDBIDListe.append({"tmdbid":TMDBID,"imdbid":IMDBID,"kodiid":DBID})
                   
                   
                 
                   
          if TrailerType=="saga" :
               #SAGA
               IMDBID=xbmc.getInfoLabel("Container(5002).ListItem.Property(IMDBNumber)")
               TMDBID=xbmc.getInfoLabel("Container(5002).ListItem.Property(TMDBNumber)")
               KODIID=xbmc.getInfoLabel("Container(5002).ListItem.DBID")
               if not TMDBID and not IMDBID:
                   json_result = utils.getJSON('VideoLibrary.GetMovieDetails', '{ "movieid":%d,"properties":["imdbnumber"] }' %(int(xbmc.getInfoLabel("Container(5002).ListItem.DBID"))))                         
                   IMDBID=json_result.get("imdbnumber")
               
               else: 
                 if not TMDBID:
                    TMDBID=utils.get_TMDBID('movie',KODIID,None)
                   #TMDBID=utils.get_externalID(IMDBID,'movie')
             
          
          if TrailerType=="videoinfo7003" or TrailerType=="":
               #acteurs videoinfo   
               KODIID=xbmc.getInfoLabel("Container(%d).ListItem.DBID" %(ContainerID)) if ContainerID else xbmc.getInfoLabel("ListItem.DBID")
               TMDBID=xbmc.getInfoLabel("Container(%d).ListItem.Property(TMDBNumber)" %(ContainerID)) if ContainerID else xbmc.getInfoLabel("ListItem.Property(TMDBNumber)")
               if TypeVideo!="episode":
                 IMDBNUMBER=xbmc.getInfoLabel("Container(%d).ListItem.IMDBNumber" %(ContainerID)) if ContainerID else xbmc.getInfoLabel("ListItem.IMDBNumber")
               else:
                 IMDBNUMBER=xbmc.getInfoLabel("Container(%d).ListItem.TVShowTitle" %(ContainerID)) if ContainerID else xbmc.getInfoLabel("ListItem.TVShowTitle")
                 Titre=IMDBNUMBER
               if not TMDBID:             
                   #TMDBID=utils.get_externalID(IMDBNUMBER,TypeVideo)
                   TMDBID=utils.get_TMDBID(TypeVideo,KODIID,None)
               #logMsg("KODIID=(%s) TMDBID=(%s) IMDBNUMBER=(%s)" %(KODIID,TMDBID,IMDBNUMBER))
      #logMsg("TrailerType (%s)(%s) : (%s)(%s)" %(TrailerType,Titre,TypeVideo,TMDBID))
      #dialog.notification('IconMixTools', __language__( 32508 ), ADDON_ICON,500) 
        
      if TMDBID!='' or len(TMDBIDListe)>0 or len(TMDBIDListeAllocine)>0:
           xbmc.executebuiltin( "ActivateWindow(busydialog)" )   
           #logMsg("TrailerType (%s) : (%s)(%s)(%s)(%s)(%s)" %(TrailerType,Titre,TypeVideo,TMDBID,ContainerID,KODIID))
           if len(TMDBIDListe)>0:
             #start_time = time.time() 
             
             
             if SETTING('allocineactif')=="true" :
                ListeTrailer=ListeTrailer+utils.GetSagaTrailersAllocine(TMDBIDListeAllocine)
             if SETTING('youtubeactif')=="true" :
                ListeTrailer=ListeTrailer+utils.GetSagaTrailers(TMDBIDListe) 
             
             
     
           else:
             if TypeVideo=="tvshow":
                Saison=None                                        
             else:
                Saison=str(xbmc.getInfoLabel("ListItem.Season"))
                
             if TypeVideo=="episode"  :
                Episode=str(xbmc.getInfoLabel("ListItem.Episode"))
                Annee=None
             else:
                Episode=None
              
             if trailerTitre:
               ListeTrailer=utils.GetAllBandesAnnonces(None,KODIID,TypeVideo,Titre,Annee,Saison,Episode,TMDBID)
             else:
               ListeTrailer=utils.GetAllBandesAnnonces(self.GlobalAnnonces,KODIID,TypeVideo,Titre,Annee,Saison,Episode,TMDBID)
             
                
           if TrailerType=="videonav" and KODIID!="": 
              ListeTrailer.append({"id":xbmc.getInfoLabel("Container(1999).ListItem.FilenameAndPath"),"position":"0","iso_639_1":"","iso_3166_1":"","key":"KODI","name":__skin_string__( 208 )+"[I]"+"[COLOR=LightGrey] "+xbmc.getInfoLabel("Container(1999).ListItem.Label").decode("utf8")+" [/I][/COLOR]","site":"YouTube","size":xbmc.getInfoLabel("Container(1999).ListItem.VideoResolution"),"type":"","landscape":xbmc.getInfoLabel("Container(1999).ListItem.Art(thumb)")})
           if TrailerType=="saga" and KODIID!="": 
              ListeTrailer.append({"id":xbmc.getInfoLabel("Container(5002).ListItem.FilenameAndPath"),"position":"0","iso_639_1":"","iso_3166_1":"","key":"KODI","name":__skin_string__( 208 )+"[I]"+"[COLOR=LightGrey] "+xbmc.getInfoLabel("Container(5002).ListItem.Label").decode("utf8")+" [/I][/COLOR]","site":"YouTube","size":xbmc.getInfoLabel("Container(5002).ListItem.VideoResolution"),"type":"","landscape":xbmc.getInfoLabel("Container(5002).ListItem.Art(thumb)")})
           if TrailerType=="videoinfo7003" and ContainerID and KODIID!="":
              ListeTrailer.append({"id":xbmc.getInfoLabel("Container(%d).ListItem.FilenameAndPath" %(ContainerID)),"position":"0","iso_639_1":"","iso_3166_1":"","key":"KODI","name":__skin_string__( 208 )+"[I]"+"[COLOR=LightGrey] "+xbmc.getInfoLabel("Container(%d).ListItem.Label" %(ContainerID)).decode("utf8")+" [/I][/COLOR]","site":"YouTube","size":xbmc.getInfoLabel("Container(%d).ListItem.VideoResolution" %(ContainerID)),"type":"","landscape":xbmc.getInfoLabel("Container(%d).ListItem.Art(thumb)"%(ContainerID))})
           if TrailerType=="videoinfo7003" and not ContainerID and  KODIID!="":
              ListeTrailer.append({"id":xbmc.getInfoLabel("ListItem.FilenameAndPath" ),"position":"0","iso_639_1":"","iso_3166_1":"","key":"KODI","name":__skin_string__( 208 )+"[I]"+"[COLOR=LightGrey] "+xbmc.getInfoLabel("ListItem.Label" ).decode("utf8")+" [/I][/COLOR]","site":"YouTube","size":xbmc.getInfoLabel("ListItem.VideoResolution" ),"type":"","landscape":xbmc.getInfoLabel("ListItem.Art(thumb)")})
           if TrailerType=="Roles" and KODIID!="": 
              ListeTrailer.append({"id":xbmc.getInfoLabel("Container(5051).ListItem.FilenameAndPath"),"position":"0","iso_639_1":"","iso_3166_1":"","key":"KODI","name":__skin_string__( 208 )+"[I]"+"[COLOR=LightGrey] "+xbmc.getInfoLabel("Container(5051).ListItem.Label").decode("utf8")+" [/I][/COLOR]","site":"YouTube","size":xbmc.getInfoLabel("Container(5051).ListItem.VideoResolution"),"type":"","landscape":xbmc.getInfoLabel("Container(5051).ListItem.Art(thumb)")})
           if TrailerType=="realisateur" and KODIID!="": 
              ListeTrailer.append({"id":xbmc.getInfoLabel("ListItem.FilenameAndPath"),"position":"0","iso_639_1":"","iso_3166_1":"","key":"KODI","name":__skin_string__( 208 )+"[I]"+"[COLOR=LightGrey] "+xbmc.getInfoLabel("ListItem.Label").decode("utf8")+" [/I][/COLOR]","site":"YouTube","size":xbmc.getInfoLabel("ListItem.VideoResolution"),"type":"","landscape":xbmc.getInfoLabel("ListItem.Art(thumb)")})
           
        
           xbmc.executebuiltin( "Dialog.Close(busydialog)" ) 
      if len(ListeTrailer)>0:
          ListeNomTrailer=[]
          Image=""
          for Item in  ListeTrailer:
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
                
                ui = dialog_select_UI('choix.xml', ADDON_PATH, 'default','1080i',listing=ListeNomTrailer,trailers=ListeTrailer,ItemId=xbmc.getInfoLabel("ListItem.DBID"),Window=None)
                self.windowhome.setProperty("IconMixTrailer","1")
                ret=ui.doModal()
                del ui                          
                self.windowhome.clearProperty('IconMixTrailer')
                  
                      
      else: 
          # 
          dialog=xbmcgui.Dialog()
          dialog.notification('IconMixTools', Titre+": "+__language__( 32506 ), "acteurs/arfffff.png", 500)
      self.windowhome.setProperty('FenetreListeChoix','')
      #retour au focus précédent
      retour={"":2008,"videonav":2999,"realisateur":7778,"videoinfo7003":7003,"dialogplus":7003,"videonavsaga":2008,"Roles":7779}
      xbmc.executebuiltin("SetFocus(%d)" %(retour[TrailerType]))      
    #------------------------------------------------------------------------------------------------------------------
  def UpdateListeEpisodes(self):
      try:
        self.Window = xbmcgui.Window(10025)
      except:
        self.Window=None
      if self.Window:
        try:
          self.ListeEpisodes=self.GetControl(self.Window,2666)
        except:
          self.ListeEpisodes=None
        if self.ListeEpisodes:
                                                    
            
            self.precedenttvshow=self.selecteditem
            try:
              #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.GetEpisodes","params":{"tvshowid":39,"properties":["cast","episode","firstaired","originaltitle","productioncode","rating","ratings","season","seasonid","showtitle","specialsortepisode","specialsortseason","tvshowid","uniqueid","userrating"]},"id":1}
              self.ListeItemx,self.Prochain =utils.GetEpisodesKodi(self.selecteditem,True,self.DBTYPE)                                              
            except:
              self.ListeItemx=None
            self.ListeEpisodes.reset()
            if self.ListeItemx:
                 try:
                   #self.ListeEpisodes.setStaticContent(self.ListeItemx)
                   self.ListeEpisodes.addItems(self.ListeItemx)
                 except:
                   logMsg("en vie... setStaticContent erreur (%s)(%s)" %(self.Prochain,self.ListeItemx))
                 self.windowhome.setProperty('IconmixProchainEpisode',str(self.Prochain))
            else:
              logMsg("Liste épisodes Vides !!!")
      else:
        logMsg("xbmc.Window(10025) vide")      
    
    
    #------------------------------------------------------------------------------------------------------------------
  def CheckListeVues(self):
      try:
        self.CurrentWindowID=xbmcgui.getCurrentWindowId()
        #self.windowhome.setProperty("currentWID",str(xbmcgui.getCurrentWindowId()))
        #self.windowhome.setProperty("currentDID",str(xbmcgui.getCurrentWindowDialogId()))
        current_view = xbmc.getInfoLabel("Container.Viewmode").decode("utf-8")
      except:
        self.CurrentWindowID=None
        self.previousContentListeVues=None
        self.previousWindowListeVues=None
      if self.previousWindowListeVues!=self.CurrentWindowID or self.previousWindowModeVues!=current_view:
        #la fenetre n'est plus la même ...on recharge la liste des vues....
        self.previousWindowListeVues=self.CurrentWindowID
        self.previousWindowModeVues=current_view
        self.previousContentListeVues=None
        #mise à jour des listes de vues
        if xbmc.getCondVisibility("Control.IsVisible(7000)"):
          #si le menu général est visible
          ContentListeVues=xbmc.getInfoLabel("Container.FolderPath")
          if self.previousContentListeVues!=ContentListeVues:
             #logMsg("listedevuesContent !!(%s)!!" %(self.previousContentListeVues))            
             
             try:
              self.CurrentWindowID=xbmcgui.getCurrentWindowId()
             except:
              self.CurrentWindowID=None
              self.previousContentListeVues=None
             try:
              CurrentWindow=xbmcgui.Window(self.CurrentWindowID)
             except:
              CurrentWindow=None
             if CurrentWindow:
               try:
                 ControlList=CurrentWindow.getControl(7007)
               except:
                 ControlList=None
                 self.previousContentListeVues=None
               if ControlList:
                 ControlList.reset()
                 self.previousContentListeVues=ContentListeVues
                 content_type = utils.VueActuelle()
                 if not content_type:
                        content_type = "files"
                  
                 ListeVues=utils.ModeVuesMenu(content_type, current_view)
                 if ListeVues:
                    ControlList.addItems(ListeVues)
    
    #------------------------------------------------------------------------------------------------------------------
  def LectureMusique(self):
      if xbmc.getCondVisibility("Player.HasAudio"):
        self.CompteurTemps=0
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
                                   ItemListe.setProperty("fanart",Item)
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
               logMsg("Probleme : AlbumData,ArtisteData=utils.GetMusicFicheAlbum(None,None,1,1)",0) 
    
    #------------------------------------------------------------------------------------------------------------------
  def DetailsVuesMusique(self):
       if xbmc.getCondVisibility("Window.IsVisible(10502)"):
          self.CompteurTemps=0
          ContainerGenre=0
          self.selecteditemMusic = xbmc.getInfoLabel("ListItem.DBID")
          LabelMusic = xbmc.getInfoLabel("ListItem.Label")
          Cover=xbmc.getInfoLabel("Container.ListItem.Icon")
            
          if self.selecteditemMusic==-1 or str(self.selecteditemMusic)=="" :
             self.vide_album()
             self.windowhome.clearProperty("IconMixExtraFanart")
             self.windowhome.clearProperty('DurationToolsEnd')
             self.windowhome.clearProperty('DurationTools')
            
          if self.selecteditemMusic>-1 and not str(self.selecteditemMusic)=="" and self.previousitemMusic != self.selecteditemMusic:
            self.previousitemMusic = self.selecteditemMusic
            #self.DBTYPE=xbmc.getInfoLabel("ListItem.DBTYPE")
            self.DBTYPE=xbmc.getInfoLabel("Container.Content")
            self.windowmusicnav = xbmcgui.Window(10502) # mymusicnav.xml
            ListeSaga=self.GetControl(self.windowmusicnav,1999)
            ListeFanarts=self.GetControl(self.windowmusicnav,2995)
            
            
            if (self.DBTYPE=="artists" or self.DBTYPE=="genres"):
                if xbmc.getCondVisibility("Container.Content(genres)"): 
                   Music1999=0
                ArtisteData=[]
                self.vide_artiste()
                 
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
                                 ItemListe.setProperty("fanart",Item)
                                 TabFanarts.append(ItemListe)
                          ListeFanarts.addItems(TabFanarts)  
                    #logMsg("Artistedata %s - %s" %(ArtisteId,ArtisteData),0)
                    self.SetArtisteHomeVar(ArtisteData)       
                                                        
                       
                
               
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
                   self.display_duration(self.selecteditem,self.DBTYPE) 
                     
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
                                     ItemListe.setProperty("fanart",Item)
                                     TabFanarts.append(ItemListe)
                              ListeFanarts.addItems(TabFanarts) 
                      self.SetArtisteHomeVar(ArtisteData)  
               except:
                   logMsg("Probleme : AlbumData,ArtisteData=utils.GetMusicFicheAlbum(self.selecteditemMusic,Cover,None)",0)  
    
    #------------------------------------------------------------------------------------------------------------------
  def ShowIconmixGuide(self):
      IconmixShowGuide=self.windowhome.getProperty('IconmixShowGuide')
      if IconmixShowGuide=="1"or IconmixShowGuide=="2":
        self.windowhome.clearProperty('IconmixShowGuide')
        #calendrier des series de KODI sur 15 jours
        self.ui = dialog_ShowGuide('guide.xml', ADDON_PATH, 'default','1080i',GlobalCalendrier=self.GlobalCalendrier,mainservice=self)
        self.ui.doModal()
        retour=self.ui.retour
        del self.ui  
        if retour:
          xbmc.executebuiltin('ActivateWindow(10025,"videodb://tvshows/titles/%s",return)' %(retour)) 
        
                   
    #------------------------------------------------------------------------------------------------------------------
  def ShowIconmixInfo(self):
      dontopenserie=None
      IconmixShowInfo=self.windowhome.getProperty('IconmixShowInfo')
      if IconmixShowInfo=="55":
        self.windowhome.clearProperty('IconmixShowInfo')
        IconmixShowInfo=None
        ContainerIDActor=None
        if xbmc.getCondVisibility("Control.IsVisible(55)"):  #liste            
          ContainerIDActor=55
        if xbmc.getCondVisibility("Control.IsVisible(906)"):  #liste incurvee            
          ContainerIDActor=906
        if ContainerIDActor:
          dbtypeinfo=xbmc.getInfoLabel("Container(%d).ListItem.DBType" %(ContainerIDActor))
          
          Actuelle=xbmcgui.Window(xbmcgui.getCurrentWindowId())
          if Actuelle and "ctor" in dbtypeinfo:
            self.ListeActeurs=Actuelle.getControl(1998)
            if self.ListeActeurs:
              NomActeur=xbmc.getInfoLabel("Container(%d).ListItem.Label" %(ContainerIDActor))
              
              if 'ector' in dbtypeinfo:
                 Photo=utils.GetPhotoRealisateur('realisateurs',realisateur=NomActeur)
              else:
                 Photo=xbmc.getInfoLabel("Container(%d).ListItem.Icon" %(ContainerIDActor))
              Acteur = xbmcgui.ListItem(label=NomActeur)
              
              #Acteur=self.CreateItemInfo(None,None,55)
              if Acteur:
                Acteur.setIconImage(Photo)
                Acteur.setProperty("DbType",dbtypeinfo)
                self.ListeActeurs.reset()              
                self.ListeActeurs.addItem(Acteur)
                self.windowhome.setProperty('ActeurVideoLocal','1')
                Actuelle.setFocusId(7779)
                self.windowhome.setProperty('IconmixShowInfo',"56")
          
        
      if IconmixShowInfo=="1" or IconmixShowInfo=="2" :
        
        DBKODI=None
        
        if IconmixShowInfo=="1":
          ContainerID=1999
          ContainerRetour=1999
        
            
        if IconmixShowInfo=="2":
          TypeInfo=xbmc.getInfoLabel("Container(1998).ListItem.Property(DbType)")
          ContainerID=5051
          ContainerRetour=7779
        DBKODI=xbmc.getInfoLabel("Container(%d).ListItem.Property(DBID)" %(ContainerID) )
        DBTYPE=xbmc.getInfoLabel("Container(%d).ListItem.DbType" %(ContainerID) )
        TMDBNUMBER=xbmc.getInfoLabel("Container(%d).ListItem.Property(TMDBNUMBER)" %(ContainerID) )
        
        ItemListe=self.CreateItemInfo(DBKODI ,TMDBNUMBER,ContainerID )           
        if ItemListe:
              ListeActeursInf=[]
              if IconmixShowInfo=="1":
                ListeActeurs=self.GetControl(self.windowvideonav,1998)
                if ListeActeurs:
                  max=ListeActeurs.size()
                  cpt=0
                  while cpt<max:
                    ListeActeursInf.append(ListeActeurs.getListItem(cpt))
                    cpt=cpt+1
              if IconmixShowInfo=="2":
                ListeActeursInf=utils.getCasting(DBTYPE,DBKODI,1,TMDBNUMBER) 
              
              
                  
             
              self.windowhome.setProperty('IconMixExtraFanart',utils.CheckItemExtrafanartPath(xbmc.getInfoLabel("Container(%d).ListItem.Path" %(ContainerID) )))   
              self.duration = xbmc.getInfoLabel("Container(%d).ListItem.Duration" %(ContainerID) ) 
              self.display_duration(DBKODI,DBTYPE)
              self.ui = dialog_ShowInfo('madialogvideoInfo.xml', ADDON_PATH, 'default','1080i',listitem=ItemListe,acteurs=ListeActeursInf,mainservice=self,dbid=DBKODI,dbtype=DBTYPE)
              ret=self.ui.doModal()
              dontopenserie=self.ui.dontshow
              Genre5001=self.ui.Genre5001
              del self.ui                          
        self.windowhome.clearProperty('IconmixShowInfo')
        if dontopenserie:
          xbmc.executebuiltin("SetFocus(%d)" %(ContainerID))
        else:
          if not Genre5001:
            xbmc.executebuiltin("ActivateWindow(10025,videodb://%ss/titles/%s/-2/,return)" %(DBTYPE,DBKODI))
          else:
            xbmc.executebuiltin("ActivateWindow(10025,videodb://%ss/genres/%s,return)"%(DBTYPE,Genre5001))
    
    #------------------------------------------------------------------------------------------------------------------
  def AutoRecherche(self):
      #if xbmc.getCondVisibility("Control.IsVisible(9010)") and xbmc.getCondVisibility("Control.IsVisible(312)"):
        """ 
        if xbmc.getCondVisibility("Control.HasFocus(9010)"):
          self.AllocineID=xbmc.getInfoLabel("Container(9010).ListItem.Property(AllocineID)")
          if self.AllocineID and self.AllocineID!="None" and self.AllocineID!=self.AllocineIDPrec:
            self.AllocineIDPrec=self.AllocineID
            try:
              window = xbmcgui.Window(10103) #dialogkeyboard.xml
              window.getControl(9099).setText("")
            except:
              return
            details=utils.Allocine_Details(IdCode=self.AllocineID ,TypeVideo="movie")            
            if details:
              
              try:             
                synopsys=details.get("movie").get("synopsisShort")              
              except:
                synopsys=None                
              if synopsys:
                try:
                  window = xbmcgui.Window(10103) #dialogkeyboard.xml
                  window.getControl(9099).setText(synopsys)
                except:
                  return
        else:
          AllocineIDPrec=None
        """
        if self.windowhome.getProperty("AutoCompletionShowItem"):
          path=self.windowhome.getProperty("AutoCompletionShowItem")
          self.windowhome.clearProperty("AutoCompletionShowItem")
          if "selectautocomplete" in path:
            try:
                id=path.split("id=")[1]
                window = xbmcgui.Window(10103) #dialogkeyboard.xml
                MyEdit=window.getControl(312) #edit
            except:
                logMsg("autocompletion failed (%s) " % id, level=logMsgNOTICE)
                return None
            window.setFocusId(312)
            MyEdit.setText(id)
            xbmc.executebuiltin("SendClick(10103,32)")
            xbmc.executebuiltin("SendClick(10103,8)")
          else:            
            DBKODI=int(xbmc.getInfoLabel("Container(9010).ListItem.DBID"))
            if "showinfoitem" in path:
              logMsg("Appel INFO")
              path=xbmc.getInfoLabel("Container(9010).ListItem.FolderPath")
              DBKODI=int(xbmc.getInfoLabel("Container(9010).ListItem.DBID"))
              DbType=xbmc.getInfoLabel("Container(9010).ListItem.DBTYPE")
              ItemListe=self.CreateItemInfo(DBKODI ,None,None,DbType )
              dontshow=None           
              if ItemListe:
                    logMsg("Itemliste.path (%s)" %(ItemListe.getPath()))
                    ListeActeursInf=utils.getCasting(DbType,DBKODI,1,None)
                    self.windowhome.setProperty('IconMixExtraFanart',utils.CheckItemExtrafanartPath(xbmc.getInfoLabel("Container(9010).ListItem.Path" )))   
                    self.duration = xbmc.getInfoLabel("Container(9010).ListItem.Duration" ) 
                    self.display_duration(DBKODI,DbType)
                    self.ui = dialog_ShowInfo('madialogvideoInfo.xml', ADDON_PATH, 'default','1080i',listitem=ItemListe,acteurs=ListeActeursInf,mainservice=self,dbid=DBKODI,dbtype=DbType)
                    self.ui.doModal()
                    dontshow=self.ui.dontshow
                   
                    del self.ui
                                 
            if path and not "showinfoitem" in path and not dontshow:
              logMsg("GO showitem (%s)(%s)" %(path,xbmc.getInfoLabel("Container(9010).ListItem.property(ItemID)")))
              try:
               path=path.lower()
               dbid=DBKODI if not "addon" in path else 1
               
              except:
                logMsg("fuck showitem (%s)(%s)" %(path,xbmc.getInfoLabel("Container(9010).ListItem.DBID"))) 
                path=None
              if path and not "addon:" in path:
                if "musicdb" in path:
                  windowid=10502                    
                else:
                  windowid=10025
                #xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.executebuiltin('SendClick(,301)')
               
                xbmc.executebuiltin('ActivateWindow(%d,%s,return)' %(windowid,path)) 
                if windowid!=10146:            
                  xbmc.executebuiltin('Container.Update(%s)' %path)
                  actuelpath=xbmc.getInfoLabel("Container.FolderPath").lower()
                  compteur=0
                  while (path!=actuelpath or xbmc.getCondVisibility("Container.IsUpdating")) and compteur<80:                
                      xbmc.sleep(20)
                      actuelpath=xbmc.getInfoLabel("Container.FolderPath").lower()
                      compteur=compteur+1
                  if compteur>=80:
                    logMsg("arffffff (%s)-(%s)-(%s)" %(path,xbmc.getInfoLabel("ListItem.FolderPath").lower(),xbmc.getInfoLabel("Container.FolderPath")))
                  
                  try:
                    windowobj=xbmcgui.Window(int(windowid))
                  except:
                    windowobj=None
                    logMsg("err1")
                  
                  try:
                    currentlistid=windowobj.getFocusId()
                    
                  except:
                    currentlistid=None
                    logMsg("err2 (%s)" %currentlistid)
                 
                  try:
                    ActuelNbItems=int(xbmc.getInfoLabel("Container.NumItems"))
                  except:
                    ActuelNbItems=None
                    logMsg("err3 (%s)" %xbmc.getInfoLabel("Container.NumItems"))
                  logMsg("CurrentID=%s , %s" %(currentlistid,windowobj.getFocus()))  
                  if ActuelNbItems:   
                    cpt=0
                    ItemFocus=0
                    while cpt<=ActuelNbItems:
                      try:
                        ITEMDBID=int(xbmc.getInfoLabel("Container(%d).ListItemAbsolute(%d).DBID" %(currentlistid,cpt)) )    
                        
                      except:
                        ITEMDBID=None
                      #logMsg("FOCUS cherche : %s/%s/%d" %(dbid,ITEMDBID,cpt ))
                      if ITEMDBID==dbid:
                        ItemFocus=cpt
                        #logMsg("FOCUS : %s" %ItemFocus )
                        break 
                      cpt=cpt+1
                    #xbmc.executebuiltin("Action(FirstPage)")
                    windowobj.getFocus().selectItem(ItemFocus)
                    #xbmc.executebuiltin("Control.SetFocus(%d,%d,True)" %(currentlistid,ItemFocus))
              elif "addon:" in path:
                path=path.replace("addon:","")
                Action=""                  
                self.start_info_actions("selectautocomplete", path)
                xbmc.executebuiltin('SendClick(,300)')
              self.windowhome.clearProperty("AutoCompletionShowItem")
              return     
            try:
              xbmcgui.Window(10103).setFocusId(9010)
              return
            except:
              return
           
        Edit312=xbmc.getInfoLabel("Control.GetLabel(312).index(1)")
        if Edit312!=self.Recherche or self.AutoCompletionProvider!=self.windowhome.getProperty("AutoCompletionProvider"):
          self.Recherche=Edit312
          
          limit=50
          self.PurgeCache=None        
          self.AutoCompletionProvider=None
          if xbmc.getCondVisibility("String.Contains(ListItem.DbType,artist) | String.Contains(ListItem.DbType,album) | String.Contains(ListItem.DbType,song)"):
            basetype="music"
          else:
            basetype="videos"
          if not len(self.windowhome.getProperty("AutoCompletionProvider"))>0:
            self.windowhome.setProperty("AutoCompletionProvider",MonAutoCompletion.GetAutoCompleteProvider())
          
          self.AutoCompletionProvider=self.windowhome.getProperty("AutoCompletionProvider")
          if "AutoCompletePurge" in self.AutoCompletionProvider:
            self.AutoCompletionProvider=MonAutoCompletion.GetAutoCompleteProvider()
            self.PurgeCache=True
          if self.AutoCompletionProvider=="AutoCompleteUpdate":
            self.AutoCompletionProvider=MonAutoCompletion.GetAutoCompleteProvider()
          self.windowhome.setProperty("AutoCompletionProvider",self.AutoCompletionProvider)
          if len(self.Recherche)<3 and not self.PurgeCache:
            #logMsg("resetProp")
            self.resetPropositions()
          else:
            Action=""                  
            self.start_info_actions("autocomplete", self.Recherche,limit,self.AutoCompletionProvider,basetype)
       #------------------------------------------------------------------------------------------------------------------
  def start_info_actions(self,action,id=None,limit=50,provider=None,basetype=None):
        if action == 'autocomplete':
            listitems = MonAutoCompletion.get_autocomplete_items(id,limit,provider, basetype,self.PurgeCache)
            self.PurgeCache=None
            self.pass_list_to_skin(listitems,limit,basetype,provider)
        
        elif action == 'selectautocomplete':
            #self.resolve_url(handle)
            try:
                window = xbmcgui.Window(10103) #dialogkeyboard.xml
                MyEdit=window.getControl(312) #edit
            except:
                logMsg("autocompletion failed (%s) " % id, level=logMsgNOTICE)
                return None
            window.setFocusId(312)
           
            MyEdit.setText(str(id))
            xbmc.executebuiltin("SendClick(10103,32)")
            xbmc.executebuiltin("SendClick(10103,8)")
            
            return None
            # xbmc.executebuiltin("SendClick(103,32)")
        
        
    #------------------------------------------------------------------------------------------------------------------
  def resetPropositions(self,Items=[]):
        try:
          window = xbmcgui.Window(10103) #dialogkeyboard.xml
        except:
          window=None
        if window:
          try:
            MyPropositions=window.getControl(9010) #edit
            MyPropositionsFond=window.getControl(9015) #image
            MyPropositionsCompteur=window.getControl(9016) #Compteur
          except:
            MyPropositions=None
            MyPropositionsFond=None
            MyPropositionsCompteur=None
          
          
          if MyPropositions and MyPropositionsFond:
            MyPropositions.reset()            
            MyPropositions.setStaticContent(Items)
            #MyPropositions.addItems(Items)
            if len(Items)>0 and MyPropositionsFond and xbmc.getInfoLabel("Skin.String(AutoCompleteProvider)")=="kodi":
              Hauteur=(44*((len(Items)//4)+1))
              if Hauteur>400:
                Hauteur=400
              MyPropositionsFond.setHeight(15+Hauteur)
              
              if MyPropositionsCompteur:
                MyPropositionsCompteur.setPosition(35,Hauteur+195)
      

    #------------------------------------------------------------------------------------------------------------------
  def pass_list_to_skin(self,data=[],  limit=False,basetype=None,provider=None):

        items=[]
        if data and limit and int(limit) < len(data) and not provider =="kodi":
            data = data[:int(limit)]
        
        
        items = self.create_listitems(data,basetype)
        #items = [(i.getProperty("path"), i, bool(i.getProperty("directory"))) for i in items]
        self.resetPropositions(items)
            
            


    #------------------------------------------------------------------------------------------------------------------
  def create_listitems(self,data=None,basetype=None):
        if not data:
            return []
        itemlist = []
        cpt=0
        for item in data:
            #listitem = xbmcgui.ListItem('%s' % (str(cpt)))
            
            listitem=xbmcgui.ListItem(label=item.get("label"))
            search_string=item.get("search_string")
            path=unicode(item.get("path"))
            if search_string:                
                  path = "plugin://script.iconmixtools/?action=selectautocomplete&id=%s" % search_string
            dbtype=item.get("dbtype")
            label=item.get("label")
            Art=item.get("art")
            icon=item.get("icon")
            dbid=item.get("dbid")
            listitem.setProperty('ItemID', str(dbid) if dbid else search_string)
            listitem.setProperty('AllocineID',"%s" %item.get("allocineid") )
            
            listitem.setLabel2(item.get("showtitle"))
            winid=item.get("winid")
            plot=item.get("plot")
            listitem.setLabel(label)
            listitem.setProperty('dbtype', dbtype)
            listitem.setProperty('winid', str(winid))
            listitem.setPath(path=path)
            
                #telex                                
            listitem.setProperty("index", str(cpt))
            if not dbtype:
              #plot=""
              logMsg("PATH=%s" %path)
              listitem.setInfo("video", {"title": label,"mediatype": "movie","plot":plot,"path":path,"year":item.get("year")}) 
            elif "movie" in dbtype:
              icon="flags/keytype/movie.png" 
              listitem.setInfo("video", {"dbid": int(dbid) if dbid else None,"title": label,"mediatype": "movie","plot":plot,"path":path,"year":item.get("year")}) 
            elif "tvshow" in dbtype: 
              icon="flags/keytype/tv.png"
              listitem.setInfo("video", {"dbid": int(dbid)  if dbid else None,"title": label,"mediatype": "tvshow","plot":plot,"path":path,"year":item.get("year")}) 
            listitem.setIconImage(icon)
            if Art:              
                  Art["thumb"]=icon
                  listitem.setArt(Art)
            
            itemlist.append(listitem)
            cpt=cpt+1
        return itemlist
  
    #------------------------------------------------------------------------------------------------------------------
  def resolve_url(self,handle):
        if handle:
            xbmcplugin.setResolvedUrl(handle=int(handle),
                                      succeeded=False,
                                      listitem=xbmcgui.ListItem())           
 #-----------------------------------------------        
    #------------------------------------------------------------------------------------------------------------------               
    #------------------------------------------------------------------------------------------------------------------
  def BandeAnnonceAutomatique(self):
       ListeTrailer=None
       NetflixView=xbmc.getCondVisibility("Control.IsVisible(562)|Control.IsVisible(563)")
       if not xbmc.Player().isPlaying() and (int(self.kodimonitor.tempsannonce)>0 or NetflixView==True) and xbmc.getCondVisibility("Window.IsActive(10025)") and not xbmc.getCondVisibility("Window.IsActive(12003)") and not xbmc.getCondVisibility("System.HasModalDialog"):
          self.PreviousBAnnonce=self.windowhome.getProperty('BAprecedenteInf')
          
          #if ((self.selecteditem in self.NetFlixBA) or (int(self.kodimonitor.tempsannonce)>0)):
          if (int(self.kodimonitor.tempsannonce)>0) or xbmc.getCondVisibility("Skin.HasSetting(NoNetflixBA)"):
            NetflixView=None
          else:
            LeType=xbmc.getInfoLabel("ListItem.DBTYPE")
            try:
              delaiBA=int(xbmc.getInfoLabel("Skin.String(BaDelai)"))*1000
            except:
              delaiBA=0
            #logMsg("self.CompteurTemps: %s self.tempsannonce: %s -%s" %(self.CompteurTemps,self.tempsannonce,LeType),0)
          if (((int(self.kodimonitor.tempsannonce)>0) and (self.CompteurTemps>(int(self.kodimonitor.tempsannonce)*1000)))or (NetflixView and self.CompteurTemps>delaiBA)) and ((LeType=="movie" and self.kodimonitor.annoncefilm=="true") or (LeType=="tvshow" and self.kodimonitor.annonceserie=="true")) and self.PreviousBAnnonce!=self.selecteditem :
            logMsg("DELAIBA %d-%d" %(self.CompteurTemps,delaiBA))
            try:
              VolumeBA=int(xbmc.getInfoLabel("Skin.String(BaVolume)"))
            except:
              VolumeBA=100
            KodiTrailer=xbmc.getInfoLabel("ListItem.Trailer")
            KODIID=xbmc.getInfoLabel("ListItem.DBID")
            if self.buttonFullScreen:
                   del self.buttonFullScreen
                   self.buttonFullScreen=None
            AllocineBA=None
           
            
            #start_time = time.time()
            self.PreviousBAnnonce=self.selecteditem
            self.NetFlixBA.append(self.selecteditem)
            self.windowhome.setProperty("BAprecedenteInf",str(self.selecteditem))
            if LeType=="movie":
              KodiTitre=xbmc.getInfoLabel("ListItem.Label").lower()
            else:
              KodiTitre=xbmc.getInfoLabel("ListItem.TVShowTitle").lower()
            Annee=xbmc.getInfoLabel("ListItem.Year")
            if not NetflixView or not KodiTrailer:
              logMsg("ListeTrailer  (%s)" %KODIID)
              ListeTrailer=utils.GetAllBandesAnnonces(self.GlobalAnnonces,KODIID,LeType,KodiTitre,Annee,None,None,None) 
            else:
              #-------- KODI --------
              
              if KodiTrailer:
                try:
                  #KodiTrailer=KodiTrailer.split("videoid=")[1]
                  logMsg("TRAILER DE KODI")
                  if "youtube" in KodiTrailer:
                     Origine="youtube"
                  else:
                     Origine=""
                  KodiTrailer=KodiTrailer.replace("plugin://plugin.video.youtube/?action=play_video&videoid=","plugin://plugin.video.youtube/play/?video_id=")
                  ListeTrailer=[{"id":KodiTrailer,"position":"0","iso_639_1":"","iso_3166_1":"","key":Origine,"name":"ooo","site":"YouTube","size":"","type":"","landscape":""}]    
                except:
                  ListeTrailer=None
    
            if ListeTrailer:
             
              
              PlayListBA=xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
              PlayListBA.clear()
              
              ListeId=[]                           
              for Item in ListeTrailer:  
                 if not  Item["id"] in ListeId:                               
                   Elements = xbmcgui.ListItem(label=utils.try_decode(Item.get("name"))+" ["+utils.try_decode(Item.get("type"))+" - "+str(Item.get("size"))+"p - "+utils.try_decode(Item.get("iso_3166_1"))+"]")
                   Elements.setInfo("video", {"title": utils.try_decode(Item.get("name"))+" ("+utils.try_decode(Item.get("type"))+" - "+str(Item.get("size"))+"p - "+utils.try_decode(Item.get("iso_3166_1"))+") ","mediatype": "movie"})
                   Elements.setArt({"poster":Item["landscape"]})
                   if "cineserie" in Item["id"]:
                     Item["id"]=utils.BACineSeriesGetVideo(Item["id"],Item.get("size"))
                   if "youtube" in Item["id"]:
                    idyoutube=Item["id"].split('video_id=')[1]
                    if idyoutube:
                      urlyoutube=youturl.getyoutubeurl(idyoutube)
                      if urlyoutube:
                        Item["id"]=urlyoutube
                   if Item["id"]:
                    PlayListBA.add(Item["id"],Elements) 
                    ListeId.append(Item["id"])
                   if xbmc.getCondVisibility("Control.IsVisible(562)|Control.IsVisible(563)"):
                    break
                                                
              if NetflixView==True:
                self.AnnonceNetflix=True
                self.kodi_player.play(PlayListBA,windowed=True,VolumeBA=VolumeBA) 
                
              else:
                if not self.kodimonitor.annoncefull or self.kodimonitor.annoncefull=="false":
                  self.ui = dialog_BandeAnnonce('annonce.xml', ADDON_PATH, 'default','1080i',PlayListItem=PlayListBA,VolumeBA=VolumeBA)                          
                  self.ui.doModal()
                  del self.ui
                  del PlayListBA
                  self.windowhome.clearProperty('annonceencours')
                else:
                  self.windowhome.setProperty('annonceencours','full')
                  if self.kodi_player:                              
                   self.kodi_player.play(PlayListBA,VolumeBA=VolumeBA,windowed=False)                                
            self.CompteurTemps=0                   
    #------------------------------------------------------------------------------------------------------------------    
    #------------------------------------------------------------------------------------------------------------------
  def checkProgressPlay(self):
      
      if  self.kodi_player.isPlaying() and self.windowhome.getProperty('annonceencours')=="" and xbmc.getCondVisibility("Skin.HasSetting(NouveauProgress)"):    
        Window=None
        WindowID=None
        if xbmc.getCondVisibility("Window.IsVisible(10142)"):
          WindowID=10142
        elif xbmc.getCondVisibility("Window.IsVisible(10115)"):
          WindowID=10115
        elif xbmc.getCondVisibility("Window.IsVisible(12901)"):
          WindowID=12901
        elif xbmc.getCondVisibility("Window.IsVisible(10120)"):
          WindowID=10120
        elif xbmc.getCondVisibility("Window.IsVisible(12006)"):
          WindowID=12006
        if WindowID:
          try:
            Window=xbmcgui.Window(WindowID) 
          except:
            Window=None
        if Window:
          try:          
            progressLabel=self.GetControl(Window,2222)
            #progressLabelEnd=self.GetControl(Window,2223)
            progressBar=self.GetControl(Window,23)
          except:
            progressLabel=None
          if progressLabel:
            try:
              progressPosition=int(progressBar.getPercent())
              PositionLecture=xbmc.getInfoLabel("Player.Time")
            except:
              progressPosition=None
              logMsg("Pas de progressPosition")
            
            if progressPosition!=None and ( PositionLecture!=self.PreviousprogressPosition or self.PreviousprogressWindow!=WindowID):
              self.PreviousprogressPosition=PositionLecture
              TT=PositionLecture.rsplit(':')
              XX=0
              LabelWidth=95
              if len(TT)==3:
                if int(TT[0])>0:
                   PositionLecture=TT[0]+":"+TT[1]+":"+TT[2]
                   LabelWidth=130
                   
                else:
                    
                    PositionLecture=TT[1]+":"+TT[2]
                
              if len(TT)==2:
                PositionLecture=TT[0]+":"+TT[1]
              progressLabel.setWidth(LabelWidth)
              self.PreviousprogressWindow=WindowID
              PosY=progressBar.getY()
              PosX=progressBar.getX()
              #progressLabelEnd.setPosition(PosX+progressBar.getWidth()-progressLabelEnd.getWidth(),PosY-30)
              PosX=PosX-(((LabelWidth*progressPosition)//100)//2)
              progressLabel.setPosition(PosX+((progressBar.getWidth()*progressPosition)//100),PosY-2)
              progressLabel.setHeight(progressBar.getHeight()+2)
              progressLabel.setLabel(PositionLecture)
      else:
            self.PreviousprogressPosition=None
            self.PreviousprogressWindow=None     
                
  
    #------------------------------------------------------------------------------------------------------------------
  def vide_artiste(self):
        self.windowhome.clearProperty("ArtistBio")
        self.windowhome.clearProperty("ArtistThumb")
        self.windowhome.clearProperty("ArtistLogo")
        self.windowhome.clearProperty("ArtistBanner")
        self.windowhome.clearProperty("ArtistFanart")
        self.windowhome.clearProperty("ArtistFanart2")
        self.windowhome.clearProperty("ArtistFanart3") 
        
    #------------------------------------------------------------------------------------------------------------------
  def vide_album(self):
       self.windowhome.clearProperty("AlbumCover")
       self.windowhome.clearProperty("AlbumBack")
       self.windowhome.clearProperty("AlbumCd")
       self.windowhome.clearProperty("AlbumInfo")
       
    #------------------------------------------------------------------------------------------------------------------
  def vide_artisteplayer(self):
        self.windowhome.clearProperty("ArtistBioPlayer")
        self.windowhome.clearProperty("ArtistThumbPlayer")
        self.windowhome.clearProperty("ArtistLogoPlayer")
        self.windowhome.clearProperty("ArtistBannerPlayer")
        self.windowhome.clearProperty("ArtistFanartPlayer")
        self.windowhome.clearProperty("ArtistFanart2Player")
        self.windowhome.clearProperty("ArtistFanart3Player") 
        
    #------------------------------------------------------------------------------------------------------------------
  def vide_albumplayer(self):
       self.windowhome.clearProperty("AlbumCoverPlayer")
       self.windowhome.clearProperty("AlbumBackPlayer")
       self.windowhome.clearProperty("AlbumCdPlayer")
       self.windowhome.clearProperty("AlbumInfoPlayer")
           

    #------------------------------------------------------------------------------------------------------------------
  def display_duration(self,DBKODI=None,DBTYPE=None):
       
        xxx="null"
        
        #self.windowhome.setProperty('ItemUniqueGenre',xbmc.getInfoLabel( "ListItem.Genre" ).replace(" /",", "))
        logMsg("self.duration (%s)" %(self.duration))
        duree=self.duration
        #if self.DBTYPE=="movie":
        #  pays.ConversionPays("movie",ContainerID)
        if not duree:
          duree=utils.GetDuration(DBKODI,DBTYPE)
        if duree :
        #else :
         if duree.find(':')!=-1: #KODI LEIA
            TT=duree.rsplit(':')
            XX=0
            if len(TT)==3:
              XX=XX+int(TT[0])*60
              XX=XX+int(TT[1])
            if len(TT)==2:
              XX=int(TT[0])
            if len(TT)>1:
             duree=str(XX)
        
         if duree.find(':')==-1:
            readable_duration = utils.in_hours_and_min(duree)
            self.windowhome.setProperty('DurationTools', readable_duration)
            if int(duree)>0:
              now = datetime.now()
              now_plus_10 = now + timedelta(minutes = int(duree))
              xxx = format(now_plus_10, '%Hh%M')
              self.windowhome.setProperty('DurationToolsEnd', xxx)
            else:
              self.windowhome.clearProperty('DurationToolsEnd')
              self.windowhome.clearProperty('DurationTools')
         else:
           self.windowhome.setProperty('DurationTools', duree)
        else:
           self.windowhome.clearProperty('DurationToolsEnd')
           self.windowhome.clearProperty('DurationTools')    
             
    #------------------------------------------------------------------------------------------------------------------
  def _init_vars(self):
      self.windowhome = xbmcgui.Window(10000) # Home.xml 
      self.windowvideonav = xbmcgui.Window(10025) # myvideonav.xml           
      self.windowvideoinf = xbmcgui.Window(12003) # dialogvideoinfo.xml 
      self.windowvideoplayer = xbmcgui.Window(12901) # videoOSD.xml 
      try:
        self.windowvideoplayerinfo = xbmcgui.Window(10142) # DialogFullScreenInfo.xml
      except:
        self.windowvideoplayerinfo = None
      self.previousitem = ""
      self.AnnonceNetflix=None
      self.previousProchainID=None
      self.previousitem8889 = ""
      self.previousitem1998 = ""
      self.previousLABEL1999 = ""
      self.previousitem1998local = ""
      self.previousitemMusic = ""
      self.previousitemPlayer= ""
      self.previousContentListeVues= ""
      self.previousWindowListeVues=""
      self.previousWindowModeVues=""
      self.previousContainer=""
      self.PreviousWindowActiveID= ""
      self.PreviousPlayerActiveID= ""
      self.PreviousBAnnonce=0
      self.DBTYPEOK = False
      self.DBTYPE= ""
      self.duration=""
      self.TvShow=""
      self.TvSeason=""      
      self.EpSa=0
      self.EpSaKodi=0
      self.precedenttype=None
      self.precedenttvshow=None
      self.windowhome.clearProperty('DurationTools')                   
      self.windowhome.clearProperty('DurationToolsEnd')
      self.windowhome.clearProperty('IconMixExtraFanart') 
      self.windowhome.clearProperty('IconMixTv')
      self.windowhome.clearProperty('IconMixSaga')
      self.windowhome.clearProperty('IconMixDirector')
      self.windowhome.clearProperty('IconMixActor')
      self.windowhome.clearProperty('IconMixActorIcon')
      self.windowhome.clearProperty('IconMixTrailer')
      self.windowhome.clearProperty('annonceencours')
      self.windowhome.clearProperty('BAprecedenteInf')
      self.windowhome.setProperty("IconMixDataPath",ADDON_DATA_PATH)
      self.windowhome.setProperty("IconMixToolsbackend","EnCours")
      self.kodimonitor = myMonitor()
      self.kodi_player = Player()
      self.annoncefull=self.kodimonitor.ADDON.getSetting('annoncefull')
      self.allocinefirst=self.kodimonitor.ADDON.getSetting('allocinefirst')
      self.allocineactif=self.kodimonitor.ADDON.getSetting('allocineactif')
      self.youtubeactif=self.kodimonitor.ADDON.getSetting('youtubeactif')
      self.annoncetoutes=self.kodimonitor.ADDON.getSetting('annoncetoutes')
      self.buttonFullScreen=None
      self.PreviousprogressPosition=None
      self.PreviousprogressWindow=None
      self.NetFlixBA=[]
      
        
    #------------------------------------------------------------------------------------------------------------------
  def GetControl(self,Window=None,Id=None):
      ControlId=None
      
      if Window:
                    
          try:
               ControlId=Window.getControl(Id)  
          except:
               ControlId=None
      return ControlId
      
    
    
    
          
    #------------------------------------------------------------------------------------------------------------------
  def CheckActeursRoles(self,F8889=None, F7781=None, F7779=None,F7777=None,IconmixShowInfo=None,ActeurRealisateur="acteurs"):
      #7779 : roles
      #7781 : acteurs
      #8889 : bio
      #7777 : director (dialogvideoinf)
      #logMsg("CheckActeursRoles (%s) : F8889 (%s) ,  F7781 (%s) ,  F7779 (%s) , F7777 (%s)" %(xbmc.getInfoLabel("Container(1998).ListItem.Label"),F8889 , F7781 , F7779 ,F7777))
      ListeRole=None
      if F8889 | F7781 | F7779 |F7777:
          self.CompteurTemps=0
          if not F8889: #si pas bio
              
              if not F7777:
                 self.selecteditem1998 = xbmc.getInfoLabel("Container(1998).ListItem.Label").split(" (")[0]  
                 ActeurRealisateur=xbmc.getInfoLabel("Container(1998).ListItem.Property(DbType)")
              else:
                 if not IconmixShowInfo:
                   self.selecteditem1998 = xbmc.getInfoLabel("ListItem.Director").split(" (")[0]
                 else:
                   self.selecteditem1998 = xbmc.getInfoLabel("Container(1990).ListItem.Director").split(" (")[0] 
                   
                 ActeurRealisateur="director" 
                 self.windowhome.setProperty('IconmixDirectorName',utils.Remove_Separator(self.selecteditem1998))
              if self.selecteditem1998:
                self.selecteditem1998=self.selecteditem1998.replace("M. ","") 
                   
                           
              
              KodiLocal=self.windowhome.getProperty('ActeurVideoLocal')
              if (self.previousitem1998 != self.selecteditem1998 and not str(self.selecteditem1998)=="") or ( self.previousitem1998local!=KodiLocal) or (IconmixShowInfo and self.selecteditem1998) :
                if not IconmixShowInfo:
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
                     if not self.windowvideoplayerinfo:
                       self.windowvideoplayerinfo = xbmcgui.Window(10142)                     
                     ListeRole=self.GetControl(self.windowvideoplayerinfo,5051)
                else:
                  try:
                    win=xbmcgui.Window(xbmcgui.getCurrentWindowDialogId())
                  except:
                    win=None
                    self.windowhome.clearProperty('IconmixShowInfo')
                  if win:
                    if not F7777:
                      ListeRole=self.GetControl(win,5051)
                    else:
                      ListeRole=self.GetControl(win,5052)
                                               
                   
                dialog=None 
                if ListeRole:
                  Acteur=self.selecteditem1998.decode("utf8") 
                  if not KodiLocal:
                         dialog = xbmcgui.DialogBusy()
                         dialog.create()
                         ListeItemx=utils.ActeurFilmsTvTMDB(ActeurRealisateur,self.selecteditem1998,1)
                         dialog.close()
                  else:
                         ListeItemx=utils.ActeurFilmsTvKODI(ActeurRealisateur,self.selecteditem1998,1) #.split(" (")[0],1)
                         if not ListeItemx:
                            ListeItemx=utils.ActeurFilmsTvTMDB(ActeurRealisateur,self.selecteditem1998,1)
                            self.windowhome.clearProperty("ActeurVideoLocal")
                       
                  ListeRole.reset()
                  if ListeItemx: 
                       for itemX in ListeItemx:
                            ListeRole.addItem(itemX)
                  else:
                     ItemVide = xbmcgui.ListItem(label="******",iconImage="DefaultTVShows.png",label2="*******") 
                     ItemVide.setProperty("dbtype","movie")
                     ItemVide.setInfo("video", {"title": "????","year": "****","originaltitle": "original_title","trailer":"id"}) 
                     ListeRole.addItem(ItemVide)                                 
                  
                  
          if not F7781:
              ActiF7779="non"
              if F7779  or F7777:
                  if F7779:
                     self.selecteditem8889 = xbmc.getInfoLabel("Container(1998).ListItem.Label")
                  else:
                     if not IconmixShowInfo:
                       self.selecteditem8889 = xbmc.getInfoLabel("ListItem.Director").split(" (")[0]
                     else:
                       self.selecteditem8889 = xbmc.getInfoLabel("Container(1990).ListItem.Director").split(" (")[0] 
              else:
                  if not xbmc.getCondVisibility("Player.HasVideo"):
                      self.selecteditem8889 = xbmc.getInfoLabel("ListItem.DBID")
                  else:
                      self.selecteditem8889 = xbmc.getInfoLabel("VideoPlayer.DBID")                   
                  
              self.previousitem = ""
              self.previousitemMusic = ""
              if (self.previousitem8889 != self.selecteditem8889 and not str(self.selecteditem8889)=="") or IconmixShowInfo:
                  if F7779 or F7777:
                    ActiF7779="oui"
                    if not F7777:
                        self.LABEL8889=xbmc.getInfoLabel("Container(1998).ListItem.Label").split(" (")[0].decode("utf8")
                        #self.DBTYPE=xbmc.getInfoLabel("Container(1998).ListItem.DBTYPE")  
                        self.DBTYPE=xbmc.getInfoLabel("Container(1998).ListItem.Property(DbType)")  
                        #self.DBTYPE="actor"                     
                    else:
                        if not IconmixShowInfo:
                           self.LABEL8889 = xbmc.getInfoLabel("ListItem.Director").split(" (")[0]
                        else:
                           self.LABEL8889 = xbmc.getInfoLabel("Container(1990).ListItem.Director").split(" (")[0] 
                        self.DBTYPE="director"
                  else: 
                    self.LABEL8889=xbmc.getInfoLabel("ListItem.Label").split(" (")[0].decode("utf8")
                    self.DBTYPE=xbmc.getInfoLabel("ListItem.DBTYPE")
                  if not IconmixShowInfo:  
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
                      #InfoSup=utils.GetActeurInfo(utils.try_decode(self.LABEL8889),self.DBTYPE)
                      InfoSup=utils.GetActeurInfo(self.LABEL8889,self.DBTYPE)
                      #logMsg("Infosup (%s)(%s)(%s)" %(self.LABEL8889,self.DBTYPE,InfoSup))
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
                               if not IconmixShowInfo:
                                  xbmc.executebuiltin("SetFocus(55)")          
          
    #------------------------------------------------------------------------------------------------------------------
  def SetArtisteHomeVar(self,ArtisteData=None):
      if ArtisteData:
        self.windowhome.setProperty("ArtistBio",ArtisteData.get("ArtistBio"))
        self.windowhome.setProperty("ArtistThumb",ArtisteData.get("ArtistThumb"))
        self.windowhome.setProperty("ArtistLogo",ArtisteData.get("ArtistLogo"))
        self.windowhome.setProperty("ArtistBanner",ArtisteData.get("ArtistBanner"))
        self.windowhome.setProperty("ArtistFanart",ArtisteData.get("ArtistFanart"))
        self.windowhome.setProperty("ArtistFanart2",ArtisteData.get("ArtistFanart2"))
        self.windowhome.setProperty("ArtistFanart3",ArtisteData.get("ArtistFanart3")) 
        
    #------------------------------------------------------------------------------------------------------------------
  def CreateItemInfo(self,DbIdItem=None,TmdbNumber=None,ContainerID=None,DbType=None)  :
      InfoLabels=None
      if not ContainerID and DbType:        
        if "movie" in DbType:
           properties='"properties":["title","genre","year","rating","userrating","director","trailer","tagline","plot","plotoutline","originaltitle","lastplayed","playcount","writer","studio","mpaa","cast","country","imdbnumber","uniqueid","runtime","set","showlink","streamdetails","top250","votes","fanart","thumbnail","file","sorttitle","resume","setid","dateadded","tag","art"]'
           InfoLabels = utils.getJSON('VideoLibrary.GetMovieDetails', '{ "movieid":%d,%s}' %(int(DbIdItem),properties))
           logMsg("INFOS : %s" %InfoLabels)
        elif "tvshow" in DbType:
           properties='"properties":["title","genre","year","rating","userrating","plot","originaltitle","lastplayed","playcount","studio","mpaa","cast","imdbnumber","uniqueid","runtime","votes","fanart","thumbnail","file","sorttitle","dateadded","tag","art"]'
           InfoLabels = utils.getJSON('VideoLibrary.GetTvShowDetails', '{ "tvshowid":%d,%s}' %(int(DbIdItem),properties))
        elif "episode" in DbType:
           properties='"properties":["showtitle","title", "rating", "userrating", "director", "plot", "originaltitle", "lastplayed", "playcount", "writer", "cast", "uniqueid", "runtime", "streamdetails", "votes", "fanart", "thumbnail", "file", "resume", "dateadded", "art"]'           
           InfoLabels = utils.getJSON('VideoLibrary.GetEpisodeDetails', '{ "episodeid":%d,%s}' %(int(DbIdItem),properties))
        elif "album" in DbType:
           properties='"properties":["dateadded","genre","fanart","thumbnail","albumlabel","compilation","description","mood","playcount","releasetype","style","theme","type","artist","artistid","displayartist","genreid","musicbrainzalbumartistid","musicbrainzalbumid","rating","title","userrating","votes","year"]'           
           InfoLabels = utils.getJSON('AudioLibrary.GetAlbumDetails', '{ "albumid":%d,%s}' %(int(DbIdItem),properties))
           InfoLabels["file"]="musicdb://albums/"
        elif "artist" in DbType:
           properties='"properties":["born","compilationartist","description","died","disbanded","formed","instrument","isalbumartist","mood","musicbrainzartistid","roles","songgenres","style","yearsactive","genre","fanart","thumbnail"]'           
           InfoLabels = utils.getJSON('AudioLibrary.GetArtistDetails', '{ "artistid":%d,%s}' %(int(DbIdItem),properties))
           InfoLabels["file"]="musicdb://artists/"
        if InfoLabels:
          InfoLabels["path"]=InfoLabels.get("file")
      elif ContainerID:
        InfoLabels=utils.GetListItemInfoLabels(ContainerID)
        DbType=InfoLabels.get('dbtype')
        
      if DbType:
        DbType=DbType.replace("id","")
      if InfoLabels: # and InfoLabels.get("path"):
           
          Titre=InfoLabels.get("title")         
          Path=InfoLabels.get("file")
          IsMedia=None
          if Path:
           IsMedia="1" if len(os.path.splitext(Path)[1])>0 else None
          
          ItemListe = xbmcgui.ListItem(label=Titre,label2=IsMedia,path=Path)
          UniqueId=InfoLabels.get("uniqueid")
          if UniqueId:
            IMDBNumber=UniqueId.get("imdb")
            TMDBNumber=UniqueId.get("tmdb")
            ItemListe.setProperty('TMDBNumber', TMDBNumber)
            ItemListe.setProperty('IMDBNumber', IMDBNumber)
          else:
            ItemListe.setProperty('TMDBNumber', '')
            ItemListe.setProperty('IMDBNumber', '')
            
          #pistes audios
          streamdetails=InfoLabels.get("streamdetails")
          if streamdetails:
            audios=streamdetails.get("audio")
            i=1              
            for Item in audios:       
                # {"channels":6,"codec":"dca","language":"fre"}  
                Language=Item.get("language")
                Channel=Item.get("channels")
                Codec=Item.get("codec")
                if Language:
                   ItemListe.addStreamInfo('audio',{'codec':Codec,'language':Language,'channels':Channel}) 
                   ItemListe.setProperty("AudioCodec.%d" %(i),Codec)
                   ItemListe.setProperty("AudioChannels.%d" %(i),str(Channel))
                   ItemListe.setProperty("AudioLanguage.%d" %(i),Language)
                   #logMsg("Audiolanguage(%d) : %s" %(i,Language))
                   i=i+1
                else:
                  break
            #pistes vidéos   
            videos=streamdetails.get("video")
            ItemListe.addStreamInfo('video', videos)
           
            #sous-titres     
            subtitles=streamdetails.get("subtitle")
            i=1
            #[{"language":"fre"}]
            for item in subtitles:          
                Language=item.get("language")              
                if Language:
                  ItemListe.addStreamInfo('subtitle',{'language':Language}) 
                  ItemListe.setProperty("SubtitleLanguage.%d" %(i),Language)
                  i=i+1
                else:
                  break
                  
          Art=InfoLabels.get("art")                  
          if Art:
            poster=Art.get("poster")
            icon=InfoLabels.get("icon")             
            ItemListe.setProperty("poster",poster) 
            ItemListe.setArt(Art)
            ItemListe.setIconImage(icon) 
          
          
          if not "director" in DbType:
             logMsg("INFOSLABELS=%s" %InfoLabels)
             INFOS=utils.GetListItemInfoLabelsJson(InfoLabels)
             logMsg("INFOS=%s" %INFOS)
             INFOS["mediatype"]=DbType
             ItemListe.setInfo("video", INFOS)
             
             
             
          MyDirector=InfoLabels.get("director")
          Director=""
          try:
            for Item in MyDirector:
              Director=Director+','+Item
          except:
            Director=MyDirector
          if Director:
             Realisateur=utils.Remove_Separator(Director).split(" (")[0].decode("utf8")         
             self.windowhome.setProperty('IconMixDirector',utils.GetPhotoRealisateur('realisateurs',realisateur=Realisateur))
          else:
            self.windowhome.clearProperty('IconMixDirector')
          return (ItemListe) 
    
      logMsg("ItemListe erreur (%s)" %(InfoLabels))
      return None 
     
      
 
#------------------------------------------------------------------------------------------------------------------
  def GetControlW(Id=None,IdWindow=None):
      ControlId=None
      
      try:
        Window = xbmcgui.Window(IdWindow)
      except:
        Window=None
      if Window:
                    
          try:
               ControlId=Window.getControl(Id)  
          except:
               ControlId=None
      logMsg("ControlId %s" %(ControlId))
      return