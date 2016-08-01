#!/usr/bin/python3

import os, os.path, re

from music_records import MusicRecord

class MyMusicRecord(MusicRecord):
    def __init__(self, *args):
        MusicRecord.__init__(self, *args)

    def asSource(self):
        """
        @return the source Rvalue which can initialize a MusicRecord
        """
        return """MusicRecord({},{},{},{},{},{})""".format(
            repr(self.disk_id),
            repr(self.disk_title),
            repr(self.author),
            repr(self.title),
            repr(self.year),
            repr(self.genre)
        )
def getByPattern(regexp, line):
    """
    gets a value prefixed by a regular expression
    @param regexp aregular expression with one possible matching group
    @param line a line of text
    @result a string
    """
    m=regexp.match(line)
    if not m:
        return ""
    else:
        return m.group(1)


def recordsFromFile(filename):
    """
    Builds a list of MusicRecord instances from a given file
    @param filename the name of the file
    @return a list of MusicRecord instances
    """
    idPattern=re.compile(r"DISCID=(.*)")
    dtitlePattern=re.compile(r"DTITLE=(.*)")
    yearPattern=re.compile(r"DYEAR=(.*)")
    genrePattern=re.compile(r"DGENRE=(.*)")
    ttitlePattern=re.compile(r"TTITLE.*=(.*)")
    separator=re.compile(" / ")

    try:
        with open(filename, encoding="utf-8") as infile:
            lines=infile.readlines()
    except:
        with open(filename, encoding="latin-1") as infile:
            lines=infile.readlines()
    disk={
        "disk_id":     idPattern,
        "title":      dtitlePattern,
        "year":       yearPattern,
        "genre":      genrePattern,
        "author_all": "",
    }
    keys=["disk_id", "title", "year", "genre"]
    waiting=0
    result=[]
    for l in lines:
        if waiting < len(keys):
            found=getByPattern(disk[keys[waiting]],l)
            if found:
                disk[keys[waiting]]=found
                if keys[waiting]=="title":
                    authorDtitle=separator.split(found)
                    if len(authorDtitle) > 1:
                        disk["author_all"]=authorDtitle[0]
                        disk["title"]=authorDtitle[1]
                waiting+=1
        else:
            assert [isinstance(disk[k],str) for k in disk] == ([True]*len(disk))
            found=getByPattern(ttitlePattern, l)
            authorTtitle=separator.split(found)
            if len(authorTtitle)>1:
                author=authorTtitle[0]
                title=authorTtitle[1]
            else:
                author=disk["author_all"]
                title=found
            if found:
                m=MyMusicRecord(
                    disk["disk_id"],
                    disk["title"],
                    author,
                    title,
                    disk["year"],
                    disk["genre"]
                )
                result.append(m)
    return result

if __name__=="__main__":
    import sys
    n=0
    with open("free_database.py","w") as outfile:
        outfile.write("from music_records import MusicRecord\n\nDatabase=[\n")
        for root, dirs, files in os.walk('./freedb'):
            for f in files:
                path=os.path.join(root, f)
                records=recordsFromFile(path)
                for r in records:
                    outfile.write("  "+r.asSource()+",\n")
                    n+=1
                print("{}\r".format(n), end="")
                sys.stdout.flush()
        outfile.write("]\n")
    print("\nWrote {} records to free_database.py".format(n))
