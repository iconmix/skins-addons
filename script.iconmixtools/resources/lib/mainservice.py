# coding: utf-8
#from __future__ import unicode_literals
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
import os
import xbmc,xbmcgui,xbmcaddon,xbmcplugin,xbmcvfs
import random
import MonAutoCompletion
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





class myMonitor(xbmc.Monitor):
  
  def __init__(self):
    self.updatesetting()
    xbmc.Monitor.__init__(self)
    
  def updatesetting(self):
    self.ADDON = xbmcaddon.Addon()
    try:
     self.tempsannonce=int(self.ADDON.getSetting('tempsannonce'))
    except:
     self.tempsannonce=0 
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
  
  def onSettingsChanged(self):
    self.updatesetting()
    #logMsg("parametres changes ...: temps=%s,full=%s,first=%s,youtube=%s,annoncefilm=%s,annonceserie=%s" %(self.tempsannonce,self.annoncefull,self.allocinefirst,self.youtubeactif,self.annoncefilm,self.annonceserie),0)
    
  #def onNotification(self, sender, method, data):
  #      logMsg("sender (%s)(%s)" %(sender,method))
        #if not sender == 'script.module.youtube.dl':
        #    return
        #self.processCommand(method.split('.', 1)[-1], self.controller.processCommandData(data))  # Remove the "Other." prefix
   
class Player(xbmc.Player):

  def play(self, item='', listitem=None, windowed=False, sublist=None):
      super(Player, self).play(item, listitem, windowed)  
   

  def __init__(self):
      self.windowhome = xbmcgui.Window(10000)
      self.windowvideo = xbmcgui.Window(10025)
      self.DureeTotale=None
      self.PositionLecture=0
      self.ItemID=None      
      self.ItemType=None
      self.noterfilm=None
      self.noterserie=None
      self.currentepisode=None
      xbmc.Player.__init__(self,0)

  def onPlayBackStarted(self):   
      self.PreviousprogressPosition=None   
      self.PreviousprogressWindow=None  
      try:
        self.DureeTotale = int(self.getTotalTime())
      except:
        self.DureeTotale=None
      try:
        self.checkProgressPlay()
      except:
        A=None
          
   
  def Notation(self):
      Annonce=self.windowhome.getProperty('annonceencours')
      try:
        self.DureeLue=int(self.PositionLecture)
      except:
        self.DureeLue=0
      if self.DureeTotale and self.DureeLue:
          if ((self.DureeTotale-20)<=self.DureeLue):
            #logMsg("ARRET DE LECTURE (%s)(%s)(%s)(%s)(%s)(%s)(%s)" %(self.DureeLue,self.DureeTotale,Annonce,self.ItemID,self.ItemType,self.noterfilm,self.noterserie),0)
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

  def onPlayBackStopped(self):
      #logMsg("Arret de lecture")
      self.PreviousprogressPosition=None
      self.PreviousprogressWindow=None
      self.Notation()
      
      

  def onPlayBackEnded(self):
      #logMsg("FIN DE LECTURE",0)
      self.PreviousprogressPosition=None
      self.PreviousprogressWindow=None
      self.Notation()
      
  def onPlayBackSeekChapter(self):
      try:
        self.checkProgressPlay()
      except:
        A=None
      
class dialog_ShowInfo(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        self.windowhome = xbmcgui.Window(10000)
        xbmcgui.WindowXMLDialog.__init__(self)
        self.listitem = kwargs.get('listitem')
        self.acteurs = kwargs.get('acteurs')
        self.mainservice = kwargs.get('mainservice')
        self.IconmixShowInfo=self.windowhome.getProperty('IconmixShowInfo')
        

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
            image=self.listitem.getArt("icon")
          if not image: 
            image="DefaultThumb.png"
          self.getControl(2000).setImage(image, False)  
          
          extrafanart=xbmcgui.Window(10000).getProperty('IconMixExtraFanart')
          if not extrafanart:
            extrafanart=self.listitem.getArt("fanart")
            if extrafanart:
              xbmcgui.Window(10000).setProperty('IconMixExtraFanart',extrafanart)
          self.ListeActeurs=self.getControl(1998)
          if self.acteurs and self.ListeActeurs:
            self.ListeActeurs.reset()
            
            for item in self.acteurs:
              self.ListeActeurs.addItem(item)
          pays.ConversionPays("movie",1990)    
     
        else:
          self.close()

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
                  CompteurTemps=0
                  #if (not action in (1,2) and (F7779 or F7778)) or (not F7779 and not F7778):
                  KodiLocal=self.windowhome.getProperty('ActeurVideoLocal')
                  if (action.getId()==4 and (F7779 or F7778) and self.Local!=KodiLocal) or (action in (1,2) and F7781) or not self.Ajour:
                     self.mainservice.CheckActeursRoles(F8889, F7781, F7779,F7777,1)
                     self.Ajour=True                      
                     self.Local=KodiLocal
                  #logMsg("Action=(%s)-F8889:(%s)  F7781:(%s) F7779:(%s) F7777:(%s) F7778:(%s)- KodiLocal:(%s)" %(action.getId(),F8889, F7781,F7779,xbmc.getCondVisibility("Control.HasFocus(7777)"),xbmc.getCondVisibility("Control.HasFocus(7778)"),KodiLocal))
        #else: logMsg("Action (%s)" %(action.getId()))

    def onClick(self, controlID):
        if controlID == 6 or controlID == 3:             
            Trailer=None
        if controlID==600:
          self.close()
        if controlID==8: #play
          Path=xbmc.getInfoLabel("Container(1990).ListItem.FileNameandPath")
          if len(Path)>3:
             self.close()
             xbmc.Player().play(Path)
        if controlID==7777:
          #logMsg("affiche directeur !!!!")
          self.mainservice.CheckActeursRoles(False, False, False,True,1)
          self.Local=self.windowhome.getProperty('ActeurVideoLocal')
          #self.Ajour=None
             
            
                

    def onFocus(self, controlID):
        pass
"""
class dialog_ListeEpisodes(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)
        self.windowhome = xbmcgui.Window(10000)
        self.listing = kwargs.get('listing')
        self.Prochain = kwargs.get('Prochain')

    def onInit(self):
        self.img_list = self.getControl(2666)            

        if self.img_list:
          self.img_list.addItems(self.listing)
          logMsg("self.Prochain (%s)" %(self.Prochain))
          if self.Prochain:
            self.img_list.selectItem(self.Prochain)
          #for item in self.listing:           
          #    self.img_list.addItem(item)
          #self.setFocus(self.img_list)          
        else:
          self.close()

    def onAction(self, action):
      # Action : 3 haut
      #Action : 4 bas
      # Action : 2 droite
      # Action : 1 gauche  
      # 11 touche "info"   
      # 6 PageDown
      #5 PageUp
      #160 Fin
      #159 Home
      #7 entree
      actionId = action.getId()   
      if actionId==11 or actionId==1 or actionId in ACTION_PREVIOUS_MENU:  
          self.windowhome.clearProperty('IconmixFlagPanelEpisode')
          Chemin = self.img_list.getSelectedItem().getfilename()
          if len(Chemin)<=0:
            self.windowhome.setProperty('IconmixFlagPanelEpisode','0')
          self.close()
          return None
      else:  
          Pos= self.img_list.getSelectedPosition()
          if actionId==3:
            Pos=Pos-1
          if actionId==4:
            Pos=Pos+1
          if actionId==5:
            Pos=Pos-10
          if actionId==6:
            Pos=Pos+10
          if actionId==159:
            Pos=0
          if actionId==160:
            Pos=self.img_list.size()
          self.img_list.selectItem(Pos)
          if actionId==7:
            #LECTURE
            Chemin = self.img_list.getSelectedItem().getfilename()
            if len(Chemin)>1:
              titre=self.img_list.getSelectedItem().getLabel()
              logMsg("ListeEpisodes -> lecture (%s)(%s)" %(Chemin,titre))
              self.windowhome.setProperty('IconmixFlagPanelEpisode',titre)
              xbmc.Player().play(Chemin)
              self.close()             
              return True         
          
          logMsg("Liste Episodes Action (%s)" %(action.getId()))
"""          
            
          
class dialog_select_UI(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)
        self.listing = kwargs.get('listing')
        self.ListeTrailer = kwargs.get('trailers')
        self.ItemId = kwargs.get('ItemId')
        self.kodi_player = Player()

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

    def onAction(self, action):
      # Action : 3 haut
      #Action : 4 bas
      # Action : 2 droite
      # Action : 1 gauche  
      # 11 touche "info"      
      if action in ACTION_PREVIOUS_MENU:
          if self.kodi_player and self.kodi_player.isPlaying():
             self.kodi_player.stop()
             xbmc.executebuiltin("SetProperty(annonceencours,,home)")
          self.close()
      

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
                if SETTING("iconmixdebug")=="true":                      
                  logMsg("dialog_select_UI : Lecture (%s) (%s)" %(Trailer,self.Windowed))
                self.kodi_player.play(Trailer,listitem=Elements,windowed=self.Windowed)
                

    def onFocus(self, controlID):
        pass
        
class dialog_Notation(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        self.DBID = kwargs.get('dbid')
        self.ItemNotation = None
        self.ItemType=kwargs.get('TypeVideo')
        xbmcgui.WindowXMLDialog.__init__(self)
        
        
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
          
          try:
               json_result = utils.getJSON('VideoLibrary.Get%sDetails' %(self.ItemType), '{ "%sid":%s,"properties":["userrating"] }' %(self.ItemType.lower(),self.DBID))
          except:
               logMsg("VideoLibrary.Get%sDetails : %s impossible = " %(self.ItemType,self.DBID) ,0 )
               
          if json_result:
             try:
              self.ItemNotation=int(json_result.get("userrating"))
             except:
              self.ItemNotation=0
             
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

    def onAction(self, action):
      # Action : 3 haut
      #Action : 4 bas
      # Action : 2 droite
      # Action : 1 gauche        
      if action in ACTION_PREVIOUS_MENU:         
          self.close()
      #else:  logMsg("Action : %s" %(action.getId()),0)


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
           

    def onFocus(self, controlID):
        pass
        
class dialog_BandeAnnonce(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        self.PlayList = kwargs.get('PlayListItem')
        self.kodi_player = Player()
        xbmcgui.WindowXMLDialog.__init__(self) 
        self.Lecture()         
   
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
 
    
    def Lecture(self):       
      if self.kodi_player and self.PlayList:         
        self.kodi_player.play(self.PlayList, windowed=True, sublist=None)        
      else:
        xbmcgui.Window(10000).clearProperty('annonceencours')
        xbmcgui.Window(10000).clearProperty('IconMixTrailer')
        self.close()
 
        

def in_hours_and_min(minutes_string):
    try:
        full_minutes = int(minutes_string)
        minutes = full_minutes % 60
        hours   = full_minutes // 60
        return str(hours) + 'h' + str(minutes).zfill(2)
    except:
        return ''

class MainService:
  
    def __init__(self):         
      
      CompteurTemps=0
      
      TvSe="o"
      TvSh="o"
      
      self._init_vars()
      self._start_time = time.time()
      self.RandomTime=0
      self.Recherche=None
      self.AutoCompletionProvider=None
      self.windowhome.setProperty("AutoCompletionProvider",SETTING("autocomplete_provider"))
      self.ListeEpisodes=None
      
      
      
      logMsg('Version : %s - Chemin : %s - Service en cours..' %(ADDON_VERSION,ADDON_PATH),0)
      
      #xbmcgui.Dialog().notification('IconMixTools',"[COLOR=Yellow] Service en cours..[/COLOR]", ADDON_ICON,300) 
      
      while not self.kodimonitor.abortRequested(): # and xbmc.getCondVisibility("!String.IsEmpty(Window(home).Property(IconMixToolsbackend))"): 
          self.windowhome.clearProperty("IconMixToolsbackend")
          
          #-------------------------- 
          self.CheckListeVues()
                      
          #recherche
          self.AutoRecherche()
          #-------------------------- MUSIQUE EN LECTURE---------------------------------
          self.LectureMusique() 
              
          #-------------------------- #VUES MUSIQUES ------------------------------------------
          self.DetailsVuesMusique()
            
        
          #-------------------------- FILMS/SERIES/ACTEURS --------------------------
          self.ShowIconmixInfo()
          
          if not self.windowhome.getProperty('annonceencours')=="full" and (self.windowhome.getProperty('IconMixTrailer')!="1") and (self.windowhome.getProperty('IconmixShowInfo')=="1" or xbmc.getCondVisibility("Window.IsVisible(10025)") or xbmc.getCondVisibility("Window.IsVisible(12901)") or xbmc.getCondVisibility("Window.IsVisible(10142)") or xbmc.getCondVisibility("Window.IsVisible(12003)")) and not xbmc.getCondVisibility("Container.Scrolling") and not xbmc.getCondVisibility("Window.IsVisible(12000)"):
              
              MiseAjour=""
              TMDBNUMBER=None
              
              #if xbmc.getCondVisibility("Control.HasFocus(2998)"):
              # self.UpdateListeEpisodes()
              
              F8889=xbmc.getCondVisibility("Control.HasFocus(8889)")
              F7781=xbmc.getCondVisibility("Control.HasFocus(7781)")
              F7779=xbmc.getCondVisibility("Control.HasFocus(7779)") or xbmc.getCondVisibility("Control.HasFocus(5051)")
              F7777=xbmc.getCondVisibility("Control.HasFocus(7777)") or xbmc.getCondVisibility("Control.HasFocus(7778)")
             
              #-------------------------- ACTEURS : Roles/Bio---------------------------------
                  
              if F8889 | F7781 | F7779 |F7777:
                CompteurTemps=0
                self.CheckActeursRoles(F8889, F7781, F7779,F7777)                                
              #-------------------------- FILMS/SERIES ---------------------------------   
              else:
                  self.previousitem8889 = ""  
                  self.previousitemMusic = ""
                  
                      
                  if xbmc.getCondVisibility("Control.HasFocus(2999)"): #
                      CompteurTemps=0
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
                          """
                          selected=xbmc.getInfoLabel("ListItem.DBID")
                          xbmc.sleep(500)
                          selectedconfirm=xbmc.getInfoLabel("ListItem.DBID")
                          if selected==selectedconfirm:                            
                            self.selecteditem = selected
                            self.DBTYPE=xbmc.getInfoLabel("ListItem.DBTYPE")
                            self.previousitemPlayer=""
                            self.PlayerActiveID=None
                          """
                                                    
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
                             #logMsg("self.previousitem (%s) self.selecteditem (%s)" %(self.previousitem,self.selecteditem))
                             if self.kodi_player and self.kodi_player.isPlayingVideo() and self.windowhome.getProperty('annonceencours'):
                                self.kodi_player.stop()
                                self.windowhome.clearProperty('annonceencours')
                             if self.selecteditem!=self.windowhome.getProperty('BAprecedenteInf'):
                                self.windowhome.clearProperty('BAprecedenteInf')
                             #--------------------------------------
                             if SETTING("iconmixdebug")=="true":
                              logMsg("Accept (%s)" %(self.selecteditem))   
                             self.previousitem = self.selecteditem
                             CompteurTemps=0
                             self.PreviousBAnnonce=0
                             MiseAjour="1"
                             
                                                      
                             
                             if xbmc.getCondVisibility("Window.IsVisible(12901)"): #videoplayer <videoosd.xml>
                                MiseAjour="3"                              
                                self.previousitemPlayer = self.selecteditem
                                
                             if xbmc.getCondVisibility("Window.IsVisible(10142)") :#videoplayer <DialogFullScreenInfo.xml>
                                MiseAjour="4"
                                self.previousitemPlayer = self.selecteditem
                                 
                             if xbmc.getCondVisibility("Window.IsVisible(12003)") :#videoinfo
                                  MiseAjour="2" 
                                  
                             self.windowhome.clearProperty('IconMixUpdateSagas')
                             if self.previousitem != self.selecteditem or self.windowhome.getProperty('IconMixUpdateEpisodes')=='1':                    
                              self.precedenttvshow=None
                              self.windowhome.clearProperty('IconMixUpdateEpisodes')
                              logMsg("self.precedenttvshow=None1")
                             
                        else:                          
                            
                          #---------------------------- BANDE ANNONCE AUTOMATIQUE-------------------------------------
                         self.BandeAnnonceAutomatique()
                               
                              
                          
                                          
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
                      if self.DBTYPE!="tvshow" and self.DBTYPE!="episode":
                          utils.ClearNextEpisode() 
                      
                      #ACTEURS ELEMENT DE SAGA ------------------------------------------------ 
                      if xbmc.getCondVisibility("Control.HasFocus(2999)"):
                          if self.selecteditem > -1 and not str(self.selecteditem)=="":                          
                            if self.DBTYPEOK:
                                  ListeActeurs=self.GetControl(self.windowvideonav,1998)
                                 
                                                                  
                                  if ListeActeurs:
                                    ListeItemx=utils.getCasting(self.DBTYPE,self.selecteditem,1,TMDBNUMBER)
                                    ListeActeurs.reset()
                                    if ListeItemx:
                                         for itemX in ListeItemx:
                                              ListeActeurs.addItem(itemX)                                                               
                                    
                                  
                                  extrafanart=utils.CheckItemExtrafanartPath(xbmc.getInfoLabel("Container(1999).ListItem.Path"))
                              
                                  self.windowhome.setProperty('IconMixExtraFanart',extrafanart)   
                                  self.duration = xbmc.getInfoLabel("Container(1999).ListItem.Duration") 
                                  self.display_duration()
                      
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
                            
                            if MiseAjour=="1":
                               #ACTEURS VIDEONAV
                               ListeActeurs=self.GetControl(self.windowvideonav,1998)
                               
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
                                   
                                   self.Episodes=utils.getallnextepisodes(self.selecteditem,None,self.DBTYPE)
                                   #ListeDiffusion.addItems(Episodes)
                                   if self.Episodes:
                                      self.ListeDiffusion.addItems(self.Episodes)
                                      #self.ListeDiffusion.setStaticContent(self.Episodes)
                                   else:
                                      self.Episodes=[]
                                      #self.ListeDiffusion.setStaticContent(self.Episodes)
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
                                     if SETTING("iconmixdebug")=="true":
                                       logMsg("utils.GetPhotoRealisateur('realisateurs',realisateur=(%s)) " %(Realisateur))
                          
                                     self.windowhome.setProperty('IconMixDirector',utils.GetPhotoRealisateur('realisateurs',realisateur=Realisateur))                                                                        
                                   ResetDirector=False
                              
                                
                            #FENETRE MYVIDEONAV (10025) ------------------------------------------------
                            #if not xbmc.getCondVisibility("Window.IsVisible(12901)") and not xbmc.getCondVisibility("Window.IsVisible(12005)") and not xbmc.getCondVisibility("Window.IsVisible(10142)") : #pas en lecture visible
                            if xbmc.getCondVisibility("Window.IsVisible(10025)"):
                              
                                #mise à jour saga (videonav ou videoinfo)
                                if (self.DBTYPE=="set" or MiseAjour=="2") : 
                                  if not MiseAjour=="2":
                                     ListeSaga=self.GetControl(self.windowvideonav,1999)
                                     ListeFanarts=self.GetControl(self.windowvideonav,5555)  
                                     SetID=self.selecteditem
                                  else:
                                     ListeSaga=self.GetControl(self.windowvideoinf,1999)
                                     ListeFanarts=None
                                     SetID=xbmc.getInfoLabel("ListItem.SetId")
                                     
                                  if ListeSaga and SetID:
                                    
                                    NbItems=ListeSaga.size()
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
                                  
                                if self.DBTYPEOK or self.DBTYPE=="tvshow":
                                   #if self.DBTYPE=="episode" or self.DBTYPE=="tvshow":
                                   #  utils.getnextepisode(self.selecteditem,None,self.DBTYPE)  
                                   
                                   self.windowhome.setProperty('IconMixExtraFanart',utils.CheckItemExtrafanartPath(xbmc.getInfoLabel("ListItem.Path")))
                                   if self.DBTYPE!="tvshow":       
                                     self.duration = xbmc.getInfoLabel("ListItem.Duration") 
                                     self.display_duration()
                                   else:
                                      self.TvSeason=""
                                      if self.selecteditem!=self.precedenttvshow:
                                        
                                        #-------------------------- affichage des episodes de la série ------------------
                                        #--- modif --

                                        if SETTING("iconmixdebug")=="true":
                                          logMsg("UpdateListeEpisodes Actuelle(%s) Precedente(%s)" %(self.selecteditem,self.precedenttvshow)) 
                                        #utils.getepisodes(self.selecteditem,None,self.DBTYPE)
                                        if not xbmc.getCondVisibility("Skin.HasSetting(DisableTvList)"):
                                          self.UpdateListeEpisodes()
                                          utils.getnextepisode(self.selecteditem,None,self.DBTYPE) 
                                        else :
                                          utils.getepisodes(self.selecteditem,None,self.DBTYPE)  
                                        """
                                        if not xbmc.getCondVisibility("Skin.HasSetting(DisableTvList)"):
                                          self.ListeEpisodes,self.Prochain =utils.GetEpisodesKodi(self.selecteditem,True)
                                        
                                        else:
                                          utils.getepisodes(self.selecteditem,None,self.DBTYPE)  
                                        """
                                        #-----
                                    #ListItem.PlayCount
                                    #--------------------------------------------------------------------------------
                                   
                                     
                                if self.DBTYPE=="episode" and xbmc.getCondVisibility("Skin.HasSetting(CheckSeries)"):
                                     TvSh=xbmc.getInfoLabel("ListItem.TVShowTitle") 
                                     TvSe=xbmc.getInfoLabel("ListItem.Season")
                                     TvId=self.selecteditem                                       
                                     if TvId and TvSe and TvSh:
                                       if TvSe!=self.TvSeason or TvSh!=self.TvShow : 
                                         self.windowhome.clearProperty('IconMixTv')
                                         self.windowhome.clearProperty('IconMixTvKodi')        
                                         self.EpSa,self.EpSaKodi,Poster=utils.getepisodes(int(TvId),int(TvSe),self.DBTYPE)                                           
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
                                self.duration = xbmc.getInfoLabel("ListItem.Duration") 
                                self.display_duration()
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
            if self.kodi_player:
              #arret si lecture mais fenetre VideoNav pas visible
              if self.kodi_player.isPlayingVideo() and not xbmc.getCondVisibility("Window.IsVisible(10025)") and self.windowhome.getProperty('annonceencours')!="":
                if not xbmc.getCondVisibility("Window.IsActive(12005)"): 
                   self.kodi_player.stop()                   
                   self.windowhome.clearProperty('annonceencours')
                   
          #arret si lecture en plein écran mais fenetre videofullscreen pas visible
          if  self.kodi_player.isPlayingVideo() and not xbmc.getCondVisibility("Window.IsActive(12005)")  and self.windowhome.getProperty('annonceencours')=="full":
                 xbmc.sleep(2000)
                 if not xbmc.getCondVisibility("Window.IsActive(12005)"):
                   CompteurTemps=0 
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
             CompteurTemps=CompteurTemps+400              
          else:
             CompteurTemps=0
             if xbmc.getCondVisibility("Window.IsVisible(12901)") or  xbmc.getCondVisibility("Window.IsVisible(12005)") or  xbmc.getCondVisibility("Window.IsVisible(10142)"):
               #self.precedenttvshow=None
               #logMsg("self.precedenttvshow=None2")
               self.windowhome.clearProperty('IconmixProchainEpisode') 
          if xbmc.getCondVisibility("Window.IsActive(10000)"):
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
          
          self.windowhome.setProperty("IconMixToolsbackend","en cours")
          xbmc.sleep(400)
            
      logMsg('Arret en cours...', 0)
      
      del self.kodi_player
      del self.kodimonitor
      self.windowhome.clearProperty("IconMixToolsbackend")
      """
      try:
        os.remove(ADDON_DATA_PATH+"/series/planningnext")
      except:
        logMsg("impossible de supprimer %s" %(ADDON_DATA_PATH+"/series/planningnext"))
      """
      try:
        #le purgatoire !!!
        os.remove(ADDON_PATH+"/resources/lib/utils.pyo")
        os.remove(ADDON_PATH+"/resources/lib/MonAutoCompletion.pyo")
        os.remove(ADDON_PATH+"/resources/lib/xml2json.pyo")
        os.remove(ADDON_PATH+"/resources/lib/mainservice.pyo")
        os.remove(ADDON_PATH+"/resources/lib/pays.pyo")
        os.remove(ADDON_PATH+"/resources/lib/__init__.pyo")
        logMsg("Purgatoire fini !!!")
      except:
        logMsg("impossible de supprimer %s" %(ADDON_PATH+"/resources/lib/*.pyo"))
      
      logMsg("Astalavista baby ;)")  
    """  
    def UpdateListeEpisodesTEST(self):
        if not self.ListeEpisodes:
         self.ListeEpisodes,self.Prochain =utils.GetEpisodesKodi(self.selecteditem,True)
        if self.ListeEpisodes:
          self.windowhome.setProperty('IconmixProchainEpisode',str(self.Prochain))
          self.dialog_ListeEpisodes = dialog_ListeEpisodes('listeepisodes.xml', ADDON_PATH, 'default','1080i',listing=self.ListeEpisodes,Prochain=self.Prochain)
          ret=self.dialog_ListeEpisodes.doModal()
          del self.dialog_ListeEpisodes  
          if not ret:
            xbmc.executebuiltin("SetFocus(55)")                        
    """
      
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
              self.ListeItemx,self.Prochain =utils.GetEpisodesKodi(self.selecteditem,True)                                              
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
              #self.ListeEpisodes.setStaticContent([])
      else:
        logMsg("xbmc.Window(10025) vide")      
    
    
    def CheckListeVues(self):
      try:
        CurrentWindow=xbmcgui.getCurrentWindowId()
      except:
        CurrentWindow=None
        self.previousContentListeVues=None
        self.previousWindowListeVues=None
      if self.previousWindowListeVues!=CurrentWindow:
        #la fenetre n'est plus la même ...on recharge la liste des vues....
        self.previousWindowListeVues=CurrentWindow
        self.previousContentListeVues=None
        #mise à jour des listes de vues
        if xbmc.getCondVisibility("Control.IsVisible(7000)"):
          #si le menu général est visible
          ContentListeVues=xbmc.getInfoLabel("Container.FolderPath")
          if self.previousContentListeVues!=ContentListeVues:
             #logMsg("listedevuesContent !!(%s)!!" %(self.previousContentListeVues))            
             
             try:
              CurrentWindow=xbmcgui.getCurrentWindowId()
             except:
              CurrentWindow=None
              self.previousContentListeVues=None
             try:
              CurrentWindow=xbmcgui.Window(CurrentWindow)
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
                 current_view = xbmc.getInfoLabel("Container.Viewmode").decode("utf-8")
                  
                 ListeVues=utils.ModeVuesMenu(content_type, current_view)
                 if ListeVues:
                    #logMsg("listedevues OK !!(%s)(%s)(%s)!!" %(content_type,current_view,ListeVues))
                    ControlList.addItems(ListeVues)
    
    def LectureMusique(self):
      if xbmc.getCondVisibility("Player.HasAudio"):
        CompteurTemps=0
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
    
    def DetailsVuesMusique(self):
       if xbmc.getCondVisibility("Window.IsVisible(10502)"):
          CompteurTemps=0
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
                                     ItemListe.setProperty("fanart",Item)
                                     TabFanarts.append(ItemListe)
                              ListeFanarts.addItems(TabFanarts) 
                      self.SetArtisteHomeVar(ArtisteData)  
               except:
                   logMsg("Probleme : AlbumData,ArtisteData=utils.GetMusicFicheAlbum(self.selecteditemMusic,Cover,None)",0)  
                   
    def ShowIconmixInfo(self):
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
              Acteur.setIconImage(Photo)
              Acteur.setProperty("DbType",dbtypeinfo)
              #Acteur=self.CreationItemInfo(None,None,55)
              if Acteur:
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
        
        ItemListe=self.CreationItemInfo(DBKODI ,TMDBNUMBER,ContainerID )           
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
              self.display_duration(ContainerID)
              self.ui = dialog_ShowInfo('madialogvideoInfo.xml', ADDON_PATH, 'default','1080i',listitem=ItemListe,acteurs=ListeActeursInf,mainservice=self)
              ret=self.ui.doModal()
              del self.ui                          
        self.windowhome.clearProperty('IconmixShowInfo')
        xbmc.executebuiltin("SetFocus(%d)" %(ContainerID))
    
    def AutoRecherche(self):
      if xbmc.getCondVisibility("Control.IsVisible(9010)") and xbmc.getCondVisibility("Control.IsVisible(312)"):
        if self.windowhome.getProperty("AutoCompletionShowItem"):
          path=self.windowhome.getProperty("AutoCompletionShowItem")
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
          else:
            if SETTING("iconmixdebug")=="true":
              logMsg("fuck showitem (%s)(%s)" %(path,xbmc.getInfoLabel("Container(9010).ListItem.property(ItemID)")))
            try:
             path=path.lower()
             dbid=int(xbmc.getInfoLabel("Container(9010).ListItem.property(ItemID)")) if not "addon" in path else 1
             
            except:
              logMsg("fuck showitem (%s)(%s)" %(path,xbmc.getInfoLabel("Container(9010).ListItem.property(ItemID)"))) 
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
                  
                if ActuelNbItems:   
                  cpt=1
                  ItemFocus=0
                  while cpt<=ActuelNbItems:
                    try:
                      ITEMDBID=int(xbmc.getInfoLabel("Container.ListItemAbsolute(%d).DBID" %(cpt)) )
                    except:
                      ITEMDBID=None
                    if ITEMDBID==dbid:
                      ItemFocus=cpt
                      break 
                    cpt=cpt+1
                  xbmc.executebuiltin("Action(FirstPage)")
                  xbmc.executebuiltin("Control.SetFocus(%d,%d)" %(currentlistid,ItemFocus))
            elif "addon:" in path:
              path=path.replace("addon:","")
              Action=""                  
              self.start_info_actions("selectautocomplete", path)
              xbmc.executebuiltin('SendClick(,300)')
              
                 
          
          self.windowhome.clearProperty("AutoCompletionShowItem")
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
                   
    def BandeAnnonceAutomatique(self):
       if int(self.kodimonitor.tempsannonce)>0 and xbmc.getCondVisibility("Window.IsActive(10025)") and not xbmc.getCondVisibility("Window.IsActive(12003)") and not xbmc.getCondVisibility("System.HasModalDialog"):
          self.PreviousBAnnonce=self.windowhome.getProperty('BAprecedenteInf')
          
          LeType=xbmc.getInfoLabel("ListItem.DBTYPE")
          #logMsg("CompteurTemps: %s self.tempsannonce: %s -%s" %(CompteurTemps,self.tempsannonce,LeType),0)
          if CompteurTemps>(int(self.kodimonitor.tempsannonce)*1000) and not xbmc.Player().isPlaying() and ((LeType=="movie" and self.kodimonitor.annoncefilm=="true") or (LeType=="tvshow" and self.kodimonitor.annonceserie=="true")) and self.PreviousBAnnonce!=self.selecteditem :
            #logMsg("Annonce (%s)(%s)(%s)" %(LeType,self.kodimonitor.annoncefilm,self.kodimonitor.annonceserie),0) 
            if self.buttonFullScreen:
                   del self.buttonFullScreen
                   self.buttonFullScreen=None
            AllocineBA=None
            ListeTrailer=[]
            CompteurTemps=0
            #start_time = time.time()
            self.PreviousBAnnonce=self.selecteditem
            xbmc.executebuiltin("SetProperty(BAprecedenteInf,%s,home)" %(self.selecteditem))
            #-------- KODI --------
            KodiTrailer=xbmc.getInfoLabel("ListItem.Trailer")
            if KodiTrailer:
              try:
                #KodiTrailer=KodiTrailer.split("videoid=")[1]
                if "youtube" in KodiTrailer:
                   Origine="youtube"
                else:
                   Origine=""
                KodiTrailer=KodiTrailer.replace("plugin://plugin.video.youtube/?action=play_video&videoid=","plugin://plugin.video.youtube/play/?video_id=")
                ListeTrailer.insert(0,{"id":KodiTrailer,"position":"0","iso_639_1":"","iso_3166_1":"","key":Origine,"name":"ooo","site":"YouTube","size":"","type":"","landscape":""})     
              except:
                KodiTrailer=None
                
            
            
            
            #-------- ALLOCINE --------
            if self.kodimonitor.allocineactif=="true" and (not KodiTrailer or self.kodimonitor.allocinefirst or self.kodimonitor.annoncetoutes=="true"):
              Annee=xbmc.getInfoLabel("ListItem.Year")
              if LeType=="movie":
                AllocineBA=utils.Allocine_BandeAnnonce(xbmc.getInfoLabel("ListItem.Label").lower(),LeType,None,None,Annee)
              else:
                Episode=None                                  
                if LeType=="tvshow":
                  Saison=None                                                              
                  AllocineBA=utils.Allocine_BandeAnnonce(xbmc.getInfoLabel("ListItem.TVShowTitle").lower(),LeType,Saison,Episode,Annee)
              if AllocineBA:
                 cpt=len(AllocineBA)-1
                 while cpt>=0:                                  
                   ListeTrailer.insert(0,AllocineBA[cpt])  
                   cpt=cpt-1
                   
                 #logMsg("BA Allocine (%s)" %(AllocineBA[0]),0)                                   
              #interval = time.time() - start_time 
              #logMsg("Allcoine duree de la recherche (%s)" %(str(interval)),0) 
              
            #-------- YOUTUBE chez TMDB--------
            if not AllocineBA or self.kodimonitor.annoncetoutes=="true":
              #youtube 
              TMDBID=''
              IMDBNUMBER=xbmc.getInfoLabel("ListItem.IMDBNumber")
              TMDBID=utils.get_externalID(IMDBNUMBER,LeType)                                              
              if TMDBID!='' :                    
                  TMDBTrailer=utils.getTrailer(TMDBID,LeType)
                  if TMDBTrailer: 
                    cpt=len(TMDBTrailer)-1
                    while cpt>=0:                                  
                       ListeTrailer.append(TMDBTrailer[cpt])  
                       cpt=cpt-1
                    #ListeTrailer.insert(0,TMDBTrailer[0])
                    #logMsg("BA TMDB (%s)" %(TMDBTrailer[0]),0)                                                                                                     
            
            #interval = time.time() - start_time 
            #logMsg("duree de la recherche (%s)" %(str(interval)),0) 
            if ListeTrailer:
              PlayListBA=xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
              PlayListBA.clear()
              if self.kodimonitor.annoncetoutes=="false":
                 ListeTrailer=[ListeTrailer[0]]  
              #logMsg("Trailers (%s) : %s" %(len(ListeTrailer),ListeTrailer),0)  
              ListeId=[]                           
              for Item in ListeTrailer:  
                 if not  Item["id"] in ListeId:                               
                   Elements = xbmcgui.ListItem(label=utils.try_decode(Item.get("name"))+" ["+utils.try_decode(Item.get("type"))+" - "+str(Item.get("size"))+"p - "+utils.try_decode(Item.get("iso_3166_1"))+"]")
                   Elements.setInfo("video", {"title": utils.try_decode(Item.get("name"))+" ("+utils.try_decode(Item.get("type"))+" - "+str(Item.get("size"))+"p - "+utils.try_decode(Item.get("iso_3166_1"))+") ","mediatype": "movie"})
                   Elements.setArt({"poster":Item["landscape"]})
                   PlayListBA.add(Item["id"],Elements) 
                   ListeId.append(Item["id"])
                                               
              
              if not self.kodimonitor.annoncefull or self.kodimonitor.annoncefull=="false":
                self.ui = dialog_BandeAnnonce('annonce.xml', ADDON_PATH, 'default','1080i',PlayListItem=PlayListBA)                          
                self.ui.doModal()
                del self.ui
                del PlayListBA
                self.windowhome.clearProperty('annonceencours')
              else:
                self.windowhome.setProperty('annonceencours','full')
                if self.kodi_player:                              
                 self.kodi_player.play(PlayListBA,windowed=False)                                
                                 
        
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
           

    def display_duration(self,ContainerID=None):
       
        xxx="null"
        
        #self.windowhome.setProperty('ItemUniqueGenre',xbmc.getInfoLabel( "ListItem.Genre" ).replace(" /",", "))
        
        if self.DBTYPE=="movie":
          pays.ConversionPays("movie",ContainerID)
       
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
      self.previousProchainID=None
      self.previousitem8889 = ""
      self.previousitem1998 = ""
      self.previousLABEL1999 = ""
      self.previousitem1998local = ""
      self.previousitemMusic = ""
      self.previousitemPlayer= ""
      self.previousContentListeVues= ""
      self.previousWindowListeVues=""
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
      #query_url="https://api.betaseries.com/planning/general?key=46be59b5b866&before=1"
      """
      try:
        os.remove(ADDON_DATA_PATH+"/series/planningnext")
      except:
        logMsg("impossible de supprimer %s" %(ADDON_DATA_PATH+"/series/planningnext"))
      
      if not xbmc.getCondVisibility("Skin.HasSetting(DisableTvList)") and not xbmcvfs.exists(ADDON_DATA_PATH+"/series/planningnext"):
         utils.updategetnextepisode()
      """     
        
    def GetControl(self,Window=None,Id=None):
      ControlId=None
      
      if Window:
                    
          try:
               ControlId=Window.getControl(Id)  
          except:
               ControlId=None
      return ControlId
      
    
    
    
          
    def CheckActeursRoles(self,F8889=None, F7781=None, F7779=None,F7777=None,IconmixShowInfo=None,ActeurRealisateur="acteurs"):
      #7779 : roles
      #7781 : acteurs
      #8889 : bio
      #7777 : director (dialogvideoinf)
      #logMsg("CheckActeursRoles (%s) : F8889 (%s) ,  F7781 (%s) ,  F7779 (%s) , F7777 (%s)" %(xbmc.getInfoLabel("Container(1998).ListItem.Label"),F8889 , F7781 , F7779 ,F7777))
      ListeRole=None
      if F8889 | F7781 | F7779 |F7777:
          CompteurTemps=0
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
          
    def SetArtisteHomeVar(self,ArtisteData=None):
      if ArtisteData:
        self.windowhome.setProperty("ArtistBio",ArtisteData.get("ArtistBio"))
        self.windowhome.setProperty("ArtistThumb",ArtisteData.get("ArtistThumb"))
        self.windowhome.setProperty("ArtistLogo",ArtisteData.get("ArtistLogo"))
        self.windowhome.setProperty("ArtistBanner",ArtisteData.get("ArtistBanner"))
        self.windowhome.setProperty("ArtistFanart",ArtisteData.get("ArtistFanart"))
        self.windowhome.setProperty("ArtistFanart2",ArtisteData.get("ArtistFanart2"))
        self.windowhome.setProperty("ArtistFanart3",ArtisteData.get("ArtistFanart3")) 
        
    def CreationItemInfo(self,DbIdItem=None,TmdbNumber=None,ContainerID=None)  :
      if ContainerID:
        InfoLabels=utils.GetListItemInfoLabels(ContainerID)
        
        if InfoLabels:
            Titre=xbmc.getInfoLabel("Container(%d).ListItem.Label" %(ContainerID))
            Path=xbmc.getInfoLabel("Container(%d).ListItem.FileNameAndPath"%(ContainerID))
            ItemListe = xbmcgui.ListItem(label=Titre,path=Path)
            IMDBNumber=xbmc.getInfoLabel("Container(%d).ListItem.IMDBNumber"%(ContainerID))
            TMDBNumber=xbmc.getInfoLabel("Container(%d).ListItem.Property(TMDBNumber)"%(ContainerID))
            
            #pistes audios
            for i in range(1,4):          
                Language=xbmc.getInfoLabel("Container(%d).ListItem.Property(AudioLanguage.%d)" %(ContainerID,i))
                Channel=xbmc.getInfoLabel("Container(%d).ListItem.Property(AudioChannels.%d)" %(ContainerID,i))
                Codec=xbmc.getInfoLabel("Container(%d).ListItem.Property(AudioCodec.%d)" %(ContainerID,i)) 
                if Language:
                   ItemListe.addStreamInfo('audio',{'codec':Codec,'language':Language,'channels':Channel}) 
                   ItemListe.setProperty("AudioCodec.%d" %(i),Codec)
                   ItemListe.setProperty("AudioChannels.%d" %(i),Channel)
                   ItemListe.setProperty("AudioLanguage.%d" %(i),Language)
                else:
                  break
            #pistes vidéos   
            infovideo={ 'codec': xbmc.getInfoLabel("Container(%d).ListItem.VideoCodec"%(ContainerID)), 'height' : xbmc.getInfoLabel("Container(%d).ListItem.VideoResolution"%(ContainerID)),'aspect':xbmc.getInfoLabel("Container(%d).ListItem.VideoAspect"%(ContainerID)),'duration': xbmc.getInfoLabel("Container(%d).ListItem.Duration"%(ContainerID))}
            ItemListe.addStreamInfo('video', infovideo)
            #ConversionPays(DBTYPE=None,ContainerID=None)
            #sous-titres     
            for i in range(1,4):          
                Language=xbmc.getInfoLabel("Container(%d).ListItem.Property(SubtitleLanguage.%d)" %(ContainerID,i))              
                if Language:
                  ItemListe.addStreamInfo('subtitle',{'language':Language}) 
                  ItemListe.setProperty("SubtitleLanguage.%d" %(i),Language)
                else:
                  break                  
            thumb=xbmc.getInfoLabel("Container(%d).ListItem.Art(thumb)"%(ContainerID))
            poster=xbmc.getInfoLabel("Container(%d).ListItem.Art(poster)"%(ContainerID))
            banner=xbmc.getInfoLabel("Container(%d).ListItem.Art(banner)"%(ContainerID))
            fanart=xbmc.getInfoLabel("Container(%d).ListItem.Art(fanart)"%(ContainerID))
            clearart=xbmc.getInfoLabel("Container(%d).ListItem.Art(clearart)"%(ContainerID))
            clearlogo=xbmc.getInfoLabel("Container(%d).ListItem.Art(clearlogo)"%(ContainerID))
            landscape=xbmc.getInfoLabel("Container(%d).ListItem.Art(landscape)"%(ContainerID))
            icon=xbmc.getInfoLabel("Container(%d).ListItem.Art(icon)"%(ContainerID))             
            ItemListe.setProperty("poster",poster) 
            ItemListe.setProperty('TMDBNumber', TMDBNumber)
            ItemListe.setProperty('IMDBNumber', IMDBNumber)
            ItemListe.setArt({'thumb':thumb,'poster':poster,'banner':fanart,'fanart':fanart,'clearart':clearart,'clearlogo':clearlogo,'landscape':landscape,'icon':icon})
            ItemListe.setIconImage(icon) 
            if xbmc.getInfoLabel("Container(%d).ListItem.DBType" %(ContainerID))!="director":
               ItemListe.setInfo("video", InfoLabels)
            
            Realisateur=utils.Remove_Separator(xbmc.getInfoLabel("Container(%d).ListItem.Director"%(ContainerID)).split(" (")[0].decode("utf8"))

            #self.windowhome.setProperty('IconMixDirector',str(utils.GetPhotoRealisateur('realisateurs',realisateur=Realisateur)))
            self.windowhome.setProperty('IconMixDirector',utils.GetPhotoRealisateur('realisateurs',realisateur=Realisateur))
            return (ItemListe) 
      
        logMsg("ItemListe erreur (%s)" %(InfoLabels))
      return None 
      
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
           
            MyEdit.setText(id)
            
            return None
            # xbmc.executebuiltin("SendClick(103,32)")
        
        
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
      

    def pass_list_to_skin(self,data=[],  limit=False,basetype=None,provider=None):
      
      
        
        items=[]
        if data and limit and int(limit) < len(data) and not provider =="kodi":
            data = data[:int(limit)]
        
        
        items = self.create_listitems(data,basetype)
        #items = [(i.getProperty("path"), i, bool(i.getProperty("directory"))) for i in items]
        self.resetPropositions(items)
            
            


    def create_listitems(self,data=None,basetype=None):
        if not data:
            return []
        itemlist = []
        for (count, result) in enumerate(data):
            listitem = xbmcgui.ListItem('%s' % (str(count)))
            for (key, value) in result.iteritems():
                if not value:
                    continue
                value = unicode(value)
                if key.lower() in ["label"]:
                    listitem.setLabel(value)
                elif key.lower() in ["search_string"]:                
                    path = "plugin://script.iconmixtools/?action=selectautocomplete&id=%s" % value
                    listitem.setPath(path=path)
                    listitem.setProperty('path', path)
                elif key.lower() in ["path"]:
                    listitem.setPath(path=value)
                    listitem.setProperty('path', value)
                elif key.lower() in ["dbid"]:                
                    listitem.setProperty('ItemID', value)
                elif key.lower() in ["dbtype"]:                
                    listitem.setProperty('dbtype', value)
                elif key.lower() in ["winid"]:                
                    listitem.setProperty('winid', str(value))
                    
                elif key.lower() in ["icon"]:                
                    listitem.setIconImage(value)
            listitem.setProperty("index", str(count))
            itemlist.append(listitem)
        return itemlist


    def resolve_url(self,handle):
        if handle:
            xbmcplugin.setResolvedUrl(handle=int(handle),
                                      succeeded=False,
                                      listitem=xbmcgui.ListItem())           
 #-----------------------------------------------
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
      return ControlId