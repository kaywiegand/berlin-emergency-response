# Data Sources — Prüfung und Themenwahl

> Stand 2026-08-29. Grundlage der Entscheidung für dieses Projekt.
> Alle Angaben stammen aus direkten Abrufen der Endpunkte, nicht aus Dokumentation.

---

## Ergebnis

Berliner Feuerwehr, Einsatz- und Hilfsfristdaten. Von vier geprüften Kandidaten
der einzige mit täglicher Aktualisierung, tiefer Historie und einer Frage, die
ohne Vorwissen verständlich ist.

**Leitfrage:** Wie schnell ist der Rettungsdienst bei kritischen Notfällen vor
Ort, wo wird die Hilfsfrist verfehlt, und verschiebt sich das über die Jahre?

---

## Geprüfte Quelle

Repository `Berliner-Feuerwehr/BF-Open-Data`, Lizenz CC BY 4.0.

| Merkmal | Befund |
| :--- | :--- |
| Aktualisierung | täglich, Commit-Message `Automatic Daily Update` |
| Letzter Stand bei Prüfung | 28.08.2026, 07:56 UTC |
| Tagesreihe | 3.155 Zeilen, lückenlos ab 01.01.2018 |
| Rohdaten | rund 600 MB Einzeleinsätze, 2017 bis laufend |
| Geografische Tiefe | 143 Bezirksregionen |
| Repo-Größe gesamt | 6,8 GB |

### Datensätze im Einzelnen

| Pfad | Inhalt | Granularität |
| :--- | :--- | :--- |
| `Daily_Data/BFw_mission_data_daily.csv` | 30 Spalten, Einsatzzahlen und Antwortzeiten | ein Tag, stadtweit |
| `Regional_Data/<Jahr>/` | Einsätze und Hilfsfrist-Erreichung | ein Jahr, je Bezirksregion |
| `Mission_Data/<Jahr>.csv` | Einzeleinsätze mit Datum, Typ, Kritikalität, Bezirk, Antwortzeit | ein Einsatz |
| `Turnout_Times/` | Ausrückzeiten | Quartal |

---

## Der Befund, der das Projekt trägt

Die **Hilfsfrist-Erreichung pro Bezirk im Zeitverlauf existiert nirgends fertig.**

- Die tägliche Zeitreihe enthält Antwortzeiten, aber **keine** Hilfsfrist-Spalten.
- Die regionale Auswertung enthält `timegoal_computed` und `timegoal_reached`,
  ist aber **nur auf Jahre aggregiert**.

Die Kennzahl muss folglich aus den Einzeleinsätzen selbst modelliert werden.
Genau das ist der fachliche Kern des Projekts und der Unterschied zu einem Case,
in dem die Kennzahl bereits in der Quelle liegt.

---

## Verworfene Alternativen

| Quelle | Geprüft | Warum nicht |
| :--- | :--- | :--- |
| SMARD Strommarkt | stündlich, ab 2018, saubere API | flache Story ohne Geografie, stark bearbeitetes Thema. **Als Folgeprojekt auf demselben Stack vorgemerkt.** |
| VBB Nahverkehr | Feed offen, 5,1 MB je Abruf | keine Historie vorgehalten. **Eigenes Sammelprojekt `vbb-realtime-archive` gestartet.** |
| PEGELONLINE | 785 Pegel, Rohdaten ab 2000 | vom Auftraggeber verworfen |
| UBA Luftqualität | Stationen ab 1992 | vom Auftraggeber verworfen |
| DIVI Intensivregister | täglich ab 2020 | Ebenen passen nicht zusammen, Kausalität schwach. Als späte Erweiterung denkbar |
| DWD Wetter | stündlich | kein eigener Erkenntniswert. Als Anreicherung vorgesehen, nicht als Thema |

---

## Bekannte Einschränkungen der Quelle

Aus den Hinweisen des Herausgebers, gehören sichtbar in den späteren Case:

- Maschinell erzeugter Datensatz, Abweichungen zum Jahresbericht möglich,
  vor allem bei der Einstufung als "sonstige" oder interne Einsätze.
- Notrufzahlen fehlen, wenn das Telefonie-Rückfallsystem aktiv war.
- Zum Jahreswechsel 2024/25 gab es eine solche Störung, die Notrufzahlen dieses
  Zeitraums sind unvollständig.
