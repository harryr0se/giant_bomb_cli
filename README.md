# giant_bomb_cli
Command line utility for downloading and streaming videos from Giant Bomb!

![Example](http://i.imgur.com/IEeJ75N.gif)

# Examples

##### Download the first 3 Mario Party Party videos
```
giant_bomb_cli.py -l 3 --sort asc --filter --name "Mario Party Party" --download
```
This searches for the first three videos with "Mario Party Party" in the title and downloads them in ascending order

##### Download all the Assassin's Creed Quick Looks at low quality
```
giant_bomb_cli.py --filter --name "Assassin's Creed" --video_show 3 --quality low --download
```
This searches for all videos with "Assassin's Creed" in the title, in the Quick Look category (video show 3).

It sets the requested quality to low and then downloads them in descending order

# Usage
```
Usage: giant_bomb_cli.py [options]

Options:
  -v, --version         show program's version number and exit
  -l <x>, --limit <x>   limits the amount of items requested, defaults to 25
  --offset <x>          specify the offest into the results, defaults to 0
  --quality QUALITY     the quality of the video, used when streaming or
                        downloading (low, high, hd) defaults to high
  --download            will attempt to download all videos matching filters
  --stream              will attempt to stream videos matching filters via
                        mplayer
  --output OUTPUTFOLDER
                        the folder to output downloaded content to
  --dump_video_shows    will dump all known ids for video shows,
  --filter              will attempt to filter by the below arguments
  --sort SORTORDER      orders the videos by their id (asc/desc) defaults to
                        desc
  --download-archive DOWNLOADARCHIVE
                        Download videos whose ids aren't listed within the
                        file, the script will also update the archive file
                        each run

Filter options:
  Use these in conjunction with --filter to customise results

  --name FILTERNAME     search for videos containing the specified phrase in
                        the name
  --id CONTENTID        id of the video
  --video_show VIDEOSHOW
                        id of the video show (see --dump_video_shows)

Debug Options:
  --debug               logs server requests and json responses
```


# FAQ

## Where can I get my api key from?
Your api key can be requested and found at http://www.giantbomb.com/api/

## Where is my api key stored?
Your api key is stored in your home directory (~/.giant_bomb_cli/config)

If you wish to change api key, just delete the config file and you'll be prompted to input a new one next time the script is run
