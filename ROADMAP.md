# ROADMAP — berlin-emergency-response

> Ausgangslage → Phasen → Ziel
> Inhaltliches Konzept: [docs/KONZEPT.md](docs/KONZEPT.md)

---

## Ausgangslage

Die Berliner Feuerwehr veröffentlicht Einsatzdaten täglich unter CC BY 4.0, ab
2018 lückenlos, bis hinunter auf den Einzeleinsatz. Die entscheidende Kennzahl,
die Hilfsfrist-Erreichung je Bezirk im Zeitverlauf, fehlt jedoch in allen
fertigen Dateien und muss selbst modelliert werden.

Das bestehende Portfolio besteht aus sieben abgeschlossenen Analysen. Keine
davon läuft weiter. Dieses Projekt schließt genau diese Lücke.

---

## Phasen

- [ ] **Phase 0 — Fundament und Quellenvertrag**
      Sondierung der Quelle in einem Notebook: Spalten, Lücken, Ausreißer,
      Zeitzonen. Hilfsfrist-Definition in `docs/DATA_DICTIONARY.md` schriftlich
      festhalten, inklusive Begründung.
      *Ergebnis: dokumentiert, welche Felder die Kennzahl bilden und warum.*

- [ ] **Phase 1 — Ingestion**
      Loader zieht gezielt einzelne Raw-Dateien, kein Repo-Clone. Roh-Landung
      mit Ladezeitpunkt, idempotent. GitHub-Actions-Cron nach dem
      Upstream-Update.
      *Ergebnis: grüner Workflow-Lauf, ab hier läuft es von allein.*

- [ ] **Phase 2 — dbt-Modellierung**
      staging, intermediate, marts sauber getrennt. Hilfsfrist-Quote je Tag und
      Bezirk als inkrementelles Modell. Window Functions für gleitende Mittel
      und Vorjahresvergleich.
      *Ergebnis: die Kennzahl, die es fertig nicht gibt, ist reproduzierbar.*

- [ ] **Phase 3 — Qualität als System**
      Standardtests, eigene Tests auf fachliche Unmöglichkeiten, source
      freshness, Schema-Drift-Erkennung.
      *Ergebnis: Fehler fallen auf, bevor sie im Dashboard stehen.*

- [ ] **Phase 4 — Dashboard**
      Überblick mit Quote, Trend und auffälligen Bezirken. Datenstand auf jeder
      Seite sichtbar. Deploy auf GitHub Pages, verlinkt aus dem Hub.
      *Ergebnis: öffentlich erreichbar und jeden Morgen von selbst aktuell.*

- [ ] **Phase 5 — CI und Portfolio-Layer**
      `dbt build` je Pull Request, Lineage-Graph in README und TechView,
      `/project-case` für Hub und Views, Kapitel zu den Aussagegrenzen.
      *Ergebnis: portfolio-ready und im Hub verlinkt.*

**Sollbruchstelle:** Nach Phase 3 ist das Projekt vorzeigbar. Alles danach
erhöht die Qualität, ist aber nicht Voraussetzung.

---

## Ziel

Ein Datenprodukt, das täglich ohne Eingriff läuft und die Frage beantwortet, wo
der Berliner Rettungsdienst seine gesetzliche Hilfsfrist hält und wo nicht.

Erfolgskriterien im Detail: [docs/KONZEPT.md](docs/KONZEPT.md), Abschnitt 6.

---

## Offene Entscheidungen

- **Hilfsfrist-Definition.** Welche Einsatzarten, ab welchem Zeitstempel, wie
  mit unvollständigen Datensätzen umgehen. Muss vor Phase 2 stehen.
- **Wetter als Anreicherung.** DWD-Daten dazuholen oder erst später. Betrifft
  die Modellierung ab Phase 2.
