# a structure to holdmusic records

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

    def summary(self):
        return "Disc Record({author} -- {title})".format(**self.__dict__)

if __name__=="__main__":
    import sys
    print("Please be patient, data loading ... ", end="")
    try:
        sys.stdout.flush()
        from free_database import Database
    except:
        from small_database import Database
    print("[Done]")

    maxShow=20
    print("==========| Complete data presentation |==========")
    n=0
    for d in Database:
        print(d)
        n+=1
        if n>maxShow:
            break

    print("==========| Summary data presentation |==========")
    n=0
    for d in Database:
        print(d.summary())
        n+=1
        if n>maxShow:
            break
    print("==========| showed {} of {} records |==========".format(
        maxShow, len(Database)
    ))
