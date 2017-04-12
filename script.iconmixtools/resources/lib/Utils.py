#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import xbmcplugin, xbmcgui, xbmc, xbmcaddon, xbmcvfs
import os,sys,io
import urllib
import httplib
import datetime
import _strptime
import time
import unicodedata
import urlparse
from xml.dom.minidom import parse
import json
import sqlite3
import operator
    
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id').decode("utf8")
ADDON_ICON = ADDON.getAddonInfo('icon').decode("utf8")
ADDON_NAME = ADDON.getAddonInfo('name').decode("utf8")
ADDON_PATH = ADDON.getAddonInfo('path').decode("utf8")
ADDON_VERSION = ADDON.getAddonInfo('version').decode("utf8")
ADDON_DATA_PATH = xbmc.translatePath("special://profile/addon_data/%s" % ADDON_ID).decode("utf8")
KODI_VERSION  = int(xbmc.getInfoLabel( "System.BuildVersion" ).split(".")[0])
WINDOW = xbmcgui.Window(10000)
SETTING = ADDON.getSetting
KODILANGUAGE = xbmc.getLanguage(xbmc.ISO_639_1)
sys.path.append(xbmc.translatePath(os.path.join(ADDON_PATH, 'resources', 'lib')).decode('utf8'))
if KODI_VERSION>16: 
        DATABASE_PATH = os.path.join(xbmc.translatePath("special://database"), 'MyVideos107.db')
else: 
        DATABASE_PATH = os.path.join(xbmc.translatePath("special://database"), 'MyVideos99.db')



def logMsg(msg, level = 1):
    if WINDOW.getProperty("IconMixTools.enableDebugLog") == "true" or level == 0:
        if isinstance(msg, unicode):
            msg = msg.encode('utf8')
        if "exception" in msg.lower() or "error" in msg.lower():
            xbmc.log("IconMixTools addon --> " + msg, level=xbmc.LOGERROR)
            print_exc()
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

    
def CheckSaga(itemId=None,Statique=None):
    TitreSaga=""
    ArrayCollection={}
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
    if not itemId or (DBTYPE!="movie" and xbmc.getCondVisibility("Window.IsVisible(12003)") and not DBTYPE=="set"):
       xbmcplugin.endOfDirectory(handle=int(sys.argv[1]))
       return
    
    if itemId:
     
       try:
          dd=int(itemId)
       except:          
          json_result = getJSON('VideoLibrary.GetMovieDetails', '{ "movieid":%d,"properties":["setid"] }' %(int(xbmc.getInfoLabel("ListItem.DBID"))))
          itemId=json_result.get("setid")
          if not itemId:              
                   return      
          
      
       if not Statique:
          xbmcplugin.setContent(int(sys.argv[1]), 'movies')
          
       savepath=ADDON_DATA_PATH+"/collections/saga"+itemId.encode('utf8')
       
       json_result = getJSON('VideoLibrary.GetMovieSetDetails', '{ "setid":%d,"movies": {"properties":["title","genre","year","rating","director","trailer","tagline","plot","plotoutline","originaltitle","lastplayed","playcount","writer","studio","mpaa","cast","country","imdbnumber","runtime","set","showlink","streamdetails","top250","votes","fanart","thumbnail","file","sorttitle","resume","setid","dateadded","tag","art"]} }' %(int(itemId)))
 
       for item in json_result.get("movies"): 
          ImdbItem.append(item.get("imdbnumber"))
       Compteur = {}.fromkeys(set(ImdbItem),0)
       for valeur in ImdbItem:
          Compteur[valeur] += 1
  
    
       for item in json_result.get("movies"):
          txx = xbmcgui.ListItem(label=item["label"],path=item["file"])
          
          item["DBID"]=item.get("movieid")
          ImdbNumber=item.get("imdbnumber")          
          
          #pistes audios
          Audio=item["streamdetails"]["audio"]
          i=1
          if Audio:               
               for AudioElement in Audio:
                    txx.setProperty('AudioLanguage.%d' %(i), AudioElement["language"])
                    txx.setProperty('AudioChannels.%d' %(i), str(AudioElement["channels"]))
                    txx.setProperty('AudioCodec.%d' %(i), AudioElement["codec"])                    
                    i=i+1
    
          #pistes vidéos 
          Video=item["streamdetails"]["video"]
          i=0
          Codec=""
          if Video:
            for VideoItem in Video:
               txx.setProperty('VideoCodec', VideoItem["codec"]) 
               
          #sous-titres     
          Subtitles=item["streamdetails"]["subtitle"]
          i=1
          
          if Subtitles:
               for SubtitleElement in Subtitles:
                    txx.setProperty('SubtitleLanguage.%d' %(i), SubtitleElement["language"])                     
                    i=i+1
                   
            
          txx.setProperty('DBID', str(item["DBID"]))
          txx.setProperty('SetId', itemId.encode('utf8'))
          txx.setProperty('IMDBNumber', str(item.get("imdbnumber")))
          txx.setProperty('TMDBNumber', '')
          txx.setProperty('DateSortie', '')
          txx.setProperty('doublons',str(Compteur[item.get("imdbnumber")]))
         
          if item.get("art"):
                txx.setArt( item.get("art"))
          txx.setIconImage(item["thumbnail"]) 
          txx.setInfo("video", {"dbid": str(item["movieid"]),"duration": item["runtime"], "title": item["title"],"mediatype": "movie","genre": item["genre"],"year": item["year"],"plot": item["plot"],"plotoutline": item["plotoutline"],"originaltitle": item["originaltitle"]}) 
          NbKodi=NbKodi+1
          if int(Compteur[item.get("imdbnumber")])>0:
             NbKodiValide=NbKodiValide+1
             if not Statique:
               ListeItem.append([item["file"],txx,True])
             else:
               ListeItem.append([int(item["year"]),txx])
             
          if int(Compteur[item.get("imdbnumber")])>1:
              Compteur[item.get("imdbnumber")]=0
              
       if not xbmcvfs.exists(savepath):
        #création du fichier de la saga !!!
         ArrayCollection=getsagaitem(itemId)
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
          
          
       
          if NbFilmsSaga and NbKodi and NbTmdb:
              if NbFilmsSaga!=NbKodi: # or NbKodi<NbTmdb: #mise a jour !!! 
                 ArrayCollection=getsagaitem(itemId.encode('utf8'),None,ArrayCollection.get("kodicollection"),ArrayCollection.get("tmdbid"))
                 NbFilmsSaga=ArrayCollection.get("kodi")
                 NbManquant=ArrayCollection.get("manquant")
                 TitreSaga=ArrayCollection.get("saga")
                 NbTmdb=ArrayCollection.get("tmdb")
    
       if NbKodiValide>0: WINDOW.setProperty('IconMixSaga',str(NbKodiValide))
       else: WINDOW.clearProperty('IconMixSaga')
       if ArrayCollection:    
         for item in ArrayCollection["missing"]:
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
              txx = xbmcgui.ListItem(label=item.get("title"),iconImage="http://image.tmdb.org/t/p/original"+item.get("poster_path"),path="RunScript(script.iconmixtools,trailer=True)") 
              fanart=item.get("backdrop_path")
              if fanart:
                  txx.setArt({"fanart":"http://image.tmdb.org/t/p/original"+fanart})
              txx.setInfo("video", {"title": item.get("title"),"mediatype": "movie","year": item.get("release_date"),"plot": item.get("overview"),"originaltitle": item.get("originaltitle")})        
              txx.setProperty('IMDBNumber', '')
              txx.setProperty('TMDBNumber', str(item.get("id")))
              txx.setProperty('DateSortie', DateSortie)
              txx.setProperty('dbtype', 'movie')
              txx.setProperty('SetId', itemId.encode('utf8'))
              if not Statique:
                 ListeItem.append([item["file"],txx,True])
              else:
                 ListeItem.append([int(item.get("release_date")[0:4]),txx])

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
               
          return ListeItemFinal
    
   
    
def getsagaitem(ItemIdxx=None,ShowBusy=None,AKodiCollection=None,ATmdbId=None):
  episodesDB= ""
  AllMovies= []
  Rspcollection= {}
  ManquantM=[]
  KodiCollection = []
  ArrayCollection={}
  IDcollection=""
  Element = ""
  NbFilmsSaga=0
  itemId=""
  ItemIdx=""
  imdbNumber= ""
  today =""
  release = ""
  flagcheck=0
  DateSortie=""
  query_url=""
  
  savepath=ADDON_DATA_PATH+"/collections/saga"+ItemIdxx.encode("utf8") 
  
  if ItemIdxx : 
      if not ShowBusy: xbmc.executebuiltin( "ActivateWindow(busydialog)" ) 
      json_result = getJSON('VideoLibrary.GetMovieSetDetails', '{ "setid":%d,"movies": {"properties": [ "title","imdbnumber" ]} }' %(int(ItemIdxx)))
      if json_result and json_result.get("movies"): 
        allMovies = json_result.get("movies")

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
                  itemId=tmdbid 
                  flagcheck=1 
                KodiCollection.append([imdbNumber,str(tmdbid)])
        
       
      if itemId:
                if not ATmdbId:
                   #numero de collection TMDB inconnu
                   query_url = "https://api.themoviedb.org/3/movie/%s?api_key=67158e2af1624020e34fd893c881b019&language=%s" % (itemId.encode("utf8"),xbmc.getInfoLabel("System.Language").encode("utf8"))
                   #logMsg("Query URL   --> " + str(query_url),0)
                   response = urllib.urlopen(query_url)
                   try:
                      str_response = response.read().decode('utf8')
                   except :
                      str_response=''
                      logMsg("Resultat  URL introuvable 1" + str(query_url),0)

                   if str_response :
                        try : 
                             json_data = json.loads(str_response)
                        except:
                             json_data=""
                             logMsg("Resultat  URL vide 1--> " + str(query_url),0)
                   if json_data:
                      Rspcollection=json_data.get("belongs_to_collection")
                      if Rspcollection: IDcollection=Rspcollection["id"]
                else: 
                   IDcollection=ATmdbId
                   
                if IDcollection:
                     query_url = "https://api.themoviedb.org/3/collection/%d?api_key=67158e2af1624020e34fd893c881b019&language=%s" % (IDcollection,xbmc.getInfoLabel("System.Language").encode("utf8"))
                     response = urllib.urlopen(query_url)
                     try:
                       str_response = response.read().decode('utf8')
                     except :
                       str_response=''
                       logMsg("Resultat  URL introuvable 2--> " + str(query_url),0)

                     if str_response :
                       try : 
                              json_data = json.loads(str_response)
                       except:
                              json_data=""
                              logMsg("Resultat  URL vide 2--> " + str(query_url),0)

                       if json_data:
                         Rspcollection=json_data.get("parts")

                         if Rspcollection:

                            NbFilmsSaga=0
                            Manquant=0
                            for check in Rspcollection:
                              if check["id"]:
                                xxx=str(check["id"])
                                zz=None
                                cpt=0
                                for yy in KodiCollection:
                                  if yy[1]==xxx:
                                    zz=1
                                    break
                                  else:
                                    cpt=cpt+1
                                
                                
                                if not zz :
                                   if check["title"] and check["release_date"] and check["poster_path"]:
                                         ManquantM.append(check)
                                         NbFilmsSaga=NbFilmsSaga+1
                                                                 
                                else: NbFilmsSaga=NbFilmsSaga+1
                            if NbFilmsSaga>0: 
                                 ArrayCollection["kodi"]=len(KodiCollection)
                                 ArrayCollection["kodicollection"]=KodiCollection
                                 ArrayCollection["saga"]=json_data.get("name")
                                 ArrayCollection["tmdb"]=len(Rspcollection)
                                 ArrayCollection["tmdbid"]=IDcollection
                                 ArrayCollection["manquant"]=len(ManquantM)
                                 ArrayCollection["missing"]=ManquantM
                                 erreur=DirStru(savepath)
                                 with io.open(savepath, 'w+', encoding='utf8') as outfile:
                                     str_ = json.dumps(ArrayCollection,indent=4, sort_keys=True,separators=(',', ':'), ensure_ascii=False)
                                     outfile.write(to_unicode(str_))
                            else :
                                 ArrayCollection["kodi"]=len(KodiCollection)
                                 ArrayCollection["kodicollection"]=KodiCollection
                                 ArrayCollection["tmdbid"]=IDcollection
                                 ArrayCollection["saga"]=xbmc.getInfoLabel("ListItem.Label")
                                 ArrayCollection["tmdb"]=len(Rspcollection)
                                 ArrayCollection["manquant"]=0
                                 ArrayCollection["missing"]=[]
                                 erreur=DirStru(savepath)
                                 with io.open(savepath, 'w+', encoding='utf8') as outfile:
                                     str_ = json.dumps(ArrayCollection,indent=4, sort_keys=True,separators=(',', ':'), ensure_ascii=False)
                                     outfile.write(to_unicode(str_))
                              
                                   
      if not ShowBusy: xbmc.executebuiltin( "Dialog.Close(busydialog)" )                           
            
 
  return ArrayCollection
  

def UpdateSagas(Une=None,Toutes=None):
     ItemId=0
     AllMovies= {}
     NbItems=0
     savepath=""
     Titre=""
     
     dp = xbmcgui.DialogProgress()
     dp.create("IconMixTools",Titre,"")
     if not Une :
       json_result = getJSON('VideoLibrary.GetMovieSets', '{}')
     #logMsg("VideoLibrary.SAGAS  --> "+str(json_result),0)
       if json_result: 
          NbItems=len(json_result)
          Compteur=0
          for Sagas in json_result:
            ItemId=Sagas.get("setid")
            savepath=ADDON_DATA_PATH+"/collections/saga%d" %(ItemId)
            
            #if Toutes or not os.path.exists(savepath) and ItemId: getsagaitem(itemId.encode('utf8'),1)
            if Toutes or not xbmcvfs.exists(savepath) and ItemId: 
               getsagaitem(itemId.encode('utf8'),1)   
               Titre=xbmc.getLocalizedString( 31924 )+" : [I]"+Sagas.get("label")+"[/I]"
            Progres=(Compteur*100)/NbItems
            Compteur=Compteur+1
            if Toutes: dp.update(Progres,Titre,"(%d/%d)" %(Compteur,NbItems))
            else : dp.update(Progres,Titre,"...")
            if dp.iscanceled(): break
     else :
          getsagaitem(str(Une),1)        
            
     dp.close()  
     
# --------------------------------------------------------------------------------------------------
    


# --------------------------------------------SERIES-------------------------------------------
def getepisodes(ItemIdxx=None,saisonID=None,DBtype=None):
  episodesDB= ""
  AllSeasons= []
  AllEpisodes=[]
  ArrayCollection={}
  NbEpisodes=0
  NbKodi=0
  itemId=""
  ItemIdx=""
  nowX = datetime.datetime.now().date()
  nowX2=nowX
  txx=0
  tsea=0
  
  
  if ItemIdxx and DBtype:
    if DBtype=="season":
     xxx=xbmc.getInfoLabel("Container.FolderPath")
     xx=xxx.split("titles/")[1]
     ItemIdxx=xx.split("/")[0]
     if ItemIdxx:
      json_result = getJSON('VideoLibrary.GetTVShowDetails', '{ "tvshowid":%d,"properties": [ "title", "imdbnumber","episode" ]}' %(int(ItemIdxx)))
      #logMsg("VideoLibrary.GetTVShowDetails  --> "+"{"+str(ItemIdxx)+"}" + str(json_result),0)
      if json_result: 
          ItemIdx=json_result.get("imdbnumber")
          NbKodi=json_result.get("episode")
          
      else : ItemIdx="" 
  	#oblige d'aller chercher l'IMDB de la serie mere dans la fiche tvshow !!! pouviez pas ajouter un champ dans la base ???? grrrrrrrrr !!!!!!
  	#quel bordel mon colonel !
  	#http://127.0.0.1:8080/jsonrpc?request={ "jsonrpc ": "2.0 ", "method ": "VideoLibrary.GetEpisodeDetails ", "params ":{ "episodeid ":220, "properties ":[ "title ", "tvshowid "]}, "id ":1}
    if DBtype=="episode":
      json_result = getJSON('VideoLibrary.GetEpisodeDetails', '{ "episodeid":%d,"properties": [ "title", "tvshowid" ]}' %(int(ItemIdxx)))
      #logMsg("VideoLibrary.GetEpisodeDetails  --> "+"{"+str(ItemIdxx)+"}" + str(json_result),0)
      if json_result and json_result.get("tvshowid"):
         ItemIdx=json_result.get("tvshowid")
         #logMsg("ItemIdx  --> " + str(ItemIdx),0)
         #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.GetTVShowDetails","params":{"ItemIdx":40,"properties":["title","imdbnumber"]},"id":1}
         json_result = getJSON('VideoLibrary.GetTVShowDetails', '{ "tvshowid":%d,"properties": [ "title", "imdbnumber","episode" ]}' %(int(ItemIdx)))
         #logMsg("VideoLibrary.GetTVShowDetails  --> "+"{"+str(ItemIdx)+"}" + str(json_result),0)
         if json_result and json_result.get("imdbnumber"):
            ItemIdx=json_result.get("imdbnumber")
            NbKodi=json_result.get("episode")
            
            #logMsg("ItemIdxImDb  --> " + str(ItemIdx),0)
         else : ItemIdx=""
    else : 
      if DBtype=="tvshow": 
        ItemIdx=xbmc.getInfoLabel("ListItem.IMDBNumber")
        NbKodi=int(xbmc.getInfoLabel("ListItem.Property(TotalEpisodes)"))
     
    if ItemIdx:
      savepath=ADDON_DATA_PATH+"/series/tv"+ItemIdx.encode("utf8")
      #if not os.path.exists(savepath):
      if not xbmcvfs.exists(savepath):
     #creation
         ArrayCollection=getallepisodes("",ItemIdx,savepath,NbKodi,1)
         
      else : 
    #if os.path.exists(savepath):      
         with open(savepath) as data_file:
            ArrayCollection = json.load(data_file)
            data_file.close()
         if not ArrayCollection or not ArrayCollection.get("v4"): # si fichier foireux ?
          #mise a jour
            ArrayCollection=getallepisodes("",ItemIdx,savepath,NbKodi,1)
  
      if ArrayCollection:
            if ArrayCollection["dateecheance"]:
               try:
                  nowX2 = datetime.datetime.strptime(str(ArrayCollection["dateecheance"]), '%Y-%m-%d').date()
               except:
                  nowX2=nowX
            
               
            if ArrayCollection["kodiid"]!=ItemIdx or ArrayCollection["nbkodi"]!=NbKodi or nowX>nowX2 or not ArrayCollection.get("v4"):
                  #mise a jour
                  ArrayCollection=getallepisodes(ArrayCollection.get("tmdbid"),ItemIdx,savepath,NbKodi)
                  
            if ArrayCollection:
                     try:
                        NbEpisodes=int(ArrayCollection["saisons"][str(saisonID)]["NbEpisodes"])
                     except:
                        NbEpisodes=0           
  
  return NbEpisodes
  
def UpdateSeries(Une=None,Toutes=None):
     ItemId=0
     AllMovies= {}
     NbItems=0
     savepath=""
     Titre=""
     
     dp = xbmcgui.DialogProgress()
     dp.create("IconMixTools",Titre,"")
     if not Une :
       json_result = getJSON('VideoLibrary.GetTvShows', '{"properties":["imdbnumber","episode"]}')
       #logMsg("VideoLibrary.TV  --> "+str(json_result),0)
       if json_result: 
          NbItems=len(json_result)
          Compteur=0
          for Series in json_result:
            ItemId=Series.get("tvshowid")
            ImdbNumber=Series.get("imdbnumber")
            NbKodi=Series.get("episode")
            savepath=ADDON_DATA_PATH+"/series/tv%s" %(ImdbNumber)
            
            #if Toutes or not os.path.exists(savepath) and ItemId: getsagaitem(itemId.encode('utf8'),1)
            if Toutes or not xbmcvfs.exists(savepath) and ItemId:                
               getallepisodes("",ImdbNumber,savepath,NbKodi,"")   
               Titre=xbmc.getLocalizedString( 20343 )+" : [I]"+Series.get("label")+"[/I]"
            Progres=(Compteur*100)/NbItems
            Compteur=Compteur+1
            if Toutes: dp.update(Progres,Titre,"(%d/%d)" %(Compteur,NbItems))
            else : dp.update(Progres,Titre,"...")
            if dp.iscanceled(): break
     else :
          NbKodi=int(xbmc.getInfoLabel("ListItem.Property(TotalEpisodes)"))
          savepath=ADDON_DATA_PATH+"/series/tv%s" %(Une)
          getallepisodes("",Une,savepath,NbKodi,1)        
            
     dp.close()     
     

  
def getallepisodesTMDB(ItemIdx=None,KodiId=None,savepath=None,NbKodi=None,ShowBusy=None):
  #https://api.betaseries.com/shows/display?key=46be59b5b866&thetvdb_id=266398
  
  KodiCollection = []
  ArrayCollection={} 
  EpisodesDiffusion={}
  EpisodesSaison =[]
  EpisodesEtcasting={}
  SaisonTab={}
  Episodes=[]
  itemId=""
  query_url=""
  nowX = datetime.datetime.now().date()+datetime.timedelta(30) #pour mise a jour une fois par mois
  
  if ItemIdx or KodiId:
     if ShowBusy: xbmc.executebuiltin( "ActivateWindow(busydialog)" ) 
     #logMsg("Appel betaseries--> " + str(KodiId),0) 
     getallepisodesBeta("",KodiId,savepath,NbKodi,1)
     if not ItemIdx and KodiId: 
        itemId=get_externalID(KodiId.encode("utf8"),"tv") # conversion imdb ou tvdb en themoviedb ....
     else :
        if ItemIdx: itemId=ItemIdx
          
     #itemid = id chez themoviedb du tvshow
     if itemId :
         ArrayCollection["name"]=xbmc.getInfoLabel("ListItem.TVShowTitle")
         ArrayCollection["tmbid"]=itemId
         ArrayCollection["kodiid"]=KodiId
         ArrayCollection["nbkodi"]=NbKodi
         ArrayCollection["dateecheance"]=nowX.strftime('%Y-%m-%d')
         ArrayCollection["v4"]="ok"
         TotalSaisons={}
          
       
         query_url = "https://api.themoviedb.org/3/tv/%s?api_key=67158e2af1624020e34fd893c881b019&language=%s" % (itemId.encode("utf8"),xbmc.getInfoLabel("System.Language").encode("utf8"))
          
         
         response = urllib.urlopen(query_url)
         try:
           str_response = response.read().decode('utf8')
         except :
           str_response=''
           logMsg("Resultat  URL introuvable 5--> " + str(query_url),0)

         if str_response :
          try:
            json_data = json.loads(str_response)
          except:
            json_data=""
            logMsg("Resultat  URL vide 5--> " + str(query_url),0)
         else:
         	json_data=""
          
         #logMsg("Resultat sortie NBep --> " + str(json_data),0)
         if json_data:
             #logMsg("Resultat sortie Saison --> "+"["+str(cpt)+"]",0)
             SaisonTab=json_data.get("seasons")
             if SaisonTab:
             	  for item in SaisonTab:             	  	       
                         EpisodesEtcasting={} 
                         EpisodesEtcasting["NbEpisodes"]=item["episode_count"]
                         TotalSaisons[str(item["season_number"])]=EpisodesEtcasting 
                              
         ArrayCollection["saisons"]=TotalSaisons         
         erreur=DirStru(savepath)
	   #if not erreur:
         with io.open(savepath, 'w+', encoding='utf8') as outfile: 
	                      str_ = json.dumps(ArrayCollection,indent=4, sort_keys=True,separators=(',', ':'), ensure_ascii=False)
	                      outfile.write(to_unicode(str_))
     if ShowBusy: xbmc.executebuiltin( "Dialog.Close(busydialog)" )                 
  return ArrayCollection 
  
def getallepisodes(ItemIdx=None,KodiId=None,savepath=None,NbKodi=None,ShowBusy=None):
  
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
  itemId=""
  query_url=""
  nowX = datetime.datetime.now().date()+datetime.timedelta(30) #pour mise a jour une fois par mois
  #logMsg("Resultat  URL betaseries--> " + str(ItemIdx),0) 
  if ItemIdx or KodiId:
     
     #itemid = id chez themoviedb du tvshow
     if KodiId :
         itemId=KodiId
         ArrayCollection["name"]=xbmc.getInfoLabel("ListItem.TVShowTitle")
         ArrayCollection["tmbid"]=""
         ArrayCollection["kodiid"]=KodiId
         ArrayCollection["nbkodi"]=NbKodi
         ArrayCollection["dateecheance"]=nowX.strftime('%Y-%m-%d')
         ArrayCollection["v4"]="ok"
         TotalSaisons={}
          
       
         query_url = "https://api.betaseries.com/shows/display?key=46be59b5b866&thetvdb_id=%s" % (itemId.encode("utf8")) 
         #logMsg("Resultat  URL betaseries--> " + str(query_url),0)         
         
         response = urllib.urlopen(query_url)
         try:
           str_response = response.read().decode('utf8')
         except :
           str_response=''
           logMsg("Resultat  URL introuvable 5--> " + str(query_url),0)

         if str_response :
          try:
            json_data = json.loads(str_response)
          except:
            json_data=""
            logMsg("Resultat  URL vide 5--> " + str(query_url),0)
         else:
         	json_data=""
          
         if json_data:
             SaisonTab=json_data.get("show")
             ArrayCollection["imdbid"]=SaisonTab.get("imdb_id")
             ArrayCollection["sa_id"]=SaisonTab.get("id")
             SaisonTab=SaisonTab.get("seasons_details")
             if SaisonTab:
             	  for item in SaisonTab:             	  	       
                         EpisodesEtcasting={} 
                         EpisodesEtcasting["NbEpisodes"]=item["episodes"]
                         TotalSaisons[str(item["number"])]=EpisodesEtcasting 
                              
         ArrayCollection["saisons"]=TotalSaisons 
                 
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
      
def getDiffusionTV(ItemIdxx=None,saisonID=None,DBtype=None):
  episodesDB= ""
  AllSeasons= []
  ArrayCollection={}
  ListeEpisodes=[]
  NbEpisodes=0
  NbKodi=0
  itemId=""
  ItemIdx=""
  nowX = datetime.datetime.now().date()
  nowX2=nowX
  txx=0
  tsea=0
  
  #logMsg("GetAirDates : "+ str(ItemIdxx)+"/"+str(saisonID)+"/"+str(DBtype),0)
  if ItemIdxx and DBtype and saisonID:
    
    if DBtype=="episode":
      json_result = getJSON('VideoLibrary.GetEpisodeDetails', '{ "episodeid":%d,"properties": [ "title", "tvshowid" ]}' %(int(ItemIdxx)))
      if json_result and json_result.get("tvshowid"):
         ItemIdx=json_result.get("tvshowid")
         json_result = getJSON('VideoLibrary.GetTVShowDetails', '{ "tvshowid":%d,"properties": [ "title", "imdbnumber","episode" ]}' %(int(ItemIdx)))
         if json_result and json_result.get("imdbnumber"):
            ItemIdx=json_result.get("imdbnumber")
            NbKodi=json_result.get("episode")
         else : ItemIdx=""
     
     
    if ItemIdx: #imdbnumber
      logMsg("Resultat  ItemIdx --> " + str(ItemIdx),0)
      savepath=ADDON_DATA_PATH+"/series/tv"+ItemIdx.encode("utf8")
      #if not os.path.exists(savepath):
      if not xbmcvfs.exists(savepath):
          #creation !!!
          ArrayCollection=getallepisodes("",ItemIdx,savepath,NbKodi,1)
      else :
    #if os.path.exists(savepath):
          with open(savepath) as data_file:
            ArrayCollection = json.load(data_file)
            data_file.close()
          if not ArrayCollection: # si fichier foireux ?
            ArrayCollection=getallepisodes("",ItemIdx,savepath,NbKodi,1)
          
  
      if ArrayCollection:
        if ArrayCollection["dateecheance"]:
          try:
             nowX2 = datetime.datetime.strptime(str(ArrayCollection["dateecheance"]), '%Y-%m-%d').date()
          except:
             nowX2=nowX  
          
        if ArrayCollection["kodiid"]!=ItemIdx or ArrayCollection["nbkodi"]!=NbKodi or nowX>nowX2:
             #mise à jour
             ArrayCollection=getallepisodes(ArrayCollection.get("tmbid"),ItemIdx,savepath,NbKodi)
             
        if ArrayCollection:
                AllSeasons=ArrayCollection["saisons"]
                #logMsg("Resultat  AllSeasons --> " + str(AllSeasons),0)
                if AllSeasons :
                   logMsg("AllSeasons",0) 
                   AllEpisodes=AllSeasons[str(saisonID)]
                   if AllEpisodes:
                      logMsg("AllEpisodes",0) 
                      for item in AllEpisodes:
                         Nom=item["name"]
                         DateDiffusion=item["air_date"]
                         Poster=item["poster"]
                         if not Poster: Poster="DefaultTVShows.png"
                         else: Poster="http://image.tmdb.org/t/p/original"+str(Poster)
                         if Nom and DateDiffusion:
                              txx=xbmcgui.ListItem(label=Nom,iconImage=Poster,label2=DateDiffusion)
                              ListeEpisodes.append(["", txx, False])
                              logMsg("Resultat  Ajout TvDiffusion --> "+Nom+"/"+DateDiffusion+"/"+Poster,0)                  
   
    xbmcplugin.addDirectoryItems(int(sys.argv[1]), ListeEpisodes)
  xbmcplugin.endOfDirectory(int(sys.argv[1]))
# --------------------------------------------UTILITAIRES/PLUGIN----------------------------------------------
def getItemPath(typex=None,itemId=None):
  allCast = []
  item = {}
  Casting = []
  Ptype=""
  PathList = []
  extrafanart_dir=""
  
  
  if typex and itemId:   
         if typex=="episode":
            typex="tvshow"
    
         Ptype="VideoLibrary.Get%sDetails" %(typex)
        
   
         json_result = getJSON(Ptype, '{ "%sid":%d,"properties": [ "file" ]}' %(typex,int(itemId)))
         #movie, tvshow
         if json_result:
               PathList.append({'path': media_path(json_result.get('file',''))})
               #for item in PathList:
               for currentmedia in PathList:
                  for item in currentmedia['path']:
                      artwork_dir = os.path.join(item + '/')
                      extrafanart_dir = os.path.join(artwork_dir + 'extrafanart' + '/')                      
                  #if not os.path.exists(extrafanart_dir):
                  succes=xbmcvfs.exists(extrafanart_dir)
                  if not succes:
                      extrafanart_dir=""
                     
                  
  return extrafanart_dir      
 
def media_path(path):
    try:
        path = os.path.split(path)[0].rsplit(' , ', 1)[1].replace(",,",",")
    except:
        path = os.path.split(path)[0]
    path = [path]
    return path  

    
def getGenre(genrex=None,genretypex=None,origtitle=None):
  itemId = None
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
          ooo = Test.get("label")
          if ooo and ooo not in json_result:            
            xyz = str(Test.get("movieid"))
            txx = xbmcgui.ListItem(label=ooo,iconImage=Test.get("thumbnail"),label2=str(xyz2))
            if ooo != origtitle:
                 genrelist.append(["", txx, False])

  xbmcplugin.addDirectoryItems(int(sys.argv[1]), genrelist) 
  xbmcplugin.endOfDirectory(int(sys.argv[1]))
  
def getCasting(Castingtypex=None,itemId=None,Statique=None):
  allCast = []
  item = {}
  Casting = []
  Castingtype=""
  imageacteur="" 
  ListeActeur=[]
  NonVide=xbmc.getCondVisibility("Skin.HasSetting(HideMovieTvCastEmpty)")
  
  #videodb://movies/actors/1132/   1132=id acteur pour retrouver ses films
  
  if sys.argv[1]:
      if itemId:     
         allCast = sql_ActeurParVideo(itemId,Castingtypex)  
         if allCast:
           for Test in allCast:
             name=Test.get("name")
             if name:
                 imageacteur=Test.get("thumbnail")
                 if not imageacteur and not NonVide:
                    imageacteur="DefaultActor.png"
                 #else :
                 if imageacteur:
                    txx = xbmcgui.ListItem(label=name,iconImage=imageacteur,label2=Test.get("role"))
                    txx.setProperty('DBID', str(Test.get("actor_id")) )  
                 
                    if not Statique:
                         ListeActeur.append(["",txx,True])
                    else:
                         ListeActeur.append(txx)
  if not Statique:
     xbmcplugin.addDirectoryItems(int(sys.argv[1]), ListeActeur)
     xbmcplugin.endOfDirectory(int(sys.argv[1]))
  else:
     return ListeActeur 

def getCastingOK(Castingtypex=None,itemId=None,Statique=None):
  allCast = []
  item = {}
  Casting = []
  Castingtype=""
  imageacteur="" 
  ListeActeur=[]
  NonVide=xbmc.getCondVisibility("Skin.HasSetting(HideMovieTvCastEmpty)")
  #videodb://movies/actors/1132/   1132=id acteur pour retrouver ses films
  
  if sys.argv[1]:
      if Castingtypex and itemId:   
         #if Castingtypex=="episode":            Castingtypex="tvshow"
    
         Castingtype="VideoLibrary.Get%sDetails" %(Castingtypex)
         json_result = getJSON(Castingtype, '{ "%sid":%d,"properties": [ "cast" ]}' %(Castingtypex,int(itemId)))
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
                    txx = xbmcgui.ListItem(label=name,iconImage=imageacteur,label2=Test.get("role"))
                 
                    if not Statique:
                         ListeActeur.append(["",txx,True])
                    else:
                         ListeActeur.append(txx)
  if not Statique:
     xbmcplugin.addDirectoryItems(int(sys.argv[1]), ListeActeur)
     xbmcplugin.endOfDirectory(int(sys.argv[1]))
  else:
     return ListeActeur 
  
def getFilmsParActeur(ActeurType=None,ActeurId=None,Statique=None):
  Donnees = []
  item = {}
  Casting = []
  RechercheType=""
  VideoPoster="" 
  ListeVideos=[]
  
  #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.GetMovies","params":{"filter":{"actor":"marion cotillard"},"properties":["thumbnail","year","file"]},"id":"1"}
  #videodb://movies/actors/1132/   1132=id acteur pour retrouver ses films
  
  if sys.argv[1]:
      if ActeurId: 
         
         Donnees=sql_VideosParActeur(str(ActeurId),ActeurType)                  
         if Donnees:
           for Item in Donnees:
             Titre=Item.get("label")
             if Titre:
                 txx = xbmcgui.ListItem(label=Titre)
                 txx.setLabel2(Item.get("role"))
                 
                 IdVideo=Item.get("movieid")
                 TypeVideo="movie"
                 if not IdVideo: 
                    IVideo=Item.get("tvshowid")
                    TypeVideo="tvshow"
                 IdVideo=str(Item.get("imdbnumber"))                 
                 txx.setArt( Item.get("art")) 
                 logMsg('backend ART =' +str(Item.get("art")),0)
                 txx.setProperty("TypeVideo",TypeVideo)
                 txx.setInfo("video", {"Mpaa": Item.get("imdbnumber"),"title": Titre,"year": Item.get("year"),"trailer":Item.get("trailer")})
                 if not Statique:
                     ListeVideos.append([Item.get("file"),txx,False])
                 else:
                     ListeVideos.append(txx)
  if not Statique:               
     xbmcplugin.addDirectoryItems(int(sys.argv[1]), ListeVideos)       
     xbmcplugin.endOfDirectory(int(sys.argv[1])) 
  else:
     return ListeVideos
   
     
def getFilmsParActeurOK(ActeurType=None,Acteur=None,Statique=None):
  Donnees = []
  item = {}
  Casting = []
  RechercheType=""
  VideoPoster="" 
  ListeVideos=[]
  
  #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.GetMovies","params":{"filter":{"actor":"marion cotillard"},"properties":["thumbnail","year","file"]},"id":"1"}
  #videodb://movies/actors/1132/   1132=id acteur pour retrouver ses films
  
  if sys.argv[1]:
      if ActeurType and Acteur: 
         
         json_result = getJSON("VideoLibrary.GetMovies", '{"filter":{"actor":"%s"},"properties":["thumbnail","year","file","art","imdbnumber","cast"]}' %(Acteur) )
         #logMsg("Resultat  Filmographie local Tv--> " +str(json_result),0) 
         json_result2 = getJSON("VideoLibrary.GetTvShows", '{"filter":{"actor":"%s"},"properties":["thumbnail","year","file","imdbnumber","art","cast"]}' %(Acteur.encode('utf-8')))
         #logMsg("Resultat  Filmographie local Tv--> "+str(Acteur)+"/" +str(json_result2),0) 
          
         if len(json_result)>0:
          Donnees=json_result
         if len(json_result2)>0:
          Donnees=Donnees+json_result2        
         #logMsg("Resultat  Filmographie local --> " + str(Acteur)+"/"+str(ActeurType)+"/"+str(json_result),0) 
         #movie, tvshow
                  
         if Donnees:
           for Item in Donnees:
             Titre=Item.get("label")
             if Titre:
                 txx = xbmcgui.ListItem(label=Titre)
                 Casting = Item.get("cast")
                 if Casting:
                    for ItemCast in  Casting:
                         if ItemCast.get("name")==Acteur:
                              txx.setLabel2(ItemCast.get("role"))
                              break               
                 
                 #logMsg("Resultat  Filmographie local --> "+str(Titre)+"/" + str(VideoPoster),0)  
                 IdVideo=Item.get("movieid")
                 TypeVideo="movie"
                 if not IdVideo: 
                    IVideo=Item.get("tvshowid")
                    TypeVideo="tvshow"
                 IdVideo=str(Item.get("imdbnumber"))                 
                 txx.setArt( Item.get("art")) 
                 logMsg('backend ART =' +str(Item.get("art")),0)
                 txx.setInfo("video", {"Mpaa": Item.get("imdbnumber"),"title": Titre,"year": Item.get("year"),"writer":TypeVideo,"trailer":Item.get("trailer")})
                 if not Statique:
                     ListeVideos.append([Item.get("file"),txx,False])
                 else:
                     ListeVideos.append(txx)
  if not Statique:               
     xbmcplugin.addDirectoryItems(int(sys.argv[1]), ListeVideos)       
     xbmcplugin.endOfDirectory(int(sys.argv[1])) 
  else:
     return ListeVideos
   
  
  
def getFilmsTv(DbType=None,Acteur=None,Statique=None):
    allInfo = []
    item = {}
    Casting = []
    Castingtype=""
    imageacteur="" 
    ListeRoles=[]
    ListeId=[]
    ActeurId=""
    ActeurCache={}
    ActeurSave=1
    #logMsg("Resultat  Filmographie --> " + str(Acteur)+"/"+str(DbType),0)  
    if DbType and Acteur!="None": 
        Acteur=try_decode(Acteur)       
        query_url = "https://api.themoviedb.org/3/search/person?api_key=67158e2af1624020e34fd893c881b019&language=%s&query=%s&page=1&include_adult=false" % (xbmc.getInfoLabel("System.Language").encode("utf8"),unicodedata.normalize('NFKD', Acteur.split("(")[0]).encode('ascii','xmlcharrefreplace'))
        response = urllib.urlopen(query_url)
        #logMsg("URL --> " + str(query_url),0)
        try:
            str_response = response.read().decode('utf8')
        except :
            str_response=''
            logMsg("Resultat  URL introuvable 6",0)

        if str_response :
            try:
                json_data = json.loads(str_response)
            except:
                json_data=""
                logMsg("Resultat  URL vide 6--> " + str(query_url),0)
       
                
        if json_data:
            #logMsg("Resultat  Acteur --> " + str(json_data),0)
            allInfo=json_data.get("results")
            ActeurId=""
            if allInfo:
                #logMsg("Resultat  Results --> " + str(Acteur),0)
                         item=allInfo[0]  #on prend le premier de la liste en esperant que ce soit le bon !                          
                         ActeurId=item.get("id")
                         #logMsg("Resultat  Acteur ID -->" + str(ActeurId),0)
                         if ActeurId:
                                 savepath=ADDON_DATA_PATH+"/acteurs/acteurTMDB"+str(ActeurId)
                                 if not xbmcvfs.exists(savepath):
                                        #logMsg("Chercher acteur --> " + str(ActeurId),0)
                                        query_url = "https://api.themoviedb.org/3/person/%s/combined_credits?api_key=67158e2af1624020e34fd893c881b019&language=%s" % (ActeurId,xbmc.getInfoLabel("System.Language").encode("utf8")) 
                                        response = urllib.urlopen(query_url)
                                        #logMsg("URL --> " + str(query_url),0)
                                        try:
                                          str_response = response.read().decode('utf8')
                                        except :
                                          str_response=''
                                          logMsg("Resultat  URL introuvable 7 --> " + str(query_url),0)

                                        if str_response :
                                          #logMsg("Chercher acteur OK--> " + str(ActeurId),0)
                                          try:
                                              json_data = json.loads(str_response)
                                          except:
                                              json_data=""
                                              logMsg("Resultat  URL vide 7--> " + str(query_url),0)
                                              
                                        #if json_data:
                                             #logMsg("Recuperer acteur OK--> " + str(ActeurId)+"/"+str(json_data),0)
                                 else : 
                                        with open(savepath) as data_file:
                                          json_data = json.load(data_file)
                                          ActeurSave=0
                                          data_file.close()
                                         
                                 if json_data:
                                         #logMsg("Resultat  Roles --> " + str(json_data.get("cast")),0)
                                         for item in json_data.get("cast"):
                                             typemedia=str(item.get("media_type"))
                                             name=""
                                             #logMsg("Resultat  Mediatype --> "+"/"+str(item.get("id"))+"/" + str(typemedia)+"/"+str(DbType),0)
                                             #if typemedia=="movie" and DbType=="movie": name=item.get("title")
                                             #else: 
                                             #     if typemedia=="tv" and DbType!="movie": name=item.get("name")
                                             if typemedia=="movie": name=item.get("title")
                                             else : name=item.get("name")
                                             if name:
                                               #logMsg("Resultat  Mediatype --> "+"/"+str(name)+"/" + str(typemedia)+"/"+str(DbType),0)
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
                                                       if typemedia=="movie": Poster="RolesFilms.png"
                                                       else: Poster="RolesSeries.png"
                                                    else: Poster="http://image.tmdb.org/t/p/original"+str(Poster)
                                                    Role=item.get("character")
                                                    if not Role:
                                                       Role="?"
                                                    txx = xbmcgui.ListItem(label=name,iconImage=Poster,label2=Role)
                                                    Annee=item.get("release_date")
                                                    if not Annee: 
                                                       Annee=item.get("first_air_date")
                                                    txx.setInfo("video", {"title": name,"year": Annee,"originaltitle": item.get("original_title"),"writer":typemedia,"trailer":item.get("id")})        
                                                    #else : txx.setInfo("video", {"title": item.get("name"),"year": item.get("first_air_date"),"originaltitle": item.get("original_name")})        
                                                    #logMsg("Resultat  Role --> " + str(name)+"/"+str(Poster)+"/"+str(item.get("character")),0)
                                                    if not Statique:
                                                       ListeRoles.append(["",txx,True])
                                                    else :
                                                       ListeRoles.append(txx)
                                                    
                                 #logMsg("Resultat  Roles Global--> " + str(ListeRoles),0)
                                         if ActeurSave>0:
                                              erreur=DirStru(savepath)
                                              #logMsg("Sauvegarder acteur --> " + str(ActeurId),0)
     	                                    #if not erreur:
                                              ActeurCache["cast"]=json_data.get("cast")
                                              ActeurCache["nom"]=unicodedata.normalize('NFKD', Acteur.split("(")[0]).encode('ascii','xmlcharrefreplace')
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
        #logMsg("DBID et Real --> " + str(DbId)+"/"+str(realisateur),0)     
        savepath=ADDON_DATA_PATH+"/"+CheminType+"s/"+CheminType+str(DbId)+".jpg"
        if xbmcvfs.exists(savepath):
             #logMsg("retour existant --> " + str(savepath),0)
             return(savepath)
        else:
            
             savepath="DefaultActor.png"
             realisateur=try_decode(realisateur)
             query_url = "https://api.themoviedb.org/3/search/person?api_key=67158e2af1624020e34fd893c881b019&language=%s&query=%s&page=1&include_adult=false" % (xbmc.getInfoLabel("System.Language").encode("utf8"),unicodedata.normalize('NFKD', realisateur.split("(")[0]).encode('ascii','xmlcharrefreplace'))
             response = urllib.urlopen(query_url)
             #logMsg("URL --> " + str(query_url),0)
             try:
                 str_response = response.read().decode('utf8')
             except :
                 str_response=''
                 logMsg("Resultat  URL introuvable 8 ",0)

             if str_response :
                 try:
                     json_data = json.loads(str_response)
                 except:
                     json_data=""
                     logMsg("Resultat  URL vide 8--> " + str(query_url),0)
            
                     
             if json_data:
                 
                 allInfo=json_data.get("results")
                 if allInfo:
                    for item in json_data.get("results"):
                      #logMsg("Resultat  realisateur --> " + str(item),0)
                      Poster=item.get("profile_path")
                      if Poster: 
                         Poster="http://image.tmdb.org/t/p/original"+str(Poster)
                         query_url=Poster
                         try:                           
                           savepath=ADDON_DATA_PATH+"/"+CheminType+"s/"+CheminType+str(DbId)+".jpg"
                           erreur=DirStru(savepath)
                           #logMsg("URL --> " + str(query_url),0)
                           urllib.urlretrieve(query_url,savepath)
                           break 
                         except :
                           str_response=''
                           savepath="DefaultActor.png"
                           logMsg("Resultat  URL introuvable 9--> " + str(query_url),0)
             return(savepath)            
                           
                   
def getTrailer(ID=None,DbType=None):
     Donnees=[]
     ListeTrailer=[]
     #https://api.themoviedb.org/3/movie/$$IDFILM$$/videos?api_key=67158e2af1624020e34fd893c881b019&language=French      
     #https://api.themoviedb.org/3/tv/$$IDTV$$/videos?api_key=67158e2af1624020e34fd893c881b019&language=French  
     if DbType and ID: 
          #xbmc.executebuiltin( "ActivateWindow(busydialog)" ) 
          if DbType!="movie":
               query_url ="https://api.themoviedb.org/3/tv/%s/videos?api_key=67158e2af1624020e34fd893c881b019&language=%s" % (ID.encode("utf8"),xbmc.getInfoLabel("System.Language").encode("utf8"))
          else:
               query_url ="https://api.themoviedb.org/3/movie/%s/videos?api_key=67158e2af1624020e34fd893c881b019&language=%s" % (ID.encode("utf8"),xbmc.getInfoLabel("System.Language").encode("utf8"))
          #logMsg("Resultat  URL --> " + str(query_url),0)
          response = urllib.urlopen(query_url)
          try:
               str_response = response.read().decode('utf8')
          except :
               str_response=''
               logMsg("Resultat  URL introuvable 10--> " + str(query_url),0)
          if str_response :
               try : 
                json_data = json.loads(str_response)
                Donnees=json_data.get("results")
               except:
                json_data=""
                logMsg("Resultat  URL vide 10--> " + str(query_url),0)
          if DbType!="movie":
               query_url ="https://api.themoviedb.org/3/tv/%s/videos?api_key=67158e2af1624020e34fd893c881b019&language=en" % (ID.encode("utf8"))
          else:
               query_url ="https://api.themoviedb.org/3/movie/%s/videos?api_key=67158e2af1624020e34fd893c881b019&language=en" % (ID.encode("utf8"))
          #logMsg("Resultat  URL --> " + str(query_url),0)
          response = urllib.urlopen(query_url)
          try:
               str_response = response.read().decode('utf8')
          except :
               str_response=''
               logMsg("Resultat  URL introuvable 11--> " + str(query_url),0)
          if str_response :
               try : 
                json_data = json.loads(str_response)
                Donnees=Donnees+json_data.get("results")
               except:
                json_data=""
                logMsg("Resultat  URL vide 11--> " + str(query_url),0)
          
          if Donnees:
               #logMsg("Resultat  URL vide --> " + str(Donnees),0)
               cc=0
               for Item in Donnees:
                    if Item.get("site")=="YouTube":
                         Item["position"]=str(cc)                         
                         ListeTrailer.append(Item)
                         cc=cc+1
                         #logMsg("Resultat Trailer " + str(ID)+":"+Item.get("name")+"-"+Item.get("key")+"-"+str(Item.get("size"))+"-"+str(Item.get("type"))+"-"+str(Item.get("site")),0)
          #xbmc.executebuiltin( "Dialog.Close(busydialog)" )
     return ListeTrailer
                    
  

def getRuntime(itemId=None,TypeID=None):
    RuntimeDB= ""
    query_url=""
    xxx=""
    if itemId:  xxx=get_externalID(itemId,TypeID)
    if xxx:
      if TypeID=="movie":
          query_url = "https://api.themoviedb.org/3/movie/%s?api_key=67158e2af1624020e34fd893c881b019" % (xxx.encode("utf8"))
      if TypeID=="episode":
         query_url = "https://api.themoviedb.org/3/tv/%s?api_key=67158e2af1624020e34fd893c881b019" % (xxx.encode("utf8"))
    
      logMsg("Runtime ->"+str(query_url),0)
      response = urllib.urlopen(query_url)
      try:
       str_response = response.read().decode('utf8')
      except :
       str_response=''
       logMsg("Resultat  URL introuvable 12--> " + str(query_url),0)
      if str_response :
          try : 
               json_data = json.loads(str_response)
          except:
               json_data=""
               logMsg("Resultat  URL vide 12--> " + str(query_url),0)
    
    # dump response data in a readable format
      if json_data:
        #logMsg("Resultat sortie --> " + str(json_data),0)
        RuntimeDB = json_data['runtime']        
        #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.GetMovieDetails","params":{"movieid":266,"properties": [ "title","runtime","imdbnumber"]},"id":1}
                  
    return str(RuntimeDB)
    
    
def get_externalID(itemId=None,ismovie=None):
   externalXX=""
   itemIDR=""
   allID=[]
   query_url=""
   if itemId.find('tt')==-1: #pas IMDB
     externalXX="tvdb_id"
   else:
     externalXX="imdb_id"
   query_url = "https://api.themoviedb.org/3/find/%s?api_key=67158e2af1624020e34fd893c881b019&language=%s&external_source=%s" % (itemId.encode("utf8"),xbmc.getInfoLabel("System.Language").encode("utf8"),externalXX)
   #logMsg("Resultat  URL --> " + str(query_url),0)
   response = urllib.urlopen(query_url)
   try:
        str_response = response.read().decode('utf8')
   except :
        str_response=''
        logMsg("Resultat  URL introuvable 13",0)
   if str_response :
      try : 
               json_data = json.loads(str_response)
      except:
               json_data=""
               logMsg("Resultat  URL vide 13",0)
      
      if json_data:
         if ismovie!="movie": 
          allID=json_data.get("tv_results")
         else:
          allID=json_data.get("movie_results")
         if allID and len(allID)>0:
             #logMsg("Resultat sortie externalALLID --> ["+str(len(allID))+"] - " + str(allID),0)
             for Test in allID:
               #if Test.get("id"):
               	  itemIDR=Test.get("id")
               	  break
               	  #logMsg("Resultat sortie externalALLID --> " + str(itemIDR),0)
                           
   return str(itemIDR)
   

		
#get external id pour themoviedb
# si ttXXXXX -> Imdb
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
                    if KODI_VERSION>16: 
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


    
def getJSON(method,params):
    #logMsg("Resultat executeJSONRPC --> " + str(method),0)
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
        #logMsg("getJson - invalid result for Method %s - params: %s - response: %s" %(method,params, str(jsonobject)))
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
 

def sql_ActeurParVideo(itemId=None,TypeVideo=""):     
     ListeActeurs=[] 
     ListeItemFinal=[] 
        
     con = sqlite3.connect(str(DATABASE_PATH))
     cursor = con.cursor()
     #cursor.execute("SELECT media_type FROM uniqueid WHERE media_id='%d';" %(int(itemId)))
     #for data_out in cursor.fetchall():
     #   TypeVideo=str(data_out[0])
     #   break
        
     if TypeVideo=='episode':
        #alors on recupere l'idShow !
        cursor.execute("SELECT idShow FROM episode WHERE idEpisode='%d';" %(int(itemId)))
        TypeVideo="tvshow"
        
        for data_out in cursor.fetchall():
            itemId=str(data_out[0])
           
     
     cursor.execute("SELECT * FROM actor_link WHERE media_id='%d' and media_type='%s';" %(int(itemId),TypeVideo))
     for data_out in cursor.fetchall():
        Details={}
        Details['actor_id']=data_out[0]
        Details['media_id']=data_out[1]
        Details['media_type']=data_out[2]
        Details['role']=data_out[3]
        Details['order']=data_out[4]
        logMsg("Acteurs du media %s:%s" %(str(Details['media_id']),str(Details['media_type'])),0)
        cursor2=con.cursor()
        cursor2.execute("SELECT * FROM actor WHERE actor_id='%d';" %(int(data_out[0])))
        for data2 in cursor2.fetchall():
          Details['name']=data2[1]
          Thumbnail=data2[2].replace("<thumb>","")
          Details['thumbnail']=Thumbnail.replace("</thumb>","")
          
        
        ListeActeurs.append([Details['order'],Details])
     
     #logMsg('backend Sql Acteurs %s=' %(itemId.encode('utf8'))+str(ListeActeurs),0)
     LL=[]          
     LL=sorted(ListeActeurs)
     cpt=0
     #trier par ordre de roles
     while cpt<len(LL):
           ListeItemFinal.append(LL[cpt][1])
           cpt=cpt+1
     con.close()
     return ListeItemFinal
      
      
def sql_VideosParActeur(IdActeur=None,DbType=None):     
     Donnees=[]
     logMsg(str(xbmc.translatePath("special://database")),0)
     con = sqlite3.connect(str(DATABASE_PATH))
     cursor = con.cursor()
     #recuperation de tous les medias de cet acteur/realisateur
     if DbType!="director":
      cursor.execute("SELECT actor_id,media_id,media_type,role FROM actor_link WHERE actor_id='%d';" %(int(IdActeur)))
     else:
      cursor.execute("SELECT actor_id,media_id,media_type FROM director_link WHERE actor_id='%d';" %(int(IdActeur)))
     for data_out in cursor.fetchall():
        Details={}
        Details['actor_id']=data_out[0]
        Details['media_id']=str(data_out[1])
        Details['media_type']=data_out[2]
        if DbType!="director":
           Details['role']=data_out[3]
        else:
           Details['role']=""
        json_result = getJSON("VideoLibrary.Get%sDetails" %(str(Details['media_type'])), '{"%sid":%d,"properties":["thumbnail","year","file","art","imdbnumber","cast"]}' %(str(Details['media_type']),int(Details['media_id'])) )
       
        if len(json_result)>0:
          json_result['role']=Details['role']
          Donnees.append(json_result)     
     con.close()
     return Donnees
      