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
import sqlite3
import operator
import locale
import hashlib
import base64
import xml.etree.ElementTree as ET
    
try:
    to_unicode = unicode
except NameError:
    to_unicode = str
    
Allocinepartner_key  = '100043982026'  

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
WINDOW = xbmcgui.Window(10000)
SETTING = ADDON.getSetting
KODILANGUAGE = xbmc.getInfoLabel( "System.Language" )
sys.path.append(xbmc.translatePath(os.path.join(ADDON_PATH, 'resources', 'lib')).decode('utf8'))


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

# ------------------------------------SAGAS--------------------------------------------------------------    

    
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
         ArrayCollection=getsagaitem(ItemId,1,None,None,json_result)
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
                 ArrayCollection=getsagaitem(ItemId,1,ArrayCollection.get("kodicollection"),ArrayCollection.get("tmdbid"),json_result)
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
                    ItemListe.setArt({"fanart":"http://image.tmdb.org/t/p/original"+fanart})
                ItemListe.setInfo("video", {"title": item.get("title"),"mediatype": "movie","year": item.get("release_date"),"plot": item.get("overview"),"originaltitle": item.get("originaltitle")})        
                ItemListe.setProperty('IMDBNumber', '')
                ItemListe.setProperty('TMDBNumber', str(item.get("id")))
                ItemListe.setProperty('DateSortie', DateSortie)
                ItemListe.setProperty('dbtype', 'movie')
                
                ItemListe.setProperty('SetId', str(ItemId))
                ItemListe.setProperty('PosterCollection',PosterCollection)
                ItemListe.setProperty('Rating',str(int(item.get("vote_average"))))
                ItemListe.setProperty('UserRating','')
                if not Statique:
                   ListeItem.append([item.get("file"),ItemListe,True])
                else:
                   ListeItem.append([int(item.get("release_date")[0:4]),ItemListe])
       #----------------------------BASE LOCALE ----------------------------
       
       #json_result = getJSON('VideoLibrary.GetMovieSetDetails', '{ "setid":%d,"movies": {"properties":["title","genre","year","rating","userrating","director","trailer","tagline","plot","plotoutline","originaltitle","lastplayed","playcount","writer","studio","mpaa","cast","country","imdbnumber","runtime","set","showlink","streamdetails","top250","votes","fanart","thumbnail","file","sorttitle","resume","setid","dateadded","tag","art"]} }' %(int(ItemId)))
       for item in json_result.get("movies"): 
          ImdbItem.append(item.get("imdbnumber"))
       Compteur = {}.fromkeys(set(ImdbItem),0)
       for valeur in ImdbItem:
          Compteur[valeur] += 1
  
    
       for item in json_result.get("movies"):
          ItemListe = xbmcgui.ListItem(label=item.get("label"),path=item.get("file"))
          
          item["DBID"]=item.get("movieid")
          ImdbNumber=item.get("imdbnumber")
          FileTab.append( os.path.dirname(item.get("file"))+"\\")          
          
          #pistes audios
          Audio=item.get("streamdetails").get("audio")
          i=1
          if Audio:               
               for AudioElement in Audio:
                    ItemListe.setProperty('AudioLanguage.%d' %(i), AudioElement.get("language"))
                    ItemListe.setProperty('AudioChannels.%d' %(i), str(AudioElement.get("channels")))
                    ItemListe.setProperty('AudioCodec.%d' %(i), AudioElement.get("codec"))                    
                    i=i+1
    
          #pistes vidéos 
          Video=item.get("streamdetails").get("video")
          i=0
          Codec=""
          if Video:
            for VideoItem in Video:
               ItemListe.setProperty('VideoCodec', VideoItem.get("codec")) 
               
          #sous-titres     
          Subtitles=item.get("streamdetails").get("subtitle")
          i=1
          
          if Subtitles:
               for SubtitleElement in Subtitles:
                    ItemListe.setProperty('SubtitleLanguage.%d' %(i), SubtitleElement.get("language"))                     
                    i=i+1
                   
            
          ItemListe.setProperty('DBID', str(item.get("DBID")))
          ItemListe.setProperty('SetId', str(ItemId))
          ItemListe.setProperty('IMDBNumber', str(item.get("imdbnumber")))
          ItemListe.setProperty('TMDBNumber', '')
          ItemListe.setProperty('DateSortie', '')
          ItemListe.setProperty('doublons',str(Compteur[item.get("imdbnumber")]))
          ItemListe.setProperty('PosterCollection',PosterCollection)
          ItemListe.setProperty('Rating',str(int(item.get("rating"))))
          UserRating=item.get("userrating")
          if UserRating:
             if int(UserRating)>0:
               ItemListe.setProperty('UserRating',str(int(item.get("userrating"))))
             else:
               ItemListe.setProperty('UserRating','')
         
          if item.get("art"):
                ItemListe.setArt( item.get("art"))
          ItemListe.setIconImage(item.get("thumbnail")) 
          Position=int(item.get("resume").get("position"))*100
          Total=int(item.get("resume").get("total"))
          
          try :
             PercentPlayed=Position/Total
          except:
             PercentPlayed=""
          ItemListe.setProperty('PercentPlayed', str(PercentPlayed))
          ItemListe.setInfo("dbid", str(item.get("movieid")))
          ItemListe.setInfo("video", {"dbid": str(item.get("movieid")),"duration": item.get("runtime"), "title": item.get("title"),"mediatype": "movie","genre": item.get("genre"),"year": item.get("year"),"plot": item.get("plot"),"plotoutline": item.get("plotoutline"),"originaltitle": item.get("originaltitle"),"playcount":item.get("playcount")}) 
          NbKodi=NbKodi+1
          if int(Compteur[item.get("imdbnumber")])>0:
             NbKodiValide=NbKodiValide+1
             if not Statique:
               ListeItem.append([item.get("file"),ItemListe,True])
             else:
               ListeItem.append([int(item.get("year")),ItemListe])
             
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
          
          
def getdatafanart(donnees=None):
  pardefaut=None
  langue=KODILANGUAGE.lower()[0:2]
  if donnees:
     
     for item in donnees:
       if item.get("lang")=="en":
        pardefaut=item.get("url")   
       if item.get("lang")==langue:  
         return item.get("url")
     return pardefaut
  
  return None  
    
      
  
def getsagaartworks(IDCollection=None)   :
  ArtWorks={}
  if IDCollection:
    UrlFanartTv="http://webservice.fanart.tv/v3/movies/%d?api_key=769f122ee8aba06f4a513830295f2bc0" %(int(IDCollection)) #infos completes
  
    json_data = requestUrlJson(UrlFanartTv)  
    
    if json_data:      
      #logo,clearart,banner,poster,fanart,thumb,discart  
      
      ArtWorks["logo"]=getdatafanart(json_data.get("hdmovielogo"))      
      ArtWorks["clearart"]=getdatafanart(json_data.get("hdclearart"))
      ArtWorks["banner"]=getdatafanart(json_data.get("moviebanner"))
      ArtWorks["poster"]=getdatafanart(json_data.get("movieposter"))
      ArtWorks["fanart"]=getdatafanart(json_data.get("moviebackground"))
      ArtWorks["thumb"]=getdatafanart(json_data.get("moviethumb"))
      ArtWorks["discart"]=getdatafanart(json_data.get("moviediscart"))
      
            
      
      #clearart,banner,poster,fanart,thumb,discart,  
      
      return ArtWorks
  return None
  

    
def getsagaitem(ItemIdxx=None,ShowBusy=None,AKodiCollection=None,ATmdbId=None,json_result=None):
  episodesDB= ""
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
  
  check_clearlogo=None
  check_clearart=None
  check_banner=None
  check_poster=None
  check_fanart=None
  check_thumb=None
  check_discart=None  
  
  
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
        
      if ItemId:
                if not ATmdbId:
                   #numero de collection TMDB inconnu
                   query_url = "https://api.themoviedb.org/3/movie/%s?api_key=67158e2af1624020e34fd893c881b019&language=%s" % (ItemId,xbmc.getInfoLabel("System.Language").encode("utf8"))
                   json_data = requestUrlJson(query_url)
                   
                   if json_data:
                      Rspcollection=json_data.get("belongs_to_collection")
                      if Rspcollection: IDcollection=Rspcollection.get("id")
                else: 
                   IDcollection=ATmdbId
                   
                if IDcollection:
                     query_url = "https://api.themoviedb.org/3/collection/%d?api_key=67158e2af1624020e34fd893c881b019&language=%s" % (IDcollection,xbmc.getInfoLabel("System.Language").encode("utf8"))
                     json_data = requestUrlJson(query_url)
                     

                     if json_data:
                         Rspcollection=json_data.get("parts")
                         if json_data.get("poster_path"):
                            PosterCollection="http://image.tmdb.org/t/p/original"+json_data.get("poster_path")

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
                            if IDcollection:
                              ArtWorks=getsagaartworks(IDcollection)
                            else:
                              ArtWorks=None
                            if ArtWorks:
                              ArrayCollection["artworks"]=ArtWorks
                            else:
                              ArtWorks=ArrayCollection.get("artworks")
                                  
                            #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.SetMovieSetDetails","params":{"setid":38,"art":{"poster":"http://image.tmdb.org/t/p/original/zrApSsUX9i0qVntcCD0Pp55TdCy.jpg"}},"id":1}
                            if KODI_VERSION>=17 and ArtWorks and  SETTING("updatesagaposter")=="true": 
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
  

def UpdateSagas(Une=None,Toutes=None):
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
               getsagaitem(ItemId,None,None,None,None)   
               Titre=xbmc.getLocalizedString( 31924 )+" : [I]"+Sagas.get("label")+"[/I]"
            Progres=(Compteur*100)/NbItems
            Compteur=Compteur+1
            if Toutes: dp.update(Progres,Titre,"(%d/%d)" %(Compteur,NbItems))
            else : dp.update(Progres,Titre,"...")
            if dp.iscanceled(): break
       dp.close()  
     else :
          getsagaitem(str(Une),1,None,None,None)        
            
     
     
# --------------------------------------------------------------------------------------------------
    


# --------------------------------------------SERIES-------------------------------------------
def getepisodes(UniqueId=None,saisonID=None,DBtype=None,NbEpisodesKodi=None):
  episodesDB= ""
  AllSeasons= []
  AllEpisodes=[]
  ArrayCollection={}
  NbEpisodes=-1
  KodiId=None
  NbKodi=None
  ItemId=""
  
  nowX = datetime.datetime.now().date()
  nowX2=nowX
  ItemListe=0
  tsea=0
  
  if UniqueId and DBtype:
    
    if DBtype=="season":
     xxx=xbmc.getInfoLabel("Container.FolderPath")
     xx=xxx.split("titles/")[1]
     UniqueId=xx.split("/")[0]
     if UniqueId:
      KodiId=UniqueId
      json_result = getJSON('VideoLibrary.GetTVShowDetails', '{ "tvshowid":%d,"properties": [ "title", "imdbnumber","episode","season" ]}' %(int(UniqueId)))
      if json_result: 
          UniqueId=json_result.get("imdbnumber")
          NbKodi=json_result.get("episode")
          
      else : UniqueId="" 
  	#oblige d'aller chercher l'IMDB de la serie mere dans la fiche tvshow !!! pouviez pas ajouter un champ dans la base ???? grrrrrrrrr !!!!!!
  	#quel bordel mon colonel !
  	#http://127.0.0.1:8080/jsonrpc?request={ "jsonrpc ": "2.0 ", "method ": "VideoLibrary.GetEpisodeDetails ", "params ":{ "episodeid ":220, "properties ":[ "title ", "tvshowid "]}, "id ":1}
    if DBtype=="episode":
      json_result = getJSON('VideoLibrary.GetEpisodeDetails', '{ "episodeid":%d,"properties": [ "title", "tvshowid" ]}' %(int(UniqueId)))
      if json_result and json_result.get("tvshowid"):
         UniqueId=json_result.get("tvshowid")
         KodiId=UniqueId
         #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.GetTVShowDetails","params":{"UniqueId":40,"properties":["title","imdbnumber"]},"id":1}
         json_result = getJSON('VideoLibrary.GetTVShowDetails', '{ "tvshowid":%d,"properties": [ "title", "imdbnumber","episode" ]}' %(int(UniqueId)))
         if json_result and json_result.get("imdbnumber"):
            UniqueId=json_result.get("imdbnumber")
            NbKodi=json_result.get("episode")
            
         else : UniqueId=""
    else : 
      if DBtype=="tvshow": 
        KodiId=xbmc.getInfoLabel("ListItem.DBID")
        UniqueId=xbmc.getInfoLabel("ListItem.IMDBNumber")
        NbKodi=int(xbmc.getInfoLabel("ListItem.Property(TotalEpisodes)"))
     
    if UniqueId:
      savepath=ADDON_DATA_PATH+"/series/tv%s" %(UniqueId)
      #if not os.path.exists(savepath):
      if not xbmcvfs.exists(savepath):
     #creation
         ArrayCollection=getallepisodes(KodiId,UniqueId,savepath,NbKodi,1)
         
      else : 
    #if os.path.exists(savepath):      
         with open(savepath) as data_file:
            ArrayCollection = json.load(data_file)
            data_file.close()
         if not ArrayCollection or not ArrayCollection.get("v5"): # si fichier foireux ?
          #mise a jour
            ArrayCollection=getallepisodes(KodiId,UniqueId,savepath,NbKodi,1)
      if ArrayCollection:
            WINDOW.setProperty('ItemCountry1',ArrayCollection.get("pays"))  
            
            
            if ArrayCollection.get("dateecheance"):
               try:
                  nowX2 = datetime.datetime.strptime(str(ArrayCollection.get("dateecheance")), '%Y-%m-%d').date()
               except:
                  nowX2=nowX  
            if NbKodi:   
               if str(ArrayCollection.get("tmdbid"))!=str(UniqueId) or str(ArrayCollection.get("nbkodi"))!=str(NbKodi) or not ArrayCollection.get("v5") or nowX>nowX2 :
                     
              #
                  #mise a jour
                  ArrayCollection=getallepisodes(KodiId,UniqueId,savepath,NbKodi,1)
                  
            if ArrayCollection and saisonID:
                     try:
                        NbEpisodes=int(ArrayCollection.get("saisons").get(str(saisonID)).get("NbEpisodes"))
                     except:
                        NbEpisodes=-1
            if ArrayCollection:
                     WINDOW.setProperty('ItemCountry1',ArrayCollection.get("pays"))
                     
            if NbEpisodesKodi:
              if NbEpisodes==int(NbEpisodesKodi):
                 NbEpisodes=0 #complet  
      
  return NbEpisodes

def getdatafanarttv(donnees=None,saison=None):  
  langue=KODILANGUAGE.lower()[0:2]
  pardefaut=None
  if donnees:
     for item in donnees:
       if item.get("lang")=="en" and item.get("season")==saison:
        pardefaut=item.get("url")   
       if item.get("lang")==langue and item.get("season")==saison:  
         return item.get("url")
     return pardefaut
  
  return None
  
def gettvartworks(IDCollection=None)   :
  ArtWorks={}
  ArtWorkSeason={}
  if IDCollection:
    UrlFanartTv="http://webservice.fanart.tv/v3/tv/%d?api_key=769f122ee8aba06f4a513830295f2bc0" %(int(IDCollection)) #infos completes
    json_data = requestUrlJson(UrlFanartTv)
    
    if json_data:      
      #logo,clearart,banner,poster,fanart,thumb,discart  
      ArtWorks["logo"]=getdatafanart(json_data.get("hdtvlogo"))
      ArtWorks["clearart"]=getdatafanart(json_data.get("hdclearart"))
      ArtWorks["banner"]=getdatafanart(json_data.get("tvbanner"))
      ArtWorks["poster"]=getdatafanart(json_data.get("tvposter"))
      ArtWorks["fanart"]=getdatafanart(json_data.get("showbackground"))
      ArtWorks["thumb"]=getdatafanart(json_data.get("tvthumb"))
      ArtWorks["discart"]=None
      ArtWorks["characterart"]=getdatafanart(json_data.get("characterart"))
      ArtWorkSeason={"poster":json_data.get("seasonposter"),"thumb":json_data.get("seasonthumb"),"banner":json_data.get("seasonbanner")}
            
      
      #clearart,banner,poster,fanart,thumb,discart,  
      
      
      return ArtWorks,ArtWorkSeason
  return None,None 
   
def UpdateSeries(Une=None,Toutes=None):
     ItemId=0
     AllMovies= {}
     NbItems=0
     savepath=""
     Titre=""
     
    
     if not Une :
       dp = xbmcgui.DialogProgress()
       dp.create("IconMixTools",Titre,"")
       json_result = getJSON('VideoLibrary.GetTvShows', '{"properties":["imdbnumber","episode"]}')
       if json_result: 
          NbItems=len(json_result)
          Compteur=0
          for Series in json_result:
            ItemId=Series.get("tvshowid")
            ImdbNumber=Series.get("imdbnumber")
            NbKodi=Series.get("episode")
            savepath=ADDON_DATA_PATH+"/series/tv%s" %(ImdbNumber)
            
            if Toutes or not xbmcvfs.exists(savepath) and ItemId:                
               getallepisodes(ItemId,ImdbNumber,savepath,NbKodi,None)   
               Titre=xbmc.getLocalizedString( 20343 )+" : [I]"+Series.get("label")+"[/I]"
            Progres=(Compteur*100)/NbItems
            Compteur=Compteur+1
            if Toutes: dp.update(Progres,Titre,"(%d/%d)" %(Compteur,NbItems))
            else : dp.update(Progres,Titre,"...")
            if dp.iscanceled(): break
       dp.close() 
     else :
          NbKodi=int(xbmc.getInfoLabel("ListItem.Property(TotalEpisodes)"))
          savepath=ADDON_DATA_PATH+"/series/tv%s" %(Une)
          getallepisodes(xbmc.getInfoLabel("ListItem.DBID"),Une,savepath,NbKodi,1)        
            
         
     


  
def getallepisodes(IdKodi=None,TvDbId=None,savepath=None,NbKodi=None,ShowBusy=None):
  
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
  ListePays={"AF":"Afghanistan","AL":"Albania","DZ":"Algeria","AS":"American Samoa","AD":"Andorra","AO":"Angola","AI":"Anguilla","AQ":"Antarctica","AG":"Antigua and Barbuda","AR":"Argentina","AM":"Armenia","AW":"Aruba","AU":"Australia","AT":"Austria","AZ":"Azerbaijan","BS":"Bahamas","BH":"Bahrain","BD":"Bangladesh","BB":"Barbados","BY":"Belarus",
"BE":"Belgium","BZ":"Belize","BJ":"Benin","BM":"Bermuda","BT":"Bhutan","BO":"Bolivia, Plurinational State of","BA":"Bosnia and Herzegovina","BW":"Botswana","BV":"Bouvet Island","BR":"Brazil","IO":"British Indian Ocean Territory","BN":"Brunei Darussalam","BG":"Bulgaria","BF":"Burkina Faso","BI":"Burundi","KH":"Cambodia","CM":"Cameroon","CA":"Canada","CV":"Cape Verde","KY":"Cayman Islands","CF":"Central African Republic","TD":"Chad",
"CL":"Chile","CN":"China","CX":"Christmas Island","CC":"Cocos (Keeling) Islands","CO":"Colombia","KM":"Comoros","CG":"Congo","CD":"Congo, the Democratic Republic of the","CK":"Cook Islands","CR":"Costa Rica","CI":"Côte d'Ivoire","HR":"Croatia","CU":"Cuba","CY":"Cyprus","CZ":"Czech Republic","DK":"Denmark","DJ":"Djibouti","DM":"Dominica","DO":"Dominican Republic","EC":"Ecuador","EG":"Egypt","SV":"El Salvador","GQ":"Equatorial Guinea","ER":"Eritrea","EE":"Estonia","ET":"Ethiopia","FK":"Falkland Islands (Malvinas)","FO":"Faroe Islands","FJ":"Fiji","FI":"Finland","FR":"France",
"GF":"French Guiana","PF":"French Polynesia","TF":"French Southern Territories","GA":"Gabon","GM":"Gambia","GE":"Georgia","DE":"Germany","GH":"Ghana","GI":"Gibraltar","GR":"Greece","GL":"Greenland","GD":"Grenada","GP":"Guadeloupe","GU":"Guam","GT":"Guatemala","GG":"Guernsey","GN":"Guinea","GW":"Guinea-Bissau","GY":"Guyana","HT":"Haiti","HM":"Heard Island and McDonald Islands","VA":"Holy See (Vatican City State)","HN":"Honduras","HK":"Hong Kong","HU":"Hungary","IS":"Iceland","IN":"India","ID":"Indonesia","IR":"Iran, Islamic Republic of","IQ":"Iraq","IE":"Ireland","IM":"Isle of Man",
"IL":"Israel","IT":"Italy","JM":"Jamaica","JP":"Japan","JE":"Jersey","JO":"Jordan","KZ":"Kazakhstan","KE":"Kenya","KI":"Kiribati","KP":"Korea, Democratic People's Republic of","KR":"Korea, Republic of","KW":"Kuwait","KG":"Kyrgyzstan","LA":"Lao People's Democratic Republic","LV":"Latvia","LB":"Lebanon","LS":"Lesotho","LR":"Liberia","LY":"Libyan Arab Jamahiriya","LI":"Liechtenstein","LT":"Lithuania","LU":"Luxembourg","MO":"Macao","MK":"Macedonia, the former Yugoslav Republic of","MG":"Madagascar","MW":"Malawi","MY":"Malaysia","MV":"Maldives","ML":"Mali","MT":"Malta","MH":"Marshall Islands","MQ":"Martinique","MR":"Mauritania","MU":"Mauritius","YT":"Mayotte","MX":"Mexico","FM":"Micronesia, Federated States of","MD":"Moldova, Republic of","MC":"Monaco",
"MN":"Mongolia","ME":"Montenegro","MS":"Montserrat","MA":"Morocco","MZ":"Mozambique","MM":"Myanmar","NA":"Namibia","NR":"Nauru","NP":"Nepal","NL":"Netherlands","AN":"Netherlands Antilles","NC":"New Caledonia","NZ":"New Zealand","NI":"Nicaragua","NE":"Niger","NG":"Nigeria","NU":"Niue","NF":"Norfolk Island","MP":"Northern Mariana Islands","NO":"Norway","OM":"Oman","PK":"Pakistan","PW":"Palau","PS":"Palestinian Territory, Occupied","PA":"Panama","PG":"Papua New Guinea","PY":"Paraguay","PE":"Peru","PH":"Philippines","PN":"Pitcairn","PL":"Poland","PT":"Portugal","PR":"Puerto Rico",
"QA":"Qatar","RE":"Réunion","RO":"Romania","RU":"Russian Federation","RW":"Rwanda","BL":"Saint Barthélemy","SH":"Saint Helena, Ascension and Tristan da Cunha","KN":"Saint Kitts and Nevis","LC":"Saint Lucia","MF":"Saint Martin (French part)","PM":"Saint Pierre and Miquelon","VC":"Saint Vincent and the Grenadines","WS":"Samoa","SM":"San Marino","ST":"Sao Tome and Principe","SA":"Saudi Arabia","SN":"Senegal","RS":"Serbia","SC":"Seychelles","SL":"Sierra Leone","SG":"Singapore","SK":"Slovakia","SI":"Slovenia","SB":"Solomon Islands","SO":"Somalia","ZA":"South Africa","GS":"South Georgia and the South Sandwich Islands","ES":"Spain","LK":"Sri Lanka","SD":"Sudan","SR":"Suriname","SJ":"Svalbard and Jan Mayen","SZ":"Swaziland","SE":"Sweden","CH":"Switzerland","SY":"Syrian Arab Republic","TW":"Taiwan, Province of China",
"TJ":"Tajikistan","TZ":"Tanzania, United Republic of","TH":"Thailand","TL":"Timor-Leste","TG":"Togo","TK":"Tokelau","TO":"Tonga","TT":"Trinidad and Tobago","TN":"Tunisia","TR":"Turkey","TM":"Turkmenistan","TC":"Turks and Caicos Islands","TV":"Tuvalu","UG":"Uganda","UA":"Ukraine","AE":"United Arab Emirates","GB":"United Kingdom","US":"United States of America","UM":"United States Minor Outlying Islands","UY":"Uruguay","UZ":"Uzbekistan","VU":"Vanuatu","VE":"Venezuela, Bolivarian Republic of","VN":"Viet Nam","VG":"Virgin Islands, British","VI":"Virgin Islands, U.S.","WF":"Wallis and Futuna","EH":"Western Sahara","YE":"Yemen","ZM":"Zambia","ZW":"Zimbabwe"
}

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
         ArrayCollection["v5"]="ok"
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
                 qurl="https://api.themoviedb.org/3/find/%s?api_key=67158e2af1624020e34fd893c881b019&language=en-US&external_source=imdb_id"  % (ArrayCollection["imdbid"])
                 json_data2 = requestUrlJson(qurl)
                 if json_data2:
                   allID=json_data2.get("tv_results")
                   ArrayCollection["pays"]=""
                   if allID and len(allID)>0:
                      for Test in allID:
               	         ItemPays=Test.get("origin_country")[0]
                      ArrayCollection["pays"]=ListePays.get(ItemPays)
                 
                 
                 SaisonTab=SaisonTab.get("seasons_details")
                 if SaisonTab:
                 	  for item in SaisonTab:             	  	       
                             EpisodesEtcasting={} 
                             EpisodesEtcasting["NbEpisodes"]=item.get("episodes")
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

def GetImdbTvNumber(ItemIdxx=None,DBtype=None):

   if DBtype=="season":
     xxx=xbmc.getInfoLabel("Container.FolderPath")
     xx=xxx.split("titles/")[1]
     ItemIdxx=xx.split("/")[0]
     if ItemIdxx:
      json_result = getJSON('VideoLibrary.GetTVShowDetails', '{ "tvshowid":%d,"properties": [ "title", "imdbnumber","episode" ]}' %(int(ItemIdxx)))
      if json_result:
          ItemIdx=json_result.get("imdbnumber")
          NbKodi=json_result.get("episode")
      else : ItemIdx=""
   if DBtype=="episode":
      json_result = getJSON('VideoLibrary.GetEpisodeDetails', '{ "episodeid":%d,"properties": [ "title", "tvshowid" ]}' %(int(ItemIdxx)))
      if json_result and json_result.get("tvshowid"):
         ItemIdx=json_result.get("tvshowid")
         json_result = getJSON('VideoLibrary.GetTVShowDetails', '{ "tvshowid":%d,"properties": [ "title", "imdbnumber","episode" ]}' %(int(ItemIdx)))
         if json_result and json_result.get("imdbnumber"):
            ItemIdx=json_result.get("imdbnumber")
            NbKodi=json_result.get("episode")
         else : ItemIdx=""
   else :
      if DBtype=="tvshow":
        ItemIdx=xbmc.getInfoLabel("ListItem.IMDBNumber")
        NbKodi=int(xbmc.getInfoLabel("ListItem.Property(TotalEpisodes)"))
      
def getDiffusionTV(IdKodi=None,saisonID=None,DBtype=None):
  episodesDB= ""
  AllSeasons= []
  ArrayCollection={}
  ListeEpisodes=[]
  NbEpisodes=0
  NbKodi=0
  ItemId=""
  ItemIdx=""
  nowX = datetime.datetime.now().date()
  nowX2=nowX
  ItemListe=0
  tsea=0
  #betaseries : https://api.betaseries.com/episodes/next?key=46be59b5b866&thetvdb_id=261690
  # https://api.betaseries.com/shows/episodes?key=46be59b5b866&thetvdb_id=268592&season=4    épisodes de "the 100 saison 4"
  #https://api.betaseries.com/shows/episodes?key=46be59b5b866&thetvdb_id=268592  tous les épisodes de la série
  # { "episodes": 
  # [
  # {"id":315312,"thetvdb_id":4543295,"youtube_id":null,"title":"Pilot","season":1,"episode":1,
  #  "show":{"id":6622,"thetvdb_id":268592,"title":"The 100","in_account":false},
  #  "code":"S01E01","global":1,"special":0,"description":"97 ans apr\u00e8s une guerre nucl\u00e9aire, les derniers humains r\u00e9sident dans une station orbitale connue sous le nom de \u00ab The Ark \u00bb. Face \u00e0 des ressources qui deviennent insuffisantes, 100 d\u00e9linquants juv\u00e9niles sont envoy\u00e9s sur Terre pour d\u00e9couvrir si elle est peut-\u00eatre de nouveau vivable.",
  #  "date":"2014-03-19","note":{"total":3479,"mean":4.21,"user":0},"user":{"seen":false,"downloaded":false},
  # "comments":"89","resource_url":"https:\/\/www.betaseries.com\/episode\/the-hundred\/s01e01","subtitles":[]},
  # ...
  #  x episodes
  # ]}
  
  
  
  if ItemIdxx and DBtype and saisonID:
    
    if DBtype=="episode":
      json_result = getJSON('VideoLibrary.GetEpisodeDetails', '{ "episodeid":%d,"properties": [ "title", "tvshowid" ]}' %(int(ItemIdxx)))
      if json_result and json_result.get("tvshowid"):
         ItemIdx=json_result.get("tvshowid")
         json_result = getJSON('VideoLibrary.GetTVShowDetails', '{ "tvshowid":%d,"properties": [ "title", "imdbnumber","episode" ]}' %(int(ItemIdx)))
         if json_result and json_result.get("imdbnumber"):
            IdKodi=ItemIdx
            ItemIdx=json_result.get("imdbnumber")
            NbKodi=json_result.get("episode")
            
         else : ItemIdx=""
     
     
    if ItemIdx: #imdbnumber
      savepath=ADDON_DATA_PATH+"/series/tv%s" %(ItemIdx)
      if not xbmcvfs.exists(savepath):
          #creation !!!
          ArrayCollection=getallepisodes(IdKodi,ItemIdx,savepath,NbKodi,1)
      else :
          with open(savepath) as data_file:
            ArrayCollection = json.load(data_file)
            data_file.close()
          if not ArrayCollection: # si fichier foireux ?
            ArrayCollection=getallepisodes(IdKodi,ItemIdx,savepath,NbKodi,1)
          
  
      if ArrayCollection:
        if ArrayCollection.get("dateecheance"):
          try:
             nowX2 = datetime.datetime.strptime(str(ArrayCollection["dateecheance"]), '%Y-%m-%d').date()
          except:
             nowX2=nowX  
          
        if ArrayCollection.get("kodiid")!=IdKodi or ArrayCollection.get("nbkodi")!=NbKodi or nowX>nowX2:
             #mise à jour
             ArrayCollection=getallepisodes(IdKodi,ArrayCollection.get("tmdbid"),savepath,NbKodi)
             
        if ArrayCollection:
                AllSeasons=ArrayCollection.get("saisons")
                if AllSeasons :
                   AllEpisodes=AllSeasons[str(saisonID)]
                   if AllEpisodes:
                      for item in AllEpisodes:
                         Nom=item.get("name")
                         DateDiffusion=item.get("air_date")
                         Poster=item.get("poster")
                         if not Poster: Poster="DefaultTVShows.png"
                         else: Poster="http://image.tmdb.org/t/p/original"+str(Poster)
                         if Nom and DateDiffusion:
                              ItemListe=xbmcgui.ListItem(label=Nom,iconImage=Poster,label2=DateDiffusion)
                              ListeEpisodes.append(["", ItemListe, False])
   
    xbmcplugin.addDirectoryItems(int(sys.argv[1]), ListeEpisodes)
  xbmcplugin.endOfDirectory(int(sys.argv[1]))
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

def getSagaFanarts():
  ListeFanarts=[] 
  
  c=0
  d=int(xbmc.getInfoLabel("Container(1999).NumItems")) 
  while c<d:
    ItemPath=CheckItemExtrafanartPath(xbmc.getInfoLabel("Container(1999).ListItem(%d).Path" %(c))) 
    if ItemPath!="":
      ListeFanart=get_filepaths(ItemPath)
  
      
    for Item in ListeFanart:
        ItemListe=xbmcgui.ListItem(label="extrafanart",iconImage=Item)
        ListeFanarts.append(["", ItemListe, False])        
    c=c+1
  
  xbmcplugin.addDirectoryItems(int(sys.argv[1]), ListeFanarts)
  xbmcplugin.endOfDirectory(int(sys.argv[1])) 
  
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
             ItemListe.setInfo("pictures", {"title": "extrafanart","picturepath": Item}) 
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
    
    """
    if directory:
      for root, directories, files in os.walk(directory):
          for filename in files:
              filepath = os.path.join(root, filename)
              file_paths.append(filepath)
    """
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
  if sys.argv[1]:

    if genretypex=="episode": #si content=episode -> tvshow
       genretypex="tvshow"
       origtitle=xbmc.getInfoLabel("ListItem.TVShowTitle")
    genretype="VideoLibrary.Get%ss" %(genretypex)
    genrelisttype=genretypex.encode("utf8")
    #recuperation du premier genre
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
            json_result = getJSON(genretype , '{ "filter": {"genreid":%d}, "properties": [ "thumbnail"] }' %xyz2)
            break
      
      if json_result:     
        for Test in json_result:
          Titre = Test.get("label")
          if Titre and Titre not in json_result:            
            xyz = str(Test.get("movieid"))
            ItemListe = xbmcgui.ListItem(label=Titre,iconImage=Test.get("thumbnail"),label2=str(xyz2))
            if Titre != origtitle:
                 genrelist.append(["", ItemListe, False])

  xbmcplugin.addDirectoryItems(int(sys.argv[1]), genrelist) 
  xbmcplugin.endOfDirectory(int(sys.argv[1]))


        
def getCasting(Castingtypex=None,ItemId=None,Statique=None):
  allCast = []
  item = {}
  Casting = []
  Castingtype=""
  imageacteur="" 
  ListeActeur=[]
  
  
  
  
  NonVide=xbmc.getCondVisibility("Skin.HasSetting(HideMovieTvCastEmpty)")
  #videodb://movies/actors/1132/   1132=id acteur pour retrouver ses films
  
  if sys.argv[1]:
      if Castingtypex and ItemId:   
         #if Castingtypex=="episode":            Castingtypex="tvshow"
    
         Castingtype="VideoLibrary.Get%sDetails" %(Castingtypex)
         json_result = getJSON(Castingtype, '{ "%sid":%d,"properties": [ "cast"]}' %(Castingtypex,int(ItemId)))
         #movie, tvshow
         if json_result:
            allCast = json_result.get("cast")  
         if allCast:
           for Test in allCast:
             name=Test.get("name")
             
             if name:
                 imageacteur=Test.get("thumbnail")
                 if not imageacteur and not NonVide:
                    imageacteur="DefaultActor.png"
                 #else :
                 if imageacteur:
                     ItemListe = xbmcgui.ListItem(label=name,iconImage=imageacteur,label2=Test.get("role"))
                     
                     if not Statique:
                         ListeActeur.append(["",ItemListe,True])
                     else:
                         ListeActeur.append(ItemListe)
  if not Statique:
     xbmcplugin.addDirectoryItems(int(sys.argv[1]), ListeActeur)
     xbmcplugin.endOfDirectory(int(sys.argv[1]))
  else:
     return ListeActeur 
 

     
def getFilmsParActeur(ActeurType=None,Acteur=None,Statique=None):
  Donnees = []
  item = {}
  Casting = []
  RechercheType=""
  VideoPoster="" 
  ListeVideos=[]
  
  #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.GetMovies","params":{"filter":{"actor":"marion cotillard"},"properties":["thumbnail","year","file"]},"id":"1"}
  #videodb://movies/actors/1132/   1132=id acteur pour retrouver ses films
  if sys.argv[1]:
      if Acteur: 
         if ActeurType and ActeurType=="director":
            Ok=""
         else: ActeurType="actor"
         
         #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.GetMovies","params":{"filter":{"field":"director","operator":"contains","value":"ridley"},"properties":["thumbnail","year","file"]},"id":"1"}       
         json_result = getJSON2("VideoLibrary.GetMovies", '{"filter":{"field":"%s","operator":"contains","value":"%s"},"properties":["plot","thumbnail","year","file","art","imdbnumber","rating","userrating","cast"]}' %(ActeurType,Acteur))
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
                 ItemListe = xbmcgui.ListItem(label=Titre)
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
                 ItemListe.setInfo("video", {"dbid": str(IdVideo),"title": Titre,"year": Item.get("year"),"trailer":Item.get("trailer"),"plot":Item.get("plot")})
                 if not Statique:
                     ListeVideos.append([Item.get("file"),ItemListe,False])
                 else:
                     ListeVideos.append(ItemListe)
  if not Statique:               
     xbmcplugin.addDirectoryItems(int(sys.argv[1]), ListeVideos)       
     xbmcplugin.endOfDirectory(int(sys.argv[1])) 
  else:
     return ListeVideos
   
def GetActeurId(Acteur):
    
  ActeurId={}
  if Acteur!="None":  
        #allocine pour les frenchies ;)
        #ActeurId["allocine"]=''
        ActeurId["allocine"]=Allocine_ChercheActeur(unidecode(Acteur))
        
          #TMDB    
                 
        query_url = "https://api.themoviedb.org/3/search/person?api_key=67158e2af1624020e34fd893c881b019&language=%s&query=%s&page=1&include_adult=false" % (xbmc.getInfoLabel("System.Language").encode("utf8"),unicodedata.normalize('NFKD', Acteur.split("(")[0]).encode('ascii','xmlcharrefreplace'))
        json_data = requestUrlJson(query_url)              
        ActeurId["tmdb"]=None        
        if json_data:
            allInfo=json_data.get("results")            
            
            if allInfo:
              for item in allInfo:
                ActeurId["tmdb"]=str(item.get("id"))
                break
  return ActeurId 

def GetActeurInfo(NomActeur,ActeurType=None):
  ActeurCache={}
  ActeurId={}
  Bio=None
  json_data={}
  SaveActeur=0
  if ActeurType and ActeurType=="director":
            ActeurType='realisateurs'
  else: ActeurType="acteurs"
  #http://api.allocine.fr/rest/v3/search?partner=YW5kcm9pZC12M3M&filter=movie&count=5&page=1&q=alien&format=json
  if NomActeur:
    savepath=ADDON_DATA_PATH+"/%s/%s" %(ActeurType,str(unidecode(NomActeur)).replace(" ", "_"))
    if xbmcvfs.exists(savepath):
        with open(savepath) as data_file:
                  json_data = json.load(data_file)
                  data_file.close() 
                  if json_data:
                      ActeurCache["cast"]=json_data.get("cast") 
                      ActeurId=json_data.get("id")
                      Bio=json_data.has_key('biographie')
                      #Bio=json_data.get("biographie")
                      
                  
   
    
    if not Bio or not ActeurId : 
          if not ActeurId :            
            ActeurId=GetActeurId(NomActeur)
          if ActeurId:
            json_data=GetActeurInfoMaj(ActeurId,NomActeur)
          else:
            return ActeurCache  
          if json_data:
            #if (json_data.get("biographie") or json_data.get("naissance") or json_data.get("nom")) and SETTING("cacheacteur")=="false":
            if SETTING("cacheacteur")=="false":
               SaveActeur=1
  
         
           
    if json_data : 
              ActeurCache["biographie"]=json_data.get("biographie")
              ActeurCache["naissance"]=json_data.get("naissance")                  
              ActeurCache["deces"]=json_data.get("deces")                                                 
              ActeurCache["lieunaissance"]=json_data.get("lieunaissance")
              ActeurCache["nom"]=json_data.get("nom")
              ActeurCache["nomreel"]=json_data.get("nomreel")
              ActeurCache["id"]=ActeurId
              
              if SaveActeur>0:
                  
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
                        #ActeurId='allo'+str(AllocineId)
                     
            #break
    if ActeurId.get("tmdb"):
        if not json_data.get("biography"):
           
          #on recherche sur tmdb dans la langue de KODI
            query_url = "https://api.themoviedb.org/3/person/%s?api_key=67158e2af1624020e34fd893c881b019&language=%s" % (ActeurId.get("tmdb"),xbmc.getInfoLabel("System.Language").encode("utf8")) 
            json_datatmdb = requestUrlJson(query_url) 
            
        if not json_data or (not json_data.get("biography") and not json_datatmdb.get("biography")):   
              #pas de biographie dans la langue de KODI alors on cherche en Anglais......
              query_url = "https://api.themoviedb.org/3/person/%s?api_key=67158e2af1624020e34fd893c881b019&language=EN" % (ActeurId.get("tmdb")) 
              json_datatmdb = requestUrlJson(query_url)
          
       
    if json_data or json_datatmdb: 
          if json_data.get("biography"):
             ActeurCache["biographie"]=json_data.get("biography")
          else:
             ActeurCache["biographie"]=json_datatmdb.get("biography")
             
          if json_data.get("birthday"):
             ActeurCache["naissance"]=json_data.get("birthday")
          else:
             ActeurCache["naissance"]=json_datatmdb.get("birthday")
             
          if json_data.get("deathday"):
             ActeurCache["deces"]=json_data.get("deathday")
          else:
             ActeurCache["deces"]=json_datatmdb.get("deathday")
             
          if json_data.get("place_of_birth"):
             ActeurCache["lieunaissance"]=json_data.get("place_of_birth")
          else:
             ActeurCache["lieunaissance"]=json_datatmdb.get("place_of_birth")
             
          if json_data.get("name"):
             ActeurCache["nom"]=json_data.get("name")
          else:
             ActeurCache["nom"]=json_datatmdb.get("name")
             
          if json_data.get("realName"):
             ActeurCache["nomreel"]=json_data.get("realName")
          else:
             ActeurCache["nomreel"]=json_datatmdb.get("realName")
                 
          

                
  return ActeurCache  
  
  
  
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


def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
        
def Allocine_ChercheActeur(Acteur=None):
      ActeurId=None
      if Acteur:
        params = {}
        params['format'] = 'json'
        params['filter'] = 'person'
        params['partner'] = Allocinepartner_key
        try:
          params['q'] = str(Acteur) #unicodedata.normalize('NFKD', Acteur.split("(")[0]).encode('ascii','xmlcharrefreplace')
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
        
          
def getFilmsTv(ActeurType=None,Acteur=None,Statique=None):
  allInfo = []
  item = {}
  Casting = []
  Castingtype=""
  imageacteur="" 
  ListeRoles=[]
  ListeId=[]
  ActeurId={}
  ActeurCache={}
  ActeurSave=1
  if ActeurType and ActeurType=="director":
            ActeurType='realisateurs'
  else: ActeurType="acteurs"
  if ActeurType and Acteur!="None": 
    
     if Acteur:
        savepath=ADDON_DATA_PATH+"/%s/%s" %(ActeurType,str(unidecode(Acteur)).replace(" ", "_"))
        if xbmcvfs.exists(savepath):
          with open(savepath) as data_file:
                  json_data = json.load(data_file)
                  ActeurSave=0
                  data_file.close()
                  if not json_data.get("cast") :
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
            ActeurId=GetActeurId(Acteur,ActeurType)            
        
        #http://api.allocine.fr/rest/v3/filmography?partner=100043982026&code=12302&profile=large&filter=movie&striptags=synopsis%2Csynopsisshort&format=json&sed=20170507&sig=jfS3iVDun%2FywD91uBJ78p1lZlog%3D

        if ActeurId.get("tmdb") and (not xbmcvfs.exists(savepath) or ActeurSave>0):
            query_url = "https://api.themoviedb.org/3/person/%s/combined_credits?api_key=67158e2af1624020e34fd893c881b019&language=%s" % (ActeurId.get("tmdb"),xbmc.getInfoLabel("System.Language").encode("utf8")) 
            json_data = requestUrlJson(query_url)
         
        if json_data:                    
                  for item in json_data.get("cast"):
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
                            Role=item.get("character")
                            if not Role:
                               Role="?"
                            ItemListe = xbmcgui.ListItem(label=name,iconImage=Poster,label2=Role)
                            Annee=item.get("release_date")
                            if not Annee: 
                               Annee=item.get("first_air_date")
                            ItemListe.setProperty("dbtype",TypeVideo)
                            ItemListe.setInfo("video", {"title": name,"year": Annee,"originaltitle": item.get("original_title"),"trailer":item.get("id")})        
                            if not Statique:
                               ListeRoles.append(["",ItemListe,True])
                            else :
                               ListeRoles.append(ItemListe)
                            
                  if ActeurSave>0 and SETTING("cacheacteur")=="false":
                        erreur=DirStru(savepath)
                        ActeurCache["cast"]=json_data.get("cast")
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
      return(ListeRoles)
               
def getRealisateur(CheminType="",DbId=None,realisateur=None):
    allInfo = []
    realisateurId=""
    savepath=""     
    
    if DbId and realisateur: 
        savepath=ADDON_DATA_PATH+"/%ss/%s.jpg" %(CheminType,str(unidecode(realisateur)).replace(" ", "_"))
        if xbmcvfs.exists(savepath):
             return(savepath)
        else:
            
             savepath="DefaultActor.png"
             realisateur=try_decode(realisateur)
             query_url = "https://api.themoviedb.org/3/search/person?api_key=67158e2af1624020e34fd893c881b019&language=%s&query=%s&page=1&include_adult=false" % (xbmc.getInfoLabel("System.Language").encode("utf8"),unicodedata.normalize('NFKD', realisateur.split(" (")[0]).encode('ascii','xmlcharrefreplace'))
             json_data = requestUrlJson(query_url)
                     
             if json_data:
                 
                 allInfo=json_data.get("results")
                 if allInfo:
                    for item in json_data.get("results"):
                      Poster=item.get("profile_path")
                      if Poster: 
                         Poster="http://image.tmdb.org/t/p/original"+str(Poster)
                         if (CheminType=="realisateur" and SETTING("cacherealisateur")=="false") or (CheminType=="acteur" and SETTING("cacheacteur")=="false"):
                             query_url=Poster
                             try:                      
                               savepath=ADDON_DATA_PATH+"/%ss/%s.jpg" %(CheminType,str(unidecode(realisateur)).replace(" ", "_"))     
                               erreur=DirStru(savepath)
                               urllib.urlretrieve(query_url,savepath)
                               break 
                             except :
                               str_response=''
                               savepath="DefaultActor.png"
                               #logMsg("Resultat  URL introuvable 9--> " + str(query_url),0)
                         else:
                          savepath=Poster
             return(savepath)            
                           
                   
def getTrailer(ID=None,DbType=None):
     Donnees=[]
     ListeTrailer=[]
     #https://api.themoviedb.org/3/movie/$$IDFILM$$/videos?api_key=67158e2af1624020e34fd893c881b019&language=French      
     #https://api.themoviedb.org/3/tv/$$IDTV$$/videos?api_key=67158e2af1624020e34fd893c881b019&language=French  
     if DbType and ID: 
          if DbType!="movie":
               query_url ="https://api.themoviedb.org/3/tv/%s/videos?api_key=67158e2af1624020e34fd893c881b019&language=%s" % (ID,xbmc.getInfoLabel("System.Language").encode("utf8"))
          else:
               query_url ="https://api.themoviedb.org/3/movie/%s/videos?api_key=67158e2af1624020e34fd893c881b019&language=%s" % (ID,xbmc.getInfoLabel("System.Language").encode("utf8"))
          json_data = requestUrlJson(query_url)
          if json_data:
            Donnees=json_data.get("results")               
          if DbType!="movie":
               query_url ="https://api.themoviedb.org/3/tv/%s/videos?api_key=67158e2af1624020e34fd893c881b019&language=en" % (ID)
          else:
               query_url ="https://api.themoviedb.org/3/movie/%s/videos?api_key=67158e2af1624020e34fd893c881b019&language=en" % (ID)
          json_data = requestUrlJson(query_url)
          if json_data:
            Donnees=Donnees+json_data.get("results")          
          
          if Donnees:
               cc=0
               for Item in Donnees:
                    Item["sizenull"]=""
                    if Item.get("site")=="YouTube":
                         Item["position"]=str(cc)                         
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
          query_url = "https://api.themoviedb.org/3/movie/%s?api_key=67158e2af1624020e34fd893c881b019" % (xxx)
      if TypeID=="episode":
         query_url = "https://api.themoviedb.org/3/tv/%s?api_key=67158e2af1624020e34fd893c881b019" % (xxx)
    
      json_data = requestUrlJson(query_url)
      
    
      if json_data:
        RuntimeDB = json_data['runtime']        
                  
    return str(RuntimeDB)
    
    
def get_externalID(ItemId=None,ismovie=None):
   externalXX=""
   ItemIdR=""
   allID=[]
   query_url=""
   if ItemId.find('tt')==-1: #pas IMDB
     externalXX="tvdb_id"
   else:
     externalXX="imdb_id"
   query_url = "https://api.themoviedb.org/3/find/%s?api_key=67158e2af1624020e34fd893c881b019&language=%s&external_source=%s" % (ItemId,xbmc.getInfoLabel("System.Language").encode("utf8"),externalXX)
   
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
#https://api.themoviedb.org/3/find/268592?api_key=67158e2af1624020e34fd893c881b019&language=en-US&external_source=tvdb_id
#https://api.themoviedb.org/3/find/268592?api_key=67158e2af1624020e34fd893c881b019&language=en-US&external_source=imdb_id
#https://api.themoviedb.org/3/find/268592?api_key=67158e2af1624020e34fd893c881b019&language=en-US&external_source=tvrage_id
#https://api.themoviedb.org/3/find/268592?api_key=67158e2af1624020e34fd893c881b019&language=en-US&external_source=freebase_id

#get episodes
#https://api.themoviedb.org/3/tv/48866/season/1?api_key=67158e2af1624020e34fd893c881b019&language=en-US
#48866 id chez themoviedb
#1 : numero de saison

def VueActuelle(containerprefix=""):
    contenu= ""
    if xbmc.getCondVisibility("Container.Content(episodes)"):
        contenu= "episodes"
    elif xbmc.getCondVisibility("Container.Content(movies) + !substring(Container.FolderPath,setid=)"):
        contenu= "movies"
    elif xbmc.getCondVisibility("[Container.Content(sets) | StringCompare(Container.Folderpath,videodb://movies/sets/)] + !substring(Container.FolderPath,setid=)"):
        contenu= "sets"
    elif xbmc.getCondVisibility("substring(Container.FolderPath,setid=)"):
        contenu= "setmovies"
    elif xbmc.getCondVisibility("!IsEmpty(Container.Content) + !StringCompare(Container.Content,pvr)"):
        contenu= xbmc.getInfoLabel("Container.Content")
    elif xbmc.getCondVisibility("Container.Content(tvshows)"):
        contenu= "tvshows"
    elif xbmc.getCondVisibility("Container.Content(seasons)"):
        contenu= "seasons"
    elif xbmc.getCondVisibility("Container.Content(musicvideos)"):
        contenu= "musicvideos"
    elif xbmc.getCondVisibility("Container.Content(songs) | StringCompare(Container.FolderPath,musicdb://singles/)"):
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
                    if KODI_VERSION>=17: 
                         Elements = xbmcgui.ListItem(label=label, iconImage=image,label2="selectionnevue")
                         Elements.setProperty("viewid", viewid)
                         Elements.setProperty("icon", image)
                         if VueActuelle==try_decode(label):
                              ListeVues.insert(0,Elements) 
                         else :
                              ListeVues.append(Elements)
                    else: 
                         if VueActuelle==try_decode(label):
                              ListeVues.insert(0,label)
                         else:
                              ListeVues.append(label)
                    if VueActuelle==try_decode(label):
                         choixpossibles.insert(0,str(viewid))
                    else:
                         choixpossibles.append(str(viewid))
        dialogC = xbmcgui.Dialog()
        if ListeVues:
            result=dialogC.select(xbmc.getLocalizedString(629), ListeVues)
            if result>=0:
                 vue = str(choixpossibles[result])
                 xbmc.executebuiltin("Container.SetViewMode(%s)" % vue)            
                  	  
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
def requestUrlJson(query_url):
  #logMsg("requestUrlJson :"+str(query_url),0)
  try:
    req = urllib2.Request(query_url.replace(" ","%20")) 
  except :
    str_response=None
    logMsg("Erreur  urllib2.Request(query_url) --> " + str(query_url),0)
  if req:
    user_agent = 'Dalvik/1.6.0 (Linux; U; Android 4.2.2; Nexus 4 Build/JDQ39E)'
    req.add_header('User-agent',user_agent)
             
  try:
    reponse = urllib2.urlopen(req, timeout = 1)
    #reponse = urllib.request.urlopen(query_url, None, 2)
  except:
    reponse=None
    logMsg("Erreur  urllib2.urlopen(query_url) --> " + str(query_url),0)
  
  json_data=None
  if reponse:
        try:
          str_response = reponse.read().decode('utf8')
        except :
          str_response=None
          logMsg("Erreur  requestUrlJson introuvable  --> " + str(query_url),0)

        if str_response :
          try:
           json_data = json.loads(str_response)
          except:
           json_data=None
           logMsg("Erreur  requestUrlJson  vide --> " + str(query_url),0)
               
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
# ----------- ----- MUSIQUE ------ -----------------


    
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
        DataItem=data.get("album")
        if not DataItem:
          if 'The ' in Album:
             Album=Album.replace('The ','')
             urlTVDB="http://www.theaudiodb.com/api/v1/json/195011/searchalbum.php?s=%s&a=%s" %(Artiste,Album)
          xbmc.sleep(100)
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
#https://api.themoviedb.org/3/search/multi?api_key=67158e2af1624020e34fd893c881b019&language=en-US&query=alfred%20hitchcock&page=1&include_adult=false     
  
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
  
    
    """  
def getallepisodesTMDB(ItemIdx=None,KodiId=None,savepath=None,NbKodi=None,ShowBusy=None):
  #https://api.betaseries.com/shows/display?key=46be59b5b866&thetvdb_id=266398
  
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
  
  if ItemIdx or KodiId:
     if ShowBusy: xbmc.executebuiltin( "ActivateWindow(busydialog)" ) 
     getallepisodesBeta("",KodiId,savepath,NbKodi,1)
     if not ItemIdx and KodiId: 
        ItemId=get_externalID(KodiId,"tv") # conversion imdb ou tvdb en themoviedb ....
     else :
        if ItemIdx: ItemId=ItemIdx
          
     #ItemId = id chez themoviedb du tvshow
     if ItemId :
         ArrayCollection["name"]=xbmc.getInfoLabel("ListItem.TVShowTitle")
         ArrayCollection["tmdbid"]=ItemId
         ArrayCollection["kodiid"]=KodiId
         ArrayCollection["nbkodi"]=NbKodi
         ArrayCollection["dateecheance"]=nowX.strftime('%Y-%m-%d')
         ArrayCollection["v5"]="ok"
         TotalSaisons={}
          
       
         query_url = "https://api.themoviedb.org/3/tv/%s?api_key=67158e2af1624020e34fd893c881b019&language=%s" % (ItemId,xbmc.getInfoLabel("System.Language").encode("utf8"))
          
         
         json_data = requestUrlJson(query_url)
         try:
           str_response = response.read().decode('utf8')
         except :
           str_response=''
           #logMsg("Resultat  URL introuvable 5--> " + str(query_url),0)

         if str_response :
          try:
            json_data = json.loads(str_response)
          except:
            json_data=""
            logMsg("Resultat  URL vide 5--> " + str(query_url),0)
         else:
         	json_data=""
          
         if json_data:
             SaisonTab=json_data.get("seasons")
             if SaisonTab:
             	  for item in SaisonTab:             	  	       
                         EpisodesEtcasting={} 
                         EpisodesEtcasting["NbEpisodes"]=item["episode_count"]
                         TotalSaisons[str(item["season_number"])]=EpisodesEtcasting 
                              
         
         ArrayCollection["saisons"]=TotalSaisons 
         ArtWorks=gettvartworks(KodiId)
         ArrayCollection["artworks"]=ArtWorks
                
          #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.SetTvShowDetails","params":{"setid":38,"art":{"poster":"http://image.tmdb.org/t/p/original/zrApSsUX9i0qVntcCD0Pp55TdCy.jpg"}},"id":1}
         if KODI_VERSION>=17 and ArtWorks and  SETTING("updatetvposter")=="true":                              
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
              MAJ=MAJ+'"landscape":"%s",' %(ArtWorks.get("thumb"))
            

            if len(MAJ)>3:
              MJTV=MAJ[0:len(MAJ)-1] #suppression de la virgule de fin
              logMsg("MAJ=%s MJSAGA=%s" %(MAJ,MJSAGA),0 )
              
              try:
               json_result = getJSON('VideoLibrary.SetTvShowDetails', '{ "tvshowid":%d,"art":{%s} }' %(int(ItemIdxx),MJTV))
              except:
                logMsg("VideoLibrary.SetTvShowDetails: %d impossible" %(int(ItemIdxx)),0 )
                                
         if SETTING("cacheserie")=="false":  
           erreur=DirStru(savepath)
           with io.open(savepath, 'w+', encoding='utf8') as outfile: 
  	                      str_ = json.dumps(ArrayCollection,indent=4, sort_keys=True,separators=(',', ':'), ensure_ascii=False)
  	                      outfile.write(to_unicode(str_))
     if ShowBusy: xbmc.executebuiltin( "Dialog.Close(busydialog)" )                 
  return ArrayCollection 
"""