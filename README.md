# Bewertung von Stadtquartieren über Soziale Medien

## Projektzusammenfassung

**Motivation** \
Die Investitionsbank Schleswig-Holstein (IB.SH) unterstützt vielältige öffentliche und private Investitionsvorhaben in Schleswig-Holstein, insbesondere auch (sozialen) Wohnungsbau. Die IB.SH hat uns im Rahmen des Anwendungsprojekts im DataScience Master der FH Kiel beauftragt zu untersuchen, ob die Attraktivität von Wohnquartieren anhand von *Webgeflüster* in sozialen Medien beurteilt und ferner die Akzeptanz konkreter Förderungsmaßnahmen analysiert werden kann. 

**Ansatz** \
Zu Beginn haben wir uns mit verschiedenen sozialen Medienplattformen und ihren APIs beschäftigt. Einige APIs waren stark eingeschränkt oder gar nicht öffentlich verfügbar, z.B. müssen selbst öffentliche Facebook-Seiten oder -gruppen einem Zugriff auf ihre Inhalte zunächst zustimmen, während AirBnB seine API nur Businesspartnern zur Verfügung stellt, die zuvor einen Bewerbungsprozess durchlaufen haben. Andere Plattformen haben sich als unbrauchbar herausgestellt, da ihre Inhalte hauptsächlich visueller Natur sind (Pinterest, Instagram) oder für unsere Zwecke relevante Posts nur sehr selten abgesetzt werden (Tumblr). 
Twitter verfügt dagegen um ausreichend Relevanz und stellt eine gut gepflegte und umfangreiche [API](https://developer.twitter.com/en/docs/twitter-api) zur Verfügung, die es erlaubt nahezu unbegrenzt Tweets zu streamen. 
Allerdings finden sich gerade zu ländlicheren Gemeinden Schleswig-Holsteins oder selbst zu Kiel verhältnismäßig wenig Tweets, sodass wir uns zum Zwecke der Exploration auf einen Vergleich Hamburger Stadtteile fokussiert haben. 

Konkret haben wir einen Tweepy-Stream mithilfe einer virtuellen Maschine auf dem FH-Clusters aufgesetzt, welcher seit dem 17.11.21 mit wenigen Unterbrechungen läuft und Tweets sammelt, die Stadtteile oder dort zu findende öffentliche Plätze und Parks erwähnen. Tweepy ist eine Python-Bibliothek, die die Twitter API in benutzerfreundlichen Funktionen ansteuerbar macht. \
Die auf diese Weise bis zum Ende des Semesters gesammelten Tweets haben wir nochmals gefiltert (Ausschluss von Tweets zum Bahnverkehr / Tweets, die sich nicht eindeutig HH zuordnen lassen) und schließlich mithilfe eines vortrainierten neuronalen Netzwerks ([BERT](https://huggingface.co/docs/transformers/model_doc/bert?highlight=berttokenizer)) auf die Stimmungslage hin anaylsiert. Die daraus resultierenden Klassifikationen in positive, neutrale und negative Tweets haben wir für eine interaktive Karte genutzt, mithilfe derer die 104 Hamburger Stadtteile anhand verschiedener Metriken miteinander verglichen  sowie alle Tweets eines bestimmten Tages oder selbstgewähltem Zeitintervalls angezeigt werden können. 

**Ergebnis** \
[Ergebnis wie viele Tweets vor / nach Filtern Stand 18.12.] Es lassen sich erhebliche Unterschiede zwischen den Stadtteilen feststellen, betrachtet man die Tweetfrequenz. Während für Harburg noch 550 Tweets nach dem Filterungsprozess übrig blieben, finden sich für 47 Stadtteile jeweils weniger als 5 Tweets. Betrachtet man die Anzahl Tweets pro Einwohner\*innen, fällt Moorburg ins Auge. Viele Tweets beziehen sich auf das dort ansässige Kohlekraftwerk. Jenfeld, Hamm, Wilhelmsburg, Sternschanze und HafenCity verzeichnen die besten Verhältnisse zwischen positiven und negativen Tweets. Allerdings findet sich für Jenfeld nur ein positiver Tweet, selbst für die HafenCity sind es nur 14. Es lassen sich zwar gerade für letzteren Stadtteil wiederkehrende Themen identifizieren, die positiv aufgenommen werden (Wohnungsbau und Kultur wie Museen, Führungen und Kino), insgesamt ist die Datenlage aber nicht ausreichend genug, um belastbare Aussagen über die Attraktivität eines Stadtteils zu treffen oder gar Vergleiche anzustellen. 

Insgesamt erscheint eine Stimmungsanalyse mithilfe von Twitterdaten auf Ebene von Stadtteilen machbar, wenn über einen noch längeren Zeitraum Daten gesammt werden und eine sorgfältige Datenbereinigung erfolgt. Erstere Bedingung gilt erst recht, wenn Langzeitauswirkungen einzelner Förderprojekte untersucht werden sollen.
Für ländliche Landstriche mag dieses Vorgehen gar nicht praktikabel sein, da eine sinnvolle Datenmenge unter Umständen schlicht nicht erreicht werden kann. 

## Dokumentation

Dokumentation der Arbeitsschritte in Jupyter Notebooks:
- [Streaming](https://github.com/jaebjgh/application-project/blob/main/tweets_hh/TwitterAPI/Streaming/demo_streaming_tweepy.ipynb)
- [Filtern von Tweets und Stimmungsanalyse mit BERT](https://github.com/jaebjgh/application-project/blob/main/tweets_hh/Sentiment/tweet_processing.ipynb) 
- [Interaktive Karte von HH mit Tweets](https://nbviewer.org/github/jaebjgh/application-project/blob/main/Viz_Demo.ipynb)

Info: [nbviewer](https://blog.jupyter.org/rendering-notebooks-on-github-f7ac8736d686) ist ein Tool des Projekt Jupyter, um CSS / Javascript Elemente von Jupyter Notebooks im Webbrowser anzeigen zu können. Das betroffene Notebook liegt im selben Verzeichnis wie diese `README.md` und enthält die interaktive Karte von HH, die ansonsten nicht angezeigt werden könnte.


@ Julian Berger & Christina Hübers (12/2021)
