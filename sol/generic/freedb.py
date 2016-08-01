#!/usr/bin/python3

import os, os.path, re

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


class MusicRecord(object):
    def __init__(self, disk_id, disk_title, author, title, year, genre):
        self.author=author
        self.title=title
        self.year=year
        self.disk_id=disk_id
        self.disk_title=disk_title
        self.genre=genre
        return
    def __str__(self):
        return """\
MusicRecord instance:
        author     = {author}
        title      = {title}
        year       = {year}
        disk_id    = {disk_id}
        disk title = {disk_title}
        genre      = {genre}
""".format(**self.__dict__)

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
            print("GRRR searching", keys[waiting])
            found=getByPattern(disk[keys[waiting]],l)
            if found:
                disk[keys[waiting]]=found
                print("GRRR found ", keys[waiting], found)
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
                m=MusicRecord(
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
    for root, dirs, files in os.walk('./freedb'):
        for f in files:
            path=os.path.join(root, f)
            print(path, "==>\n", recordsFromFile(path))
            break
