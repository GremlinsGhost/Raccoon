

#DebugSend Raccoonin debug-tapahtumien lähetysrajapinta

#Kaikki osat kutsuvat tätä aina kun jokin muuttuu eli:

#DebugCore vastaanottaa eventin
#DebugCore tallentaa sen stateen
#DebugCore lisää sen historiaan
#DebugCore tunnistaa virheet
#DebugView voi myöhemmin piirtää kaiken

from .DebugCore import handle_event

def send(event: str, data: dict):
    
    #Lähetä debug-tapahtuma DebugCorelle.

    #event: tapahtuman nimi, esim. "rects", "motion", "shell"
    #data: tapahtuman sisältö (dict)
    
    try:
        handle_event(event, data)
    except Exception as e:
        # Core ei saa koskaan kaataa Raccoonia
        handle_event("error", {"state": "error", "message": str(e)})
