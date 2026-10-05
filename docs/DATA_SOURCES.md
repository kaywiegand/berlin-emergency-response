
# Data Sources — Prüfung und Themenwahl

> Stand 2026-08-29. Grundlage der Entscheidung für dieses Projekt.
> Alle Angaben stammen aus direkten Abrufen der Endpunkte, nicht aus Dokumentation.

---

## Ergebnis

Berliner Feuerwehr, Einsatz- und Hilfsfristdaten. Von vier geprüften Kandidaten der einzige mit täglicher Aktualisierung, tiefer Historie und einer Frage, die ohne Vorwissen verständlich ist[cite: 2].

**Leitfrage:** Wie schnell ist der Rettungsdienst bei kritischen Notfällen vor Ort, wo wird die Hilfsfrist verfehlt, und verschiebt sich das über die Jahre[cite: 2]?

---

## Geprüfte Quelle

Repository `Berliner-Feuerwehr/BF-Open-Data`, Lizenz CC BY 4.0[cite: 2].

| Merkmal | Befund |
| :--- | :--- |
| Aktualisierung | täglich, Commit-Message `Automatic Daily Update`[cite: 2] |
| Letzter Stand bei Prüfung | 28.08.2026, 07:56 UTC[cite: 2] |
| Tagesreihe | 3.155 Zeilen, lückenlos ab 01.01.2018[cite: 2] |
| Rohdaten | rund 600 MB Einzeleinsätze, 2017 bis laufend[cite: 2] |
| Geografische Tiefe | 143 Bezirksregionen[cite: 2] |
| Repo-Größe gesamt | 6,8 GB[cite: 2] |

### Datensätze im Einzelnen

| Pfad | Inhalt | Granularität |
| :--- | :--- | :--- |
| `Daily_Data/BFw_mission_data_daily.csv` | 30 Spalten, Einsatzzahlen und Antwortzeiten | ein Tag, stadtweit[cite: 2] |
| `Regional_Data/<Jahr>/` | Einsätze und Hilfsfrist-Erreichung | ein Jahr, je Bezirksregion[cite: 2] |
| `Mission_Data/<Jahr>.csv` | Einzeleinsätze mit Datum, Typ, Kritikalität, Bezirk, Antwortzeit | ein Einsatz[cite: 2] |
| `Turnout_Times/` | Ausrückzeiten | Quartal[cite: 2] |

---

## Der Befund, der das Projekt trägt

Die **Hilfsfrist-Erreichung pro Bezirk im Zeitverlauf existiert nirgends fertig.**[cite: 2]

- Die tägliche Zeitreihe enthält Antwortzeiten, aber **keine** Hilfsfrist-Spalten[cite: 2].
- Die regionale Auswertung enthält `timegoal_computed` und `timegoal_reached`, ist aber **nur auf Jahre aggregiert**[cite: 2].

Die Kennzahl muss folglich aus den Einzeleinsätzen selbst modelliert werden[cite: 2]. Genau das ist der fachliche Kern des Projekts und der Unterschied zu einem Case, in dem die Kennzahl bereits in der Quelle liegt[cite: 2].

---

## Bekannte Einschränkungen der Quelle

- Maschinell erzeugter Datensatz, Abweichungen zum Jahresbericht möglich, vor allem bei der Einstufung als "sonstige" oder interne Einsätze[cite: 2].
- Notrufzahlen fehlen, wenn das Telefonie-Rückfallsystem aktiv war[cite: 2].
- Zum Jahreswechsel 2024/25 gab es eine solche Störung, die Notrufzahlen dieses Zeitraums sind unvollständig[cite: 2].