### TNotes {version}
===========

tnotes is a console notes manager that stores notes in tsv format.
It might be useful for people who want do CRUD things to their notes in the terminal.
By default tnotes creates /home/$USER/.config/tnotes/default.tsv for your notes you can provide different name by -f flag,
then tnotes will work with ~/.config/tnotes/YOUR_FILE_NAME

#### (screenshot might be helpful)


## Examples
### Writing
```
$ tnotes new_idea -w "I need to make online poker site and be rich"
I need to make online poker site and be rich
$ tnotes new_idea -w "it should have corrupt RNG as anywhere else"
it should have corrupt RNG as anywhere else

$ tnotes new_idea -i
you're writing in /home/grail/.config/tnotes/default.tsv,
enter empty line to end input
>this is way to write my ideas in several lines
>but result would be stored in one index
>

$ tnotes new_idea -is
you're writing in /home/grail/.config/tnotes/default.tsv,
enter empty line to end input
>-is flag is similar to -i flag
>but every line has its own index
>
```

now we can see what we wrote under "new_idea" title:

```
$ tnotes new_idea
new_idea
0 	I need to make online poker site and be rich
1 	it should have corrupt RNG as anywhere else
2 	this is way to write my ideas in several lines
	but result would be stored in one index
3 	-is flag is similar to -i flag
4 	but every line has its own index

```

### replacing

```
#lets fix note at index 1
$ tnotes new_idea 1 -wr "RNG should be uncorrupt"
$ tnotes new_idea
new_idea
0 	I need to make online poker site and be rich
1 	RNG should be uncorrupt
2 	this is way to write my ideas in several lines
	but result would be stored in one index
3 	-is flag is similar to -i flag
4 	but every line has its own index


# write new note
$ tnotes old_idea -is
you're writing in /home/grail/.config/tnotes/default.tsv,
enter empty line to end input
>corrupt RNG
>buy socks
>

$ tnotes old_idea
old_idea
0 	corrupt RNG
1 	buy socks

# replace the whole note
$ tnotes old_idea -wr "build shelters for homeless"
$ tnotes old_idea
old_idea
0 	build shelters for homeless
```

### reading/searching
```
# get notes of title new_idea with 2-3 indexes (incuding right index)
$ tnotes new_idea 2:3
new_idea
2 	this is way to write my ideas in several lines
	but result would be stored in one index
3 	-is flag is similar to -i flag

# write new line to old_idea note containing word "idea"
$ tnotes old_idea -w "this is an old idea note"

# search for word "idea" in old_idea note with -s flag
# search of text is case insensitive, but titles have case sensitivity
$ tnotes old_idea -s idea
old_idea
1 	this is an old idea note

# search for word "idea" in every note
$ tnotes -s idea
new_idea
2 	this is way to write my ideas in several lines
	but result would be stored in one index
old_idea
1 	this is an old idea note


```


## Usage
```
    usage: tnotes [-h] [-f NOTES_FILE] [-w WRITE_MODE]
    [-wr REPLACE_MODE] [-i]
                [-is] [-d] [-l] [-s SEARCH]
                [title [title ...]]

    notes in tsv format

    positional arguments:
    title             title to write your notes;
                        date->title->note

    optional arguments:
    -h, --help        show this help message and exit
    -f NOTES_FILE     tsv file to store your notes; consider
                        difference in column titles
    -w WRITE_MODE     when given writes to file,
                     if given existing title - adds a note
    -wr REPLACE_MODE  replaces note text
    -i                when given uses promt to get input
                         from user to add a note
    -is               same as interactive mode but splits each line in
                    individual note line/index
    -d                deletes note with given title
    -l                lists all titles
    -s SEARCH         text to search in note with given title
                        or all notes if title was not given
```
