# querying a database of music records

from music_records import MusicRecord
from collections import OrderedDict
import sys

def dialog(choice):
    """
    Simple text-based dialog to select an option
    @param choice an ordered dictionary keyword => choice explanation
    @return a key in the dictionary
    """
    ok=False
    k=""
    while not ok:
        print ("Please make a choice:")
        for k in choice:
            print("  {}  ==> {}".format(k, choice[k]))
        k=input("({}): ".format(", ".join(choice.keys())))
        if k in choice:
            ok=True
    return k

if __name__=="__main__":
    import sys
    print("Please be patient, data loading ... ", end="")
    try:
        sys.stdout.flush()
        from free_database import Database
    except:
        from small_database import Database
    print("[Done]")

    choice=OrderedDict((
        ("a", "selection by author"),
        ("t", "selection by title"),
        ("g", "selection by genre"),
    ))
    k=dialog(choice)
    if k=="a": # selection by author
        a=input("Please give some part of the author's name: ")
        possibilities=set([d.author for d in Database if a.lower() in d.author.lower()])
        while len(possibilities)>20: # too many possibilities; change the condition
            print ("There are {} matches; please give more details".format(len(possibilities)))
            a=input("Please give some part of the author's name: ")
            possibilities=set([d.author for d in Database if a.lower() in d.author.lower()])
        choice=OrderedDict()
        n=1
        for p in sorted(list(possibilities)):
            choice[str(n)]=p
            n+=1
        k=dialog(choice)
        a=choice[k]
        print("==| search result with author = {} |==".format(a))
        for d in Database:
            if a.lower()==d.author.lower():
                print(d)
        sys.exit(0)
    elif k=="t": # selection by title
        a=input("Please give some part of the title: ")
        possibilities=set([d.title for d in Database if a.lower() in d.title.lower()])
        while len(possibilities)>20: # too many possibilities; change the condition
            print ("There are {} matches; please give more details".format(len(possibilities)))
            a=input("Please give some part of the title: ")
            possibilities=set([d.title for d in Database if a.lower() in d.title.lower()])
        choice=OrderedDict()
        n=1
        for p in sorted(list(possibilities)):
            choice[str(n)]=p
            n+=1
        k=dialog(choice)
        a=choice[k]
        print("==| search result with title = {} |==".format(a))
        for d in Database:
            if a.lower()==d.title.lower():
                print(d)
                sys.exit(0)
    elif k=="g": # selection by genre
        a=input("Please give some part of the genre's name: ")
        possibilities=set([d.genre for d in Database if a.lower() in d.genre.lower()])
        while len(possibilities)>20: # too many possibilities; change the condition
            print ("There are {} matches; please give more details".format(len(possibilities)))
            a=input("Please give some part of the genre's name: ")
            possibilities=set([d.genre for d in Database if a.lower() in d.genre.lower()])
        choice=OrderedDict()
        n=1
        for p in sorted(list(possibilities)):
            choice[str(n)]=p
            n+=1
        k=dialog(choice)
        a=choice[k]
        print("==| search result with genre = {} |==".format(a))
        for d in Database:
            if a.lower()==d.genre.lower():
                print(d)
                sys.exit(0)
    else:
        raise("This should never happen")
