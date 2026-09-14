"""wl_registry.global -viestin jäsentely.

Waylandin string-tyyppi:
  uint32  pituus (tavuina)
  N       tavua UTF-8 dataa
  padding 0-3 tavua (4 tavun rajaan)

HUOM: pituuden tulkinta vaihtelee toteutuksittain:
  - Wayland-spesifikaatio: pituus EI sisällä NULL-terminaattoria
  - Jotkut toteutukset (mm. KDE Plasma): pituus SISÄLTÄÄ NULLin

Tämä funktio sietää molemmat: se poistaa lopusta NULLit ja
laskee paddingin todellisen pituuden perusteella.
"""

import struct


def parse_global(payload):
    """Jäsennä wl_registry.global -viestin payload.

    Palauttaa (name, interface, version).
    """
    offset = 0

    name, = struct.unpack_from("I", payload, offset)
    offset += 4

    iface_len, = struct.unpack_from("I", payload, offset)
    offset += 4

    # Lue ilmoitettu määrä tavuja
    raw = payload[offset:offset + iface_len]

    # Siivoa NULLit lopusta – sietää molemmat konventiot
    interface = raw.rstrip(b"\x00").decode("utf-8")

    # Offset eteenpäin ilmoitetun pituuden mukaan
    offset += iface_len

    # Padding 4 tavun rajaan (offset on nyt absoluuttinen payloadin alusta)
    offset = (offset + 3) & ~3

    version, = struct.unpack_from("I", payload, offset)

    return name, interface, version