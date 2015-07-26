# wiva - Wikitext Validator 

`wiva` is a lint-like tool for wikitext, working from the command-line. 

## Installation

	cd wiva
	sudo pip -r requirements.txt
	
## Running
	Usage: wiva <url> [ <revision> ]
            [ --all-articles [ --from=<from> ]]
            [ --wikitext=<wikitext_file> ]
            [ --debug ] [--json]
         
### Basic usage
Most basic usage is just to point `wiva` at an url, it will report all the issues with wikitext.
            
	./wiva http://pl.muppet.wikia.com/wiki/Muppet_Wiki 
	             
	WARNING: Inline style looks bad on mobile
	  <div style="text-align: center;"> </div>
	      ^^^^^^^

	WARNING: Inline style looks bad on mobile
	  <div style="text-align: center;">
	      ^^^^^^^
	      
### Advanced usage
You can also run the check on all articles on a Wikia using the `--all-articles` flag.

	./wiva http://pl.muppet.wikia.com/wiki/a --all-articles         
	
	[    1] Bo nie ma jak sequel ...
	[    2] Constantine ...
	[    3] Czas na Muppet Show ...
	[    4] Gonzo ...
	[    5] Muppet Wiki ...
	WARNING: Inline style looks bad on mobile
	  <div style="text-align: center;"> </div>
	      ^^^^^^^

	WARNING: Inline style looks bad on mobile
	  <div style="text-align: center;">
	      ^^^^^^^

	[    6] Muppety: Poza Prawem ...
You can add a `--from` flag to start from a letter.

	./wiva http://pl.muppet.wikia.com/wiki/a --all-articles --from g
	
	[    1] Gonzo ...
	[    2] Muppet Wiki ...
	WARNING: Inline style looks bad on mobile
	  <div style="text-align: center;"> </div>
	      ^^^^^^^

	WARNING: Inline style looks bad on mobile
	  <div style="text-align: center;">
	      ^^^^^^^

	[    3] Muppety: Poza Prawem ...
	[    4] Muppety (Film) ...
	[    5] Muppety na Manhattanie ...
	[    6] Panna Piggy ...

You can also report this as json using the `--json` flag. This flag also works for single articles. You can pipe it with `> file` as the progress is reported on `stderr` and just the json file is printed on `stdout`. `start` and `end` keys in the json are the character range where the problem occurs.

	./wiva http://es.muppet.wikia.com/wiki/a --all-articles --json         
	[    1] "Bert y Ernie" frente a "Ernie y Bert" ...
	[    2] Episode 119: Vincent Price ...
	[    3] Episodio 1 ...
	[    4] Hitori Mazoji ...
	[    5] Nickelodeon ...
	[    6] Portada ...
	[    7] Rufo Toca El Piano Pero Es Golpeado Por Fozzie ...
	[    8] The Jim Henson Company ...
	[    9] Wiki Muppet ...
	{
	    "http://es.muppet.wikia.com": {
	        "http://es.muppet.wikia.com/wiki/Wiki Muppet": [
	            {
	                "end": 11,
	                "severity": "WARNING",
	                "start": 4,
	                "text": "Inline style looks bad on mobile"
	            },
	            {
	                "end": 50,
	                "severity": "WARNING",
	                "start": 43,
	                "text": "Inline style looks bad on mobile"
	            },
	            {
	                "end": 1839,
	                "severity": "WARNING",
	                "start": 1832,
	                "text": "Inline style looks bad on mobile"
	            }
	        ]
	    }
	}

## Saved Outputs

* [Elder Scrolls Wikia](https://gist.github.com/alistra/8a73185de04db1d573c6) - 290 errors, 29406 warnings generated
* [Spanish Pokekemon](https://gist.github.com/alistra/ae129e5fa1a8cdd4056b) - 564 errors, 68341 warnings generated
* [Fallout](https://gist.github.com/alistra/ca8215e6681e51982efa) - 235 errors, 9107 warnings generated
