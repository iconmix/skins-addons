# -*- coding: utf8 -*-

# Copyright (C) 2015 - Philipp Temminghoff <phil65@kodi.tv>
# This program is Free Software see LICENSE file for details

import xbmcaddon
import xbmcvfs
import urllib
import codecs
import os
import operator

import time
import hashlib
import urllib2
import xbmc
import simplejson
import resources.lib.Utils as utils
from resources.lib.Utils import logMsg
import xbmcplugin, xbmcgui, xbmc, xbmcaddon, xbmcvfs

ADDON = xbmcaddon.Addon()
SETTING = ADDON.getSetting
ADDON_PATH = os.path.join(os.path.dirname(__file__), "..")
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_DATA_PATH = xbmc.translatePath("special://profile/addon_data/%s" % ADDON_ID).decode("utf-8")
HEADERS = {'User-agent': 'Mozilla/5.0'}
WINDOW = xbmcgui.Window(10000)
cache_path = xbmc.translatePath(os.path.join(ADDON_DATA_PATH, "AutoCompleteKodi/"))

def GetAutoCompleteProvider():
   return xbmc.getInfoLabel("Skin.String(AutoCompleteProvider)")

def get_autocomplete_items(search_str, limit=50, providerchoice=None,basetype=None,PurgeCache=None):
    """
    get dict list with autocomplete
    """
    if xbmc.getCondVisibility("System.HasHiddenInput") or providerchoice=="off":
        return []
    if providerchoice:
      if providerchoice == "youtube":
          provider = GoogleProvider(youtube=True, limit=limit)
      elif providerchoice == "google":
          provider = GoogleProvider(limit=limit)
      elif providerchoice == "bing":
          provider = BingProvider(limit=limit)
      #elif providerchoice == "historique":
      #    provider = LocalDictProvider(limit=limit)
      elif providerchoice == "kodi":
          if basetype:
             provider = BaseTypeDictProvider(limit=limit,basetype=basetype,Purge=PurgeCache)
          else:
             provider = GoogleProvider(limit=limit)
      
    else: 
      AutoCompleteProvider= GetAutoCompleteProvider()
      if AutoCompleteProvider == "off":
        return []
      if AutoCompleteProvider == "youtube":
          provider = GoogleProvider(youtube=True, limit=limit)
      elif AutoCompleteProvider == "google":
          provider = GoogleProvider(limit=limit)
      elif AutoCompleteProvider == "bing":
          provider = BingProvider(limit=limit)
      #elif AutoCompleteProvider == "historique":
      #    provider = LocalDictProvider(limit=limit)
      else:
          #Kodi
          if basetype:
             provider = BaseTypeDictProvider(limit=limit,basetype=basetype,Purge=PurgeCache)
          else:
             provider = GoogleProvider(limit=limit)
    provider.limit = limit
    return provider.get_predictions(search_str)


class BaseProvider(object):

    def __init__(self, *args, **kwargs):
        self.limit = kwargs.get("limit", 50)

    def get_predictions(self, search_str):
        pass

    def prep_search_str(self, text):
        if type(text) != unicode:
            text = text.decode('utf-8')
        for chr in text:
            if ord(chr) >= 1488 and ord(chr) <= 1514:
                return text[::-1]
        return text

    def get_prediction_listitems(self, search_str):
        for item in self.get_predictions(search_str):
            li = {"label": item,
                  "search_string": search_str}
            yield li


class GoogleProvider(BaseProvider):

    def __init__(self, *args, **kwargs):
        super(GoogleProvider, self).__init__(*args, **kwargs)
        self.youtube = kwargs.get("youtube", False)

    def get_predictions(self, search_str):
        """
        get dict list with autocomplete labels from google
        """
        if not search_str:
            return []
        items = []
        result = self.fetch_data(search_str)
        for i, item in enumerate(result):
            li = {"label": item,
                  "search_string": self.prep_search_str(item)}
            items.append(li)
            if i > self.limit:
                break
        return items

    def fetch_data(self, search_str):
        base_url = "http://clients1.google.com/complete/"
        url = "search?hl=%s&q=%s&json=t&client=serp" % (SETTING("autocomplete_lang"), urllib.quote_plus(search_str))
        if self.youtube:
            url += "&ds=yt"
        result = get_JSON_response(url=base_url + url,
                                   headers=HEADERS,
                                   folder="Google")
        if not result or len(result) <= 1:
            return []
        else:
            return result[1]


class BingProvider(BaseProvider):

    def __init__(self, *args, **kwargs):
        super(BingProvider, self).__init__(*args, **kwargs)

    def get_predictions(self, search_str):
        """
        get dict list with autocomplete labels from bing
        """
        if not search_str:
            return []
        items = []
        result = self.fetch_data(search_str)
        for i, item in enumerate(result):
            li = {"label": item,
                  "search_string": self.prep_search_str(item)}
            items.append(li)
            if i > self.limit:
                break
        return items

    def fetch_data(self, search_str):
        base_url = "http://api.bing.com/osjson.aspx?"
        url = "query=%s" % (urllib.quote_plus(search_str))
        result = get_JSON_response(url=base_url + url,
                                   headers=HEADERS,
                                   folder="Bing")
        if not result:
            return []
        else:
            return result[1]


class LocalDictProvider(BaseProvider):

    def __init__(self, *args, **kwargs):
        super(LocalDictProvider, self).__init__(*args, **kwargs)

    def get_predictions(self, search_str):
        """
        get dict list with autocomplete labels from locally saved lists
        """
        listitems = []
        k = search_str.rfind(" ")
        if k >= 0:
            search_str = search_str[k + 1:]
        path = os.path.join(ADDON_PATH, "resources", "data", "common_%s.txt" % SETTING("autocomplete_lang_local"))
        with codecs.open(path, encoding="utf8") as f:
            for i, line in enumerate(f.readlines()):
                if not line.startswith(search_str) or len(line) <= 2:
                    continue
                li = {"label": line,
                      "search_string": line}
                listitems.append(li)
                if len(listitems) > self.limit:
                    break
        return listitems
        
class BaseTypeDictProvider(BaseProvider):

    def __init__(self, *args, **kwargs):
        self.basetype = kwargs.get("basetype", None)
        self.listitems = []
        self.Data={}
        self.PurgeCache = kwargs.get("Purge", None)
        super(BaseTypeDictProvider, self).__init__(*args, **kwargs)
        
    def check_update(self,KodiTotal=None,dbtype=None):
      if KodiTotal and dbtype:
        self.Data["total"]=KodiTotal
        #logMsg("%s = %d : %d" %(dbtype,int(self.Data.get("total")),int(self.GlobalCache[dbtype])))
        try:
          if int(self.Data.get("total"))!=int(self.GlobalCache[dbtype]):
            return True
          else:
            return None
        except:
           return True
      return True
      
    def dpupdate(self,compteur=100,label="cache"):
      Titre="Creation du cache...."
      if not self.dp:
        self.dp = xbmcgui.DialogProgress()
        self.dp.create("IconMixTools",Titre,"")
      self.dp.update(compteur,Titre,label)
        
        
    def create_cache(self):
        updateActorMovie=None
        updateActorTvShow=None
        updateDirectorMovie=None
        #--- ---------------CACHE ----------------------------------------------
        Titre=None
        self.dp=None
        
        
        self.GlobalCache=utils.GetCache(None,cache_path+"total")
        if self.check_update(WINDOW.getProperty("Movies.count"),"films") or not xbmcvfs.exists(cache_path+"films") or self.PurgeCache:
          self.dpupdate(0,"Films")
          json_result = utils.getJSON("VideoLibrary.GetMovies", '{"properties":["setid"]}')
          self.Data["resultats"]=json_result
          utils.SaveFile(cache_path+"films",self.Data)
          self.GlobalCache["films"]=self.Data.get("total")
          updateActorMovie=True


        if self.check_update(WINDOW.getProperty("TVShows.count"),"tvshows") or not xbmcvfs.exists(cache_path+"tvshows") or self.PurgeCache:
          self.dpupdate(16,"tvshows")
          json_result = utils.getJSON("VideoLibrary.GetTvShows", '{"properties":["episode"]}' )        
          self.Data["resultats"]=json_result
          utils.SaveFile(cache_path+"tvshows",self.Data)
          self.GlobalCache["tvshows"]=self.Data.get("total")
          updateActorTvShow=True


        
        if self.check_update(WINDOW.getProperty("Episodes.count"),"episodes") or not xbmcvfs.exists(cache_path+"episodes") or self.PurgeCache:
          self.dpupdate(32,"Episodes")
          json_result = utils.getJSON("VideoLibrary.GetEpisodes", '{"properties":["tvshowid"]}' )
          self.Data["resultats"]=json_result
          utils.SaveFile(cache_path+"episodes",self.Data)
          self.GlobalCache["episodes"]=self.Data.get("total")

        ListeActors=[]
        if updateActorMovie or not xbmcvfs.exists(cache_path+"acteurs") or self.PurgeCache:
          self.dpupdate(48,"Acteurs")
          json_result = utils.getJSON("Files.GetDirectory", '{"directory":"videodb://movies/actors"}')
          
          if json_result:
            for item in json_result:
               ListeActors.append({"actormovieid":item.get("id"),"label":item["label"]}) 
            self.GlobalCache["actormovie"]=len(ListeActors)
                           
        if updateActorTvShow or not xbmcvfs.exists(cache_path+"acteurs") or self.PurgeCache: 
          self.dpupdate(58,"Acteurs")   
          json_result = utils.getJSON("Files.GetDirectory", '{"directory":"videodb://tvshows/actors"}')
          if json_result:
            for item in json_result:
              ListeActors.append({"actortvshowid":item.get("id"),"label":item["label"]})
            self.GlobalCache["actortv"]=len(ListeActors)
          self.Data["resultats"]=ListeActors
          utils.SaveFile(cache_path+"acteurs",self.Data) 
        Listedirectors=[]   
        if updateActorMovie or not xbmcvfs.exists(cache_path+"realisateurs") or self.PurgeCache:
          self.dpupdate(64,"Realisateurs")    
          json_result = utils.getJSON("Files.GetDirectory", '{"directory":"videodb://movies/directors"}')
          
          if json_result:          
            for item in json_result:
                Listedirectors.append({"directormovieid":item.get("id"),"label":item["label"]})
            self.GlobalCache["directormovie"]=len(Listedirectors)
            
        if updateActorTvShow or not xbmcvfs.exists(cache_path+"realisateurs") or self.PurgeCache:  
          json_result = utils.getJSON("Files.GetDirectory", '{"directory":"videodb://tvshows/directors"}')
          if json_result:
            for item in json_result:
                Listedirectors.append({"directortvshowid":item.get("id"),"label":item["label"]})
            self.GlobalCache["directortv"]=len(Listedirectors)
          self.Data["resultats"]=Listedirectors
          utils.SaveFile(cache_path+"realisateurs",self.Data)  
        
        if self.check_update(WINDOW.getProperty("Music.Artistscount"),"artistes") or not xbmcvfs.exists(cache_path+"artistes") or self.PurgeCache:
          self.dpupdate(80,"Artistes")
          json_result = utils.getJSON("AudioLibrary.GetArtists", '{}' )
          self.Data["resultats"]=json_result
          utils.SaveFile(cache_path+"artistes",self.Data)
          self.GlobalCache["artistes"]=self.Data.get("total")

        if self.check_update(WINDOW.getProperty("Music.Albumscount"),"albums") or not xbmcvfs.exists(cache_path+"albums") or self.PurgeCache:
          self.dpupdate(96,"Albums")
          json_result = utils.getJSON("AudioLibrary.GetAlbums", '{"properties":["artistid"]}' )
          self.Data["resultats"]=json_result
          utils.SaveFile(cache_path+"albums",self.Data)
          self.GlobalCache["albums"]=self.Data.get("total")
          
        if (xbmc.getCondVisibility("Window.IsVisible(10040)") and not xbmcvfs.exists(cache_path+"addons")) or self.PurgeCache:
          self.dpupdate(99,"Addons")
          json_result = utils.getJSON("Addons.GetAddons", '{"properties":["name"]}')
          Listeaddons=[]
          if json_result:          
              for item in json_result:
                  Listeaddons.append({"addonid":item.get("addonid"),"label":item["name"],"type":item["type"]})
          self.Data["resultats"]=Listeaddons
          utils.SaveFile(cache_path+"addons",self.Data)
          self.GlobalCache["addons"]=len(Listeaddons)
        
        GlobalSave={}
        GlobalSave["resultats"]=self.GlobalCache        
        utils.SaveFile(cache_path+"total",GlobalSave)
        self.PurgeCache=None


        if self.dp:
          self.dp.close()
        #--- ---------------CACHE ----------------------------------------------
  
        

    def get_predictions(self, search_str):
        """
        get dict list with autocomplete labels from locally saved lists
        """
        self.listitems = []
        json_result=""
        json_result2=""
        Donnees=None
        MaxItems=50
        
        
        RecherchePartout=xbmc.getCondVisibility("Skin.HasSetting(AutoCompleteTous)")
        if self.PurgeCache and SETTING("autocomplete_cache")=="true":
          logMsg("purge_cache " )
          self.create_cache()
        if len(search_str)>3:
            if SETTING("autocomplete_cache")=="true":
              if not self.PurgeCache:
                self.create_cache()
          #logMsg("basetype (%s)" %self.basetype)
          #if self.basetype=="videos" or RecherchePartout:
          
            if not xbmc.getCondVisibility("Window.IsVisible(10040)"):

              if RecherchePartout or xbmc.getCondVisibility("Skin.HasSetting(AutoCompleteFilms)"):
                json_result=utils.GetCache(search_str,cache_path+"films")
                if json_result:
                  
                    self.createlistitems(json_result,"movie")
              if RecherchePartout or xbmc.getCondVisibility("Skin.HasSetting(AutoCompletetvshows)"):
                json_result=utils.GetCache(search_str,cache_path+"tvshows")
                if json_result:
                  self.createlistitems(json_result,"tvshow")
                #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"VideoLibrary.GetEpisodes","params":{"limits":{"end":2},"filter":{"field":"title","operator":"contains","value":"the"},"properties":["title","tvshowid"]},"id":"1"}
                json_result=utils.GetCache(search_str,cache_path+"episodes")
                if json_result:
                  self.createlistitems(json_result,"episode")
              if RecherchePartout or xbmc.getCondVisibility("Skin.HasSetting(AutoCompleteActeurs)"):
                #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"Files.GetDirectory","params":{"directory":"videodb://movies/actors","limits":{"end":4}},"id":1}
                json_result=utils.GetCache(search_str,cache_path+"acteurs")
                if json_result:
                  ListeActorsMovie=[]
                  ListeActorsTvShow=[]
                  recherche=search_str.lower()
                  for item in json_result:
                    if recherche in item["label"].lower():
                      if item.get("actormovieid"):
                        ListeActorsMovie.append({"actormovieid":item.get("actormovieid"),"label":item["label"]})
                      if item.get("actortvshowid"):
                        ListeActorsTvShow.append({"actortvshowid":item.get("actortvshowid"),"label":item["label"]})
                  if len(ListeActorsMovie)>0:
                    self.createlistitems(ListeActorsMovie,"actormovie")
                  if len(ListeActorsTvShow)>0:
                    self.createlistitems(ListeActorsTvShow,"actortvshow")
                    
                #json_result = utils.getJSON("Files.GetDirectory", '{"directory":"videodb://tvshows/actors"}')
                """
                json_result=utils.GetCache("")
                if json_result:
                  ListeActors=[]
                  recherche=search_str.lower()
                  for item in json_result:
                    if recherche in item["label"].lower():
                      ListeActors.append({"actortvshowid":item.get("id"),"label":item["label"]})
                  if len(ListeActors)>0:
                    self.createlistitems(ListeActors,"actortvshow")
                """
                    
              if RecherchePartout or xbmc.getCondVisibility("Skin.HasSetting(AutoCompleteRealisateurs)"):
                #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"Files.GetDirectory","params":{"directory":"videodb://movies/directors","limits":{"end":4}},"id":1}
                json_result=utils.GetCache(search_str,cache_path+"realisateurs")
                if json_result:
                  Listedirectors=[]
                  recherche=search_str.lower()
                  for item in json_result:
                    if recherche in item["label"].lower():
                      Listedirectors.append({"directormovieid":item.get("directormovieid"),"label":item["label"]})
                  if len(Listedirectors)>0:
                    self.createlistitems(Listedirectors,"directormovie")
                    
                #json_result = utils.getJSON("Files.GetDirectory", '{"directory":"videodb://tvshows/directors"}')
                """
                json_result=utils.GetCache(search_str,cache_path+"realisateurs")
                if json_result:
                  Listedirectors=[]
                  recherche=search_str.lower()
                  for item in json_result:
                    if recherche in item["label"].lower():
                      Listedirectors.append({"directortvshowid":item.get("id"),"label":item["label"]})
                  if len(Listedirectors)>0:
                    self.createlistitems(Listedirectors,"directortvshow")
                """
            #if self.basetype=="music" or RecherchePartout: 
              #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"AudioLibrary.GetArtists","params":{"limits":{"end":2},"filter":{"field":"artist","operator":"contains","value":"madon"}},"id":"1"}     
              #http://127.0.0.1:8080/jsonrpc?request={"jsonrpc":"2.0","method":"AudioLibrary.GetAlbums","params":{"limits":{"end":2},"filter":{"field":"album","operator":"contains","value":"Fear"}},"id":"1"}
              if RecherchePartout or xbmc.getCondVisibility("Skin.HasSetting(AutoCompleteArtistes)"):
                json_result=utils.GetCache(search_str,cache_path+"artistes")
                if json_result:
                    self.createlistitems(json_result,"artist")
              if RecherchePartout or xbmc.getCondVisibility("Skin.HasSetting(AutoCompleteAlbums)"):
                json_result=utils.GetCache(search_str,cache_path+"albums")
                if json_result:
                    self.createlistitems(json_result,"album") 
            else:
              json_result=utils.GetCache(search_str,cache_path+"addons")
              if json_result:                  
                    self.createlistitems(json_result,"addon")
                  
              
        #logMsg("Items (%s)" %self.listitems)
        LL=[] 
        #if (SETTING("autocomplete_tri")=="titre" or xbmc.getCondVisibility("Skin.HasSetting(AutoCompleteTriTitre)"))  and not xbmc.getCondVisibility("Skin.HasSetting(AutoCompleteTriCategorie)"):
        if xbmc.getCondVisibility("Skin.HasSetting(AutoCompleteTriTitre)"):
          #LL=sorted(self.listitems,key=operator.itemgetter('label'))
          LL=sorted(self.listitems, key = lambda x: (x['label']))
          #logMsg("tri par titre")
        else:
          #LL=sorted(self.listitems,key=operator.itemgetter('dbtype'))
          LL=sorted(self.listitems, key = lambda x: (x['dbtype'],x['label']))
          
          #logMsg("tri par categorie")
                     
        return LL            
          
    def createlistitems(self,Donnees=None,DbType=None):
      
      if Donnees:
             for Item in Donnees:
               Titre=Item.get("label")
               try:
                
                DBID=Item.get("%sid" %DbType)
               except:
                DBID=None
               Path=None
               Icon=None
               if DBID:
                
                  if DbType=="artist":
                    Path="musicdb://artists/"
                    Icon="flags/keytype/artist.png"
                    WinId=10502
                  if DbType=="album":
                    Path="musicdb://artists/%s/" %(Item.get("artistid")[0])
                    Icon="flags/keytype/album.png"
                    WinId=10502
                  if DbType=="movie":
                    try:
                      SetId=int(Item.get("setid"))
                    except:
                      SetId=0
                    if SetId>0:
                      Path="videodb://movies/sets/%d/" %(SetId)
                    else:
                      Path="videodb://movies/titles/"
                    Icon="flags/keytype/movie.png"
                    WinId=10025
                  if DbType=="actormovie":
                    Path="videodb://movies/actors/" 
                    Icon="flags/keytype/actor.png"
                    WinId=10025
                  if DbType=="directormovie":
                    Path="videodb://movies/directors/" 
                    Icon="flags/keytype/director.png"
                    WinId=10025
                  if DbType=="tvshow":
                    Path="videodb://tvshows/titles/" 
                    Icon="flags/keytype/tv.png"
                    try:
                      if int(Item.get("episode")>0):
                        WinId=10025
                      else:
                        Titre=None
                    except:
                        Titre=None
                  if DbType=="actortvshow":
                    Path="videodb://tvshows/actors/" 
                    Icon="flags/keytype/actor.png"
                    WinId=10025
                  if DbType=="directortvshow":
                    Path="videodb://tvshows/directors/" 
                    Icon="flags/keytype/director.png"
                    WinId=10025
                  if DbType=="episode":
                    Path="videodb://tvshows/titles/%d/" %(Item.get("tvshowid"))
                    Icon="flags/keytype/episode.png"
                    WinId=10025
                  if DbType=="addon":
                    Path="addon:"+Titre #"addons://user/%s/" %(DBID)
                    Icon="flags/keytype/addon.png"
                    WinId=10146
                
               if Titre:
                 li = {"label": Titre,"dbid":DBID,"dbtype":DbType,"path":Path,"icon":Icon,"winid":WinId}
                 self.listitems.append(li)
               
  



def get_JSON_response(url="", cache_days=7.0, folder=False, headers=False):
    """
    get JSON response for *url, makes use of file cache.
    """
    now = time.time()
    hashed_url = hashlib.md5(url).hexdigest()
    if folder:
        cache_path = xbmc.translatePath(os.path.join(ADDON_DATA_PATH, folder))
    else:
        cache_path = xbmc.translatePath(os.path.join(ADDON_DATA_PATH))
    path = os.path.join(cache_path, hashed_url + ".txt")
    cache_seconds = int(cache_days * 86400.0)
    if xbmcvfs.exists(path) and ((now - os.path.getmtime(path)) < cache_seconds):
        results = read_from_file(path)
        logMsg("loaded file for %s. time: %f" % (url, time.time() - now))
    else:
        response = get_http(url, headers)
        try:
            results = simplejson.loads(response)
            logMsg("download %s. time: %f" % (url, time.time() - now))
            #save_to_file(results, hashed_url, cache_path)
        except:
            logMsg("Exception: Could not get new JSON data from %s. Tryin to fallback to cache" % url)
            logMsg(response)
            if xbmcvfs.exists(path):
                results = read_from_file(path)
            else:
                results = []
    if results:
        return results
    else:
        return []


def get_http(url=None, headers=False):
    """
    fetches data from *url, returns it as a string
    """
    succeed = 0
    if not headers:
        headers = {'User-agent': 'XBMC/14.0 ( phil65@kodi.tv )'}
    request = urllib2.Request(url)
    for (key, value) in headers.iteritems():
        request.add_header(key, value)
    while (succeed < 2) and (not xbmc.abortRequested):
        try:
            response = urllib2.urlopen(request, timeout=3)
            data = response.read()
            return data
        except:
            logMsg("get_http: could not get data from %s" % url)
            xbmc.sleep(1000)
            succeed += 1
    return None


def read_from_file(path="", raw=False):
    """
    return data from file with *path
    """
    if not xbmcvfs.exists(path):
        return False
    try:
        with open(path) as f:
            logMsg("opened textfile %s." % (path))
            if raw:
                return f.read()
            else:
                return simplejson.load(f)
    except:
        logMsg("failed to load textfile: " + path)
        return False




def save_to_file(content, filename, path=""):
    """
    dump json and save to *filename in *path
    """
    if not xbmcvfs.exists(path):
        xbmcvfs.mkdirs(path)
    text_file_path = os.path.join(path, filename + ".txt")
    now = time.time()
    text_file = xbmcvfs.File(text_file_path, "w")
    simplejson.dump(content, text_file)
    text_file.close()
    logMsg("saved textfile %s. Time: %f" % (text_file_path, time.time() - now))
    return True
