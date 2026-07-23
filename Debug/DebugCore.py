#Kerää kaikki tapahtumat Raccoonin eri osista

#Tallentaa viimeisimmän tilan jokaiselle event‑tyypille

#Tunnistaa virheet automaattisesti, jos data["state"] == "error"

#Rakentaa muutoshistorian, jota DebugView voi myöhemmin visualisoida

#Tarjoaa yhteenvedon, jota voi tulostaa konsoliin tai UI:hin


#  muutoskoneen ydin

# Vastaanottaa tapahtumia DebugSendiltä ja pitää kirjaa kaikista muutoksista, virheistä ja tiloista.


from datetime import datetime

class DebugCore:
    def __init__(self):
        self.events = []          # kaikki tapahtumat
        self.state = {}           # viimeisin tila per avain
        self.errors = []          # virheet
        self.history = []         # muutoshistoria

    def handle_event(self, event: str, data: dict):
        # Käsittelee yhden debug tapahtuman
        timestamp = datetime.now().isoformat()
        entry = {"event": event, "data": data, "time": timestamp}
        self.events.append(entry)
        self.state[event] = data

        # virheiden tunnistus
        if isinstance(data, dict) and data.get("state") == "error":
            self.errors.append(entry)

        # muutoshistoria
        self.history.append(f"{timestamp}: {event}")

    def summary(self) -> dict:
        # palauttaa debug tilan yhteenvedon
        return {
            "events": len(self.events),
            "errors": len(self.errors),
            "last_event": self.events[-1]["event"] if self.events else None,
            "state_keys": list(self.state.keys()),
        }

# Yksittäinen instanssi jota muut moduulit voivat käyttää
core = DebugCore()

def handle_event(event: str, data: dict):
    # Ulkoisen kutsun rajapinta (DebugSend käyttää tätä)
    core.handle_event(event, data)
