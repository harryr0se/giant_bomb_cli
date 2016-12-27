#!/usr/bin/python
import urllib2
import json
import sys
import optparse
from subprocess import call
import os

class colours:
    Desc         	= '\033[94m'
    Title         	= '\033[93m'
    Error         	= '\033[31m'
    Debug         	= '\033[32m'
    End         	= '\033[0m'

video_qualities = {  "low",
                     "high",
                     "hd",
                 }

configLocation = os.path.expanduser("~/.giant_bomb_cli")

def gb_log(colour, str):
    print(colour + str + colours.End)

def file_exists_on_server(url):

    #Make the server request
    response = None
    try:
        response = urllib2.urlopen(url)
    except Exception:
        return False

    return True

def convert_seconds_to_string(seconds):
    mins = str(seconds/60)
    secs = str(seconds%60)

    # clean up instance of single digit second values
    # eg [2:8] -> [2:08]
    if( len(secs) == 1 ):
        secs = "0" + secs

    return mins + ":" + secs

def get_status_code_as_string(status_code):
    int_status_code = int(status_code)

    if(int_status_code == 1):
        return "OK"
    elif(int_status_code == 100):
        return "Invalid API Key"
    elif(int_status_code == 101):
        return "Object Not Found"
    elif(int_status_code == 102):
        return "Error in URL Format"
    elif(int_status_code == 103):
        return "'jsonp' format requires a 'json_callback' argument"
    elif(int_status_code == 104):
        return "Filter Error"
    elif(int_status_code == 104):
        return "Subscriber only video is for subscribers only"

def create_filter_string_from_args(args):

    filterString = ""
    if(args.shouldFilter):
        filterString         += "&filter="
        if( args.filterName  != None):
            filterString     += "name:"        + args.filterName + ","
        if( args.contentID   != None):
            filterString     += "id:"          + args.contentID + ","
        if( args.videoType   != None):
            filterString     += "video_type:"  + args.videoType + ","

    return filterString

def create_request_url(args, api_key):
    request_url = "http://www.giantbomb.com/api"
    request_url += "/videos/"
    request_url += "?api_key=" + api_key
    request_url += "&format=json"
    request_url += "&limit=" + str(args.limit)
    request_url += "&offset=" + str(args.offest)
    request_url += "&sort=id:" + args.sortOrder
    return request_url


# Grabs the json file from the server, validates the error code
# If this function returns true then the json obj passed in has been filled with valid data
def retrieve_json_from_url(url, jsonObj):

    #Make the server request
    response = None
    try:
        response = urllib2.urlopen(url).read()
    except urllib2.HTTPError, e:
        gb_log(colours.Error, "HTTPError = " + str(e.code))
    except urllib2.URLError, e:
        gb_log(colours.Error, "URLError = " + str(e.reason))
    except httplib.HTTPException, e:
        gb_log(colours.Error, "HTTPException")
    except Exception:
        gb_log(colours.Error, "generic exception when requesting url: " + url)

    if( response != None):
        jsonFile = json.loads(response)

        if ("status_code" in jsonFile):
            error = get_status_code_as_string(jsonFile["status_code"]);
            if( error == "OK"):
                jsonObj.update(jsonFile)
                return True
        else:
            gb_log(colours.Error, "Error occured: " + error)

    return False

def dump_video_types(api_key):
    gb_log(colours.Title, "Dumping video type IDs")
    video_types_url = "http://www.giantbomb.com/api/video_types/?api_key=" + api_key + "&format=json"
    jsonObj = json.loads("{}")

    if  False == retrieve_json_from_url(video_types_url, jsonObj):
        gb_log(colours.Error, "Failed to retrieve video types from GB API")
        return 1
    
    for video_type in jsonObj["results"]:
        gb_log(colours.Desc, ("\t %2i: %s - (%s)") % (video_type["id"], video_type["name"], video_type["deck"]))

def validate_args(opts):
    # Validate filters
    if( False == opts.shouldFilter ):
        if( opts.filterName != None or opts.contentID != None or opts.videoType != None ):
            gb_log(colours.Error, "Please use --filter command to process filter arguments")
            return False

    if( opts.quality != None ):
        if( opts.quality not in video_qualities):
            gb_log(colours.Error, "Invalid quality value, options are 'low', 'high', 'hd'")
            return False

    if( opts.sortOrder != "asc" and opts.sortOrder != "desc" ):
        gb_log(colours.Error, "Invalid sort value, options are 'asc' or 'desc'")
        return False

    return True

def stream_video(url):
    if( url == None ):
        gb_log(colours.Error, "Invalid URL, perhaps try another quality level?")
        return

    try:
        call(["mplayer", url + "?api_key=" + get_api_key()])
    except Exception:
        gb_log(colours.Error, "Something has gone wrong whilst trying to stream, is mplayer installed?")

def download_video(url, filename):
    if( url == None ):
        gb_log(colours.Error, "Invalid URL, perhaps try another quality level?")
        return

    gb_log(colours.Title, "Downloading " + url + " to " + filename)
    try:
        call(["wget", "--user-agent", "downloading via giant_bomb_cli", url + "?api_key=" + get_api_key(), "-c", "-O", filename])
    except Exception:
        gb_log(colours.Error, "Something has gone wrong whilst trying to download, is wget installed?")

# Prints details of videos found
def output_response(response, args):

    for video in response["results"]:
        name        = video["name"]
        desc        = video["deck"]
        timeInSecs  = video["length_seconds"]
        videoID     = video["id"]
        videoType   = video["video_type"]
        url         = video[args.quality + "_url"]

        gb_log(colours.Title, "%s (%s) [%s] ID:%i" % (name, videoType, convert_seconds_to_string(timeInSecs), videoID))
        gb_log(colours.Desc, "\t" + desc)

        if(args.shouldStream):
            stream_video(url)
        elif(args.shouldDownload):
            # Construct filename
            filename     = name.replace(" ", "_")
            filename     = filename.replace("/", "-")
            filename     = filename.replace(":", "")
            filename     += "." + url.split(".")[-1]

            if(args.outputFolder != None):
                if(not os.path.exists(args.outputFolder)):
                    os.makedirs(args.outputFolder)
                    filename = args.outputFolder + "/" + filename

            download_video(url, filename)

    if(len(response["results"]) == 0):
        gb_log(colours.Desc, "No video results")

def get_api_key():
    if(False == os.path.exists(configLocation)):
        os.makedirs(configLocation)

    configFilePath = configLocation + "/config"

    config_json = json.loads("{}")
    if(os.path.isfile(configFilePath)):
        config_json = json.load(open(configFilePath, "r"))
    else:
        userAPI = raw_input('Please enter your API key: ')
        config_json["API_KEY"] = userAPI.strip();
        json.dump(config_json, open(configFilePath, "w"))

    return config_json["API_KEY"]

def main():
    parser = optparse.OptionParser(version='Giant Bomb Command Line Interface v1.0.0')

    parser.add_option('-l', '--limit'       , dest="limit"               , action="store"         , type="int", default=25, metavar="<x>", help="limits the amount of items requested, defaults to %default")
    parser.add_option('--offset'            , dest="offest"              , action="store"         , type="int", default=0, metavar="<x>", help="specify the offest into the results, defaults to %default")
    parser.add_option('--quality'           , dest="quality"             , action="store"         , default="high", help="the quality of the video, used when streaming or downloading, (low, high, hd) defaults to %default")
    parser.add_option('--download'          , dest="shouldDownload"      , action="store_true"    , help="will attempt to download all videos matching filters", default=False)
    parser.add_option('--stream'            , dest="shouldStream"        , action="store_true"    , help="will attempt to stream videos matching filters via mplayer", default=False)
    parser.add_option('--output'            , dest="outputFolder"        , action="store"         , help="the folder to output downloaded content to")
    parser.add_option('--dump_video_types'  , dest="shouldDumpIDs"       , action="store_true"    , help="will dump all known ids for video types,", default=False )
    parser.add_option('--filter'            , dest="shouldFilter"        , action="store_true"    , help="will attempt to filter by the below arguments", default=False )
    parser.add_option('--sort'              , dest="sortOrder"           , action="store"         , default="desc", help="orders the videos by their id (asc/desc) defaults to desc")

    # Filter options
    filter_options = optparse.OptionGroup(parser, "Filter options", "Use these in conjunction with --filter to customise results")
    filter_options.add_option('--name'              , dest="filterName"          , action="store"         , help="search for videos containing the specified phrase in the name")
    filter_options.add_option('--id'                , dest="contentID"           , action="store"         , help="id of the video")
    filter_options.add_option('--video_type'        , dest="videoType"           , action="store"         , help="id of the video type (see --dump_video_types)")

    # Debug options
    degbug_options = optparse.OptionGroup(parser, "Debug Options")
    degbug_options.add_option('--debug'             , dest="debugMode"           , action="store_true"    , help="logs server requests and json responses", default=False)

    parser.add_option_group(filter_options)
    parser.add_option_group(degbug_options)
    (opts, args) = parser.parse_args()

    if( False == validate_args(opts) ):
        return 1

    # Check for API key
    api_key = get_api_key();

    if( opts.shouldDumpIDs ):
        dump_video_types(api_key)
        return 0

    # Create the url and make the request
    requestURL	= create_request_url(opts, api_key) + create_filter_string_from_args(opts)
    jsonObj    	= json.loads("{}")

    if( opts.debugMode ):
        gb_log(colours.Debug, "Requesting url: " + requestURL)

    if( False == retrieve_json_from_url(requestURL, jsonObj) ):
        gb_log(colours.Error, "Failed to get response from server")
        return 1

    if( opts.debugMode ):
        gb_log(colours.Debug, "Received %i of %i possible results" % (jsonObj["number_of_page_results"], jsonObj["number_of_total_results"]))
        gb_log(colours.Debug, json.dumps(jsonObj, sort_keys=True, indent=4))

    output_response(jsonObj, opts)

main()
