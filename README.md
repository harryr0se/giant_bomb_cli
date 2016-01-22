# giant_bomb_cli
Command line utility for downloading and streaming videos from Giant Bomb!

![Example](http://i.imgur.com/IEeJ75N.gif)

```
Usage: giant_bomb_cli.py [options]

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -l <x>, --limit=<x>   limits the amount of items requested, defaults to 25
  --offset=<x>          specify the offest into the results, defaults to 0
  --quality=QUALITY     the quality of the video, used when streaming or
                        downloading, defaults to high
  --download            will attempt to download all videos matching filters
  --stream              will attempt to stream videos matching filters via
                        mplayer
  --output=OUTPUTFOLDER
                        the folder to output downloaded content to
  --dump_video_types    will dump all known ids for video types,
  --filter              will attempt to filter by the below arguments

  Filter options:
    Use these in conjunction with --filter to customise results

    --name=FILTERNAME   search for videos containing the specified phrase in
                        the name
    --id=CONTENTID      id of the video
    --video_type=VIDEOTYPE
                        id of the video type (see --dump_video_types)

  Debug Options:
    --debug             logs server requests and json reponses
```

# FAQ

## Where can I get my api key from?
Your api key can be requested and found at http://www.giantbomb.com/api/

## Where is my api key stored?
Your api key is stored in your home directory (~/.giant_bomb_cli/config)

If you wish to change api key, just delete the config file and you'll be prompted to input a new one next time the script is run
