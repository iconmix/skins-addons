#!/usr/bin/python
# coding: utf-8
#from __future__ import unicode_literals
import xbmcplugin, xbmcgui, xbmc, xbmcaddon, xbmcvfs
import os,sys,io,shutil
import urllib2, urllib
import httplib
import datetime
from unidecode import unidecode
import HTMLParser
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
import re
import locale
import ssl
from threading import Thread
import threading

import zipfile

try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED

modes = { zipfile.ZIP_DEFLATED: 'deflated',
          zipfile.ZIP_STORED:   'stored',
          }


    
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
WindowHome = xbmcgui.Window(10000)
SETTING = ADDON.getSetting
KODILANGUAGE = xbmc.getInfoLabel( "System.Language" )
KODILANGCODE = xbmc.getLanguage(xbmc.ISO_639_1).lower()
__skin_string__ = xbmc.getLocalizedString

TMDBApiKey="67158e2af1624020e34fd893c881b019"
TrakTvId='e5de24726a01bd4592ae7b47367e122447a854bb7263bc0681e7c99758fb893c'
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
CalendrierPath=ADDON_DATA_PATH+"/series/planningnextV5"
Calendrier2SemaineSeriesPath=ADDON_DATA_PATH+"/series/planning2semaines"
Calendrier2SemaineSeriesTvMazePath=ADDON_DATA_PATH+"/series/planning2semainesTvMaze"
Calendrier2SemaineSeriesIncomingPath=ADDON_DATA_PATH+"/series/incoming2semaines"
Aujourdhui = datetime.date.today()
#TVDBToken=None
sys.path.append(xbmc.translatePath(os.path.join(ADDON_PATH, 'resources', 'lib')).decode('utf8'))
#----------------------------------------------------------------------------------------------------
def CheckTMDB():
  query_url="https://api.themoviedb.org/3/find/341663?api_key=%s&language=fr&external_source=tvdb_id&include_adult=true" %TMDBApiKey
  json_result = requestUrlJson(query_url)
  if json_result:
        return "https://api.themoviedb.org/3/"
  return "http://api.themoviedb.org/3/"

#-------------------------- FENETRE ARTWORKS ----------------------------------------------------------
    
class dialog_select_Arts(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self)
        self.listing = kwargs.get('listing')
        self.Actuels = kwargs.get('actuels')
        self.Extrafanart = kwargs.get('extrafanart')
        self.Title = kwargs.get('Title')
        
        

    def onInit(self):
        self.Choix={}
        if self.Actuels:
         for key in self.Actuels:
          self.Choix[key]=self.Actuels[key]
        self.Retour=False
        self.NbWebFanart=0
        self.DownloadExtraFanart=False
        self.ListeAffiche = self.getControl(200)
        self.ListeBanniere = self.getControl(201)
        self.ListeLogo = self.getControl(202)
        self.ListeClearArt = self.getControl(203)
        self.ListeVignette = self.getControl(204)
        self.ListeDisque = self.getControl(205)
        self.ListeFanart = self.getControl(206)
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
          if Label2=="fanart" and self.ListeFanart:  #32703         
              self.ListeFanart.addItem(item)
              if "Web" in item.getLabel():
                self.NbWebFanart=self.NbWebFanart+1
              
        
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
        if self.Choix.get("fanart") :
          self.getControl(16).setImage(self.Choix["fanart"], False)       
        
        self.getControl(1).setLabel("[COLOR=yellow][I]"+self.Title+": [/I][/COLOR]"+__language__( 32614 )) 
        self.getControl(20).setLabel(__language__( 32700 )+" [I]("+str(self.ListeAffiche.size())+")[/I]")
        self.getControl(21).setLabel(__language__( 32705 )+" [I]("+str(self.ListeVignette.size())+")[/I]")
        self.getControl(22).setLabel(__language__( 32702 )+" [I]("+str(self.ListeBanniere.size())+")[/I]")
        self.getControl(23).setLabel(__language__( 32704 )+" [I]("+str(self.ListeClearArt.size())+")[/I]")
        self.getControl(24).setLabel(__language__( 32703 )+" [I]("+str(self.ListeDisque.size())+")[/I]")
        self.getControl(25).setLabel(__language__( 32701 )+" [I]("+str(self.ListeLogo.size())+")[/I]")
        self.getControl(26).setLabel(__language__( 32706 )+" [I]("+str(self.ListeFanart.size())+")[/I]")
        self.getControl(8).setLabel(__language__( 32712) %str(self.NbWebFanart) )
        if not self.Extrafanart:
          self.getControl(8).setVisible(False)
       
        #self.getControl(100).setLabel(__language__( 32611 ))
        
        if self.ListeAffiche:
          self.setFocus(self.ListeAffiche)
        
           
                  
       # else:          self.close()
        

    def onAction(self, action):
        idaction=action.getId()
        if action in ACTION_PREVIOUS_MENU:
            self.Retour=False 
            self.DownloadExtraFanart=None        
            self.close()
        if (idaction==3 or idaction==4) and (self.getFocusId()>=200):
          Image = self.getControl(self.getFocusId()).getSelectedItem().getProperty("Icon") 
          typex=self.getControl(self.getFocusId()).getSelectedItem().getLabel2()
          if typex=="poster": 
            self.getControl(9).setHeight(350)
          else:
            self.getControl(9).setHeight(220) 
            
          self.getControl(9).setImage(Image, False)
          self.getControl(30).setLabel("$INFO[Container("+str(self.getFocusId())+").CurrentItem]/$INFO[Container("+str(self.getFocusId())+").NumItems]")
        
       
        
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
            self.DownloadExtraFanart=None
            self.close()
            
        if controlID == 5: #OK
            self.Retour=True
            self.DownloadExtraFanart=self.getControl(8).isSelected()
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
        self.getControl(30).setLabel("$INFO[Container("+str(self.getFocusId())+").CurrentItem]/$INFO[Container("+str(self.getFocusId())+").NumItems]")
        

   
# ------------------------------------ARTWORKS SAGAS/FILMS/TV--------------------------------------------------------------    

def sagachoixartcommun(Donnees=None,Lab2=None,RetourElements=None):
  if Donnees:
    for item in Donnees: 
      if item.get("lang")=="en" or item.get("lang")==KODILANGCODE or item.get("lang")=="00" or item.get("lang")=="99" or item.get("lang")=="98"or item.get("lang")=="" : 
        langue=item.get("lang").replace("00","?").replace("99","Local").replace("98","Web")
        
        if langue=="":
          langue="?"  
        if langue=="en":
          langue="English"    
        if langue==KODILANGCODE:
          langue=KODILANGUAGE 
        try:
          UrlHttp=item.get("url").replace("https://assets","http://assets")
        except:
          UrlHttp=item.get("url")
        Elements = xbmcgui.ListItem(label=langue, iconImage=UrlHttp,label2=str(Lab2))
        Elements.setProperty("Icon",str(UrlHttp))
        Elements.setProperty("Original","")
        RetourElements.append(Elements)
  return RetourElements

def sagachoixart(donnees=None,OriginalArt=None,TypeVideo="movie",chemin=None,Title=None): #movie ou tv
  ListeChoixArt=[]
  langue=KODILANGCODE #les 2 premieres lettres uniquement pour TMDB
  #OriginalArt:"logo","clearart","banner","poster","fanart","thumb","discart"
  #KeyStr={"logo":32701,"clearart":32704,"banner":32702,"poster":32700,"fanart":32706,"thumb":32705,"discart":32703,"fanart":32706}
  if OriginalArt:
    for key in OriginalArt:
      if OriginalArt.get(key):
        if OriginalArt.get(key)!="None":
           
           Elements = xbmcgui.ListItem(label="[I][kodi][/I]", iconImage=OriginalArt.get(key),label2=key)
           Elements.setProperty("Icon",OriginalArt.get(key))
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
    sagachoixartcommun(donnees.get("%s" %("moviebackground" if TypeVideo!="tv" else "showbackground")),"fanart",ListeChoixArt)
    
    
    
  if ListeChoixArt:
    #C:\Users\HTPC\AppData\Roaming\Kodi\addons\script.iconmixtools
    DialogChoixArtWorks = dialog_select_Arts('choixsagasarts.xml', __cwd__, 'default','1080i',listing=ListeChoixArt,actuels=OriginalArt,extrafanart=chemin,Title=Title) 
    DialogChoixArtWorks.doModal()
    DownloadExtraFanart=DialogChoixArtWorks.DownloadExtraFanart
    ret=DialogChoixArtWorks.Retour   
    if ret: 
      OriginalArt=DialogChoixArtWorks.Choix   
    del DialogChoixArtWorks 
    return OriginalArt,DownloadExtraFanart
  else :
    return None,None 
    
    
def getdatafanart(donnees=None):
  langue=KODILANGCODE
  pardefaut=None
  if donnees:     
     for item in donnees:
       try:
        UrlHttp=item.get("url").replace("https://assets","http://assets")
       except:
        UrlHttp=item.get("url")
       if item.get("lang")=="en":
        pardefaut=UrlHttp   
       if item.get("lang")==langue:  
         return UrlHttp
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

def DownloadAllExtraFanart(chemin=None,Allfanart=None,OnlyCheck=None):
  dp=None
  if Allfanart and chemin:
        CheckFanart=[]
        try:
          #if not xbmcvfs.exists(chemin):
            i=1
            try:
              erreur=os.mkdir(chemin)  
            except:
              i=0
            if not OnlyCheck:
             dp = xbmcgui.DialogProgress()
             dp.create("IconMixTools","WEB Fanarts","")
             NbItems=len(Allfanart)
             Compteur=0    
              
            for item in Allfanart:
              
              try:
                UrlHttp=item.get("url").replace("https://assets","http://assets")
              except:
                UrlHttp=item.get("url")
              if dp:
                Progres=(Compteur*100)/NbItems
                Compteur=Compteur+1
                dp.update(Progres,UrlHttp,"(%d/%d)" %(Compteur,NbItems))
                if dp.iscanceled(): break
              if UrlHttp:
                
                if not xbmcvfs.exists(chemin+(UrlHttp.split("background")[1])):
                  if not OnlyCheck:
                    try:
                         urllib.urlretrieve(UrlHttp,chemin+UrlHttp.split("background")[1])           
                    except:
                         i=0 
                  else:
                    item["lang"]="98"
                    CheckFanart.append(item)
              
              
            if dp:
              dp.close()
            if OnlyCheck:
              logMsg("CheckFanart %s" %CheckFanart)
              return CheckFanart        
        except:
          i=0
  else:
    logMsg("Erreur DownloadAllExtraFanart(%s,%s)" %(chemin,Allfanart))
  
   
def getartworks(IDCollection=None,OriginalArt=None,updateartwork=None,TypeVideo="movie",IDKodiSetouSaisonTv=None,forceupdateartwork=None,FanartPath=None,Title=None)   :
                                            
  ArtWorks={}
  json_data2=None
  chemin=None
  
  if IDCollection:  
    if updateartwork:
       xbmc.executebuiltin( "ActivateWindow(busydialog)" ) 
       
                                  
    if TypeVideo=="movie":
       UrlFanartTv="http://webservice.fanart.tv/v3/movies/%s?api_key=769f122ee8aba06f4a513830295f2bc0" %(IDCollection) #infos completes
       logMsg("UrlFanartTv (%s)" %(UrlFanartTv))
       json_data = requestUrlJson(UrlFanartTv)
       
       if not json_data and IDKodiSetouSaisonTv: # on va récupérer tous les artworks des films de la saga également.....
         json_result = getJSON('VideoLibrary.GetMovieSetDetails', '{ "setid":%d,"movies":{"properties": ["imdbnumber"]} }' %(int(IDKodiSetouSaisonTv)))
         logMsg("UrlFanartTv json_data(%s)" %(json_data))
         if json_result and json_result.get("movies"): 
           allMovies = json_result.get("movies")
           for item in allMovies:
             UrlFanartTv="http://webservice.fanart.tv/v3/movies/%s?api_key=769f122ee8aba06f4a513830295f2bc0" %(item.get("imdbnumber")) #infos completes
             json_data=MergeArtwork(json_data,requestUrlJson(UrlFanartTv))
             
    else:
       UrlFanartTv="http://webservice.fanart.tv/v3/tv/%s?api_key=769f122ee8aba06f4a513830295f2bc0" %(IDCollection) #infos completes
       json_data = requestUrlJson(UrlFanartTv) 
       logMsg("UrlFanartTv (%s)" %(UrlFanartTv))
       TvDbArt=GetArtWorksSerieTVDB(IDCollection)
       if TvDbArt:
          json_data=MergeArtwork(json_data,TvDbArt)
          
    if json_data and FanartPath:      
      chemin="%s\\extrafanart" %FanartPath[0]
      AllfanartCheck=DownloadAllExtraFanart(chemin,json_data.get("%sbackground" %(TypeVideo.replace("tv","show"))),True)
      if AllfanartCheck:
        Allfanart=AllfanartCheck[:]
      else:
        AllFanart=[]
      
      i=1
      try:
        erreur=os.mkdir(chemin)  
      except:
        try:
          listfiles=os.listdir(chemin)
          logMsg("liste %s" %listfiles)                
        except:
          listfiles=[]
        key="moviebackground" if TypeVideo!="tv" else "showbackground"
        
        for item in listfiles:
          Allfanart.append({"url":chemin+"\\"+item,"lang":"99"})
        json_data[key]=Allfanart
        logMsg("liste extfanart (%s) %s" %(len(Allfanart) if Allfanart else 0,json_data.get(key))  )        
        if (len(listfiles)>= len(Allfanart)):
          i=0
          logMsg("%s deja existant !!! ABANDON %s/%s" %(chemin,len(listfiles),len(Allfanart)))
        else:
          i=1  
      if (i==0):
        chemin=None
      
      
          
       
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
        json_data2,DownloadExtraFanart=sagachoixart(json_data,OriginalArt,TypeVideo,chemin,Title)
        logMsg("DownloadExtraFanart=%s" %DownloadExtraFanart)
        if json_data2:
            if DownloadExtraFanart:
              logMsg("lancement de DownloadAllExtraFanart(%s - %s)"% (chemin,AllfanartCheck))              
              DownloadAllExtraFanart(chemin,AllfanartCheck)
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
            if ((TypeVideo=="movie" and not SETTING("forceupdatesagaposter")=="true" and IDKodiSetouSaisonTv ) or (not TypeVideo=="movie" and not SETTING("forceupdatetvshowposter")=="true")) and not forceupdateartwork:
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
    
def media_path(path):
    # Check for stacked movies
    try:
        path = os.path.split(path)[0].rsplit(' , ', 1)[1].replace(",,",",")
    except:
        path = os.path.split(path)[0]
    # Fixes problems with rared movies and multipath
    if path.startswith("rar://"):
        path = [os.path.split(urllib.url2pathname(path.replace("rar://","")))[0]]
    elif path.startswith("multipath://"):
        temp_path = path.replace("multipath://","").split('%2f/')
        path = []
        for item in temp_path:
            path.append(urllib.url2pathname(item))
    else:
        path = [path]
    return path
    
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
  forceupdateartwork=None

   
  if ItemIdxx : 
        json_result = getJSON('VideoLibrary.GetMovieDetails', '{ "movieid":%s,"properties":["title","art","imdbnumber","file"]}' %(ItemIdxx))
        ItemPath=media_path(json_result.get("file"))
        logMsg("Item path=%s" %ItemPath)
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
             ArtWorks,updateartwork=getartworks(IMDBNumber,Actuels,updateartwork,"movie",None,forceupdateartwork,ItemPath,json_result.get("title"))  
          else:
             ArtWorks,bidon=getartworks(IMDBNumber,Actuels,False,"movie",None,forceupdateartwork,ItemPath,json_result.get("title"))
                                                
          if KODI_VERSION>=17 and ArtWorks and ( updateartwork or not Unique or forceupdateartwork): 
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
                
def updatetvartwork(ItemIdxx=None,Unique=True,Saison=None,forceupdateartwork=None): 
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
        json_result = getJSON('VideoLibrary.GetTvShowDetails', '{ "tvshowid":%s,"properties":["title","art","uniqueid","file"]}' %(ItemIdxx))
        IMDBNumber=GetTvDbId(json_result.get("uniqueid"))
        ItemPath=media_path(json_result.get("file"))
        logMsg("Item path=%s" %ItemPath)
        logMsg("updatetvartwork (%s)" %IMDBNumber)
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
             ArtWorks,updateartwork=getartworks(IMDBNumber,Actuels,updateartwork,"tv",None,forceupdateartwork,ItemPath,json_result.get("title"))  
          else:
             ArtWorks,bidon=getartworks(IMDBNumber,Actuels,False,"tv",None,forceupdateartwork,ItemPath,json_result.get("title"))
                                                
          if KODI_VERSION>=17 and ArtWorks and ( updateartwork or not Unique or forceupdateartwork): 
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
"""    
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
"""  
def GetTvDbId(UniqueId=None,TvShowId=None):
  #uniqueid : {"imdb":"tt5193358","tvdb":"304591","tmdb":"61692"}
  if UniqueId:
    if UniqueId.get("tvdb"):
      return UniqueId["tvdb"]
    if not UniqueId.get("tmdb") and UniqueId.get("imdb"):
      #TMDBID=get_externalID(UniqueId["imdb"],"tvshow")
      TMDBID=get_TMDBID("tvshow",TvShowId,UniqueId)
      if TMDBID:
        UniqueId["tmdb"]=TMDBID
    if UniqueId.get("tmdb"):
      query_url="%stv/%s/external_ids?api_key=%s&language=en-US&include_adult=true" % (BaseUrlTMDB,UniqueId["tmdb"],TMDBApiKey) 
      logMsg("GetTvDbId query_url (%s)" %query_url)
      json_result = requestUrlJson(query_url)
      if json_result:
        #logMsg("GetTvdb json_result (%s) (%s)" %(TvShowId,json_result))
        TVDBID=json_result.get("tvdb_id")
        if TVDBID and TvShowId:
          UniqueId["tvdb"]=str(TVDBID)
          UniqueStr='{'
          if UniqueId.get("imdb"):
           UniqueStr=UniqueStr+'"imdb":"%s",' %(UniqueId["imdb"])
          UniqueStr=UniqueStr+'"tvdb":"%s",' %(UniqueId["tvdb"])
          if UniqueId.get("tmdb"):
           UniqueStr=UniqueStr+'"tmdb":"%s",' %(UniqueId["tmdb"])
          UniqueStr=UniqueStr+'}'
          UniqueStr=UniqueStr.replace(",}","}")
          #logMsg("UniqueStr (%s)(%s)(%s)" %(TVDB,UniqueStr,UniqueId))
          
          try:
            json_result = setJSON('VideoLibrary.SetTvShowDetails', '{ "tvshowid":%d,"uniqueid":%s }' %(int(TvShowId),UniqueStr))
          except:
            logMsg("VideoLibrary.SetTvShowDetails TVDB serie : %d impossible" %(int(TvShowId)),0 )
          
        return TVDBID
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
    WindowHome.clearProperty('IconMixSaga')
    
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
       json_result = getJSON('VideoLibrary.GetMovieSetDetails', '{ "setid":%d,"properties":["art"],"movies": {"properties":["title","genre","year","rating","userrating","director","trailer","tagline","plot","plotoutline","originaltitle","lastplayed","playcount","writer","studio","mpaa","cast","country","imdbnumber","uniqueid","runtime","set","showlink","streamdetails","top250","votes","fanart","thumbnail","file","sorttitle","resume","setid","dateadded","tag","art"]} }' %(int(ItemId)))
       logMsg("CheckSaga 1 (%s)" %(json_result))
       if json_result:
         NbKodi=int(json_result.get("limits").get("total"))
         
              #----------------------------BASE TMDB ----------------------------       
       if not xbmcvfs.exists(savepath):
        #création du fichier de la saga !!!
         logMsg("création du fichier de la saga !!!")
         ArrayCollection=getsagaitem(ItemId,None,None,None,json_result,None)
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
          logMsg("[CheckSaga] NbFilmsSagas (%s) NbKodi (%s) NbTmdb (%s)" %(NbFilmsSaga,NbKodi,NbTmdb))
          if NbFilmsSaga and NbKodi and NbTmdb :
              MonLabel=json_result.get('label')
              
              logMsg("[CheckSaga] NbFilmsSaga (%s) TitreSaga (%s) json_result (%s)" %(NbFilmsSaga,TitreSaga,MonLabel))
              if NbFilmsSaga!=NbKodi or TitreSaga!=MonLabel: # or NbKodi<NbTmdb: #mise a jour !!! 
                 #ArrayCollection=getsagaitem(ItemId,1,ArrayCollection.get("kodicollection"),ArrayCollection.get("tmdbid"),json_result,None)
                 ArrayCollection=getsagaitem(ItemId,None,None,None,json_result,None)
                 if ArrayCollection:
                     NbFilmsSaga=ArrayCollection.get("kodi")
                     NbManquant=ArrayCollection.get("manquant")
                     TitreSaga=ArrayCollection.get("saga")
                     NbTmdb=ArrayCollection.get("tmdb")
                     PosterCollection=ArrayCollection.get("poster")
    
       
       if ArrayCollection: 
         ArtWorks= ArrayCollection.get("artworks") 
         
         
         if ArtWorks:
           WindowHome.setProperty('IconMixSagaClearArt',ArtWorks.get('clearart'))
           WindowHome.setProperty('IconMixSagaClearLogo',ArtWorks.get('logo'))
           WindowHome.setProperty('IconMixSagaBackGround',ArtWorks.get('fanart'))
           WindowHome.setProperty('IconMixSagaBanner',ArtWorks.get('banner'))
           WindowHome.setProperty('IconMixSagaDiscArt',ArtWorks.get('discart'))
           WindowHome.setProperty('IconMixSagaPoster',ArtWorks.get('poster'))
           WindowHome.setProperty('IconMixSagaThumb',ArtWorks.get('thumb'))
           
         if ArrayCollection.get("missing") :
           for item in ArrayCollection.get("missing"):
             today=item.get("release_date")
             DateSortie="??/????"
             if today:
                 DateSortie=today[5:7]+"/"+today[0:4] #mois/annee
             if today and xbmc.getCondVisibility("Skin.HasSetting(SagaDate)"):
                #nowX2 = datetime.datetime.strptime(today, '%Y-%m-%d').date()
                nowX2 = datetime.datetime(int(today[0:4]),int(today[5:7]),int(today[8:10]),0,0).date()
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
          logMsg("[CheckSaga] Valeur item.get : (%s)" %(item.get("movieid")))
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
           
 

    #BOUQUET FINAL 

    if NbKodiValide==len(ListeItem) and NbKodiValide>0: 
       WindowHome.setProperty('IconMixSaga','complet')
       logMsg("[CheckSaga] setProperty('IconMixSaga','complet') (%d)(%d)" %(NbKodiValide,len(ListeItem)))
    else:
       if NbKodiValide>0: 
          WindowHome.setProperty('IconMixSaga',str(NbKodiValide))
          logMsg("[CheckSaga] setProperty('IconMixSaga',str(NbKodiValide)) (%d)(%d)" %(NbKodiValide,len(ListeItem)))
       else:
          WindowHome.clearProperty('IconMixSaga') 
          logMsg("[CheckSaga] clearProperty('IconMixSaga') (%d)(%d)" %(NbKodiValide,len(ListeItem)))
       
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
          logMsg("[Checksaga] : Filetab (%s)" %(FileTab))     
          return ListeItemFinal,FileTab
  
        

def getsagaitem(KODISET_ID=None,ShowBusy=None,KodiCollection=None,TMDB_ID=None,json_result=None,updateartwork=None,forceupdateartwork=None):
  
  allArt=None
  KodiMovies= []
  TmdbCollection= {}
  ManquantM=[]
  
  ArrayCollection={}
  PosterCollection=None
  IDcollection=None
  Element = ""
  NbFilmsSaga=0
  ItemId=None
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
    
  if not KodiCollection:
    KodiCollection = []
  
  logMsg("getsagaitem : KODISET_ID=%s,ShowBusy=%s,KodiCollection=%s,TMDB_ID=%s" %(KODISET_ID,ShowBusy,KodiCollection,TMDB_ID),0)
       
  if KODISET_ID : 
      savepath=ADDON_DATA_PATH+"/collections/saga%s" %(KODISET_ID)
      logMsg("getsagaitem : savepath (%s)" %(savepath))
      if ShowBusy: 
        xbmc.executebuiltin( "ActivateWindow(busydialog)" ) 
        
      if not json_result:
        json_result = getJSON('VideoLibrary.GetMovieSetDetails', '{ "setid":%d,"properties":["art"],"movies": {"properties": [ "title","imdbnumber","uniqueid","art" ]} }' %(int(KODISET_ID)))
        
      if json_result and json_result.get("movies"): 
        KodiMovies = json_result.get("movies")
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

        if KodiMovies :
          
          for KodiMoviesItem in KodiMovies:
             #TMDBID=str(KodiMoviesItem.get("imdbnumber"))
             TMDBID=get_TMDBID("movie",KodiMoviesItem.get("movieid"),KodiMoviesItem.get("uniqueid"))
             IMDBID=KodiMoviesItem.get("imdbnumber")
             if TMDBID :
               zz=None
               for yy in KodiCollection:
                 if TMDBID==yy[1] or IMDBID==yy[0]:
                     zz=1
                     break
                 
               if not zz:
                 #TMDBID=get_externalID(TMDBID,"movie") # conversion imdb ou tvdb en themoviedb ....
                  if flagcheck==0:
                    ItemId=TMDBID 
                    flagcheck=1 
                  KodiCollection.append([IMDBID,TMDBID])
                  
        if xbmcvfs.exists(savepath):       
          #lecture dans le fichier existant
           with open(savepath) as data_file:
            data = json.load(data_file)
            if data:
              Actuels=data.get("artworks")
            data_file.close()  
            
      if ItemId:
                if not TMDB_ID:
                   #numero de collection TMDB inconnu
                   query_url = "%smovie/%s?api_key=%s&language=%s&include_adult=true" % (BaseUrlTMDB,ItemId,TMDBApiKey,KODILANGCODE)
                   json_data = requestUrlJson(query_url)
                   logMsg("getsagaitem : collection TMDB inconnu (%s)(%s)" %(query_url,json_data))
                   try:
                     IDcollection=json_data.get("belongs_to_collection").get("id")
                   except:
                     IDcollection=None
                  
                else: 
                   IDcollection=TMDB_ID
                   
                if IDcollection:
                     query_url = "%scollection/%d?api_key=%s&language=%s&include_adult=true" % (BaseUrlTMDB,IDcollection,TMDBApiKey,KODILANGCODE)
                     json_data = requestUrlJson(query_url)
                     logMsg("getsagaitem : collection TMDB trouvee (%s)(%s)" %(query_url,json_data))
                     

                     if json_data:
                         TmdbCollection=json_data.get("parts")
                         if json_data.get("poster_path"):
                            PosterCollection="http://image.tmdb.org/t/p/original"+json_data.get("poster_path")
                         else:
                            PosterCollection=None
                         if json_data.get("backdrop_path"):
                            FanartCollection="http://image.tmdb.org/t/p/original"+json_data.get("backdrop_path")
                         else:
                            FanartCollection=None

                         if TmdbCollection:
                            NbItemsCollection=len(TmdbCollection)

                            NbFilmsSaga=0
                            Manquant=0
                            if NbItemsCollection>0:
                              for check in TmdbCollection:
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
                                        
                                        logMsg("getsagaitem : check (%s)" %(check)) 
                                        if not zz :
                                           if check.get("title") and check.get("release_date") and check.get("poster_path"):
                                                 ManquantM.append(check)
                                                 NbFilmsSaga=NbFilmsSaga+1
                                                                         
                                        else: NbFilmsSaga=NbFilmsSaga+1
                                  else:
                                    if NbItemsCollection>0:
                                       NbItemsCollection=NbItemsCollection-1
                            logMsg("getsagaitem : Sortie boucle (%s)" %(ManquantM)) 
                            logMsg("getsagaitem : len(KodiCollection) (%s)" %(len(KodiCollection)))
                            logMsg("getsagaitem : KodiCollection (%s)" %(KodiCollection))
                            logMsg("getsagaitem : IDcollection (%s)" %(IDcollection))
                            logMsg("getsagaitem : NbItemsCollection (%s)" %(NbItemsCollection))
                            logMsg("getsagaitem : PosterCollection (%s)" %(PosterCollection))
                            logMsg("getsagaitem : FanartCollection (%s)" %(FanartCollection))      
                            ArrayCollection["kodi"]=len(KodiCollection)
                            ArrayCollection["kodicollection"]=KodiCollection
                            ArrayCollection["tmdbid"]=IDcollection
                            ArrayCollection["tmdb"]=NbItemsCollection
                            ArrayCollection["poster"]=PosterCollection
                            ArrayCollection["fanart"]=FanartCollection
                            logMsg("getsagaitem : ArrayCollection (%s)" %(ArrayCollection))
                            if IDcollection:
                              xxActuels=ArrayCollection.get("artworks")
                              if Actuels:
                                for key in Actuels:
                                  if not Actuels[key] and key=="clearart":
                                    xxActuels[key]=Actuels.get(key)
                                #xxActuels.update(Actuels)
                              Kupdateartwork=updateartwork                                  
                              ArtWorks,updateartwork=getartworks(IDcollection,xxActuels,updateartwork,"movie",KODISET_ID,forceupdateartwork)
                            else:
                              if Actuels:
                                ArtWorks=Actuels
                              
                            if ArtWorks:
                              ArrayCollection["artworks"]=ArtWorks
                            else:
                              if KodiCollection[0]:
                                updateartwork=Kupdateartwork
                                ArtWorks,updateartwork=getartworks(KodiCollection[0][1],Actuels,updateartwork,"movie",None,forceupdateartwork)
                            if ArtWorks:   
                              if PosterCollection and not ArtWorks.get("poster"):   
                                 ArtWorks["poster"]=PosterCollection
                              if FanartCollection and not ArtWorks.get("fanart"):  
                                 ArtWorks["fanart"]=FanartCollection
                            ArrayCollection["artworks"]=ArtWorks
                                 
                            if forceupdateartwork:
                              updateartwork=forceupdateartwork  
                            #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.SetMovieSetDetails","params":{"setid":38,"art":{"poster":"http://image.tmdb.org/t/p/original/zrApSsUX9i0qVntcCD0Pp55TdCy.jpg"}},"id":1}
                            if KODI_VERSION>=17 and ArtWorks and  (SETTING("updatesagaposter")=="true" or updateartwork): 
                              MAJ=""                            
                              if ArtWorks.get("logo") and ( not  check_clearlogo or updateartwork ):
                                MAJ='"clearlogo":"%s",' %(ArtWorks.get("logo"))
                              if ArtWorks.get("clearart") and ( not  check_clearart or updateartwork ):
                                MAJ=MAJ+'"clearart":"%s",' %(ArtWorks.get("clearart"))
                              if ArtWorks.get("banner") and ( not  check_banner or updateartwork ):
                                MAJ=MAJ+'"banner":"%s",' %(ArtWorks.get("banner"))
                              if ArtWorks.get("poster") and ( not  check_poster or updateartwork ):
                                MAJ=MAJ+'"poster":"%s",' %(ArtWorks.get("poster"))
                              if ArtWorks.get("fanart") and ( not  check_fanart or updateartwork ):
                                MAJ=MAJ+'"fanart":"%s",' %(ArtWorks.get("fanart"))
                              if ArtWorks.get("thumb") and ( not  check_thumb or updateartwork ):
                                MAJ=MAJ+'"thumb":"%s",' %(ArtWorks.get("thumb"))
                              if ArtWorks.get("discart") and ( not  check_discart or updateartwork ):
                                MAJ=MAJ+'"discart":"%s",' %(ArtWorks.get("discart"))

                              if len(MAJ)>3:
                                MJSAGA=MAJ[0:len(MAJ)-1] #suppression de la virgule de fin²
                                
                                try:
                                 json_result = setJSON('VideoLibrary.SetMovieSetDetails', '{ "setid":%d,"art":{%s} }' %(int(KODISET_ID),MJSAGA))
                                except:
                                  logMsg("VideoLibrary.SetMovieSetDetails : %d impossible = " %(int(KODISET_ID)) + str(MJSAGA),0 )
                                
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
                     
                     
                if SETTING("cachesaga")=="false"  and savepath:
                       erreur=DirStru(savepath)
                       try:
                         with io.open(savepath, 'w+', encoding='utf8',errors='ignore') as outfile:
                           str_ = json.dumps(ArrayCollection,indent=4, sort_keys=True,separators=(',', ':'), ensure_ascii=False)
                           outfile.write(to_unicode(str_))
                       except:
                         logMsg("Erreur getsagaitem io.open (%s)" %(savepath) )
                              
      if ShowBusy: xbmc.executebuiltin( "Dialog.Close(busydialog)" )                           
            
 
  return ArrayCollection
  

  

def UpdateSagas(Une=None,Toutes=None,updateartwork=None,Initialisation=""):
     ItemId=0
     AllMovies= {}
     NbItems=0
     savepath=""
     Titre=""
     
     forceupdateartwork=None
     if not updateartwork:
             dialogC = xbmcgui.Dialog()
             ret=dialogC.yesno(__language__(32582), __language__(32617 )," ","") #-- Show a dialog 'YES/NO'.
             if ret>0:
               forceupdateartwork=True
     if not Une :
       dp = xbmcgui.DialogProgress()
       dp.create("IconMixTools"+Initialisation,Titre,"")
       json_result = getJSON('VideoLibrary.GetMovieSets', '{}')
       if json_result: 
          NbItems=len(json_result)
          Compteur=0
          for Sagas in json_result:
            ItemId=Sagas.get("setid")
            savepath=ADDON_DATA_PATH+"/collections/saga%d" %(ItemId)
            
            #if Toutes or not os.path.exists(savepath) and ItemId: getsagaitem(ItemId.encode('utf8'),1)
            if Toutes or not xbmcvfs.exists(savepath) and ItemId: 
               getsagaitem(ItemId,None,None,None,None,updateartwork,forceupdateartwork)   
               Titre=xbmc.getLocalizedString( 31924 )+" : [I]"+Sagas.get("label")+"[/I]"
            Progres=(Compteur*100)/NbItems
            Compteur=Compteur+1
            if Toutes: dp.update(Progres,Titre,"(%d/%d)" %(Compteur,NbItems))
            else : dp.update(Progres,Titre,"...")
            if dp.iscanceled(): break
       dp.close()  
     else :      
          
          getsagaitem(str(Une),1,None,None,None,updateartwork,forceupdateartwork)        
            
     


# --------------------------------------------SERIES-------------------------------------------



def GetTvShowSaisons(IdKodi=None):
  logMsg("GetTvShowSaisons(%s)" %IdKodi)
  json_result = getJSON('VideoLibrary.GetSeasons', '{ "tvshowid":%d,"properties": [ "season","episode"]}' %(int(IdKodi)))
  return json_result
  
def CheckSaisonComplete(IdKodi=None):
  return None
  
def GetEpisodesKodi(TvShowId=None,Statique=True,DbType=None):
  ListeEpisodesFinal=[]
  ListeEpisodes=[]
  SaisonDetails=[]
  json_result=None
  prochain=0
  logMsg("GetEpisodesKodi : (%s)(%s)" %(TvShowId,DbType))
  if TvShowId:
    if DbType=="season":
      #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.GetSeasonDetails","params":{"seasonid":42,"properties":["tvshowid","episode","season"]},"id":"1"}
      json_saison = getJSON('VideoLibrary.GetSeasonDetails', '{ "seasonid":%d,"properties": ["tvshowid","episode","season"]}' %(int(TvShowId)))
      logMsg("json_saison (%s)" %(json_saison))
      if json_saison:
        json_result=getJSON('VideoLibrary.GetEpisodes', '{ "tvshowid":%d,"season":%d,"properties": ["playcount","file","art","resume","plot","director","episode","firstaired","title","originaltitle","productioncode","rating","ratings","season","seasonid","showtitle","specialsortepisode","specialsortseason","tvshowid","uniqueid","userrating","streamdetails","runtime"]}' %(int(json_saison.get("tvshowid")),int(json_saison.get("season"))))
        
    else:
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
               Ordre="%d%s" %(item.get("season"),str(item.get("episode")).zfill(3))
          except:
               Ordre=None
          try :
             PercentPlayed=Position/Total
          except:
             PercentPlayed=""
          
          ItemListe.setProperty('PercentPlayed', str(PercentPlayed))
          
         
          ItemListe.setInfo("dbid", str(item.get("episodeid")))
          #
          LabelsEpisodes=GetListItemInfoLabelsJson(item)
          vu=0
          if LabelsEpisodes:  
            try:
              vu=int(LabelsEpisodes["playcount"]) 
            except:
              vu=0    
            if vu!=0:
              if  PercentPlayed!="":
                vu=0    
            ItemListe.setInfo("video", LabelsEpisodes) 
          ItemListe.setPath(item.get("file"))
          try:
            Saison=int(item.get("season"))
          except:
            Saison=0
          ListeEpisodes.append([Ordre,ItemListe,item.get("file"),Saison,Art.get("season.poster"),str(item.get("episodeid")),vu])
          
          
      ListeEpisodesFinal=[]
      LL=[] 
                     
      LL=sorted(ListeEpisodes, key=lambda x:x[0],reverse=False)  
      cpt=0
      Saison=0
      SaisonTab={}
      PosterSaison=None
      while cpt<len(LL):
         Saison=str(LL[cpt][3])
         if SaisonTab.get(Saison):
           SaisonTab[Saison]=SaisonTab[Saison]+1
         else:
           SaisonTab[Saison]=1
       
         cpt=cpt+1
      NbEpisodes=-1
      NbEpisodesKodi=0   
      Saison=0
      cpt=0
      prochain=0
      cpt2=0
      SaisonTab=getepisodes(TvShowId,None,DbType,"local") 
      while cpt<len(LL):
        
             if LL[cpt][3]!=Saison:
                  Saison=LL[cpt][3]
                  PosterSaison=None
                  Data=SaisonTab.get(str(Saison))
                  if Data:
                    PosterSaison=Data.get("poster")
                    
                    try:
                        NbEpisodes=int(Data.get("NbEpisodes"))
                        NbEpisodesKodi=int(Data.get("NbEpisodesKodi"))
                        
                    except:
                        NbEpisodes=-1
                        NbEpisodesKodi=0
                    Complet=1    
                    if NbEpisodesKodi:
                      if NbEpisodes<=NbEpisodesKodi:
                         Complet=0 #complet 
                    
                  #Complet,NbKodi,PosterSaison=getepisodes(TvShowId,Saison,DbType,"local")
                  
                  Item=xbmcgui.ListItem(label=str(NbEpisodesKodi),label2=str(Saison),path="")
                  Item.setPath("")
                  cpt2=cpt2+1
                  if Complet==0:
                    Item.setProperty('Complet', "")
                  else:
                    Item.setProperty('Complet', str(NbEpisodes))
                  if PosterSaison:
                     Item.setProperty('PosterSaison', PosterSaison)
                  else:
                    Item.setProperty('PosterSaison', LL[cpt][4])
                  Episodes=0
                  if not Statique:
                 
                    ListeEpisodesFinal.append(["",Item,False])
                  else:
                    ListeEpisodesFinal.append(Item)
             if PosterSaison:
                     LL[cpt][1].setProperty('PosterSaison', PosterSaison)
             else:
                     LL[cpt][1].setProperty('PosterSaison', LL[cpt][4])
        
             
             if LL[cpt][6]==0 and prochain==0:
              prochain=cpt2     
             if not Statique:    
                 ListeEpisodesFinal.append([LL[cpt][2],LL[cpt][1],False])
             else:
                 ListeEpisodesFinal.append(LL[cpt][1])
             #ListeEpisodesFinal.append(LL[cpt][1])
             cpt=cpt+1
             cpt2=cpt2+1
  return ListeEpisodesFinal,prochain

def getepisodes(IdKodi=None,saisonID=None,DBtype=None,Local=None):
  Status={"ended":32862,"continuing":32863,"unknown":32864,"returning series":32863}
  UniqueId=None
  SaisonDetails=None
  ArrayCollection=None
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
  
  WindowHome.clearProperty('IconMixTvStatus')
  WindowHome.clearProperty('IconMixTvNetwork')
  WindowHome.clearProperty('IconMixTvCharacter')
  
  
  if IdKodi and DBtype:  
      
    if DBtype=="season":
     xxx=xbmc.getInfoLabel("Container.FolderPath")
     xx=xxx.split("titles/")[1]
     IdKodi=xx.split("/")[0]
     
        
    if DBtype=="episode":
      json_result = getJSON('VideoLibrary.GetEpisodeDetails', '{ "episodeid":%d,"properties": [ "title", "tvshowid","season" ]}' %(int(IdKodi)))
      logMsg("[getepisodes] : GetEPisodeDetails (%s)" %(json_result))
      if json_result and json_result.get("tvshowid"):
         IdKodi=json_result.get("tvshowid") 
         saisonID=json_result.get("season")
         logMsg("TVSHOWID : %s - saison : %s" %(IdKodi,saisonID),0)
      else : IdKodi=None
    
    if IdKodi:       
         json_result = getJSON('VideoLibrary.GetTVShowDetails', '{ "tvshowid":%d,"properties": [ "title", "uniqueid","episode" ]}' %(int(IdKodi)))
         if json_result and json_result.get("uniqueid"):
            UniqueId=GetTvDbId(json_result.get("uniqueid"))           
            NbKodi=json_result.get("episode")
            SaisonDetails=GetTvShowSaisons(IdKodi)
       
     #---- ------------- ----------------------------------------------------------------
    if UniqueId:
      
      savepath=ADDON_DATA_PATH+"/series/tv%s" %(UniqueId)
      
      if xbmcvfs.exists(savepath):
         with open(savepath) as data_file:
            ArrayCollection = json.load(data_file)
            data_file.close()
            if ArrayCollection:
              if SaisonDetails:
                for Episodes in SaisonDetails:
                  try:
                    NbKodiCollection=int(ArrayCollection.get("saisons").get(str(Episodes.get("season"))).get("NbEpisodesKodi"))
                    NbKodiEpisodes=int(Episodes.get("episode"))
                  except:
                    NbKodiCollection=-1
                    
                  if NbKodiCollection>=0:
                    logMsg("[GetEpisodes] Season (%s) epkodi (%s) NbKodiCollection (%s)" %(Episodes.get("season"),Episodes.get("episode"),NbKodiCollection))
                    if NbKodiCollection!=NbKodiEpisodes or not ArrayCollection.has_key("network"):
                      ArrayCollection=None #mise a jour !!!!
                      break
                  #logMsg(" season (%s) epkodi (%s) NbKodiCollection (%s)" %(Episodes.get("season"),Episodes.get("episode"),NbKodiCollection))
         if not ArrayCollection or not ArrayCollection.get("v7"): # si fichier foireux ?
          #mise a jour
            ArrayCollection=GetFicheBetaSeries(IdKodi,UniqueId,savepath,NbKodi,None,SaisonDetails)
     
         
      else : 
         #creation
          
         #if not Local:
           logMsg("[GetEpisodes] Creation (%s) " %(Local))
           ArrayCollection=GetFicheBetaSeries(IdKodi,UniqueId,savepath,NbKodi,None,SaisonDetails)
     
            
      if ArrayCollection:
            if not Local:
               try:
                 windowhome=xbmcgui.Window(10000)
               except:
                 windowhome=None
               if windowhome:
                 windowhome.setProperty('ItemCountry1',ArrayCollection.get("pays"))
                 logMsg("[GetEpisodes] ItemCountry1 (%s) " %(ArrayCollection.get("pays")))             
            
            if ArrayCollection.get("dateecheance"):
               try:
                  #nowX2 = datetime.datetime.strptime(str(ArrayCollection.get("dateecheance")), '%Y-%m-%d').date()
                  today=str(ArrayCollection.get("dateecheance"))
                  nowX2 = datetime.datetime(int(today[0:4]),int(today[5:7]),int(today[8:10]),0,0).date()
               except:
                  nowX2=nowX  
                  logMsg("Fuck time 2")
                  
                  
            if NbKodi and not Local:   
               if str(ArrayCollection.get("tmdbid"))!=str(UniqueId) or str(ArrayCollection.get("nbkodi"))!=str(NbKodi) or not ArrayCollection.get("v7") or nowX>nowX2 :
                  #mise a jour
                  ArrayCollection=GetFicheBetaSeries(IdKodi,UniqueId,savepath,NbKodi,None,SaisonDetails)
                      
                  
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
                     if not saisonID:
                       WindowHome.clearProperty('IconMixTvSaisons')
                       Saisons=ArrayCollection.get("saisons")
                       if Saisons:
                          NbSaisons=len(Saisons)
                          SaisonsCompletes=0
                          cpt=1
                          while cpt<=NbSaisons:
                            itemSaisons=Saisons.get(str(cpt))
                            if itemSaisons:
                              try:
                                NbEpisodes=int(itemSaisons.get("NbEpisodes"))
                                NbEpisodesKodi=int(itemSaisons.get("NbEpisodesKodi"))
                              except:
                                NbEpisodes=1
                                NbEpisodesKodi=0
                              logMsg("Saison (%s) NbEpisodes (%s) NbEpisodesKodi (%s)" %(cpt,NbEpisodes,NbEpisodesKodi)) 
                              #if NbEpisodes==NbEpisodesKodi:
                              if NbEpisodesKodi!=0:
                                SaisonsCompletes=SaisonsCompletes+1
                            cpt=cpt+1
                          logMsg("[GetEpisodes] Saisons (%s) (%s)-(%s)" %(SaisonsCompletes,NbSaisons,Saisons))    
                          if SaisonsCompletes>=0:
                            #if SaisonsCompletes>=NbSaisons:
                            #   WindowHome.setProperty('IconMixTvSaisons',__language__(32866))
                            #else:
                            WindowHome.setProperty('IconMixTvSaisons','[COLOR=FFFFFFFF]%s[/COLOR]/%s'%(SaisonsCompletes,NbSaisons))
                          
                     WindowHome.setProperty('ItemCountry1',ArrayCollection.get("pays"))
                     
            if NbEpisodesKodi:
              if NbEpisodes==int(NbEpisodesKodi):
                 NbEpisodes=0 #complet  
  logMsg("[GetEpisodes] Retour getepisodes (%s)" %(ArrayCollection.get("status"))) 
  try:   
     WindowHome.setProperty('IconMixTvStatus',__language__(Status[ArrayCollection.get("status").lower()]).encode("utf8"))
  except:
    WindowHome.clearProperty('IconMixTvStatus')
  WindowHome.setProperty('IconMixTvNetwork',ArrayCollection.get("network"))
  try:
    WindowHome.setProperty('IconMixTvCharacter',ArrayCollection.get("artworks").get("characterart"))
  except:
    WindowHome.clearProperty('IconMixTvCharacter')
  if not saisonID:
    return ArrayCollection.get("saisons")
  else:
    return NbEpisodes,NbEpisodesKodi,PosterSaison

def getdatafanarttv(donnees=None,saison=None):  
  langue=KODILANGCODE
  pardefaut=None
  if donnees:
     for item in donnees:
        if item:
           try:
            UrlHttp=item.get("url").replace("https://assets","http://assets")
           except:
            UrlHttp=item.get("url")
           if item.get("lang")=="en" and item.get("season")==saison:
            pardefaut=UrlHttp
           if not pardefaut and item.get("season")==saison:
            pardefaut=UrlHttp   
           if item.get("lang")==langue and item.get("season")==saison:  
             return UrlHttp
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
     forceupdateartwork=None
     
     dialogC = xbmcgui.Dialog()
     ret=dialogC.yesno(__language__(32582), __language__(32617 )," ","") #-- Show a dialog 'YES/NO'.
     if ret>0:
       forceupdateartwork=True

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
            #logMsg("UpdateSeries : UniqueId : (%s)" %UniqueId)
            NbKodi=Series.get("episode")
            savepath=ADDON_DATA_PATH+"/series/tv%s" %(ImdbNumber)
            
            if Toutes or not xbmcvfs.exists(savepath) and ItemId:
               SaisonDetails=GetTvShowSaisons(ItemId)
               GetFicheBetaSeries(ItemId,ImdbNumber,savepath,NbKodi,None,SaisonDetails,forceupdateartwork)   
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
            logMsg("UpdateSeries Seule : UniqueId : (%s)" %UniqueId)
            savepath=ADDON_DATA_PATH+"/series/tv%s" %(UniqueId)
            SaisonDetails=GetTvShowSaisons(Une)
            GetFicheBetaSeries(Une,UniqueId,savepath,NbKodi,1,SaisonDetails,forceupdateartwork)   
            
def ClearNextEpisode():
  try:
   windowhome = xbmcgui.Window(10000)
  except:
    windowhome=None
  if windowhome:
    windowhome.clearProperty('MonNextAired.NextDay')
    windowhome.clearProperty('MonNextAired.NextTitle')
    windowhome.clearProperty('MonNextAired.NextEpisode')
    windowhome.clearProperty('MonNextAired.IsFinal')
    
def Sauvegarde_Calendrier(GlobalCalendrier=None): 
  
  if GlobalCalendrier:
    erreur=DirStru(CalendrierPath)
    try:
     with io.open(CalendrierPath, 'w+', encoding='utf8',errors='ignore') as outfile: 
                  str_ = json.dumps(GlobalCalendrier,indent=4, sort_keys=True,separators=(',', ':'), ensure_ascii=False)
                  outfile.write(to_unicode(str_))
    except:
     logMsg("echec Sauvegarde planning (%s)(%s)" %(CalendrierPath,GlobalCalendrier) )         

def Charge_Calendrier():
  
  Calendrier=[{}]
  KodiTvShow=[]
  Update=True
  try:
      windowhome = xbmcgui.Window(10000)  
  except:
      windowhome=None               
  if windowhome:
      windowhome.setProperty('MonNextAired.Actif','oui')
  
  
  if xbmcvfs.exists(CalendrierPath):
          with open(CalendrierPath) as data_file:
            try:
               Calendrier = json.load(data_file)
            except:
               Calendrier=[{}]
            data_file.close()
          if Calendrier!=[{}]:
             Update=None
             try:
               json_result = getJSON('VideoLibrary.GetTvShows', '{ "properties":["uniqueid"]}')
               logMsg("Comparaison (%s) (%s)" %(len(Calendrier[0]),len(json_result)))
               fuck=0
               #if len(Calendrier[0])>len(json_result):
               if fuck==1:
                #des séries ont été effacées alors on recharge le planning....
                Calendrier=[{}]
                updategetnextepisode(None,Calendrier)
                Update=True  
               else:             
               
                 for itemtvshow in json_result:
                    TvDbId=GetTvDbId(itemtvshow.get("uniqueid"),itemtvshow.get("tvshowid"))
                    
                    if TvDbId:
                      KodiTvShow.append(TvDbId)
                      if not Calendrier[0].get(str(TvDbId)):#serie pas dans le planning ?
                       logMsg("ChargeCalendrier ajout de  : TvDbId : (%s) KodiId :  (%s)" %(TvDbId,itemtvshow.get("tvshowid"))) 
                       updategetnextepisode(itemtvshow.get("tvshowid"),Calendrier) 
                       Update=True  
                 CalendrierTemp=[{}]      
                 for itemcalendrier in Calendrier[0]:
                  if itemcalendrier in KodiTvShow:
                   CalendrierTemp[0][itemcalendrier]=Calendrier[0].get(str(itemcalendrier)) 
                  else:
                   Update=True 
                  
                 
                 Calendrier=CalendrierTemp
                    
             except:
               #Update=True  
               updategetnextepisode(None,Calendrier)
          else:
            updategetnextepisode(None,Calendrier)     
  else:
    updategetnextepisode(None,Calendrier)           
  if Update:     
    Sauvegarde_Calendrier(Calendrier)
  if windowhome:
    windowhome.clearProperty('MonNextAired.Actif')         
  return Calendrier

def GetSerieStatusNetwork(TvDbId=None,xx=None):
  Status=None
  Network=None
  SaisonsDetails={}
  if xx:
      if xx.has_key("status"):
         Status=xx["status"]
      if xx.has_key("network"):
         Network=xx["network"]
      if xx.has_key("saisons"):
         SaisonsDetails=xx["saisons"]
      
  if not Status or not Network or len(SaisonsDetails)<1:
    if xbmcvfs.exists(ADDON_DATA_PATH+"/series/tv%s" %(TvDbId)):
       with open(ADDON_DATA_PATH+"/series/tv%s" %(TvDbId)) as data_file:
          DataSeries = json.load(data_file)
          data_file.close()
       if DataSeries:
        Status=DataSeries.get("status")
        Network=DataSeries.get("network")
        Saisons=DataSeries.get("saisons")
        for key, value in Saisons.items() :
          SaisonsDetails[str(value.get("saison"))]=value.get("NbEpisodes")       
  if not Status:
    Status=""
  if not Network:
    Network=""
  return Status,Network,SaisonsDetails
  
def Diffusion2Semaines(GlobalCalendrier=None):
  #calendrier série KODI uniquement
  Retour=[[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
  
  dt=[]
  for i in range(0,15):
    dt.append(str(datetime.date.today() + datetime.timedelta(i)))
  # datetime.date.today() + datetime.timedelta(2)
  if GlobalCalendrier:
     Calendrier=GlobalCalendrier[0]
     for TvDbId in Calendrier:
        
        Item=Calendrier[TvDbId]
        Episodes=Item.get("episodes")
        try:
          Poster=Item.get("poster")
        except:
          Poster=None
        try:
          Banner=Item.get("banner")
        except:
          Banner=None
        try:
          Fanart=Item.get("fanart")
        except:
          Fanart=None
        try:
          ClearArt=Item.get("clearart")
        except:
          ClearArt=None
        try:
          TitreSerie=Item.get("TitreSerie")
        except:
          TitreSerie=None
        try:
          KodiId=Item.get("KodiId")
        except:
          KodiId=None
        try:
          Saisons=Item.get("Saisons")
        except:
          Saisons=None
        if Episodes:
          for EpDay in Episodes:
            
            if EpDay.get("date"):
               DateNext=EpDay["date"]
               NextDate=str(datetime.date(int(DateNext[0:4]),int(DateNext[5:7]),int(DateNext[8:10])))
               cpt=0
               while (cpt<14):
                if dt[cpt]==NextDate:
                 Retour[cpt].append({"next":EpDay,"tvdbid":TvDbId,"poster":Poster,"clearart":ClearArt,"fanart":Fanart,"banner":Banner,"TitreSerie":TitreSerie,"KodiId":KodiId,"Saisons":Saisons})
                 cpt=15
                else:
                  cpt=cpt+1
             
                
  logMsg("Diffusion2Semaines retour %s" %(Retour))        
  
  return Retour
  
def GetNextEpisodesKodi() :
    ListeNextEpisodes=[]
    Calendrier=Charge_Calendrier() 
    MonCalendrier=Diffusion2Semaines(Calendrier)
    loc = locale.getlocale(locale.LC_ALL)
    locale.setlocale(locale.LC_ALL, xbmc.getLanguage(xbmc.ISO_639_1))
    for DateItem in MonCalendrier:
            if len(DateItem)>0:                          
              
              for Item in DateItem:
                  #code : S01E02
                  #title : titre de l'episode
                  #TitreSerie : titre de la serie
                 Plot=Item.get("next").get("description")
                 tvdbid=str(Item.get("tvdbid"))
                 Unique={"tvdb":tvdbid}
                 Name=Item.get("next").get("title")
                 Code=Item.get("next").get("code")
                 if not Plot or len(Plot)<5:
                   
                    try:
                     Saison=int(Code.split("E")[0].replace("S",""))
                     Episode=int(Code.split("E")[1].replace("E",""))
                    except:
                      Saison=None
                      Episode=none
                    if Saison and Episode :                
                       TMDBNUMBER=get_TMDBID(DbType="tvshow",KodiId=None,UniqueId=Unique)
                       query_url="%stv/%s/season/%d/episode/%d?api_key=%s&language=en" %(BaseUrlTMDB,TMDBNUMBER,Saison,Episode,TMDBApiKey) #infos completes        
                       json_data = requestUrlJson(query_url)
                       logMsg("Queryurl (%s) : jsondata (%s)" %(query_url,json_data))
                       if json_data:
                        #Name=json_data.get("name")
                        Plot=json_data.get("overview")
                  #https://api.themoviedb.org/3/tv/1418/season/1/episode/1?api_key=67158e2af1624020e34fd893c881b019&language=FR
                 Elements = xbmcgui.ListItem(label="[COLOR=FFFFD966]"+Code+": [/COLOR]"+Name, label2=Code)
                 Elements.setArt({"poster":Item.get("poster"),"banner":Item.get("banner"),"fanart":Item.get("fanart"),"clearart":Item.get("clearart")})
                 Elements.setProperty("TitreSerie",Item.get("TitreSerie"))
                              
                 KodiId=Item.get("KodiId")                 
                 NetWork="resource://resource.images.studios.white"+str(Item.get("next").get("network"))+".png"                 
                 Elements.setProperty("Network",NetWork)
                 Elements.setInfo("video", {"dbid": str(KodiId),"mediatype": "tvshow","title": Item.get("TitreSerie"),"plot":Plot})
                 Elements.setProperty("KodiId",str(KodiId))
                 
                 
                 DateNext=Item.get("next").get("date")
                 NextDate=datetime.date(int(DateNext[0:4]),int(DateNext[5:7]),int(DateNext[8:10]))
                 Date=NextDate.strftime("%A %d/%m/%Y")
                 Jour=NextDate.strftime("%A")
                 Elements.setProperty("airdate",str(Date))
                 #Elements.setProperty("airday",str(Jour))
                 Elements.setProperty("tvdbid",tvdbid)
                 Elements.setProperty("plot",Item.get("next").get("description"))
                 
                 ListeNextEpisodes.append(["",Elements,True])
                 
    try:  
        locale.setlocale(locale.LC_ALL, loc)
    except:
        i=0  
    return ListeNextEpisodes            


  
def GetProgress(VideoType=None):
  Liste=[]
  logMsg("GetProgress : %s" %VideoType)
  json_result = getJSON("VideoLibrary.Get%ss" %VideoType, '{"filter":{"operator":"true", "field":"inprogress", "value":""},"properties":["title","genre","year","rating","userrating","director","trailer","plot","plotoutline","originaltitle","writer","studio","mpaa","cast","country","imdbnumber","runtime","resume","set","showlink","streamdetails","file","sorttitle","dateadded","art"]}')
  if json_result:
     for Item in json_result:
        Titre=Item.get("label")
        logMsg("Titre %s" %Titre)
        try:
          Poster=Item.get("art").get("poster").replace("image://","")
        except:
          Poster=None
        try:
          Banner=Item.get("art").get("banner").replace("image://","")
        except:
          Banner=None
        try:
          Fanart=Item.get("art").get("fanart").replace("image://","")
        except:
          Fanart=None
        try:
          clearart=Item.get("art").get("clearart").replace("image://","")
        except:
          clearart=None
        Elements = xbmcgui.ListItem(label=Titre)
        Elements.setArt({"poster":Poster,"banner":Banner,"fanart":Fanart,"clearart":clearart})
        Elements.setIconImage(Item.get("poster")) 
        KodiId=Item.get("%sid" %VideoType)
        Elements.setInfo("video", {"dbid": str(KodiId),"mediatype": VideoType,"title": Titre,"plot":Item.get("plot")})
        Elements.setProperty("KodiId",str(KodiId))
        #pistes audios tele
        Audio=Item.get("streamdetails").get("audio")
        i=1
        if Audio:               
             for AudioElement in Audio:  
                  Elements.setProperty('AudioLanguage.%d' %(i), AudioElement.get("language"))
                  Elements.setProperty('AudioChannels.%d' %(i), str(AudioElement.get("channels")))
                  Elements.setProperty('AudioCodec.%d' %(i), AudioElement.get("codec")) 
                  Elements.addStreamInfo('audio',AudioElement)                   
                  i=i+1

        #pistes vidéos 
        Video=Item.get("streamdetails").get("video")
        i=0
        Codec=""
        if Video:
          #{"aspect":2.3975000381469726563,"codec":"h264","duration":5584,"height":800,"language":"eng","stereomode":"","width":1918}
          for VideoItem in Video:
             Elements.setProperty('VideoCodec', VideoItem.get("codec")) 
             Elements.addStreamInfo('video',VideoItem)
             
        #sous-titres     
        Subtitles=Item.get("streamdetails").get("subtitle")
        i=1
        
        if Subtitles:
             for SubtitleElement in Subtitles:
                  Elements.setProperty('SubtitleLanguage.%d' %(i), SubtitleElement.get("language"))  
                  Elements.addStreamInfo('subtitle',SubtitleElement)                   
                  i=i+1
        Position=int(Item.get("resume").get("position"))*100
        Total=int(Item.get("resume").get("total"))
        
        try :
           PercentPlayed=Position/Total
        except:
           PercentPlayed=""
        Elements.setProperty('PercentPlayed', str(PercentPlayed))    
        Liste.append(["",Elements,True])    
  
  
  return Liste
    

              
"""        
def CalendrierTRAKTV():

  headers = {'Content-Type': 'application/json','trakt-api-version': '2','trakt-api-key': TrakTvId}
  request = urllib2.Request('https://api.trakt.tv/calendars/all/shows/%s/15' %(Aujourdhui), headers=headers)

  response_body = urllib2.urlopen(request).read()
"""
#--------------------------------------- TVMAZE --------------------------------------------------     
def GetCalendrierTvMaze(ShowProgress=True):
#http://api.tvmaze.com/schedule?country=US&date=2018-07-12
#"http://api.tvmaze.com/schedule?country=%s&date=2018-07-12" %(KODILANGCODE)
  ValideNetwork=["abc","fox","nbc","cw","cbs","fx","showtime","hbo","freeform","amc","usa network","tnt","bbc1","starz","comedy central","tv land","history","bravo","bet","own","hulu","cmt","audience network","paramount network"]
  LastDate=Aujourdhui
  Difference=14
  global_json_data=[]
  global_json_data2=[]
  Update=0
  if xbmcvfs.exists(Calendrier2SemaineSeriesTvMazePath):
          with open(Calendrier2SemaineSeriesTvMazePath) as data_file:
            try:
               global_json_data = json.load(data_file)
            except:
               global_json_data=None
            data_file.close()
          if global_json_data:               
              DateNext=global_json_data[0]["airdate"]
              NextDate=datetime.date(int(DateNext[0:4]),int(DateNext[5:7]),int(DateNext[8:10]))
              logMsg("NextDate (%s,%s)" %(NextDate,Aujourdhui))
              
              if Aujourdhui>NextDate:
                Update=1
                ToDel=0  
                AujourdhuiPresent=None
                Debut=0
                for item in global_json_data:
                   """
                   if Aujourdhui == datetime.date(int(item["airdate"][0:4]),int(item["airdate"][5:7]),int(item["airdate"][8:10])): 
                        AujourdhuiPresent=True
                        Debut=Debut+1
                   else:
                   """
                   if Aujourdhui > datetime.date(int(item["airdate"][0:4]),int(item["airdate"][5:7]),int(item["airdate"][8:10])):
                        ToDel=ToDel+1
                   else:
                    break
                #logMsg("Avant effacement %s" %global_json_data)  
                logMsg("ToDel (%s) (%s)" %(Debut,ToDel))
                if ToDel>0:
                   del global_json_data[Debut:ToDel]
                  
                #global_json_data=[item for item in global_json_data if Aujourdhui < datetime.date(int(item["airdate"][0:4]),int(item["airdate"][5:7]),int(item["airdate"][8:10]))]
                if len(global_json_data)>1:
                  LastDateStr=global_json_data[-1]["airdate"]
                else:
                  LastDateStr=str(Aujourdhui)
                LastDate=datetime.date(int(LastDateStr[0:4]),int(LastDateStr[5:7]),int(LastDateStr[8:10]))
                #Difference=abs(((Aujourdhui + datetime.timedelta(13)) - LastDate).days)-1
                Difference=abs(((Aujourdhui + datetime.timedelta(14)) - LastDate).days)
                if AujourdhuiPresent:
                  LastDate=LastDate+ datetime.timedelta(1)
                  Difference=Difference-1
                  
                
                
                
          else:
            Update=1
  else:
     Update=1 
  #effacement des jours avant aujourdhui
  
  
  
         
  if Update>0:
    
    dp=None
    if ShowProgress:
      dp = xbmcgui.DialogProgress()
      Titre="recuperation des donnees"
      dp.create("IconMixTools",Titre,"")   
    for i in range(0,int(Difference)):
       if dp:
          Progres=(i*100)/13
          dp.update(Progres,Titre,"(%d/%d)" %(i+1,14))
          if dp.iscanceled(): break
       Date=(LastDate + datetime.timedelta(i)).strftime("%Y-%m-%d")
       query_url="http://api.tvmaze.com/schedule?country=US&date=%s" %Date
       
       json_data = requestUrlJson(query_url)
       
       if json_data:
        #logMsg("recharge CalendrierTvMaze (%d) (%s)" %(len(json_data),query_url))
        global_json_data2=global_json_data2+json_data
        
       query_url="http://api.tvmaze.com/schedule?country=%s&date=%s" %(KODILANGCODE,Date)
       
       json_data = requestUrlJson(query_url)
       
       if json_data:
        #logMsg("recharge CalendrierTvMazeFR (%d) (%s)" %(len(json_data),query_url))
        global_json_data2=global_json_data2+json_data 
        
    if global_json_data2:    
      global_json_data=[]      
      for EpDay in global_json_data2:
        DateNext=EpDay["airdate"]
        try:
          Network=EpDay.get("show").get("network").get("name").lower()
        except:
          Network=None
        try:
          Pays=EpDay.get("show").get("network").get("country").get("code").lower()
        except:
          Pays=None     
          
        try:
          TvDbId=EpDay.get("show").get("externals").get("thetvdb")                    
        except:
          TvDbId=0
        try:
          Status=EpDay.get("show").get("status")
        except:
          Status=None            
        try:
          Saison=str(EpDay["season"])
          if len(Saison)<2:
            Saison="0"+Saison
        except:
          Saison=""
        try:
          Episode=str(EpDay["number"])
          if len(Episode)<2:
            Episode="0"+Episode
        except:
          Episode=""
        try:
          Poster=EpDay.get("show").get("image").get("medium")
        except:
          Poster=None
        Banner=None
        Fanart=None
        if TvDbId!=0 and (Network in ValideNetwork or Pays==KODILANGCODE) and Saison and (Episode and Episode!="None"):
          #logMsg("EpDay : %s" %EpDay)
          EpisodeDetails={"date":DateNext,"title":EpDay["name"],"code":"S"+Saison+"E"+Episode,"status":Status,"network":Network,"description":EpDay["summary"]}
          global_json_data.append({"next":EpisodeDetails,"airdate":DateNext,"tvdbid":TvDbId,"poster":Poster,"clearart":None,"fanart":Fanart,"network":Network,"banner":Banner,"TitreSerie":EpDay["show"].get("name"),"KodiId":None})
        else:
          logMsg("Rejet : (%s)(%s)(%s)(%s)(%s)(%s)" %(TvDbId,Network,Pays,Saison,Episode,EpDay))    
       
    if dp:
      dp.close()      
  #logMsg("retour global_json_data (%s)" %(global_json_data)) 
  return global_json_data,Update
  
def GetCalendrier2SemaineTvMaze(ShowProgress=None,Incoming=None):  
  
 
  ValideNetwork=["abc","fox","nbc","cw","cbs","fx","showtime","hbo","freeform","amc","usa network","tnt","bbc1","starz","comedy central","tv land","history","bravo","bet","own","hulu","cmt","audience network","paramount network"]
  Retour=[[],[],[],[],[],[],[],[],[],[],[],[],[],[]]  
  dt=[]
  
  for i in range(0,14):
    dt.append(str(datetime.date.today() + datetime.timedelta(i)))
  global_json_data=[]  
  itemTvMaze,Update=GetCalendrierTvMaze(ShowProgress)
  
  if itemTvMaze:     
            

      for EpDay in itemTvMaze:
         
         try:
           NumberStr=EpDay.get("next").get("code").split("E")[1]
           Number=int(NumberStr)
         except:
          Number=0
         if (Number==1 and Incoming) or (not Incoming and Number>0):
           DateNext=EpDay["airdate"]
           NextDate=str(datetime.date(int(DateNext[0:4]),int(DateNext[5:7]),int(DateNext[8:10])))
           cpt=0
           while (cpt<14):
              if dt[cpt]==NextDate:
                Retour[cpt].append(EpDay)
                cpt=15
              else:
                cpt=cpt+1
  
      for i in range(0,14):
        LL=sorted(Retour[i], key = lambda x: (x['network']))
        Retour[i]=LL
        global_json_data=global_json_data+LL
  
  if Update>0:       
    erreur=DirStru(Calendrier2SemaineSeriesTvMazePath)
    try:
     with io.open(Calendrier2SemaineSeriesTvMazePath, 'w+', encoding='utf8',errors='ignore') as outfile: 
                  str_ = json.dumps(global_json_data, ensure_ascii=False)
                  outfile.write(to_unicode(str_))
    except:
     logMsg("echec CalendrierTvMaze (%s)" %(Calendrier2SemaineSeriesTvMazePath) )   
  
          
  
  return Retour        
#-----------------------------------------------------------------
def Charge_Calendrier2SemaineSeries(Incoming=None):
  Sauve=None
  Update=0
  if Incoming:
    Chemin=Calendrier2SemaineSeriesIncomingPath
    Calendar="incoming"
  else:
    Chemin=Calendrier2SemaineSeriesPath
    Calendar="general"
  
  if xbmcvfs.exists(Chemin):
          with open(Chemin) as data_file:
            try:
               json_data = json.load(data_file)
            except:
               json_data=None
            data_file.close()
          if json_data:
            Tempo=json_data.get("episodes")
            if Tempo:    
              DateNext=Tempo[0]["date"]
              NextDate=datetime.date(int(DateNext[0:4]),int(DateNext[5:7]),int(DateNext[8:10]))
              if Aujourdhui>NextDate:
                Update=1
          else:
            Update=1
  else:
     Update=1        
           
  if Update>0:  
    #query_url="http://api.betaseries.com/planning/general?key=46be59b5b866&after=7&before=1" 
    query_url="http://api.betaseries.com/planning/%s?key=46be59b5b866&after=14&before=1" %Calendar 
    logMsg("recharge Charge_Calendrier2SemaineSeries (%s)" %(query_url))
    json_data = requestUrlJson(query_url)
    Sauve=True
    if Incoming:
      if json_data:
        Merge_Data=json_data.get("episodes")
      else:
        Merge_Data={}
      query_url="https://api.betaseries.com/planning/general?key=46be59b5b866&before=1&after=7&type=premieres"
      json_data2 = requestUrlJson(query_url)
      if json_data2:
        Merge_Data=Merge_Data+json_data2.get("episodes")
      json_data={"episodes":Merge_Data}
        
  
    Tempo=[] 
    Episodes=json_data.get("episodes")
    
    if Episodes:
      LL=[]
      
      for Item in Episodes:   
          DateNext=Item["date"]
          NextDate=datetime.date(int(DateNext[0:4]),int(DateNext[5:7]),int(DateNext[8:10]))
          if Aujourdhui<=NextDate:          
            Tempo.append(Item)
      LL=sorted(Tempo, key = lambda x: (x['date']))
      json_data={"episodes":LL}  
    else:
      json_data=None
      
  if Sauve and json_data:
      erreur=DirStru(Chemin)
      try:
       with io.open(Chemin, 'w+', encoding='utf8',errors='ignore') as outfile: 
                    str_ = json.dumps(json_data, ensure_ascii=False)
                    outfile.write(to_unicode(str_))
      except:
       logMsg("echec Charge_Calendrier2SemaineSeries (%s)" %(Chemin) )   
  return json_data
  


  
     
def GetCalendrierSemaine(Incoming=None):     
  #calendrier série à venir et toutes
#https://api.betaseries.com/planning/general?key=46be59b5b866&after=7&before=0
  
  Retour=[[],[],[],[],[],[],[],[],[],[],[],[],[],[]]  
  dt=[]
  xbmc.executebuiltin( "ActivateWindow(busydialog)" ) 
  for i in range(0,15):
    dt.append(str(datetime.date.today() + datetime.timedelta(i)))
  json_data=Charge_Calendrier2SemaineSeries(Incoming)
  
  if json_data:     
      itemBetaSeries=json_data.get("episodes")
      
      if itemBetaSeries:
          #LL=[]
          #LL=sorted(itemBetaSeries, key = lambda x: (x['date']))
          #for EpDay in LL:          
          for EpDay in itemBetaSeries:
              if EpDay.get("date") and EpDay.get("show").get("thetvdb_id")!=0 and EpDay.get("description")!="":
                 DateNext=EpDay["date"]
                 NextDate=str(datetime.date(int(DateNext[0:4]),int(DateNext[5:7]),int(DateNext[8:10])))
                 cpt=0
                 #while (cpt<7):
                 while (cpt<14):
                    if dt[cpt]==NextDate:
                      Status=None
                      Network=None
                      Banner=None
                      Fanart=None
                      Poster=None
                      Episode={"date":DateNext,"title":EpDay["title"],"code":EpDay["code"],"status":Status,"network":Network,"description":EpDay["description"]}
                       
                      Retour[cpt].append({"next":Episode,"tvdbid":EpDay.get("show").get("thetvdb_id"),"poster":Poster,"clearart":None,"fanart":Fanart,"banner":Banner,"TitreSerie":EpDay["show"].get("title"),"KodiId":None})
                      #cpt=7
                      cpt=15
                    else:
                      cpt=cpt+1
  #logMsg("GetCalendrierSemaine retour %s" %(Retour)) 
  xbmc.executebuiltin( "Dialog.Close(busydialog)" )        
  
  return Retour
                       

  
def updategetnextepisode(KodiIdUnique=None,GlobalCalendrier=None):
  #https://api.betaseries.com/planning/general?key=46be59b5b866&before=0&after=8
  
  #{"id":1023964,"thetvdb_id":6593667,"youtube_id":null,"title":"START","season":6,"episode":10,
  #"show":{"id":5629,"thetvdb_id":261690,"title":"The Americans (2013)","in_account":false},
  #"code":"S06E10","global":75,"special":0,"description":"Dans l'\u00e9pisode final, les Jennings font face \u00e0 un choix qui va changer leur vie pour toujours.",
  #"date":"2018-05-30","note":{"total":0,"mean":0,"user":0},"user":{"seen":false,"downloaded":false,"friends_watched":[]},"comments":"0","resource_url":"https:\/\/www.betaseries.com\/episode\/the-americans-2012\/s06e10","subtitles":[]}
  NextDay=None
  NextTitle=None
  
  ItemOk=None
  item=None
  Calendrier={}
  RetourUnique=None
  dp=None
  Titre=""
    
  
  
  
  if GlobalCalendrier:
    try:
      Calendrier=GlobalCalendrier[0]
    except:
      return None
                         
  if KodiIdUnique and not dp:
         
         json_data = getJSON('VideoLibrary.GetTvShowDetails', '{ "tvshowid":%s,"properties":["uniqueid","art"]}' %(KodiIdUnique))
         if json_data:
          json_result=[json_data]
  else: 
    
    if len(Calendrier)<=0:
      dp = xbmcgui.DialogProgress()
      dp.create("IconMixTools",Titre,"")
        
    json_result = getJSON('VideoLibrary.GetTvShows', '{ "properties":["uniqueid","art"]}')

  if json_result:
      if dp:
        NbItems=len(json_result)
        Compteur=0
      for itemtvshow in json_result:
          CalendrierTemp=[]
          Status="aucun"
          Titre=__language__(32865)+" : [I]"+itemtvshow.get("label")+"[/I]"
          try:
            Poster=urllib.unquote(itemtvshow.get("art").get("poster").replace("image://","")[:-1])
          except:
            Poster=None
          try:
            Banner=urllib.unquote(itemtvshow.get("art").get("banner").replace("image://","")[:-1])
          except:
            Banner=None
          try:
            Fanart=urllib.unquote(itemtvshow.get("art").get("fanart").replace("image://","")[:-1])
          except:
            Fanart=None
          try:
            clearart=urllib.unquote(itemtvshow.get("art").get("clearart").replace("image://","")[:-1])
          except:
            clearart=None
               
          try:
            TitreSerie=itemtvshow.get("label")
          except:
            TitreSerie=None
          try:
            KodiId=itemtvshow.get("tvshowid")
          except:
            KodiId=None
          if dp:
            Progres=(Compteur*100)/NbItems
            Compteur=Compteur+1
            dp.update(Progres,Titre,"(%d/%d)" %(Compteur,NbItems))
            if dp.iscanceled(): break
          
          TvDbId=GetTvDbId(itemtvshow.get("uniqueid"),itemtvshow.get("tvshowid"))
          
          if TvDbId:
            if Calendrier.get(str(TvDbId)):#serie deja dans le planning ?
                   xx=Calendrier[str(TvDbId)]["episodes"][0]                   
                   Status,Network,Saisons=GetSerieStatusNetwork(TvDbId,xx)
                  
                   if xx.has_key("date"): #date existante pour le prochain épisode ?
                     DateNext=xx["date"]
                     NextDate=datetime.date(int(DateNext[0:4]),int(DateNext[5:7]),int(DateNext[8:10]))
                     if Aujourdhui<=NextDate: #aujourd'hui inferieur à la premiere date ?
                      Calendrier[str(TvDbId)]["episodes"][0]={"date":DateNext,"title":xx["title"],"code":xx["code"],"status":Status,"network":Network,"description":xx["description"]}
                      Calendrier[str(TvDbId)]["poster"]=Poster
                      Calendrier[str(TvDbId)]["banner"]=Banner
                      Calendrier[str(TvDbId)]["fanart"]=Fanart
                      Calendrier[str(TvDbId)]["clearart"]=clearart
                      Calendrier[str(TvDbId)]["TitreSerie"]=TitreSerie
                      Calendrier[str(TvDbId)]["KodiId"]=KodiId
                      Calendrier[str(TvDbId)]["Saisons"]=Saisons
                      
                      if KodiIdUnique:
                        RetourUnique={"episodes":Calendrier[str(TvDbId)]}                      
                      # return xx #alors pas besoin d'aller plus loin
            else:
              logMsg("serie pas dans le calendrier TvDbId : (%s) (%s)" %(TvDbId,Calendrier))
              Status,Network,Saisons=GetSerieStatusNetwork(TvDbId,None)
              
              if not RetourUnique and Status!="ended":      
                query_url="https://api.betaseries.com/shows/episodes?key=46be59b5b866&thetvdb_id=%s" %(TvDbId)
                logMsg("recharge planning complet (%s)" %(query_url))
                json_data = requestUrlJson(query_url)     
                if json_data:     
                    itemBetaSeries=json_data.get("episodes")
                    if itemBetaSeries:              
                      xxx=[]
                      for xx in itemBetaSeries:
                        if xx.has_key("date"):
                          DateNext=xx["date"]
                          NextDate=datetime.date(int(DateNext[0:4]),int(DateNext[5:7]),int(DateNext[8:10]))
                          if Aujourdhui<=NextDate:                      
                            CalendrierTemp.append({"date":DateNext,"title":xx["title"],"code":xx["code"],"status":Status,"network":Network,"description":xx["description"]})
                            
                          
                      if len(CalendrierTemp)>0:
                        LL=[]
                        LL=sorted(CalendrierTemp, key = lambda x: (x['date']))
                        Calendrier[str(TvDbId)]={"episodes":LL,"Saisons":Saisons,"poster":Poster,"clearart":clearart,"banner":Banner,"fanart":Fanart,"TitreSerie":TitreSerie,"KodiId":KodiId}
                        if KodiIdUnique and not RetourUnique:
                          RetourUnique={"episodes":LL,"Saisons":Saisons,"poster":Poster,"banner":Banner,"TitreSerie":TitreSerie,"clearart":clearart,"fanart":Fanart,"KodiId":KodiId}
                      else:
                        Calendrier[str(TvDbId)]={"episodes":[{"title":None,"status":Status,"network":Network,"description":None}],"TitreSerie":TitreSerie,"KodiId":KodiId}
                else:
                  Calendrier[str(TvDbId)]={"episodes":[{"title":None,"status":Status,"network":Network,"description":None}],"saisons":Saisons,"TitreSerie":TitreSerie,"KodiId":KodiId}
 
                        
  if dp:
    dp.close()
         
  if len(Calendrier)>0:
    if GlobalCalendrier:
          del GlobalCalendrier[0]
          GlobalCalendrier.append(Calendrier)
    
  if KodiIdUnique and RetourUnique:
    return RetourUnique         

def getnextepisode(IdKodi=None,TvDbId=None,DbType=None,GlobalCalendrier=None,PrecedentTvShow=None):
  #https://api.betaseries.com/planning/general?key=46be59b5b866&before=0&after=8
  
  #{"id":1023964,"thetvdb_id":6593667,"youtube_id":null,"title":"START","season":6,"episode":10,
  #"show":{"id":5629,"thetvdb_id":261690,"title":"The Americans (2013)","in_account":false},
  #"code":"S06E10","global":75,"special":0,"description":"Dans l'\u00e9pisode final, les Jennings font face \u00e0 un choix qui va changer leur vie pour toujours.",
  #"date":"2018-05-30","note":{"total":0,"mean":0,"user":0},"user":{"seen":false,"downloaded":false,"friends_watched":[]},"comments":"0","resource_url":"https:\/\/www.betaseries.com\/episode\/the-americans-2012\/s06e10","subtitles":[]}
  NextDay=None
  NextTitle=None
  
  ItemOk=None
  item=None
  #Calendrier=[{}]
  
  
  
 
  Calendrier=GlobalCalendrier[0]
  #logMsg("Calendrier1 (%d) (%s)" %(len(GlobalCalendrier),GlobalCalendrier))
   
  
  if DbType=="episode" or DbType=="season":
      json_result = getJSON('VideoLibrary.Get%sDetails' %(DbType), '{ "%sid":%d,"properties": [ "tvshowid","season" ]}' %(DbType,int(IdKodi)))
      if json_result and json_result.get("tvshowid"):
         IdKodi=json_result.get("tvshowid")                  
      else : IdKodi=None
  logMsg("getnextepisode : IdKodi (%s) PrecedentTvShow : (%s) DbType: (%s)" %(IdKodi,PrecedentTvShow,DbType))
  if str(IdKodi)!=str(PrecedentTvShow):
    ClearNextEpisode()
    if IdKodi:
             json_result = getJSON('VideoLibrary.GetTvShowDetails', '{ "tvshowid":%s,"properties":["uniqueid","art"]}' %(IdKodi))
             if json_result:
                  TvDbId=GetTvDbId(json_result.get("uniqueid"))  
                  #logMsg("getnextepisode : TvDbId : (%s) (%s)" %(TvDbId,Calendrier))
                  logMsg("getnextepisode : IdKodi (%s) TvDbId : (%s) DbType: (%s)" %(IdKodi,TvDbId,DbType))
          
          
    if TvDbId:
      status=None
      network=None
      
      ItemOk=Calendrier.get(str(TvDbId))
      logMsg("ItemOk (%s,%s)" %(IdKodi,ItemOk)) 
      if ItemOk:
        try:
          status=ItemOk.get("episodes")[0].get("status")
          network=ItemOk.get("episodes")[0].get("network")
        except:    
          status=None
          network=None
        
         
      if not ItemOk or not status or not network: 
        logMsg("updateget status network")
        ItemOk=updategetnextepisode(IdKodi,GlobalCalendrier)
        
        
                
              
      if ItemOk: 
              DetailsEp=ItemOk.get("episodes")
              for item in DetailsEp: 
                try:
                  NextTitle=item["title"]
                except:
                  NextTitle=None
                if NextTitle:
                  try:
                    DateNext=str(item["date"])
                  except:
                    DateNext=None
                  if DateNext:
                    NextDate = datetime.date(int(DateNext[0:4]),int(DateNext[5:7]),int(DateNext[8:10]))
                     
                    if Aujourdhui<=NextDate:
                      locale.setlocale(locale.LC_ALL,'')
                      NextDay=NextDate.strftime('%A %d/%m/%Y')
                      
                      if Aujourdhui==NextDate :
                        NextDay=__language__(32618)
                      
                      
                      try:
                        windowhome = xbmcgui.Window(10000)  
                      except:
                        windowhome=None               
                      if windowhome:
                        Code=item["code"]
                       
                        windowhome.setProperty('MonNextAired.NextDay',NextDay)                      
                        windowhome.setProperty('MonNextAired.NextEpisode',Code)
                        try:
                           Saison=int(Code.split("E")[0].replace("S",""))
                           Episode=int(Code.split("E")[1].replace("E",""))
                           NbEpisodes=int(ItemOk.get("Saisons").get(str(Saison)))
                           logMsg("Saison (%s) Episode (%s) NbEpisodes (%s)" %(Saison,Episode,NbEpisodes))
                           if Episode==NbEpisodes:
                              #NextTitle=NextTitle+" FINAL !!!"
                              windowhome.setProperty('MonNextAired.IsFinal',"   >>"+__skin_string__(31795))
                           
                        except:
                           Saison=None
                           Episode=None
                        
                        windowhome.setProperty('MonNextAired.NextTitle',NextTitle)   
                      break
      
         
  
def getallnextepisodes(IdKodi=None,TvDbId=None,DbType=None,GlobalCalendrier=None):
  NextDay=None
  NextTitle=None
  
  ItemOk=None
  item=None
  ListeNextEpisodes=[]
  #logMsg("getallnexepisodes (%s)(%s)(%s)" %(IdKodi,TvDbId,DbType))
  #Calendrier=Charge_Calendrier(savepath,GlobalCalendrier)
  Calendrier=GlobalCalendrier[0]
  IdKodi=int(IdKodi)
  if DbType=="episode":
      json_result = getJSON('VideoLibrary.GetEpisodeDetails', '{ "episodeid":%d,"properties": [ "title", "tvshowid","season" ]}' %(IdKodi))
      if json_result and json_result.get("tvshowid"):
         IdKodi=json_result.get("tvshowid") 
         
      else : IdKodi=None
  
  if IdKodi and not TvDbId:
    json_result = getJSON('VideoLibrary.GetTvShowDetails', '{ "tvshowid":%s,"properties":["uniqueid"]}' %(IdKodi))
    if json_result:
        TvDbId=GetTvDbId(json_result.get("uniqueid"))
        logMsg("getallnextepisodes : TvDbId : (%s)" %TvDbId)
  
  if TvDbId:
    status=None
    network=None
    
    if Calendrier.has_key(str(TvDbId)):
      ItemOk=Calendrier[str(TvDbId)]
      try:
        status=ItemOk.get("episodes")[0].get("status")
        network=ItemOk.get("episodes")[0].get("network")
      except:    
        status=None
        network=None
      
       
    if not ItemOk or not status or not network: 
      ItemOk=updategetnextepisode(IdKodi,Calendrier)
      
              
            
    if ItemOk:    
       
        
       ListeNextEpisodes=[]  
       LL=[]  
       for item in ItemOk.get("episodes"):
          if item["title"] :
            DateNext=item["date"].decode("utf8")
            NextDate = datetime.date(int(DateNext[0:4]),int(DateNext[5:7]),int(DateNext[8:10]))
            if Aujourdhui<=NextDate:               
              NextDay=NextDate.strftime('%d/%m/%Y') 
              Elements = xbmcgui.ListItem(label=item["title"], iconImage=item["code"],label2=NextDay)
              Elements.setProperty("network",item["network"])
              ListeNextEpisodes.append(Elements)
            
                  
  return ListeNextEpisodes          
               
      
def GetFicheTmdbSeries(TvDbId=None,NbKodiSaison=None,ArtWorkSeason=None):   
  ArrayCollectionTMDB={} 
  TotalSaisonsTMDB={}
  ItemId=get_TMDBID(DbType="tvshow",KodiId=None,UniqueId={"tvdb":TvDbId})
  #https://api.themoviedb.org/3/tv/11466?api_key=67158e2af1624020e34fd893c881b019&language=en-US
  query_url = "%stv/%s?api_key=%s&include_adult=true" % (BaseUrlTMDB,ItemId,TMDBApiKey)
  SaisonTabTMDB = requestUrlJson(query_url)
  
  if SaisonTabTMDB:
       ArrayCollectionTMDB["name"]=SaisonTabTMDB.get("name")
       
       ArrayCollectionTMDB["imdbid"]=None
       ArrayCollectionTMDB["sa_id"]=None
       
       ArrayCollectionTMDB["status"]=SaisonTabTMDB.get("status")
       NetWorks=SaisonTabTMDB.get("networks")
       if NetWorks:
         ArrayCollectionTMDB["network"]=NetWorks[0].get("name")
       ArrayCollectionTMDB["pays"]=SaisonTabTMDB.get("origin_country")[0]
       #recupération du pays
       #---------------------------------
       
       SaisonTabTMDB=SaisonTabTMDB.get("seasons")
       if SaisonTabTMDB:
           for item in SaisonTabTMDB:                          
                   EpisodesEtcastingTMDB={} 
                   EpisodesEtcastingTMDB["NbEpisodes"]=item.get("episode_count")
                   EpisodesEtcastingTMDB["NbEpisodesKodi"]=0
                   if NbKodiSaison:
                     for check in NbKodiSaison:
                       if check.get("season")==item.get("season_number"):
                          EpisodesEtcastingTMDB["NbEpisodesKodi"]=check.get("episode")
                   if ArtWorkSeason:
                       EpisodesEtcastingTMDB["saison"]=str(item.get("season_number"))
                       EpisodesEtcastingTMDB["banner"]=None
                       if item.get("poster_path"):
                          EpisodesEtcastingTMDB["poster"]="http://image.tmdb.org/t/p/original"+item.get("poster_path")
                       EpisodesEtcastingTMDB["thumb"]=None
                   TotalSaisonsTMDB[str(item.get("season_number"))]=EpisodesEtcastingTMDB 
  
  return ArrayCollectionTMDB,TotalSaisonsTMDB
              

  
def GetFicheBetaSeries(IdKodi=None,TvDbId=None,savepath=None,NbKodi=None,ShowBusy=None,NbKodiSaison=None,forceupdateartwork=None):
#Va chercher la fiche complete de la serie sur BetaSeries, met a jour les ARTs   
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
  check_clearlogo=None
  check_clearart=None
  check_banner=None
  check_poster=None
  check_fanart=None
  check_thumb=None
  check_characterart=None  
  nowX = datetime.datetime.now().date()+datetime.timedelta(30) #pour mise a jour une fois par mois
  logMsg("GetFicheBetaSeries IdKodi(%s) ,TvDbId(%s) ,savepath(%s) ,NbKodi(%s) ,ShowBusy(%s) ,NbKodiSaison(%s) ,forceupdateartwork(%s) " %(IdKodi,TvDbId,savepath,NbKodi,ShowBusy,NbKodiSaison,forceupdateartwork))
  if IdKodi or TvDbId:
  
     json_result = getJSON('VideoLibrary.GetTVShowDetails', '{ "tvshowid":%d,"properties":["art"]}' %(int(IdKodi)))
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
          if allArt.get("characterart"):
            check_characterart=urllib.unquote(allArt.get("characterart").replace("image://","")[:-1])   

     
     if TvDbId :
         if ShowBusy: xbmc.executebuiltin( "ActivateWindow(busydialog)" )                             
      
         
         
         TotalSaisons={}
         ArtWorkSerie,ArtWorkSeason=gettvartworks(TvDbId)
         if ArtWorkSerie:        
            ArrayCollection["artworks"]=ArtWorkSerie 
         
         query_url = "https://api.betaseries.com/shows/display?key=46be59b5b866&thetvdb_id=%s" % (TvDbId) 
         json_data = requestUrlJson(query_url)
         logMsg("GetFicheBetaSeries (%s)(%s)" %(query_url,json_data))
          
         if not json_data:
           ArrayCollection,TotalSaisons=GetFicheTmdbSeries(TvDbId,NbKodiSaison,ArtWorkSeason)
           logMsg("GetFicheBetaSeriesTMDB (%s)(%s)" %(ArrayCollection,TotalSaisons))
          
         ArrayCollection["tmdbid"]=TvDbId
         ArrayCollection["kodiid"]=IdKodi
         ArrayCollection["nbkodi"]=NbKodi
         ArrayCollection["dateecheance"]=nowX.strftime('%Y-%m-%d')
         ArrayCollection["v7"]="ok" 
         
         if json_data:
             SaisonTab=json_data.get("show")
             if SaisonTab:
                 ArrayCollection["name"]=SaisonTab.get("title")
                 ArrayCollection["imdbid"]=SaisonTab.get("imdb_id")
                 ArrayCollection["sa_id"]=SaisonTab.get("id")
                 ArrayCollection["status"]=SaisonTab.get("status")
                 ArrayCollection["network"]=SaisonTab.get("network")
                 #recupération du pays
                 qurl="%sfind/%s?api_key=%s&language=en-US&external_source=tvdb_id&include_adult=true"  % (BaseUrlTMDB,TvDbId,TMDBApiKey)
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
            if ArtWorkSerie.get("logo") and ( forceupdateartwork or not  check_clearlogo):
              MAJ='"clearlogo":"%s",' %(ArtWorkSerie.get("logo"))
            if ArtWorkSerie.get("clearart") and ( forceupdateartwork or not  check_clearart):
              MAJ=MAJ+'"clearart":"%s",' %(ArtWorkSerie.get("clearart"))
            if ArtWorkSerie.get("banner") and ( forceupdateartwork or not  check_banner):
              MAJ=MAJ+'"banner":"%s",' %(ArtWorkSerie.get("banner"))
            if ArtWorkSerie.get("poster") and ( forceupdateartwork or not  check_poster):
              MAJ=MAJ+'"poster":"%s",' %(ArtWorkSerie.get("poster"))
            if ArtWorkSerie.get("fanart") and ( forceupdateartwork or not  check_fanart):
              MAJ=MAJ+'"fanart":"%s",' %(ArtWorkSerie.get("fanart"))
            if ArtWorkSerie.get("thumb") and ( forceupdateartwork or not  check_thumb):
              MAJ=MAJ+'"landscape":"%s",' %(ArtWorkSerie.get("thumb"))  
            if ArtWorkSerie.get("characterart") and ( forceupdateartwork or not  check_characterart):
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
                  
     
                
         if SETTING("cacheserie")=="false"  and savepath and ArrayCollection.get("name"):        
             erreur=DirStru(savepath)
             try:
               with io.open(savepath, 'w+', encoding='utf8',errors='ignore') as outfile: 
                            str_ = json.dumps(ArrayCollection,indent=4, sort_keys=True,separators=(',', ':'), ensure_ascii=False)
                            outfile.write(to_unicode(str_))
             except:
               logMsg("Erreur GetFicheBetaSeries io.open (%s)" %(savepath) )
         if ShowBusy: xbmc.executebuiltin( "Dialog.Close(busydialog)" )                 
  return ArrayCollection 

                
     

# --------------------------------------------UTILITAIRES/PLUGIN----------------------------------------------

def GetVolume():
  json_result = getJSON('Application.GetProperties','{"properties":["volume","muted"]}')
  if json_result:
     return json_result.get("volume")
     
def GetDuration(DBID=None,DBTYPE=None):
  if "episode" in DBTYPE:
        json_result = getJSON('VideoLibrary.GetEpisodeDetails', '{ "episodeid":%d,"properties":["tvshowid"] }' %(int(DBID)))
        if json_result:
          DBID=json_result.get("tvshowid")
          DBTYPE="tvshow"
        else: DBTYPE=None
  
  
  if DBID and DBTYPE:      
     json_result = getJSON('VideoLibrary.Get%sDetails'%(DBTYPE), '{ "%sid":%d,"properties":["runtime"] }' %(DBTYPE,int(DBID)))
     if json_result:
      return str(datetime.timedelta(seconds=int(json_result.get("runtime"))))
  return None



def GetListItemInfoLabelsJson(data=None):
    
  if data:
    Valeur={}
#    Valeur["resume"]=data.get("resume")
    
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
    if data.get("tvshowid"):
      Valeur["dbid"]=int(data.get("tvshowid"))
    if data.get("episodeid"):
      Valeur["dbid"]=int(data.get("episodeid"))
      Valeur["mediatype"]="episode"
      Valeur["episode"]=data.get("episode") if data.get("episode") else None
      Valeur["season"]=data.get("season") if data.get("season") else None
      
    return Valeur
  else:
    return None             
def GetListItemInfoLabels(ContainerID=None):
  if ContainerID:
    
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
              'overlay':xbmc.getInfoLabel("Container(%d).ListItem.Overlay" %(ContainerID)) if xbmc.getInfoLabel("Container(%d).ListItem.Overlay" %(ContainerID)) else None,
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

def getGenreListe(KodiId=None,genretypex=None):
  ItemId = None
  genretype=""
  genre=""
  genrelist=[]
  genrelistID=[]
  if  (len(sys.argv)>1 and sys.argv[1]):
    
    if genretypex=="episode": #si content=episode -> tvshow
       genretypex="tvshow"
    json_genrelist = getJSON("VideoLibrary.GetGenres",'{"type":"%s"}' %genretypex)
    #logMsg(" json_genrelist : (%s) (%s)" %(genretypex,json_genrelist))
    if json_genrelist:
      finalliste={}
      for item in json_genrelist:
        finalliste[item.get("label")]=str(item.get("genreid"))
        
    genretype="VideoLibrary.Get%sDetails" %(genretypex)
    genrelisttype=genretypex.encode("utf8")
    json_result = getJSON(genretype, '{ "%sid":%s,"properties":["genre"]}' %(genretypex,KodiId))
    if json_result:
      genrelistID=json_result.get("genre")
      IDgenre=None
      for item in genrelistID: 
        Id=str(finalliste.get(item))
        Image="moviegenres/%s.jpg" %item
        
        ImageUrl=xbmc.translatePath(os.path.join('special://home/addons/skin.iconmix-krypton/media/' ,Image))
        if not xbmcvfs.exists(ImageUrl):
          Image="frames/iconvignette.png"
          logMsg("Image non trouvee") 
        ItemListe = xbmcgui.ListItem(label=item,iconImage=Image,label2=str(Id))
        ItemListe.setIconImage(Image) 
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
            query_url="%s%s/%s/credits?api_key=%s&language=%s&include_adult=true" % (BaseUrlTMDB,Typex,MissingId,TMDBApiKey,KODILANGCODE) 
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
         json_result = getJSON("VideoLibrary.GetMovies", '{"filter":{"field":"%s","operator":"contains","value":"%s"},"properties":["title","genre","year","rating","userrating","director","trailer","tagline","plot","plotoutline","originaltitle","lastplayed","playcount","writer","studio","mpaa","cast","country","imdbnumber","runtime","set","showlink","streamdetails","top250","votes","fanart","thumbnail","file","sorttitle","resume","setid","dateadded","tag","art"]}' %(ActeurType,Acteur))
         json_result2 = getJSON("VideoLibrary.GetTvShows", '{"filter":{"field":"%s","operator":"contains","value":"%s"},"properties":["plot","thumbnail","year","file","art","imdbnumber","rating","userrating","cast"]}' %(ActeurType,Acteur))
         
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
                   ItemListe.setPath(Item.get("file"))
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
        try:
          savepath=ADDON_DATA_PATH+"/%s/%s" %(ActeurType,check.replace(" ", "_"))
        except:
          savepath=None
        #savepath=ADDON_DATA_PATH+"/%s/%s" %(ActeurType,str(unidecode(Acteur)).replace(" ", "_"))
        if savepath and xbmcvfs.exists(savepath):
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
        else:
          ActeurId=GetActeurId(Acteur) 
        
        #http://api.allocine.fr/rest/v3/filmography?partner=100043982026&code=12302&profile=large&filter=movie&striptags=synopsis%2Csynopsisshort&format=json&sed=20170507&sig=jfS3iVDun%2FywD91uBJ78p1lZlog%3D

        if savepath and ActeurId.get("tmdb") and (not xbmcvfs.exists(savepath) or ActeurSave>0):
            
            query_url = "%sperson/%s/combined_credits?api_key=%s&language=%s&include_adult=true" % (BaseUrlTMDB,ActeurId.get("tmdb"),TMDBApiKey,KODILANGCODE) 
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
                
                            
                  if savepath and ActeurSave>0 and SETTING("cacheacteur")=="false"  and savepath:
                        erreur=DirStru(savepath)
                        #ActeurCache["cast"]=json_data.get("cast") 
                        #ActeurCache["crew"]=json_data.get("crew")  
                        
                        if not ActeurCache["nom"]: ActeurCache["nom"]=str(unidecode(Acteur))                         
                        if not ActeurCache["id"]: ActeurCache["id"]=ActeurId    
                        try:                    
                          with io.open(savepath, 'w+', encoding='utf8',errors='ignore') as outfile: 
                            str_ = json.dumps(ActeurCache,indent=4, sort_keys=True,separators=(',', ':'), ensure_ascii=False)
                            outfile.write(to_unicode(str_)) 
                        except:
                          logMsg("Erreur ActeurFilmsTvTMDB io.open (%s)" %(savepath) ) 
                          
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
        query_url = "%ssearch/person?api_key=%s&language=%s&query=%s&page=1&include_adult=true" % (BaseUrlTMDB,TMDBApiKey,KODILANGCODE,urllib.quote(check))
        logMsg("getacteurid : query_url (%s)" %(query_url))
        json_data = requestUrlJson(query_url)              
        ActeurId["tmdb"]=None        
        if json_data:
            allInfo=json_data.get("results")            
            
            if allInfo:
              for item in allInfo:
                if not ActeurId["tmdb"]:
                   ActeurId["tmdb"]=str(item.get("id"))
                   logMsg("GetActeurId ActeurTMDBID (%s)" %(str(ActeurId["tmdb"])),0)
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
    
    check=remove_accents(try_decode(NomActeur))
    #savepath=ADDON_DATA_PATH+"/%s/%s" %(ActeurType,remove_accents(NomActeur.encode("utf8","ignore").decode("utf8","ignore").replace(" ", "_")))
    #NomActeur=NomActeur.encode("utf8","ignore").decode("utf8","ignore")
    try:
          savepath=ADDON_DATA_PATH+"/%s/%s" %(ActeurType,check.replace(" ", "_"))
    except:
      savepath=None
    
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
              if SETTING("cacheacteur")=="false" and savepath:
                  erreur=DirStru(savepath) 
                  try:           
                    with io.open(savepath, 'w+', encoding='utf8',errors='ignore') as outfile: 
                      str_ = json.dumps(ActeurCache,indent=4, sort_keys=True,separators=(',', ':'), ensure_ascii=False)
                      outfile.write(to_unicode(str_))
                  except:
                    logMsg("Erreur GetActeurInfo io.open (%s)" %(savepath) )
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
            query_url = "%sperson/%s?api_key=%s&language=%s&include_adult=true" % (BaseUrlTMDB,ActeurId.get("tmdb"),TMDBApiKey,KODILANGCODE) 
            json_datatmdb = requestUrlJson(query_url) 
            
        if not json_data or (not json_data.get("biography") and not json_datatmdb.get("biography")):   
              #pas de biographie dans la langue de KODI alors on cherche en Anglais......
              query_url = "%sperson/%s?api_key=%s&language=EN&include_adult=true" % (BaseUrlTMDB,ActeurId.get("tmdb"),TMDBApiKey) 
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
          
          if not Poster and savepath:  
             Poster="DefaultActor.png" 
             Cache=GetActeurInfo(zig,CheminType)
             if Cache :
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
#------------------------------------


    
class Annonces(Thread):
    #def __init__(self, KODIID=None,LeType=None,KodiTitre=None,Annee=None,Saison=None,Episode=None):
    def __init__(self, KODIID,LeType,KodiTitre,Annee,GlobalAnnonces,GlobalAnnoncesThread,TMDBID):
        Thread.__init__(self)
        self.KODIID=KODIID
        self.LeType=LeType
        self.KodiTitre=KodiTitre
        self.Annee=Annee
        self.Saison=None
        self.Episode=None
        self.TMDBID=TMDBID
        #self.Saison=Saison
        #self.Episode=Episode
        self.GlobalAnnonces=GlobalAnnonces
        self.GlobalAnnoncesThread=GlobalAnnoncesThread
        
        
        

    def run(self):
        if not self.KODIID in self.GlobalAnnoncesThread:
          self.GlobalAnnoncesThread.append(str(self.KODIID))
          if len(self.GlobalAnnonces)<=0:
            data=init_bande_annonces()
            if len(data)>0:           
              self.GlobalAnnonces.append(data)
            #logMsg("INITIALISATION DE LA BASE (%d) : %s" %(len(self.GlobalAnnonces),self.GlobalAnnonces))
          
          ListeTrailer=GetAllBandesAnnonces(self.GlobalAnnonces,self.KODIID,self.LeType,self.KodiTitre,self.Annee,self.Saison,self.Episode,self.TMDBID)
          logMsg("THREAD (%s)/(%s)/(%s) pour %s FINI !!!! ()" %(self.KodiTitre,threading.current_thread().name,threading.active_count(),self.KODIID))
          Allocine=[]
          Youtube=[]
          Cineserie=[]
          for item in ListeTrailer:
              if item.get("key")=="Allocine":
                Allocine.append(item)
              elif item.get("key")=="Cineserie":
                Cineserie.append(item)
              elif item.get("key")=="YouTube":
                Youtube.append(item)
          data={"KodiTitre":self.KodiTitre,"TypeVideo":self.LeType,"Annee":self.Annee}  
          if SETTING("allocineactif")=="true": data["Allocine"]=Allocine
          if SETTING("cineserieactif")=="true": data["Cineserie"]=Cineserie
          if SETTING("youtubeactif")=="true": data["YouTube"]=Youtube
          if len(self.GlobalAnnonces)>0:
            self.GlobalAnnonces[0][str(self.KODIID)]=data
          else:
            self.GlobalAnnonces.append({str(self.KODIID):data})
          self.GlobalAnnoncesThread.remove(str(self.KODIID))
        else:
          logMsg("THREAD pour %s deja en cours...." %(str(self.KODIID)))
        

class GetAnnonceFrom(Thread):

    def __init__(self, KODIID=None,LeType=None,KodiTitre=None,Annee=None,Fournisseur=None):
        Thread.__init__(self)
        self.KODIID=KODIID
        self.LeType=LeType
        self.KodiTitre=KodiTitre
        self.Annee=Annee
        self.Fournisseur=Fournisseur
        
        self.ListeTrailer=[]

    def run(self):
        FList=["","allocine","cineseries","tmdb"]
        if self.Fournisseur:
          if self.Fournisseur==1:
            self.ListeTrailer=Allocine_BandeAnnonce(self.KodiTitre,self.LeType,None,None,self.Annee)
          elif self.Fournisseur==2:
            self.ListeTrailer=BACineSeries(self.KodiTitre,self.LeType,self.Annee)
          elif self.Fournisseur==3:
            self.ListeTrailer=getTrailer(self.KODIID,self.LeType)
          logMsg("THREAD GetAnnonceFrom (%s) (%s)/(%s) pour %s FINI !!!!" %(FList[self.Fournisseur],threading.active_count(),threading.current_thread().name,self.KODIID))
        
    def join(self):
        Thread.join(self)
        return self.ListeTrailer
            
            
#------------------------------------  
def SaveBandeAnnoncesFull(ListeTrailer=None):
  
    if ListeTrailer:       
        
        savepath=ADDON_DATA_PATH+"/bandeannonces/annonces"         
        erreur=DirStru(savepath)
        try:
         with io.open(savepath, 'w+', encoding='utf8',errors='ignore') as outfile:
           str_ = json.dumps(ListeTrailer,indent=4, sort_keys=True,separators=(',', ':'))
           outfile.write(to_unicode(str_))
         logMsg('creating archive')
         zf = zipfile.ZipFile(savepath+'.zip', mode='w')
         try:
              zf.write(savepath,"annonces",compress_type=compression)
         finally:
              zf.close()
              os.remove(savepath)


        except:
         logMsg("Erreur bandeannonce io.open (%s)" %(savepath) )
#------------------------------------  


def init_bande_annonces():
  
  savepath=ADDON_DATA_PATH+"/bandeannonces/annonces"
  try:
    zf = zipfile.ZipFile(savepath+'.zip')
  except:
    zf=None
  if zf:
    try:            
        zf.extract("annonces",ADDON_DATA_PATH+"/bandeannonces/")         
    except KeyError:
        logMsg('ERROR: Did not find %s in zip file' %ziparchive )       
  
  if xbmcvfs.exists(savepath):                  
    #lecture dans le fichier existant
     with open(savepath) as data_file:
      try:
       data = json.load(data_file)
       data=data[0]
      except:
       data=[] 
      data_file.close()
      os.remove(savepath)
  else:
    data=[]
  return data

def GetBandeAnnonces(GlobalAnnonces,BAID,KodiTitre,Annee):
  ListeTrailer=[]
  LenTrailer=[-1,-1,-1]
  if BAID:
      if len(GlobalAnnonces)<=0:       
        
        data=init_bande_annonces()
        if data:
          GlobalAnnonces.append(data)
        else:
          GlobalAnnonces=[]
      if len(GlobalAnnonces)>0:
        if GlobalAnnonces[0].has_key(str(BAID)):
          data=GlobalAnnonces[0].get(str(BAID))
          #Titre=data.get("KodiTitre").lower()
          #if Titre==KodiTitre.decode('utf8').lower():
          if data.get("Annee")==Annee:
            if SETTING("allocineactif")=="true":
              try: 
                ListeTrailer=ListeTrailer+data.get("Allocine")
                LenTrailer[0]=1
              except:
                LenTrailer[0]=-1
            if SETTING("cineserieactif")=="true":
              try: 
                ListeTrailer=ListeTrailer+data.get("Cineserie")
                LenTrailer[1]=1
              except:
                LenTrailer[1]=-1
            if SETTING("youtubeactif")=="true":
              try: 
                ListeTrailer=ListeTrailer+data.get("YouTube")
                LenTrailer[2]=1
              except:
                LenTrailer[2]=-1
        
  return ListeTrailer,LenTrailer


def GetAllBandesAnnonces(GlobalAnnonces,KODIID,LeType,KodiTitreX,Annee,Saison,Episode,TMDBID):
  LenTrailer=[0,0,0]
  AllocineBA=None
  CineSerieBA=None
  t1=None
  t2=None
  t3=None
  try:
    KodiTitre=remove_accents(KodiTitreX)
  except:
    KodiTitre=KodiTitreX
  if GlobalAnnonces:
    ListeTrailer,LenTrailer=GetBandeAnnonces(GlobalAnnonces,KODIID,KodiTitre,Annee)
  else:
    ListeTrailer=[]
    LenTrailer=[-1,-1,-1]
  
  if len(ListeTrailer)<=0 or (-1 in LenTrailer):
    try:
      windowvideonav = xbmcgui.Window(10025)
      waitimage=xbmcgui.ControlImage(x=25, y=25, width=40, height=30, filename="sablier.gif",aspectRatio = 0)
      windowvideonav.addControl(waitimage)
    except:
      windowvideonav=None
    #-------- ALLOCINE --------    
    if SETTING("allocineactif")=="true" and LenTrailer[0]==-1:
      t1=GetAnnonceFrom(KODIID,LeType,KodiTitre,Annee,1)
      t1.start()
      
           
    #-------------CINESERIE----------------    
    if SETTING("cineserieactif")=="true" and LenTrailer[1]==-1:
      TypeCineSerie=LeType
      if TypeCineSerie!="movie":     
        TypeCineSerie="tvshow"  
      t2=GetAnnonceFrom(KODIID,TypeCineSerie,KodiTitre,Annee,2)
      t2.start()
      
    
    #-------- YOUTUBE chez TMDB--------
    if SETTING("youtubeactif")=="true" and LenTrailer[2]==-1:
      if GlobalAnnonces and not TMDBID:        
        TMDBID=get_TMDBID(LeType,KODIID,None)
      
      if TMDBID:   
          t3=GetAnnonceFrom(TMDBID,LeType,KodiTitre,Annee,3)
          t3.start()
          
              
    if t1:
      AllocineBA=t1.join()
      if AllocineBA:
         cpt=len(AllocineBA)-1
         while cpt>=0:                                  
           ListeTrailer.insert(0,AllocineBA[cpt])  
           cpt=cpt-1
    if t2:
      CineSerieBA=t2.join()
      if CineSerieBA:
           cpt=len(CineSerieBA)-1
           while cpt>=0:                                  
             ListeTrailer.append(CineSerieBA[cpt])  
             cpt=cpt-1
    if t3:
      TMDBBA=t3.join()
      if TMDBBA: 
            cpt=len(TMDBBA)-1
            while cpt>=0:                                  
               ListeTrailer.append(TMDBBA[cpt])  
               cpt=cpt-1
    if windowvideonav:
      windowvideonav.removeControl(waitimage)
  return ListeTrailer
# --------------------------- CINESERIES ----------------------

def getCineseries(url=None):
  logMsg("GetCineSeries (%s)" %url)
  userAgent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:24.0) Gecko/20100101 Firefox/24.0"  
  headers = { "User-Agent" : userAgent }
  myRequest = urllib2.Request(url, data=None, headers=headers) 
  context = ssl.create_default_context()
  myHTTPSHandler = urllib2.HTTPSHandler(context=context)
  myOpener = urllib2.build_opener(myHTTPSHandler)
  urllib2.install_opener(myOpener)  
  data=None
  try: 
      response = urllib2.urlopen(myRequest) 
      data=response.read()
  except IOError, e: 
      if hasattr(e, 'code'): # HTTPError 
          print 'http error code: ', e.code 
      elif hasattr(e, 'reason'): # URLError 
          print "can't connect, reason: ", e.reason 
      
  return data

def BACineSeriesGetVideo(url=None,MQualite=None):
  URLRetour=None
  if url and MQualite :
    try:
      MediaQualite=int(Qualite)
    except:
      MediaQualite=720
    data=getCineseries(url)
    if data:
      linkarray=data.split('{"sources":[')[1]
      newlinkjson='{'+data.split('vc.player_setup = {')[1].rsplit('};')[0].replace('\/','/')+'}'
      datajson=json.loads(newlinkjson)
      linkjson=datajson.get("playlist")[0].get('sources')
      
      if linkjson:
        for itemx in linkjson:
          label=itemx.get('label')
          try:
            qualite=int(label.replace('p',''))
          except:
            qualite=0
          
          if qualite==MediaQualite :            
            URLRetour=itemx.get('file')
            break
         
  return URLRetour
 
def BACineSeries2(Titre=None,typevideo=None,Annee=None,Saison=None)  :
  TrailerLink=[]
  XQualite=[720,480,320]
  try:               
    MediaQualite=XQualite[int(SETTING("BAMiniQualite"))]
  except:
    MediaQualite=720 #par défaut
  
  if Titre: 
    #TitreUrl=Titre+" bande annonce"
    TitreUrl=Titre
    if typevideo!="tvshow":
        typevideo="eb_movie"
        
    else:
        typevideo="eb_serie"
        if Saison:
          TitreUrl=TitreUrl+" season %s" %(Saison) 
         
    
    data=getCineseries("https://www.cineserie.com/search/%s/?post_type=eb_video&post-category=%s" %(TitreUrl.replace(" ","+").lower(),typevideo))
    CineLink=[]
    h= HTMLParser.HTMLParser()
          
    if data:
          Liste=data.split('" class="tie-video video-popup"')
          for item in Liste:
            try:            
               videotype=(item.split('<span>')[1].split('</span')[0]) .lower()
            except:
               videotype=""
            if "nnonce" in videotype or "teaser" in videotype:
              try:
               Name=item.split('data-title="')[1].split('"')[0]
              except:
               Name=""
              if Name.lower()==Titre.lower():
                link=item.rsplit('href="')[1].split('">')[0]
                if 'https://www.cineserie.com' in link:
                  titreba=item.rsplit('href="')[1].split('">')[1].split('</a>')[0]
                  titreba=h.unescape(titreba)
                  if titreba.endswith('VO'):
                    langue='VO'
                  else:
                    langue='VF'              
                  if (typevideo!="eb_serie") or (typevideo=="eb_serie" and ('season' in titreba.lower() or not Saison) and not 'episode' in titreba.lower()):
                    CineLink.append({"url":link,"titre":titreba,"langue":langue})
                  if len(CineLink)>5:
                      break
          CineVideoLink=[]
          for item in CineLink:
            data=getCineseries(item.get("url"))
            
            if data:
              ItemAnnee=data.split('-date\/')[1].split('\/","')[0]
              logMsg("CineLinkAnnee : %s - %s" %(ItemAnnee,Annee))
              if ItemAnnee==Annee:
                linky=data.split('<div class="containerkowe">')[1]
                #allowfullscreen data-rocket-lazyload="fitvidscompatible" data-lazy-src="//videos.cineserie.com/player/index/98079/3/18"></iframe><nosc
                #link=linky.split("//")[1].split('" class="videokowe')[0]
                link=linky.split('src="//videos.cineserie.com/player/')[1].split('"')[0]
                CineVideoLink.append({"url":"https://videos.cineserie.com/player/"+link,"titre":item.get("titre"),"langue":item.get("langue")})
                
          for item in CineVideoLink:
            data=getCineseries(item.get("url"))
            if data:
              linkarray=data.split('{"sources":[')[1]
              newlinkjson='{'+data.split('vc.player_setup = {')[1].rsplit('};')[0].replace('\/','/')+'}'
              datajson=json.loads(newlinkjson)
              linkjson=datajson.get("playlist")[0].get('sources')
              titre=item.get("titre")
              vignette=datajson.get("playlist")[0].get('image')
              if linkjson:
                for itemx in linkjson:
                  label=itemx.get('label')
                  try:
                    qualite=int(label.replace('p',''))
                  except:
                    qualite=0
                  if qualite>=MediaQualite :
                    TrailerLink.append({"key":"Cineserie","typevideo":"trailer","type":"Bande-annonce","name":titre.replace('Bande-annonce','').replace(' VO','').replace(' VF',''),"key":"Cineserie","iso_3166_1":item.get("langue"),"size":str(qualite),"id":item.get("url"),"landscape":str(vignette)})
                    break
    
    return TrailerLink 
    
def BACineSeries(Titre=None,typevideo=None,Annee=None,Saison=None)  :
  TrailerLink=[]
  XQualite=[720,480,320]
  try:               
    MediaQualite=XQualite[int(SETTING("BAMiniQualite"))]
  except:
    MediaQualite=720 #par défaut
  
  if Titre: 
    #TitreUrl=Titre+" bande annonce"
    TitreUrl=Titre
    if typevideo!="tvshow":
        typevideo="eb_movie"
        
    else:
        typevideo="eb_serie"
        if Saison:
          TitreUrl=TitreUrl+" season %s" %(Saison) 
         
    
    data=getCineseries("https://www.cineserie.com/search/%s/?post_type=%s" %(TitreUrl.replace(" ","+").lower(),typevideo))
    CineLink=[]
    h= HTMLParser.HTMLParser()
          
    if data:
          Liste=data.split('<h2 class="post-box-title">')
          logMsg("LEN ITEM CINSERIES %d" %len(Liste))
          if len(Liste)>1:
            for item in Liste[1:]:
              #logMsg("ITEM CINSERIES %s" %item)
                try:            
                 Name=(item.split('data-title="')[1].split('"')[0]).replace('&rsquo;',"'")
                 Name=remove_accents(Name)
                except:
                 Name=None
                if Name and Name.lower()==Titre.lower():
                  link=item.split('data-title="')[1].split('href="')[1].split('">')[0]
                  if 'https://www.cineserie.com' in link:                
                    CineLink.append({"url":link,"titre":Name,"langue":"VO"})
                    logMsg("CineLink : %s" %link)
                    if len(CineLink)>5:
                        break
          CineVideoLink=[]
          for item in CineLink:
            data=getCineseries(item.get("url"))
            
            if data:
              ItemAnnee=data.split('-date\/')[1].split('\/","')[0]
              logMsg("CineLinkAnnee : %s - %s" %(ItemAnnee,Annee))
              if ItemAnnee==Annee:
                linky=data.split('<div class="containerkowe">')[1]
                #allowfullscreen data-rocket-lazyload="fitvidscompatible" data-lazy-src="//videos.cineserie.com/player/index/98079/3/18"></iframe><nosc
                #link=linky.split("//")[1].split('" class="videokowe')[0]
                link=linky.split('src="//videos.cineserie.com/player/')[1].split('"')[0]
                CineVideoLink.append({"url":"https://videos.cineserie.com/player/"+link,"titre":item.get("titre"),"langue":item.get("langue")})
                
          for item in CineVideoLink:
            data=getCineseries(item.get("url"))
            if data:
              linkarray=data.split('{"sources":[')[1]
              newlinkjson='{'+data.split('vc.player_setup = {')[1].rsplit('};')[0].replace('\/','/')+'}'
              datajson=json.loads(newlinkjson)
              linkjson=datajson.get("playlist")[0].get('sources')
              titre=item.get("titre")
              vignette=datajson.get("playlist")[0].get('image')
              if linkjson:
                for itemx in linkjson:
                  label=itemx.get('label')
                  try:
                    qualite=int(label.replace('p',''))
                  except:
                    qualite=0
                  if qualite>=MediaQualite :
                    TrailerLink.append({"key":"Cineserie","typevideo":"trailer","type":"Bande-annonce","name":titre.replace('Bande-annonce','').replace(' VO','').replace(' VF',''),"key":"Cineserie","iso_3166_1":item.get("langue"),"size":str(qualite),"id":item.get("url"),"landscape":str(vignette)})
                    break
    
    return TrailerLink 
         
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

       
       sed = Aujourdhui.strftime('%Y%m%d')
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
     if Liste and len(Liste)>0:
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
    MediaQualite=XQualite[int(SETTING("BAMiniQualite"))]
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
              try:
                 total=int(jsonobject.get("totalResults") )
              except:
                 total=0
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
    try:
      resp = conn.getresponse()
    except:
      resp = 400
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
     if Liste and len(Liste)>0:
       for Item in Liste:   
          KODIID=Item.get("kodiid")
          TMDBID=Item.get("tmdbid")
          IMDBID=Item.get("imdbid")
          if not TMDBID:
             #TMDBID=get_externalID(IMDBID,"movie")
             TMDBID=get_TMDBID("movie",KODIID,None)
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
     

     
     if ID:
        if DbType: 
          try:               
            MediaQualite=int(XQualite[int(SETTING("BAMiniQualite"))])
          except:
            MediaQualite=720 #par défau
          logMsg("getTrailer (%s)(%s)" %(DbType,ID))
          if DbType!="movie":
               query_url ="%stv/%s/videos?api_key=%s&language=%s&include_adult=true" % (BaseUrlTMDB,ID,TMDBApiKey,KODILANGCODE)
          else:
               query_url ="%smovie/%s/videos?api_key=%s&language=%s&include_adult=true" % (BaseUrlTMDB,ID,TMDBApiKey,KODILANGCODE)
          json_data = requestUrlJson(query_url) #en francais
          if json_data:
            Donnees=json_data.get("results")               
          if DbType!="movie":
               query_url ="%stv/%s/videos?api_key=%s&language=en&include_adult=true" % (BaseUrlTMDB,ID,TMDBApiKey)
          else:
               query_url ="%smovie/%s/videos?api_key=%s&language=en&include_adult=true" % (BaseUrlTMDB,ID,TMDBApiKey)
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
                    #if Site=="youtube" and ItemSize>=MediaQualite and (TypeTrailer=="trailer" or not AnnonceUniquement):
                    if Site=="youtube" and ItemSize>=MediaQualite and TypeTrailer=="trailer":
                         Item["position"]=str(cc) 
                         Item["id"]='plugin://plugin.video.youtube/play/?video_id=%s' %(Item["key"])                         
                         Item["landscape"]="http://img.youtube.com/vi/%s/hqdefault.jpg" %(Item["key"]) 
                         Item["key"]="YouTube"      
                         ListeTrailer.append(Item)
                         cc=cc+1
     return ListeTrailer
                    
  
"""
def getRuntime(ItemId=None,TypeID=None):
    RuntimeDB= ""
    query_url=""
    xxx=""
    if ItemId:  xxx=get_externalID(ItemId,TypeID)
    if xxx:
      if TypeID=="movie":
          query_url = "%smovie/%s?api_key=%s&include_adult=true" % (xxx,TMDBApiKey)
      if TypeID=="episode":
         query_url = "%stv/%s?api_key=%s&include_adult=true" % (xxx,TMDBApiKey)
    
      json_data = requestUrlJson(query_url)      
    
      if json_data:
        RuntimeDB = json_data['runtime']        
                  
    return str(RuntimeDB)
"""
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
  return None
    
def get_TMDBIDtest(ItemId=None,ismovie=None,ItemSource=None):
   ItemIdR=""
  
   if ItemId:

     query_url = "%sfind/%s?api_key=%s&language=%s&external_source=%s_id&include_adult=true" % (BaseUrlTMDB,ItemId,TMDBApiKey,KODILANGCODE,ItemSource)
     
     json_data = requestUrlJson(query_url)
     
 
     ItemIdR=str(ItemId) 
     if json_data:
           if ismovie!="movie": 
            allID=json_data.get("tv_results")
           else:
            allID=json_data.get("movie_results")
           if allID and len(allID)>0:
               for item in allID:
                     ItemIdR=item.get("id")
                     break
     #logMsg("json_data (%s)(%s)" %(ItemId,json_data))
     
   return str(ItemIdR)
   
def get_TMDBID(DbType=None,KodiId=None,UniqueId=None):
   externalXX=None
   ItemIdR=None
   
   if not UniqueId and KodiId and DbType:
      if DbType=="episode":
        json_result = getJSON("VideoLibrary.GetEpisodeDetails",'{"episodeid":%d,"properties":["tvshowid"]}' %(int(KodiId)))
        if json_result:
          KodiId=json_result.get("tvshowid")
        else :
          return None
         
         
      json_result = getJSON("VideoLibrary.Get%sDetails" %(DbType), '{"%sid":%d,"properties":["uniqueid"]}' %(DbType,int(KodiId)))
      if json_result:
        UniqueId=json_result.get("uniqueid")
        
   
   
   if UniqueId:
       IMDBNUMBER=UniqueId.get("imdb")
       TMDBNUMBER=UniqueId.get("tmdb")
       TVDBNUMBER=UniqueId.get("tvdb")
       UNKNNUMBER=UniqueId.get("unknown")
       if TMDBNUMBER:
         return str(TMDBNUMBER)
       elif TVDBNUMBER:
         externalXX="tvdb_id"
         ItemId=str(TVDBNUMBER)
       elif IMDBNUMBER:
         if str(IMDBNUMBER).find('tt')==-1:
           externalXX=None
         else:
           externalXX="imdb_id"
           ItemId=str(IMDBNUMBER)
       else:
         externalXX=None
       
   if externalXX:
     query_url = "%sfind/%s?api_key=%s&language=%s&external_source=%s&include_adult=true" % (BaseUrlTMDB,ItemId,TMDBApiKey,KODILANGCODE,externalXX) 
     logMsg("get_TMDBID(%s)" %query_url)    
     json_data = requestUrlJson(query_url)
     ItemIdR=str(ItemId) 
     if json_data:
           if DbType!="movie": 
            allID=json_data.get("tv_results")
           else:
            allID=json_data.get("movie_results")
           if allID and len(allID)>0:
               for item in allID:
                     ItemIdR=item.get("id")
                     break
     #logMsg("json_data (%s)(%s)" %(ItemId,json_data))
   if ItemIdR:  
     return str(ItemIdR)
   else:
    return None
   
   

    
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
        ListeVuesTriee=GetModeVues(content_type) 
        choixpossibles=[]
        
        if KODI_VERSION>=17:
          ListeVues,choixpossibles=retourListeVues(ListeVuesTriee)
        else:           
            if ListeVuesTriee:
              for view in ListeVuesTriee:
                      label = view[0]
                      viewid = view[1]
                      mediatypes = view[2]                
                      image = view[3]
                      ListeVues.append(label)
                      choixpossibles.append(str(viewid))
        dialogC = xbmcgui.Dialog()
        result=dialogC.select(xbmc.getLocalizedString(629), ListeVues)
        if result>=0:
             vue = str(choixpossibles[result])
             xbmc.executebuiltin("Container.SetViewMode(%s)" % vue)
             xbmc.executebuiltin("SetFocus(55)")     

def GetModeVues(content_type=None):
        
        ListeVuesTriee=[] 
        ListeVues=[] 
        
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
            reindex=None
            cpt=0  
            for item in ListeVuesTriee:
              label = item[0]
              if VueActuelle==try_decode(label):
                item[0]="[COLOR=yellow][B]"+item[0]+"[/B][/COLOR]"
                reindex=cpt
                break
              cpt=cpt+1

            if reindex and reindex>0:
              cpt=reindex
              LL=[]
              while cpt<len(ListeVuesTriee):
                LL.append(ListeVuesTriee[cpt])
                cpt=cpt+1
              cpt=0
              while cpt<reindex:
                LL.append(ListeVuesTriee[cpt])
                cpt=cpt+1
              ListeVuesTriee=LL 
        return ListeVuesTriee 
        
def retourListeVues(ListeVuesTriee=None) :
  ListeVues = []
  choixpossibles=[]
  if ListeVuesTriee:
    for view in ListeVuesTriee:
      label = view[0] 
      viewid = view[1]
      mediatypes = view[2]                
      image = view[3]
      
      Elements = xbmcgui.ListItem(label=label, iconImage=image,label2="selectionnevue",path="RunScript(script.iconmixtools,setviewmenu=True&id=%s)" % viewid)
      Elements.setProperty("viewid", viewid)
      Elements.setProperty("icon", image)
      ListeVues.append(Elements)
      choixpossibles.append(str(viewid))
      #logMsg("Vues : (%s)(%s)(%s)" %(current_view,viewid,label))
    return ListeVues,choixpossibles
  else:
    return None,None
  
def ModeVuesMenu(content_type=None, current_view=None):
        label = ""
        
        ListeVuesTriee=GetModeVues(content_type) 
        ListeVues,choixpossibles=retourListeVues(ListeVuesTriee)
        
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
        elif jsonobject.has_key('seasons'):
            return jsonobject['seasons']
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
        elif "GetProperties" in method:
            return jsonobject
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
    if msg and SETTING("iconmixdebug")=="true" : # or level == 0:
        if isinstance(msg, unicode):
            msg = msg.encode('utf8')
        if "exception" in msg.lower() or "error" in msg.lower():
            xbmc.log("IconMixTools addon --> " + msg, level=xbmc.LOGERROR)
            #print_exc()
        else:
            xbmc.log("IconMixTools addon --> " + msg, level=xbmc.LOGNOTICE)

def GetCache(search_str=None,Cache=None):
   if Cache:
     if SETTING("autocomplete_cache")=="true":
       if xbmcvfs.exists(Cache):
             with open(Cache) as data_file:
              ArrayCollection = json.load(data_file)
              data_file.close()
              try:
                if search_str:
                  Liste=[]
                  recherche=search_str.lower()
                  for item in ArrayCollection.get("resultats"):
                    if recherche in item["label"].lower():
                      Liste.append(item)
                  return Liste
                else:
                  return ArrayCollection.get("resultats")
              except:
                return []
     if search_str:
          MaxItems=50
          if "films" in Cache:
            logMsg("ICI : %s,%s" %(Cache,search_str))
            return getJSON("VideoLibrary.GetMovies", '{"limits":{"end":%d},"filter":{"field":"%s","operator":"contains","value":"%s"},"properties":["setid"]}' %(MaxItems,"title",search_str))

          if "tvshows"  in Cache:
            return getJSON("VideoLibrary.GetTvShows", '{"limits":{"end":%d},"filter":{"field":"%s","operator":"contains","value":"%s"},"properties":["episode"]}' %(MaxItems,"title",search_str))
           
             
          if "episodes"  in Cache:
            return getJSON("VideoLibrary.GetEpisodes", '{"limits":{"end":%d},"filter":{"field":"%s","operator":"contains","value":"%s"},"properties":["tvshowid"]}' %(MaxItems,"title",search_str))

          if "acteurs"  in Cache:
            return getJSON("Files.GetDirectory", '{"directory":"videodb://movies/actors"}')
            ListeActors=[]
            if json_result:
              for item in json_result:
                 ListeActors.append({"actormovieid":item.get("id"),"label":item["label"]}) 
                
            json_result = getJSON("Files.GetDirectory", '{"directory":"videodb://tvshows/actors"}')
            if json_result:
              for item in json_result:
                ListeActors.append({"actortvshowid":item.get("id"),"label":item["label"]})
            return ListeActors  
          
          if "realisateurs"  in Cache:
            json_result = getJSON("Files.GetDirectory", '{"directory":"videodb://movies/directors"}')
            Listedirectors=[]
            if json_result:          
              for item in json_result:
                  Listedirectors.append({"directormovieid":item.get("id"),"label":item["label"]})
            """
            json_result = getJSON("Files.GetDirectory", '{"directory":"videodb://tvshows/directors"}')
            if json_result:
              for item in json_result:
                  Listedirectors.append({"directortvshowid":item.get("id"),"label":item["label"]})
            """            
            return Listedirectors 
            
          if "addons"  in Cache:
            json_result = getJSON("Addons.GetAddons", '{"properties":["name"]}')
            Listeaddons=[]
            if json_result:          
              for item in json_result:
                  Listeaddons.append({"addonid":item.get("id"),"label":item["name"],"type":item["type"]})
            return Listeaddons        
          
          if "artistes"  in Cache:
            return getJSON("AudioLibrary.GetArtists", '{"limits":{"end":%d},"filter":{"field":"%s","operator":"contains","value":"%s"}}' %(MaxItems,"artist",search_str))


          if "albums"  in Cache:
            return getJSON("AudioLibrary.GetAlbums", '{"limits":{"end":%d},"filter":{"field":"%s","operator":"contains","value":"%s"},"properties":["artistid"]}' %(MaxItems,"album",search_str))

   return {}

def SaveFile(savepath=None,save_data=None):
  if savepath and save_data:
    erreur=DirStru(savepath) 
    try:
      with io.open(savepath, 'w+', encoding='utf8',errors='ignore') as outfile: 
        str_ = json.dumps(save_data,indent=4, sort_keys=True,separators=(',', ':'), ensure_ascii=False)
        outfile.write(to_unicode(str_))
    except:
        logMsg("Erreur SAVEFILE io.open (%s)" %(savepath) )


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
            Resultat["AlbumLabel"]=Item.get("strLabel")
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
   
           

        if SETTING("cachemusic")=="false"  and savepath:
            erreur=DirStru(savepath) 
            save_data["kodiArtisteId"]=str(ArtisteId)
            try:
              with io.open(savepath, 'w+', encoding='utf8',errors='ignore') as outfile: 
                str_ = json.dumps(save_data,indent=4, sort_keys=True,separators=(',', ':'), ensure_ascii=False)
                outfile.write(to_unicode(str_))
            except:
                logMsg("Erreur GetMusicFicheArtiste io.open (%s)" %(savepath) )
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
              save_data["AlbumStudio"]=Details.get("AlbumStudio")
              
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
  
              
        if MAJ==1 and SETTING("cachemusic")=="false"  and savepath:
            erreur=DirStru(savepath)             
            save_data["kodiArtisteId"]=str(ArtisteId)
            save_data["Artiste"]=unidecode(Artiste)
            #save_data["albumsdetails"]=albumIdBrainz
            try:
              with io.open(savepath, 'w+', encoding='utf8',errors='ignore') as outfile: 
                str_ = json.dumps(save_data,indent=4, sort_keys=True,separators=(',', ':'), ensure_ascii=False)
                outfile.write(to_unicode(str_)) 
            except:
              logMsg("Erreur GetMusicFicheAlbum io.open (%s)" %(savepath) )    
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
BaseUrlTMDB=CheckTMDB()