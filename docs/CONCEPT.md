# Concept — Berlin Emergency Response

> Was gebaut wird, warum, und woran der Erfolg gemessen wird.
> Grundlage: [DATA_SOURCES.md](DATA_SOURCES.md). Phasenplan: [ROADMAP.md](../ROADMAP.md).

---

## 1 · Worum es geht

Der Rettungsdienst hat eine gesetzlich definierte Frist, innerhalb derer er bei
einem kritischen Notfall vor Ort sein soll. Ob diese Frist gehalten wird, ist
eine öffentlich diskutierte Frage. Die Berliner Feuerwehr veröffentlicht die
nötigen Daten, aber die Kennzahl selbst wird nur jährlich und nur grob regional
ausgewiesen.

**Leitfrage**
Wie schnell ist der Rettungsdienst bei kritischen Notfällen tatsächlich vor Ort,
in welchen Bezirken wird die Hilfsfrist verfehlt, und wie verschiebt sich das
über die Jahre?

**Abgrenzung — was dieses Projekt nicht ist**
Keine Bewertung der Einsatzkräfte. Antwortzeiten hängen an Standortdichte,
Verkehr, Bebauung und Einsatzaufkommen, nicht an der Leistung einzelner Teams.
Das Projekt beschreibt Struktur, nicht Verschulden.

---

## 2 · Was das Projekt vom bisherigen Portfolio unterscheidet

Sieben bestehende Cases zeigen, dass Datensätze beherrscht werden. Alle sind
eingefroren: Datensatz rein, Analyse, Präsentation, fertig.

Dieses Projekt ist das erste, das **läuft**. Es holt sich jeden Tag neue Daten,
prüft sie automatisch und aktualisiert sein Ergebnis ohne Zutun. Das ist der
Unterschied zwischen jemandem, der Analysen liefert, und jemandem, der ein
Datenprodukt verantwortet.

Konkret belegt es folgende Fähigkeiten, die bisher fehlen:

| Fähigkeit | Wird sichtbar durch |
| :--- | :--- |
| SQL in der Tiefe | dbt-Modelle mit CTEs, Window Functions, inkrementeller Logik |
| Datenmodellierung | Layer-Trennung, Fakten und Dimensionen, bewusst gewählte Korngröße |
| Datenqualität als Prozess | automatische Tests statt einmaliger Prüfung |
| Orchestrierung | geplanter Lauf, Fehlerbehandlung, nachvollziehbare Historie |
| Kennzahl definieren | Hilfsfrist selbst hergeleitet und schriftlich begründet |
| Betrieb über Zeit | läuft weiter, auch wenn niemand hinschaut |

---

## 3 · Die zentrale fachliche Aufgabe

Die Hilfsfrist-Quote pro Bezirk und Tag existiert in keiner Quelldatei. Sie muss
aus den Einzeleinsätzen gebildet werden. Damit rückt eine Definitionsfrage in
den Mittelpunkt, die vor der ersten Zeile SQL schriftlich beantwortet sein muss:

- **Welche Einsätze zählen?** Nur kritische Rettungsdiensteinsätze, oder auch
  Brandeinsätze mit eigener Frist?
- **Ab wann läuft die Uhr?** Notrufannahme, Alarmierung oder Ausrücken.
- **Was gilt als "vor Ort"?** Erstes Fahrzeug oder das fachlich erforderliche.
- **Wie werden unvollständige Zeitstempel behandelt?** Die Quelle unterscheidet
  selbst zwischen `timegoal_computed` und `timegoal_reached`. Einsätze ohne
  vollständige Zeitstempel dürfen die Quote nicht schönen.

Diese Entscheidungen gehören mit Begründung in `docs/DATA_DICTIONARY.md`. Sie
sind der Teil, der im Fachgespräch geprüft wird.

---

## 4 · Architektur

Bewusst kleiner Stack. Jede Komponente ist kostenlos, ohne Kreditkarte nutzbar
und in Bewerbungsgesprächen ein bekannter Name.

```
BF-Open-Data (GitHub)
        │  gezielt einzelne Raw-Dateien, kein Clone (Upstream ist 6,8 GB)
        ▼
   Ingestion (Python)  ──►  data/raw/  mit Ladezeitpunkt
        │
        ▼
     DuckDB  ◄── dbt: staging → intermediate → marts
        │           plus Tests und source freshness
        ▼
   Dashboard (Evidence.dev)  ──►  GitHub Pages
        │
        └── CI: dbt build bei jedem Pull Request
```

| Schicht | Werkzeug | Begründung |
| :--- | :--- | :--- |
| Orchestrierung | GitHub Actions | Cron ohne Server, Läufe öffentlich einsehbar |
| Ingestion | Python, httpx | gezielter Abruf, Upstream-Clone verbietet sich |
| Warehouse | DuckDB | eine Datei, SQL-vollständig, 600 MB problemlos |
| Transformation | dbt-core | eigentlicher Zweck: Layering, Tests, Lineage |
| Serving | Evidence.dev | SQL-natives BI, statisches HTML, passt in den bestehenden Hub |
| CI | GitHub Actions | `dbt build` je Pull Request |

### Modell-Layer

- **staging** — eine Sicht je Quelldatei. Nur Umbenennung, Typisierung,
  Zeitzone. Keine fachliche Logik.
- **intermediate** — Einsätze auf Tag und Bezirk verdichtet, Hilfsfrist-Flag je
  Einsatz nach dokumentierter Definition, Wetter angereichert.
- **marts** — `fct_missions_daily`, `fct_response_times`, `dim_district`,
  `dim_date`. Bedient Dashboard und Ad-hoc-Fragen.

---

## 5 · Qualitätssicherung

Der Bogen zum bestehenden Portfolio: im Telefónica-Case wurde ein negativer
Anrufzähler von Hand gefunden, den die Musterlösung übersehen hatte. Richtig,
aber manuell. Hier fängt ein Test das automatisch ab, bevor es in ein Dashboard
gelangt.

- Standardtests auf Schlüssel, Pflichtfelder, Wertebereiche
- Eigene Tests auf fachliche Unmöglichkeiten: negative Antwortzeiten, Quoten
  über 100 Prozent, mehr erreichte als berechnete Fristen
- `source freshness`, schlägt an, wenn der Upstream ausfällt
- Test auf Schema-Drift, falls die Behörde Spalten umbenennt

---

## 6 · Erfolgskriterien

Das Projekt gilt als gelungen, wenn:

1. Die Pipeline seit mindestens vier Wochen täglich ohne Eingriff läuft.
2. Die Hilfsfrist-Definition schriftlich begründet und im Modell umgesetzt ist.
3. Ein Fremder das Dashboard öffnen und sehen kann, dass die Daten von heute
   drin sind.
4. Mindestens ein Test im Betrieb einen echten Datenfehler abgefangen hat.
5. Ein Kapitel zu den Aussagegrenzen existiert, wie in den anderen Cases.

Punkt 4 ist der wertvollste und lässt sich nicht erzwingen. Er kommt von selbst,
wenn das Projekt lange genug läuft.

---

## 7 · Risiken

| Risiko | Umgang |
| :--- | :--- |
| Upstream-Repo mit 6,8 GB | niemals klonen, nur einzelne Raw-Dateien abrufen. Rohdaten nicht ins eigene Repo |
| Schema-Drift der Quelle | nicht verhinderbar, aber erkennbar. Der Test dafür ist Teil der Story |
| Sensibles Thema | sachlicher Ton, keine Zuspitzung, keine Schuldzuweisung |
| Aussagegrenzen der Quelle | Herausgeber-Hinweise sichtbar in den Case, nicht in eine Fußnote |
| Scope-Drift Richtung Prognose | widerstehen. Der Wert liegt im Betrieb, nicht in einem weiteren Modell |
| Zeitbudget | Phasen 0 bis 3 zuerst. Ein Dashboard ohne belastbares Modell ist wertlos |

---

## 8 · Anschluss

Der Stack ist quellenunabhängig. Steht er einmal, kostet eine zweite Domäne
einen Bruchteil. Vorgemerkt:

- **SMARD Strommarkt** als Folgeprojekt, wegen Arbeitsmarkt-Anschluss in der
  Energiewirtschaft. Historie liegt fertig vor, kein Sammeln nötig.
- **VBB Nahverkehr** über das parallel laufende `vbb-realtime-archive`, sobald
  dort genug Historie entstanden ist.

Aus zwei Cases wird dann das stärkere Argument: eine Plattform, die mehrere
Domänen bedient.
