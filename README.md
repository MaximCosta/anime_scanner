
# anime_scanner

## Package :
 - argparse  
 - time
 - mysql.connector  
 - requests  
 - bs4 
 - progress.bar

## Install :
`python3 -m pip install argparse mysql-connector-python requests bs4 progress`

## Start

    $ python3 main.py -n 1 # scan page one
    $ python3 main.py -n 1 -f # scan page one and force update in data base
    $ python3 main.py -n 24 # Scans the first page to twenty-fourth page
    $ python3 main.py -n 1 -a # Scans the first page every hours
    $ python3 main.py -n 1 -a -t 2 # Scans the first page every 2 hours
    $ python3 main.py -p "https://vostfree.com/878-jujutsu-kaisen-vostfr-ddl-streaming.html" # return episode info on terminal
    $ python3 main.py -p "https://vostfree.com/878-jujutsu-kaisen-vostfr-ddl-streaming.html" -o <input> # return episode info on file

## Help

	usage: vostree_scrap_new [-h] [-n nbpage] [-f] [-p page] [-o output] [-u] [-a] [-t time]

	Get new anime from vostree

	optional arguments:

		  -h, --help                      show this help message and exit
		  -n nbpage, --nbpage nbpage      Number of pages that will be analyzed
		  -f, --force                     force update anime
		  -p page, --page page            return episode of specified page
		  -o output, --output output      The output file of the page that will be analyzed, if it is not specified, the output will be on the command line
		  -a, --alwaysup        run prgram, every hours
		  -t time, --time time  every X hours program run
