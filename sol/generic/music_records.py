# a structure to holdmusic records

class Music(object):
    
    def __init__(self, title="unknown", author="", editor="",
                 duration=0, styles=[]):
        """
        the constructor.
        @param title title of the record
        @param author author of the record
        @param editor editor of the record
        @param duration duration of the record (seconds)
        @param styles list of musical categories
        """
        self.title=title
        self.author=author
        self.editor=editor
        self.duration=duration
        self.styles=styles
        return
        
    def __str__(self):
        """
        Defaut conversion to string
        """
        result="Music Record\n"
        result += "  TITLE:    {title}\n".format(**self.__dict__)
        result += "  AUTHOR:   {author}\n".format(**self.__dict__)
        result += "  EDITOR:   {editor}\n".format(**self.__dict__)
        result += "  DURATION: {}\n".format(self.minutes())
        result += "  STYLES:   {}\n".format(", ".join(self.styles))
        return result
        
    def minutes(self):
        """
        format the duration as a string with hours, minutes and seconds
        @return a string
        """
        d=self.duration
        h = d // 3600
        d = d % 3600
        m = d // 60
        s = d % 60
        result=[]
        if h:
            result.append("{} h".format(h))
        if m:
            result.append("{} min".format(m))
        result.append("{} s".format(s))
        return " ".join(result)

    def summary(self):
        """
        gives a very short summary of a record
        @return a short string
        """
        return "{} -- {}".format(self.author, self.title)
        
        
myMusic=[]
myMusic.append(
    Music(
        "I'm Happy, Darling, Dancing With You",
        "Dizzy Gillespie",
        "Bluebird",
        179,
        ["Jazz","Blues","Fantasy"]
    )
)
myMusic.append(
    Music(
        "Worried Life Blues",
        "Dizzy Gillespie",
        "Xanadu",
        195,
        ["Jazz","Blues"]
    )
)
     
if __name__=="__main__":
    for m in myMusic:
        print(m)
    print ("==================")
    for m in myMusic:
        print(m.summary())
        
    
