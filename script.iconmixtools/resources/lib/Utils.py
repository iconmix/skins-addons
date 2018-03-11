#!/usr/bin/python
# coding: utf-8
#from __future__ import unicode_literals
import xbmcplugin, xbmcgui, xbmc, xbmcaddon, xbmcvfs
import os,sys,io,shutil
import urllib2, urllib
import httplib
import datetime
from unidecode import unidecode

import _strptime
import time
import unicodedata
import urlparse
from xml.dom.minidom import parse
import json
import resources.lib.xml2json as xml2json
import sqlite3
import operator
import locale
import hashlib
import base64
import xml.etree.ElementTree as ET
from platform import machine
import re

    
try:
    to_unicode = unicode
except NameError:
    to_unicode = str
    
Allocinepartner_key  = '100043982026'  

ADDON = xbmcaddon.Addon()
__addonid__    = ADDON.getAddonInfo('id')
__version__    = ADDON.getAddonInfo('version')
__language__   = ADDON.getLocalizedString
__cwd__        = xbmc.translatePath(ADDON.getAddonInfo('path')).decode('utf-8')   
ADDON_ID = ADDON.getAddonInfo('id').decode("utf8")
ADDON_ICON = ADDON.getAddonInfo('icon').decode("utf8")
ADDON_NAME = ADDON.getAddonInfo('name').decode("utf8")
ADDON_PATH = ADDON.getAddonInfo('path').decode("utf8")
ADDON_VERSION = ADDON.getAddonInfo('version').decode("utf8")
ADDON_DATA_PATH = xbmc.translatePath("special://profile/addon_data/%s" % ADDON_ID).decode("utf8")
KODI_VERSION  = int(xbmc.getInfoLabel( "System.BuildVersion" ).split(".")[0])
WINDOW = xbmcgui.Window(10000)
SETTING = ADDON.getSetting
KODILANGUAGE = xbmc.getInfoLabel( "System.Language" )
KODILANGCODE = xbmc.getLanguage(xbmc.ISO_639_1).lower()
TMDBApiKey="67158e2af1624020e34fd893c881b019"
#ACTION_PREVIOUS_MENU = (9, 10, 92, 216, 247, 257, 275, 61467, 61448)
ACTION_PREVIOUS_MENU = (9, 10, 92)
ListePays={"?":"Inconnu","AF":"Afghanistan","AL":"Albania","DZ":"Algeria","AS":"American Samoa","AD":"Andorra","AO":"Angola","AI":"Anguilla","AQ":"Antarctica","AG":"Antigua and Barbuda","AR":"Argentina","AM":"Armenia","AW":"Aruba","AU":"Australia","AT":"Austria","AZ":"Azerbaijan","BS":"Bahamas","BH":"Bahrain","BD":"Bangladesh","BB":"Barbados","BY":"Belarus",
"BE":"Belgium","BZ":"Belize","BJ":"Benin","BM":"Bermuda","BT":"Bhutan","BO":"Bolivia, Plurinational State of","BA":"Bosnia and Herzegovina","BW":"Botswana","BV":"Bouvet Island","BR":"Brazil","IO":"British Indian Ocean Territory","BN":"Brunei Darussalam","BG":"Bulgaria","BF":"Burkina Faso","BI":"Burundi","KH":"Cambodia","CM":"Cameroon","CA":"Canada","CV":"Cape Verde","KY":"Cayman Islands","CF":"Central African Republic","TD":"Chad",
"CL":"Chile","CN":"China","CX":"Christmas Island","CC":"Cocos (Keeling) Islands","CO":"Colombia","KM":"Comoros","CG":"Congo","CD":"Congo, the Democratic Republic of the","CK":"Cook Islands","CR":"Costa Rica","CI":"Côte d'Ivoire","HR":"Croatia","CU":"Cuba","CY":"Cyprus","CZ":"Czech Republic","DK":"Denmark","DJ":"Djibouti","DM":"Dominica","DO":"Dominican Republic","EC":"Ecuador","EG":"Egypt","SV":"El Salvador","GQ":"Equatorial Guinea","ER":"Eritrea","EE":"Estonia","ET":"Ethiopia","FK":"Falkland Islands (Malvinas)","FO":"Faroe Islands","FJ":"Fiji","FI":"Finland","FR":"France",
"GF":"French Guiana","PF":"French Polynesia","TF":"French Southern Territories","GA":"Gabon","GM":"Gambia","GE":"Georgia","DE":"Germany","GH":"Ghana","GI":"Gibraltar","GR":"Greece","GL":"Greenland","GD":"Grenada","GP":"Guadeloupe","GU":"Guam","GT":"Guatemala","GG":"Guernsey","GN":"Guinea","GW":"Guinea-Bissau","GY":"Guyana","HT":"Haiti","HM":"Heard Island and McDonald Islands","VA":"Holy See (Vatican City State)","HN":"Honduras","HK":"Hong Kong","HU":"Hungary","IS":"Iceland","IN":"India","ID":"Indonesia","IR":"Iran, Islamic Republic of","IQ":"Iraq","IE":"Ireland","IM":"Isle of Man",
"IL":"Israel","IT":"Italy","JM":"Jamaica","JP":"Japan","JE":"Jersey","JO":"Jordan","KZ":"Kazakhstan","KE":"Kenya","KI":"Kiribati","KP":"Korea, Democratic People's Republic of","KR":"Korea, Republic of","KW":"Kuwait","KG":"Kyrgyzstan","LA":"Lao People's Democratic Republic","LV":"Latvia","LB":"Lebanon","LS":"Lesotho","LR":"Liberia","LY":"Libyan Arab Jamahiriya","LI":"Liechtenstein","LT":"Lithuania","LU":"Luxembourg","MO":"Macao","MK":"Macedonia, the former Yugoslav Republic of","MG":"Madagascar","MW":"Malawi","MY":"Malaysia","MV":"Maldives","ML":"Mali","MT":"Malta","MH":"Marshall Islands","MQ":"Martinique","MR":"Mauritania","MU":"Mauritius","YT":"Mayotte","MX":"Mexico","FM":"Micronesia, Federated States of","MD":"Moldova, Republic of","MC":"Monaco",
"MN":"Mongolia","ME":"Montenegro","MS":"Montserrat","MA":"Morocco","MZ":"Mozambique","MM":"Myanmar","NA":"Namibia","NR":"Nauru","NP":"Nepal","NL":"Netherlands","AN":"Netherlands Antilles","NC":"New Caledonia","NZ":"New Zealand","NI":"Nicaragua","NE":"Niger","NG":"Nigeria","NU":"Niue","NF":"Norfolk Island","MP":"Northern Mariana Islands","NO":"Norway","OM":"Oman","PK":"Pakistan","PW":"Palau","PS":"Palestinian Territory, Occupied","PA":"Panama","PG":"Papua New Guinea","PY":"Paraguay","PE":"Peru","PH":"Philippines","PN":"Pitcairn","PL":"Poland","PT":"Portugal","PR":"Puerto Rico",
"QA":"Qatar","RE":"Réunion","RO":"Romania","RU":"Russian Federation","RW":"Rwanda","BL":"Saint Barthélemy","SH":"Saint Helena, Ascension and Tristan da Cunha","KN":"Saint Kitts and Nevis","LC":"Saint Lucia","MF":"Saint Martin (French part)","PM":"Saint Pierre and Miquelon","VC":"Saint Vincent and the Grenadines","WS":"Samoa","SM":"San Marino","ST":"Sao Tome and Principe","SA":"Saudi Arabia","SN":"Senegal","RS":"Serbia","SC":"Seychelles","SL":"Sierra Leone","SG":"Singapore","SK":"Slovakia","SI":"Slovenia","SB":"Solomon Islands","SO":"Somalia","ZA":"South Africa","GS":"South Georgia and the South Sandwich Islands","ES":"Spain","LK":"Sri Lanka","SD":"Sudan","SR":"Suriname","SJ":"Svalbard and Jan Mayen","SZ":"Swaziland","SE":"Sweden","CH":"Switzerland","SY":"Syrian Arab Republic","TW":"Taiwan, Province of China",
"TJ":"Tajikistan","TZ":"Tanzania, United Republic of","TH":"Thailand","TL":"Timor-Leste","TG":"Togo","TK":"Tokelau","TO":"Tonga","TT":"Trinidad and Tobago","TN":"Tunisia","TR":"Turkey","TM":"Turkmenistan","TC":"Turks and Caicos Islands","TV":"Tuvalu","UG":"Uganda","UA":"Ukraine","AE":"United Arab Emirates","GB":"United Kingdom","US":"United States of America","UM":"United States Minor Outlying Islands","UY":"Uruguay","UZ":"Uzbekistan","VU":"Vanuatu","VE":"Venezuela, Bolivarian Republic of","VN":"Viet Nam","VG":"Virgin Islands, British","VI":"Virgin Islands, U.S.","WF":"Wallis and Futuna","EH":"Western Sahara","YE":"Yemen","ZM":"Zambia","ZW":"Zimbabwe","":"?","00":"?"
}

#TVDBToken=None
sys.path.append(xbmc.translatePath(os.path.join(ADDON_PATH, 'resources', 'lib')).decode('utf8'))
#----------------------------------------------------------------------------------------------------

#-------------------------- FENETRE ARTWORKS ----------------------------------------------------------
    
class dialog_select_Arts(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)
        self.listing = kwargs.get('listing')
        self.Actuels = kwargs.get('actuels')
        
        

    def onInit(self):
        self.Choix={}
        if self.Actuels:
         for key in self.Actuels:
          self.Choix[key]=self.Actuels[key]
        self.Retour=False
        self.ListeAffiche = self.getControl(200)
        self.ListeBanniere = self.getControl(201)
        self.ListeLogo = self.getControl(202)
        self.ListeClearArt = self.getControl(203)
        self.ListeVignette = self.getControl(204)
        self.ListeDisque = self.getControl(205)
        #self.Liste201 = self.getControl(201)
        for item in self.listing:
          try:
            Label2=item.getLabel2()
          except:
            Label2=""
           
          if Label2=="poster" and self.ListeAffiche:  #32700         
              self.ListeAffiche.addItem(item)
          if Label2=="banner" and self.ListeBanniere:  #32702         
              self.ListeBanniere.addItem(item)
          if Label2=="logo" and self.ListeLogo:        #32701   
              self.ListeLogo.addItem(item)
          if Label2=="clearart" and self.ListeClearArt: #32704          
              self.ListeClearArt.addItem(item)
          if Label2=="thumb" and self.ListeVignette:  #32705         
              self.ListeVignette.addItem(item)
          if Label2=="discart" and self.ListeDisque:  #32703         
              self.ListeDisque.addItem(item)
              
        
        #artworks en cours
        #{"logo","clearart","banner","poster","fanart","thumb","discart"}
        if self.Choix.get("poster") :
          self.getControl(10).setImage(self.Choix["poster"], False)
        if self.Choix.get("banner") :
          self.getControl(11).setImage(self.Choix["banner"], False)
        if self.Choix.get("logo") :
          self.getControl(12).setImage(self.Choix["logo"], False)
        if self.Choix.get("clearart") :
          self.getControl(13).setImage(self.Choix["clearart"], False)
        if self.Choix.get("thumb") :
          self.getControl(14).setImage(self.Choix["thumb"], False)        
        if self.Choix.get("discart") :
          self.getControl(15).setImage(self.Choix["discart"], False)        
        
        self.getControl(1).setLabel(__language__( 32614 )) 
        self.getControl(20).setLabel(__language__( 32700 )+" [I]("+str(self.ListeAffiche.size())+")[/I]")
        self.getControl(21).setLabel(__language__( 32705 )+" [I]("+str(self.ListeVignette.size())+")[/I]")
        self.getControl(22).setLabel(__language__( 32702 )+" [I]("+str(self.ListeBanniere.size())+")[/I]")
        self.getControl(23).setLabel(__language__( 32704 )+" [I]("+str(self.ListeClearArt.size())+")[/I]")
        self.getControl(24).setLabel(__language__( 32703 )+" [I]("+str(self.ListeDisque.size())+")[/I]")
        self.getControl(25).setLabel(__language__( 32701 )+" [I]("+str(self.ListeLogo.size())+")[/I]")
       
        #self.getControl(100).setLabel(__language__( 32611 ))
        
        if self.ListeAffiche:
          self.setFocus(self.ListeAffiche)
        
           
                  
       # else:          self.close()
        

    def onAction(self, action):
        idaction=action.getId()
        if action in ACTION_PREVIOUS_MENU:
            self.Retour=False         
            self.close()
        if (idaction==3 or idaction==4) and (self.getFocusId()>=200):
          Image = self.getControl(self.getFocusId()).getSelectedItem().getProperty("Icon") 
          typex=self.getControl(self.getFocusId()).getSelectedItem().getLabel2()
          if typex=="poster": 
            self.getControl(9).setHeight(350)
          else:
            self.getControl(9).setHeight(220) 
            
          self.getControl(9).setImage(Image, False)
        #else : logMsg("IdAction : "+str(idaction),0)    
       
        
# Action : 3 haut
#Action : 4 bas
# Action : 2 droite
# Action : 1 gauche

    def onClick(self, controlID): 
        #logMsg("ControlId :"+str(controlID),0)
                     
        if controlID>=200 and controlID<=210: #entrée
            item=self.getControl(controlID).getSelectedItem()
            Image=item.getProperty("Icon")
            Label2="Delete"
            
            if not item.getProperty("Original")=="":
              Label2Actuel=self.getControl(controlID+100).getLabel()
              if Label2Actuel=="Delete" : #on supprime
                
                Label2=""
              else:
                Image="None"
                Label2="Delete"
            
            self.getControl(controlID+100).setLabel(Label2)
              
              
            imagetype=item.getLabel2()                    
            self.Choix[imagetype]=Image 
            
            ImageContainer = self.getControl(controlID-190)   
            ImageContainer.setImage(Image, False)
            
            
        if controlID == 7: #cancel
            self.Retour=False 
            self.close()
            
        if controlID == 5: #OK
            self.Retour=True
            #logMsg("Choix = "+str(self.Choix),0)
            self.close()
            
    def onFocus(self, controlID)    :
      if controlID>=200 and controlID<=210:
        Image = self.getControl(self.getFocusId()).getSelectedItem().getProperty("Icon")
        typex=self.getControl(self.getFocusId()).getSelectedItem().getLabel2()
        if typex=="poster": 
          self.getControl(9).setHeight(350)
        else:
          self.getControl(9).setHeight(220)  
        self.getControl(9).setImage(Image, False)

   
# ------------------------------------ARTWORKS SAGAS/FILMS/TV--------------------------------------------------------------    

def sagachoixartcommun(Donnees=None,Lab2=None,RetourElements=None):
  if Donnees:
    for item in Donnees: 
      if item.get("lang")=="en" or item.get("lang")==KODILANGCODE or item.get("lang")=="00" or item.get("lang")=="" : 
        langue=item.get("lang").replace("00","?")
        if langue=="":
          langue="?"  
        if langue=="en":
          langue="English"    
        if langue==KODILANGCODE:
          langue=KODILANGUAGE      
        Elements = xbmcgui.ListItem(label=langue, iconImage=str(item.get("url")),label2=str(Lab2))
        Elements.setProperty("Icon",str(item.get("url")))
        Elements.setProperty("Original","")
        RetourElements.append(Elements)
  return RetourElements

def sagachoixart(donnees=None,OriginalArt=None,TypeVideo="movie"): #movie ou tv
  ListeChoixArt=[]
  langue=KODILANGCODE #les 2 premieres lettres uniquement pour TMDB
  #OriginalArt:"logo","clearart","banner","poster","fanart","thumb","discart"
  KeyStr={"logo":32701,"clearart":32704,"banner":32702,"poster":32700,"fanart":32706,"thumb":32705,"discart":32703}
  if OriginalArt:
    for key in OriginalArt:
      if OriginalArt.get(key):
        if OriginalArt.get(key)!="None":
           Elements = xbmcgui.ListItem(label="[I][kodi][/I]", iconImage=str(OriginalArt.get(key)),label2=key)
           Elements.setProperty("Icon",str(OriginalArt.get(key)))
           Elements.setProperty("Original","Original")
           Elements.setProperty("Delete","Delete")
           ListeChoixArt.append(Elements)
  
  
  if donnees:
    sagachoixartcommun(donnees.get("%sposter" %(TypeVideo)),"poster",ListeChoixArt)
    sagachoixartcommun(donnees.get("hd%slogo" %(TypeVideo)),"logo",ListeChoixArt)
    sagachoixartcommun(donnees.get("%slogo" %(TypeVideo)),"logo",ListeChoixArt)
    sagachoixartcommun(donnees.get("hd%sbanner" %(TypeVideo)),"banner",ListeChoixArt)
    sagachoixartcommun(donnees.get("%sbanner" %(TypeVideo)),"banner",ListeChoixArt)
    sagachoixartcommun(donnees.get("moviedisc"),"discart",ListeChoixArt) 
    sagachoixartcommun(donnees.get("hd%sthumb" %(TypeVideo)),"thumb",ListeChoixArt)  
    sagachoixartcommun(donnees.get("%sthumb" %(TypeVideo)),"thumb",ListeChoixArt) 
    sagachoixartcommun(donnees.get("%s" %("hdmoviecleart" if TypeVideo!="tv" else "hdclearart")),"clearart",ListeChoixArt)
    sagachoixartcommun(donnees.get("clearart"),"clearart",ListeChoixArt)
    
    
  if ListeChoixArt:
    #C:\Users\HTPC\AppData\Roaming\Kodi\addons\script.iconmixtools
    DialogChoixArtWorks = dialog_select_Arts('choixsagasarts.xml', __cwd__, 'default','1080i',listing=ListeChoixArt,actuels=OriginalArt) 
    DialogChoixArtWorks.doModal()
    ret=DialogChoixArtWorks.Retour   
    if ret: 
      OriginalArt=DialogChoixArtWorks.Choix   
    del DialogChoixArtWorks 
    return OriginalArt
  else :
    return None 
    
    
def getdatafanart(donnees=None):
  pardefaut=None
  langue=KODILANGCODE
  if donnees:     
     for item in donnees:
       if item.get("lang")=="en":
        pardefaut=item.get("url")   
       if item.get("lang")==langue:  
         return item.get("url")
     return pardefaut  
  return None 

def MergeArtwork(json_data=None,json_data2=None):
  if json_data2:
      if not json_data:
            json_data={}
            
      for xx in json_data2:
        if json_data and json_data.get(xx):
          json_data[xx]=json_data[xx]+json_data2.get(xx)
        else:
          json_data[xx]=json_data2.get(xx)
  return json_data
   
def getartworks(IDCollection=None,OriginalArt=None,updateartwork=None,TypeVideo="movie",IDKodiSetouSaisonTv=None)   :
     
                                                
  ArtWorks={}
  json_data2=None
  
  if IDCollection:  
    if updateartwork:
       xbmc.executebuiltin( "ActivateWindow(busydialog)" ) 
                                  
    if TypeVideo=="movie":
       UrlFanartTv="http://webservice.fanart.tv/v3/movies/%s?api_key=769f122ee8aba06f4a513830295f2bc0" %(IDCollection) #infos completes
       json_data = requestUrlJson(UrlFanartTv)
       if not json_data and IDKodiSetouSaisonTv: # on va récupérer tous les artworks des films de la saga également.....
         json_result = getJSON('VideoLibrary.GetMovieSetDetails', '{ "setid":%d,"movies":{"properties": ["imdbnumber"]} }' %(int(IDKodiSetouSaisonTv)))
         if json_result and json_result.get("movies"): 
           allMovies = json_result.get("movies")
           for item in allMovies:
             UrlFanartTv="http://webservice.fanart.tv/v3/movies/%s?api_key=769f122ee8aba06f4a513830295f2bc0" %(item.get("imdbnumber")) #infos completes
             json_data=MergeArtwork(json_data,requestUrlJson(UrlFanartTv))
             
    else:
       UrlFanartTv="http://webservice.fanart.tv/v3/tv/%s?api_key=769f122ee8aba06f4a513830295f2bc0" %(IDCollection) #infos completes
       json_data = requestUrlJson(UrlFanartTv)      
       TvDbArt=GetArtWorksSerieTVDB(IDCollection)
       if TvDbArt:
          json_data=MergeArtwork(json_data,TvDbArt)
          """
          seasonposterTvDb=TvDbArt.get("seasonposter")
          if seasonposterTvDb:
            for item in seasonposterTvDb:
                seasonposter.append(item)
          seasonbannerTvDb=TvDbArt.get("seasonbanner")
          if seasonbannerTvDb:
            for item in seasonbannerTvDb:
                seasonbanner.append(item)
          """
    
       #json_data=MergeArtwork(json_data,getTVDBartworks(IDCollection,"tvbanner",IDKodiSetouSaisonTv))       
       #json_data=MergeArtwork(json_data,getTVDBartworks(IDCollection,"tvposter",IDKodiSetouSaisonTv))
       
    if (not json_data or len(json_data)<1) and updateartwork :
      xbmc.executebuiltin( "Dialog.Close(busydialog)" ) 
      dialog=xbmcgui.Dialog()
      dialog.notification('IconMixTools', __language__( 32512 ), "acteurs/arfffff.png", 3000)
    else:
      if updateartwork:
        xbmc.executebuiltin( "Dialog.Close(busydialog)" ) 
    if json_data or (OriginalArt and updateartwork):    
       
      #logo,clearart,banner,poster,fanart,thumb,discart  
      if updateartwork:
        json_data2=sagachoixart(json_data,OriginalArt,TypeVideo)
        if json_data2:
            return json_data2,True          
        else:
            return None,None
      else:
        
        ArtWorks["logo"]=getdatafanart(json_data.get("hd%slogo" %(TypeVideo)))
        if not ArtWorks["logo"]:
           ArtWorks["logo"]=getdatafanart(json_data.get("%slogo"  %(TypeVideo)))     
        #logMsg("Typevideo = "+str(TypeVideo),0)
        ArtWorks["banner"]=getdatafanart(json_data.get("%sbanner" %(TypeVideo)))
        ArtWorks["poster"]=getdatafanart(json_data.get("%sposter" %(TypeVideo)))
        if TypeVideo=="movie":
         ArtWorks["fanart"]=getdatafanart(json_data.get("moviebackground"))
         ArtWorks["clearart"]=getdatafanart(json_data.get("hdmovieclearart"))
        else:
         ArtWorks["fanart"]=getdatafanart(json_data.get("showbackground"))
         ArtWorks["clearart"]=getdatafanart(json_data.get("hdclearart"))
        ArtWorks["thumb"]=getdatafanart(json_data.get("%sthumb" %(TypeVideo)))
        ArtWorks["landscape"]=ArtWorks["thumb"]
        ArtWorks["discart"]=getdatafanart(json_data.get("moviedisc"))
        
        for key in OriginalArt:      
          if OriginalArt.get(key):
            ArtWorks[key]=OriginalArt.get(key)
     
      #clearart,banner,poster,fanart,thumb,discart,  
      
        return ArtWorks,None
  return None,None  
  
def updateartworkall(TypeVideo="Movies"):
  dialogC = xbmcgui.Dialog()
  ret=dialogC.yesno("ICONMIXTOOLS !!!", __language__( 32612 )," ", __language__( 32613 )) #-- Show a dialog 'YES/NO'.
  if ret<=0:
     return
  json_result = getJSON('VideoLibrary.Get%s' %(TypeVideo), '{}') 
  Titre=""
  if json_result:
    dp = xbmcgui.DialogProgress()
    dp.create("IconMixTools",Titre,"")
    NbItems=len(json_result)
    Compteur=0
    for item in json_result: 
      Titre=item.get("label")
      if TypeVideo=="Movies":
         updatemovieartwork(item.get("movieid"),False) 
      else:
         updatetvartwork(item.get("tvshowid"),False) 
      Progres=(Compteur*100)/NbItems
      Compteur=Compteur+1
      dp.update(Progres,Titre,"(%d/%d)" %(Compteur,NbItems))
      if dp.iscanceled(): break
    dp.close()       

def updatemovieartwork(ItemIdxx=None,Unique=True): 
  Actuels={}
  check_clearlogo=None
  check_clearart=None
  check_banner=None
  check_poster=None
  check_fanart=None
  check_thumb=None
  check_discart=None  
  updateartwork=True

  
  if ItemIdxx : 
        json_result = getJSON('VideoLibrary.GetMovieDetails', '{ "movieid":%s,"properties":["art","imdbnumber"]}' %(ItemIdxx))
        IMDBNumber=json_result.get("imdbnumber")
        allArt=json_result.get("art")
        if allArt:          
          if allArt.get("clearlogo"):
            check_clearlogo=urllib.unquote(allArt.get("clearlogo").replace("image://","")[:-1])
          if allArt.get("clearart"):
            check_clearart=urllib.unquote(allArt.get("clearart").replace("image://","")[:-1])
          if allArt.get("banner"):
            check_banner=urllib.unquote(allArt.get("banner").replace("image://","")[:-1])
          if allArt.get("poster"):
            check_poster=urllib.unquote(allArt.get("poster").replace("image://","")[:-1])
          if allArt.get("fanart"):
            check_fanart=urllib.unquote(allArt.get("fanart").replace("image://","")[:-1])
          if allArt.get("thumb"):
            check_thumb=urllib.unquote(allArt.get("thumb").replace("image://","")[:-1])
          if allArt.get("discart"):
            check_discart=urllib.unquote(allArt.get("discart").replace("image://","")[:-1])   
        Actuels={"logo":check_clearlogo,"clearart":check_clearart,"banner":check_banner,"poster":check_poster,"fanart":check_fanart,"thumb":check_thumb,"discart":check_discart}
           
        if IMDBNumber:
          if Unique :
             ArtWorks,updateartwork=getartworks(IMDBNumber,Actuels,updateartwork)  
          else:
             ArtWorks,bidon=getartworks(IMDBNumber,Actuels,False)
                                                
          if KODI_VERSION>=17 and ArtWorks and ( updateartwork or not Unique): 
            MAJ=""                            
            if ArtWorks.get("logo"):
              MAJ='"clearlogo":"%s",' %(ArtWorks.get("logo"))
            if ArtWorks.get("clearart"):
              MAJ=MAJ+'"clearart":"%s",' %(ArtWorks.get("clearart"))
            if ArtWorks.get("banner"):
              MAJ=MAJ+'"banner":"%s",' %(ArtWorks.get("banner"))
            if ArtWorks.get("poster"):
              MAJ=MAJ+'"poster":"%s",' %(ArtWorks.get("poster"))
            if ArtWorks.get("fanart"):
              MAJ=MAJ+'"fanart":"%s",' %(ArtWorks.get("fanart"))
            if ArtWorks.get("thumb"):
              MAJ=MAJ+'"thumb":"%s",' %(ArtWorks.get("thumb"))
            if ArtWorks.get("discart"):
              MAJ=MAJ+'"discart":"%s",' %(ArtWorks.get("discart"))

            if len(MAJ)>3:
              MJSAGA=MAJ[0:len(MAJ)-1] #suppression de la virgule de fin              
              try:
               json_result = setJSON('VideoLibrary.SetMovieDetails', '{ "movieid":%s,"art":{%s} }' %(ItemIdxx,MJSAGA))
              except:
                logMsg("VideoLibrary.SetMovieDetails : %s impossible = " %(ItemIdxx) + str(MJSAGA),0 )

#--------------------------------------------TVDB---------------------------------------------
def getTVDBToken():
  request = urllib2.Request(
      'https://api.thetvdb.com/login',
      json.dumps({'userkey': '61E6A873385FBC44','apikey': '685D1677F8A17481','username': 'metropolicon'}),
      headers = { 'Content-Type':'application/json' ,'Accept':'application/json'}
  )
  try:
    handle = urllib2.urlopen(request)
  except:
    handle=None
  
  if handle:
    zzz=json.loads(handle.read())
    if zzz.get("token"):
      return zzz.get("token")
  
  return None
    
def getTVDBData(url=None):
  Langue=KODILANGCODE
  token=SETTING("TvdbToken")
  if not token:
    token=getTVDBToken()
    if token:
      ADDON.setSetting(id='TvdbToken', value=token)
  if url and token:
    
      request = urllib2.Request(url,headers = { 'Accept':'application/json','Accept-Language': KODILANGCODE,'Authorization':' Bearer %s' %(token)})
      try:
        handle = urllib2.urlopen(request)
      except urllib2.HTTPError as e:
        #logMsg("erreur (%s) : %s" %(e.code,url),0)
        handle=None
        if e.code==401:
          token=getTVDBToken()
          if token:
            ADDON.setSetting(id='TvdbToken', value=token)
        
      if not handle:
        Langue='en'
        request = urllib2.Request(url,headers = { 'Accept':'application/json','Accept-Language': 'en','Authorization':' Bearer %s' %(token)})
        try:
          handle = urllib2.urlopen(request)
        except urllib2.HTTPError as e:
          #logMsg("erreur (%s) : %s" %(e.code,url),0)
          handle=None
        
      if handle:
        zzz=json.loads(handle.read())
        if zzz.get("data"):
         return zzz.get("data"),Langue
      
  return None,None
    
def getTVDBartworks(IDShow=None,ArtType=None,Saison=None):
  KeyStr={'series':'tvbanner','poster':'tvposter','fanart':"showbackground","season":"seasonposter","seasonwide":"seasonbanner"}
  #if not TVDBToken:
  if ArtType and IDShow:
      TypeArtWork=None
      for xx in KeyStr:
        if KeyStr.get(xx)==ArtType:
          TypeArtWork=xx
          break
      if TypeArtWork:       
          if 'tt' in str(IDShow):
             Data,Langue=getTVDBData('https://api.thetvdb.com/search/series?imdbId=%s' %(IDShow))
             if Data:
               IDShow=Data[0].get("id")
             else:
               IDShow=None
          
          if IDShow:  
            QueryUrl='https://api.thetvdb.com/series/%s/images/query?keyType=%s' %(IDShow,TypeArtWork)
            if Saison:
              QueryUrl=QueryUrl+"&subKey=%d" %(Saison)   
            Data,Langue=getTVDBData(QueryUrl)
            if Data:
              ArtWork=[]    
              for item in Data:
                ArtWork.append({"url":"https://www.thetvdb.com/banners/%s" %item.get("fileName"),"lang":Langue})
              return {"%s" %(ArtType):ArtWork}
  
  return None
  
def GetTvDbId(UniqueId=None):
  #uniqueid : {"imdb":"tt5193358","tvdb":"304591","tmdb":"61692"}
  if UniqueId.get("tvdb"):
    return UniqueId["tvdb"]
  if not UniqueId.get("tmdb") and UniqueId.get("imdb"):
    TMDBID=get_externalID(UniqueId["imdb"],"tvshow")
    if TMDBID:
      UniqueId["tmdb"]=TMDBID
  if UniqueId.get("tmdb"):
    query_url="https://api.themoviedb.org/3/tv/%s/external_ids?api_key=%s&language=en-US&include_adult=true" % (UniqueId["tmdb"],TMDBApiKey) 
    json_result = requestUrlJson(query_url)
    if json_result:
      return json_result.get("tvdb_id")
  if UniqueId.get("unknown"):
    return UniqueId["unknown"]
  return None
      
#--------------------------------------------SAGAS--------------------------------------------------          
def CheckSaga(ItemId=None,Statique=None):
    TitreSaga=""
    ArrayCollection={}
    PosterCollection=None
    FileTab=[]
    item = {}
    NbFilmsSaga=0
    NbKodi=0
    NbKodiValide=0
    NbTmdb=0
    Audio={}
    DateSortie=""
    today=""
    nowX = datetime.datetime.now().date()   
    ListeItem=[]
    ImdbItem=[]  
    
    DBTYPE=xbmc.getInfoLabel("ListItem.DBTYPE") 
    if not ItemId or (DBTYPE!="movie" and xbmc.getCondVisibility("Window.IsVisible(12003)") and not DBTYPE=="set"):
       if not Statique: xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))
       return
    
    if ItemId:
       try:
          dd=int(ItemId)
       except:          
          json_result = getJSON('VideoLibrary.GetMovieDetails', '{ "movieid":%d,"properties":["setid"] }' %(int(xbmc.getInfoLabel("ListItem.DBID"))))
          ItemId=json_result.get("setid")
          if not ItemId:              
                   return      
          
      
       if not Statique:
          xbmcplugin.setContent(int(sys.argv[1]), 'movies')
          
       savepath=ADDON_DATA_PATH+"/collections/saga%s" %(ItemId)
       #json_result = getJSON('VideoLibrary.GetMovieSetDetails', '{ "setid":%d,"movies": {"properties": [ "title","imdbnumber","art" ]} }' %(int(ItemId)))
       json_result = getJSON('VideoLibrary.GetMovieSetDetails', '{ "setid":%d,"properties":["art"],"movies": {"properties":["title","genre","year","rating","userrating","director","trailer","tagline","plot","plotoutline","originaltitle","lastplayed","playcount","writer","studio","mpaa","cast","country","imdbnumber","runtime","set","showlink","streamdetails","top250","votes","fanart","thumbnail","file","sorttitle","resume","setid","dateadded","tag","art"]} }' %(int(ItemId)))
       if json_result:
         NbKodi=int(json_result.get("limits").get("total"))
         
              #----------------------------BASE TMDB ----------------------------       
       if not xbmcvfs.exists(savepath):
        #création du fichier de la saga !!!
         ArrayCollection=getsagaitem(ItemId,1,None,None,json_result,None)
       else : 
        #lecture dans le fichier existant
         with open(savepath) as data_file:
          ArrayCollection = json.load(data_file)
          data_file.close()
          
       if ArrayCollection:         
          NbFilmsSaga=ArrayCollection.get("kodi")
          NbManquant=ArrayCollection.get("manquant")
          TitreSaga=ArrayCollection.get("saga")
          NbTmdb=ArrayCollection.get("tmdb")         
          PosterCollection=ArrayCollection.get("poster")
       
          if NbFilmsSaga and NbKodi and NbTmdb:
              if NbFilmsSaga!=NbKodi: # or NbKodi<NbTmdb: #mise a jour !!! 
                 ArrayCollection=getsagaitem(ItemId,1,ArrayCollection.get("kodicollection"),ArrayCollection.get("tmdbid"),json_result,None)
                 if ArrayCollection:
                     NbFilmsSaga=ArrayCollection.get("kodi")
                     NbManquant=ArrayCollection.get("manquant")
                     TitreSaga=ArrayCollection.get("saga")
                     NbTmdb=ArrayCollection.get("tmdb")
                     PosterCollection=ArrayCollection.get("poster")
    
       
       if ArrayCollection: 
         ArtWorks= ArrayCollection.get("artworks") 
         
         
         if ArtWorks:
           WINDOW.setProperty('IconMixSagaClearArt',ArtWorks.get('clearart'))
           WINDOW.setProperty('IconMixSagaClearLogo',ArtWorks.get('logo'))
           WINDOW.setProperty('IconMixSagaBackGround',ArtWorks.get('fanart'))
           WINDOW.setProperty('IconMixSagaBanner',ArtWorks.get('banner'))
           WINDOW.setProperty('IconMixSagaDiscArt',ArtWorks.get('discart'))
           WINDOW.setProperty('IconMixSagaPoster',ArtWorks.get('poster'))
           WINDOW.setProperty('IconMixSagaThumb',ArtWorks.get('thumb'))
           
         if ArrayCollection.get("missing") :
           for item in ArrayCollection.get("missing"):
             today=item.get("release_date")
             DateSortie="??/????"
             if today:
                 DateSortie=today[5:7]+"/"+today[0:4] #mois/annee
             if today and xbmc.getCondVisibility("Skin.HasSetting(SagaDate)"):
                nowX2 = datetime.datetime.strptime(today, '%Y-%m-%d').date()
             else :
                nowX2=nowX 
                today="????/??" 
                
             if nowX2<=nowX :            
                ItemListe = xbmcgui.ListItem(label=item.get("title"),iconImage="http://image.tmdb.org/t/p/original"+item.get("poster_path"),path="RunScript(script.iconmixtools,trailer=True)") 
                fanart=item.get("backdrop_path")
                if fanart:
                   fanart="http://image.tmdb.org/t/p/original"+fanart
                ItemListe.setArt({"poster":"http://image.tmdb.org/t/p/original"+item.get("poster_path"),"fanart":fanart})
                ItemListe.setInfo("video", {"title": item.get("title"),"setid":ItemId,"mediatype": "movie","year": item.get("release_date"),"plot": item.get("overview"),"originaltitle": item.get("originaltitle")})        
                ItemListe.setProperty('IMDBNumber', '')
                ItemListe.setProperty('TMDBNumber', str(item.get("id")))
                ItemListe.setProperty('DBID', "")                
                ItemListe.setProperty('DateSortie', DateSortie)
                ItemListe.setProperty('dbtype', 'movie')
                
                ItemListe.setProperty('SetId', str(ItemId))
                ItemListe.setProperty('PosterCollection',PosterCollection)
                ItemListe.setProperty('Rating',str(int(item.get("vote_average"))))
                ItemListe.setProperty('UserRating','')
                if not Statique:
                   ListeItem.append([item.get("file"),ItemListe,True])
                else:
                   
                   try:
                    release_date=item.get("release_date")[0:4]
                   except:
                    release_date="0"
                   if not release_date or release_date=="":
                    release_date="0" 
                   ListeItem.append([int(release_date),ItemListe])
       #----------------------------BASE LOCALE ----------------------------
       
       #json_result = getJSON('VideoLibrary.GetMovieSetDetails', '{ "setid":%d,"movies": {"properties":["title","genre","year","rating","userrating","director","trailer","tagline","plot","plotoutline","originaltitle","lastplayed","playcount","writer","studio","mpaa","cast","country","imdbnumber","runtime","set","showlink","streamdetails","top250","votes","fanart","thumbnail","file","sorttitle","resume","setid","dateadded","tag","art"]} }' %(int(ItemId)))
       for item in json_result.get("movies"): 
          ImdbItem.append(item.get("imdbnumber"))
       Compteur = {}.fromkeys(set(ImdbItem),0)
       for valeur in ImdbItem:
          Compteur[valeur] += 1
  
    
       for item in json_result.get("movies"):
          ItemListe = xbmcgui.ListItem(label=item.get("label"),path=item.get("file"))
          item["DBID"]=str(item.get("movieid"))     
          ImdbNumber=item.get("imdbnumber")
          FileTab.append( os.path.dirname(item.get("file"))+"\\")          
          
          #pistes audios tele
          Audio=item.get("streamdetails").get("audio")
          i=1
          if Audio:               
               for AudioElement in Audio:
                    ItemListe.setProperty('AudioLanguage.%d' %(i), AudioElement.get("language"))
                    ItemListe.setProperty('AudioChannels.%d' %(i), str(AudioElement.get("channels")))
                    ItemListe.setProperty('AudioCodec.%d' %(i), AudioElement.get("codec")) 
                    ItemListe.addStreamInfo('audio',AudioElement)                   
                    i=i+1
    
          #pistes vidéos 
          Video=item.get("streamdetails").get("video")
          i=0
          Codec=""
          if Video:
            #{"aspect":2.3975000381469726563,"codec":"h264","duration":5584,"height":800,"language":"eng","stereomode":"","width":1918}
            for VideoItem in Video:
               ItemListe.setProperty('VideoCodec', VideoItem.get("codec")) 
               ItemListe.addStreamInfo('video',VideoItem)
               
          #sous-titres     
          Subtitles=item.get("streamdetails").get("subtitle")
          i=1
          
          if Subtitles:
               for SubtitleElement in Subtitles:
                    ItemListe.setProperty('SubtitleLanguage.%d' %(i), SubtitleElement.get("language"))  
                    ItemListe.addStreamInfo('subtitle',SubtitleElement)                   
                    i=i+1
                    
          ItemListe.setProperty('DBID', str(item.get("movieid")))
          logMsg("Valeur item.get : (%s)" %(item.get("movieid")))
          ItemListe.setProperty('SetId', str(ItemId))
          ItemListe.setProperty('IMDBNumber', str(item.get("imdbnumber")))
          ItemListe.setProperty('TMDBNumber', '')
          ItemListe.setProperty('DateSortie', '')
          ItemListe.setProperty('doublons',str(Compteur[item.get("imdbnumber")]))
          ItemListe.setProperty('PosterCollection',PosterCollection)
          ItemListe.setProperty('Affiche',item.get("art")["poster"])
          ItemListe.setProperty('Rating',str(int(item.get("rating"))))
          UserRating=item.get("userrating")
          if UserRating:
             if int(UserRating)>0:
               ItemListe.setProperty('UserRating',str(int(item.get("userrating"))))
             else:
               ItemListe.setProperty('UserRating','')
         
          if item.get("art"):
                ArtWorkLocal=item.get("art")
                ArtWorkLocal["thumb"]=item.get("art")["poster"]
                ArtWorkFanartOk=urllib.unquote(ArtWorkLocal.get("fanart").replace("g/","g"))
                ArtWorkLocal["fanart"]=ArtWorkFanartOk.replace("image://","")
                ItemListe.setArt(ArtWorkLocal)
          #ItemListe.setIconImage(item.get("art")["poster"]) 
          Position=int(item.get("resume").get("position"))*100
          Total=int(item.get("resume").get("total"))
          
          try :
             PercentPlayed=Position/Total
          except:
             PercentPlayed=""
          ItemListe.setProperty('PercentPlayed', str(PercentPlayed))
          ItemListe.setInfo("dbid", str(item.get("movieid")))
          #ItemListe.setInfo("video", {"dbid": str(item.get("movieid")),"rating":item.get("rating"),"userrating":UserRating,"duration": item.get("runtime"),"set": item.get("set"),"setid": item.get("setid"), "title": item.get("title"),"mediatype": "movie","genre": item.get("genre"),"year": item.get("year"),"plot": item.get("plot"),"plotoutline": item.get("plotoutline"),"originaltitle": item.get("originaltitle"),"playcount":item.get("playcount"),"imdbnumber":item.get("imdbnumber")}) 
          LabelsSaga=GetListItemInfoLabelsJson(item)  
          if LabelsSaga:            
            ItemListe.setInfo("video", LabelsSaga) 
            
          NbKodi=NbKodi+1
          if int(Compteur[item.get("imdbnumber")])>0:
             NbKodiValide=NbKodiValide+1
             if not Statique:
               ListeItem.append([item.get("file"),ItemListe,True])
             else:
               try:
                    Annee=item.get("year")
               except:
                    Annee="0"
               if not Annee or Annee=="":
                Annee="0" 
               ListeItem.append([int(Annee),ItemListe])
             
          if int(Compteur[item.get("imdbnumber")])>1:
              Compteur[item.get("imdbnumber")]=0
       
       if NbKodiValide>0: WINDOW.setProperty('IconMixSaga',str(NbKodiValide))
       else: WINDOW.clearProperty('IconMixSaga')       
              
 

    #BOUQUET FINAL 

    if NbKodiValide==len(ListeItem): WINDOW.setProperty('IconMixSaga','complet')
    if not Statique:
          xbmcplugin.addDirectoryItems(int(sys.argv[1]), ListeItem)
          xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))
    else:
          ListeItemFinal=[]
          LL=[]          
          LL=sorted(ListeItem)
          #tri par année
          cpt=0
          while cpt<len(LL):
                 ListeItemFinal.append(LL[cpt][1])
                 cpt=cpt+1
               
          return ListeItemFinal,FileTab
          
          
          
        

def getsagaitem(ItemIdxx=None,ShowBusy=None,AKodiCollection=None,ATmdbId=None,json_result=None,updateartwork=None):
  
  allArt=None
  AllMovies= []
  Rspcollection= {}
  ManquantM=[]
  KodiCollection = []
  ArrayCollection={}
  PosterCollection=None
  IDcollection=None
  Element = ""
  NbFilmsSaga=0
  ItemId=""
  ItemIdx=""
  imdbNumber= ""
  today =""
  release = ""
  flagcheck=0
  DateSortie=""
  query_url=""
  Actuels={}
  check_clearlogo=None
  check_clearart=None
  check_banner=None
  check_poster=None
  check_fanart=None
  check_thumb=None
  check_discart=None  
  
  #logMsg("getsagaitem : ItemIdxx=%s,ShowBusy=%s,AKodiCollection=%s,ATmdbId=%s" %(ItemIdxx,ShowBusy,AKodiCollection,ATmdbId),0)
  if ItemIdxx : 
      savepath=ADDON_DATA_PATH+"/collections/saga%s" %(ItemIdxx)
      if ShowBusy: xbmc.executebuiltin( "ActivateWindow(busydialog)" ) 
      if not json_result:
        json_result = getJSON('VideoLibrary.GetMovieSetDetails', '{ "setid":%d,"properties":["art"],"movies": {"properties": [ "title","imdbnumber","art" ]} }' %(int(ItemIdxx)))
      if json_result and json_result.get("movies"): 
        allMovies = json_result.get("movies")
        allArt=json_result.get("art")
        if allArt:
          
          #ArrayCollection["artworks"]=allArt
          if allArt.get("clearlogo"):
            check_clearlogo=urllib.unquote(allArt.get("clearlogo").replace("image://","")[:-1])
          if allArt.get("clearart"):
            check_clearart=urllib.unquote(allArt.get("clearart").replace("image://","")[:-1])
          if allArt.get("banner"):
            check_banner=urllib.unquote(allArt.get("banner").replace("image://","")[:-1])
          if allArt.get("poster"):
            check_poster=urllib.unquote(allArt.get("poster").replace("image://","")[:-1])
          if allArt.get("fanart"):
            check_fanart=urllib.unquote(allArt.get("fanart").replace("image://","")[:-1])
          if allArt.get("thumb"):
            check_thumb=urllib.unquote(allArt.get("thumb").replace("image://","")[:-1])
          if allArt.get("discart"):
            check_discart=urllib.unquote(allArt.get("discart").replace("image://","")[:-1])   
          ArrayCollection["artworks"]={"logo":check_clearlogo,"clearart":check_clearart,"banner":check_banner,"poster":check_poster,"fanart":check_fanart,"thumb":check_thumb,"discart":check_discart}               

        if allMovies :
          if AKodiCollection:
            KodiCollection=AKodiCollection
          for Test in allMovies:
             imdbNumber=str(Test.get("imdbnumber"))
             if imdbNumber :
               zz=None
               for yy in KodiCollection:
                 if yy[0]==imdbNumber:
                   zz=1
                   break
             
               if not zz:
                 tmdbid=get_externalID(imdbNumber,"movie") # conversion imdb ou tvdb en themoviedb ....
                 if tmdbid :
                  if flagcheck==0:
                    ItemId=tmdbid 
                    flagcheck=1 
                  KodiCollection.append([imdbNumber,str(tmdbid)])
        if xbmcvfs.exists(savepath):       
          #lecture dans le fichier existant
           with open(savepath) as data_file:
            data = json.load(data_file)
            if data:
              Actuels=data.get("artworks")
            data_file.close()  
      if ItemId:
                if not ATmdbId:
                   #numero de collection TMDB inconnu
                   query_url = "https://api.themoviedb.org/3/movie/%s?api_key=%s&language=%s&include_adult=true" % (ItemId,TMDBApiKey,KODILANGCODE)
                   json_data = requestUrlJson(query_url)
                   
                   if json_data:
                      Rspcollection=json_data.get("belongs_to_collection")
                      if Rspcollection: IDcollection=Rspcollection.get("id")
                else: 
                   IDcollection=ATmdbId
                   
                if IDcollection:
                     query_url = "https://api.themoviedb.org/3/collection/%d?api_key=%s&language=%s&include_adult=true" % (IDcollection,TMDBApiKey,KODILANGCODE)
                     json_data = requestUrlJson(query_url)
                     

                     if json_data:
                         Rspcollection=json_data.get("parts")
                         if json_data.get("poster_path"):
                            PosterCollection="http://image.tmdb.org/t/p/original"+json_data.get("poster_path")
                         if json_data.get("backdrop_path"):
                            FanartCollection="http://image.tmdb.org/t/p/original"+json_data.get("backdrop_path")

                         if Rspcollection:
                            NbItemsCollection=len(Rspcollection)

                            NbFilmsSaga=0
                            Manquant=0
                            if NbItemsCollection>0:
                              for check in Rspcollection:
                                if check.get("id"):
                                  if check.get("genre_ids"):
                                    if check.get("genre_ids")[0]!=99:
                                        xxx=str(check.get("id"))
                                        zz=None
                                        cpt=0
                                        if KodiCollection:
                                            for yy in KodiCollection:
                                              if yy[1]==xxx:
                                                zz=1
                                                break
                                              else:
                                                cpt=cpt+1
                                        
                                        
                                        if not zz :
                                           if check.get("title") and check.get("release_date") and check.get("poster_path"):
                                                 ManquantM.append(check)
                                                 NbFilmsSaga=NbFilmsSaga+1
                                                                         
                                        else: NbFilmsSaga=NbFilmsSaga+1
                                  else:
                                    if NbItemsCollection>0:
                                       NbItemsCollection=NbItemsCollection-1
                                  
                            ArrayCollection["kodi"]=len(KodiCollection)
                            ArrayCollection["kodicollection"]=KodiCollection
                            ArrayCollection["tmdbid"]=IDcollection
                            ArrayCollection["tmdb"]=NbItemsCollection
                            ArrayCollection["poster"]=PosterCollection
                            ArrayCollection["fanart"]=FanartCollection
                            if IDcollection:
                              xxActuels=ArrayCollection.get("artworks")
                              if Actuels:
                                for key in Actuels:
                                  if not Actuels[key] and key=="clearart":
                                    xxActuels[key]=Actuels.get(key)
                                #xxActuels.update(Actuels)
                              Kupdateartwork=updateartwork                                  
                              ArtWorks,updateartwork=getartworks(IDcollection,xxActuels,updateartwork,"movie",ItemIdxx)
                            else:
                              if Actuels:
                                ArtWorks=Actuels
                              
                            if ArtWorks:
                              ArrayCollection["artworks"]=ArtWorks
                            else:
                              if KodiCollection[0]:
                                updateartwork=Kupdateartwork
                                ArtWorks,updateartwork=getartworks(KodiCollection[0][1],Actuels,updateartwork)
                            if ArtWorks:   
                              if PosterCollection and not ArtWorks.get("poster"):   
                                 ArtWorks["poster"]=PosterCollection
                              if FanartCollection and not ArtWorks.get("fanart"):  
                                 ArtWorks["fanart"]=FanartCollection
                            ArrayCollection["artworks"]=ArtWorks
                                 
                              
                                  
                            #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.SetMovieSetDetails","params":{"setid":38,"art":{"poster":"http://image.tmdb.org/t/p/original/zrApSsUX9i0qVntcCD0Pp55TdCy.jpg"}},"id":1}
                            if KODI_VERSION>=17 and ArtWorks and  (SETTING("updatesagaposter")=="true" or updateartwork): 
                              MAJ=""                            
                              if ArtWorks.get("logo") and ( SETTING("forceupdatesagaposter") or not  check_clearlogo):
                                MAJ='"clearlogo":"%s",' %(ArtWorks.get("logo"))
                              if ArtWorks.get("clearart") and ( SETTING("forceupdatesagaposter") or not  check_clearart):
                                MAJ=MAJ+'"clearart":"%s",' %(ArtWorks.get("clearart"))
                              if ArtWorks.get("banner") and ( SETTING("forceupdatesagaposter") or not  check_banner):
                                MAJ=MAJ+'"banner":"%s",' %(ArtWorks.get("banner"))
                              if ArtWorks.get("poster") and ( SETTING("forceupdatesagaposter") or not  check_poster):
                                MAJ=MAJ+'"poster":"%s",' %(ArtWorks.get("poster"))
                              if ArtWorks.get("fanart") and ( SETTING("forceupdatesagaposter") or not  check_fanart):
                                MAJ=MAJ+'"fanart":"%s",' %(ArtWorks.get("fanart"))
                              if ArtWorks.get("thumb") and ( SETTING("forceupdatesagaposter") or not  check_thumb):
                                MAJ=MAJ+'"thumb":"%s",' %(ArtWorks.get("thumb"))
                              if ArtWorks.get("discart") and ( SETTING("forceupdatesagaposter") or not  check_discart):
                                MAJ=MAJ+'"discart":"%s",' %(ArtWorks.get("discart"))

                              if len(MAJ)>3:
                                MJSAGA=MAJ[0:len(MAJ)-1] #suppression de la virgule de fin
                                
                                try:
                                 json_result = setJSON('VideoLibrary.SetMovieSetDetails', '{ "setid":%d,"art":{%s} }' %(int(ItemIdxx),MJSAGA))
                                except:
                                  logMsg("VideoLibrary.SetMovieSetDetails : %d impossible = " %(int(ItemIdxx)) + str(MJSAGA),0 )
                                
                if NbFilmsSaga>0: 
                   
                     ArrayCollection["saga"]=json_data.get("name")
                     ArrayCollection["manquant"]=len(ManquantM)
                     ArrayCollection["missing"]=ManquantM
                else :
                    
                     ArrayCollection["saga"]=xbmc.getInfoLabel("ListItem.Label").decode("utf8")
                     ArrayCollection["commentaire"]="introuvable sur TMDB"
                     ArrayCollection["manquant"]=0
                     ArrayCollection["missing"]=[]
                     ArrayCollection["kodi"]=len(KodiCollection)
                     ArrayCollection["kodicollection"]=KodiCollection
                     ArrayCollection["tmdbid"]=None
                     ArrayCollection["tmdb"]=len(KodiCollection)
                     ArrayCollection["poster"]=None                     
                     ArrayCollection["artworks"]={}
                     
                     
                if SETTING("cachesaga")=="false":
                       erreur=DirStru(savepath)
                       with io.open(savepath, 'w+', encoding='utf8') as outfile:
                           str_ = json.dumps(ArrayCollection,indent=4, sort_keys=True,separators=(',', ':'), ensure_ascii=False)
                           outfile.write(to_unicode(str_))
                              
      if ShowBusy: xbmc.executebuiltin( "Dialog.Close(busydialog)" )                           
            
 
  return ArrayCollection
  

def UpdateSagas(Une=None,Toutes=None,updateartwork=None):
     ItemId=0
     AllMovies= {}
     NbItems=0
     savepath=""
     Titre=""
     
     
     if not Une :
       dp = xbmcgui.DialogProgress()
       dp.create("IconMixTools",Titre,"")
       json_result = getJSON('VideoLibrary.GetMovieSets', '{}')
       if json_result: 
          NbItems=len(json_result)
          Compteur=0
          for Sagas in json_result:
            ItemId=Sagas.get("setid")
            savepath=ADDON_DATA_PATH+"/collections/saga%d" %(ItemId)
            
            #if Toutes or not os.path.exists(savepath) and ItemId: getsagaitem(ItemId.encode('utf8'),1)
            if Toutes or not xbmcvfs.exists(savepath) and ItemId: 
               getsagaitem(ItemId,None,None,None,None,None)   
               Titre=xbmc.getLocalizedString( 31924 )+" : [I]"+Sagas.get("label")+"[/I]"
            Progres=(Compteur*100)/NbItems
            Compteur=Compteur+1
            if Toutes: dp.update(Progres,Titre,"(%d/%d)" %(Compteur,NbItems))
            else : dp.update(Progres,Titre,"...")
            if dp.iscanceled(): break
       dp.close()  
     else :
          
          getsagaitem(str(Une),1,None,None,None,updateartwork)        
            
     


# --------------------------------------------SERIES-------------------------------------------
def updatetvartwork(ItemIdxx=None,Unique=True,Saison=None): 
  Actuels={}
  check_clearlogo=None
  check_clearart=None
  check_banner=None
  check_poster=None
  check_fanart=None
  check_thumb=None
  check_discart=None  
  updateartwork=True

  
  if ItemIdxx : 
        json_result = getJSON('VideoLibrary.GetTvShowDetails', '{ "tvshowid":%s,"properties":["art","uniqueid"]}' %(ItemIdxx))
        IMDBNumber=GetTvDbId(json_result.get("uniqueid"))
        allArt=json_result.get("art")
        if allArt:          
          if allArt.get("clearlogo"):
            check_clearlogo=urllib.unquote(allArt.get("clearlogo").replace("image://","")[:-1])
          if allArt.get("clearart"):
            check_clearart=urllib.unquote(allArt.get("clearart").replace("image://","")[:-1])
          if allArt.get("banner"):
            check_banner=urllib.unquote(allArt.get("banner").replace("image://","")[:-1])
          if allArt.get("poster"):
            check_poster=urllib.unquote(allArt.get("poster").replace("image://","")[:-1])
          if allArt.get("fanart"):
            check_fanart=urllib.unquote(allArt.get("fanart").replace("image://","")[:-1])
          if allArt.get("thumb"):
            check_thumb=urllib.unquote(allArt.get("thumb").replace("image://","")[:-1])
          if allArt.get("discart"):
            check_discart=urllib.unquote(allArt.get("discart").replace("image://","")[:-1])   
        Actuels={"logo":check_clearlogo,"clearart":check_clearart,"banner":check_banner,"poster":check_poster,"fanart":check_fanart,"thumb":check_thumb,"discart":check_discart}
           
        if IMDBNumber:
          if Unique :
             ArtWorks,updateartwork=getartworks(IMDBNumber,Actuels,updateartwork,"tv")  
          else:
             ArtWorks,bidon=getartworks(IMDBNumber,Actuels,False,"tv")
                                                
          if KODI_VERSION>=17 and ArtWorks and ( updateartwork or not Unique): 
            MAJ=""                            
            if ArtWorks.get("logo"):
              MAJ='"clearlogo":"%s",' %(ArtWorks.get("logo"))
            if ArtWorks.get("clearart"):
              MAJ=MAJ+'"clearart":"%s",' %(ArtWorks.get("clearart"))
            if ArtWorks.get("banner"):
              MAJ=MAJ+'"banner":"%s",' %(ArtWorks.get("banner"))
            if ArtWorks.get("poster"):
              MAJ=MAJ+'"poster":"%s",' %(ArtWorks.get("poster"))
            if ArtWorks.get("fanart"):
              MAJ=MAJ+'"fanart":"%s",' %(ArtWorks.get("fanart"))
            if ArtWorks.get("thumb"):
              MAJ=MAJ+'"thumb":"%s",' %(ArtWorks.get("thumb"))
            if ArtWorks.get("discart"):
              MAJ=MAJ+'"discart":"%s",' %(ArtWorks.get("discart"))

            if len(MAJ)>3:
              MJSAGA=MAJ[0:len(MAJ)-1] #suppression de la virgule de fin              
              try:
               json_result = setJSON('VideoLibrary.SetTvShowDetails', '{ "tvshowid":%s,"art":{%s} }' %(ItemIdxx,MJSAGA))
              except:
                logMsg("VideoLibrary.SetTvShowDetails : %s impossible = " %(ItemIdxx) + str(MJSAGA),0 )


def GetEpisodeSaison(KodiDbId=None):
  json_result = getJSON('VideoLibrary.GetSeasons', '{ "tvshowid":%d,"properties": [ "season","episode"]}' %(int(KodiDbId)))
  return json_result
  
def CheckSaisonComplete(KodiDbId=None):
  return None
  
def GetEpisodesKodi(TvShowId=None,Statique=True):
  ListeEpisodesFinal=[]
  ListeEpisodes=[]
  if TvShowId:
    json_result = getJSON('VideoLibrary.GetEpisodes', '{ "tvshowid":%d,"properties": ["playcount","file","art","resume","plot","director","episode","firstaired","title","originaltitle","productioncode","rating","ratings","season","seasonid","showtitle","specialsortepisode","specialsortseason","tvshowid","uniqueid","userrating","streamdetails","runtime"]}' %(int(TvShowId)))
    if json_result:
      for item in json_result:
          
          Art=item.get("art") 
          if Art:
              if Art.get("thumb"):
                Art["poster"]=Art["thumb"]
              else:
                Art["poster"]="DefaultThumb.png"
              try:
                ItemListe.setProperty('PosterSaison', Art.get("season.poster"))
              except:
                i=0
          else:
             Art={"poster":"DefaultThumb.png"}            
      
          ItemListe = xbmcgui.ListItem(label=item.get("title"),iconImage=Art[u"poster"],path=item.get("file"))
          ItemListe.setArt(Art)          
          
           #pistes audios tele
          try:
           Audio=item.get("streamdetails").get("audio")
          except:
           Audio=None
          i=1
          if Audio:               
               for AudioElement in Audio:
                    ItemListe.setProperty('AudioLanguage.%d' %(i), AudioElement.get("language"))
                    ItemListe.setProperty('AudioChannels.%d' %(i), str(AudioElement.get("channels")))
                    ItemListe.setProperty('AudioCodec.%d' %(i), AudioElement.get("codec")) 
                    ItemListe.addStreamInfo('audio',AudioElement)                   
                    i=i+1
    
          #pistes vidéos 
          try:
           Video=item.get("streamdetails").get("video")
          except:
           Video=None
          i=0
          Codec=""
          if Video:
            #{"aspect":2.3975000381469726563,"codec":"h264","duration":5584,"height":800,"language":"eng","stereomode":"","width":1918}
            for VideoItem in Video:
               ItemListe.setProperty('VideoCodec', VideoItem.get("codec")) 
               ItemListe.addStreamInfo('video',VideoItem)
               
          #sous-titres  
          try:   
           Subtitles=item.get("streamdetails").get("subtitle")
          except:
           Subtitles=None
          i=1
          
         
          
          if Subtitles:
               for SubtitleElement in Subtitles:
                    ItemListe.setProperty('SubtitleLanguage.%d' %(i), SubtitleElement.get("language"))  
                    ItemListe.addStreamInfo('subtitle',SubtitleElement)                   
                    i=i+1
               
          

          Position=int(item.get("resume").get("position"))*100
          Total=int(item.get("resume").get("total"))
          try:
               Ordre="%d%d" %(item.get("season"),item.get("episode"))
          except:
                Ordre=None
          
          try :
             PercentPlayed=Position/Total
          except:
             PercentPlayed=""
          
          ItemListe.setProperty('PercentPlayed', str(PercentPlayed))
          
         
          ItemListe.setInfo("dbid", str(item.get("episodeid")))
          LabelsEpisodes=GetListItemInfoLabelsJson(item)
          if LabelsEpisodes:            
            ItemListe.setInfo("video", LabelsEpisodes) 
          try:
            Saison=int(item.get("season"))
          except:
            Saison=0
          ListeEpisodes.append([int(Ordre),ItemListe,item.get("file"),Saison,Art.get("season.poster"),str(item.get("episodeid"))])
          
          
      ListeEpisodesFinal=[]
      LL=[]               
      LL=sorted(ListeEpisodes, key=lambda x:x[0],reverse=False)     
      cpt=0
      Saison=0
      SaisonTab={}
      while cpt<len(LL):
         Saison=str(LL[cpt][3])
         if SaisonTab.get(Saison):
           SaisonTab[Saison]=SaisonTab[Saison]+1
         else:
           SaisonTab[Saison]=1
       
         cpt=cpt+1
         
      #logMsg("Saison : (%s)" %(SaisonTab))
      Saison=0
      cpt=0
      while cpt<len(LL):
        
             if not Statique:
                 if LL[cpt][3]!=Saison:
                  Saison=LL[cpt][3]
                  Complet,NbKodi,PosterSaison=getepisodes(TvShowId,Saison,"tvshow")
                  Item=xbmcgui.ListItem(label=str(NbKodi),label2=str(Saison),path="")
                  if Complet==0:
                    Item.setProperty('Complet', "")
                  else:
                    Item.setProperty('Complet', str(Complet))
                  if PosterSaison:
                     Item.setProperty('PosterSaison', PosterSaison)
                  else:
                    Item.setProperty('PosterSaison', LL[cpt][4])
                  Episodes=0
                  ListeEpisodesFinal.append(["",Item,False])
                 if PosterSaison:
                     LL[cpt][1].setProperty('PosterSaison', PosterSaison)
                 else:
                    LL[cpt][1].setProperty('PosterSaison', LL[cpt][4])
                 ListeEpisodesFinal.append([LL[cpt][2],LL[cpt][1],False])
             else:
                 ListeEpisodesFinal.append(LL[cpt][1])
             #ListeEpisodesFinal.append(LL[cpt][1])
             cpt=cpt+1
  return ListeEpisodesFinal

def getepisodes(KodiDbId=None,saisonID=None,DBtype=None):
  
  SaisonDetails=None
  ArrayCollection={}
  NbEpisodes=-1
  NbEpisodesKodi=None
  KodiId=None
  NbKodi=None
  PosterSaison=None
  ItemId=""
  
  nowX = datetime.datetime.now().date()
  nowX2=nowX
  ItemListe=0
  tsea=0
  
  if KodiDbId and DBtype:  
      
    if DBtype=="season":
     xxx=xbmc.getInfoLabel("Container.FolderPath")
     xx=xxx.split("titles/")[1]
     KodiDbId=xx.split("/")[0]
     
        
    if DBtype=="episode":
      json_result = getJSON('VideoLibrary.GetEpisodeDetails', '{ "episodeid":%d,"properties": [ "title", "tvshowid","season" ]}' %(int(KodiDbId)))
      if json_result and json_result.get("tvshowid"):
         KodiDbId=json_result.get("tvshowid") 
         saisonID=json_result.get("season")
         #logMsg("TVSHOWID : %s - saison : %s" %(KodiDbId,saisonID),0)
      else : KodiDbId=None
    
    if KodiDbId:       
         json_result = getJSON('VideoLibrary.GetTVShowDetails', '{ "tvshowid":%d,"properties": [ "title", "uniqueid","episode" ]}' %(int(KodiDbId)))
         if json_result and json_result.get("uniqueid"):
            UniqueId=GetTvDbId(json_result.get("uniqueid"))
            NbKodi=json_result.get("episode")
            SaisonDetails=GetEpisodeSaison(KodiDbId)
       
     #---- ------------- ----------------------------------------------------------------
    if UniqueId:
      savepath=ADDON_DATA_PATH+"/series/tv%s" %(UniqueId)
      if not xbmcvfs.exists(savepath):
     #creation
         ArrayCollection=getallepisodes(KodiDbId,UniqueId,savepath,NbKodi,1,SaisonDetails)
         
      else : 
         with open(savepath) as data_file:
            ArrayCollection = json.load(data_file)
            data_file.close()
         if not ArrayCollection or not ArrayCollection.get("v6"): # si fichier foireux ?
          #mise a jour
            ArrayCollection=getallepisodes(KodiDbId,UniqueId,savepath,NbKodi,1,SaisonDetails)
            
      if ArrayCollection:
            WINDOW.setProperty('ItemCountry1',ArrayCollection.get("pays"))             
            
            if ArrayCollection.get("dateecheance"):
               try:
                  nowX2 = datetime.datetime.strptime(str(ArrayCollection.get("dateecheance")), '%Y-%m-%d').date()
               except:
                  nowX2=nowX  
            if NbKodi:   
               if str(ArrayCollection.get("tmdbid"))!=str(UniqueId) or str(ArrayCollection.get("nbkodi"))!=str(NbKodi) or not ArrayCollection.get("v6") or nowX>nowX2 :
                  #mise a jour
                  ArrayCollection=getallepisodes(KodiDbId,UniqueId,savepath,NbKodi,1,SaisonDetails)
                  
            if ArrayCollection and saisonID:
                     try:
                        NbEpisodes=int(ArrayCollection.get("saisons").get(str(saisonID)).get("NbEpisodes"))
                        NbEpisodesKodi=int(ArrayCollection.get("saisons").get(str(saisonID)).get("NbEpisodesKodi"))
                     except:
                        NbEpisodes=-1
                        NbEpisodesKodi=0
                     try:
                        PosterSaison=ArrayCollection.get("saisons").get(str(saisonID)).get("poster")
                     except:
                        PosterSaison=None
            if ArrayCollection:
                     WINDOW.setProperty('ItemCountry1',ArrayCollection.get("pays"))
                     
            if NbEpisodesKodi:
              if NbEpisodes==int(NbEpisodesKodi):
                 NbEpisodes=0 #complet  
      
  return NbEpisodes,NbEpisodesKodi,PosterSaison

def getdatafanarttv(donnees=None,saison=None):  
  langue=KODILANGCODE
  pardefaut=None
  if donnees:
     for item in donnees:
        if item:
           if item.get("lang")=="en" and item.get("season")==saison:
            pardefaut=item.get("url")
           if not pardefaut and item.get("season")==saison:
            pardefaut=item.get("url")   
           if item.get("lang")==langue and item.get("season")==saison:  
             return item.get("url")
     return pardefaut
  
  return None
  
def GetArtWorksSerieTVDB(IDShow=None):
  Data={}
  QueryUrl='http://thetvdb.com/api/685D1677F8A17481/series/%s/banners.xml' %(IDShow)
  Donnees=requestUrlJson(QueryUrl,True)
  if Donnees:
    #{"Banners": {"Banner": [{"id": "1270021", "BannerPath": "fanart/original/304591-1.jpg", "BannerType": "fanart", "BannerType2": "1280x720", "Colors": null, "Language": "en", "Rating": "10.0000", "RatingCount": "1", "SeriesName": "false", "ThumbnailPath": "_cache/fanart/original/304591-1.jpg", "VignettePath": "fanart/vignette/304591-1.jpg"}, {"id": "1120759", "BannerPath": "fanart/original/304591-2.jpg", "BannerType": "fanart", "BannerType2": "1920x1080", "Colors": null, "Language": "en", "Rating": "8.2000", "RatingCount": "5", "SeriesName": "false", "ThumbnailPath": "_cache/fanart/original/304591-2.jpg", "VignettePath": "fanart/vignette/304591-2.jpg"}, {"id": "1120760", "BannerPath": "fanart/original/304591-3.jpg", "BannerType": "fanart", "BannerType2": "1920x1080", "Colors": null, "Language": "en", "Rating": "5.5000", "RatingCount": "2", "SeriesName": "false", "ThumbnailPath": "_cache/fanart/original/304591-3.jpg", "VignettePath": "fanart/vignette/304591-3.jpg"}, {"id": "1127151", "BannerPath": "fanart/original/304591-5.jpg", "BannerType": "fanart", "BannerType2": "1920x1080", "Colors": null, "Language": "en", "Rating": "5.5000", "RatingCount": "2", "SeriesName": "false", "ThumbnailPath": "_cache/fanart/original/304591-5.jpg", "VignettePath": "fanart/vignette/304591-5.jpg"}, {"id": "1120800", "BannerPath": "fanart/original/304591-4.jpg", "BannerType": "fanart", "BannerType2": "1280x720", "Colors": null, "Language": "en", "Rating": "4.0000", "RatingCount": "3", "SeriesName": "true", "ThumbnailPath": "_cache/fanart/original/304591-4.jpg", "VignettePath": "fanart/vignette/304591-4.jpg"}, {"id": "1270252", "BannerPath": "posters/304591-5.jpg", "BannerType": "poster", "BannerType2": "680x1000", "Language": "en", "Rating": "10.0000", "RatingCount": "1"}, {"id": "1270020", "BannerPath": "posters/304591-4.jpg", "BannerType": "poster", "BannerType2": "680x1000", "Language": "en", "Rating": "10.0000", "RatingCount": "1"}, {"id": "1120761", "BannerPath": "posters/304591-1.jpg", "BannerType": "poster", "BannerType2": "680x1000", "Language": "en", "Rating": "7.0000", "RatingCount": "3"}, {"id": "1142057", "BannerPath": "posters/304591-2.jpg", "BannerType": "poster", "BannerType2": "680x1000", "Language": "en", "Rating": "5.6667", "RatingCount": "3"}, {"id": "1244423", "BannerPath": "posters/304591-3.jpg", "BannerType": "poster", "BannerType2": "680x1000", "Language": "en", "Rating": null, "RatingCount": "0"}, {"id": "1270255", "BannerPath": "seasons/304591-2.jpg", "BannerType": "season", "BannerType2": "season", "Language": "en", "Rating": "10.0000", "RatingCount": "1", "Season": "2"}, {"id": "1270254", "BannerPath": "seasons/304591-1-2.jpg", "BannerType": "season", "BannerType2": "season", "Language": "en", "Rating": "10.0000", "RatingCount": "1", "Season": "1"}, {"id": "1142061", "BannerPath": "seasons/304591-1.jpg", "BannerType": "season", "BannerType2": "season", "Language": "en", "Rating": "5.5000", "RatingCount": "2", "Season": "1"}, {"id": "1123501", "BannerPath": "graphical/304591-g4.jpg", "BannerType": "series", "BannerType2": "graphical", "Language": "en", "Rating": "10.0000", "RatingCount": "1"}, {"id": "1142059", "BannerPath": "graphical/304591-g5.jpg", "BannerType": "series", "BannerType2": "graphical", "Language": "en", "Rating": "10.0000", "RatingCount": "1"}, {"id": "1120799", "BannerPath": "graphical/304591-g3.jpg", "BannerType": "series", "BannerType2": "graphical", "Language": "en", "Rating": "5.5000", "RatingCount": "2"}, {"id": "1120758", "BannerPath": "graphical/304591-g2.jpg", "BannerType": "series", "BannerType2": "graphical", "Language": "en", "Rating": "5.5000", "RatingCount": "2"}, {"id": "1120757", "BannerPath": "graphical/304591-g.jpg", "BannerType": "series", "BannerType2": "graphical", "Language": "en", "Rating": null, "RatingCount": "0"}]}}
    #BannerType : 
    #<BannerType>fanart</BannerType> de la série
    #<BannerType>poster</BannerType> de la série
    #<BannerType>season</BannerType> poster,.... de la saison
    #<BannerType2>season</BannerType2> poster de la saison
    #<BannerType2>seasonwide</BannerType2> banniere de la saison
    
    SeasonPoster=[]
    SeasonBanner=[]
    tvbanner=[]
    tvposter=[]
    
    Donnees=Donnees.get("Banners")
    if Donnees:
        Donnees=Donnees.get("Banner")
        if Donnees:
            for Item in Donnees:
                Type=Item.get("BannerType")
                if Type and Type=="season":
                    Type2=Item.get("BannerType2")
                    XX={"id":Item.get("id"),"url":"https://www.thetvdb.com/banners/%s" %(Item.get("BannerPath")),"lang":Item.get("Language"),"season":Item.get("Season")}
                    if Type2 and Type2=="season": #poster de saison
                        SeasonPoster.append(XX)
                    if Type2 and Type2=="seasonwide": #banniere de saison
                        SeasonBanner.append(XX)
                if Type and Type=="series":
                    Type2=Item.get("BannerType2")
                    XX={"id":Item.get("id"),"url":"https://www.thetvdb.com/banners/%s" %(Item.get("BannerPath")),"lang":Item.get("Language")}
                    if Type2 and Type2=="graphical": #banniere de la série
                        tvbanner.append(XX)
                if Type and Type=="poster": #poster de la série
                    XX={"id":Item.get("id"),"url":"https://www.thetvdb.com/banners/%s" %(Item.get("BannerPath")),"lang":Item.get("Language")}
                    tvposter.append(XX)
                    
            if len(SeasonPoster):
                Data["seasonposter"]=SeasonPoster
            if len(SeasonBanner):
                Data["seasonbanner"]=SeasonBanner
            if len(tvbanner):
                Data["tvbanner"]=tvbanner
            if len(tvposter):
                Data["tvposter"]=tvposter
  return Data
        
           
  
 
  #Zig=getTVDBartworks(IDCollection,'seasonposter',None)
  #logMsg("GetTV (%s) (%s)" %(IDCollection,Zig))
  
def gettvartworks(IDCollection=None)   :
  ArtWorks={}
  ArtWorkSeason={}
  tvposter=None
  tvbanner=None
  #SAISON
  seasonposter=None
  seasonbanner=None
   
  
  
  
  if IDCollection:
    UrlFanartTv="http://webservice.fanart.tv/v3/tv/%d?api_key=769f122ee8aba06f4a513830295f2bc0" %(int(IDCollection)) #infos completes
    
    json_data = requestUrlJson(UrlFanartTv)
    TvDbArt=GetArtWorksSerieTVDB(IDCollection)
    
    if not json_data:
        json_data={"fake":[]}
    
    if json_data:      
      #logo,clearart,banner,poster,fanart,thumb,discart
      tvposter=json_data.get("tvposter")     
      tvbanner=json_data.get("tvbanner")      
      #SAISON
      seasonposter=json_data.get("seasonposter")      
      seasonbanner=json_data.get("seasonbanner")   
      
      
      if not tvposter:
        tvposter=[]
      if not seasonbanner:
        seasonbanner=[]
      if not seasonposter:
        seasonposter=[] 
      if not tvbanner:
        tvbanner=[] 
      
      tvposterTvDb=TvDbArt.get("tvposter")
      if tvposterTvDb:
        for item in tvposterTvDb:
            tvposter.append(item)
      tvbannerTvDb=TvDbArt.get("tvbanner")
      if tvbannerTvDb:
        for item in tvbannerTvDb:
            tvbanner.append(item)
      
      
      ArtWorks["logo"]=getdatafanart(json_data.get("hdtvlogo"))
      ArtWorks["clearart"]=getdatafanart(json_data.get("hdclearart"))
      ArtWorks["banner"]=getdatafanart(tvbanner)
      ArtWorks["poster"]=getdatafanart(tvposter)
      ArtWorks["fanart"]=getdatafanart(json_data.get("showbackground"))
      ArtWorks["thumb"]=getdatafanart(json_data.get("tvthumb"))
      ArtWorks["discart"]=None
      ArtWorks["characterart"]=getdatafanart(json_data.get("characterart"))     
      
      if TvDbArt:
          seasonposterTvDb=TvDbArt.get("seasonposter")
          if seasonposterTvDb:
            for item in seasonposterTvDb:
                seasonposter.append(item)
          seasonbannerTvDb=TvDbArt.get("seasonbanner")
          if seasonbannerTvDb:
            for item in seasonbannerTvDb:
                seasonbanner.append(item)
    
       
      ArtWorkSeason={"poster":seasonposter,"thumb":json_data.get("seasonthumb"),"banner":seasonbanner}
    
      return ArtWorks,ArtWorkSeason
  return None,None 
   
def UpdateSeries(Une=None,Toutes=None):
     ItemId=0
     AllMovies= {}
     NbItems=0
     savepath=""
     Titre=""
     SeasonDetails=None
     
    
     if not Une :
       dp = xbmcgui.DialogProgress()
       dp.create("IconMixTools",Titre,"")
       json_result = getJSON('VideoLibrary.GetTvShows', '{"properties":["uniqueid","episode"]}')
       if json_result: 
          NbItems=len(json_result)
          Compteur=0
          for Series in json_result:
            ItemId=Series.get("tvshowid")
            ImdbNumber=GetTvDbId(Series.get("uniqueid"))
            NbKodi=Series.get("episode")
            savepath=ADDON_DATA_PATH+"/series/tv%s" %(ImdbNumber)
            
            if Toutes or not xbmcvfs.exists(savepath) and ItemId:
               SaisonDetails=GetEpisodeSaison(ItemId)
               getallepisodes(ItemId,ImdbNumber,savepath,NbKodi,None,SaisonDetails)   
               Titre=xbmc.getLocalizedString( 20343 )+" : [I]"+Series.get("label")+"[/I]"
            Progres=(Compteur*100)/NbItems
            Compteur=Compteur+1
            if Toutes: dp.update(Progres,Titre,"(%d/%d)" %(Compteur,NbItems))
            else : dp.update(Progres,Titre,"...")
            if dp.iscanceled(): break
       dp.close() 
     else :
          TTEpisodes=xbmc.getInfoLabel("ListItem.Property(TotalEpisodes)")
          if TTEpisodes and TTEpisodes!="":
               NbKodi=int(TTEpisodes)
          
          json_result = getJSON('VideoLibrary.GetTVShowDetails', '{ "tvshowid":%d,"properties": [ "title", "uniqueid","episode" ]}' %(int(Une)))
          if json_result and json_result.get("uniqueid"):
            UniqueId=GetTvDbId(json_result.get("uniqueid"))
            savepath=ADDON_DATA_PATH+"/series/tv%s" %(UniqueId)
            SaisonDetails=GetEpisodeSaison(Une)
            getallepisodes(Une,UniqueId,savepath,NbKodi,1,SaisonDetails)        
            
  
  
def getallepisodes(IdKodi=None,TvDbId=None,savepath=None,NbKodi=None,ShowBusy=None,NbKodiSaison=None):
  
#https://api.betaseries.com/shows/display?key=46be59b5b866&thetvdb_id=266398  
#{ "show": {"id":6268,"thetvdb_id":266398,"imdb_id":"tt2249364","title":"Broadchurch","description":"Le meurtre d'un jeune gar\u00e7on \u00e0 Broadchurch, une petite ville c\u00f4ti\u00e8re, entraine un d\u00e9ferlement m\u00e9diatique qui menace de d\u00e9chirer les liens de sa communaut\u00e9.\n","seasons":"3",
#           "seasons_details":[{"number":1,"episodes":9},{"number":2,"episodes":8},{"number":3,"episodes":8}],
#           "episodes":"24","followers":"19435","comments":"112","similars":"33","characters":"16","creation":"2013",
#           "genres":["Crime","Drama"],
#           "length":"45","network":"ITV","rating":"","status":"Continuing","language":"en",
#           "notes":{"total":758,"mean":4.405,"user":0},
#           "in_account":false,
#           "images":{"show":"https:\/\/www.betaseries.com\/images\/fonds\/show\/6268_1172412.jpg","banner":"https:\/\/www.betaseries.com\/images\/fonds\/banner\/6268_952795.jpg","box":"https:\/\/www.betaseries.com\/images\/fonds\/box\/6268_952795.jpg","poster":"https:\/\/www.betaseries.com\/images\/fonds\/poster\/266398.jpg"},
#           "aliases":["Broadchurch"],
#           "user":{"archived":false,"favorited":false,"remaining":0,"status":0,"last":"S00E00","tags":null},
#           "resource_url":"https:\/\/www.betaseries.com\/serie\/broadchurch"}, 
#           "errors": [] }
 

  KodiCollection = []
  ArrayCollection={} 
  EpisodesDiffusion={}
  EpisodesSaison =[]
  EpisodesEtcasting={}
  SaisonTab={}
  Episodes=[]
  ItemId=""
  query_url=""
  nowX = datetime.datetime.now().date()+datetime.timedelta(30) #pour mise a jour une fois par mois
  if IdKodi or TvDbId:
     
     if TvDbId :
         if ShowBusy: xbmc.executebuiltin( "ActivateWindow(busydialog)" )                             
      
         
         ArrayCollection["tmdbid"]=TvDbId
         ArrayCollection["kodiid"]=IdKodi
         ArrayCollection["nbkodi"]=NbKodi
         ArrayCollection["dateecheance"]=nowX.strftime('%Y-%m-%d')
         ArrayCollection["v6"]="ok"
         TotalSaisons={}
         ArtWorkSerie,ArtWorkSeason=gettvartworks(TvDbId)
         if ArtWorkSerie:        
            ArrayCollection["artworks"]=ArtWorkSerie 
         
       
         query_url = "https://api.betaseries.com/shows/display?key=46be59b5b866&thetvdb_id=%s" % (TvDbId) 
         json_data = requestUrlJson(query_url)
         
          
         if json_data:
             SaisonTab=json_data.get("show")
             if SaisonTab:
                 ArrayCollection["name"]=SaisonTab.get("title")
                 ArrayCollection["imdbid"]=SaisonTab.get("imdb_id")
                 ArrayCollection["sa_id"]=SaisonTab.get("id")
                 #recupération du pays
                 qurl="https://api.themoviedb.org/3/find/%s?api_key=%s&language=en-US&external_source=imdb_id&include_adult=true"  % (ArrayCollection["imdbid"],TMDBApiKey)
                 json_data2 = requestUrlJson(qurl)
                 if json_data2:
                   allID=json_data2.get("tv_results")
                   ArrayCollection["pays"]=""
                   if allID and len(allID)>0:
                      for Test in allID:
                        try:
               	         ItemPays=Test.get("origin_country")[0]
               	        except:
               	         ItemPays=None
                      if ItemPays:
                        ArrayCollection["pays"]=ListePays.get(ItemPays.upper())
                 #---------------------------------
                 
                 SaisonTab=SaisonTab.get("seasons_details")
                 if SaisonTab:
                 	  for item in SaisonTab:             	  	       
                             EpisodesEtcasting={} 
                             EpisodesEtcasting["NbEpisodes"]=item.get("episodes")
                             EpisodesEtcasting["NbEpisodesKodi"]=0
                             if NbKodiSaison:
                               for check in NbKodiSaison:
                                 if check.get("season")==item.get("number"):
                                    EpisodesEtcasting["NbEpisodesKodi"]=check.get("episode")
                             if ArtWorkSeason:
                                 # allez ! va chercher et dans la bonne langue !
                                 EpisodesEtcasting["saison"]=str(item.get("number"))
                                 EpisodesEtcasting["banner"]=getdatafanarttv(ArtWorkSeason.get("banner"),str(item.get("number")))
                                 EpisodesEtcasting["poster"]=getdatafanarttv(ArtWorkSeason.get("poster"),str(item.get("number")))
                                 EpisodesEtcasting["thumb"]=getdatafanarttv(ArtWorkSeason.get("thumb"),str(item.get("number")))
                             TotalSaisons[str(item.get("number"))]=EpisodesEtcasting 
                             
                              
         ArrayCollection["saisons"]=TotalSaisons 
         
                
          #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.SetTvShowDetails","params":{"setid":38,"art":{"poster":"http://image.tmdb.org/t/p/original/zrApSsUX9i0qVntcCD0Pp55TdCy.jpg"}},"id":1}
         if KODI_VERSION>=17 and ArtWorkSerie and  SETTING("updatetvposter")=="true":                              
            MAJ=""
            if ArtWorkSerie.get("logo"):
              MAJ='"clearlogo":"%s",' %(ArtWorkSerie.get("logo"))
            if ArtWorkSerie.get("clearart"):
              MAJ=MAJ+'"clearart":"%s",' %(ArtWorkSerie.get("clearart"))
            if ArtWorkSerie.get("banner"):
              MAJ=MAJ+'"banner":"%s",' %(ArtWorkSerie.get("banner"))
            if ArtWorkSerie.get("poster"):
              MAJ=MAJ+'"poster":"%s",' %(ArtWorkSerie.get("poster"))
            if ArtWorkSerie.get("fanart"):
              MAJ=MAJ+'"fanart":"%s",' %(ArtWorkSerie.get("fanart"))
            if ArtWorkSerie.get("thumb"):
              MAJ=MAJ+'"landscape":"%s",' %(ArtWorkSerie.get("thumb"))  
            if ArtWorkSerie.get("characterart"):
              MAJ=MAJ+'"characterart":"%s",' %(ArtWorkSerie.get("characterart"))           

            if len(MAJ)>3:
              MJTV=MAJ[0:len(MAJ)-1] #suppression de la virgule de fin
              
              try:
               json_result = setJSON('VideoLibrary.SetTvShowDetails', '{ "tvshowid":%d,"art":{%s} }' %(int(IdKodi),MJTV))
              except:
                logMsg("VideoLibrary.SetTvShowDetails serie : %d impossible" %(int(IdKodi)),0 )
                
         if KODI_VERSION>=17 and TotalSaisons and  SETTING("updatetvposter")=="true":  
              #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.GetSeasons","params":{"tvshowid":75,"properties":["art"]},"id":1}
              json_result = getJSON('VideoLibrary.GetSeasons','{"tvshowid":%d,"properties":["season"]}' %(int(IdKodi)))
              if json_result:
                for item in json_result:
                  MAJ=""
                  if item.get("seasonid"):
                    season=item.get("season")
                    if TotalSaisons[str(season)].get("banner"):                   
                      MAJ=MAJ+'"banner":"%s",' %(TotalSaisons[str(season)].get("banner"))
                    if TotalSaisons[str(season)].get("poster"):                   
                      MAJ=MAJ+'"poster":"%s",' %(TotalSaisons[str(season)].get("poster"))
                    if TotalSaisons[str(season)].get("thumb"):                   
                      MAJ=MAJ+'"banner":"%s",' %(TotalSaisons[str(season)].get("thumb"))
                    if len(MAJ)>3:
                      MJTV=MAJ[0:len(MAJ)-1] #suppression de la virgule de fin
                      try:
                       json_result = setJSON('VideoLibrary.SetSeasonDetails', '{ "seasonid":%d,"art":{%s} }' %(int(item.get("seasonid")),MJTV))
                      except:
                        logMsg("VideoLibrary.SetTvSeasonDetails serie : %d impossible" %(int(item.get("seasonid"))),0 )
                  
     
                
         if SETTING("cacheserie")=="false":        
             erreur=DirStru(savepath)
             with io.open(savepath, 'w+', encoding='utf8') as outfile: 
    	                      str_ = json.dumps(ArrayCollection,indent=4, sort_keys=True,separators=(',', ':'), ensure_ascii=False)
    	                      outfile.write(to_unicode(str_))
         if ShowBusy: xbmc.executebuiltin( "Dialog.Close(busydialog)" )                 
  return ArrayCollection 

                
     

# --------------------------------------------UTILITAIRES/PLUGIN----------------------------------------------



def MergeContainers(Cont1Size=None,Cont2Size=None):
  windowvideonav = xbmcgui.Window(self,10025)
  try:
     Cont1=windowvideonav.getControl(self,2996)  
  except:
     Cont1=None
  try:
     Cont2=windowvideonav.getControl(self,2997)  
  except:
     Cont2=None
 
  
  if Cont1 or Cont2:
    ListesDest=[]
    if Cont1:
        c=0
        d=Cont1.size()
        while c<d:
          ItemListe=Cont1.getListItem(c)
          if ItemListe:
            logMsg("-O-"+str(c)+"/"+str(xxx),0)
          c=c+1
    if Cont2:  
        c=0
        Cont2.reset()
        d=Cont2.size()
        while c<d:
          ItemListe=Cont2.getListItem(c)
          if ItemListe:
             logMsg("-O-"+str(c)+"/"+str(xxx),0)
             #ListesDest.append(["", ItemListe, False])
          c=c+1
    
    xbmcplugin.addDirectoryItems(int(sys.argv[1]), ListeDest) 
  else:
    logMsg("merging....vide !",0)
  xbmcplugin.endOfDirectory(int(sys.argv[1])) 

def GetListItemInfoLabelsJson(data=None):
    
  if data:
    Valeur={}
    
    Valeur["genre"]=data.get("genre")
    if data.get("country"):
      Country=[]
      if len(data.get("country"))>1:
        for xx in data.get("country"):
          Country.append(xx)
      else:
        Country=data.get("country")[0]
     
      Valeur["country"]=Country
    Valeur["year"]=int(data.get("year")) if data.get("year") else None
    if not Valeur["year"]:
        if data.get("firstaired"):
            try:
             Valeur["year"]=int(data.get("firstaired").split("-")[0])
            except:
             Valeur["year"]=None   
        else:
           if data.get("premiered"):
            try:
              Valeur["year"]=int(data.get("premiered").split("-")[0])
            except:
              Valeur["year"]=None
              
    Valeur["top250"]=int(data.get("top250")) if data.get("top250") else None
    Valeur["setid"]=int(data.get("setid")) if data.get("setid") else None
    Valeur["rating"]=float(data.get("rating")) if data.get("rating") else None
    Valeur["userrating"]=int(data.get("userrating")) if data.get("userrating") else None
    Valeur["playcount"]=int(data.get("playcount")) if data.get("playcount") else None
    Valeur["overlay"]=int(data.get("overlay")) if data.get("overlay") else None
 
    if data.get("cast"):
      Casting=[]
      CastingRole=[]
      for xx in data.get("cast"):
        Casting.append(xx["name"])
        CastingRole.append((xx["name"],xx["role"]))      
      Valeur["castandrole"]=CastingRole
      Valeur["cast"]=Casting
    if data.get("director"):
      director=[]
      if len(data.get("director"))>1:
        for xx in data.get("director"):
          director.append(xx)
      else:
        director=data.get("director")[0]
      Valeur["director"]=director
    
    
    Valeur["mpaa"]=data.get("mpaa")
    Valeur["plot"]=data.get("plot")
    Valeur["plotoutline"]=data.get("plotoutline")
    Valeur["title"]=data.get("title")
    Valeur["originaltitle"]=data.get("originaltitle")
    Valeur["duration"]=int(data.get("duration")) if data.get("duration") else None
    if data.get("studio"):
      studio=[]
      if len(data.get("studio"))>1:
        for xx in data.get("studio"):
          studio.append(xx)
      else:
        studio=data.get("studio")[0]
      Valeur["studio"]=studio
    Valeur["tagline"]=data.get("tagline")
    if data.get("writer"):
      writer=[]
      if len(data.get("writer"))>1:
        for xx in data.get("writer"):
          writer.append(xx)
      else:
        writer=data.get("writer")[0]
      Valeur["writer"]=writer
    Valeur["tvshowtitle"]=data.get("showtitle")
    Valeur["premiered"]=data.get("premiered")
    Valeur["status"]=data.get("status")
    Valeur["set"]=data.get("set")
    Valeur["firstaired"]=data.get("firstaired")
    Valeur["imdbnumber"]=data.get("imdbnumber")
    if data.get("credits"):
      credits=[]
      if len(data.get("credits"))>1:
        for xx in data.get("credits"):
          credits.append(xx)
      else:
        credits=data.get("credits")[0]
      Valeur["credits"]=credits
    Valeur["lastplayed"]=data.get("lastplayed")
    Valeur["votes"]=data.get("votes")
    Valeur["path"]=data.get("file")
    Valeur["trailer"]=data.get("trailer")
    Valeur["dateadded"]=data.get("dateadded")
    
    Valeur["dbid"]=None
    if data.get("movieid"):
      Valeur["dbid"]=int(data.get("movieid"))
      Valeur["mediatype"]="movie"
    if data.get("episodeid"):
      Valeur["dbid"]=int(data.get("episodeid"))
      Valeur["mediatype"]="episode"
      Valeur["episode"]=data.get("episode") if data.get("episode") else None
      Valeur["season"]=data.get("season") if data.get("season") else None
      
    #logMsg("Valeur : (%s)" %(Valeur["dbid"]))
    return Valeur
  else:
    return None             
def GetListItemInfoLabels(ContainerID=None):
  if ContainerID:
    #logMsg("GetLabel (%s)" %(xbmc.getInfoLabel("Container(%d).ListItem.Country" %(ContainerID))))
    return  ({'genre':xbmc.getInfoLabel("Container(%d).ListItem.Genre" %(ContainerID)),
              'country':xbmc.getInfoLabel("Container(%d).ListItem.Country" %(ContainerID)),
              'year':int(xbmc.getInfoLabel("Container(%d).ListItem.Year" %(ContainerID))) if xbmc.getInfoLabel("Container(%d).ListItem.Year" %(ContainerID)) else None,
              'episode':(int(xbmc.getInfoLabel("Container(%d).ListItem.Episode" %(ContainerID)))) if xbmc.getInfoLabel("Container(%d).ListItem.Episode" %(ContainerID)) else None,
              'season':int(xbmc.getInfoLabel("Container(%d).ListItem.Season" %(ContainerID))) if xbmc.getInfoLabel("Container(%d).ListItem.Season" %(ContainerID)) else None,
              'top250':int(xbmc.getInfoLabel("Container(%d).ListItem.Top250" %(ContainerID))) if xbmc.getInfoLabel("Container(%d).ListItem.Top250" %(ContainerID)) else None,
              'setid':int(xbmc.getInfoLabel("Container(%d).ListItem.SetId" %(ContainerID))) if xbmc.getInfoLabel("Container(%d).ListItem.SetID" %(ContainerID)) else None,
              'tracknumber':int(xbmc.getInfoLabel("Container(%d).ListItem.TrackNumber" %(ContainerID))) if xbmc.getInfoLabel("Container(%d).ListItem.TrackNumber" %(ContainerID)) else None,
              'rating':float(xbmc.getInfoLabel("Container(%d).ListItem.Rating" %(ContainerID))) if xbmc.getInfoLabel("Container(%d).ListItem.Rating" %(ContainerID)) else None,
              'userrating':int(xbmc.getInfoLabel("Container(%d).ListItem.UserRating" %(ContainerID))) if xbmc.getInfoLabel("Container(%d).ListItem.UserRating" %(ContainerID)) else None,
              'watched':xbmc.getInfoLabel("Container(%d).ListItem.Watched" %(ContainerID)),
              'playcount':int(xbmc.getInfoLabel("Container(%d).ListItem.PlayCount" %(ContainerID))) if xbmc.getInfoLabel("Container(%d).ListItem.PlayCount" %(ContainerID)) else None,
              'overlay':int(xbmc.getInfoLabel("Container(%d).ListItem.Overlay" %(ContainerID))) if xbmc.getInfoLabel("Container(%d).ListItem.Overlay" %(ContainerID)) else None,
              'cast':[xbmc.getInfoLabel("Container(%d).ListItem.Cast")],
              'castandrole':[xbmc.getInfoLabel("Container(%d).ListItem.CastAndRole")],
              'director':xbmc.getInfoLabel("Container(%d).ListItem.Director" %(ContainerID)),
              'mpaa':xbmc.getInfoLabel("Container(%d).ListItem.Mpaa" %(ContainerID)),
              'plot':xbmc.getInfoLabel("Container(%d).ListItem.Plot" %(ContainerID)),
              'plotoutline':xbmc.getInfoLabel("Container(%d).ListItem.PlotOutline" %(ContainerID)),
              'title':xbmc.getInfoLabel("Container(%d).ListItem.Title" %(ContainerID)),
              'originaltitle':xbmc.getInfoLabel("Container(%d).ListItem.OriginalTitle" %(ContainerID)),
              'duration':int(xbmc.getInfoLabel("Container(%d).ListItem.Duration" %(ContainerID))) if xbmc.getInfoLabel("Container(%d).ListItem.Duration" %(ContainerID)) else None,
              'studio':xbmc.getInfoLabel("Container(%d).ListItem.Studio" %(ContainerID)),
              'tagline':xbmc.getInfoLabel("Container(%d).ListItem.Tagline" %(ContainerID)),
              'writer':xbmc.getInfoLabel("Container(%d).ListItem.Writer" %(ContainerID)),
              'tvshowtitle':xbmc.getInfoLabel("Container(%d).ListItem.TvShowTitle" %(ContainerID)),
              'premiered':xbmc.getInfoLabel("Container(%d).ListItem.Premiered" %(ContainerID)),
              'status':xbmc.getInfoLabel("Container(%d).ListItem.Status" %(ContainerID)),
              'set':xbmc.getInfoLabel("Container(%d).ListItem.Set" %(ContainerID)),
              'imdbnumber':xbmc.getInfoLabel("Container(%d).ListItem.IMDBNumber" %(ContainerID)),
              'credits':xbmc.getInfoLabel("Container(%d).ListItem.Credits" %(ContainerID)),
              'lastplayed':xbmc.getInfoLabel("Container(%d).ListItem.LastPlayed" %(ContainerID)),
              'album':xbmc.getInfoLabel("Container(%d).ListItem.Album" %(ContainerID)),
              'artist':[xbmc.getInfoLabel("Container(%d).ListItem.Artist")],
              'votes':xbmc.getInfoLabel("Container(%d).ListItem.Votes" %(ContainerID)),
              'path':xbmc.getInfoLabel("Container(%d).ListItem.Path" %(ContainerID)),
              'trailer':xbmc.getInfoLabel("Container(%d).ListItem.Trailer" %(ContainerID)),
              'dateadded':xbmc.getInfoLabel("Container(%d).ListItem.DateAdded" %(ContainerID)),
              'mediatype':xbmc.getInfoLabel("Container(%d).ListItem.DBTYPE" %(ContainerID)),
              'dbid':int(xbmc.getInfoLabel("Container(%d).ListItem.DBID" %(ContainerID)))  if xbmc.getInfoLabel("Container(%d).ListItem.DBID" %(ContainerID)) else None})    


def CheckItemExtrafanartPath(ItemPath=None,ItemSsRep='extrafanart'):
 
  ListeFanart = []
  extrafanart_dir=""
  
  if ItemPath and ItemPath!='':
     extrafanart_dir = ItemPath + ItemSsRep + '/'
     
     ListeFanart=get_filepaths(extrafanart_dir)

     for Item in ListeFanart:
          if Item.endswith('.jpg') or Item.endswith('.jpeg') or Item.endswith('.png'):
             return extrafanart_dir 
             break   
  
 
  return ""  


  
def getSagaFanartsV2(SagaItemPath=None):
  ListeFanarts=[] 
  #logMsg("Fanartsaga: %s" %(SagaItemPath),0)
  ListeFanart=None
  if SagaItemPath:
      ItemPath=CheckItemExtrafanartPath(SagaItemPath) 
      if ItemPath!="":
        ListeFanart=get_filepaths(ItemPath)
      if ListeFanart:    
        for Item in ListeFanart:
            
            if Item.endswith('.jpg') or Item.endswith('.jpeg') or Item.endswith('.png'):
               ItemListe=xbmcgui.ListItem(label="extrafanart",iconImage=Item)
               ItemListe.setProperty("fanart",Item)
               #ItemListe.setInfo("pictures", {"title": "extrafanart","picturepath": Item}) 
               ListeFanarts.append(ItemListe)        
  return ListeFanarts
  

 
def media_path(path):
    try:
        path = os.path.split(path)[0].rsplit(' , ', 1)[1].replace(",,",",")
    except:
        path = os.path.split(path)[0]
    path = [path]
    return path  
    
def get_filepaths(directory):
    file_paths = []

    # Walk the tree.
    if directory:
      if xbmcvfs.exists(directory):
        
        dirs,files=xbmcvfs.listdir(directory)
        for filename in files:
                  filepath = directory+ filename
                  file_paths.append(filepath)
    
    
    return file_paths  
    
def get_files(directory,sansextension=None):
    file_paths = []
    
    if directory:
      if xbmcvfs.exists(directory):
        dirs,files=xbmcvfs.listdir(directory)
        for filename in files:
            if not sansextension:
                  filepath = filename
            else:
                  filepath = filename.replace(".xsp","")
            file_paths.append(filepath)

    # Walk the tree.
    """
    if directory:
      for root, directories, files in os.walk(directory):
          for filename in files:
              if not sansextension:
                filepath = filename
              else:
                filepath = os.path.splitext(filename)[0]
              file_paths.append(filepath)
    """
    return file_paths  
    
    
def getGenre(genrex=None,genretypex=None,origtitle=None):
  ItemId = None
  item = {}
  genretype=""
  genre=""
  genrelist=[]
  if  (len(sys.argv)>1 and sys.argv[1]):
    
    if genretypex=="episode": #si content=episode -> tvshow
       genretypex="tvshow"
       origtitle=xbmc.getInfoLabel("ListItem.TVShowTitle")
    genretype="VideoLibrary.Get%ss" %(genretypex)
    genrelisttype=genretypex.encode("utf8")
    #recuperation du premier genre
    if genrex:
      genre = genrex.split(" /")[0]
      
    
     
    if genre  :
      
     #recuperation des IDs de tous les genres  
     json_genrelist = getJSON("VideoLibrary.GetGenres",'{"type":"%s"}' %genretypex)
     if json_genrelist:         		  
       #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.GetGenres","params":{"type":"movie"},"id":1}
      xyz2=0      
      for Test1 in json_genrelist:
        xyz1=Test1.get("label")
        
        if xyz1 == genre:
            xyz2 = Test1.get("genreid")
            #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.GetMovies","params":{ "filter": {"genreid":16}, "properties": [ "title", "Test" ] },"id":1}
            json_result = getJSON(genretype , '{ "filter": {"genreid":%d}, "properties": [ "art"] }' %xyz2)
            break
      
      if json_result:     
        for Test in json_result:
          Titre = Test.get("label")
          if Titre and Titre not in json_result:            
            xyz = str(Test.get("movieid"))
            ItemListe = xbmcgui.ListItem(label=Titre,iconImage=Test.get("art").get("poster"),label2=str(xyz2))
            if Titre != origtitle:
                 genrelist.append(["", ItemListe, False])

  xbmcplugin.addDirectoryItems(int(sys.argv[1]), genrelist) 
  xbmcplugin.endOfDirectory(int(sys.argv[1]))

# --------------------------------------------ACTEURS/REALISATEURS----------------------------------------------
        
def getCasting(Castingtypex=None,ItemId=None,Statique=None,MissingId=None):
  allCast = []
  item = {}
  Casting = []
  Castingtype=""
  imageacteur="" 
  ListeActeur=[]
 
  
  NonVide=xbmc.getCondVisibility("Skin.HasSetting(HideMovieTvCastEmpty)")
  #videodb://movies/actors/1132/   1132=id acteur pour retrouver ses films
  
  if  (len(sys.argv)>1 and sys.argv[1]) or Statique:
      if Castingtypex and ( ItemId or MissingId ):   
         #if Castingtypex=="episode":            Castingtypex="tvshow"
    
         Castingtype="VideoLibrary.Get%sDetails" %(Castingtypex)
         if ItemId and not MissingId:
          json_result = getJSON(Castingtype, '{ "%sid":%d,"properties": [ "cast"]}' %(Castingtypex,int(ItemId)))
         else :
            if not 'movie' in Castingtypex:
              Typex="tv"
            else:
              Typex="movie"
            query_url="https://api.themoviedb.org/3/%s/%s/credits?api_key=%s&language=%s&include_adult=true" % (Typex,MissingId,TMDBApiKey,KODILANGCODE) 
            json_result = requestUrlJson(query_url)

         #movie, tvshow
         if json_result:
            allCast = json_result.get("cast")  
         if allCast:
           for Test in allCast:
             name=Test.get("name")
             if Castingtypex=="episode":
              if int(Test.get("order"))==0 and Test.get("role")=="": #directeur
                name=None
             if name :
                 if ItemId and not MissingId:
                   imageacteur=Test.get("thumbnail")
                 else:
                   if Test.get("profile_path"):
                    imageacteur="http://image.tmdb.org/t/p/original"+str(Test.get("profile_path"))
                   else:
                    imageacteur=None
                 if not imageacteur and not NonVide:
                    imageacteur="DefaultActor.png"
                 #else :
                 if imageacteur:
                     if not MissingId:
                       imageacteur=urllib.unquote(imageacteur.replace("image://","")[:-1])
                     else:
                       imageacteur=urllib.unquote(imageacteur.replace("image://",""))
                     label2x=Test.get("role")
                     if not label2x:
                       label2x=Test.get("character")
                     ItemListe = xbmcgui.ListItem(label=name,iconImage=imageacteur,label2=label2x)
                     ItemListe.setProperty("DbType","acteurs")
                     #logMsg("Acteurs : "+str(ItemId)+"/"+str(imageacteur),0)   
                     if not Statique:
                         ListeActeur.append(["",ItemListe,True])
                     else:
                         ListeActeur.append(ItemListe)
                         
  if not Statique:
     xbmcplugin.addDirectoryItems(int(sys.argv[1]), ListeActeur)
     xbmcplugin.endOfDirectory(int(sys.argv[1]))
  else:
     return ListeActeur 
 

     
def ActeurFilmsTvKODI(ActeurType=None,Acteur=None,Statique=None):
  Donnees = []
  item = {}
  Casting = []
  RechercheType=""
  VideoPoster="" 
  ListeVideos=[]
  
  #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.GetMovies","params":{"filter":{"actor":"marion cotillard"},"properties":["thumbnail","year","file"]},"id":"1"}
  #videodb://movies/actors/1132/   1132=id acteur pour retrouver ses films
  if  (len(sys.argv)>1 and sys.argv[1]) or Statique:
      if Acteur: 
         if ActeurType and ActeurType=="director":
            Ok=""
         else: ActeurType="actor"
         Acteur=Remove_Separator(Acteur)
         #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.GetMovies","params":{"filter":{"field":"director","operator":"contains","value":"ridley"},"properties":["thumbnail","year","file"]},"id":"1"}       
         json_result = getJSON2("VideoLibrary.GetMovies", '{"filter":{"field":"%s","operator":"contains","value":"%s"},"properties":["title","genre","year","rating","userrating","director","trailer","tagline","plot","plotoutline","originaltitle","lastplayed","playcount","writer","studio","mpaa","cast","country","imdbnumber","runtime","set","showlink","streamdetails","top250","votes","fanart","thumbnail","file","sorttitle","resume","setid","dateadded","tag","art"]}' %(ActeurType,Acteur))
         json_result2 = getJSON2("VideoLibrary.GetTvShows", '{"filter":{"field":"%s","operator":"contains","value":"%s"},"properties":["plot","thumbnail","year","file","art","imdbnumber","rating","userrating","cast"]}' %(ActeurType,Acteur))
         
         #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.GetEpisodes","params":{"tvshowid":30,"properties":["cast"],"filter":{"actor":"CynthiaAddai-Robinson"}},"id":"1"}
         #pour obtenir tous les episodes comprenant l'acteur
         
         if len(json_result)>0:
          Donnees=json_result
         if len(json_result2)>0:
          Donnees=Donnees+json_result2        
         #movie, tvshow
                  
         if Donnees:
           
           for Item in Donnees:
             Titre=Item.get("label")
             if Titre:
                 ItemListe = xbmcgui.ListItem(label=Titre,iconImage=Item.get("art").get("poster"))
                 #logMsg("Poster : %s" %(Item.get("art").get("poster")),0)
                 ItemListe.setProperty("poster",Item.get("art").get("poster")) 
                 Casting = Item.get("cast")
                 if Casting:
                    for ItemCast in  Casting:
                         if ItemCast.get("name").encode('utf8')==Acteur:
                              ItemListe.setLabel2(ItemCast.get("role"))
                              break  
                 
                 IdVideo=Item.get("movieid")
                 TypeVideo="movie"
                 if not IdVideo: 
                    IdVideo=Item.get("tvshowid")
                    TypeVideo="tvshow"
                 ItemListe.setArt( Item.get("art"))
                 Fanart=Item.get("art").get("fanart")
                 if Fanart:
                     ItemListe.setProperty("fanart",Fanart)
                 else:
                     ItemListe.setProperty("fanart","")
                 
                 ItemListe.setProperty('DBID', str(IdVideo))
                 ItemListe.setProperty('dbtype',TypeVideo)
                 ItemListe.setProperty('IMDBNumber', str(Item.get("imdbnumber")))
                 ItemListe.setProperty('Rating',str(int(Item.get("rating")))) 
                 UserRating=Item.get("userrating")
                 if UserRating:
                     if int(UserRating)>0:
                       ItemListe.setProperty('UserRating',str(int(Item.get("userrating"))))
                     else:
                       ItemListe.setProperty('UserRating','')
                 
                 #pistes audios tele
                 try:
                   Audio=Item.get("streamdetails").get("audio")
                 except:
                   Audio=None
                 i=1
                 if Audio:               
                       for AudioElement in Audio:
                            ItemListe.setProperty('AudioLanguage.%d' %(i), AudioElement.get("language"))
                            ItemListe.setProperty('AudioChannels.%d' %(i), str(AudioElement.get("channels")))
                            ItemListe.setProperty('AudioCodec.%d' %(i), AudioElement.get("codec")) 
                            ItemListe.addStreamInfo('audio',AudioElement)                   
                            i=i+1
            
                  #pistes vidéos 
                 try:
                   Video=Item.get("streamdetails").get("video")
                 except:
                   Video=None
                 i=0
                 Codec=""
                 if Video:
                    #{"aspect":2.3975000381469726563,"codec":"h264","duration":5584,"height":800,"language":"eng","stereomode":"","width":1918}
                    for VideoItem in Video:
                       ItemListe.setProperty('VideoCodec', VideoItem.get("codec")) 
                       ItemListe.addStreamInfo('video',VideoItem)
                       
                  #sous-titres  
                 try:   
                   Subtitles=Item.get("streamdetails").get("subtitle")
                 except:
                   Subtitles=None
                 i=1
                  
                 if Subtitles:
                       for SubtitleElement in Subtitles:
                            ItemListe.setProperty('SubtitleLanguage.%d' %(i), SubtitleElement.get("language"))  
                            ItemListe.addStreamInfo('subtitle',SubtitleElement)                   
                            i=i+1
                            
                 InfoLabels=GetListItemInfoLabelsJson(Item)
                 if InfoLabels:
                   InfoLabels["mediatype"]= TypeVideo
                   #ItemListe.setInfo("video", {"dbid": str(IdVideo),"mediatype": TypeVideo,"title": Titre,"year": Item.get("year"),"trailer":Item.get("trailer"),"plot":Item.get("plot")})
                   ItemListe.setInfo("video", InfoLabels)
                   if not Statique:
                       ListeVideos.append([Item.get("file"),ItemListe,False])
                   else:
                       #ListeVideos.append(ItemListe)
                       try:
                            Annee=Item.get("year")
                       except:
                            Annee="0"
                       if not Annee or Annee=="":
                        Annee="0" 
                       ListeVideos.append([int(Annee),ItemListe])
  if not Statique:               
     xbmcplugin.addDirectoryItems(int(sys.argv[1]), ListeVideos)       
     xbmcplugin.endOfDirectory(int(sys.argv[1])) 
  else:
     ListeItemFinal=[]
     LL=[]               
     LL=sorted(ListeVideos, key=lambda x:x[0],reverse=True)
     #tri par année
     #logMsg("LL="+str(LL),0)
     cpt=0
     while cpt<len(LL):
             ListeItemFinal.append(LL[cpt][1])
             cpt=cpt+1
           
     return ListeItemFinal

def ActeurFilmsTvTMDB(ActeurType=None,Acteur=None,Statique=None):
  allInfo = []
  item = {}
  Casting = []
  Castingtype=""
  imageacteur="" 
  ListeRoles=[]
  ListeId=[]
  ActeurId={}
  ActeurCache={}
  json_data=None
  
  ActeurSave=1
  ActeurCache["nom"]=None
  ActeurCache["id"]=None
  if ActeurType and ActeurType=="director":
            ActeurType='realisateurs'
            ActeurCache["crew"]=[]
  else: ActeurType="acteurs"
  if ActeurType and Acteur!="None": 
     
     if Acteur:
        Acteur=Remove_Separator(Acteur)
        ActeurCache["cast"]=[] 
        check=remove_accents(Acteur).encode("utf8","ignore")
        savepath=ADDON_DATA_PATH+"/%s/%s" %(ActeurType,check.replace(" ", "_"))
        #savepath=ADDON_DATA_PATH+"/%s/%s" %(ActeurType,str(unidecode(Acteur)).replace(" ", "_"))
        if xbmcvfs.exists(savepath):
          with open(savepath) as data_file:
                  json_data = json.load(data_file)
                  ActeurSave=0
                  data_file.close()
                  if not json_data.get("cast") or not json_data.get("checkcastV7") or (ActeurType=="realisateurs" and not json_data.get("crew")):
                    ActeurSave=1
                  #if not json_data.get("biographie"):  
                  #  json_data=json_data+GetActeurInfo(Acteur)
                  #  ActeurSave=1
                  if json_data:                      
                      ActeurCache["biographie"]=json_data.get("biographie")
                      ActeurCache["naissance"]=json_data.get("naissance")                  
                      ActeurCache["deces"]=json_data.get("deces")                                                 
                      ActeurCache["lieunaissance"]=json_data.get("lieunaissance")
                      ActeurCache["nom"]=json_data.get("nom")
                      ActeurCache["nomreel"]=json_data.get("nomreel")
                      ActeurCache["id"]=json_data.get("id")
                      ActeurId=json_data.get("id")
        else :
            ActeurId=GetActeurId(Acteur) 
        
        #http://api.allocine.fr/rest/v3/filmography?partner=100043982026&code=12302&profile=large&filter=movie&striptags=synopsis%2Csynopsisshort&format=json&sed=20170507&sig=jfS3iVDun%2FywD91uBJ78p1lZlog%3D

        if ActeurId.get("tmdb") and (not xbmcvfs.exists(savepath) or ActeurSave>0):
            
            query_url = "https://api.themoviedb.org/3/person/%s/combined_credits?api_key=%s&language=%s&include_adult=true" % (ActeurId.get("tmdb"),TMDBApiKey,KODILANGCODE) 
            json_data = requestUrlJson(query_url)
            ActeurCache["checkcastV7"]="ok"
         
        if json_data: 
                  Donnees=None
                  if ActeurType!='realisateurs':
                    Donnees=json_data.get("cast")
                  if ActeurType=='realisateurs':
                    Donnees=json_data.get("crew")
                    
                  if Donnees:
                                     
                    for item in Donnees:                       
                       TypeVideo=str(item.get("media_type"))
                       name=""                     
                       if TypeVideo=="movie": name=item.get("title")
                       else : name=item.get("name")
                       if name:
                         
                         IdFix=item.get("id")
                         Ajout=1
                         if IdFix:
                            if not IdFix in ListeId:
                               ListeId.append(IdFix)                                                     
                            else:
                               Ajout=0
                         if Ajout>0:                                                                                
                              Poster=item.get("poster_path")
                              if not Poster: 
                                 if TypeVideo=="movie": Poster="RolesFilms.png"
                                 else: Poster="RolesSeries.png"
                              else: Poster="http://image.tmdb.org/t/p/original"+str(Poster)
                              if TypeVideo=="tv":
                                TypeVideo="tvshow"
                              
                              if ActeurType!='realisateurs':
                                ActeurCache["cast"].append(item)
                                Role=item.get("character")
                              if ActeurType=='realisateurs':
                                ActeurCache["crew"].append(item)
                                Role=item.get("job")
                              if not Role:
                                 Role="?"
                              ItemListe = xbmcgui.ListItem(label=name,iconImage=Poster,label2=Role)
                              ItemListe.setProperty("poster",Poster)
                              ItemListe.setArt({"poster":Poster})
                              Fanart=item.get("backdrop_path")
                              if Fanart:
                                 Fanart="http://image.tmdb.org/t/p/original"+Fanart
                                 ItemListe.setProperty("fanart",Fanart)
                              else:
                                 Fanart=""
                                 
                              try:
                                Annee=item.get("release_date").split("-")[0]
                              except:
                                Annee=None
                              if not Annee:
                                 try: 
                                   Annee=item.get("first_air_date").split("-")[0]
                                 except:
                                   Annee="0"
                              if not Annee or Annee=="":
                                Annee="0"
                             
                              
                              try:
                                Rating=str(int(item.get("vote_average")))
                              except:
                                Rating=""
                              try:
                       	         ItemPays=item.get("origin_country")
                       	      except:
                       	         ItemPays=None
                              if ItemPays:
                                Pays=[]
                                for paysitem in ItemPays:
                                  if len(paysitem)<4:
                                    Pays.append(ListePays.get(paysitem.upper()).encode("utf8"))
                                  else:
                                    Pays.append(paysitem.upper().encode("utf8"))
                                
                              else:
                                  Pays=None
                              ItemListe.setProperty("TMDBNumber",str(IdFix))
                              ItemListe.setProperty('Rating',Rating) 
                              ItemListe.setProperty("dbtype",TypeVideo)
                              ItemListe.setArt({'poster':Poster,'fanart':Fanart,'landscape':Fanart,'icon':Poster})
                              ItemListe.setInfo("video", {"title": name,"mediatype": TypeVideo,"rating":Rating,"year": Annee,"originaltitle": item.get("original_title"),"trailer":item.get("id"),"plot":item.get("overview"),"country":Pays})        
                              if not Statique:
                                 ListeRoles.append(["",ItemListe,True])
                              else :
                                 #ListeRoles.append(ItemListe)
                                 ListeRoles.append([int(Annee),ItemListe])
                  """             
                  if ActeurType=='realisateurs' and json_data.get("crew"):             
                      for item in json_data.get("crew"):
                         TypeVideo=str(item.get("media_type"))
                         name=""                     
                         if TypeVideo=="movie": name=item.get("title")                          
                         else : 
                           name=item.get("name")
                           TypeVideo="tvshow"
                         if name:
                           IdFix=item.get("id")
                           Ajout=1
                           if IdFix:
                              if not IdFix in ListeId:
                                 ListeId.append(IdFix)  
                                 #logMsg("Id :  "+str(IdFix),0)                                                   
                              else:
                                 Ajout=0
                           if Ajout>0:  
                                                                                
                                Poster=item.get("poster_path")
                                if not Poster: 
                                   if TypeVideo=="movie": Poster="RolesFilms.png"
                                   else: Poster="RolesSeries.png"
                                else: Poster="http://image.tmdb.org/t/p/original"+str(Poster)
                                Fanart=item.get("backdrop_path")
                               
                                
                                Role=item.get("job")
                                if not Role:
                                   Role="?"
                                ItemListe = xbmcgui.ListItem(label=name,iconImage=Poster,label2=Role)
                                if Fanart:
                                   ItemListe.setProperty("fanart","http://image.tmdb.org/t/p/original"+Fanart)
                                else:
                                   ItemListe.setProperty("fanart","zz")
                                if Poster:
                                   ItemListe.setProperty("poster",Poster)
                                   ItemListe.setArt({"poster":Poster})
                                else:
                                   ItemListe.setProperty("poster","zz")
                                #logMsg("name (%s) Poster (%s)" %(name,Poster))
                                try:
                                  Annee=item.get("release_date").split("-")[0]
                                except:
                                  Annee=None
                                if not Annee:
                                   try: 
                                     Annee=item.get("first_air_date").split("-")[0]
                                   except:
                                     Annee="0"
                                if not Annee or Annee=="":
                                  Annee="0"
                                ActeurCache["crew"].append(item)
                                try:
                       	           ItemPays=item.get("origin_country")[0]
                       	        except:
                         	         ItemPays=None
                                if ItemPays:
                                  Pays=ListePays.get(ItemPays.upper())
                                else:
                                  Pays=None
                                ItemListe.setProperty("TMDBNumber",str(IdFix))
                                ItemListe.setProperty("dbtype",TypeVideo)
                                ItemListe.setInfo("video", {"plot":item.get("overview"),"title": name,"mediatype": TypeVideo,"year": Annee,"originaltitle": item.get("original_title"),"trailer":item.get("id"),"country":Pays})        
                                if not Statique:
                                   ListeRoles.append(["",ItemListe,True])
                                else :
                                   #ListeRoles.append(ItemListe)
                                   ListeRoles.append([int(Annee),ItemListe])
                  """
                            
                  if ActeurSave>0 and SETTING("cacheacteur")=="false":
                        erreur=DirStru(savepath)
                        #ActeurCache["cast"]=json_data.get("cast") 
                        #ActeurCache["crew"]=json_data.get("crew")  
                        
                        if not ActeurCache["nom"]: ActeurCache["nom"]=str(unidecode(Acteur))                         
                        if not ActeurCache["id"]: ActeurCache["id"]=ActeurId                        
                        with io.open(savepath, 'w+', encoding='utf8') as outfile: 
                          str_ = json.dumps(ActeurCache,indent=4, sort_keys=True,separators=(',', ':'), ensure_ascii=False)
                          outfile.write(to_unicode(str_)) 
                       
                          
                  if not Statique:     
                      xbmcplugin.addDirectoryItems(int(sys.argv[1]), ListeRoles)
                                      
  if not Statique:
      xbmcplugin.endOfDirectory(int(sys.argv[1])) 
  else:
     ListeItemFinal=[]
     LL=[]          
     #LL=sorted(ListeRoles,reverse=True)
     LL=sorted(ListeRoles, key=lambda x:x[0],reverse=True)
     #tri par année
     cpt=0
     while cpt<len(LL):
             ListeItemFinal.append(LL[cpt][1])
             cpt=cpt+1
           
     return ListeItemFinal     
   
def GetActeurId(Acteur):
    
  ActeurId={}
  if Acteur!="None":  
        #allocine pour les frenchies ;)
        #ActeurId["allocine"]=''
        #Acteur=try_decode(Acteur.split("(")[0])
        ActeurId["allocine"]=Allocine_ChercheActeur(Acteur)
        
          #TMDB   
        try:
          check=Acteur.encode('utf8')
        except:
          check=Acteur 
        query_url = "https://api.themoviedb.org/3/search/person?api_key=%s&language=%s&query=%s&page=1&include_adult=true" % (TMDBApiKey,KODILANGCODE,urllib.quote(check))
        #logMsg("Query="+str(query_url),0)
        json_data = requestUrlJson(query_url)              
        ActeurId["tmdb"]=None        
        if json_data:
            allInfo=json_data.get("results")            
            
            if allInfo:
              for item in allInfo:
                if not ActeurId["tmdb"]:
                   ActeurId["tmdb"]=str(item.get("id"))
                   #logMsg("AxteurID="+str(ActeurId["tmdb"]),0)
                break
  return ActeurId 

def GetActeurInfo(NomActeur,ActeurType="acteurs"):
  ActeurCache={}
  ActeurId={}
  Bio=None
  json_data={}
  SaveActeur=0
  
  if ActeurType and "director" in ActeurType:
            ActeurType='realisateurs'
  if ActeurType and "actor" in ActeurType:
            ActeurType='acteurs'
  if NomActeur and ActeurType:
    NomActeur=Remove_Separator(NomActeur)
    check=remove_accents(NomActeur).encode("utf8","ignore")
    #savepath=ADDON_DATA_PATH+"/%s/%s" %(ActeurType,remove_accents(NomActeur.encode("utf8","ignore").decode("utf8","ignore").replace(" ", "_")))
    savepath=ADDON_DATA_PATH+"/%s/%s" %(ActeurType,check.replace(" ", "_"))
    #NomActeur=NomActeur.encode("utf8","ignore").decode("utf8","ignore")
    
    if xbmcvfs.exists(savepath):
        with open(savepath) as data_file:
                  try:
                    json_data = json.load(data_file)
                  except:
                    json_data=None
                  data_file.close() 
                  if json_data:
                      ActeurCache["cast"]=json_data.get("cast") 
                      ActeurId=json_data.get("id")
                      Bio=json_data.has_key('biographie')
                      if not json_data.get("v6"):
                        Bio=None
                       
                      #Bio=json_data.get("biographie")
                      
                  
   
    
    if not Bio or not ActeurId :
          if not ActeurId :            
            ActeurId=GetActeurId(NomActeur)
          if ActeurId:
            json_data=GetActeurInfoMaj(ActeurId,NomActeur)
          else:
            return ActeurCache          
           
    if json_data : 
              ActeurCache["biographie"]=json_data.get("biographie")
              ActeurCache["naissance"]=json_data.get("naissance")                  
              ActeurCache["deces"]=json_data.get("deces")                                                 
              ActeurCache["lieunaissance"]=json_data.get("lieunaissance")
              ActeurCache["nom"]=try_decode(json_data.get("nom"))
              ActeurCache["nomreel"]=try_decode(json_data.get("nomreel"))
              ActeurCache["poster"]=json_data.get("poster")
              ActeurCache["id"]=ActeurId
              ActeurCache["v6"]="ok"
              if SETTING("cacheacteur")=="false":
                  erreur=DirStru(savepath)            
                  with io.open(savepath, 'w+', encoding='utf8') as outfile: 
                    str_ = json.dumps(ActeurCache,indent=4, sort_keys=True,separators=(',', ':'), ensure_ascii=False)
                    outfile.write(to_unicode(str_))
  return ActeurCache

def GetActeurInfoMaj(ActeurId,NomActeur):
  #http://www.imdb.com/xml/find?json=1&nr=1&nm=on&q=Cynthia%20Addai-Robinson
  json_data={}
  json_datatmdb={}
  ActeurCache={}
  if ActeurId:
    if NomActeur:
      ActeurCache["nom"]=NomActeur
    if KODILANGUAGE[0:4]=='Fren' and ActeurId.get("allocine"):
          if (ActeurId["allocine"]!='') :        
            #si pas de bio en francais  et language de Kodi est French 
            json_datax=Allocine_Acteur(ActeurId.get("allocine"))
            
            if json_datax:
              
              jsonacteurdata=json.loads(json_datax)             
              if jsonacteurdata and KODILANGUAGE[0:4]=='Fren':
                      jsonActeur=jsonacteurdata.get("person")
                      if jsonActeur:
                        json_data["name"]=NomActeur 
                        json_data["realName"]=jsonActeur.get("realName")
                        json_data["biography"]=jsonActeur.get("biography")
                        json_data["birthday"]=jsonActeur.get("birthDate")      
                        json_data["deathday"]=''                                                 
                        json_data["place_of_birth"]=jsonActeur.get("birthPlace")
                        try:
                          json_data["poster"]=jsonActeur.get("picture")["href"] 
                        except:
                          json_data["poster"]=None
                        #ActeurId='allo'+str(AllocineId)                     
            
    if ActeurId.get("tmdb"):
        if not json_data.get("biography"):           
          #on recherche sur tmdb dans la langue de KODI
            query_url = "https://api.themoviedb.org/3/person/%s?api_key=%s&language=%s&include_adult=true" % (ActeurId.get("tmdb"),TMDBApiKey,KODILANGCODE) 
            json_datatmdb = requestUrlJson(query_url) 
            
        if not json_data or (not json_data.get("biography") and not json_datatmdb.get("biography")):   
              #pas de biographie dans la langue de KODI alors on cherche en Anglais......
              query_url = "https://api.themoviedb.org/3/person/%s?api_key=%s&language=EN&include_adult=true" % (ActeurId.get("tmdb"),TMDBApiKey) 
              json_datatmdb = requestUrlJson(query_url)
          
       
    if json_data or json_datatmdb: 
          if json_data.get("biography"):
             ActeurCache["biographie"]=json_data.get("biography")
          else:
             if not json_datatmdb:
              ActeurCache["biographie"]=""
             else:
              ActeurCache["biographie"]=json_datatmdb.get("biography")
             
          if json_data.get("birthday"):
             ActeurCache["naissance"]=json_data.get("birthday")
          else:
             if not json_datatmdb:
              ActeurCache["naissance"]=""
             else:
              ActeurCache["naissance"]=json_datatmdb.get("birthday")
             
          if json_data.get("deathday"):
             ActeurCache["deces"]=json_data.get("deathday")
          else:
             if not json_datatmdb:
              ActeurCache["deces"]=""
             else:
              ActeurCache["deces"]=json_datatmdb.get("deathday")
             
          if json_data.get("place_of_birth"):
             ActeurCache["lieunaissance"]=json_data.get("place_of_birth")
          else:
             if not json_datatmdb:
              ActeurCache["lieunaissance"]=""
             else:
              ActeurCache["lieunaissance"]=json_datatmdb.get("place_of_birth")
             
          if json_data.get("name"):
             ActeurCache["nom"]=json_data.get("name")
          else:
             if not json_datatmdb:
              ActeurCache["nom"]=""
             else:
              ActeurCache["nom"]=json_datatmdb.get("name")
             
          if json_data.get("realName"):
             ActeurCache["nomreel"]=json_data.get("realName")
          else:
             if not json_datatmdb:
              ActeurCache["nomreel"]=""
             else:
              ActeurCache["nomreel"]=json_datatmdb.get("realName")
          
          
          #"picture":{"name":"Photo Matthew Vaughn","path":"/pictures/15/01/15/17/40/151965.jpg","href":"http://fr.web.img2.acsta.net/pictures/15/01/15/17/40/151965.jpg"}
          
          
          if json_data.get("poster"):
             ActeurCache["poster"]=json_data.get("poster")
          else:
             if not json_datatmdb:
              ActeurCache["poster"]=""
             else:
              if json_datatmdb.get("profile_path"):
                ActeurCache["poster"]="http://image.tmdb.org/t/p/original"+json_datatmdb.get("profile_path")    
              
                 
          

                
  return ActeurCache  
    
def GetPhotoRealisateur(CheminType="",realisateur=None,HttpUniquement=None):
    allInfo = []
    realisateurId=""
    savepath=""   
    Poster=None  
    #savepath=ADDON_DATA_PATH+"/%s/%s" %(ActeurType,str(unidecode(NomActeur)).replace(" ", "_"))
    
    if realisateur and len(realisateur)>4: 
          realisateur=Remove_Separator(realisateur)
          #logMsg("realisateur (%s)" %(realisateur))
          zig=try_decode(realisateur).replace('"','')
          check=remove_accents(zig.replace(" ", "_"))
          #logMsg("realisateur (%s)(%s)" %(zig,check))
          savepath=ADDON_DATA_PATH+"/%s/%s" %(CheminType,check)
          if xbmcvfs.exists(savepath+".jpg"):
              return(savepath+".jpg")
              
          if xbmcvfs.exists(savepath):
              with open(savepath) as data_file:
                  try:
                    json_data = json.load(data_file)
                  except:
                    json_data=None
                  data_file.close() 
                  Poster=None
                  if json_data:
                      Poster=json_data.get("poster") 
                      if savepath:
                        return Poster
                      #Bio=json_data.get("biographie")
          
          if not Poster:  
             Poster="DefaultActor.png" 
             Cache=GetActeurInfo(zig,CheminType)
             if Cache:
                Poster=Cache.get("poster")
                
                if (CheminType=="realisateurs" and SETTING("cacherealisateur")=="false") or (CheminType=="acteurs" and SETTING("cacheacteur")=="false"):
                   query_url=Poster
                   try:                      
                     erreur=DirStru(savepath+".jpg")
                     urllib.urlretrieve(query_url,savepath+".jpg")
                   except :
                     str_response=''
                     Poster="DefaultActor.png"

    return(Poster if Poster else "DefaultActor.png")     
  
     
# --------------------------ALLOCINE --------------------------------------------

def Allocine_Acteur(IdActeur=None):
      if IdActeur:
        params = {}
        params['format'] = 'json'
        params['partner'] = Allocinepartner_key
        params['profile'] = 'medium'
        params['code'] = str(IdActeur)
        params['striptags'] = 'biography'

        response = Allocine_request('person', params)
        
        return response


def Allocine_request(method=None, params=None):
     
       api_url = 'http://api.allocine.fr/rest/v3'
       secret_key = '29d185d98c984a359e6e6f26a0474269'
       response=None
       user_agent = 'Dalvik/1.6.0 (Linux; U; Android 4.2.2; Nexus 4 Build/JDQ39E)'    
       query_url =api_url+'/'+method
       try:
          str_params=urllib.urlencode(params)
       except:
          return None

       today = datetime.date.today()
       sed = today.strftime('%Y%m%d')
       sha1 = hashlib.sha1(secret_key+str_params+'&sed='+sed).digest()
       b64 = base64.b64encode(sha1)
       sig = urllib2.quote(b64)
       query_url += '?'+str_params+'&sed='+sed+'&sig='+sig
       req = urllib2.Request(query_url)
       req.add_header('User-agent',user_agent)

       try:
           response = urllib2.urlopen(req, timeout = 3)       
            
       except :
           str_response=None
           response=None
           #logMsg("Resultat  URL introuvable 5--> " + str(query_url),0)
           
       if response :
          str_response = response.read().decode('utf8')
          #logMsg("Reponse allocine : "+str(str_response.encode("utf8")),0)
       
       return str_response
       
def GetSagaTrailersAllocine(Liste=None):
     #logMsg("Allocine SagaAnnonces : %s" %(Liste),0)
     ListeTrailer=[]
     try:
       zz=int(len(Liste))
     except:
       zz=-1
     cpt=0
     while cpt<zz:  
       Data= Allocine_BandeAnnonce(Liste[cpt]["Titre"],"movie",None,None,Liste[cpt]["Annee"],True)
       
       if Data:
         for Item in Data:
           ListeTrailer.append(Item)
       cpt=cpt+1
     return ListeTrailer 
     
def Allocine_BandeAnnonce(Titre=None,TypeVideo="movie",Saison=None,Episode=None,Annee=None,BAuniquement=None):
  ListeBandeAnnonce=[]
  XQualite=[720,480,320]
  TypeOk=[31003,31004,31016] #31003 : bande annonce / 31004 : extrait video / 31016 : Teaser
  QualiteEncode={"720":"720","480":"480","320":"480"}
  MediaEncode={"720":"_hd","480":"_sd","320":"_l"}
  Saisons=[]
  DataSeries=[]
  try:               
    MediaQualite=XQualite[int(SETTING("AllocineMiniQualite"))]
  except:
    MediaQualite=720 #par défaut 
  if BAuniquement:
    TypeOk=[31003]
  if Titre:
     if TypeVideo!="movie":
       TypeVideo="tvseries"
     if xbmcaddon.Addon().getSetting("allocinepasdetrailer") and not BAuniquement:
          TypeOk=[31003,31004]
     AllocineID=Allocine_ChercheFilmSerie(Titre,TypeVideo,Annee)
     #logMsg("Allocine ID : (%s)(%s)(%s) : %s - (%s)" %(Titre,TypeVideo,Annee,AllocineID,TypeOk),0)
     
     
     if AllocineID:
       Data,Saisons=Allocine_Medias(AllocineID,TypeVideo,Saison)
       #logMsg("(%s)(%s) Saisons (%s)" %(TypeVideo,Saison,Saisons),0)
       if Data:
         
         if TypeVideo!="movie" and Saisons:
            ListeTitres=[]
            if Saison :              
              for Item in Data: 
                  try:
                    MediaVType=int(Item.get("type")["code"])
                  except:
                    MediaVType=0
                  #TypeOk=[31003,3]
                  if MediaVType in TypeOk : #bande-annonce
                    try:
                      MediaTitre=Item.get("title")
                    except:
                      MediaTitre=""
                    if ("saison %s" %(Saison)) in MediaTitre:
                      if Episode: #episode fourni ?
                         if (("pisode %s" %(Episode)) in MediaTitre) or (not "pisode" in MediaTitre):
                          DataSeries.append(Item)
                          #logMsg("ajout episode : (%s)" %(MediaTitre))
                         #else:
                          #logMsg("rejet episode : (%s)" %(MediaTitre))
                      else:
                         DataSeries.append(Item)                      
              Data=DataSeries             
            else:
              if Data:
                for Item in Data:
                  try:
                    MediaVType=int(Item.get("type")["code"])
                  except:
                    MediaVType=0
                  if MediaVType in TypeOk : #bande-annonce
                    try:
                      MediaTitre=Item.get("title")
                    except:
                      MediaTitre=""
                    if (not "pisode" in MediaTitre or MediaVType==31003) and not MediaTitre in ListeTitres: #pas les episodes ni boublons !
                      DataSeries.append(Item)
                      ListeTitres.append(MediaTitre)
                    
              Data=DataSeries  
                             
                
         #test des données    
         if Data:
           ListeTitres=[]
           for Item in Data:
            if Item.has_key('class'):
              if Item.get('class')=="video":
                MediaId=Item.get("code")
                try:
                  MediaVType=int(Item.get("type")["code"])
                except:
                  MediaVType=0
                if MediaVType in TypeOk and MediaId:
                  
                  try:
                      MediaType=Item.get("type")["$"]
                  except:
                      MediaType=""                 
                  try:
                    if TypeVideo!="movie":
                      MediaTitre=Item.get("title").rsplit(MediaType,1)[0]
                    else:
                      MediaTitre=Item.get("title").replace(MediaType,"") #.replace("VO","").replace("VF","")
                  except:
                      MediaTitre=""
                  try:
                      MediaLanguageCode=Item.get("version")["code"]
                  except:
                      MediaLanguageCode=""
                  CheckTitre=MediaTitre
                  Remplacer=-1
                  if xbmcaddon.Addon().getSetting("allocinefrancais")=="true":
                    #pas de doublons VF/VO
                    tmpmediatitre=Item.get("title").replace(MediaType,"").replace("VO","").replace("VF","")
                    
                    for xx in ListeBandeAnnonce:
                      
                      if (xx["name"].replace("VO","").replace("VF","")) ==tmpmediatitre:
                         if MediaLanguageCode==6001 and xx["LanguageCode"]!=6001:
                          #même titre mais cette fois en francais !
                          Remplacer=ListeBandeAnnonce.index(xx)
                         if MediaLanguageCode!=6001 and xx["LanguageCode"]==6001: 
                          #même titre mais en francais déjà présent !
                          MediaVType=0 
                          
                  if BAuniquement and MediaTitre and MediaVType in TypeOk :
                            data=re.sub(r"\(.\)|\(..\)","", MediaTitre)
                            CheckTitre=data
                            
                  CheckTitre=CheckTitre.replace(" ","").lower()
                  
                  
                  if (not CheckTitre in ListeTitres or Remplacer>=0) and MediaVType>0: #bande-annonce....
                    try:
                      MediaApercu=Item.get("thumbnail")["href"]
                    except:
                      MediaApercu=""
                    try:
                      MediaPath=Item.get("thumbnail")["path"]
                    except:
                      MediaPath=None
                                      
                    
                    #MediaTitre=Item.get("title").rsplit(MediaType,1)[0]
                    MediaTitre=Item.get("title").replace(MediaType,"").replace("VO","").replace("VF","")
                    if BAuniquement and MediaTitre:
                            data=re.sub(r"\(.\)|\(..\)","", MediaTitre)
                            MediaTitre=data
                    try:
                      MediaLanguage=Item.get("version")["$"]
                    except:
                      MediaLanguage=""
                   
                      
                    if MediaPath:
                      MediaUrl=MediaPath.replace("/videothumbnails/","/nmedia/33/")
                      MediaUrl=MediaUrl.replace("/medias/nmedia/","/nmedia/33/").rsplit("/", 1)[0]
                      SplitCode=2
                      if "/medias/nmedia/" in MediaPath:
                         SplitCode=1
                      MediaUrlOrg=MediaPath.replace("/videothumbnails/","/nmedia/33/")
                      MediaUrlOrg=MediaUrlOrg.replace("/medias/nmedia/","/nmedia/33/").rsplit("/", SplitCode)[0]
                      CheckOk=None
                      UrlOk=None
                      for Qualite in XQualite:
                        
                        if int(Qualite)>=int(MediaQualite):
                          MediaUrl="http://fr.vid.m.%sp.acsta.net" %(QualiteEncode[str(Qualite)])+MediaUrlOrg+"/"+str(MediaId)+"%s_013.mp4" %(MediaEncode[str(Qualite)])
                          if not checkUrl(MediaUrl):
                            MediaUrl="http://s3.vid.web.acsta.net/FR/"+MediaUrlOrg+"/"+str(MediaId)+"%s_013.mp4" %(MediaEncode[str(Qualite)])
                            if checkUrl(MediaUrl):                            
                              UrlOk=True
                              break                                                 
                          else:
                            UrlOk=True 
                            break                           
                          
                        else: #test de l'url pour qualité inférieure...si Ok c'est pas un problème d'URL mais que la qualité demandée n'existe pas....
                              # donc pas besoin de double check dessous
                          MediaUrl="http://fr.vid.m.%sp.acsta.net" %(QualiteEncode[str(Qualite)])+MediaUrlOrg+"/"+str(MediaId)+"%s_013.mp4" %(MediaEncode[str(Qualite)])
                          if not checkUrl(MediaUrl) and not UrlOk:
                            MediaUrl="http://s3.vid.web.acsta.net/FR/"+MediaUrlOrg+"/"+str(MediaId)+"%s_013.mp4" %(MediaEncode[str(Qualite)])
                            if checkUrl(MediaUrl):
                              CheckOk=True 
                              break                      
                          else:
                            CheckOk=True
                            break
                          
                            
                      if not UrlOk and not CheckOk:
                        DataMedia=Allocine_Media(str(MediaId))
                        if DataMedia:
                          for ZQualite in XQualite:
                            if int(ZQualite)>=int(MediaQualite):
                              for ItemMedia in DataMedia:
                                if int(ItemMedia["height"])>=int(ZQualite):
                                  MediaUrl=ItemMedia["href"] 
                                  Qualite= int(ZQualite)                             
                                  UrlOk=1
                                  break
                            if UrlOk:
                              break
                              
                      if UrlOk:
                           if CheckTitre:
                                ListeTitres.append(CheckTitre)
                           if Remplacer>=0:
                             ListeBandeAnnonce[Remplacer]={"typevideo":str(MediaVType),"type":MediaType.encode('utf-8','ignore'),"name":MediaTitre,"key":"Allocine","iso_3166_1":MediaLanguage.upper(),"Language":MediaLanguage,"size":str(Qualite),"id":MediaUrl,"landscape":str(MediaApercu),"LanguageCode":MediaLanguageCode}
                           else:
                            ListeBandeAnnonce.append({"typevideo":str(MediaVType),"type":MediaType.encode('utf-8','ignore'),"name":MediaTitre,"key":"Allocine","iso_3166_1":MediaLanguage.upper(),"Language":MediaLanguage,"size":str(Qualite),"id":MediaUrl,"landscape":str(MediaApercu),"LanguageCode":MediaLanguageCode})
                  #else:
                  #  logMsg("Rejet : (%s)(%s)(%s)" %(MediaLanguageCode,Remplacer,CheckTitre))
  if ListeBandeAnnonce:
    #on range tout ca : d'abord les bandes annonces et par titre....
    ListeBandeAnnonce=sorted(ListeBandeAnnonce,key=operator.itemgetter('typevideo','name','LanguageCode'))
            
  return ListeBandeAnnonce             
        #{u'code': 19574082, u'acShow': {u'nameShort': u'allocinezap', u'code': 0, u'$': u'AlloCin\xe9 Zap'}, u'title': u'American Assassin BONUS VO "Un moyen pour parvenir \xe0 une fin"', u'trailerEmbed': u"<div id='ACEmbed'><iframe src='http://www.allocine.fr/_video/iblogvision.aspx?cmedia=19574082&amp;isApp=true' style='width:480px; height:270px' frameborder='0' allowfullscreen='true'></iframe></div>", u'thumbnail': {u'path': u'/videothumbnails/17/09/20/12/40/3248158.jpg', u'href': u'http://fr.web.img4.acsta.net/videothumbnails/17/09/20/12/40/3248158.jpg'}, u'version': {u'code': 6002, u'original': 0, u'$': u'Anglais'}, u'statistics': {u'commentCount': 0, u'viewCount': 55}, u'titleShort': u'American Assassin BONUS VO "Un moyen pour parvenir \xe0 une fin"', u'runtime': 155, u'type': {u'code': 31018, u'$': u'Making Of'}, u'class': u'video'}
     
        

def Allocine_ChercheFilmSerie(KodiTitre=None,TypeVideo="movie",Annee=None):
      VideoId=None
      if KodiTitre:
        KodiTitre=KodiTitre.split("(",1)[0].replace(":"," ")
        params = {}
        params['count'] = 50
        params['format'] = 'json'
        params['filter'] = TypeVideo
        params['partner'] = Allocinepartner_key
        try:
          params['q'] = KodiTitre #unicodedata.normalize('NFKD', Acteur.split("(")[0]).encode('ascii','xmlcharrefreplace')
        except:
          return VideoId
        response = Allocine_request('search', params)
        try:          
          jsonobject=json.loads(response)
        except:
          jsonobject={}
          
        if jsonobject: 
            #logMsg("Recherche--- (%s)(%s) : %s" %(Annee,KodiTitre,jsonobject),0)
            if(jsonobject.has_key('feed')):
              jsonobject = jsonobject['feed'] 
              total=int(jsonobject.get("totalResults") )
              KodiTitre=try_decode(KodiTitre).lower().replace(" ","")
              if total>0:         
                for Item in jsonobject.get(TypeVideo):                                  
                    VideoId=str(Item.get("code"))                     
                    try:
                      AllocineAnnee=int(Item.get("yearStart"))
                    except:
                      AllocineAnnee=0
                    if AllocineAnnee==0:
                      try:
                        AllocineAnnee=int(Item.get("productionYear"))
                      except:
                        AllocineAnnee=0                      
                    try:
                      AllocineTitre=try_decode(Item.get("title").lower()).replace(" ","")
                    except:
                      AllocineTitre=None
                    try:
                      AllocineTitreOrg=try_decode(Item.get("originalTitle").lower()).replace(" ","")
                    except:
                      AllocineTitreOrg=None
                    #logMsg("Recherche  * (%s) : %s" %(Annee,Item.get("yearStart")),0) 
                    if (AllocineTitre==KodiTitre or AllocineTitreOrg==KodiTitre):
                      if Annee:                                             
                        if AllocineAnnee==int(Annee):
                          break
                      #logMsg("Recherche Ok (%s) : %s" %(Annee,Item),0)  
                      #on a trouvé le bon ! même titre et même année            
                      else:
                        #pas d'année...croisons les doigts !!! episode de serie ??
                        break     
      return VideoId
      
def Allocine_Medias(IdMedia=None,TypeVideo="movie",Saison="1"):
      if IdMedia:
        params = {}
        params['format'] = 'json'
        params['partner'] = Allocinepartner_key
        params['profile'] = 'large'
        params['code'] = str(IdMedia)
        params['striptags']= "trailerEmbed,synopsis"
        params['mediafmt']='mp4-hip'        
        
        SaisonsId=[]
        Medias=[]
        try:
          response = json.loads(Allocine_request(TypeVideo, params))
        except:
          response=None
        if response:
          try:
           SaisonsId=response.get(TypeVideo)["season"]
          except:
           SaisonsId=None
          try:
            Medias=response.get(TypeVideo)["media"]
          except:
            Medias=None
        
          return (Medias,SaisonsId)
          
          #{u'code': 19574082, u'acShow': {u'nameShort': u'allocinezap', u'code': 0, u'$': u'AlloCin\xe9 Zap'}, u'title': u'American Assassin BONUS VO "Un moyen pour parvenir \xe0 une fin"', u'trailerEmbed': u"<div id='ACEmbed'><iframe src='http://www.allocine.fr/_video/iblogvision.aspx?cmedia=19574082&amp;isApp=true' style='width:480px; height:270px' frameborder='0' allowfullscreen='true'></iframe></div>", u'thumbnail': {u'path': u'/videothumbnails/17/09/20/12/40/3248158.jpg', u'href': u'http://fr.web.img4.acsta.net/videothumbnails/17/09/20/12/40/3248158.jpg'}, u'version': {u'code': 6002, u'original': 0, u'$': u'Anglais'}, u'statistics': {u'commentCount': 0, u'viewCount': 55}, u'titleShort': u'American Assassin BONUS VO "Un moyen pour parvenir \xe0 une fin"', u'runtime': 155, u'type': {u'code': 31018, u'$': u'Making Of'}, u'class': u'video'}
      return None,None
        
def Allocine_Media(IdMedia=None):
      if IdMedia:
        params = {}
        params['format'] = 'json'
        params['partner'] = Allocinepartner_key
        params['profile'] = 'medium'
        params['code'] = str(IdMedia)
        params['mediafmt']='mp4-hip'

        response = Allocine_request('media', params)
        if response:
          try:
           return json.loads(response).get("media")["rendition"]
          except:
            return None
      return None
      
def Allocine_ChercheActeur(Acteur=None):
      ActeurId=None
      if Acteur:
        params = {}
        params['format'] = 'json'
        params['filter'] = 'person'
        params['partner'] = Allocinepartner_key
        try:
          check=Acteur.encode('utf8')
        except:
          check=Acteur 
        try:
          params['q'] = urllib.quote(check) # str(Acteur) #unicodedata.normalize('NFKD', Acteur.split("(")[0]).encode('ascii','xmlcharrefreplace')
        except:
          return ActeurId
        response = Allocine_request('search', params)
        try:          
          jsonobject=json.loads(response)
        except:
          jsonobject={}
          
        if jsonobject: 
            if(jsonobject.has_key('feed')):
              jsonobject = jsonobject['feed'] 
              total=int(jsonobject.get("totalResults") )
              if total>0:         
                for Item in jsonobject.get("person"):                                  
                    ActeurId=str(Item.get("code"))                 
                    break
      return ActeurId
           
      
# ----------------------------------------------------------------------        
def checkUrl(url):
    p = urlparse.urlparse(url)
    conn = httplib.HTTPConnection(p.netloc)
    conn.request('HEAD', p.path)
    resp = conn.getresponse()
    return resp.status < 400
     
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD',  try_decode(input_str))
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
    
def Remove_Separator(Chaine=None):
  if Chaine:
    Chaine=Chaine.split("/")[0].rstrip()
    Chaine=Chaine.split("&")[0].rstrip()
    Chaine=Chaine.split(",")[0].rstrip()
    Chaine=Chaine.replace('"','')
    Chaine=Chaine.replace("'",'')
  return Chaine  
        
               
         
                           
def GetSagaTrailers(Liste=None):
     #logMsg("SagaAnnonces : %s" %(Liste),0)
     ListeTrailer=[]
     for Item in Liste:   
        TMDBID=Item.get("tmdbid")
        IMDBID=Item.get("imdbid")
        if not TMDBID:
           TMDBID=get_externalID(IMDBID,"movie")
        if TMDBID:
          Data= getTrailer(TMDBID,"movie",True)
       
          if Data:
             for Item in Data:
               ListeTrailer.append(Item)
     return ListeTrailer    
                             
def getTrailer(ID=None,DbType=None,AnnonceUniquement=None,SaisonID=None):
     Donnees=[]
     ListeTrailer=[]
     XQualite=[720,480,320]
     #https://api.themoviedb.org/3/movie/$$IDFILM$$/videos?api_key=67158e2af1624020e34fd893c881b019&language=French      
     #https://api.themoviedb.org/3/tv/$$IDTV$$/videos?api_key=67158e2af1624020e34fd893c881b019&language=French  
     #https://api.themoviedb.org/3/search/tv?api_key=67158e2af1624020e34fd893c881b019&language=en-US&query=American%20Horror%20Story&page=1
     

     
     try:               
      MediaQualite=int(XQualite[int(SETTING("YoutubeMiniQualite"))])
     except:
      MediaQualite=720 #par défau
     if DbType and ID: 
          #logMsg("getTrailer (%s)(%s)" %(DbType,ID))
          if DbType!="movie":
               query_url ="https://api.themoviedb.org/3/tv/%s/videos?api_key=%s&language=%s&include_adult=true" % (ID,TMDBApiKey,KODILANGCODE)
          else:
               query_url ="https://api.themoviedb.org/3/movie/%s/videos?api_key=%s&language=%s&include_adult=true" % (ID,TMDBApiKey,KODILANGCODE)
          json_data = requestUrlJson(query_url) #en francais
          if json_data:
            Donnees=json_data.get("results")               
          if DbType!="movie":
               query_url ="https://api.themoviedb.org/3/tv/%s/videos?api_key=%s&language=en&include_adult=true" % (ID,TMDBApiKey)
          else:
               query_url ="https://api.themoviedb.org/3/movie/%s/videos?api_key=%s&language=en&include_adult=true" % (ID,TMDBApiKey)
          #logMsg("getTrailer (%s)(%s)(%s)" %(DbType,ID,query_url))
          json_data = requestUrlJson(query_url) #en anglais
          if json_data:
            Donnees=Donnees+json_data.get("results") 
            #{"id":181808,"results":[{"id":"59dca043c3a368623e070253","iso_639_1":"fr","iso_3166_1":"FR","key":"_pkhEAC8YTU","name":"Bande Annonce VOST","site":"YouTube","size":1080,"type":"Trailer"}]}         
          
          if Donnees:
               cc=0
               for Item in Donnees:
                    #{"id":"56609361c3a36875e00047c2","iso_639_1":"en","iso_3166_1":"US","key":"ScY179qa5pM","name":"Season 5 (Hotel) Opening","site":"YouTube","size":1080,"type":"Opening Credits"}
                    Item["sizenull"]=""
                    try:               
                      ItemSize=int(Item.get("size"))
                    except:
                      ItemSize=720 #par défaut
                    try:
                      TypeTrailer=Item.get("type").lower()
                    except:
                      TypeTrailer=""
                    try:
                      Site=Item.get("site").lower()
                    except:
                      Site=""  
                      
                    if SaisonID:
                      Nom=Item.get("name")
                      if Nom:
                        data=re.search(r"Season (.{1,3}) ", Nom)
                        if data:
                          try:
                            SaisonTMDB=int(data.group(1))
                          except:
                            SaisonTMDB=0
                          if SaisonTMDB!=int(SaisonID):
                            Site="rejet"
                    #logMsg("YT TypeTrailer (%s)(%s)(%s)(%s)(%s)" %(ID,TypeTrailer,Item.get("key"),Site,ItemSize),0)
                    if Site=="youtube" and ItemSize>=MediaQualite and (TypeTrailer=="trailer" or not AnnonceUniquement):
                         Item["position"]=str(cc) 
                         Item["id"]='plugin://plugin.video.youtube/play/?video_id=%s' %(Item["key"])                         
                         Item["landscape"]="http://img.youtube.com/vi/%s/hqdefault.jpg" %(Item["key"]) 
                         Item["key"]="YouTube"      
                         ListeTrailer.append(Item)
                         cc=cc+1
     return ListeTrailer
                    
  

def getRuntime(ItemId=None,TypeID=None):
    RuntimeDB= ""
    query_url=""
    xxx=""
    if ItemId:  xxx=get_externalID(ItemId,TypeID)
    if xxx:
      if TypeID=="movie":
          query_url = "https://api.themoviedb.org/3/movie/%s?api_key=%s&include_adult=true" % (xxx,TMDBApiKey)
      if TypeID=="episode":
         query_url = "https://api.themoviedb.org/3/tv/%s?api_key=%s&include_adult=true" % (xxx,TMDBApiKey)
    
      json_data = requestUrlJson(query_url)      
    
      if json_data:
        RuntimeDB = json_data['runtime']        
                  
    return str(RuntimeDB)

def get_uniqueid(ItemId=None,DbType=None):
  #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.GetMovieDetails","params":{"movieid":221,"properties":["imdbnumber","uniqueid"]},"id":"1"}    
  json_result = getJSON('VideoLibrary.GetMovieDetails', '{ "movieid":%d,"properties":["uniqueid"] }' %(int(ItemId)))
  if json_result:
    UniqueId=json_result.get("uniqueid")
    if UniqueId:
       IMDBNUMBER=UniqueId.get("imdb")
       TMDBNumber=UniqueId.get("tmdb")
       UNKNNUMBER=UniqueId.get("unknown")
       if IMDBNUMBER:
        return IMDBNUMBER
       if UNKNNUMBER and ("tt" in UNKNNUMBER):
        return IMDBNUMBER
       if TMDBNumber:
        return TMDBNumber
    
def get_externalID(ItemId=None,ismovie=None):
   externalXX=""
   ItemIdR=""
   allID=[]
   query_url=""
   if ismovie=="episode":
         json_result2 = getJSON2("VideoLibrary.GetTvShows", '{"filter":{"field":"title","operator":"is","value":"%s"},"properties":["imdbnumber"]}' %(ItemId))
         if json_result2:
           for item in json_result2:
              ItemId=item.get("imdbnumber")
         else:
           ItemId=None
   else:
     if ItemId.find('tt')==-1 and ismovie=="movie": #pas IMDB donc TMDB direct
       return str(ItemId)
   if ItemId:
     if ItemId.find('tt')==-1: #pas IMDB mais movie et TMDB direct
       externalXX="tvdb_id"
     else:
       externalXX="imdb_id"
     query_url = "https://api.themoviedb.org/3/find/%s?api_key=%s&language=%s&external_source=%s&include_adult=true" % (ItemId,TMDBApiKey,KODILANGCODE,externalXX)
     
     json_data = requestUrlJson(query_url)
 
      
     if json_data:
           if ismovie!="movie": 
            allID=json_data.get("tv_results")
           else:
            allID=json_data.get("movie_results")
           if allID and len(allID)>0:
               for Test in allID:
                 	  ItemIdR=Test.get("id")
                 	  break
   return str(ItemIdR)
   

		
#get external id pour themoviedb
# si tItemListeXXX -> Imdb
#sinon tvdb
#https://api.themoviedb.org/3/find/268592?api_key=67158e2af1624020e34fd893c881b019&language=en-US&external_source=tvdb_id ou imdb_id ou tvrage_id ou freebase_id

#get episodes
#https://api.themoviedb.org/3/tv/48866/season/1?api_key=67158e2af1624020e34fd893c881b019&language=en-US
#48866 id chez themoviedb
#1 : numero de saison

def VueActuelle(containerprefix=""):
    contenu= ""
    if xbmc.getCondVisibility("Container.Content(episodes)"):
        contenu= "episodes"
    elif xbmc.getCondVisibility("Container.Content(movies) + !String.Contains(Container.FolderPath,setid=)"):
        contenu= "movies"
    elif xbmc.getCondVisibility("[Container.Content(sets) | String.IsEqual(Container.Folderpath,videodb://movies/sets/)] + !String.Contains(Container.FolderPath,setid=)"):
        contenu= "sets"
    elif xbmc.getCondVisibility("String.Contains(Container.FolderPath,setid=)"):
        contenu= "setmovies"
    elif xbmc.getCondVisibility("!String.IsEmpty(Container.Content) + !String.IsEqual(Container.Content,pvr)"):
        contenu= xbmc.getInfoLabel("Container.Content")
    elif xbmc.getCondVisibility("Container.Content(tvshows)"):
        contenu= "tvshows"
    elif xbmc.getCondVisibility("Container.Content(seasons)"):
        contenu= "seasons"
    elif xbmc.getCondVisibility("Container.Content(musicvideos)"):
        contenu= "musicvideos"
    elif xbmc.getCondVisibility("Container.Content(songs) | String.IsEqual(Container.FolderPath,musicdb://singles/)"):
        contenu= "songs"
    elif xbmc.getCondVisibility("Container.Content(artists)"):
        contenu= "artists"
    elif xbmc.getCondVisibility("Container.Content(albums)"):
        contenu= "albums"
    elif xbmc.getCondVisibility("Window.IsActive(MyPVRChannels.xml) | Window.IsActive(MyPVRGuide.xml) | Window.IsActive(MyPVRSearch.xml) | Window.IsActive(pvrguideinfo)"):
        contenu= "tvchannels"
    elif xbmc.getCondVisibility("Window.IsActive(MyPVRRecordings.xml) | Window.IsActive(MyPVRTimers.xml) | Window.IsActive(pvrrecordinginfo)"):
        contenu= "tvrecordings"
    elif xbmc.getCondVisibility("Window.IsActive(programs) | Window.IsActive(addonbrowser)"):
        contenu= "addons"
    elif xbmc.getCondVisibility("Window.IsActive(pictures)"):
        contenu= "pictures"
    elif xbmc.getCondVisibility("Container.Content(genres)"):
        contenu= "genres"
    elif xbmc.getCondVisibility("Container.Content(files)"):
        contenu= "files"
    
    return contenu

def ModeVues(content_type=None, current_view=None):
        label = ""
        ListeVues = []
        ListeVuesTriee=[] 
        choixpossibles=[]
         
        views_file = xbmc.translatePath('special://skin/extras/views.xml').decode("utf8")
        if xbmcvfs.exists(views_file):
            doc = parse(views_file)
            listing = doc.documentElement.getElementsByTagName('view')
            VueActuelle=try_decode(xbmc.getInfoLabel("Container.Viewmode"))
            
            for view in listing:
                label = xbmc.getLocalizedString(int(view.attributes['languageid'].nodeValue))
                viewid = view.attributes['value'].nodeValue
                mediatypes = view.attributes['type'].nodeValue.lower().split(",")
                if (("all" in mediatypes or content_type.lower() in mediatypes) and
                    (not "!" + content_type.lower() in mediatypes)):
                    image = "special://skin/extras/viewthumbs/%s.jpg" % viewid
                    ListeVues.append([label,viewid,mediatypes,image])
                    
            ListeVuesTriee=sorted(ListeVues, key=lambda x:x[0],reverse=False)
           
            ListeVues=[]
            for view in ListeVuesTriee:
                    label = view[0]
                    viewid = view[1]
                    mediatypes = view[2]                
                    image = view[3]
                    if VueActuelle==try_decode(label):
                          label="[COLOR=yellow][B]"+label+"[/B][/COLOR]"
                         
                    if KODI_VERSION>=17: 
                         Elements = xbmcgui.ListItem(label=label, iconImage=image,label2="selectionnevue")
                         Elements.setProperty("viewid", viewid)
                         Elements.setProperty("icon", image)
                         ListeVues.append(Elements)
                    else:                          
                       ListeVues.append(label)
                    choixpossibles.append(str(viewid))
        dialogC = xbmcgui.Dialog()
        if ListeVuesTriee:
            result=dialogC.select(xbmc.getLocalizedString(629), ListeVues)
            if result>=0:
                 vue = str(choixpossibles[result])
                 xbmc.executebuiltin("Container.SetViewMode(%s)" % vue)
                 xbmc.executebuiltin("SetFocus(55)")     
                        
def ModeVuesMenu(content_type=None, current_view=None):
        label = ""
        ListeVues = []
        ListeVuesTriee=[] 
        choixpossibles=[]
        
        #logMsg("ContentType (%s)" %(content_type)) 
        views_file = xbmc.translatePath('special://skin/extras/views.xml').decode("utf8")
        if xbmcvfs.exists(views_file):
            doc = parse(views_file)
            listing = doc.documentElement.getElementsByTagName('view')
            VueActuelle=try_decode(xbmc.getInfoLabel("Container.Viewmode"))
            
            for view in listing:
                label = xbmc.getLocalizedString(int(view.attributes['languageid'].nodeValue))
                viewid = view.attributes['value'].nodeValue
                mediatypes = view.attributes['type'].nodeValue.lower().split(",")
                if (("all" in mediatypes or content_type.lower() in mediatypes) and
                    (not "!" + content_type.lower() in mediatypes)):
                    image = "special://skin/extras/viewthumbs/%s.jpg" % viewid
                    ListeVues.append([label,viewid,mediatypes,image])
                    
            ListeVuesTriee=sorted(ListeVues, key=lambda x:x[0],reverse=False)
           
            ListeVues=[]
            for view in ListeVuesTriee:
                    label = view[0] 
                    viewid = view[1]
                    mediatypes = view[2]                
                    image = view[3]
                    if VueActuelle==try_decode(label):
                          label="[COLOR=yellow][B]"+label+"[/B][/COLOR]"
                         
                     
                    Elements = xbmcgui.ListItem(label=label, iconImage=image,label2="selectionnevue",path="RunScript(script.iconmixtools,setviewmenu=True&id=%s)" % viewid)
                    Elements.setProperty("viewid", viewid)
                    Elements.setProperty("icon", image)
                    ListeVues.append(Elements)
                    #logMsg("Vues : (%s)(%s)(%s)" %(current_view,viewid,label))
            if len(ListeVues)>0:
              return ListeVues
        return None     
                         
                  	                    	  
# --------------------------------------------------------------------------------------------------
def vidercache(quelcache=None):
  
  if quelcache:
      savepath=ADDON_DATA_PATH+"/%s" %(str(quelcache))
      if not os.path.exists(savepath):
          logMsg("(vidange) repertoire introuvable : "+str(savepath),0)
          return
      else:
          shutil.rmtree(savepath)
          logMsg("(vidange) suppression effectuee de "+str(savepath),0)

# --------------------------------------------------------------------------------------------------


  
def requestUrlJson(query_url,XmlUrl=None):
  #logMsg("requestUrlJson :"+str(query_url),0)
  try:
    req = urllib2.Request(query_url.replace(" ","%20")) 
  except :
    str_response=None
    logMsg("Erreur1  urllib2.Request(query_url) --> " + str(query_url),0)
  if req:
    user_agent = 'Dalvik/1.6.0 (Linux; U; Android 4.2.2; Nexus 4 Build/JDQ39E)'
    req.add_header('User-agent',user_agent)
             
  try:
    reponse = urllib2.urlopen(req, timeout = 1)
    #reponse = urllib.request.urlopen(query_url, None, 2)
  except:
    reponse=None
    logMsg("Erreur2  urllib2.urlopen(query_url) --> " + str(query_url),0)
  
  json_data=None
  if reponse:
        try:
          str_response = reponse.read().decode('utf8')
        except :
          str_response=None
          logMsg("Erreur  requestUrlJson introuvable  --> " + str(query_url),0)

        if str_response :
            if not XmlUrl:  
              try:
               json_data = json.loads(str_response)
              except:
               json_data=None
               logMsg("Erreur  requestUrlJson  vide --> " + str(query_url),0)
            else:
               #xml    = ET.parse(str_response)
               xml=ET.fromstring(str_response)
               jsondata = xml2json.elem2json(xml, None)
               json_data = json.loads(jsondata)
               #json_data = parseXmlToJson(xml)
               
  return json_data
# --------------------------------------------------------------------------------------------------
    
def getJSON(method,params):
    json_response = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method" : "%s", "params": %s, "id":1 }' %(method, try_encode(params)))
    jsonobject = json.loads(json_response.decode('utf8','replace'))
    if(jsonobject.has_key('result')):
        jsonobject = jsonobject['result']
        if isinstance(jsonobject, list):
            return jsonobject
        if jsonobject.has_key('files'):
            return jsonobject['files']
        elif jsonobject.has_key('movies'):
            return jsonobject['movies']
        elif jsonobject.has_key('tvshows'):
            return jsonobject['tvshows']
        elif jsonobject.has_key('seasons'):
            return jsonobject['seasons']
        elif jsonobject.has_key('episodes'):
            return jsonobject['episodes']
        elif jsonobject.has_key('musicvideos'):
            return jsonobject['musicvideos']
        elif jsonobject.has_key('channels'):
            return jsonobject['channels']
        elif jsonobject.has_key('recordings'):
            return jsonobject['recordings']
        elif jsonobject.has_key('timers'):
            return jsonobject['timers']
        elif jsonobject.has_key('channeldetails'):
            return jsonobject['channeldetails']
        elif jsonobject.has_key('recordingdetails'):
            return jsonobject['recordingdetails']
        elif jsonobject.has_key('songs'):
            return jsonobject['songs']
        elif jsonobject.has_key('albums'):
            return jsonobject['albums']
        elif jsonobject.has_key('songdetails'):
            return jsonobject['songdetails']
        elif jsonobject.has_key('albumdetails'):
            return jsonobject['albumdetails']
        elif jsonobject.has_key('artistdetails'):
            return jsonobject['artistdetails']
        elif jsonobject.get('favourites'):
            return jsonobject['favourites']
        elif jsonobject.has_key('tvshowdetails'):
            return jsonobject['tvshowdetails']
        elif jsonobject.has_key('episodedetails'):
            return jsonobject['episodedetails']
        elif jsonobject.has_key('moviedetails'):
            return jsonobject['moviedetails']
        elif jsonobject.has_key('setdetails'):
            return jsonobject['setdetails']
        elif jsonobject.has_key('musicvideodetails'):
            return jsonobject['musicvideodetails']
        elif jsonobject.has_key('sets'):
            return jsonobject['sets']
        elif jsonobject.has_key('video'):
            return jsonobject['video']
        elif jsonobject.has_key('artists'):
            return jsonobject['artists']
        elif jsonobject.has_key('channelgroups'):
            return jsonobject['channelgroups']
        elif jsonobject.get('sources'):
            return jsonobject['sources']
        elif jsonobject.has_key('addons'):
            return jsonobject['addons']
        elif jsonobject.has_key('item'):
            return jsonobject['item']
        elif jsonobject.has_key('genres'):
            return jsonobject['genres']
        elif jsonobject.has_key('value'):
            return jsonobject['value']
        else:
            return {}

    else:
        return {}
        
def getJSON2(method,params):
    json_response = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method" : "%s", "params": %s, "id":1 }' %(method, params))
    jsonobject = json.loads(json_response.decode('utf8','replace'))
    if(jsonobject.has_key('result')):
        jsonobject = jsonobject['result']
        if isinstance(jsonobject, list):
            return jsonobject
        if jsonobject.has_key('files'):
            return jsonobject['files']
        elif jsonobject.has_key('movies'):
            return jsonobject['movies']
        elif jsonobject.has_key('tvshows'):
            return jsonobject['tvshows']
        elif jsonobject.has_key('episodes'):
            return jsonobject['episodes']
        elif jsonobject.has_key('musicvideos'):
            return jsonobject['musicvideos']
        elif jsonobject.has_key('channels'):
            return jsonobject['channels']
        elif jsonobject.has_key('recordings'):
            return jsonobject['recordings']
        elif jsonobject.has_key('timers'):
            return jsonobject['timers']
        elif jsonobject.has_key('channeldetails'):
            return jsonobject['channeldetails']
        elif jsonobject.has_key('recordingdetails'):
            return jsonobject['recordingdetails']
        elif jsonobject.has_key('songs'):
            return jsonobject['songs']
        elif jsonobject.has_key('albums'):
            return jsonobject['albums']
        elif jsonobject.has_key('songdetails'):
            return jsonobject['songdetails']
        elif jsonobject.has_key('albumdetails'):
            return jsonobject['albumdetails']
        elif jsonobject.has_key('artistdetails'):
            return jsonobject['artistdetails']
        elif jsonobject.get('favourites'):
            return jsonobject['favourites']
        elif jsonobject.has_key('tvshowdetails'):
            return jsonobject['tvshowdetails']
        elif jsonobject.has_key('episodedetails'):
            return jsonobject['episodedetails']
        elif jsonobject.has_key('moviedetails'):
            return jsonobject['moviedetails']
        elif jsonobject.has_key('setdetails'):
            return jsonobject['setdetails']
        elif jsonobject.has_key('musicvideodetails'):
            return jsonobject['musicvideodetails']
        elif jsonobject.has_key('sets'):
            return jsonobject['sets']
        elif jsonobject.has_key('video'):
            return jsonobject['video']
        elif jsonobject.has_key('artists'):
            return jsonobject['artists']
        elif jsonobject.has_key('channelgroups'):
            return jsonobject['channelgroups']
        elif jsonobject.get('sources'):
            return jsonobject['sources']
        elif jsonobject.has_key('addons'):
            return jsonobject['addons']
        elif jsonobject.has_key('item'):
            return jsonobject['item']
        elif jsonobject.has_key('genres'):
            return jsonobject['genres']
        elif jsonobject.has_key('value'):
            return jsonobject['value']
        else:
            return {}

    else:
        return {}
        
def decode_json(jsonobject=None):
    if(jsonobject.has_key('result')):
        jsonobject = jsonobject['result']
        if isinstance(jsonobject, list):
            return jsonobject
        if jsonobject.has_key('files'):
            return jsonobject['files']
        elif jsonobject.has_key('movies'):
            return jsonobject['movies']
        elif jsonobject.has_key('tvshows'):
            return jsonobject['tvshows']
        elif jsonobject.has_key('episodes'):
            return jsonobject['episodes']
        elif jsonobject.has_key('musicvideos'):
            return jsonobject['musicvideos']
        elif jsonobject.has_key('channels'):
            return jsonobject['channels']
        elif jsonobject.has_key('recordings'):
            return jsonobject['recordings']
        elif jsonobject.has_key('timers'):
            return jsonobject['timers']
        elif jsonobject.has_key('channeldetails'):
            return jsonobject['channeldetails']
        elif jsonobject.has_key('recordingdetails'):
            return jsonobject['recordingdetails']
        elif jsonobject.has_key('songs'):
            return jsonobject['songs']
        elif jsonobject.has_key('albums'):
            return jsonobject['albums']
        elif jsonobject.has_key('songdetails'):
            return jsonobject['songdetails']
        elif jsonobject.has_key('albumdetails'):
            return jsonobject['albumdetails']
        elif jsonobject.has_key('artistdetails'):
            return jsonobject['artistdetails']
        elif jsonobject.get('favourites'):
            return jsonobject['favourites']
        elif jsonobject.has_key('tvshowdetails'):
            return jsonobject['tvshowdetails']
        elif jsonobject.has_key('episodedetails'):
            return jsonobject['episodedetails']
        elif jsonobject.has_key('moviedetails'):
            return jsonobject['moviedetails']
        elif jsonobject.has_key('setdetails'):
            return jsonobject['setdetails']
        elif jsonobject.has_key('musicvideodetails'):
            return jsonobject['musicvideodetails']
        elif jsonobject.has_key('sets'):
            return jsonobject['sets']
        elif jsonobject.has_key('video'):
            return jsonobject['video']
        elif jsonobject.has_key('artists'):
            return jsonobject['artists']
        elif jsonobject.has_key('channelgroups'):
            return jsonobject['channelgroups']
        elif jsonobject.get('sources'):
            return jsonobject['sources']
        elif jsonobject.has_key('addons'):
            return jsonobject['addons']
        elif jsonobject.has_key('item'):
            return jsonobject['item']
        elif jsonobject.has_key('genres'):
            return jsonobject['genres']
        elif jsonobject.has_key('value'):
            return jsonobject['value']
        else:
            return {}

    else:
        return {}


def try_encode(text, encoding="utf8"):
    try:
        return text.encode(encoding,"ignore")
    except:
        return text

def try_decode(text, encoding="utf8"):
    try:
        return text.decode(encoding,"ignore")
    except:
        return text
        

def logMsg(msg, level = 0):
    if WINDOW.getProperty("IconMixTools.enableDebugLog") == "true" or level == 0:
        if isinstance(msg, unicode):
            msg = msg.encode('utf8')
        if "exception" in msg.lower() or "error" in msg.lower():
            xbmc.log("IconMixTools addon --> " + msg, level=xbmc.LOGERROR)
            #print_exc()
        else:
            xbmc.log("IconMixTools addon --> " + msg, level=xbmc.LOGNOTICE)

def DirStru(filename):
   try:
        erreur=os.makedirs(os.path.dirname(filename))        
   except: 
        erreur="1"
   return erreur 
    
def setJSON(method,params):
    json_response = xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "method" : "%s", "params": %s, "id":1 }' %(method, try_encode(params)))
    jsonobject = json.loads(json_response.decode('utf8','replace'))
    return jsonobject
    
# ----------- ---------- MUSIQUE --------- -----------------    
def remove_text_inside_brackets(text, brackets="()[]"):
    count = [0] * (len(brackets) // 2) # count open/close brackets
    saved_chars = []
    for character in text:
        for i, b in enumerate(brackets):
            if character == b: # found bracket
                kind, is_close = divmod(i, 2)
                count[kind] += (-1)**is_close # `+1`: open, `-1`: close
                if count[kind] < 0: # unbalanced bracket
                    count[kind] = 0  # keep it
                else:  # found bracket to remove
                    break
        else: # character is not a [balanced] bracket
            if not any(count): # outside brackets
                saved_chars.append(character)
    return ''.join(saved_chars)  
  
def GetMusicAlbumsInfos(Artiste="",Album=""): 
   ArtBrainzId=None 
   ArtisteId=None 
   AlbumCover=None
   AlbumBack=None
   AlbumCd=None 
   Resultat={}
     
   
   if Artiste:
      if not Album:
        Album=""
      else:
        Album=remove_text_inside_brackets(Album)
      urlTVDB="http://www.theaudiodb.com/api/v1/json/195011/searchalbum.php?s=%s&a=%s" %(Artiste,Album)
      for cpt in range(0,3):        
        data=requestUrlJson(urlTVDB)
        if data:  
          DataItem=data.get("album")
          if not DataItem:
            if 'The ' in Album:
               Album=Album.replace('The ','')
               urlTVDB="http://www.theaudiodb.com/api/v1/json/195011/searchalbum.php?s=%s&a=%s" %(Artiste,Album)
            xbmc.sleep(10)
          else:
            break
        else:          
          break
         
         
      if DataItem:  
           
        for Item in DataItem:
            Resultat["ArtBrainzId"]=Item.get("strMusicBrainzID")            
            Resultat["ArtisteId"]=Item.get("strMusicBrainzArtistID")
            Resultat["AlbumCover"]=Item.get("strAlbumThumb")
            Resultat["AlbumBack"]=Item.get("strAlbumThumbBack")
            Resultat["AlbumCd"]=Item.get("strAlbumCDart") 
            Resultat["ArtisteTVDBID"]=Item.get("idArtist")
            Resultat["AlbumTVDBID"]=Item.get("idAlbum")
            if KODILANGUAGE[0:4]=='Fren' :
             Resultat["AlbumInfo"]=Item.get("strDescriptionFR")
            if not Resultat.get("AlbumInfo"): 
             Resultat["AlbumInfo"]=Item.get("strDescriptionEN")
            break
    
               
   return Resultat
  

def GetMusicFicheArtiste(Artiste=None,ArtisteId=None,Force=None):
  save_data={}
  ArtisteTVDBID=None
  MAJ=1
  
  
  if ArtisteId and int(ArtisteId)>0:
    savepath=ADDON_DATA_PATH+"/music/artiste%s/artiste" %(str(ArtisteId))
    #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"AudioLibrary.GetAlbums","params":{"filter":{"artistid":61}},"id":1}
    if xbmcvfs.exists(savepath) and not Force :
        with open(savepath) as data_file:
          try:
            save_data = json.load(data_file)
          except:
            save_data={}
          data_file.close()
          if Artiste==save_data.get("ArtistName"):
            MAJ=0
          
     
    if MAJ==1: #creation fiche artiste
      #on recherche un nom d'album pour diminuer les doublons lors de la recherche de l'artiste
        #allAlbums = getJSON('AudioLibrary.GetAlbums', '{ "limits":{"end":1},"filter":{"artistid":%d},"properties":["artist","musicbrainzalbumid"]}' %(int(ArtisteId))) 
        if ArtisteTVDBID:
          urlTVDB="http://www.theaudiodb.com/api/v1/json/195011/artist.php?i=%s" %(str(ArtisteTVDBID))
        else:
          urlTVDB="http://www.theaudiodb.com/api/v1/json/195011/search.php?s=%s" %(unidecode(remove_text_inside_brackets(Artiste)))
        data=requestUrlJson(urlTVDB)
        if data.get("artists"):
          for DataItem in data.get("artists"):
            if KODILANGUAGE[0:4]=='Fren' :
               save_data["ArtistBio"]=DataItem.get("strBiographyFR")
            if not save_data.get("ArtistBio"): 
               save_data["ArtistBio"]=DataItem.get("strBiographyEN")
            save_data["ArtistThumb"]=DataItem.get("strArtistThumb")
            save_data["ArtistLogo"]=DataItem.get("strArtistLogo") 
            save_data["ArtistBanner"]=DataItem.get("strArtistBanner") 
            save_data["ArtistFanart"]=DataItem.get("strArtistFanart") 
            save_data["ArtistFanart2"]=DataItem.get("strArtistFanart2") 
            save_data["ArtistFanart3"]=DataItem.get("strArtistFanart3") 
            save_data["ArtistBrainzID"]=DataItem.get("strMusicBrainzID")
            save_data["ArtistTVDBID"]=DataItem.get("idArtist")
            save_data["ArtistName"]=DataItem.get("strArtist")
            break
            
          if save_data.get("ArtistBrainzID"): # and (not save_data.get("ArtistBanner")  or not save_data.get("ArtistLogo")):
            #or not save_data["AlbumBack"]
              UrlFanartTv="http://webservice.fanart.tv/v3/music/%s?api_key=769f122ee8aba06f4a513830295f2bc0" %(save_data["ArtistBrainzID"]) #infos completes
              json_data = requestUrlJson(UrlFanartTv)  
              
              if json_data:
                if not save_data.get("ArtistBanner"):
                  try:
                    save_data["ArtistBanner"]=json_data.get("musicbanner")[0].get("url")
                  except:
                    save_data["ArtistBanner"]=None
                #if not save_data["AlbumBack"]:
                #  save_data["AlbumBack"]=json_data["albums"][save_data["ArtBrainzId"]]["albumback"]["id"][0]
                if not save_data.get("ArtistLogo"):
                  try:
                    save_data["ArtistLogo"]=json_data.get("hdmusiclogo")[0].get("url")
                  except:
                    save_data["ArtistLogo"]=None
                fanarts=json_data.get("artistbackground") 
                
                listefanarts=[]
                if fanarts:
                  for itemfanart in fanarts:
                    listefanarts.append(itemfanart.get("url"))
                  
                try:
                  save_data["fanarts"]=listefanarts
                except:
                  save_data["fanarts"]=None 
                

                #save_data["BrainzArts"]=json_data     
        else:
          save_data["ArtistName"]=unidecode(Artiste)
   
           

        if SETTING("cachemusic")=="false":
            erreur=DirStru(savepath) 
            save_data["kodiArtisteId"]=str(ArtisteId)
            with io.open(savepath, 'w+', encoding='utf8') as outfile: 
              str_ = json.dumps(save_data,indent=4, sort_keys=True,separators=(',', ':'), ensure_ascii=False)
              outfile.write(to_unicode(str_))
    if save_data.get("ArtistBanner"): 
       savepath=ADDON_DATA_PATH+"/music/artiste%s/banner.jpg" %(str(ArtisteId))
       if not xbmcvfs.exists(savepath) or Force:
         try:
           urllib.urlretrieve(save_data.get("ArtistBanner"),savepath)              
         except:
           #logMsg("Banniere impossible : "+str(savepath)+":"+str(save_data.get("ArtistBanner")),0)
           savepath=""
    if save_data.get("ArtistLogo"): 
       savepath=ADDON_DATA_PATH+"/music/artiste%s/clearlogo.jpg" %(str(ArtisteId))
       if not xbmcvfs.exists(savepath) or Force:
         try:
           urllib.urlretrieve(save_data.get("ArtistLogo"),savepath)              
         except:
           #logMsg("ClearLogo impossible : "+str(savepath)+":"+str(save_data.get("ArtistLogo")),0)
           savepath=""
   
    return save_data  
  
  
def GetMusicFicheAlbum(AlbumId=None,Cover=None,GetArtistData=None,PlayerActif=None,Chanson=None,Force=None,IdArtiste=None):
  Donnees=[] 
  save_data={}
  albumIdBrainz=[]
  ThumbNail=None
  ArtisteData=[]
  Artiste=""
  ArtisteTVDBID=None
  ArtisteId=None
  MAJ=1
  #atchung! si cover vide alors on met a jour :)
  
  if Chanson:
    #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"AudioLibrary.GetSongDetails","params":{"songid":5975,"properties":["albumid"]},"id":1}
    Donnees = getJSON('AudioLibrary.GetSongDetails', '{ "songid":%d,"properties":["albumid","artistid","artist","album"]}' %(int(AlbumId))) 
    if Donnees:
        
        AlbumId=Donnees.get("albumid")
        Artiste=Donnees.get("artist")[0]
        if not IdArtiste:          
         ArtisteId=Donnees.get("artistid")[0]
        else:
          ArtisteId=IdArtiste
        AlbumLabel=remove_text_inside_brackets(Donnees.get("album"))
        GetArtistData=1
        
  if not AlbumId and PlayerActif:
    #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"Player.GetItem","params":{"playerid":0,"properties":["artistid","albumid"]},"id":1}
    Donnees = getJSON('Player.GetItem', '{ "playerid":0,"properties":["albumid","artistid","artist","album"]}') 
    if Donnees:
        AlbumId=Donnees.get("albumid")
        Artiste=Donnees.get("artist")[0]
        ArtisteId=Donnees.get("artistid")[0]
        AlbumLabel=remove_text_inside_brackets(Donnees.get("album"))
        GetArtistData=1
  
  if AlbumId  and int(AlbumId)>0:
    if not Donnees or not ArtisteId: 
      Donnees = getJSON('AudioLibrary.GetAlbumDetails', '{ "albumid":%d,"properties":["artist","artistid","thumbnail"]}' %(int(AlbumId))) 
      if Donnees.get("label"): 
        AlbumLabel=remove_text_inside_brackets(Donnees.get("label"))
       
        if not IdArtiste:          
         ArtisteId=Donnees.get("artistid")[0]
        else:
          ArtisteId=IdArtiste
        Artiste=Donnees.get("artist")[0]
        ThumbNail=Donnees.get("thumbnail")
        if ThumbNail:
          ThumbNail=ThumbNail.replace("image://","").decode('utf8')
        
    if Donnees:
        if GetArtistData!=0:
          ArtisteData=GetMusicFicheArtiste(Artiste,ArtisteId,Force)  
          
        savepath=ADDON_DATA_PATH+"/music/artiste%s/album%s" %(str(ArtisteId),str(AlbumId))
        if xbmcvfs.exists(savepath) and not Force:
            with open(savepath) as data_file:
              save_data = json.load(data_file)
              data_file.close()
              if AlbumLabel==save_data.get("label"):
                MAJ=0
        if MAJ==1  : #creation fiche artiste
          #on recherche un nom d'album pour diminuer les doublons lors de la recherche de l'artiste  
            Details=GetMusicAlbumsInfos(unidecode(Artiste),unidecode(AlbumLabel))
            if Details:
              ArtisteTVDBID=Details.get("ArtisteTVDBID")
              save_data["ArtisteTVDBID"]=Details.get("ArtisteTVDBID")
              save_data["AlbumTVDBID"]=Details.get("AlbumTVDBID")
              save_data["ArtBrainzId"]=Details.get("ArtBrainzId")
              save_data["AlbumCover"]=Details.get("AlbumCover")
              save_data["AlbumBack"]=Details.get("AlbumBack")
              save_data["AlbumCd"]=Details.get("AlbumCd")
              save_data["AlbumInfo"]=Details.get("AlbumInfo")
              
              if save_data.get("ArtBrainzId") and (not save_data.get("AlbumCover")  or not save_data.get("AlbumCd")):
                #or not save_data["AlbumBack"]
                  UrlFanartTv="http://webservice.fanart.tv/v3/music/albums/%s?api_key=769f122ee8aba06f4a513830295f2bc0" %(save_data["ArtBrainzId"]) #infos completes
                  json_data = requestUrlJson(UrlFanartTv)  
                  
                  if json_data:
                    if not save_data.get("AlbumCover"):
                      try:
                        save_data["AlbumCover"]=json_data.get(save_data.get("ArtBrainzId")).get("albumcover")[0].get("url")
                      except:
                        save_data["AlbumCover"]=None
                    #if not save_data["AlbumBack"]:
                    #  save_data["AlbumBack"]=json_data["albums"][save_data["ArtBrainzId"]]["albumback"]["id"][0]
                    if not save_data.get("AlbumCd"):
                      try:
                        save_data["AlbumCd"]=json_data.get(save_data.get("ArtBrainzId")).get("cdart")[0].get("url")
                      except:
                        save_data["AlbumCd"]=None
                    save_data["BrainzArts"]=json_data         
            

            save_data["label"]=AlbumLabel
            
        if not save_data.get("AlbumCover")  and ThumbNail:
           save_data["AlbumCover"]=ThumbNail
           
        if SETTING("cachemusiccover")=="true":    
          savepathcover=ADDON_DATA_PATH+"/music/artiste%s/album%scover.jpg" %(str(ArtisteId),str(AlbumId))
          if not xbmcvfs.exists(savepathcover):
            try:
             urllib.urlretrieve(save_data.get("AlbumCover"),savepathcover)              
            except:
             savepathcover=save_data.get("AlbumCover")       
            save_data["AlbumCover"]=savepathcover      
  
              
        if MAJ==1 and SETTING("cachemusic")=="false":
            erreur=DirStru(savepath)             
            save_data["kodiArtisteId"]=str(ArtisteId)
            save_data["Artiste"]=unidecode(Artiste)
            #save_data["albumsdetails"]=albumIdBrainz
            with io.open(savepath, 'w+', encoding='utf8') as outfile: 
              str_ = json.dumps(save_data,indent=4, sort_keys=True,separators=(',', ':'), ensure_ascii=False)
              outfile.write(to_unicode(str_)) 
              
  return save_data,ArtisteData
  
  
def CheckArtisteAlbums(ArtisteId=None,Force=None,ShowProgress=None):
  ListeItem=[]
  ArtisteData=[]
  dp=None
  if ArtisteId:
    json_result = getJSON('AudioLibrary.GetAlbums', '{ "filter":{"artistid":%d},"properties":["artist","musicbrainzalbumid","thumbnail","playcount","rating"]}' %(int(ArtisteId))) 
    #{u'rating': 0, u'artist': [u'Armin van Buuren'], u'thumbnail': u'image://music@Y%3a%5cMusic%5cArminVanBuuren%5cArmin%20van%20Buuren%20-%20A%20State%20Of%20Trance%20714.mp3/', u'label': u'Singles', u'albumid': 129, u'playcount': 0, u'musicbrainzalbumid': u''}
    if json_result:         
        savepath=ADDON_DATA_PATH+"/music/artiste%s/artiste" %(str(ArtisteId))        
        if not xbmcvfs.exists(savepath) or Force:
            Titre="Mise a jour"
            if ShowProgress:
              dp = xbmcgui.DialogProgress()
              dp.create("IconMixTools",__language__( 32509 ),"") 
        NbItems=len(json_result)
        Compteur=0
        FanartTab=[]
        cck=0
        for item in json_result:
              Progres=(Compteur*100)/NbItems
              Compteur=Compteur+1
              if dp: dp.update(Progres,__language__( 32509 )+item.get("artist")[0],"(%d/%d)[CR]%s" %(Compteur,NbItems,item.get("label")))
              ItemListe = xbmcgui.ListItem(label=item.get("label"),iconImage=item.get("thumbnail"))
              
              if not ArtisteData:                
                AlbumData,ArtisteData=GetMusicFicheAlbum(item.get("albumid"),item.get("thumbnail"),1,None,None,Force,ArtisteId)
                if ArtisteData:
                  FanartTab=[ArtisteData.get("ArtistFanart"),ArtisteData.get("ArtistFanart2"),ArtisteData.get("ArtistFanart3")]
              else:
                AlbumData,ArtisteDataNull=GetMusicFicheAlbum(item.get("albumid"),item.get("thumbnail"),0,None,None,Force,ArtisteId)
              if AlbumData:
                
                if not AlbumData.get("AlbumCover"):
                 ItemListe.setProperty("AlbumCover",FanartTab[cck])
                else:
                 ItemListe.setProperty("AlbumCover",AlbumData.get("AlbumCover")) 
                 
                ItemListe.setProperty("AlbumBack",AlbumData.get("AlbumBack"))  
                
                if not AlbumData.get("AlbumCd"):
                   if AlbumData.get("AlbumCover"):
                     ItemListe.setProperty("AlbumCd",AlbumData.get("AlbumCover"))
                   else:
                     if item.get("thumbnail"):
                       ItemListe.setProperty("AlbumCd",item.get("thumbnail"))
                     else:
                       ItemListe.setProperty("AlbumCd",FanartTab[cck])                   
                else:                    
                   ItemListe.setProperty("AlbumCd",AlbumData.get("AlbumCd"))
                ItemListe.setProperty("AlbumInfo",AlbumData.get("AlbumInfo"))
                
                ItemListe.setProperty("AlbumFanart",FanartTab[cck])
                cck=cck+1
                if cck>2: cck=0
              if ArtisteData:
                ItemListe.setProperty("ArtistBio",ArtisteData.get("ArtistBio"))
                ItemListe.setProperty("ArtistThumb",ArtisteData.get("ArtistThumb"))
                ItemListe.setProperty("ArtistLogo",ArtisteData.get("ArtistLogo"))
                ItemListe.setProperty("ArtistBanner",ArtisteData.get("ArtistBanner"))
                ItemListe.setProperty("ArtistFanart",ArtisteData.get("ArtistFanart"))
                ItemListe.setProperty("ArtistFanart2",ArtisteData.get("ArtistFanart2"))
                ItemListe.setProperty("ArtistFanart3",ArtisteData.get("ArtistFanart3"))  
              musicbrainzalbumid=item.get("musicbrainzalbumid")                   
              ItemListe.setProperty('DBID', str(item.get("albumid")))
              ItemListe.setProperty('musicbrainzalbumid', str(musicbrainzalbumid)) 
                        
              ItemListe.setIconImage(item.get("thumbnail"))          
              ItemListe.setInfo("music", { "title": item.get("label"),"playcount":item.get("playcount"),"rating":item.get("rating")}) 
              
              ListeItem.append(ItemListe)
        if dp: 
          dp.close()      
          #xbmc.executebuiltin( "UpdateLibrary(music)") 
  return ListeItem,ArtisteData

def UpdateArtistes(Une=None,Toutes=None):
     ItemId=0
     AllMovies= {}
     NbItems=0
     savepath=""
     Titre=""
     
     dp = xbmcgui.DialogProgress()
     dp.create("IconMixTools",Titre,"")
     if not Une :
       json_result = getJSON('AudioLibrary.GetArtists', '{}')
       if json_result: 
          NbItems=len(json_result)
          Compteur=0
          for Artiste in json_result:
            ItemId=Artiste.get("artistid")            
            if ItemId:                
               if Toutes:
                 CheckArtisteAlbums(ItemId,1,None)   
               else:
                 CheckArtisteAlbums(ItemId,None,None) 
               Titre=xbmc.getLocalizedString( 36916 )+" : [I]"+Artiste.get("label")+"[/I]"
            Progres=(Compteur*100)/NbItems
            Compteur=Compteur+1
            if Toutes: dp.update(Progres,Titre,"(%d/%d)" %(Compteur,NbItems))
            else : dp.update(Progres,Titre,"...")
            if dp.iscanceled(): break
     else :
          CheckArtisteAlbums(Une,1,1)       
            
     dp.close()  
        
def CheckGenres(GenreLabel=None):
     ArtisteData=None
     ListeItem=[]
     
     if GenreLabel :
       json_result = getJSON('AudioLibrary.GetArtists', '{"filter": {"genre":"%s"}}' %(GenreLabel))
       #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"AudioLibrary.GetArtists","params":{"filter":%20{"genre":"rock"}},"id":"1"}
       if json_result: 
          NbItems=len(json_result)
          Compteur=0
          for Artiste in json_result:
            ArtisteId=Artiste.get("artistid") 
            ArtisteLabel=  Artiste.get("artist")          
            if ArtisteId:            
                 ArtisteData=GetMusicFicheArtiste(ArtisteLabel,ArtisteId,None) 
                 
                 if ArtisteData:
                    ItemListe = xbmcgui.ListItem(label=ArtisteData.get("ArtistName"),iconImage=ArtisteData.get("ArtistThumb"))
                    ItemListe.setProperty("ArtistBio",ArtisteData.get("ArtistBio"))
                    ItemListe.setProperty("DBID",str(ArtisteId))
                    ItemListe.setProperty("ArtistThumb",ArtisteData.get("ArtistThumb"))
                    ItemListe.setProperty("ArtistLogo",ArtisteData.get("ArtistLogo"))
                    ItemListe.setProperty("ArtistBanner",ArtisteData.get("ArtistBanner"))
                    ItemListe.setProperty("ArtistFanart",ArtisteData.get("ArtistFanart"))
                    ItemListe.setProperty("ArtistFanart2",ArtisteData.get("ArtistFanart2"))
                    ItemListe.setProperty("ArtistFanart3",ArtisteData.get("ArtistFanart3")) 
                    ListeItem.append(ItemListe) 
               
               
     return ListeItem  
     
#-------------------------------------ARTWORK-------------------------------------------------
#https://api.themoviedb.org/3/search/multi?api_key=67158e2af1624020e34fd893c881b019&language=en-US&query=alfred%20hitchcock&page=1&include_adult=true     
  
#--------------------------------------PLAYLIST-----------------------------------------------
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def ChoixPlayList(Label=None,Suppression=None):
   ListePlayList=[]
   
   ListePlayList=get_files(xbmc.translatePath('special://profile/playlists/video/' ),1) 
   if ListePlayList:
     if not Suppression:
        ListePlayList.insert(0,__language__( 32605 ))
        Titre=__language__( 32604 )+Label
     else:
        Titre=__language__( 32608 )+Label
     if len(ListePlayList)>0:
        dialogC = xbmcgui.Dialog()
        result=dialogC.select(Titre, ListePlayList)
        if result==0 and not Suppression: #creation
          dialog = xbmcgui.Dialog()
          Reponse = dialog.input(__language__( 32606 ), type=xbmcgui.INPUT_ALPHANUM)
          if Reponse:
             return xbmc.translatePath('special://profile/playlists/video/%s.xsp' %(Reponse)),Reponse
          else:
             return None,None        
        else:
          if result>=0:
             return xbmc.translatePath('special://profile/playlists/video/%s.xsp' %(ListePlayList[result]) ).decode("utf8"),ListePlayList[result] 
          else :
             return None,None     

def DelFromPlayList(): 
    suppr=0 
    Title=xbmc.getInfoLabel("ListItem.Label").decode("utf-8") 
    views_file,NomPlayList = ChoixPlayList(Title,1)
    if xbmcvfs.exists(views_file):            
            tree = ET.parse(views_file)
            root = tree.getroot()  
            for prop in root.findall('rule'):
              
              xx=prop.find('value').text
              
              if len(xx)>0:
                if xx==Title:
                  root.remove(prop)
                  suppr=1
            if suppr==1:
              tree.write(views_file,encoding='utf-8', xml_declaration=True)
              dialog=xbmcgui.Dialog()
              dialog.notification('IconMixTools', "[COLOR=yellow]"+Title+"[/COLOR][COLOR=white]"+__language__( 32609 )+"[/COLOR][COLOR=yellow]["+NomPlayList+"][/COLOR]", "acteurs/films.png", 1000)            
            else:
              dialog=xbmcgui.Dialog()
              dialog.notification('IconMixTools', xbmc.getLocalizedString( 13328 )%(Title), "acteurs/arfffff.png", 1000)
              
                                     
                
      
def AddToPlayList():    
    Title=xbmc.getInfoLabel("ListItem.Label").decode("utf-8")
    views_file,NomPlayList = ChoixPlayList(Title,None)
    if views_file:
        #views_file = xbmc.translatePath('special://profile/playlists/video/%s.xsp' %(NomPlayList) ).decode("utf8")   
        if not xbmcvfs.exists(views_file):
           root=ET.Element("smartplaylist")
           root.set('type','movies')
           name=ET.SubElement(root,'name')
           name.text=NomPlayList
           name=ET.SubElement(root,'match')
           name.text='any'
           indent(root)
           tree = ET.ElementTree(root)
           tree.write(views_file,encoding='utf-8', xml_declaration=True)
           
           
       
        if xbmcvfs.exists(views_file):
            
            tree = ET.parse(views_file)
            root = tree.getroot()        
            xx=root
            new=ET.SubElement(xx,'rule')
            new.set('field', 'title')
            new.set('operator','is')
            xxx=ET.SubElement(new,'value')
            xxx.text=Title
            indent(root)
            tree.write(views_file,encoding='utf-8', xml_declaration=True)
            #'<rule field="filename" operator="is"><value>%s</value></rule>' %(NomPlayList)
            dialog=xbmcgui.Dialog()
            dialog.notification('IconMixTools', "[COLOR=yellow]"+Title+"[/COLOR][COLOR=white]"+__language__( 32607 )+"[/COLOR][COLOR=yellow]["+NomPlayList+"][/COLOR]", "acteurs/films.png", 1000)
            

           
        else:
            dialog=xbmcgui.Dialog()
            dialog.notification('IconMixTools', NomPlayList+" : ERROR", "acteurs/arfffff.png", 1000)
            logMsg("%s introuvable " %(str(views_file)),0)  
  
    
