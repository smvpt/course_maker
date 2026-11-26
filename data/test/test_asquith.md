# Basic well log analysis for geologists Asquith, George B; Gibson

*OCR: mistral-ocr-latest  |  рисунки: sglang-qwen3-vl/qwen3-vl-32b-instruct  |  2026-08-26*

---

<!-- page 1 -->
DEPARTMENT OF THE ARMY
UNITED STATES OF AMERICA

AAPG Methods in Exploration Series, No. 16

# Second Edition

# Basic
# Well Log
# Analysis


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━

**Глубина:** интервал 7846–7852 (значения на оси: 7846, 7848, 7850, 7852). Направление оси глубины — вниз (глубина увеличивается вниз). Единицы измерения глубины на изображении явно не подписаны; значения характерны для глубины в футах.

**Дорожки (слева направо):**
1. **GR (API)** — шкала 0–200.
2. **C13, C24 (in)** — шкала 6–16 (дюймы).
3. **AZ (m/s)** — шкала 7.5–12 (м/с).
4. **Колонка глубин** — значения 7846, 7848, 7850, 7852.
5. **Панель имиджа 1: "Accelerometer Corrected"** (раздвижка стенки скважины, 360°, горизонтальная ось N → S → N).
6. **Панель имиджа 2: "Not Accelerometer Corrected"** (раздвижка стенки скважины, 360°, горизонтальная ось N → S → N).

**Кривые (поведение качественное):**
- **GR** — чёрная кривая. Низкие показания в кровле интервала, постепенный рост к отметке ~7850, затем спад.
- **C13** — зелёная кривая. Пик (раскрытие) в районе ~7847 (стрелка-указатель "C13").
- **C24** — синяя кривая. Пик (раскрытие) в районе ~7851 (стрелка-указатель "C24").
- **AZ** — красная кривая. Пик в районе ~7848 (стрелка-указатель "AZ").
- Стрелка-указатель "GR" направлена на чёрную кривую в районе ~7850.

**Цвет/проводимость на имиджах:** светлые зоны — высокоомные (резистивные), тёмные зоны — проводящие. Цветовая шкала на изображении не подписана.

**Интервальная таблица:**

| Интервал, фт | Поведение кривых | Имидж: подписанные особенности | Интерпретация |
|---|---|---|---|
| 7846–7848 | GR — низкие значения; C13 — пик (~7847); AZ — пик (~7848) | На скорректированной панели ("Accelerometer Corrected") — вертикальная тёмная (проводящая) полоса, подписанная **V1** | Вертикальное проводящее нарушение (интерпретация по подписи V1) |
| 7848–7850 | GR — постепенный рост; C13, C24 — небольшие вариации | На скорректированной панели — горизонтальная тёмная (проводящая) полоса, подписанная **S1** | Горизонтальная проводящая зона (граница/прослой) |
| 7850–7852 | GR — пик (~7850), затем спад; C24 — пик (~7851) | На нескорректированной панели ("Not Accelerometer Corrected") — горизонтальная тёмная полоса **S2** и вертикальная тёмная полоса **V2** | Те же типы нарушений, но без коррекции акселерометром |

**Сравнение панелей:** на панели "Not Accelerometer Corrected" тёмные полосы (V2, S2) имеют волнистый, искажённый вид по сравнению с прямолинейными полосами (V1, S1) на панели "Accelerometer Corrected". Это демонстрирует влияние коррекции акселерометром на геометрию и достоверность имиджевых данных.

**Подписи элементов имиджа (по расположению):**
- **V1** — вертикальная тёмная полоса на скорректированной панели, ~7846–7847.
- **S1** — горизонтальная тёмная полоса на скорректированной панели, ~7849–7850.
- **S2** — горизонтальная тёмная полоса на нескорректированной панели, ~7850–7851.
- **V2** — вертикальная тёмная полоса на нескорректированной панели, ~7851–7852.

KEYWORDS: каротажная диаграмма, ГИС, имидж скважины, коррекция акселерометра, гамма-каротаж, кавернометрия, акустический каротаж, трещиноватость, развёртка стенки скважины, проводящие зоны
----


By George Asquith and
Daniel Krygowski

(with sections by
Steven Henderson and
Neil Hurley

no. 30M
Inclusion
<!-- page 2 -->
Jorge Vega

Nov/2007

MARGARITA/V

# Basic Well Log Analysis

(Second Edition)

By

George Asquith and Daniel Krygowski

(with sections by Steven Henderson and Neil Hurley)

AAPG Methods in Exploration Series 16

Published by

The American Association of Petroleum Geologists

Tulsa, Oklahoma
<!-- page 3 -->
Copyright © 2004

By the American Association of Petroleum Geologists

All Rights Reserved

ISBN: 0-89181-667-4

AAPG grants permission for a single photocopy of an item from this publication for personal use.
Authorization for additional copies of items from this publication for personal or internal use is granted
by AAPG provided that the base fee of $3.50 per copy and $.50 per page is paid directly to the Copy-
right Clearance Center, 222 Rosewood Drive, Danvers, Massachusetts 01923 (phone: 978/750-8400).
Fees are subject to change.

AAPG Editor: Ernest A. Mancini

Geoscience Director: J. B. "Jack" Thomas

This publication is available from:

The AAPG Bookstore

P.O. Box 979

Tulsa, OK U.S.A. 74101-0979

Phone: 1-918-584-2555

or 1-800-364-AAPG (U.S.A. only)

Fax: 1-918-560-2652

Or 1-800-898-2274 (U.S.A. only)

E-mail: bookstore@aapg.org

www.aapg.org

The American Association of Petroleum Geologists (AAPG) does not endorse or recommend products or services that may
be cited, used, or discussed in AAPG publications or in presentations at events associated with AAPG.
<!-- page 4 -->
iii

# Table of Contents

|  Acknowledgements | v  |
| --- | --- |
|  About the Authors | vi  |
|  Preface (Second Edition) | viii  |
|  Preface (First Edition) | ix  |
|  **1: Basic Relationships of Well Log Interpretation** | 1  |
|  Introduction | 1  |
|  General | 1  |
|  Borehole Environment | 4  |
|  Invasion and Resistivity Profiles | 6  |
|  Basic Information Needed in Log Interpretation | 7  |
|  Common Equations | 8  |
|  Review | 10  |
|  **2: The Spontaneous Potential Log** | 21  |
|  General | 21  |
|  Formation Water Resistivity (R_{w}) Determination | 22  |
|  Shale Volume Calculation | 23  |
|  Review | 24  |
|  **3: Gamma Ray Log** | 31  |
|  General | 31  |
|  Shale Volume Calculation | 31  |
|  Spectral Gamma Ray Log | 32  |
|  Review | 32  |
|  **4: Porosity Logs** | 37  |
|  General | 37  |
|  Nuclear Magnetic Resonance Log | 37  |
|  Sonic Log | 37  |
|  Density Log | 39  |
|  Neutron Log | 40  |
|  Porosity Measurement Combinations | 41  |
|  Consistency in Lithology Prediction | 54  |
|  Review | 56  |
|  **5: Resistivity Logs** | 77  |
|  General | 77  |
|  Laterologs | 78  |
|  Induction Logs | 79  |
|  Flushed Zone Resistivity Logs | 81  |
|  Interpretation | 82  |
|  High Frequency (dielectric) Measurements | 82  |
|  Review | 86  |
|  **6: Magnetic Resonance Imaging Logs: by Steven Henderson** | 103  |
|  General | 103  |
|  Limitations of Conventional Logs | 103  |
|  Nuclear Magnetic Resonance Applications | 103  |
|  Principle of NMR Logging | 103  |
<!-- page 5 -->
iv

|  Pore Size and Fluid Moveability | 104  |
| --- | --- |
|  NMR Permeability | 104  |
|  Direct Hydrocarbon Typing | 105  |
|  NMR Applications in Carbonates | 106  |
|  Review | 106  |
|  **7: Log Interpretation** | 115  |
|  General | 115  |
|  Scanning the Logs: A Reconnaissance Technique | 115  |
|  Archie Water Saturations: S_{w} and S_{xo} | 115  |
|  Quick-look Methods | 117  |
|  Bulk Volume Water | 120  |
|  Saturation Crossplots | 121  |
|  Permeability From Logs | 123  |
|  Shaly Sand Analysis | 125  |
|  Review | 128  |
|  **8: Petrophysical Techniques** | 137  |
|  General | 137  |
|  Neutron-Density Lithology Plot | 137  |
|  Neutron-Sonic Lithology Plot | 137  |
|  Density-Sonic Lithology Plot | 138  |
|  M-N Lithology Plot | 138  |
|  MID (Matrix Identification) Lithology Plot (ρ_{maa} vs. Δt_{maa}) | 138  |
|  MID (Matrix Identification) Lithology Plot (U_{maa} vs. ρ_{maa}) | 140  |
|  Alpha Mapping From the SP Log | 141  |
|  Clean Sand or Carbonate Maps From the Gamma Ray Log | 141  |
|  Rock Typing and Facies Mapping | 141  |
|  Review | 142  |
|  **9: Borehole Imaging: by Neil Hurley** | 151  |
|  General | 151  |
|  Electrical Borehole Images | 151  |
|  Acoustic Borehole Images | 152  |
|  Downhole Video Images | 153  |
|  Emerging Technologies: Other Borehole Images | 154  |
|  Borehole Image Interpretation | 154  |
|  Review | 156  |
|  **10: Interpretation Case Studies** | 165  |
|  1: Pennsylvanian Atoka Sandstone, Permian Basin, U.S.A. | 168  |
|  2: Mississippian Mission Canyon Formation, Williston Basin, U.S.A. | 180  |
|  3: Eocene Wilcox Sandstone, Gulf Coast, U.S.A. | 195  |
|  4: Pennsylvanian Upper Morrow Sandstone, Anadarko Basin, U.S.A. | 205  |
|  5: Cretaceous Pictured Cliffs Sandstone, San Juan Basin, U.S.A. | 213  |
|  6: Ordovician-Silurian Chimneyhill Subgroup, Hunton Group, Anadarko Basin, U.S.A. | 224  |
|  7: Pennsylvanian Canyon Limestone, New Mexico, U.S.A. | 235  |
|  **References** | 240  |
<!-- page 6 -->
V

# Acknowledgements

The idea for this revision came from a discussion at an AAPG Annual Meeting, between George Asquith, members of the AAPG Staff, and myself. At the time, George and I had been teaching the AAPG Basic Well Logging short course for about a decade. We all agreed that a revision of Basic Well Log Analysis for Geologists was in order, to capture the technological advancements in well logging that had been made since the book's publication.

George suggested that I start the revisions, to provide a different perspective on his original efforts. Our collaboration began in that way, with the revisions as a starting place for a continuing dialog which resulted in this edition. My sincere thanks and appreciation go to George for his confidence in my abilities, his willingness to put all of his work on the table, and for his efforts as the managing partner in this endeavor.

Our thanks to Bob Cluff who critically reviewed the original book at the beginning of this project. His comments were taken to heart. The review efforts of Rick Erickson and Gary Stewart are to be commended. Not only did they review the text, but they also attacked the case study data in great detail, comparing log displays with printed log values and final results. A special thanks goes out to Jack Thomas at AAPG who has shepherded this process in its final stages.

Many charts and figures used in the text were provided by Baker Atlas, Schlumberger Oilfield Services, and Halliburton. Our thanks for their willingness to share their information with this project.

The log displays from the original book were scanned by Neuralog and provided for the project. Neuralog software converted those images to digital data for display and interpretive processing. The raw data were stored, processed, and displayed using software from Landmark Graphics (a Halliburton Company). The PetroWorks and OpenWorks products were used for this purpose. The log plots and crossplots in the text were produced using PetroWorks software. Our thanks to both companies for providing the means to efficiently convert this work from the paper realm to the digital realm.

And finally a very special thank you to my wife, Monica Krygowski, who has supported me in an effort that took much longer than originally anticipated. Her comments, positive outlook, and encouragement are an integral part of this publication.

Daniel A. Krygowski
Austin, Texas, U.S.A.
October, 2003
<!-- page 7 -->
vi

# About the Authors

## GEORGE B. ASQUITH

George Asquith holds the Pevehouse Chair of Petroleum Geology and is Professor of Geosciences and Director of the Center for Applied Petrophysical and Reservoir Studies at Texas Tech University. He received his B.S. (honors) in geology with a minor in mathematics from Texas Tech and his M.S. and Ph.D. from the University of Wisconsin-Madison with a minor in geophysics. His 25 years of petroleum industry experience include work as research geologist, Atlantic-Richfield Co.; staff geologist, ALPAR Resources; chief geologist, Search Drilling Co.; district geologist, Pioneer Production Corp.; and project leader, Mesa Limited Partnership. His industry projects have included the determination of the reservoir architecture and remaining gas reserves in the Hugoton and West Panhandle fields and exploration and reservoir characterization of selected reservoirs from the Gulf Coast (onshore and offshore), Permian, Alberta, San Juan, Williston, Arkoma, Cooper (Australia), Neiva (Colombia), Maracaibo (Venezuela), and Anadarko basins.

He has authored 123 publications including 5 books in the fields of petrophysics, computer geology, and carbonate and clastic sedimentation and petrology. His book, *Basic Well Log Analysis for Geologists* won the AAPG best book award in 1984 and is the top selling book in the history of AAPG. During 1991-1992, *Log Evaluation of Shaly Sandstones: A Practical Guide* was one of the top 3 selling AAPG publications. His numerous awards include the Distinguished Service and Best Paper Awards from the Society of Professional Well Log Analysts (1994); Leverson Award for best paper at the AAPG Southwest Section meeting (1996); AAPG Distinguished Educator Award (1997); Educator of the Year Award presented by the AAPG Southwest Section (1999); West Texas Geological Society Distinguished Service Award (1999); and the Monroe Cheney Science Award from the Southwest Section of AAPG and Dallas Geological Society (2001).

He has served as Distinguished Lecturer for the Society of Professional Well Log Analysts (1991-1992 and 1994-1995), lecturer for the AAPG Subsurface Carbonate Depositional Modeling school (1980-1986), and is currently lecturer and science advisor for the AAPG Basic Well Log Analysis, Carbonate Well Log Analysis, and Shaly Sand Well Log Analysis schools (1982-present).

Dr. Asquith’s research interests include the documentation and quantitative mapping of relationships between petrophysical responses and depositional and diagenetic lithofacies, the petrophysics of carbonate and shaly-sand reservoirs, and the application of computers to petrophysical analysis.

## DANIEL A. KRYGOWSKI

Daniel Krygowski is part of the software development staff in the Austin, Texas, office of Landmark Graphics (a Halliburton company). As a Domain Expert in the research and development organization, he is focused on the usability, user interface, and petrophysical technology content of PetroWorks and other software products. He received a B.A. in physics from the State University of New York College at Geneseo and M.S. and Ph.D. degrees in geophysics from the Colorado School of Mines. Previous to his employment at Landmark, he held a number of technical and management positions in petrophysics and software development at Cities Service Company (now Occidental) and Atlantic Richfield Company (now BP).

Dan is a member of the AAPG, Society of Petrophysicists and Well Log Analysts, Society of Petroleum Engineers, and Society of Exploration Geophysicists. He teaches the AAPG Basic Well Log Analysis continuing education course with George Asquith.
<!-- page 8 -->
vii

## NEIL F. HURLEY

Neil Hurley received B.S. degrees in geology and petroleum engineering from the University of Southern California in 1976. He received his M.S. degree in geology from the University of Wisconsin-Madison in 1978. His thesis work involved stratigraphic studies in the Permian reef complex of the Guadalupe Mountains, New Mexico. From 1978 through 1982 he worked as an exploration and research geologist for Conoco in Denver, Colorado; Lafayette, Louisiana; and Ponca City, Oklahoma. In 1982, he entered the University of Michigan as an Exxon Teaching Fellow. In 1986, he received his Ph.D. degree, doing his research on the geology of Devonian reefs in Western Australia. From 1986 to 1996, he worked in reservoir characterization at Marathon's Petroleum Technology Center in Littleton, Colorado. In 1991-92, he toured the U.S. as an AAPG Distinguished Lecturer. In 1996, Neil Hurley was awarded the Charles Boettcher Distinguished Chair in Petroleum Geology, and he is now a Professor in the Department of Geology and Geological Engineering at the Colorado School of Mines. At CSM, he teaches beginning and advanced log analysis, carbonate geology, field seminars, and integrated exploration courses. He has been the Editor for AAPG, and he is a member of the Society of Professional Well Log Analysts, Society of Petroleum Engineers, Society for Sedimentary Geology, Society of Independent Earth Scientists, International Association of Sedimentologists, Society of Exploration Geophysicists, European Association of Geoscientists and Engineers, Geological Society of America, and Rocky Mountain Association of Geologists. His specialties include carbonate sedimentology and diagenesis, fractured reservoirs, formation evaluation, borehole-imaging logs, and horizontal drilling.

## STEVE HENDERSON

Steve Henderson is a technical instructor at the Fort Worth Training Center of Halliburton Energy Services where he is involved with the training of wireline engineers in measurement physics, field operations, and log analysis. He received his B.S. in geological sciences from The University of Texas at Austin and M.S. and Ph.D. in geosciences from Texas Tech University. His research interests include carbonate diagenesis, clay mineralogy, and their implications in well log analysis. He has authored several published technical articles on the Permian San Andres and Pennsylvanian Cross Cut formations of west Texas, and he is a member of the AAPG, Society for Sedimentary Geology, and Society of Petrophysicists and Well Log Analysts.
<!-- page 9 -->
viii

# Preface to Basic Well Log Analysis

## (Second Edition)

Formation evaluation (or well log analysis or petrophysics) is at the intersection of a number of disciplines, including, but not limited to, geology, geophysics, and reservoir engineering. Each discipline that encounters and uses well log data does so from its own perspective. In doing so, each discipline sometimes uses the data without a full understanding of how the measurements are made. That incomplete understanding can encompass the processing of the actual measurements into the raw data provided by the data logging companies and to the interpretation methods that convert that data into usable information about the subsurface. It is this incomplete understanding of well log data that commonly produces conflicting interpretations from different sources, when the goal should be a single cohesive model of the subsurface that can be consistently applied by all disciplines.

This book is a revision of George Asquith’s *Basic Well Log Analysis for Geologists*, of one of the most popular books published by the American Association of Petroleum Geologists (AAPG). It does not claim to provide all information about well logs from all perspectives. Like the original publication, it remains focused on the interpretation of basic, or common openhole logging measurements. It also remains focused on the traditional interpretive goals of formation porosity, fluid saturation, and lithology.

The impetus for this revised text was a perception that an update was needed to address the technologies that had been introduced in the two decades since the original publication. We have endeavored to do so, from inclusion of the photoelectric effect ($P_e$ or PEF) curve of the newest-generation density tools, to chapters specifically addressing nuclear magnetic resonance (NMR) logging (by Steven Henderson) and borehole imaging (by Neil Hurley).

Accompanying this book is a CD, which you will find attached to the inside back cover. The CD contains 10 data-based files so that readers of this book will be able to practice the techniques described in the book.

The authors hope that this introductory text will lead the readers to seek other sources on well logs and well log interpretation, which will lead to a deeper and broader understanding of formation evaluation. George Asquith’s Preface to the original publication (reproduced in this edition) still rings true; an understanding of the data and the discipline still comes primarily from the hands-on application of the information and methods shown here, and in other sources. If you have read this far, take the time to read that Preface as well.

There are many resources for petrophysical data. We hesitate to list specific sources here, especially online sources as websites can appear, change, and disappear quickly. Two good (and stable) sources for information (electronic and hardcopy) are the Society of Petrophysicists and Well Log Analysts (SPWLA) and the American Association of Petroleum Geologists (AAPG).
<!-- page 10 -->
ix

# Preface to Basic Well Log Analysis for Geologists

This book is a basic introduction to open hole logging.

Study of the properties of rocks by petrophysical techniques using electric, nuclear, and acoustical sources is as important to a geologist as the study of rock properties by more conventional means using optical, x-ray, and chemical methods. Nevertheless, despite the importance of petrophysics, it is frequently underutilized by many geologists who are either intimidated by logging terminology and mathematics, or who accept the premise that an in-depth knowledge of logging is only marginally useful to their science because, they feel, it more properly belongs in the province of the log analyst or engineer.

The enormous importance of logging dictates that as geologists, we put aside old notions and apply ourselves diligently to learning log interpretation. The rewards are obvious; in fact, no less than achieving an understanding of the ancient record hangs in the balance. And, it is likely that the success or failure of an exploration program may hinge on a geologist's logging expertise.

In the interest of conciseness, and so that logs used most often in petroleum exploration are thoroughly discussed, the text is restricted to open hole logs. I hope that the reader initiates his or her own study of other log types which are beyond the scope of this book.

Unfortunately, learning about open hole logging requires more of the reader than a light skimming of the text's material. The plain truth is that a great deal of hard work, including memorizing log terminology, awaits the serious student; and even then, a facility with logs develops only after plenty of real-life experience. The intent here is simply to provide a foundation of knowledge which can be built upon later. Consequently, many exceptions to rules are left to more advanced books.

It is quite possible that some colleagues will raise objections about the lack of time devoted to tool theory; they may also comment on the paucity of qualifying statements in the text. These objections are understood and indeed there may be disagreements about what constitutes over-simplification. In defense of brevity, it should be pointed out that the surfeit of information available on petrophysics often discourages all but the most ardent beginner. Certainly, many of the difficult decisions which had to be faced in preparing the manuscript dealt with selecting information judged indispensable at an elementary level.

Many in the audience will note frequent references to a book by Douglas Hilchie, Golden, Colorado, entitled *Applied Open Hole Log Interpretation* (1978). For those who are interested in expanding their knowledged of logs, his book will be a great help. Another helpful book is *The Glossary of Terms and Expressions Used in Well Logging*, The Society of Professional Well Log Analysts (1975), which explains the meaning of logging terms by extended definitions.

Finally, a last word — a substantial effort was expended to ensure that a minimum number of errors would appear in the text. However, given the nature of the subject and the almost infinite possibility for mistakes, there may be slip-ups, regardless; hopefully they will not be too serious.

George B. Asquith

Pioneer Production Corporation

Amarillo, Texas

October, 1982
<!-- page 11 -->

<!-- page 12 -->
1

Asquith, G., and D. Krygowski, 2004, Basic Relationships of Well Log Interpretation, in G. Asquith and D. Krygowski, Basic Well Log Analysis: AAPG Methods in Exploration 16, p. 1-20.

# Basic Relationships of Well Log Interpretation

## INTRODUCTION

This chapter provides a general introduction to well logging principles and methods that will be used throughout the book. Succeeding chapters (2 through 6) introduce the reader to specific log types. The text discusses how different log types measure various properties in the wellbore and surrounding formations, what factors affect these measurements, where on a standard log display a particular curve is recorded, and how interpreted information is obtained from the logs using both charts and mathematical formulas. Unlike many other logging texts, the logging tools are grouped according to their primary interpretation target, rather than their underlying measurement physics.

Spontaneous potential (SP) and gamma ray logs are discussed first, as their primary use is correlation and their primary interpretive target is gross lithology (the distinction between reservoir and nonreservoir). The porosity logs (i.e., sonic, density, and neutron logs) are covered next, then the resistivity logs. Nuclear magnetic-resonance logs, although they provide porosity (among other quantities of interest), are presented after resistivity logs. This is due in part to their recent arrival and to their relative absence in historical data archives.

The final four chapters again deal with interpretation of the data, this time in detail with example problems and their solutions. These chapters bring the introductory material of Chapter 1 together with the specific measurement information and are intended to provide a coherent view of the interpretation process. The reader is encouraged to work the examples to gain familiarity with the interpretation techniques and to begin to understand the limitations on interpretation that are present due to the nature of subsurface information.

The use of charts and simple calculations throughout the text, rather than the use of petrophysical com

computer software, is intentional. It is only through experience with such manual methods that the reader can gain an appreciation for the effects of parameters on the calculations, and gain a better understanding of the accuracy and precision of the techniques discussed here.

When the first edition of this book was published, virtually all well-logging data were acquired through the use of wireline-conveyed tools; that is, logging tools lowered in the borehole on a 7-conductor cable over which power, operating instructions, and data were sent. Since the mid-1980s, a second formation-evaluation technique, measurement while drilling (MWD) or logging while drilling (LWD), has developed. In this method, the logging sensors are imbedded in the thick-walled drill collars used at the bottom of the drill string (near the bit), and measurement of formation properties is done continuously during the drilling process (hence the name, MWD). Initially, MWD logging technology borrowed heavily from wireline technology, with the goal being to produce LWD measurements comparable to wireline measurements. As LWD technology has progressed, sensor design and other features of LWD have been incorporated back into wireline technology, for the improvement of those measurements.

Unless specifically noted in the text, the interpretation of borehole data is the same irrespective of the source of the data, either wireline or LWD sensors and measurement systems. The techniques shown here are applicable to both data sources and can even be extended to incorporate equivalent core measurements.

## GENERAL

As logging tools and interpretive methods are developing in accuracy and sophistication, they are playing an expanded role in the geological decision-

1
<!-- page 13 -->
2

ASQUITH AND KRYGOWSKI

making process. Today, petrophysical log interpretation is one of the most useful and important tools available to a petroleum geologist.

Besides their traditional use in exploration to correlate zones and to assist with structure and isopach mapping, logs help define physical rock characteristics such as lithology, porosity, pore geometry, and permeability. Logging data are used to identify productive zones, to determine depth and thickness of zones, to distinguish between oil, gas, or water in a reservoir, and to estimate hydrocarbon reserves. Also, geologic maps developed from log interpretation help with determining facies relationships and drilling locations. Increasingly, the importance of petrophysics and well-log analysis is becoming more evident as more attention is being devoted to the ongoing management of reservoirs. The industry is realizing the importance of detailed petrophysical analyses, based on the details of the available data in monitoring, simulating, and enhancing reservoir performance to maximize the return on investment.

Of the various types of logs, the ones used most frequently in hydrocarbon exploration are called open-hole logs. The name open hole is applied because these logs are recorded in the uncased portion of the wellbore. All the different types of logs and their curves discussed in this text are of this type.

A geologist's first exposure to log interpretation can be a frustrating experience. This is not only because of its lengthy and unfamiliar terminology, but also because knowledge of many parameters, concepts, and measurements is needed before an understanding of the logging process is possible.

Perhaps the best way to begin a study of logging is by introducing the reader to some of the basic concepts of well log analysis. Remember that a borehole represents a dynamic system; that fluid used in the drilling of a well affects the rock surrounding the borehole and, therefore, log measurements. In addition, the rock surrounding the borehole has certain properties that affect the movement of fluids into and out of it.

The two primary parameters determined from well log measurements are porosity and the fraction of pore space filled with hydrocarbons (i.e., hydrocarbon saturation). The parameters of log interpretation are determined directly or inferred indirectly and are measured by one of three general types of logs:

- electrical
- nuclear
- acoustic or sonic logs

The names refer to the sources used to obtain the measurements. The different sources create records (logs), which contain one or more curves related to

some property in the rock surrounding the wellbore (see Society of Professional Well Log Analysts, 1984). For the reader unfamiliar with petrophysical logging, some confusion may develop over the use of the word log. In common usage, the word log may refer to a particular curve, a suite or group of curves, the physical (paper) record of the measurements, a logging tool (sonde), or the process of logging.

Rock properties or characteristics that affect logging measurements are: porosity, lithology, mineralogy, permeability, and water saturation. Additionally, the resistivity of the rock is important because it is directly measured and is an essential part in the interpretation process. It is essential that the reader understand these properties and the concepts they represent before proceeding with a study of log interpretation.

### Porosity

Porosity can be defined as the ratio of voids to the total volume of rock. It is represented as a decimal fraction or as a percentage and is usually represented by the Greek letter phi, $\phi$.

$$\text{porosity, } \phi = \frac{\text{volume of pores}}{\text{total volume of rock}} \tag{1.1}$$

The amount of internal space or voids in a given volume of rock is a measure of the amount of fluid a rock will hold. This is illustrated by Equation 1.1 and is called the total porosity. The amount of void space that is interconnected, and thus able to transmit fluids, is called effective porosity. Isolated pores and pore volume occupied by adsorbed water are excluded from a definition of effective porosity but are included in the definition of total porosity.

### Lithology and Mineralogy

In well-log analysis, the terms lithology and mineralogy are used with some ambiguity. Lithology is often used to describe the solid (matrix) portion of the rock, generally in the context of a description of the primary mineralogy of the rock (e.g., a sandstone as a description of a rock composed primarily of quartz grains, or a limestone composed primarily of calcium carbonate). In the early days of log interpretation (with limited measurements), this was usually a sufficient description. Probably the first instances of lithologic effects on the logs were observed in shaly or clay-containing sandstones. With the advent of multiple porosity measurements and the development of more detailed interpretive methods, it has become possible to estimate the primary solid constituents, normally as a mineral pair or triad.
<!-- page 14 -->
Basic Relationships of Well Log Interpretation

3

The literature has tended to follow the improved understanding of the constitution of the solid part of the formations of interest, with most current literature referring to the determination of mineralogy instead of lithology. When one considers the physics of logging measurements, the ambiguity continues. Some measurements (primarily nuclear) are made as the result of molecular-level interactions between the formation and the logging tool. These might be considered as being affected by the formation's mineralogy. Others, especially the acoustic measurements, interact with the formation on a bulk or framework level, and could be considered to be more affected by lithology (S. L. Morriss, 1999, personal communication).

The ambiguity between lithology and mineralogy is best seen in porosity crossplots which, through time, have moved from estimating lithology to estimating mineralogy, while the underlying measurements and interpretive techniques have remained essentially the same.

As noted above, the first lithologic effects were probably due to the presence of clays and shales in formations of interest. One parameter that has been used consistently to account for these effects has been shale volume. As our understanding of geological processes matured, it became understood that shale and clay were different, and that shaly sands were usually not just sands with shales mixed in, but sands that contained clays — clays that could be very different from the clays present in the shales near those sands of interest. Again, the literature and our interpretive techniques often use the terms shale volume and clay volume interchangeably. In this text, shale volume will be used preferentially because most of the interpretive techniques in which the volumes are used derive those volumes from the properties of nearby shales.

## Permeability

Permeability is the ability of a rock to transmit fluids. It is related to porosity but is not always dependent upon it. Permeability is controlled by the size of the connecting passages (pore throats or capillaries) between pores. It is measured in darcys or millidarcys (md) and is represented by the symbol K. The ability of a rock to transmit a single fluid, when it is completely saturated with that fluid, is called absolute permeability. Effective permeability refers to the ability of the rock to transmit one fluid in the presence of another fluid when the two fluids are immiscible.

Formation water (connate water in the formation) held by capillary pressure in the pores of a rock serves to inhibit the transmission of hydrocarbons. Stated dif-

ferently, formation water takes up space both in pores and in the connecting passages between pores. As a consequence, it may block or otherwise reduce the ability of other fluids to move through the rock.

Relative permeability is the ratio between effective permeability of a fluid at partial saturation and the permeability at 100% saturation (absolute permeability). When relative permeability of a formation's water is zero, the formation produces water-free hydrocarbons (i.e., the relative permeability to hydrocarbons is 100%). With increasing relative permeabilities to water, the formation produces increasing amounts of water relative to hydrocarbons.

## Water Saturation

Water saturation is the amount of pore volume in a rock that is occupied by formation water. It is represented as a decimal fraction or as a percentage and has the symbol $S_w$.

$$\text{water saturation, } S_w = \frac{\text{formation water occupying pores}}{\text{total pore space in the rock}} \quad 1.2$$

Although hydrocarbon saturation is the quantity of interest, water saturation is usually used because of its direct calculation in equations such as Archie's equation, discussed in a later section in this chapter. Hydrocarbon saturation is usually determined by the difference between unity and water saturation:

$$S_h = 1 - S_w \tag{1.3}$$

Irreducible water saturation or $S_w$ irr is the term used to describe the water saturation at which all the water is adsorbed on the grains in a rock or is held in the capillaries by capillary pressure. At irreducible water saturation, water does not move and the relative permeability to water is zero.

## Resistivity

Resistivity is the rock property on which the entire science of logging first developed. Resistivity is the inherent property of all materials, regardless of their shape and size, to resist the flow of an electric current. Different materials have different abilities to resist the flow of electricity.

While the resistance of a material depends on its shape and dimensions, the resistivity is an invariant property; the reciprocal of resistivity is conductivity. In log interpretation, the hydrocarbons, the rock, and the fresh water of the formation are all assumed to act
<!-- page 15 -->
4

ASQUITH AND KRYGOWSKI

as insulators and are, therefore, nonconductive (or at least very highly resistive) to electric current flow. Salt water, however, is a conductor and has a low resistivity. The measurement of resistivity is then a measurement, albeit indirect, of the amount (and salinity) of the formation water. The unit of measure used for the conductor is a cube of the formation, one meter on each edge. The measured units are ohm-meters²/meter and are called ohm-meters.

$$R = \frac{r \times A}{L} \tag{1.4}$$

where:

$R =$ resistivity (ohm-m)

$r =$ resistance (ohms)

$A =$ cross-sectional area of substance being measured (m²)

$L =$ length of substance being measured (m)

Resistivity is a basic measurement of a reservoir's fluid saturation and is a function of porosity, type of fluid (i.e., hydrocarbons, salt water, or fresh water), amount of fluid, and type of rock. Because both the rock and hydrocarbons act as insulators but salt water is conductive, resistivity measurements made by logging tools can be used to detect hydrocarbons and estimate the porosity of a reservoir. During the drilling of a well, fluids move into porous and permeable formations surrounding a borehole, so resistivity measurements recorded at different distances into a formation often have different values. Resistivity is measured by electric logs, commonly known (in the West) as laterologs and induction logs.

Conrad Schlumberger in 1912 began the first experiments which led, eventually, to the development of modern-day petrophysical logs. The first electric log was run September 5, 1927, by H. G. Doll in Alsace-Lorraine, France. In 1941, G. E. Archie with Shell Oil Company presented a paper to the AIME in Dallas, Texas, which set forth the concepts used as a basis for modern quantitative log interpretation (Archie, 1942).

Archie's experiments showed that the resistivity of a water-filled formation ($R_o$) could be related to the resistivity of the water ($R_w$) filling the formation through a constant called the formation resistivity factor ($F$):

$$R_o = F \times R_w \tag{1.5}$$

Archie's experiments also revealed that the formation factor ($F$) could be related to the porosity of the formation by the following formula:

$$F = \frac{a}{\phi^m} \tag{1.6}$$

where $m$ is the cementation exponent whose value varies with grain size, grain-size distribution, and the complexity of the paths between pores (tortuosity), and $a$ is the tortuosity factor. The higher the tortuosity of the formation, the higher the value of m. The tortuosity factor ($a$) is commonly set to 1.0, but is allowed to vary by some petrophysicists.

Water saturation ($S_w$) is determined from the water-filled resistivity ($R_o$) and the actual (true) formation resistivity ($R_f$) by the following relationship:

$$S_w = \left(\frac{R_o}{R_f}\right)^{\frac{1}{n}} \tag{1.7}$$

where $n$ is the saturation exponent, whose value typically varies from 1.8 to 2.5 but is most commonly assumed to be 2.

By combining equations 1.6 and 1.7, the water-saturation formula can be rewritten in the following form:

$$S_w = \left(\frac{F \times R_w}{R_f}\right)^{\frac{1}{n}} \tag{1.8}$$

This is the formula that is most commonly referred to as the Archie equation for water saturation ($S_w$). All present methods of interpretation involving resistivity curves are derived from this equation. In its most general form, Archie's equation becomes:

$$S_w = \left(\frac{a \times R_w}{R_f \times \phi^m}\right)^{\frac{1}{n}} \tag{1.9}$$

Table 1.1 illustrates the range of values for $a$ and $m$. In first-pass or reconnaissance-level interpretations, or where there is no knowledge of the local parameters, the following values can be used to achieve an initial estimate of water saturation:

$$a = 1.0; m = n = 2.0$$

Now that the reader is introduced to some of the basic concepts of well log interpretation, our discussion can continue in more detail about the factors that affect logging measurements.

### BOREHOLE ENVIRONMENT

Where a hole is drilled into a formation, the rock plus the fluids in it (the rock-fluid system) are altered in the vicinity of the borehole. The borehole and the rock surrounding it are contaminated by the drilling mud, which affects logging measurements. Figure 1.1
<!-- page 16 -->
Basic Relationships of Well Log Interpretation

5

Table 1.1. Different coefficients and exponents used to calculate formation factor (F). (Modified after Asquith, 1980.)

|  a: Tortuosity factor | m: Cementation exponent | Comments  |
| --- | --- | --- |
|  1.0 | 2.0 | Carbonates^{1}  |
|  0.81 | 2.0 | Consolidated sandstones^{1}  |
|  0.62 | 2.15 | Unconsolidated sands (Humble formula)^{1}  |
|  1.45 | 1.54 | Average sands (after Carothers, 1968)  |
|  1.65 | 1.33 | Shaly sands (after Carothers, 1968)  |
|  1.45 | 1.70 | Calcareous sands (after Carothers, 1968)  |
|  0.85 | 2.14 | Carbonates (after Carothers, 1968)  |
|  2.45 | 1.08 | Pliocene sands, southern California (after Carothers and Porter, 1970)  |
|  1.97 | 1.29 | Miocene sands, Texas–Louisiana Gulf Coast (after Carothers and Porter, 1970)  |
|  1.0 | φ^{(2.05-φ)} | Clean granular formations (after Sethi, 1979)  |

$^{1}$Most commonly used

is a schematic illustration of a porous and permeable formation that is penetrated by a borehole filled with drilling mud.

Some of the more important symbols shown in Figure 1.1 are:

### Hole Diameter ($d_h$)

The borehole size is determined by the outside diameter of the drill bit. But, the diameter of the borehole may be

- larger than the bit size because of washout and/or collapse of shale and poorly cemented porous rocks, or
- smaller than the bit size because of a build up of mud cake on porous and permeable formations (Figure 1.1).

Common borehole sizes normally vary from 7-7/8 in. to 12 in., and modern logging tools are designed to operate within these size ranges. The size of the borehole is measured by a caliper log.

### Drilling mud Resistivity ($R_m$)

Today, most wells are drilled with rotary bits and the use of a special fluid, called drilling mud, as a circulating fluid. The mud helps remove cuttings from the wellbore, lubricate and cool the drill bit, and maintain an excess of borehole pressure over formation pressure. The excess of borehole pressure over forma-

tion pressure prevents blowouts. The density of the mud is usually kept high enough so that hydrostatic pressure in the mud column is greater than formation pressure. This pressure difference forces some of the drilling fluid to invade porous and permeable formations. As invasion occurs, many of the solid particles (i.e., clay minerals from the drilling mud) are trapped on the side of the borehole and form mud cake (having a resistivity of $R_{mc}$; Figure 1.1). Fluid that filters into the formation during invasion is called mud filtrate (with a resistivity of $R_{mf}$; Figure 1.1). The resistivity values for drilling mud, mud cake, and mud filtrate are recorded on a log's header (Figure 1.2), and are used in interpretation.

### Invaded Zone

The zone in which much of the original fluid is replaced by mud filtrate is called the invaded zone. It consists of a flushed zone (of resistivity $R_{xo}$) and a transition or annulus zone (of resistivity $R_i$). The flushed zone occurs close to the borehole (Figure 1.1) where the mud filtrate has almost completely flushed out a formation's hydrocarbons and/or water ($R_w$). The transition or annulus zone, where a formation's fluids and mud filtrate are mixed, occurs between the flushed zone and the uninvaded zone (of resistivity $R_t$). The uninvaded zone is defined as the area beyond the invaded zone where a formation's fluids are uncontaminated by mud filtrate.

The depth of mud-filtrate invasion into the invaded
<!-- page 17 -->
6

ASQUITH AND KRYGOWSKI

zone is referred to as diameter of invasion ($d_i$ and $d_j$; Figure 1.1). The diameter of invasion is measured in inches or expressed as a ratio: $d_j/d_h$ (where $d_h$ represents the borehole diameter). The amount of invasion that takes place is dependent upon the permeability of the mud cake and not upon the porosity of the rock. In general, an equal volume of mud filtrate can invade low-porosity and high-porosity rocks if the drilling muds have equal amounts of solid particles. The solid particles in the drilling muds coalesce and form an impermeable mud cake. The mud cake then acts as a barrier to further invasion. Because an equal volume of fluid can be invaded before an impermeable mud-cake barrier forms, the diameter of invasion is greatest in low-porosity rocks. This occurs because low-porosity rocks have less storage capacity or pore volume to fill with the invading fluid, and, as a result, pores throughout a greater volume of rock are affected. General invasion diameters in permeable formations are

$d_j/d_h = 2$, for high-porosity rocks;

$d_j/d_h = 5$, for intermediate-porosity rocks; and

$d_j/d_h = 10$, for low-porosity rocks.

### Flushed zone Resistivity ($R_{xo}$)

The flushed zone extends only a few inches from the wellbore and is part of the invaded zone. If invasion is deep or moderate, most often the flushed zone is completely cleared of its formation water by mud filtrate (of resistivity $R_{mf}$). When oil is present in the flushed zone, the degree of flushing by mud filtrate can be determined from the difference between water saturations in the flushed ($S_{xo}$) zone and the uninvaded ($S_w$) zone (Figure 1.1). Usually, about 70% to 95% of the oil is flushed out; the remaining oil is called residual oil [$S_{ro} = (1.0 - S_{xo})$, where $S_{ro}$ is the residual oil saturation, (ROS)].

### Uninvaded zone Resistivity ($R_t$)

The uninvaded zone is located beyond the invaded zone (Figure 1.1). Pores in the uninvaded zone are uncontaminated by mud filtrate; instead, they are saturated with formation water ($R_w$), oil, and/or gas.

Even in hydrocarbon-bearing reservoirs, there is always a layer of formation water on grain surfaces. Water saturation ($S_w$; Figure 1.1) of the uninvaded zone is an important factor in reservoir evaluation because, by using water saturation data, a geologist can determine a reservoir's hydrocarbon saturation. Equation 1.3 expresses the calculation and is repeated here:

$$S_h = 1 - S_w$$

where:

$S_h$ = hydrocarbon saturation (i.e., the fraction of pore volume filled with hydrocarbons).

$S_w$ = water saturation of the uninvaded zone (i.e., the fraction of pore volume filled with water).

The ratio of the uninvaded zone's water saturation ($S_w$) to the flushed zone's water saturation ($S_{xo}$) is an index of hydrocarbon moveability.

### INVASION AND RESISTIVITY PROFILES

Invasion and resistivity profiles are diagrammatic, theoretical, cross-sectional views of subsurface conditions moving away from the borehole and into a formation. They illustrate the horizontal distributions of the invaded and uninvaded zones and their corresponding relative resistivities. There are three commonly recognized invasion profiles:

- step
- transition
- annulus

These three invasion profiles are illustrated in Figure 1.3.

The step profile has a cylindrical geometry with an invasion diameter equal to $d_j$. Shallow-reading resistivity logging tools read the resistivity of the invaded zone ($R_i$), while deeper reading resistivity logging tools read true resistivity of the uninvaded zone ($R_t$).

The transition profile also has a cylindrical geometry with two invasion diameters: $d_i$ (flushed zone) and $d_j$ (transition zone). It is probably a more realistic model for true borehole conditions than is the step profile. At least three resistivity measurements, each sensitive to a different distance away from the borehole, are needed to measure a transitional profile. These three measure resistivities of the flushed ($R_{xo}$), transition ($R_i$), and uninvaded zones ($R_t$) (see Figure 1.3). By using these three resistivity measurements, the deep reading resistivity measurement can be corrected to a more accurate value of true resistivity ($R_t$), and the depth of invasion can be determined.

This ability to estimate the invasion in a formation arrived with the wide introduction of the dual induction and dual laterolog tools in the 1960s. As the names imply, each tool made two induction or two laterolog measurements. These two measurements investigate different distances into the formation and are referred to as medium and deep measurements. The word dual in the names of these logging tools can be
<!-- page 18 -->
Basic Relationships of Well Log Interpretation 7

7

confusing, because each tool also made a third measurement, which was shallower than the medium and deep measurements. In the 1980s, array resistivity tools made their appearance. Through the use of more sensors, they investigate more distances into the formation (usually 5 to 7), which provides for a more detailed picture of the formation and its invasion.

An annulus profile is only sometimes recorded on a log, because it rapidly dissipates in a well. The annulus profile is detected only by an induction log run soon after a well is drilled. However, it is very important to a geologist, because the profile can only occur in zones that bear hydrocarbons. As the mud filtrate invades the hydrocarbon-bearing zone, the hydrocarbons are moved out first. Next, formation water is pushed out in front of the mud filtrate, forming an annular (circular) ring at the edge of the invaded zone (Figure 1.3). The annulus effect is detected by a higher resistivity reading on a deep induction log than by one on a medium induction log.

Log resistivity profiles illustrate the resistivity values of the invaded and uninvaded zones in the formation being investigated. They are of particular interest because, by using them, a geologist can quickly scan a log and look for potential zones of interest such as hydrocarbon zones. Because of their importance, resistivity profiles for both water-bearing and hydrocarbon-bearing zones are discussed here. These profiles vary, depending on the relative resistivity values of $R_w$ and $R_{mf}$. All the variations and their associated profiles are illustrated in Figures 1.4 and 1.5.

### Water-bearing Zones

Figure 1.4 illustrates the borehole and resistivity profiles for water-bearing zones where the resistivity of the mud filtrate ($R_{mf}$) for a freshwater mud is much greater than the resistivity of the formation water ($R_w$), and where resistivity of the mud filtrate ($R_{mf}$) for a saltwater mud is approximately equal to the resistivity of the formation water ($R_w$). A freshwater mud (i.e., $R_{mf} > 3 R_w$) results in a wet log profile where the shallow ($R_{so}$), medium ($R_i$), and deep ($R_t$) resistivity measurements separate and record high ($R_{so}$), intermediate ($R_i$), and low ($R_t$) resistivities (Figure 1.4). A saltwater mud (i.e., $R_w = R_{mf}$) results in a wet profile where the shallow ($R_{so}$), medium ($R_i$), and deep ($R_t$) resistivity measurements all read low resistivity (Figure 1.4). Figures 1.6 and 1.7 illustrate the resistivity curves for wet zones invaded with either freshwater or saltwater mud.

### Hydrocarbon-bearing Zones

Figure 1.5 illustrates the borehole and resistivity profiles for hydrocarbon-bearing zones where the resistivity of the mud filtrate ($R_{mf}$) for a freshwater mud is much greater than the resistivity of the formation water ($R_w$), and where $R_{mf}$ of a saltwater mud is approximately equal to $R_w$. A hydrocarbon zone invaded with freshwater mud results in a resistivity profile where the shallow ($R_{so}$), medium ($R_i$), and deep ($R_t$) resistivity measurements all record high resistivities (Figure 1.5). In some instances, the deep resistivity is higher than the medium resistivity. When this happens, it is called the annulus effect. A hydrocarbon zone invaded with saltwater mud results in a resistivity profile where the shallow ($R_{so}$), medium ($R_i$), and deep ($R_t$) resistivity measurements separate and record low ($R_{so}$), intermediate ($R_i$) and high ($R_t$) resistivities (Figure 1.5). Figures 1.8 and 1.9 illustrate the resistivity curves for hydrocarbon zones invaded with either freshwater or saltwater mud.

### BASIC INFORMATION NEEDED IN LOG INTERPRETATION

#### Lithology

In quantitative log analysis, there are several reasons why it is important to know the lithology of a zone (i.e., sandstone, limestone, or dolomite). Porosity logs require a lithology or a matrix constant before the porosity ($\phi$) of the zone can be calculated. The formation factor ($F$), a variable used in the Archie water-saturation equation, also varies with lithology. As a consequence, the calculated water saturation changes as $F$ changes. Table 1.1 is a list of several different values for calculating formation factor and illustrates how lithology affects the formation factor.

#### Formation Temperature

Formation temperature ($T_f$) is also important in log analysis, because the resistivities of the drilling mud ($R_m$), the mud filtrate ($R_{mf}$), and the formation water ($R_w$) vary with temperature. The temperature of a formation is determined by knowing:

- formation depth
- bottom hole temperature (BHT)
- total depth of the well (TD)
- surface temperature
<!-- page 19 -->
8

ASQUITH AND KRYGOWSKI

A reasonable value for the formation temperature can be determined by using these data and by assuming a linear geothermal gradient (Figure 1.10). The formation temperature is also calculated (Asquith, 1980) by using the linear regression equation:

$$y = mx + c \tag{1.10}$$

where:

$x =$ depth

$y =$ temperature

$m =$ slope (In this example it is the geothermal gradient.)

$c =$ a constant (In this example it is the mean annual surface temperature.)

An example of how to calculate formation temperature is illustrated here:

### Temperature Gradient Calculation

Assume that:

$y =$ bottom hole temperature (BHT) = 250°F

$x =$ total depth (TD) = 15,000 ft

$c =$ mean annual surface temperature = 70°F

Solve for $m$ (i.e., slope or temperature gradient):

$$m = \frac{y - c}{x}$$

Therefore,

$$m = \frac{250^\circ - 70^\circ}{15,000 \text{ ft}}$$

$$m = 0.012^\circ / \text{ft or } 1.2^\circ / 100 \text{ ft}$$

### Formation Temperature Calculation

Assume:

$m =$ temperature gradient = 0.012°/ft

$x =$ formation depth = 8,000 ft

$c =$ surface temperature = 70°

Remember:

$$y = mx + c$$

Therefore:

$$y = (0.012 \times 8,000) + 70$$

$y = 166^\circ$ formation temperature at 8,000 ft

After a formation's temperature is determined either by chart (Figure 1.10) or by calculation, the resistivities of the different fluids ($R_m$, $R_{mf}$, or $R_w$) can be corrected to formation temperature. Figure 1.11 is a chart that is used for correcting fluid resistivities to the formation temperature. This chart is closely approximated by the Arp's formula:

$$R_{TF} = \frac{R_{temp}(Temp + 6.77)}{(T_f + 6.77)} \left( = \frac{R_{temp}(Temp + 21.0)}{(T_f + 21.0)} \begin{array}{c} \text{for depth} \\ \text{in meters} \end{array} \right) \tag{1.10}$$

where:

$R_{TF} =$ resistivity at formation temperature

$R_{temp} =$ resistivity at a temperature other than formation temperature

$Temp =$ temperature at which resistivity was measured (usually Fahrenheit for depth in feet, Celsius for depth in meters)

$T_f =$ formation temperature (usually Fahrenheit for depth in feet, Celsius for depth in meters)

Using a formation temperature of 166°F and assuming an $R_w$ of 0.04 measured at 70°F, the $R_w$ at 166°F is:

$$R_{w166} = 0.04 \times (70 + 6.77) / (166 + 6.77)$$

$$R_{w166} = 0.018 \text{ ohm-m}$$

Resistivity values of the drilling mud ($R_m$), mud filtrate ($R_{mf}$), mud cake ($R_{mc}$), and the temperatures at which they are measured are recorded on a log's header (Figure 1.2). The resistivity of a formation's water ($R_w$) is obtained by analysis of water samples from a drill stem test, a water-producing well, or from a catalog of water resistivity values. Formation water resistivity ($R_w$) is also determined from the spontaneous-potential log (discussed in Chapter 2), or it can be calculated in water zones (i.e., where $S_w=1$) by the apparent water resistivity ($R_{wa}$) method (see Chapter 7).

### COMMON EQUATIONS

Table 1.2 is a list of common equations that are used for the log evaluation of potential hydrocarbon reservoirs. These formulas are discussed in detail in subsequent chapters.
<!-- page 20 -->
Basic Relationships of Well Log Interpretation

9

Table 1.2. Common equations of well-log interpretation

Porosity, $\phi$:

|  $\phi_{Sonic} = \frac{\Delta t_{log} - \Delta t_{matrix}}{\Delta t_{fluid} - \Delta t_{matrix}}$ | Sonic log porosity (Wyllie time-average equation)  |
| --- | --- |
|  $\phi_{Sonic} = \frac{5}{8} \times \left( \frac{\Delta t_{log} - \Delta t_{matrix}}{\Delta t_{log}} \right)$ | Sonic log porosity (Raymer-Hunt-Gardner equation)  |
|  $\phi_{Density} = \frac{\rho_{matrix} - \rho_{bulk(log)}}{\rho_{matrix} - \rho_{fluid}}$ | Density log porosity  |
|  $\phi_{NDgas} = \sqrt{\frac{\phi_N^2 + \phi_D^2}{2}}$ | Porosity in a gas zone from neutron and density  |

Formation factor, $F$:

|  $F = a/\phi^m$ | General form of the equation  |
| --- | --- |
|  $F = 1.0/\phi^{2.0}$ | Carbonates  |
|  $F = 0.81/\phi^{2.0}$ | Consolidated sandstones  |
|  $F = 0.62/\phi^{2.15}$ | Unconsolidated sands  |

Formation-water resistivity:

|  $SSP = -K \times \log(R_{mf}/R_w)$ | Basic SP response equation  |
| --- | --- |
|  $R_w = 10^{(K \times \log(R_{mf}) + SP)/K}$ | First-order approximation of $R_w$ from the SP  |

Water saturation:

|  $S_w = \left( \frac{a \times R_w}{R_t \times \phi^m} \right)^{\frac{1}{n}}$ | Water saturation in the uninvaded zone  |
| --- | --- |
|  $S_{so} = \left( \frac{a \times R_{mf}}{R_{so} \times \phi^m} \right)^{\frac{1}{n}}$ | Water saturation in the flushed zone  |
|  $S_w = \left( \frac{R_{so}/R_t}{R_{mf}/R_w} \right)^{0.625}$ | Water saturation, ratio method  |

Bulk volume water:

$$BVW = \phi \times S_w$$

Permeability (estimated):

|  $K_e = \left( 250 \times \left( \frac{\phi^3}{S_{wirr}} \right) \right)^2$ | Permeability in millidarcys, oil reservoir  |
| --- | --- |
|  $K_e = \left( 79 \times \left( \frac{\phi^3}{S_{wirr}} \right) \right)^2$ | Permeability in millidarcys, gas reservoir  |
<!-- page 21 -->
10

ASQUITH AND KRYGOWSKI

# REVIEW

1. The four most fundamental rock properties used in petrophysical logging are:

- porosity
- permeability
- water saturation
- lithology

2. The Archie equation for water saturation is:

$$S_w = \left( \frac{a \times R_w}{R_t \times \phi^m} \right)^{\frac{1}{n}}$$

where:

$S_w$ = water saturation of uninvaded zone

$R_w$ = formation water resistivity

$R_t$ = formation resistivity (uninvaded zone)

$\phi$ = porosity

$a$ = tortuosity factor

$m$ = cementation exponent

$n$ = saturation exponent

3. Where a porous and permeable formation is penetrated by the drill bit, the liquid part of the drilling mud invades the formation as mud filtrate. The mud filtrate resistivity is designated $R_{mf}$.

4. The invasion of a porous and permeable forma-

tion by mud filtrate creates invaded zones around the wellbore. Shallow-, medium-, and deep-reading resistivity measurements provide information about the invaded and uninvaded zones and about the depth of invasion of the drilling fluid.

5. The lithology of a formation must be known because:

- A matrix value (usually sandstone, limestone, or dolomite) is needed to determine porosity from logs.

- The formation factor varies with lithology.

- The variation in the formation factor changes the water-saturation values.

6. The four fluids (and the symbols for their resistivity) that affect logging measurements are:

- drilling mud ($R_m$)

- mud filtrate ($R_{mf}$)

- formation water ($R_w$)

- hydrocarbons (assumed infinite resistivity, no symbol)

7. The resistivities of the drilling mud ($R_m$), mud cake ($R_{mc}$), mud filtrate ($R_{mf}$) and formation water ($R_w$) all vary with changes in temperature. Consequently, a formation's temperature ($T_f$) must be determined and all resistivities corrected to $T_f$.
<!-- page 22 -->
Basic Relationships of Well Log Interpretation 11


━━━ FORMAT 9: TECHNICAL SCHEMATIC ━━━

**Subject:** Cross-sectional schematic of the mud-filtrate invasion profile around a borehole, showing resistivity zones and dimensions.

**Legend (top left):**
| Symbol | Meaning |
|--------|---------|
| □ (square) | Resistivity of the zone |
| ○ (circle) | Resistivity of the water in the zone |
| △ (triangle) | Water saturation in the zone |

**Physical arrangement:**

The image shows a vertical borehole (Hole diameter, d_h) penetrating a permeable bed of thickness h (Bed thickness). Mud fills the borehole at the top (Mud, R_m — circle symbol). The bed is bounded above and below by Adjacent bed, each marked with R_s (square symbol).

Around the borehole, within the bed, three concentric zones are shown:

1. **Flushed zone** — dark gray shading, immediately adjacent to the borehole wall. Marked with R_mc (circle symbol, resistivity of the water in the zone).
2. **Zone of invasion or annulus** — medium gray shading, between the flushed zone and the uninvaded zone. Marked with R_xo (square symbol, resistivity of the zone).
3. **Uninvaded zone** — light gray shading, outermost. Marked with R_t (square symbol, resistivity of the zone), plus a circle symbol (resistivity of the water in the zone) and a triangle symbol (water saturation in the zone).

**Callout labels and dimensions:**
- **Mud** — at top of borehole, with R_m (circle symbol).
- **Bed thickness** — left side, labeled h (vertical dimension).
- **Invasion diameter** — bottom right label, dimension d_i at bottom left.
- **Hole diameter** — bottom center, labeled d_h.

**Demonstrates:** The standard invasion model used in well-log interpretation, showing the resistivity profile from the flushed zone (R_mc, R_xo) through the annulus to the uninvaded formation (R_t), and the different resistivity R_s of the adjacent beds.

KEYWORDS: invasion profile, flushed zone, annulus, uninvaded zone, resistivity, mud cake, borehole, true formation resistivity, well logging, petrophysics
----


Courtesy Schlumberger Wireline & Testing, ©1998 Schlumberger

Figure 1.1. The borehole environment and symbols used in log interpretation.

This schematic diagram illustrates an idealized version of what happens when fluids from the borehole invade the surrounding rock. Dotted lines indicate the cylindrical nature of the invasion.

$d_b$ = hole diameter

$d_i$ = diameter of invaded zone (inner boundary of flushed zone)

$d_j$ = diameter of invaded zone (outer boundary of invaded zone)

$\Delta r_j$ = radius of invaded zone (outer boundary)

$h_{mc}$ = thickness of mud cake

$R_m$ = resistivity of the drilling mud

$R_{mc}$ = resistivity of the mud cake

$R_{mf}$ = resistivity of mud filtrate

$R_s$ = resistivity of the overlying bed (commonly assumed to be shale)

$R_t$ = resistivity of uninvaded zone (true formation resistivity)

$R_w$ = resistivity of formation water

$R_{so}$ = resistivity of flushed zone

$S_o$ = water saturation of uninvaded zone

$S_{so}$ = water saturation flushed zone

| HALLIBURTON | HIGH RES INDUCTION SPECTRAL DENSITY DUAL SPACED NEUTRON |
| --- | --- |
| COMPANY GO FOR IT WELL 1 COUNTY 3 STATE TEXAS | COMPANY GO FOR IT WELL 1 FIELD TRAVIS 2 COUNTY TRAVIS STATE TEXAS |
| API No. 2222 Location 1350' FWL & 2560' FNL OF BALCONES A' LEASE | Other Services SFT 4 |
| Sect N/A Twp N/A Rge N/A |  |
| Permanent Datum G.L. Elev 291.00 Log measured from T.K.B. 26.000 ft. above perm. datum Drilling measured from T.K.B. | Elev. K.B. 317.00 D.F. 316.00 G.L. 291.00 |
| Date | 11-14-1999 | 11-21-1999 | 11-27-1999 | 62000 |
| Run No. |  |  |  |  |
| Depth - Driller | 8000.00000 | 11900.0000 | 12910.0000 | 6 |
| Depth - Logger | 7986.00000 | 11908.0000 | 12906.0000 |  |
| Bottom - Logged Interval | 7977.00000 | 11899.0000 | 12897.0000 |  |
| Top - Logged Interval | 2008.00000 | 8000.00000 | 11906.0000 |  |
| Casing - Driller | 13.37 @ 2008.0 | 9.625 @ 8000.0 | 7.625 @ 11900. | @ |
| Casing - Logger | 2008.00000 | 8000.00000 | 11906.0000 |  |
| Bit Size | 12.250000 | 8.500000 | 6.500000 |  |
| Type Fluid in Hole | WATER BASE MUD | OIL BASE MUD | OIL BASE MUD |  |
| Dens. | Visc. | 12.80 | 41.000 | 16.00 | 53.000 | 14.30 | 47.000 | | |
| Ph | Fluid Loss | 9.200 | 6.4000 | | 4.0000 | | 8.0000 | | |
| Source of Sample | FLOW LINE | FLOW LINE | FLOW LINE |  |
| Rm @ Meas. Temp. | 1.670 @ 75.00 | @ | @ | @ |
| Rmf @ Meas. Temp. | 1.200 @ 75.00 | @ | @ | @ |
| Rmc @ Meas. Temp. | 2.080 @ 75.00 | @ | @ | @ |
| Source Rmf | Rmc | MEAS. | MEAS. | N/A | N/A | N/A | N/A | | |
| Rm @ BHT | 0.630 @ 210.0 | @ | @ | @ |
| Time Since Circ. | 8 | 10 | 8 |  |
| Time on Bottom | 320 | 430 | 1914 |  |
| Mar. Rec. Temp. | 210.0 @ | 210.0 @ | 210.0 @ | 210.0 @ |
| Equip. | Location | 51561 | ALICE | 51731 | ALICE | 54261 | ALICE | 7 |
| Recorded By | J. ZIMMER | VISHOK JAIN | AL PADILLA |  |
| Witnessed By | DAN | PAUL |  |  |

Figure 1.2. Reproduction of a typical log heading.

This is the first page of a typical log heading. Following pages contain details of the logging equipment used, the scales used to display the data, general information about the borehole direction, remarks about the logging job, and a disclaimer which outlines the responsibilities of both the acquisition company and the client.

1. The title indicates the services that are associated with the data that appear on this log.
2. Basic well name and location information.
3. More detailed information about the physical surface location of the well.
4. Other services that were run at the same time (during the same trip to the well) as the services in this log.
5. Information about location and elevation from which the well depths are measured. K.B. = kelly bushing elevation, D.F. = drill floor elevation, G.L. = ground level elevation, T.K.B. = top of kelly bushing
6. Environmental information about the well. The drilling mud and borehole size values are especially important in applying the proper environmental corrections and interpretation parameters to the data.
7. General information about the logging equipment, the engineer, and any clients who witnessed the logging job. More detailed information about the specific logging tools is listed in the pages that usually follow this one and in tables that detail the calibration techniques and results.
<!-- page 23 -->
12

ASQUITH AND KRYGOWSKI

Figure 1.3. Resistivity profiles for three idealized versions of fluid distributions in the vicinity of the borehole. As mud filtrate ($R_{so}$) moves into a porous and permeable formation, it can invade the formation in several different ways. Various fluid distributions are represented by the step, transition, or annulus profiles. All three profiles illustrate the effect of a freshwater mud; for profiles using saltwater mud see figures 1.4 and 1.5. Mud cake thickness is indicated by $h_{mc}$.

# Step profile:

This idealized model is the one inferred by the use of three resistivity logs to estimate invasion. Mud filtrate is distributed with a cylindrical shape around the borehole and creates an invaded zone. The cylindrical invaded zone is characterized by its abrupt contact with the uninvaded zone. The diameter of the cylinder is represented as $d_j$. In the invaded zone, pores are filled with mud filtrate ($R_{so}$); pores in the uninvaded zone are filled with formation water ($R_{so}$) and hydrocarbons. In this example, the uninvaded zone is wet (water saturated and no hydrocarbons), thus the resistivity beyond the invaded zone is low. The resistivity of the invaded zone is $R_{so}$, and the resistivity of the uninvaded zone is $R_f$ (where $R_f$ reduces to $R_o$ when the formation is water bearing).

# Transition profile:

This is the most realistic model of true borehole conditions. Here again invasion is cylindrical, but in this profile, the invasion of the mud filtrate ($R_{so}$) diminishes gradually, rather than abruptly, through a transition zone toward the outer boundary of the invaded zone (see $d_j$ on diagram for location of outer boundary).

In the flushed part ($R_{so}$) of the invaded zone, pores are filled with mud filtrate ($R_{so}$), giving a high resistivity reading. In the transition part of the invaded zone, pores are filled with mud filtrate ($R_{so}$), formation water ($R_{so}$), and, if present, residual hydrocarbons. Beyond the outer boundary of the invaded zone, pores are filled with either formation water or formation water and hydrocarbons. In this diagram, hydrocarbons are not present, so resistivity of the uninvaded zone is low. The resistivity of the invaded zone is $R_{so}$, and the resistivity of the uninvaded zone is $R_f$ (where $R_f$ reduces to $R_o$ when the formation is water bearing).

# Annulus profile:

This reflects a temporary fluid distribution and is a condition that should disappear with time (if the logging operation is delayed, it might not be recorded on the logs at all). The annulus profile represents a fluid distribution that occurs between the invaded zone and the uninvaded zone and only exists in the presence of hydrocarbons.

In the flushed part ($R_{so}$) of the invaded zone, pores are filled with both mud filtrate ($R_{so}$) and residual hydrocarbons. Thus the resistivity reads high. Pores beyond the flushed part of the invaded zone ($R_f$) are filled with a mixture of mud filtrate ($R_{so}$), formation water ($R_{so}$), and residual hydrocarbons.

Beyond the outer boundary of the invaded zone is the annulus zone, where pores are filled with formation water ($R_{so}$) and residual hydrocarbons. When an annulus profile is present, there is an abrupt drop in measured resistivity at the outer boundary of the invaded zone. The abrupt resistivity drop is due to the high concentration of formation water ($R_{so}$) in the annulus zone. Formation water has been pushed ahead by the invading mud filtrate into the annulus zone. This causes a temporary absence of hydrocarbons, which have been pushed ahead of the formation water.

Beyond the annulus is the uninvaded zone, where pores are filled with formation water ($R_{so}$) and hydrocarbons. The resistivity of the invaded zone is $R_{so}$, and the resistivity of the uninvaded zone is $R_f$ (where $R_f$ reduces to $R_o$ when the formation is water bearing).


----
━━━ FORMAT 9: TECHNICAL SCHEMATIC / ТЕХНИЧЕСКАЯ СХЕМА ━━━

**Title:** Step Profile

The schematic is an idealized "step" resistivity profile around a borehole, representing the invasion model.

**Axes:**
- Vertical (ordinate): Resistivity, increases upward (indicated by an upward arrow on the left).
- Horizontal (abscissa): Distance from the borehole, increases to the right (indicated by a rightward arrow at the bottom).

**Physical arrangement (left to right):**
1. **Borehole wall** — vertical line at the far left; a callout "borehole wall" with a leader line points to it.
2. **Mudcake** — narrow vertical band of thickness **h_mc** adjacent to the borehole wall.
3. **d_i** — first dashed vertical line, located within the R_xo plateau.
4. **d_j** — second dashed vertical line, located at the position of the step down.
5. Step-function curve:
   - **R_xo** — constant high resistivity from the outer edge of the mudcake to **d_j**.
   - At **d_j**, an abrupt vertical drop to **R_o**.
   - **R_o** — constant lower resistivity from **d_j** onward.

**Callout labels and leader-line annotations:**
1. "borehole wall" → points to the leftmost vertical line.
2. "R_xo" → written above the upper horizontal plateau.
3. "R_o" → written above the lower horizontal plateau.
4. "h_mc" → written at the base of the mudcake band.
5. "d_i" → written at the base of the first dashed line.
6. "d_j" → written at the base of the second dashed line.

The schematic demonstrates the simplified step model of mud-filtrate invasion: a flushed zone with resistivity R_xo extends from the borehole wall (after a mudcake of thickness h_mc) to a distance d_j, where it abruptly transitions to the uninvaded formation with true resistivity R_o.

KEYWORDS: invasion profile, step profile, flushed zone, uninvaded zone, mudcake, R_xo, R_o, h_mc, d_i, d_j
----


━━━ FORMAT 9: TECHNICAL SCHEMATIC / ТЕХНИЧЕСКАЯ СХЕМА ━━━
Schematic of the resistivity transition profile away from the borehole in a permeable formation (invasion profile).

Physical arrangement (left to right along the horizontal distance axis):
- A vertical narrow rectangle at the far left represents the mudcake; its thickness on the distance axis is labelled **h_mc**. An arrow labelled **borehole wall** points to this rectangle.
- The resistivity curve begins at a high plateau labelled **R_xo** (flushed-zone resistivity) immediately outside the mudcake.
- At distance **d_i** the curve starts to decline; the descending segment is labelled **R_i** (invaded/transition-zone resistivity), marked by a vertical dashed line.
- At distance **d_j** the curve flattens to a constant level labelled **R_o** (uninvaded-zone resistivity) and remains flat thereafter, marked by a vertical dashed line.

Axes:
- Vertical axis: **Resistivity** (arrow upward; no numerical scale shown).
- Horizontal axis: **Distance from the borehole** (arrow pointing right), with labelled positions **h_mc**, **d_i**, **d_j**.

This schematic demonstrates the classic invasion profile: mudcake (h_mc), flushed zone (R_xo), invaded/transition zone (R_i), and uninvaded zone (R_o).

KEYWORDS: invasion profile, resistivity, R_xo, R_i, R_o, mudcake, flushed zone, invaded zone, borehole, transition profile
----


----
━━━ FORMAT 9: TECHNICAL SCHEMATIC / ТЕХНИЧЕСКАЯ СХЕМА ━━━
**Title in the image:** Annulus Profile

**Demonstrates:** Radial distribution of electrical resistivity around a borehole caused by mud-filtrate invasion.

**Axes:**
- Vertical axis: **Resistivity** (arrow directed upward). No numerical scale or units printed.
- Horizontal axis: **Distance from the borehole** (arrow directed rightward). No numerical scale or units printed.

**Structural elements and labels (in spatial order):**
1. **borehole wall** — a filled/stippled vertical bar at the far left of the plot; a leader line with the label "borehole wall" points to it.
2. **Rxo** (subscript *xo*) — a high, horizontal solid segment immediately to the right of the borehole wall (flushed zone).
3. **Ri** (subscript *i*) — a straight, downward-sloping solid segment to the right of Rxo (invaded/transition zone).
4. **Annulus** — a near-vertical drop at the end of the Ri segment, followed by a short horizontal segment at a pronounced low value.
5. **Rt** (subscript *t*) — a step up from the annulus low to a horizontal solid segment (true formation resistivity). Rt is lower than Rxo but higher than the annulus low.
6. **Rw** (subscript *w*) — a dotted horizontal line near the bottom of the plot, representing formation water resistivity (reference level only, not part of the solid curve).

**Vertical dashed boundary lines** (labels printed below the horizontal axis):
- **d_mc** (subscript *mc*) — at the outer edge of the borehole-wall bar.
- **d_i** (subscript *i*) — at the end of the Ri sloping segment (base of the annulus drop).
- **d_j** (subscript *j*) — at the end of the annulus (start of the Rt segment).

KEYWORDS: annulus profile, invasion, resistivity, Rxo, Ri, Rt, Rw, mud filtrate, flushed zone, borehole wall
----


<!-- page 24 -->
Basic Relationships of Well Log Interpretation

13


----
━━━ FORMAT 9: TECHNICAL SCHEMATIC / ТЕХНИЧЕСКАЯ СХЕМА ━━━

The schematic demonstrates the radial distribution of resistivities around a borehole penetrating a permeable water-bearing bed, contrasting freshwater-mud and saltwater-mud invasion profiles.

**Title (verbatim):** "Horizontal section through a permeable water-bearing bed"

**Top schematic — concentric zones (from centre outward):**
A plan-view cross-section with dashed vertical lines connecting zone boundaries to the x-axis of the plots below.

| Zone | Symbol |
|------|--------|
| Borehole (centre) | R_m |
| Mudcake (annulus) | R_mf |
| Flushed zone | R_xo |
| Invaded zone | R_i |
| Uninvaded zone | R_t |
| Formation water (outer region) | R_w |

**Callout labels (numbered, verbatim):**
1. "borehole wall" — leader line to the inner circle boundary, with symbol R_m inside the circle.
2. "mudcake" — leader line to the annulus immediately outside the borehole wall, with symbol R_mf.
3. "Flushed zone" — label for the first annulus, with symbol R_xo.
4. "Invaded zone" — label for the second annulus, with symbol R_i.
5. "Uninvaded zone" — label for the outermost annulus, with symbol R_t.
6. "fluid resistivities" — label in the outer region, with symbol R_w in the uninvaded zone.

**Bottom plots — "Radial distribution of resistivities":**
Two stacked XY plots, each with:
- Y-axis: "Resistivity" (arrow pointing upward; qualitative linear scale)
- X-axis: "Distance from the borehole" (arrow pointing to the right; qualitative linear scale)
- X-axis labelled positions (left to right): h_mc, d_i, d_j
- A vertical line at the left boundary (borehole wall)

**Plot 1 — Freshwater muds (Rmf >> Rw):**
- Condition label (verbatim): "Freshwater muds Rmf >> Rw"
- Curve: Starts at a high value labelled R_xo, decreases across the invaded zone, and levels off at a lower value labelled R_w in the uninvaded zone.
- Displays R_xo >> R_w — a pronounced radial resistivity gradient.

**Plot 2 — Saltwater muds (Rmf ~ Rw):**
- Condition label (verbatim): "Saltwater muds Rmf ~ Rw"
- Curve: Starts at a value labelled R_xo approximately equal to R_w, remains approximately flat at R_w across the invaded and uninvaded zones.
- Displays R_xo ≈ R_w — a minimal radial resistivity gradient.

**Key idea communicated:** The contrast between mud filtrate resistivity (Rmf) and formation water resistivity (Rw) controls the shape of the radial resistivity profile — freshwater muds create a high-resistivity flushed zone that decays to Rw, while saltwater muds produce an almost flat radial resistivity profile.

KEYWORDS: invasion profile, flushed zone, invaded zone, uninvaded zone, mudcake, R_xo, R_i, R_t, R_mf, R_w
----


Figure 1.4. Resistivity profile for a transition-style invasion of a water-bearing formation.

Note: These examples are shown because freshwater muds and saltwater muds are used in different geographic regions, usually exclusively. The geologist needs to be aware that a difference exists. To find out which mud is used in your area, check the log heading of existing wells or ask your drilling engineer. The type of mud used affects the log package selected, as will be shown in later chapters.

# Freshwater muds:

The resistivity of the mud filtrate ($R_{mf}$) is greater than the resistivity of the formation water ($R_w$) (remember, saltwater is conductive). A general rule when freshwater muds are used is: $R_{mf} > 3 R_w$. The flushed zone ($R_{so}$), which has a greater amount of mud filtrate, has higher resistivities. Away from the borehole, the resistivity of the invaded zone ($R_i$) decreases due to the decreasing amount of mud filtrate ($R_{mf}$) and the increasing amount of formation water ($R_w$).

With a water-bearing formation, the resistivity of the uninvaded zone is low because the pores are filled with formation water ($R_w$). In the uninvaded zone, true resistivity ($R_i$) is equal to wet resistivity ($R_o$) because the formation is completely saturated with formation water ($R_f = R_o$ where the formation is completely saturated with formation water).

To summarize: in a water-bearing zone, the resistivity of the flushed zone ($R_{so}$) is greater than the resistivity of the invaded zone ($R_i$), which in turn has a greater resistivity than the uninvaded zone ($R_i$). Therefore: $R_{so} > R_i > R_f$ in water-bearing zones.

# Saltwater muds:

Because the resistivity of mud filtrate ($R_{mf}$) is approximately equal to the resistivity of formation water ($R_{mf} \sim R_w$), there is no appreciable difference in the resistivity from the flushed ($R_{so}$) to the invaded zone ($R_i$) to the uninvaded zone ($R_{so} = R_i = R_f$); all have low resistivities.

Both the above examples assume that the water saturation of the uninvaded zone is much greater than 60%.
<!-- page 25 -->
14

ASQUITH AND KRYGOWSKI

Figure 1.5. Resistivity profile for a transition-style invasion of a hydrocarbon-bearing formation.

# Freshwater muds:

Because the resistivities of both the mud filtrate ($R_{mf}$) and residual hydrocarbons are much greater than formation water ($R_w$), the resistivity of the flushed zone ($R_{xo}$) is comparatively high (remember that the flushed zone has mud filtrate and some residual hydrocarbons).

Beyond its flushed part ($R_{xo}$), the invaded zone ($R_i$) has a mixture of mud filtrate ($R_{mf}$), formation water ($R_w$), and some residual hydrocarbons. Such a mixture causes high resistivities. In some cases, resistivity of the invaded zone ($R_i$) almost equals that of the flushed zone ($R_{xo}$).

The presence of hydrocarbons in the uninvaded zone causes higher resistivity than if the zone had only formation water ($R_w$), because hydrocarbons are more resistant than formation water. In such a case, $R_i > R_w$. The resistivity of the uninvaded zone ($R_i$) is normally somewhat less than the resistivity of the flushed and invaded zones ($R_{xo}$ and $R_i$). However, sometimes when an annulus profile is present, the invaded zone's resistivity ($R_i$) can be slightly lower than the uninvaded zone's resistivity ($R_i$).

To summarize: $R_{xo} > R_i > R_f$ or $R_{xo} > R_i < R_f$ in hydrocarbon-bearing zones.

# Saltwater muds:

Because the resistivity of the mud filtrate ($R_{mf}$) is approximately equal to the resistivity of formation water ($R_{mf} \sim R_w$), and the amount of residual hydrocarbons is low, the resistivity of the flushed zone ($R_{xo}$) is low.

Away from the borehole, as more hydrocarbons mix with mud filtrate in the invaded zone the resistivity of the invaded zone ($R_i$) increases.

Resistivity of the uninvaded zone ($R_i$) is much greater than if the formation were completely water saturated ($R_w$) because hydrocarbons are more resistant than saltwater. Resistivity of the uninvaded zone ($R_i$) is greater than the resistivity of the invaded ($R_i$) zone. So, $R_i > R_i > R_{xo}$. Both the above examples assume that the water saturation of the uninvaded zone is much less than 60%.

Horizontal section through a permeable oil-bearing bed


━━━ FORMAT 9: TECHNICAL SCHEMATIC / ТЕХНИЧЕСКАЯ СХЕМА ━━━

**Schematic demonstrates:** the radial distribution of resistivities around a borehole invaded by mud filtrate, comparing freshwater-mud and saltwater-mud invasion profiles.

**1. Borehole cross-section (concentric rings, centre = borehole axis)**

Physical arrangement, from centre outward:

- **Rm** — resistivity of the mud inside the borehole
- **Borehole wall** — circular boundary between mud and mudcake (arrowed)
- **Mudcake** — thin annular deposit on the borehole wall
- **Flushed zone** — region just outside the mudcake, flushed by mud filtrate; contains **Rxo** (flushed-zone resistivity)
- **Invaded zone** — zone beyond the flushed zone; contains **Ri** (invaded-zone resistivity)
- **Annulus** — annular boundary zone between the invaded and uninvaded zones
- **Uninvaded zone** — outermost formation, containing **Rt** (true formation resistivity)
- **Fluid resistivities** — label in the annular region, referring to **Rw** (formation-water resistivity)

Callout labels (leader lines):
1. borehole wall
2. mudcake
3. Rm
4. flushed zone
5. Rxo
6. fluid resistivities
7. Rw
8. Invaded zone
9. Ri
10. Annulus
11. Uninvaded zone
12. Rt

Vertical dashed lines connect the schematic rings to the x-axis of the plots below, mapping radial zone boundaries onto distance from the borehole.

**2. Radial resistivity distribution — Freshwater muds (Rmf >> Rw)**

Plot: y-axis **Resistivity** (no scale given); x-axis **Distance from the borehole** (no scale given). Markers on the x-axis: **h_mc** (mudcake thickness), **d_i** (invasion diameter).

- Rxo (flushed zone) — high plateau immediately outside the mudcake
- Sharp drop across the mudcake and into the annulus
- Rm — low trough at the annulus
- Gradual rise outward
- Rt — intermediate value, lower than Rxo but higher than Rm

**3. Radial resistivity distribution — Saltwater muds (Rmf ~ Rw)**

Plot: y-axis **Resistivity** (no scale given); x-axis **Distance from the borehole** (no scale given). Markers on the x-axis: **h_mc**, **d_i**.

- Rxo (flushed zone) — low plateau immediately outside the mudcake
- Slight rise at the annulus
- Rm — small local maximum at the annulus
- Gradual rise outward
- Rt — high value, above both Rxo and Rm

KEYWORDS: radial resistivity distribution, invasion zone, mudcake, Rxo, Rt, Rm, Rw, borehole wall, flushed zone, annulus, uninvaded zone


<!-- page 26 -->
Basic Relationships of Well Log Interpretation

15


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━

The image shows a two-track well log. Depth is on the left axis, in **Feet MD** (Measured Depth), and **increases downward**. Visible depth labels: 5870, 5900, 5970 ft. The logged interval extends from approximately 5840 ft to approximately 6000 ft (partially visible gridlines).

**Track 1 (left):**
- Curve: **SP** (Spontaneous Potential), units: mV, linear scale from −160 to 40.
- Line style: solid.

**Track 2 (right):**
- Curves: **ILD** (Deep Induction Log), **ILM** (Medium Induction Log), **SFLU** (Spherically Focused Log), all in ohm‑m, logarithmic scale from 0.2 to 2000 (gridlines at 0.2, 1, 10, 100, 1000, 2000).
- Line styles: ILD — solid; ILM — dashed; SFLU — dotted.

**Interval table:**

| Interval, ft | Lithology (from column) | Curves: behaviour | Interpretation (if labelled) |
|---|---|---|---|
| Above ~5860 | No lithology column | SP near baseline (right side of track). SFLU high (~10–100 ohm‑m); ILD and ILM lower (~1–10 ohm‑m), ILD slightly below ILM. Maximum separation between SFLU and ILD/ILM. | None |
| ~5860–5900 | No lithology column | SP shows a negative excursion (deflects left toward −60…−80 mV). All three resistivity curves shift to lower values: ILD near 1 ohm‑m, ILM ~2–3 ohm‑m, SFLU ~10–20 ohm‑m. Curves are less separated. | None |
| ~5900–5960 | No lithology column | SP returns toward baseline. Resistivity increases: ILD and ILM converge (~5–10 ohm‑m); SFLU shows a high‑resistivity spike (up to ~100–1000 ohm‑m) before decreasing again. | None |
| ~5960 and below | No lithology column | SP shows a strong negative anomaly (deflects far left). Resistivity curves shift lower again: ILD near 1 ohm‑m, ILM slightly higher, SFLU elevated relative to ILD/ILM. | None |

Notes:
- The curve traces are described qualitatively; no point‑by‑point digitisation was performed.
- No lithology column, bed boundaries (отбивки), perforation intervals, fluid contacts, or interpreted intervals are labelled within the image.

KEYWORDS: well log, SP, induction log, resistivity, ohm-m, measured depth, feet, ILD, ILM, SFLU, spontaneous potential
----


Figure 1.6. Example of dual induction log curves through a water-bearing zone.

Given: the drilling mud is freshwater based ($R_{mf} > 3R_w$).

Where freshwater drilling muds invade a water-bearing formation ($S_w > 60\%$), there is high resistivity in the flushed zone ($R_{mf}$), a lesser resistivity in the invaded zone ($R_f$), and a low resistivity in the uninvaded zone ($R_f$).

See Figure 1.4 for review. (Figure 1.8 shows the response of these resistivity curves in a hydrocarbon-bearing zone.)

Compare the three curves on the right side of the log (tracks 2 and 3). Resistivity increases from left to right. A key for reading this logarithmic resistivity scale is shown at the bottom of the log. Depth scale is in feet with each vertical increment equal to 2 ft.

# Log curve ILD:

Deep induction log resistivity curves usually measure true formation resistivity ($R_f$), the resistivity of the formation beyond the outer boundary of the invaded zone. In water-bearing zones (in this case from 5870 to 5970 ft), the curve reads a low resistivity because the pores of the formation are saturated with low resistivity connate water ($R_w$).

# Log curve ILM:

Medium induction log resistivity curves measure the resistivity of the invaded zone ($R_f$). In a water-bearing formation, the curve reads a resistivity between $R_f$ and $R_{mf}$ because the fluid in the formation is a mixture of formation water ($R_w$) and mud filtrate ($R_{mf}$).

# Log curve SFLU:

Spherically focused log resistivity curves measure the resistivity of the flushed zone ($R_{mf}$). In a water-bearing zone, the curve reads a high resistivity because freshwater mud filtrate ($R_{mf}$) has a high resistivity. The SFL pictured here records a greater resistivity than either the deep (ILD) or medium (ILM) induction curves.
<!-- page 27 -->
16

ASQUITH AND KRYGOWSKI


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━

Depth scale: feet MD, depth increases downward. Visible depth range approximately 9830–9960 ft. Labelled depth markers: 9866 ft, 9900 ft, 9934 ft (evenly spaced at 34 ft intervals).

**Track 1 (left) — GR / CALI**
| Curve | Mnemonic | Scale range | Units | Line style |
|---|---|---|---|---|
| Gamma Ray | GR | 0–100 | API | Solid |
| Caliper | CALI | 6–16 | inches | Dashed |

**Track 2 (right) — Resistivity (logarithmic scale)**
| Curve | Mnemonic | Scale range | Units | Line style |
|---|---|---|---|---|
| Laterolog Deep | LLD | 0.2–2000 | ohm-m | Solid |
| Laterolog Shallow | LLS | 0.2–2000 | ohm-m | Dashed |
| Flushed-zone resistivity | RXO | 0.2–2000 | ohm-m | Dotted |

**Interval table**
| Interval, ft | Lithology (by column) | Curves: behaviour | Interpretation (if labelled) |
|---|---|---|---|
| ≈9830–9866 | No lithology column shown | GR: low, oscillating ≈10–40 API; CALI: ≈6–8 in; resistivity: moderate, LLD > LLS > RXO, moderate separation | None |
| 9866–9900 | No lithology column shown | GR: low, ≈5–20 API; CALI: ≈6 in; resistivity: high, LLD ≈500–1000+ ohm-m, LLS ≈100–500 ohm-m, RXO ≈10–50 ohm-m; strong separation (LLD ≫ LLS ≫ RXO) | None |
| 9900–9934 | No lithology column shown | GR: low, ≈10–30 API; CALI: ≈6–7 in; resistivity: high, LLD ≈300–1000 ohm-m, LLS and RXO progressively lower; strong separation | None |
| ≈9934–9960 | No lithology column shown | GR: variable, increases to ≈40–60 API in places; CALI: ≈6–8 in; resistivity: lower, curves converge to ≈50–200 ohm-m | None |

No results panel (Кп, Кн, Кпр, effective thickness) is printed. No lithology column and no interpretation labels are present in the image.

KEYWORDS: well log, gamma ray, caliper, laterolog, resistivity, invasion, hydrocarbon-bearing zone, ohm-m, API, depth track
----


Figure 1.7. Example of dual laterolog curves through a water-bearing zone.

Given: The drilling mud is saltwater based ($R_{ad} \sim R_w$).

Where saltwater drilling muds invade a water-bearing formation ($S_w > 60\%$), there is low resistivity in the flushed zone ($R_{za}$), a low resistivity in the invaded zone ($R_i$), and low resistivity in the uninvaded zone ($R_i$). Because $R_{ad}$ is approximately equal to $R_w$, the pores in the flushed ($R_{za}$), invaded ($R_i$), and uninvaded ($R_i$) zones are all filled with saline waters; the presence of salt results in low resistivity.

See Figure 1.4 for review. (Figure 1.9 shows the response of these resistivity curves in a hydrocarbon-bearing zone.)

Compare the three curves on the right side of the log (tracks 2 and 3). Resistivity increases from left to right. A key for reading this logarithmic resistivity scale is shown at the bottom of the log. Depth scale is in feet with each vertical increment equal to 2 ft.

### Log curve LLD:

Deep laterolog resistivity curves usually measure true formation resistivity ($R_f$), the resistivity of the formation beyond the outer boundary of the invaded zone. In water-bearing zones (in this case from 9866 to 9924 ft), the curve reads a low resistivity because the pores of the formation are saturated with low resistivity connate water ($R_w$).

### Log curve LLS:

Shallow laterolog resistivity curves measure the resistivity in the invaded zone ($R_i$). In a water-bearing zone, the shallow laterolog (LLS) records a low resistivity because $R_{ad}$ is approximately equal to $R_w$.

### Log curve RXO:

Microresistivity curves measure the resistivity of the flushed zone ($R_{za}$). In water-bearing zones the curve records a low resistivity because saltwater mud filtrate has low resistivity. The resistivity recorded by the microresistivity log is low and approximately equal to the resistivities of the invaded and uninvaded zones.
<!-- page 28 -->
Basic Relationships of Well Log Interpretation

17


━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth range: 8700–8800 ft (Feet MD — measured depth); depth increases downward.

Track 1 (left): SP (spontaneous potential), scale −160 to 40 mV, linear scale.
Track 2 (right): ILD (deep induction log), ILM (medium induction log), SFLU (spherically focused log); shared logarithmic scale 0.2 to 2000 ohm-m; curves plotted as solid lines.

| Интервал, фт | Кривые: поведение | Интерпретация |
|---|---|---|
| 8700 – ~8730 | SP: слабо отрицательная, ≈ −20…−30 мВ, плавная; ILD, ILM, SFLU: низкие показания ≈ 0,5–2 Ом·м, кривые слиты (не разделяются) | Глинистая толща |
| ~8730 – ~8780 | SP: отрицательная аномалия, минимум ≈ −80…−100 мВ; ILD, ILM, SFLU: повышенные показания, значительное разделение кривых; SFLU (максимум) ≈ 100–200 Ом·м > ILM ≈ 50–100 Ом·м > ILD (минимум) ≈ 20–50 Ом·м | Проницаемый пласт с зоной проникновения; положительная стрела проникновения (SFLU > ILM > ILD) |
| ~8780 – 8800 | SP: возврат к ≈ −40…−50 мВ; ILD, ILM, SFLU: низкие показания ≈ 0,5–2 Ом·м, кривые слиты | Глинистая толща |

Notes:
- All boundaries between intervals are approximate, read visually from curve behaviour; no explicit bed boundaries, contacts or perforation intervals are printed on the log.
- SP values and resistivity values for non-labelled samples are read from the grid and are approximate.

KEYWORDS: well log, SP, ILD, ILM, SFLU, resistivity, induction log, invasion zone, permeable interval, measured depth


Figure 1.8. Example of dual induction log curves through a hydrocarbon-bearing zone.

Given: the drilling mud is freshwater based ($R_{\mathrm{ad}} > 3R_{\mathrm{w}}$).

Where freshwater drilling muds invade a hydrocarbon-bearing formation ($S_{\mathrm{w}} < 60\%$), there is high resistivity in the flushed zone ($R_{\mathrm{ad}}$), high resistivity in the invaded zone ($R_{\mathrm{i}}$), and high resistivity in the uninvaded zone ($R_{\mathrm{j}}$). Normally, the flushed zone has slightly higher resistivity than the uninvaded zone.

See Figure 1.5 for review. (Figure 1.6 shows the response of these resistivity curves in a water-bearing zone.)

Compare the three curves on the right side of the log (tracks 2 and 3). Resistivity increases from left to right.

## Log curve ILD:

Deep induction log resistivity curves usually measure true formation resistivity ($R_{\mathrm{f}}$), the resistivity of the formation beyond the outer boundary of the invaded zone. In hydrocarbon-bearing zones (in this case from 8748 to 8774 ft), the curve records a high resistivity because hydrocarbons are more resistant than saltwater in the formation ($R_{\mathrm{f}} > R_{\mathrm{o}}$).

## Log curve ILM:

Medium induction log resistivity curves measure the resistivity of the invaded zone ($R_{\mathrm{f}}$). In a hydrocarbon-bearing zone, because of a mixture of mud filtrate ($R_{\mathrm{ad}}$), formation water ($R_{\mathrm{w}}$), and residual hydrocarbons in the pores, the curve records a high resistivity. This resistivity is normally equal to or slightly more than the deep induction curve (ILD). But, in an annulus situation, the medium curve (ILM) can record a resistivity slightly less than the deep induction (ILD) curve.

## Log curve SFLU:

Spherically focused log resistivity curves measure the resistivity of the flushed zone ($R_{\mathrm{ad}}$). In a hydrocarbon-bearing zone, the curve reads a higher resistivity than the deep (ILD) or medium (ILM) induction curves because the flushed zone ($R_{\mathrm{ad}}$) contains mud filtrate and residual hydrocarbons. The SFL pictured here records a greater resistivity than either the deep (ILD) or medium (ILM) induction curves.
<!-- page 29 -->
18

ASQUITH AND KRYGOWSKI


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━

**Well log presentation, depth interval 9300–9400 ft MD (Measured Depth). Depth increases downward.**

**Header row (top of log, left to right):** `0 GR 150` | `6 CALI 16` | `Feet MD` | `0.2 LLD 2000` | `0.2 LLS 2000` | `0.2 MSFL 2000`

**Track 1 (leftmost):**
- GR (Gamma Ray): scale 0–150 API. Solid line.
- CALI (Caliper): scale 6–16 inches. Dashed line.
- Both curves share one track; GR reads from the left edge (0) to right edge (150), CALI reads from the left edge (6) to right edge (16).

**Track 2 (right):**
- LLD (Deep Laterolog): scale 0.2–2000, logarithmic axis. Resistivity unit not printed in the visible header.
- LLS (Shallow Laterolog): scale 0.2–2000, logarithmic axis. Unit not printed.
- MSFL (Microspherically Focused Log): scale 0.2–2000, logarithmic axis. Unit not printed.
- Three curves are plotted in one track; separation between the curves is visible in high-resistivity intervals. Line-style assignment (solid/dashed/dotted) for individual curves is not legible from the raster.

**Interval table:**

| Interval, ft | Lithology (per column) | Curve behaviour | Interpretation (if labelled) |
|---|---|---|---|
| 9300–9320 | No lithology column shown | GR: low (approx. 20–50 API). CALI: near gauge (approx. 8–9 in). LLD/LLS/MSFL: high readings (approx. 100–1000 on the 0.2–2000 scale); significant curve separation; very spiky character | Not labelled |
| 9320–9350 | No lithology column shown | GR: high (approx. 60–100 API). CALI: localised enlargement (approx. 10–12 in). Resistivity curves: low readings (approx. <10); curves close together | Not labelled |
| 9350–9400 | No lithology column shown | GR: low (approx. 20–40 API). CALI: near gauge. Resistivity curves: high readings (approx. 100–1000); curve separation visible | Not labelled |

**Notes:**
- Depth track: major labels at 9300 and 9400 ft; minor tick at approximately 9350 ft; fine gridlines at regular intervals.
- No lithology column and no results panel (porosity, saturation, net pay) are printed on this log.
- Qualitative pattern indicates an alternation of low-GR / high-resistivity intervals (9300–9320, 9350–9400) with a high-GR / low-resistivity interval (9320–9350).

KEYWORDS: well log, gamma ray, caliper, laterolog, LLD, LLS, MSFL, measured depth, resistivity, permeable interval
----


Figure 1.9. Example of dual laterolog curves through a hydrocarbon-bearing zone.

Given: The drilling mud is saltwater based ($R_{ad} - R_w$).

Where saltwater drilling muds invade a hydrocarbon-bearing formation ($S_w << 60\%$), there is low resistivity in the flushed zone ($R_{ad}$), an intermediate resistivity in the invaded zone ($R_i$), and high resistivity in the uninvaded zone ($R_i$). The reason for the increase in resistivities deeper into the formation is because of the increasing hydrocarbon saturation.

See Figure 1.5 for review. (Figure 1.7 shows the response of these resistivity curves in a water-bearing zone.)

Compare the three curves on the right side of the log (tracks 2 and 3). Resistivity increases from left to right.

# Log curve LLD:

Deep laterolog resistivity curves usually measure true formation resistivity ($R_f$), the resistivity of the formation beyond the outer boundary of the invaded zone. In hydrocarbon-bearing zones (in this case from 9306 to 9409 ft), the curve reads a high resistivity because of high hydrocarbon saturation in the uninvaded zone ($R_i$).

# Log curve LLS:

Shallow laterolog resistivity curves measure the resistivity in the invaded zone ($R_i$). In a hydrocarbon-bearing zone, the shallow laterolog (LLS) records a lower resistivity than the deep laterolog (LLD) because the invaded zone ($R_i$) has a lower hydrocarbon saturation than the uninvaded zone ($R_i$)

# Log curve MSFL:

Microspherically focused log resistivity curves measure the resistivity of the flushed zone ($R_{ad}$). In hydrocarbon-bearing zones, the curve records a low resistivity because saltwater mud filtrate has low resistivity and the residual hydrocarbon saturation in the flushed zone ($R_{ad}$) is low. Therefore, in a hydrocarbon-bearing zone with saltwater-based drilling mud, the uninvaded zone ($R_i$) has high resistivity, the invaded zone ($R_i$) has a lower resistivity, and the flushed zone ($R_{ad}$) has the lowest resistivity.
<!-- page 30 -->
Basic Relationships of Well Log Interpretation

19


----
━━━ FORMAT 7: NOMOGRAM / ПАЛЕТКА ━━━
This is a geothermal gradient nomogram (pallete) for calculating formation temperature based on depth and surface temperature.

The nomogram has three axes:
- Left vertical axis: Depth, D (ft × 1000), linear scale, range 0 to 30.
- Top horizontal axis: Formation Temperature, T_f (°C), linear scale, range 16 to 225.
- Bottom horizontal axis: Formation Temperature, T_f (°F), linear scale, range 40 to 450.
- Right vertical axis: Depth, D (m × 1000), linear scale, range 0 to 9.

The family of curves represents constant geothermal gradients, labeled as:
- 0.5, 0.8, 1.0, 1.2, 1.4, 1.6 °F/100 ft
- 1.0, 1.5, 2.0, 2.5, 3.0 °C/100 m

The leftmost point is labeled "Mean Surface Temperature, T_ms" and connects to the depth axis via a diagonal line.

Reading procedure: To find formation temperature at a given depth and surface temperature, draw a line from the surface temperature on the left axis to the depth on the vertical axis. The intersection with a geothermal gradient curve gives the formation temperature on the top or bottom axis.

Anchor points (approximate, for extreme curves):
- For 0.5 °F/100 ft: at D=10 (ft×1000), T_f ≈ 60 °F; at D=20 (ft×1000), T_f ≈ 110 °F.
- For 1.6 °F/100 ft: at D=10 (ft×1000), T_f ≈ 100 °F; at D=20 (ft×1000), T_f ≈ 160 °F.
- For 3.0 °C/100 m: at D=2 (m×1000), T_f ≈ 60 °C; at D=5 (m×1000), T_f ≈ 150 °C.
- For 0.5 °F/100 ft: at D=2 (m×1000), T_f ≈ 50 °C; at D=5 (m×1000), T_f ≈ 80 °C.

The nomogram is designed for quick estimation of subsurface temperature using surface temperature, depth, and assumed geothermal gradient.

KEYWORDS: геотермический градиент, температура пласта, глубина, номограмма, °F/100 ft, °C/100 m, T_ms, T_f, палетка
----


Figure 1.10. Chart for estimating formation temperature ($T_f$) with depth (linear gradient assumed). (Western Atlas International, Inc., 1995, Figure 2-1)
Given:

Surface temperature = 80°F

Bottom hole temperature (BHT) = 200°F

Total depth (TD) = 10,000 ft

Formation depth = 7000 feet

# Procedure:

1. Locate BHT (200°F) on the 80 scale (bottom of the chart; mean surface temperature = 80°F).
2. Follow BHT (200°F) vertically up until it intersects the 10,000 ft (TD) line. This intersection defines the temperature gradient.
3. Move parallel to the (diagonal) temperature gradient line up to 7000 ft (formation depth).
4. Formation temperature (164°F) is read on the bottom scale (i.e., 80 scale) vertically down from the point where the 7000 ft line intersects the temperature gradient.

NOTE: In the United States (as an example), 80°F is used commonly as the mean surface temperature in the southern states, and 60°F is used commonly in the northern states. However, a specific mean surface temperature can be calculated if such precision is desired. Another source for mean surface-temperature gradients is any world atlas with such listings.
<!-- page 31 -->
20

ASQUITH AND KRYGOWSKI

Figure 1.11. Chart for adjusting fluid resistivities for temperature. (Schlumberger, 1998, Figure Gen-9.)

Given:

Resistivity of drilling mud (Rdr) equals 1.2 ohm-m at 75°F. Formation temperature (Tf) = 160°F.

Procedure:

1. Locate the resistivity value, 1.2 ohm-m, on the scale at the left of the chart.
2. Move to the right horizontally along the 1.2 ohm-m line until the vertical line representing a temperature of 75°F (from the bottom of the chart) is encountered (point A on the chart).
3. Move parallel to the (diagonal) constant salinity line to where it intersects the vertical line representing a temperature value of 160°F (point B on the chart).
4. From point B, follow the horizontal line to the left to determine the resistivity of the fluid at the desired temperature (0.58 ohm-m at 160°F).

Each diagonal line on the chart shows the resistivity of a solution of fixed concentration over a range of temperatures. The diagonal lines at the bottom of the chart indicate that an NaCl solution can hold no more than 250,000 to 300,000 ppm NaCl depending on temperature (i.e., the solution is completely salt saturated).


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
This is a nomogram-style chart showing the relationship between gas solubility in oil and temperature, with pressure as a parameter.

- **X-axis (horizontal):** Temperature, with dual scales:
  - Left scale: °F, range 50 to 400
  - Bottom scale: °C, range 10 to 200
  - Scale type: linear

- **Y-axis (vertical, left):** Solubility of solution (gas in oil), unit: mm³/mm³ (or equivalently, volume of gas per volume of oil), range 0.01 to 8 (logarithmic scale).

- **Right Y-axis (vertical):** Naphtha concentration, unit: ppm or grains/gal, range 0 to 20,000 (linear scale). This axis is labeled "Naphtha concentration (ppm or grains/gal)" and is aligned with the solubility axis.

- **Family of curves:** The chart contains a family of diagonal lines, each representing a constant pressure. The pressure values are labeled along the right side of the chart, ranging from 200 psi to 10,000 psi, with intermediate values at 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2500, 3000, 4000, 5000, 6000, 7000, 8000, 9000, and 10,000 psi. The lines are labeled with their pressure values (e.g., "200 psi", "400 psi", etc.).

- **Two marked data points:**
  - Point A: Located at approximately 100°F (38°C) and 1.0 mm³/mm³ solubility, corresponding to ~2000 psi pressure.
  - Point B: Located at approximately 150°F (66°C) and 0.5 mm³/mm³ solubility, corresponding to ~4000 psi pressure.

- **Equation at top:** "Convection approximated by Rg = R1[(T1 + 6.77)/(Tg + 6.77)]^F or Rg = R1[(T1 + 21.5)/(Tg + 21.5)]^F" — this appears to be a formula for gas solubility (Rg) as a function of temperature (T1, Tg) and a factor F, with R1 as a reference solubility. The units for temperature in the formula are not specified, but the chart uses °F.

- **Reading procedure:** To use the chart, locate the temperature on the x-axis, move vertically to the curve corresponding to the pressure (from the right-side labels), and read the solubility on the left y-axis (or naphtha concentration on the right y-axis).

- **Trend:** Gas solubility in oil decreases with increasing temperature at constant pressure. At higher pressures, gas solubility is higher for a given temperature. The relationship is approximately linear on this log-linear plot for each pressure curve.

> Тренд: С увеличением температуры растворимость газа в нефти уменьшается при постоянном давлении. При более высоких давлениях растворимость газа выше для данной температуры.

KEYWORDS: газовая растворимость, температура, давление, нефть, номограмма, ppm, grains/gal, mm³/mm³, PVT, фазовые свойства
----


<!-- page 32 -->
2

Asquith, G., and D. Krygowski, 2004, Spontaneous Potential, in G. Asquith and D. Krygowski, Basic Well Log Analysis: AAPG Methods in Exploration 16, p. 21-30.

# Spontaneous Potential

## GENERAL

The spontaneous potential (SP) log was one of the earliest measurements used in the petroleum industry, and it has continued to play a significant role in well log interpretation. Most wells today have this type of log included in their log suites. Primarily, the SP log is used for determining gross lithology (i.e., reservoir vs. nonreservoir) through its ability to distinguish permeable zones (such as sandstones) from impermeable zones (such as shales). It is also used to correlate zones between wells. However, as will be discussed later in this chapter, the SP log has several other uses that are perhaps equally important.

The SP log is a record of direct current (DC) voltage (or *potential*) that develops naturally (or *spontaneously*) between a moveable electrode in the well bore and a fixed electrode located at the surface (Doll, 1948). It is measured in millivolts (mV). Electric voltages arising primarily from electrochemical factors within the borehole and the adjacent rock create the SP log response. These electrochemical factors are brought about by differences in salinities between mud filtrate and formation water within permeable beds. Salinity of a fluid is inversely proportional to its resistivity, and in practice salinity is indicated by mud filtrate resistivity ($R_{mf}$) and formation water resistivity ($R_w$). Because a conductive fluid is needed in the borehole for the generation of these voltages, the SP cannot be used in nonconductive (e.g., oil-base) drilling muds or in air-filled holes.

The SP log is usually recorded on the left track of the log (track 1) and is used to

- detect permeable beds
- detect boundaries of permeable beds
- determine formation-water resistivity \((R_{w})\)
- determine the volume of shale in permeable beds

An auxiliary use of the SP curve is in the detection of hydrocarbons by the suppression of the SP response.

The concept of static spontaneous potential (SSP) is important because SSP represents the maximum SP that a thick, shale-free, porous, and permeable formation can have for a given ratio between $R_{mf}$ and $R_w$. SSP is determined by formula or chart and is a necessary element for determining accurate values of $R_w$ and volume of shale. The measured SP value is influenced by bed thickness, bed resistivity, borehole diameter, invasion, shale content, hydrocarbon content, and most important: the ratio of $R_{mf}$ to $R_w$ (Figure 2.1A).

## Bed Thickness

In a thin formation (i.e., less than about 10 ft [3 m] thick), the measured SP is less than SSP (Figure 2.1B). However, the SP curve can be corrected by chart for the effects of bed thickness. As a general rule, whenever the SP curve is narrow and pointed, the SP should be corrected for bed thickness before being used in the calculation of $R_w$.

## Bed Resistivity

Higher resistivities reduce the deflection of the SP curves.

## Borehole and Invasion

Hilchie (1978) indicates that the effects of borehole diameter and invasion on the SP log are very small and, in general, can be ignored.

## Shale Content

The presence of shale in a permeable formation reduces the SP deflection (Figure 2.1B). In water-bear-

21
<!-- page 33 -->
22

ASQUITH AND KRYGOWSKI

ing zones, the amount of SP reduction is related to the amount of shale in the formation.

## Hydrocarbon Content

In hydrocarbon-bearing zones, the SP deflection is reduced. This effect is called hydrocarbon suppression (Hilchie, 1978). Hydrocarbon suppression of the SP is a qualitative phenomenon, and cannot be used to determine the hydrocarbon saturation of the formation.

The SP response of shales is relatively constant and follows a straight line called a shale baseline. The SP value of the shale baseline is assumed to be zero, and SP curve deflections are measured from this baseline. Permeable zones are indicated where there is SP deflection from the shale baseline. For example, if the SP curve moves either to the left (negative deflection; $R_{mf} > R_w$) or to the right (positive deflection; $R_{mf} < R_w$) of the shale baseline, permeable zones are present.

Permeable bed boundaries are placed at the points of inflection from the shale baseline.

Note that when recording through impermeable zones or through permeable zones where $R_{mf}$ is equal to $R_w$, the SP curve does not deflect from the shale baseline. The magnitude of SP deflection is due to the difference in salinity between mud filtrate and formation water and not to the amount of permeability. This salinity difference produces a difference in the resistivities of the mud filtrate ($R_{mf}$) and formation water ($R_w$).

Over long intervals (several hundreds to thousands of feet), the SP baseline can drift, either in the positive or negative direction. While this is of little consequence when making calculations local to a specific formation, it may introduce errors if the SP magnitude is being calculated over that long interval, especially by means of a computer. Accordingly, the baseline drift can be removed (many programs have such editing routines) so that the SP baseline retains a constant value (usually set to zero) over the length of the logged interval.

## FORMATION WATER RESISTIVITY ($R_w$) DETERMINATION

Figure 2.2 is an induction electric log with an SP curve from a Pennsylvanian upper Morrow sandstone in Beaver County, Oklahoma. In this example, the SP curve is used to find a value for $R_w$ by the following procedure:

1. After determining the formation temperature, correct the resistivities of the mud filtrate ($R_{mf}$) and drilling mud ($R_m$) (obtained from the log heading) to formation temperature (see Chapter 1).
2. To minimize the effect of bed thickness, the SP is corrected to static SP (SSP). SSP represents the maximum SP a formation can have if unaffected by bed thickness. Figure 2.3 is a chart used to correct SP to SSP. The data necessary to use this chart are:

- bed thickness,
- resistivity from the shallow-reading resistivity tool ($R_i$)
- the resistivity of the drilling mud ($R_m$) at formation temperature

3. Once the value of SSP is determined, it is used on the chart illustrated in Figure 2.4 to obtain a value for the $R_{mf}/R_{we}$ ratio. Equivalent resistivity ($R_{we}$) is obtained by dividing $R_{mf}$ by the $R_{mf}/R_{we}$ value from the chart (Figure 2.4).

4. The value of $R_{we}$ is then corrected to $R_w$, using the chart illustrated in Figure 2.5, for average deviation from sodium chloride solutions, and for the influence of formation temperature.

A careful examination of Figures 2.2 to 2.5 should help you gain an understanding of the procedure to determine $R_w$ from the SP. But, rather than using charts in the procedure, you might prefer using the mathematical formulas listed in Table 2.1.

It is important to remember that normally the SP curve has less deflection in hydrocarbon-bearing zones (i.e., hydrocarbon suppression). Using a hydrocarbon-bearing zone to calculate $R_w$ results in too high a value for $R_w$ calculated from SSP. Using a too-high value of $R_w$ in Archie's equation to determine water saturation produces a value of $S_w$ that is also too high, creating the chance for missed production in the interpretive process. Therefore, to determine $R_w$ from SP it is best, whenever possible, to use the SP curve produced by a zone that is known to contain only water.
<!-- page 34 -->
Spontaneous Potential 23

Table 2.1. Mathematical Calculation of $R_w$ from SSP, for temperatures in °F (after Western Atlas Logging Services, 1985).

|  Identify a zone on the logs that is clean, wet, and permeable. Pick the maximum value for SP in the zone. |   |
| --- | --- |
|  Calculate formation temperature at the depth of the SP value. $AMST$ = Annual Mean Surface Temperature $BHT$ = Bottom Hole Temperature $FD$ = Formation Depth $T_f$ = formation temperature | $T_f = \left( \frac{BHT - AMST}{TD} \times FD \right) + AMST$  |
|  Convert $R_{mf}$ from surface (measured) temperature to formation temperature. $R_{mf} = R_{mf}$ at formation temperature $R_{mfsurf} = R_{mf}$ at measured temperature $T_{surf}$ = Measured temperature of $R_{mf}$ | $R_{mf} = \frac{R_{mfsurf}(T_{surf} + 6.77)}{T_f + 6.77}$  |
|  Find the equivalent formation water resistivity, $R_{we}$, from the SP and $R_{mf}$. $R_{we}$ = equivalent $R_w$ | $R_{we} = R_{mf} \times 10^{SP/(61+0.133-BHT)}$  |
|  Convert $R_{we}$ to $R_w$ (this value is at formation temperature). | $R_w = \frac{R_{we} + 0.131 \times 10^{\left( \frac{1}{\log(BHT/19.9)} \right)^{-2}}}{-0.5 \times R_{we} + 10^{\left( \frac{0.0426}{\log(BHT/50.8)} \right)}}$  |

### SHALE VOLUME CALCULATION

The volume of shale in a sand can be used in the evaluation of shaly sand reservoirs (Chapter 6) and as a mapping parameter for both sandstone and carbonate facies analysis (Chapter 7). The SP log can be used to calculate the volume of shale in a permeable zone by the following formula:

$$V_{shale} = 1.0 - \frac{PSP}{SSP} \tag{2.1}$$

where:

$V_{shale}$ = volume of shale

$PSP$ = pseudostatic spontaneous potential (maximum SP of shaly formation)

$SSP$ = static spontaneous potential of a nearby thick clean sand

Or, alternately:

$$V_{shale} = \frac{PSP - SSP}{SP_{shale} - SSP} \tag{2.2}$$

where:

$V_{shale}$ = volume of shale

$PSP$ = pseudostatic spontaneous potential (maximum SP of shaly formation)

$SSP$ = static spontaneous potential of a nearby thick clean sand

$SP_{shale}$ = value of SP in a shale (usually assumed to be zero)
<!-- page 35 -->
24

ASQUITH AND KRYGOWSKI

# REVIEW

1. The spontaneous potential log (SP) can be used to

- detect permeable beds
- detect boundaries of permeable beds
- determine formation water resistivity ($R_w$)
- determine volume of shale ($V_{shale}$) in a permeable bed

2. The variations in the SP are the result of an electric potential that is present between the well bore and the formation as a result of differences in salinities between mud filtrate and formation water. This salinity difference produces a resistivity difference between $R_{mf}$ and $R_w$.

3. The SP response in shales is relatively constant, and a vertical line drawn along the SP response in a shale is referred to as the shale baseline. In permeable beds, the SP has the following responses relative to the shale baseline:

- negative deflection (to the left of the shale baseline) where $R_{mf} > R_w$
- positive deflection (to the right of the shale baseline) where $R_{mf} < R_w$
- no deflection where $R_{mf} = R_w$

4. The SP response can be suppressed by thin beds, shaliness, and the presence of hydrocarbons.

Throughout this text, italics are used to indicate variable names with numeric values. The notation SP is the abbreviation for spontaneous potential, and the variable SP indicates the numerical value (in mV) taken from the SP log.
<!-- page 36 -->
Spontaneous Potential

25


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━

Schematic SP (self-potential) log illustrating the effect of the mud filtrate/formation water resistivity contrast on the SP curve relative to the shale baseline.

Vertical axis: depth, increasing downward; no depth scale or units printed.
Horizontal axis at top: SP deflection direction, labelled "–" (left) and "+" (right) relative to the "Shale Baseline".

Track 1 (left): SP curve — solid line. The "Shale Baseline" is a vertical reference line. Deflection to the left of the baseline (toward "–") is a negative SP anomaly; deflection to the right (toward "+") is a positive SP anomaly.
Track 2 (right): interval column — alternating unshaded (white) and shaded (gray) rectangular blocks. The shaded blocks correspond to intervals in which the SP responds; the white blocks separate them. No lithology legend is provided inside the image, so lithology is not determined (литология не определяется без легенды).

Interval table (top to bottom):

| Interval | Column block | SP curve behaviour | Printed label |
|---|---|---|---|
| 1 | White | At shale baseline (no deflection) | — |
| 2 | Gray | At shale baseline (no deflection) | R_mf = R_w |
| 3 | White | Return to shale baseline | — |
| 4 | Gray | Deflection to the left (negative anomaly) | R_mf > R_w |
| 5 | White | Return to shale baseline | — |
| 6 | Gray | Deflection to the left, greater amplitude (stronger negative anomaly) | R_mf >> R_w |
| 7 | White | Return to shale baseline | — |
| 8 | Gray | Deflection to the right (positive anomaly) | R_mf < R_w |

Interpretation: the figure demonstrates that the direction and magnitude of the SP deflection relative to the shale baseline depend on the ratio of mud filtrate resistivity (R_mf) to formation water resistivity (R_w). When R_mf = R_w, no SP is generated; when R_mf > R_w or R_mf >> R_w, the SP deflects negatively (to the left); when R_mf < R_w, the SP deflects positively (to the right).

KEYWORDS: SP log, self-potential, shale baseline, mud filtrate resistivity, formation water resistivity, Rmf, Rw, well logging, resistivity contrast
----


2.1A


━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Schematic SP (spontaneous potential) log with lithology column. 
Vertical axis: no depth scale is printed; intervals are shown schematically from top to bottom.
Horizontal axis: SP deflection, from negative ("−") on the left to positive ("+") on the right.
Shale baseline: dashed vertical line.
Condition printed at top right: "Rmf >> Rx for all sands" — SP curves deflect to the negative side for all sand intervals.

Tracks (left to right):
1. SP curve (solid black line), labelled with response types: SSP, SP, PSP, SP, PSP (top to bottom).
2. Lithology column: stippled (dotted) rectangles, each with a printed lithology label.

Interval table (top to bottom):

| № | Curve label | Curve behaviour | Lithology (printed in column) | Interpretation |
|---|---|---|---|---|
| 1 | SSP | Blocky, maximum negative deflection from shale baseline | Thick clean wet sand | Static spontaneous potential; clean, thick, water-bearing sand |
| 2 | SP | Concave (bell-shaped), reduced negative deflection | Thin sand | SP reduced by thin-bed effect |
| 3 | PSP | Blocky, small negative deflection | Thick shaly wet sand | Pseudo static spontaneous potential; shaliness reduces SP |
| 4 | SP | Blocky, moderate negative deflection (less than SSP, greater than PSP) | Thick clean gas sand | SP reduced by gas effect (higher resistivity) |
| 5 | PSP | Blocky, small negative deflection | Thick shaly gas sand | Pseudo static spontaneous potential; combined shaliness + gas effect |

KEYWORDS: SP log, spontaneous potential, SSP, PSP, shale baseline, clean sand, shaly sand, gas sand, thin bed, Rmf, lithology column


2.1B

Figure 2.1. Examples of SP deflection from the shale baseline.

2.1A. SP deflection with different resistivities of mud filtrate ($R_{mf}$) and formation water ($R_w$). Where resistivity of the mud filtrate ($R_{mf}$) is equal to the resistivity of the formation water ($R_w$), there is no deflection, positive or negative, from the shale baseline.

Where $R_{mf}$ is greater than $R_w$, the SP deflects to the left of the shale baseline (negative deflection). Where $R_{mf}$ greatly exceeds $R_w$, the deflection is proportionately greater. This is often called a normal SP.

Where $R_{mf}$ is less than $R_w$, the SP deflects to the right of the shale baseline (positive deflection). This condition, often called a reversed SP, is produced by a formation containing fresh water.

Remember, the SP log can used only with conductive (i.e., saltwater base or freshwater base) drilling muds. This log does not work with oil-base muds or in air-filled holes.

2.1B. SP deflection with resistivity of the mud filtrate ($R_{mf}$) much greater than formation water ($R_w$). SSP (static spontaneous potential) at the top of the diagram, is the maximum deflection possible in a thick, shale-free, and water-bearing (wet) sandstone for a given ratio of $R_{mf}/R_w$. All other deflections are less and are relative in magnitude.

SP shows the SP response due to the presence of thin beds and/or the presence of gas.

PSP (pseudostatic spontaneous potential) is the SP response if shale is present.

The formula for the theoretical calculated value of SSP is given:

$$SSP = -K \times \log(R_{mf} / R_w) \tag{2.2}$$

where:

$$K = (0.133 \times T_f) + 60 \tag{2.3}$$
<!-- page 37 -->
26

ASQUITH AND KRYGOWSKI


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━

**Depth axis:** Feet MD (measured depth in feet). Depth increases downward. Visible depth range approximately 7380–7520 ft, with printed depth ticks at 7400 ft and 7500 ft. Grid divisions: 10 ft between minor gridlines.

**Track 1 (left): SP — spontaneous potential**
- Curve: SP, single solid line.
- Scale: −160 to 40 mV, linear, increasing left-to-right.

**Track 2 (right): CILD — deep induction resistivity**
- Curves: IL (deep induction) and SN (short normal), both solid lines.
- Scale: 1000 to 0 ohm.m, linear, decreasing left-to-right (high resistivity at left, low resistivity at right). Labeled scale values: 1000 (left edge), 50 (near right), 0 (right edge).

**Interval table:**

| Interval, ft | Lithology (from column) | SP: curve behavior | IL: curve behavior | SN: curve behavior | Interpretation (if labeled) |
|---|---|---|---|---|---|
| 7400–7440 | Not shown | Near baseline (≈ 0 to −20 mV), stable | High resistivity (≈ 1000 ohm.m), stable | Moderate resistivity (approximately 100–200 ohm.m), spiky | Not labeled |
| 7440–7490 | Not shown | Negative anomaly (deflection left), maximum deflection around 7460–7470 ft | Sharp decrease in resistivity, approaching 0 ohm.m, forming a pronounced low-resistivity zone | Low resistivity values, spiky | Not labeled |
| 7490–7500 | Not shown | Returns to baseline | Returns to high resistivity (≈ 1000 ohm.m) | Moderate resistivity values, spiky | Not labeled |

**Notes:**
- No lithology column is shown on the log; lithology cannot be determined from this image.
- No bed boundaries, perforation intervals, or fluid contacts are explicitly marked.
- Sign convention: SP negative values to the left, positive to the right; CILD high resistivity to the left, low to the right.

KEYWORDS: well log, SP, CILD, induction log, SN, resistivity, spontaneous potential, ohm.m, mV, measured depth
----


<!-- page 38 -->
Spontaneous Potential

27

Figure 2.2. Determination of formation water resistivity ($R_m$) from an SP log. This example uses the charts on Figures 2.3 through 2.5.

Given:

$R_{mf} = 0.51 \text{ ohm-m at } 135^{\circ}\text{F (BHT)}$

$R_m = 0.91 \text{ ohm-m at } 135^{\circ}\text{F (BHT)}$

Surface temperature = 60°F

Total depth = 8007 ft

Bottom hole temperature (BHT) = 135°F

From the log:

Formation depth at maximum SP deflection is 7446 ft.

The maximum SP deflection in the sand coincides with -50 mV on the log scale, and the shale base line is at -5 mV. Note that the SP scale goes from -160 mV on the left to +40 mV on the right and has 20 mV per division.

Bed thickness is 8 ft (7442 to 7450 ft).

Short-normal (SN) resistivity ($R_f$) is 33 ohm-m. The short-normal (or 16-inch normal) log measures the shallow formation resistivity (i.e., the resistivity of the invaded zone, $R_f$).

Procedure:

1. Determine $T_f$.

Use Figure 1.10 and the information above to calculate the formation temperature ($T_f$).

$T_f = 130^{\circ}\text{F}$.

2. Correct $R_m$ and $R_{mf}$ to $T_f$.

Use Figure 1.11 and the information above to correct $R_m$ and $R_{mf}$ to formation temperature.

$R_m = 0.94 \text{ ohm-m at } 130^{\circ}\text{F and } R_{mf} = 0.53 \text{ ohm-m at } 130^{\circ}\text{F}$.

3. Determine SP.

Read the maximum deflection directly from the SP curve in Figure 2.2. In this case, because the SP baseline has a nonzero value (-5 mV), its value must be subtracted from the value of the SP curve.

The SP value is: SP (read from log) - baseline value = (-50 mV) - (-5 mV) = -45 mV

$SP = -45 \text{ mV}$.

4. Correct SP to SSP (correct for a thin bed):

See the procedure in Figure 2.3

$SSP = -59 \text{ mV}$

5. Determine $R_{mf} / R_{we}$ ratio, and from that, determine $R_{we}$:

See the procedure in Figure 2.4

$R_{we} = 0.096 \text{ ohm-m}$

6. Correct $R_{we}$ to $R_w$:

Use the chart in Figure 2.5, and the $R_{we}$ value in step 6

$R_w = 0.10 \text{ ohm-m at } T_f$
<!-- page 39 -->
28

ASQUITH AND KRYGOWSKI


━━━ FORMAT 7: NOMOGRAM / ПАЛЕТКА ━━━

**SP Correction Factor Chart** (Courtesy Baker Atlas, © 1996-1999 Baker Hughes, Inc.)

**Purpose:** graphical determination of the SP correction factor for bed thickness and conversion of a measured SP log value to the static spontaneous potential (SSP).

**Axes:**
- **Left vertical axis:** Bed Thickness, ft — linear scale, range 3–30 ft. Labeled ticks: 3, 4, 5, 6, 7, 8, 10, 15, 20, 30.
- **Right vertical axis:** Bed Thickness, m — linear scale, range 1–9 m. Labeled ticks: 1, 1.5, 2, 2.5, 3, 3.5, 4, 5, 6, 7, 8, 9.
- **Bottom horizontal axis:** SP Correction Factor — logarithmic scale, range 1.0–10.0. Labeled ticks: 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0.
- **Top inset, left scale:** SP from Log — linear scale, range 20–120. Labeled ticks: 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120.
- **Top inset, diagonal scale:** SP Correction Factor — logarithmic scale, range 1.0–5.0. Labeled ticks: 1.0, 1.2, 1.3, 1.4, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0.
- **Top inset, right scale:** SSP — linear scale, range 20–120. Labeled ticks: 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120.

**Family of curves (main plot):**
parameter **R_i / R_m** (ratio of formation resistivity to mud filtrate resistivity).
Labeled curves from leftmost to rightmost: **5, 20, 50, 100, 200**.

**Reading procedure:**
1. Enter the chart on the left axis with bed thickness (ft), draw a horizontal line to the intersection with the curve for the given R_i / R_m ratio.
2. From the intersection, drop vertically down to the bottom axis and read the SP Correction Factor.
3. On the top inset, from the "SP from Log" value, move horizontally right to the diagonal "SP Correction Factor" line at the found correction-factor value; from that intersection, move vertically up to the "SSP" scale and read the static spontaneous potential.

**Demonstrated example (shown with blue annotation):**
- Entry: bed thickness = 8 ft (left axis), R_i / R_m = 5.
- Horizontal blue line from 8 ft to the R_i / R_m = 5 curve.
- Vertical blue line down to the bottom axis: SP Correction Factor ≈ 1.5.
- Blue arrow in the inset points from the diagonal correction-factor value of 1.5 toward the SSP scale (direction of the final reading step).

**Anchor points for the extreme curves (ориентировочно / approx.):**
- R_i / R_m = 5 curve: at bed thickness 8 ft → SP Correction Factor ≈ 1.5; at 30 ft → ≈ 1.05.
- R_i / R_m = 200 curve: at bed thickness 3 ft → ≈ 3.0; at 30 ft → ≈ 1.05.

KEYWORDS: SP log, spontaneous potential, static spontaneous potential, SSP, correction factor, bed thickness, R_i/R_m, nomogram, Baker Atlas, well log interpretation

----


Figure 2.3. SP bed-thickness correction to determine SSP from SP. (Western Atlas, 1995, Figure 3-1)

Procedure, using the values from the log in Figure 2.2:

1. Calculate the ratio $R_i/R_m$ using the values determined in Figure 2.2, where $R_i$ is equal to the short-normal (SN) resistivity and $R_m$ is the value determined at formation temperature.

$R_i = SN = 34 \text{ ohm}\cdot\text{m}$

$R_m = 0.94 \text{ ohm}\cdot\text{m}$

$R_i/R_m = 36$

2. Locate a bed thickness on the vertical scale. Bed thickness = 8 ft.

3. Follow the bed-thickness value horizontally across until it intersects the $R_i/R_m$ curve.

(Because $R_i/R_m = 36$, the point lies between the $R_i/R_m = 20$ and the $R_i/R_m = 50$ curves.)

3. Drop vertically from this intersection and read the SP correction factor on the scale across the bottom.

SP correction factor is approximately 1.3.

4. Multiply SP by the SP correction factor to find SSP.

$SSP = SP \times \text{correction factor}$

$SSP = -45 \text{ mV} \times 1.3$ (SP value taken at 7446 ft, see Figure 2.2)

$SSP = -59 \text{ mV}$

The nomogram in the upper right part of this figure also gives SSP. Draw a straight line from 45 on the SP scale on the left side of the nomogram through 1.3 on the diagonal SP correction factor scale. Continue this straight line to where it crosses the SSP scale at 59 mV. Remember that the SP value is negative, so the SSP value is also negative.
<!-- page 40 -->
Spontaneous Potential 29


----
━━━ FORMAT 7: NOMOGRAM / ПАЛЕТКА ━━━

**Static Spontaneous Potential (SSP) interpretation chart**

**Axes:**
- **Ordinate (vertical):** Static Spontaneous Potential, SSP (mv). Linear scale, range from −200 mv (top edge) to +75 mv (bottom edge). The axis is inverted — SSP values increase downward. Labelled major grid lines every 25 mv: −200, −175, −150, −125, −100, −75, −50, −25, 0, 25, 50, 75.
- **Abscissa (horizontal):** R_mf/R_eq — dimensionless resistivity ratio (mud filtrate to equivalent formation water). Logarithmic scale, range 0.3 to 30.0. Labelled major ticks: 0.3, 0.5, 1.0, 3.0, 5.0, 10.0, 30.0.

**Family parameter:** Formation temperature.
**Full list of labelled curve values (top to bottom):**
- 500°F / 250°C
- 400°F / 200°C
- 300°F / 150°C
- 100°C / 200°F
- 50°C / 100°F

All curves converge at a common point: (R_mf/R_eq = 1.0, SSP = 0 mv).

**Reading procedure:** From the known R_mf/R_eq value on the abscissa, move vertically upward to the curve corresponding to the formation temperature, then move horizontally left to read the SSP on the ordinate. The blue arrow example on the chart illustrates this: at R_mf/R_eq = 10.0, using the 100°C/200°F curve, SSP ≈ −70 mv.

**Anchor points for extreme curves (read off the grid, approximate):**
- **500°F/250°C curve (top):** (R_mf/R_eq = 1.0, SSP = 0 mv) → (10.0, ≈ −130 mv) → (30.0, ≈ −190 mv)
- **50°C/100°F curve (bottom):** (R_mf/R_eq = 1.0, SSP = 0 mv) → (10.0, ≈ −55 mv) → (30.0, ≈ −80 mv)

**Curve behaviour:** For R_mf/R_eq > 1.0, SSP is negative and its magnitude increases with increasing R_mf/R_eq and with increasing temperature. For R_mf/R_eq < 1.0, SSP becomes positive. The chart contains no auxiliary nomographic scales beyond the two plotted axes.

KEYWORDS: SSP, static spontaneous potential, Rmf/Req, mud filtrate resistivity, formation temperature, SP log interpretation, well logging, nomogram
----


Courtesy Baker Atlas, © 1996-1999 Baker Hughes, Inc.

Figure 2.4. Chart used for determining the $R_{\text{std}}/R_{\text{we}}$ ratio from SSP values. (Western Atlas, 1995, Figure 3-2)

Procedure, using the log data in Figure 2.2 and the values from Figure 2.3:

1. Locate the SSP value on the scale on the left edge of the chart.
$SSP = -59 \text{ mV}$
2. Follow the value horizontally until it intersects the sloping formation temperature line (130°F; imagine a line between the 100°F and 200°F temperature lines).
3. Move vertically from this intersection and read the ratio value on the scale at the bottom of the chart.

The $R_{\text{std}}/R_{\text{we}}$ ratio value is 5.5

4. Divide the corrected value for $R_{\text{std}}$ by the ratio $R_{\text{std}}/R_{\text{we}}$ value.

$R_{\text{we}} = R_{\text{std}}/(R_{\text{std}}/R_{\text{we}})$

$R_{\text{we}} = 0.53/5.5$

$R_{\text{we}} = 0.096 \text{ ohm-m}$
<!-- page 41 -->
30

ASQUITH AND KRYGOWSKI


----
━━━ FORMAT 7: NOMOGRAM / ПАЛЕТКА ━━━
**Palette name:** Formation water resistivity (\(R_w\)) / mud filtrate resistivity (\(R_{mf}\)) to equivalent resistivity at 75°F (\(R_{we}\) / \(R_{mfe}\)) conversion nomogram. Labelled "English" (unit system). Courtesy Baker Atlas, © 1996-1999 Baker Hughes, Inc.

**Axes:**
- X-axis: \(R_w\) or \(R_{mf}\), Ω·m — logarithmic scale, range 0.005 to 2.
- Y-axis: \(R_{we}\) or \(R_{mfe}\), Ω·m — logarithmic scale, range 0.001 to 2.

**Family parameter:** Temperature (°F). Labelled values: 75°F, 100°F, 150°F, 200°F, 300°F, 400°F, 500°F.

**Curve families:**
1. "NaCl at 75°F" — straight-line curves (upper-right region).
2. "Saturation" — curved lines (lower-left region).

**Reading procedure (indicated by the blue arrows):** Enter the chart at the known \(R_w\) (or \(R_{mf}\)) on the x-axis, move vertically to the curve of the appropriate temperature, then read \(R_{we}\) (or \(R_{mfe}\)) on the y-axis. The blue arrows demonstrate one conversion: \(R_w \approx 0.08\) Ω·m ↔ \(R_{we} \approx 0.075\) Ω·m via the 75°F curve (intersection at ≈ (0.08; 0.075)).

**Anchor points (approximate, read from the grid):**
- NaCl, 75°F (reference): (\(R_w = 0.1\), \(R_{we} = 0.1\)); (\(R_w = 2\), \(R_{we} = 2\)).
- NaCl, 500°F: (\(R_w = 0.1\), \(R_{we} \approx 0.005\)); (\(R_w = 2\), \(R_{we} \approx 0.07\)).
- Saturation, 75°F: (\(R_w = 0.02\), \(R_{we} \approx 0.02\)); (\(R_w = 0.1\), \(R_{we} \approx 0.1\)).
- Saturation, 500°F: (\(R_w = 0.02\), \(R_{we} \approx 0.002\)); (\(R_w = 0.1\), \(R_{we} \approx 0.006\)).

KEYWORDS: nomogram, palette, formation water resistivity, mud filtrate resistivity, Rwe, Rmfe, temperature correction, log interpretation, Baker Atlas, 75°F
----


Figure 2.5. Chart for determining the value of $R_w$ from $R_{we}$. (Western Atlas, 1995, Figure 3-3)

Procedure, using the values from Figure 2.4:

1. Locate the value of $R_{we}$ on the vertical scale. $R_{we} = 0.096$ ohm·m
2. Follow it horizontally until it intersects the temperature curve desired. 130°F lies between the 100°F and 150°F temperature curves.
3. Drop vertically from the intersection and read a value for $R_w$ on the scale at the bottom.

$R_w = 0.10$ ohm·m
<!-- page 42 -->
3

Asquith, G., and D. Krygowski, 2004, Gamma Ray, in G. Asquith and D. Krygowski, Basic Well Log Analysis: AAPG Methods in Exploration 16, p. 31–35.

# Gamma Ray

## GENERAL

Gamma ray (GR) logs measure the natural radioactivity in formations and can be used for identifying lithologies and for correlating zones. Shale-free sandstones and carbonates have low concentrations of radioactive material and give low gamma ray readings. As shale content increases, the gamma ray log response increases because of the concentration of radioactive material in shale. However, clean sandstone (i.e., with low shale content) might also produce a high gamma ray response if the sandstone contains potassium feldspars, micas, glauconite, or uranium-rich waters.

In zones where the geologist is aware of the presence of potassium feldspars, micas, or glauconite, a spectral gamma ray log can be run in place of the standard the gamma ray log. The spectral gamma ray log records not only the number of gamma rays emitted by the formation but also the energy of each, and processes that information into curves representative of the amounts of thorium (Th), potassium (K), and uranium (U) present in the formation.

If a zone has a high potassium content coupled with a high gamma ray log response, the zone might not be shale. Instead, it could be a feldspathic, glauconitic, or micaceous sandstone.

Like the SP log, gamma ray logs can be used not only for correlation, but also for the determination of shale (clay) volumes. These volumes are essential in calculating water saturations in shale-bearing formations by some shaly-sand techniques. Unlike the SP log, the gamma ray response is not affected by formation water resistivity ($R_w$), and because the gamma ray log responds to the radioactive nature of the formation rather than the electrical nature, it can be used in cased holes and in open holes containing nonconducting drilling fluids (i.e., oil-based muds or air).

The gamma ray log is usually displayed in the left track (track 1) of a standard log display, commonly with a caliper curve. Tracks 2 and 3 usually contain

porosity or resistivity curves. Figure 3.1 is an example of such a display.

## SHALE VOLUME CALCULATION

Because shale is usually more radioactive than sand or carbonate, gamma ray logs can be used to calculate volume of shale in porous reservoirs. The volume of shale expressed as a decimal fraction or percentage is called $V_{shale}$. This value can then be applied to the analysis of shaly sands (see Chapter 7).

Calculation of the gamma ray index is the first step needed to determine the volume of shale from a gamma ray log:

$$I_{GR} = \frac{GR_{\log} - GR_{\min}}{GR_{\max} - GR_{\min}} \tag{3.1}$$

where:

$I_{GR}$ = gamma ray index

$GR_{log}$ = gamma ray reading of formation

$GR_{min}$ = minimum gamma ray (clean sand or carbonate)

$GR_{max}$ = maximum gamma ray (shale)

Unlike the SP log, which is used in a single linear relationship between its response and shale volume, the gamma ray log has several nonlinear empirical responses as well as a linear response. The nonlinear responses are based on geographic area or formation age, or if enough other information is available, chosen to fit local information. Compared to the linear response, all nonlinear relationships are more optimistic; that is, they produce a shale volume value lower than that from the linear equation. For a first-order estimation of shale volume, the linear response, where $V_{shale} = I_{GR}$, should be used.

31
<!-- page 43 -->
32

ASQUITH AND KRYGOWSKI

The nonlinear responses, in increasing optimism (lower calculated shale volumes), are:

Larionov (1969) for Tertiary rocks:

$$V_{sh} = 0.083(2^{3.7 I_{GR}} - 1) \tag{3.2}$$

Steiber (1970):

$$V_{sh} = \frac{I_{GR}}{3 - 2 \times I_{GR}} \tag{3.3}$$

Clavier (1971):

$$V_{sh} = 1.7 - [3.38 - (I_{GR} - 0.7)^2]^{\frac{1}{2}} \tag{3.4}$$

Larionov (1969) for older rocks:

$$V_{sh} = 0.33 \times (2^{2 I_{GR}} - 1) \tag{3.5}$$

See Figures 3.1 and 3.2 for an example of a shale volume calculation using the gamma ray log.

## SPECTRAL GAMMA RAY LOG

The response of the normal gamma ray log is made up of the combined radiation from uranium, thorium, potassium, and a number of associated daughter products of radioactive decay. Because these different radioactive elements emit gamma rays at different energy levels, the radiation contributed by each element can be analyzed separately. Potassium (potassium 40) has a single energy of 1.46 MeV (million electron volts). The thorium and uranium series emit radiation at various energies; however, they have prominent energies at 2.614 MeV (thorium) and 1.764 MeV (uranium). By using energy-selective sensor windows, the total gamma ray response can be separated into the gamma rays related to each of these elements (Dewan, 1983). Figure 3.3 illustrates one format used to display output from the spectral gamma ray log. In addition to the individual elements shown in tracks 2 and 3, the spectral gamma ray data can be displayed in track 1 as total gamma radiation (SGR-dashed curve) and total gamma radiation minus uranium (CGR-solid curve).

Important uses of the spectral gamma ray log include (Dresser-Atlas, 1981):

- determining shale (clay) volume ($V_{shale}$) in sandstone reservoirs that contain uranium minerals, potassium feldspars, micas, and/or glauconite
- differentiating radioactive reservoirs from shales
- source-rock evaluation
- evaluation of potash deposits
- geologic correlations
- clay typing
- fracture detection
- rock typing in crystalline basement rocks

In most log analyses, the first two uses listed above are the most important uses of spectral log data.

In determining shale volume ($V_{shale}$) in sandstones, Dewan (1983) has suggested the use of only the thorium and potassium components instead of total GR in the $V_{shale}$ equations, because uranium salts are soluble and can be transported and precipitated in the formation after deposition. If potassium minerals are present in the sandstone, Dewan (1983) suggested the use of only the thorium component in the $V_{shale}$ equations. Radioactive reservoirs like the "hot" dolomites of the Permian (west Texas and New Mexico) and Williston (Montana, North Dakota, and South Dakota) basins of the United States are normally differentiated from shales by the low thorium and potassium contents and high uranium content.

## REVIEW

1. Gamma ray logs are lithology logs that measure the natural radioactivity of a formation.
2. Because radioactive material is concentrated in shale, shale has a high gamma ray reading.

Shale-free sandstones and carbonates, therefore, usually have low gamma ray readings.

3. Gamma ray logs are used to identify lithologies, correlate between formations, and calculate volume of shale.
<!-- page 44 -->
Gamma Ray

33


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: increases downward, units: feet (Ft), range: 13534–13720 ft.
Track 1 (left): GR — Gamma Ray, scale: 0–150 API units, curve: solid line.
Track 2 (right): 
- RHOB — Bulk Density, scale: 2.0–3.0 g/cm³, curve: solid line.
- NPHI — Neutron Porosity, scale: 0.3–0.1 (fractional porosity, decimal), curve: dashed line.
- DRHO — Density Derivative (or Δρ), scale: 0.25–0.25 (unit not specified, likely g/cm³), curve: dotted line.

Interpretation:
- Depth interval 13534–13570 ft: GR shows moderate to high values (80–120 API), RHOB shows low density (~2.2 g/cm³), NPHI shows high porosity (~0.30–0.35), indicating a porous, likely sandstone interval.
- Depth interval 13570–13590 ft: GR decreases to ~50 API, RHOB increases to ~2.4 g/cm³, NPHI decreases to ~0.25, suggesting a transition to shaly or denser rock.
- Depth interval 13590–13600 ft: GR increases again to ~80 API, RHOB ~2.3 g/cm³, NPHI ~0.30, indicating return to porous zone.
- Depth interval 13600–13700 ft: GR shows variable but generally high values (70–110 API), RHOB ~2.2–2.3 g/cm³, NPHI ~0.25–0.35, consistent with sandstone with variable shale content.
- Depth interval 13700–13720 ft: GR shows a sharp increase to ~130 API, RHOB increases to ~2.5 g/cm³, NPHI decreases to ~0.20, indicating a transition to shaly or clay-rich zone.

Marked bed boundaries (отбивки) are indicated by dashed horizontal lines at approximately 13534, 13570, 13590, 13600, 13700, and 13720 ft.

No petrophysical results panel (Кп, Кн, Кпр, etc.) is present.

KEYWORDS: well log, gamma ray, density, neutron porosity, depth, feet, API units, g/cm³, porosity, lithology interpretation, sandstone, shale, bed boundaries
----


Figure 3.1. Example of a gamma ray log with neutron-density log.

This example illustrates the curves and scales of a gamma ray log, and is also used to pick values for Figure 3.2.

Track 1 (to the left of the depth track): The gamma ray log (GR) is the only one represented on this track. Note that the scale increases from left to right, and ranges from 0 to 150 API gamma ray units in increments of 15 API units.

Tracks 2 and 3 (used together, to the right of the depth track): These tracks include logs representing bulk density (RHOB), neutron porosity (NPH), and density correction (DRHO). Bulk density (RHOB) is represented by a solid line and ranges from 2.0 to 3.0 g/cm³ increasing from left to right. Neutron porosity (NPH) is represented by a dashed line and ranges from -0.10 (-10%) to +0.30 (30%) increasing from right to left. The correction curve (DRHO) is represented by a dotted line and ranges from -0.25 to +0.25 g/cm³ increasing from left to right, but only uses track 3.

# Calculation of Gamma Ray Index $I_{GR}$ for Shale Volume Calculation

The minimum gamma ray value ($GR_{min}$) occurs at 13,593 ft and is 14 API units (slightly less than 1 scale division from zero).

The maximum gamma ray value ($GR_{max}$) occurs at 13,577 ft and at 13,720 ft and is 130 API units. These are the smallest zones in the interval.

The gamma ray readings from three depths are shown in the table below.

From Equation 3.1, the gamma ray index ($I_{GR}$) is:

$$
I_{GR} = \frac{GR_{log} - GR_{min}}{GR_{max} - GR_{min}} \tag{3.6}
$$

|  Depth (ft) | $GR_{log}$ | $I_{GR}$  |
| --- | --- | --- |
|  13,534 | 32 | 0.16  |
|  13,570 | 28 | 0.12  |
|  13,701 | 55 | 0.35  |

See Figure 3.2 to convert \( I_{GR} \) to shale volume (\( V_{\text{shale}} \)).
<!-- page 45 -->
34

ASQUITH AND KRYGOWSKI

Figure 3.2. Chart for correcting the gamma ray index ($I_{GR}$) to the shale volume ($V_{shale}$). (Western Atlas, 1995, Figure 4-24)

Given (from Figure 3.1):

|  Depth (ft) | $GR_{lag}$ | $I_{GR}$  |
| --- | --- | --- |
|  13,534 | 32 | 0.16  |
|  13,570 | 28 | 0.12  |
|  13,701 | 55 | 0.35  |

# Procedure:

1. For each zone below, find the gamma ray index value \((I_{GR})\) on the horizontal scale on the bottom.
2. Follow the value vertically to where it intersects curve each of the curves listed below.
3. From each curve, move horizontally to the scale at the left and read the shale volume. This is the amount of shale in the formation expressed as a decimal fraction.


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━

**Crossplot of Shale Volume (V_sh) versus Radioactivity Index (I_GR)**

Axes:
- X-axis: Radioactivity Index, I_GR (dimensionless), linear scale, range 0 to 1, major gridlines every 0.1.
- Y-axis: Shale Volume, V_sh (dimensionless fraction), linear scale, range 0 to 1, major gridlines every 0.1.

Labelled curves (from top to bottom):
1. **Linear Scaling** — a straight line from the origin (0,0) to the top-right corner (1,1), representing V_sh = I_GR.
2. **Larionov (Older rocks)** — a curve lying just below the linear line.
3. **Clavier et al** — a curve lying below the Larionov (Older rocks) curve.
4. **Stieber** — a curve lying below the Clavier curve.
5. **Larionov (Tertiary rocks)** — a curve lying below the Stieber curve; the lowest estimate of V_sh for a given I_GR.

All curves intersect at the point (1, 1).

No numeric data points, regression equations, or coefficients are printed on the plot; the curves are identified solely by author names.

> Trend: For a fixed Radioactivity Index, the linear scaling yields the highest shale volume, whereas the Larionov (Tertiary rocks) relation yields the lowest. The divergence between the curves is maximal at intermediate I_GR values and converges at I_GR = 1.

KEYWORDS: crossplot, shale volume, radioactivity index, V_sh, I_GR, Larionov, Stieber, Clavier, well logging, petrophysics
----


Courtesy Baker Atlas, ©1996-1999 Baker Hughes, Inc.

|  Depth (ft) | $GR_{lag}$ | $I_{GR}$ | Shale volume, $V_{shale}$  |   |   |
| --- | --- | --- | --- | --- | --- |
|   |   |   |  Linear | Larionov (for rocks older than Tertiary) | Steiber  |
|  13,534 | 32 | 0.16 | 0.16 | 0.08 | 0.06  |
|  13,570 | 28 | 0.12 | 0.12 | 0.06 | 0.04  |
|  13,701 | 55 | 0.35 | 0.35 | 0.21 | 0.15  |
<!-- page 46 -->
Gamma Ray

35


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━

**Spectral gamma ray log (SGR, CGR, POTA, URAN, THOR)**

Depth range: 9500–9606 ft (Measured Depth, MD). Depth increases downward. Depth units: feet.

No lithology column is present; lithology is not determined without a legend.

Tracks (left to right):
- Track 1: SGR (Standard Gamma Ray) — solid line, scale 0–250 API; CGR (Computed Gamma Ray) — dashed line, same scale 0–250 API.
- Track 2: POTA (Potassium) — solid line, scale 0–10 %.
- Track 3: URAN (Uranium) — solid line, scale 0–10 ppm.
- Track 4: THOR (Thorium) — solid line, scale 0–20 ppm.

| Interval, ft | Lithology (from column) | Curves: behavior | Interpretation (if labelled) |
|---|---|---|---|
| 9500–~9560 | Not shown | SGR, CGR low, closely tracking each other; POTA low; URAN low; THOR moderate | Not labelled |
| ~9560–~9580 | Not shown | SGR, CGR slight increase with small deflections; POTA slight increase; URAN slight increase; THOR some variation | Not labelled |
| ~9580–~9595 | Not shown | SGR, CGR significant increase with a large peak; SGR notably higher than CGR; POTA increases; URAN large increase; THOR moderate increase | Not labelled |
| ~9595–9606 | Not shown | SGR, CGR decrease; POTA, URAN, THOR decrease | Not labelled |

An unlabelled dash annotation ("-") is present between the SGR/CGR track and the POTA track at approximately 9590 ft.

KEYWORDS: spectral gamma ray, SGR, CGR, POTA, URAN, THOR, potassium, uranium, thorium, well log
----


Figure 3.3. Spectral gamma ray log.

This example is from West Texas. The Mississippian Barnett Shale contacts the underlying Mississippian limestone at 9606 ft. In the Barnett Shale, note the great variations in the potassium (POTA), uranium (URAN), and thorium (THOR) contents above the contact with the Mississippian limestone indicating changes in shale mineralogy.

# Symbols:

SGR Total gamma ray (dashed curve, track 1)

CGR Total gamma ray minus uranium (solid curve, track 1)

POTA Potassium 40 in weight percent (tracks 2 and 3)

URAN Uranium in ppm (tracks 2 and 3)

THOR Thorium in ppm (tracks 2 and 3)
<!-- page 47 -->

<!-- page 48 -->
4

Asquith, G., and D. Krygowski, 2004, Porosity Logs, in G. Asquith and D. Krygowski, Basic Well Log Analysis: AAPG Methods in Exploration 16, p. 37-76.

# Porosity Logs

## GENERAL

The next class of well logs to be considered is generally referred to as porosity logs. Although each produces a porosity value from basic measurements, none actually measures porosity directly. Two such logs, the density and neutron, are nuclear measurements. A third log, the sonic, uses acoustic measurements, and the fourth and newest log senses the magnetic resonance of formation nuclei. When used individually, each of the first three has a response to lithology which must be accounted for, but when used in concert, two or three at a time, lithology can be estimated and a more accurate porosity derived.

## NUCLEAR MAGNETIC RESONANCE LOG

Nuclear magnetic resonance (NMR) logging was first introduced by Schlumberger in 1978 (Maute, 1992) but was not initially widely used because of operational limitations. With the commercial introduction of the Magnetic Resonance Imaging Log (MRIL) by NUMAR Corporation (now part of Halliburton) in 1980 (Halliburton, 1999) and the release of the Combinable Magnetic Resonance Tool (CMR) by Schlumberger, the technique is steadily gaining acceptance.

The measurement technique is closely related to medical Magnetic Resonance Imaging (MRI) in that it senses the fluids in the formation surrounding the borehole (like MRI senses the fluids in the body) while the solids are largely invisible. In the logging tool, a powerful permanent magnet in the tool causes the protons in the formation fluids (mostly in the hydrogen) to align. An antenna in the tool then sends a signal into the formation, causing the protons to tip away from that original alignment. When the antenna signal is turned off, the protons begin to realign in the strong magnetic field, producing a signal called the *spin echo*. Repeated application of the antenna’s signal

leads to the measurement of many spin echoes, gathered as a *spin echo train* which is interpreted to estimate formation properties. Different interpretation and measurement methods lead to estimates of porosity, pore fluid types, and pore size distribution in the formation. Like the other porosity measurements, NMR measures mostly in the invaded and mixed zones of the formation around the wellbore. Unlike the other porosity measurements, the porosity determined from it is much less sensitive to lithologic changes than the porosities determined from those measurements.

Because wide use of NMR logs is relatively new, this technique is often used alone in the determination of porosity rather than in concert with the other porosity tools (sonic, density, and neutron). For these reasons, NMR logging is considered separately in Chapter 6.

## SONIC LOG

The sonic log is a porosity log that measures interval transit time ($\Delta t$, delta t, or DT) of a compressional sound wave traveling through the formation along the axis of the borehole. The sonic log device consists of one or more ultrasonic transmitters and two or more receivers. Modern sonic logs are borehole-compensated (BHC) devices. These devices are designed to greatly reduce the spurious effects of borehole size variations (Kobesh and Blizard, 1959) as well as errors due to tilt of the tool with respect to the borehole axis (Schlumberger, 1972) by averaging signals from different transmitter-receiver combinations over the same length of borehole.

Interval transit time ($\Delta t$) in microseconds per foot, $\mu$sec/ft (or microseconds per meter, $\mu$sec/m) is the reciprocal of the velocity of a compressional sound wave in feet per second (or meters per second). Interval transit time (DT) is usually displayed in tracks 2 and 3 of a log (Figure 4.1). A sonic-derived porosity

37
<!-- page 49 -->
38

ASQUITH AND KRYGOWSKI

curve (SPHI) is sometimes displayed in tracks 2 and 3, along with the DT curve. Track 1 usually contains a caliper (CALI), and a gamma ray (GR) or an SP.

The interval transit time ($\Delta t$) is dependent upon both lithology and porosity. Therefore, a formation's matrix interval transit time (Table 4.1) must be known to derive sonic porosity either by chart (Figure 4.2) or by the following formulas:

Wyllie time-average equation (Wyllie et al., 1958):

$$\phi_S = \frac{\Delta t_{log} - \Delta t_{ma}}{\Delta t_{fl} - \Delta t_{ma}} \tag{4.1}$$

Raymer-Hunt-Gardner (RHG) equation (Raymer et al., 1980):

$$\phi_S = \frac{5}{8} \times \frac{\Delta t_{log} - \Delta t_{ma}}{\Delta t_{log}} \tag{4.2}$$

where:

$\phi_S$ = sonic-derived porosity

$\Delta t_{ma}$ = interval transit time in the matrix (Table 4.1)

$\Delta t_{log}$ = interval transit time in the formation

$\Delta t_{fl}$ = interval transit time in the fluid in the formation (freshwater mud = 189 $\mu$sec/ft; saltwater mud = 185 $\mu$sec/ft)

### Unconsolidated Formations

The Wyllie et al. (1958) formula for calculating sonic porosity can be used to determine porosity in consolidated sandstones and carbonates with intergranular porosity (grainstones) or intercrystalline porosity (sucrosic dolomites). However, when sonic

porosities of carbonates with vuggy or fracture porosity are calculated by the Wyllie formula, porosity values are too low. This happens because the sonic log only records matrix porosity rather than vuggy or fracture secondary porosity. The percentage of vuggy or fracture secondary porosity can be calculated by subtracting sonic porosity from total porosity. Total porosity values are obtained from one of the nuclear logs (i.e., density, neutron, or preferably the combination of density and neutron). The percentage of secondary porosity, called SPI or secondary porosity index, can be a useful mapping parameter in carbonate exploration.

Where a sonic log is used to determine porosity in unconsolidated sands, an empirical compaction factor ($C_p$) should be added to the Wyllie et al. (1958) equation:

$$\phi_S = \left( \frac{\Delta t_{log} - \Delta t_{ma}}{\Delta t_{fl} - \Delta t_{ma}} \right) \times \frac{1}{C_p} \tag{4.3}$$

where:

$C_p$ = compaction factor

The compaction factor is obtained from the following formula:

$$C_p = \frac{\Delta t_{sh} \times C}{100} \tag{4.4}$$

where:

$t_{sh}$ = interval transit time in a shale adjacent to the formation of interest.

$C$ = a constant which is normally 1.0 (Hilchie, 1978).

Interval transit time values from selected depths on

Table 4.1. Sonic Velocities and Interval Transit Times for Different Matrices. These constants are used in the sonic porosity formulas above (after Schlumberger, 1972).

|  Lithology/ Fluid | Matrix velocity ft/sec | $\Delta t_{matrix}$ or $\Delta t_{fluid}$ (Wyllie) $\mu$sec/ft [$\mu$sec/m] | $\Delta t_{matrix}$ (RHG) $\mu$sec/ft [$\mu$sec/m]  |
| --- | --- | --- | --- |
|  Sandstone | 18,000 to 19,500 | 55.5 to 51.0 [182 to 168] | 56 [184]  |
|  Limestone | 21,000 to 23,000 | 47.6 [156] | 49 [161]  |
|  Dolomite | 23,000 to 26,000 | 43.5 [143] | 44 [144]  |
|  Anhydrite | 20,000 | 50.0 [164] |   |
|  Salt | 15,000 | 66.7 [219] |   |
|  Casing (iron) | 17,500 | 57.0 [187] |   |
|  Freshwater mud filtrate | 5,280 | 189 [620] |   |
|  Saltwater mud filtrate | 5,980 | 185 [607] |   |
<!-- page 50 -->
Porosity Logs

39

the log in Figure 4.1 are listed in Table 4.5. Those values are used in the chart in Figure 4.2 to determine sonic porosity, which is listed in Table 4.6.

## Hydrocarbon Effects

The interval transit time ($\Delta t$) of a formation is increased due to the presence of hydrocarbons (i.e., hydrocarbon effect). If the effect of hydrocarbons is not corrected, the sonic-derived porosity is too high. Hilchie (1978) suggests the following empirical corrections for hydrocarbon effect:

$$\phi = \phi_s \times 0.7 \quad (\text{gas}) \tag{4.5}$$

$$\phi = \phi_s \times 0.9 \quad (\text{oil}) \tag{4.6}$$

## DENSITY LOG

Density is measured in grams per cubic centimeter, g/cm$^3$ (or Kg/m$^3$ or Mg/m$^3$), and is indicated by the Greek letter $\rho$ (rho). Two separate density values are used by the density log: the bulk density ($\rho_b$ or RHOB) and the matrix density ($\rho_{ma}$). The bulk density is the density of the entire formation (solid and fluid parts) as measured by the logging tool. The matrix density is the density of the solid framework of the rock. It may be thought of as the density of a particular rock type (e.g., limestone or sandstone) that has no porosity. Since the late 1970s, the density log has also been used for the photoelectric-effect measurement (P$_e$, PE, or PEF) to determine lithology of a formation. The density log can assist the geologist to:

- identify evaporite minerals
- detect gas-bearing zones
- determine hydrocarbon density
- evaluate shaly-sand reservoirs and complex lithologies (Schlumberger, 1972)

The density logging tool has a relatively shallow depth of investigation, and as a result, is held against the side of the borehole during logging to maximize its response to the formation. The tool is comprised of a medium-energy gamma ray source (cobalt 60, cesium 137, or in some newer designs, an accelerator-based source). Two gamma ray detectors provide some measure of compensation for borehole conditions (similar to the sonic logging tool).

When the emitted gamma rays collide with electrons in the formation, the collisions result in a loss of energy from the gamma ray particle. The scattered

gamma rays that return to the detectors in the tool are measured in two energy ranges. The number of returning gamma rays in the higher energy range, affected by Compton scattering, is proportional to the electron density of the formation. For most earth materials of interest in hydrocarbon exploration, the electron density is related to formation bulk density through a constant (Tittman and Wahl, 1965), and the bulk density is related to porosity. Gamma ray interactions in the lower energy range are governed by the photoelectric effect. The response from this energy range is strongly dependent on lithology and only very slightly dependent on porosity.

The bulk-density curve (RHOB) is recorded in tracks 2 and 3 (Figure 4.3). The photoelectric-effect curve (P$_e$ in barns per electron, b/e) is displayed in either track 2 or track 3, with its placement set to minimize its overlap with the bulk-density curve. A correction curve (DRHO in g/cm$^3$ or Kg/m$^3$), is also displayed in either track 2 or track 3 (Figure 4.3). This curve indicates how much correction has been added to the bulk-density curve during processing due to borehole effects (primarily mudcake thickness) and is used primarily as a quality-control indicator. Whenever the correction curve (DRHO) exceeds 0.20 g/cm$^3$, the value of the bulk density obtained from the bulk-density curve (RHOB) should be considered suspect and possibly invalid. A density-derived porosity curve (DPHI) is sometimes present in tracks 2 and 3 along with the bulk-density (RHOB) and correction (DRHO) curves. Track 1 usually contains a gamma ray log and a caliper (Figure 4.3).

The photoelectric-effect curve appeared as part of the second-generation density tools, which are commonly referred to as *Litho* or *Spectral* tools and were introduced around 1978.

Formation bulk density ($\rho_b$) is a function of matrix density, porosity, and density of the fluid in the pores (saltwater mud, freshwater mud, or hydrocarbons). To determine density porosity, either by chart (Figure 4.4) or by calculation, the matrix density (Table 4.2) and type of fluid in the formation must be known. The formula for calculating density porosity is:

$$\phi_D = \frac{\rho_{ma} - \rho_b}{\rho_{ma} - \rho_{fl}} \tag{4.7}$$

where:

$\phi_D$ = density derived porosity

$\rho_{ma}$ = matrix density (see Table 4.2 for values)

$\rho_b$ = formation bulk density (the log reading)

$\rho_{fl}$ = fluid density (see Table 4.2 for values)
<!-- page 51 -->
40

ASQUITH AND KRYGOWSKI

Table 4.2. Matrix densities and photoelectric-effect ($P_e$) values of common lithologies (Courtesy Halliburton, 1991).

|  Lithology/ Fluid | $\rho_{ma}$ or $\rho_{fl}$ g/cm$^3$ [Kg/m$^3$] | $P_e$ (b/e)  |
| --- | --- | --- |
|  Sandstone | 2.644 [2644] | 1.81  |
|  Limestone | 2.710 [2710] | 5.08  |
|  Dolomite | 2.877 [2877] | 3.14  |
|  Anhydrite | 2.960 [2960] | 5.05  |
|  Salt | 2.040 [2040] | 4.65  |
|  Fresh water | 1.0 [1000] |   |
|  Salt water | 1.15 [1150] |   |
|  Barite (mud additive) |  | 267  |

### Importance of Correct $\rho_{ma}$ and $\rho_{fl}$ values

A computer in the logging unit calculates density porosity from the measured bulk density of the formation using Equation 4.7. The wellsite geologist or logging unit engineer specifies the matrix and fluid densities that are to be used. If the formation's actual matrix density ($\rho_{ma}$) is less than the matrix density used to calculate the porosity [e.g., calculating porosity of a sandstone ($\rho_{ma} = 2.64$ g/cm$^3$) using a limestone matrix density ($\rho_{ma} = 2.71$ g/cm$^3$)], the log shows a calculated porosity that is higher than the actual porosity of the formation. If the formation's actual fluid density is less than the fluid density used to calculate the porosity [e.g., calculating the porosity of a saltwater-filled formation ($\rho_{fl} = 1.1$ g/cm$^3$) using a freshwater value ($\rho_{fl} = 1.0$ g/cm$^3$)], the log shows a calculated porosity that is lower than the actual porosity of the formation. Because of the wider range of matrix-density values than fluid-density values, errors in estimating the matrix density have a larger impact on the calculated porosity.

Bulk-density values from selected depths on the log in Figure 4.3 are listed in Table 4.7. Those values are used in the chart in Figure 4.4 to determine density porosity, which is listed in Table 4.8.

### Hydrocarbon Effects

Where invasion of a formation is shallow, the low density of the formation's hydrocarbons causes the calculated density porosity to be greater than the actual porosity. Oil does not significantly affect density porosity, but gas does (gas effect). Hilchie (1978) suggests using a gas density of 0.7 g/cm$^3$ for fluid density

ty ($\rho_{fl}$) in the density-porosity formula if gas density is unknown. Because the presence of oil has little effect on the density log, this tool usually provides the best indication of porosity in liquid-filled holes.

### Heavy Minerals

Any time the bulk density of a formation ($\rho_b$) is greater than the assumed matrix density ($\rho_{ma}$) of the formation [e.g., when measurements are made in an anhydrite ($\rho_{ma} = 2.96$ g/cm$^3$) but are recorded using a limestone matrix ($\rho_{ma} = 2.71$ g/cm$^3$)], the resulting density porosity is negative. It is important to note that in cases like this the logging tool is operating properly, but the assumptions made in the conversion between bulk density and density porosity are incorrect. In cases like this, where the porosity is clearly erroneous (because it is negative), the log still yields good information. Negative density porosity is often a good indication of the presence of anhydrite or other heavy minerals, as shown in Figure 4.5 over the intervals 11,550 to 11,567 ft and 11,600 to 11,618 ft.

Powdered barite is commonly added to mud to increase mud density. When heavy muds are used (e.g., 14 lb/gal), the high $P_e$ of the barite (Table 4.2) in the mud can mask the $P_e$ of the adjacent rock layers.

### NEUTRON LOG

Neutron logs are porosity logs that measure the hydrogen concentration in a formation. In clean formations (i.e., shale-free) where the porosity is filled with water or oil, the neutron log measures liquid-filled porosity ($\phi_N$, PHIN, or NPHI).

Neutrons are created from a chemical source in the neutron logging tool. The chemical source is usually a mixture of americium and beryllium which continuously emit neutrons. When these neutrons collide with the nuclei of the formation the neutron loses some of its energy. With enough collisions, the neutron is absorbed by a nucleus and a gamma ray is emitted. Because the hydrogen atom is almost equal in mass to the neutron, maximum energy loss occurs when the neutron collides with a hydrogen atom. Therefore, the energy loss is dominated by the formation's hydrogen concentration. Because hydrogen in a porous formation is concentrated in the fluid-filled pores, energy loss can be related to the formation's porosity.

The neutron curves are commonly displayed over tracks 2 and 3, in units referenced to a specific lithology (usually either limestone or sandstone, depending on the geologic environment expected to be encountered), as illustrated in Figure 4.5.
<!-- page 52 -->
Porosity Logs

41

Neutron log responses vary, depending on:

- differences in detector types and what they detect (gamma rays and/or neutrons of different energies)
- spacing between source and detector
- lithology (i.e., sandstone, limestone, and dolomite)

While the variations due to detector types and tool design are fixed (and are accounted for in the data processing), the variations in response due to lithology must be accounted for by using the appropriate charts (Figures 4.6 and 4.7). A geologist should remember that the responses of different neutron logs differ from each other (unlike all other logs) and must be interpreted from the specific chart designed for a specific log (i.e., Schlumberger charts for Schlumberger logs and Halliburton charts for Halliburton logs). The reason for this is that while other logs are calibrated in basic physical units, neutron logs are not (Dresser Atlas, 1975).

Table 4.11 shows the results of lithology corrections that are made to neutron measurements using the correct and incorrect charts for the specific neutron tool.

The first neutron logs detected the gamma rays that were products of neutron capture by formation nuclei. Initially, each logging company had its own calibration system, but eventually the American Petroleum Institute (API) developed calibration pits to provide a common standard for measurement (Serra, 1984). Generally these logs were displayed in counts per second (cps) or API Neutron Units rather than porosity. Although charts to convert from displayed units to porosity exist (Bassiouni, 1994), arbitrary conversions using core data or estimated formation porosities have most often been used. It should be noted that the neutron log response is inversely proportional to porosity so that low-measurement unit values correspond to high porosities, and high-measurement unit values correspond to low porosities.

The first modern neutron log (where porosity was directly displayed) was the sidewall neutron log. Like the density log (and for the same reason of limited depth of investigation), the sidewall neutron log has both the source and detector in a pad that is pushed against the side of the borehole. Although the sidewall neutron log was relatively insensitive to lithologic effects, it was sensitive to borehole effects, such as rugosity (roughness) which caused measurement difficulties.

The most commonly used neutron log is the compensated neutron log which has a neutron source and

two detectors. Like the sidewall neutron log, it directly displays values of porosity. The advantage of compensated neutron logs over sidewall neutron logs is that they are less affected by borehole irregularities. Both the sidewall and compensated neutron logs can be recorded in apparent limestone, sandstone, or dolomite porosity units. If a formation is limestone, and the neutron log is recorded in apparent limestone porosity units, apparent porosity is equal to true porosity. However, when the lithology of a formation is sandstone or dolomite, apparent limestone porosity must be corrected to true porosity by using the appropriate chart (Figure 4.6 illustrates the lithology corrections for one model of Halliburton neutron log, and Figure 4.7 the corrections for a Schlumberger neutron log). The procedure is identical for each of the charts and is shown in Figures 4.6 and 4.7.

Neutron-porosity values from selected depths on the log in Figure 4.5 are listed in Table 4.9. Those values are used in the chart in Figure 4.6 to determine sonic porosity, which is listed in Table 4.10.

## Hydrocarbon effects

Whenever pores are filled with gas rather than oil or water, the reported neutron porosity is less than the actual formation porosity. This occurs because there is a lower concentration of hydrogen in gas than in oil or water. This lower concentration is not accounted for by the processing software of the logging tool, and thus is interpreted as low porosity. A decrease in neutron porosity by the presence of gas is called *gas effect*.

## Shale Effect

Whenever clays are part of the formation matrix, the reported neutron porosity is greater than the actual formation porosity. This occurs because the hydrogen that is within the clay's structure and in the water bound to the clay is sensed in addition to the hydrogen in the pore space. Because the processing software of the logging tool expects all hydrogen in the formation to reside in the pores, the extra hydrogen is interpreted as being part of the porosity. An increase in neutron porosity by the presence of clays is called *shale effect*.

## POROSITY MEASUREMENT COMBINATIONS

Although the advent of porosity logs provided a substantial improvement in log interpretation, the significant change, from a geological viewpoint, was the development of interpretive techniques that combined the measurements from different porosity tools. With
<!-- page 53 -->
42

ASQUITH AND KRYGOWSKI

combinations of two or three measurements, lithology could be interpreted (rather than having to be known) and a better estimate of porosity produced. The interpretation of lithology and porosity is accomplished through crossplots. These are x-y plots of the quantities of interest, usually overlain with lines for “pure” lithologies (normally sandstone, limestone, and dolomite) with porosity indicated on each lithology line (e.g., Figure 4.11).

## Neutron-density Combination: Quick-look Lithology and Porosity

The combination of the neutron and density measurements is probably the most widely used porosity log combination. The neutron-density log display consists of neutron-porosity (NPHI) and density-porosity (DPHI) curves recorded in tracks 2 and 3 (Figure 4.5) and a caliper (CALI) and gamma ray (GR) in track 1. Both the neutron and density curves are normally recorded in limestone porosity units, however, porosity referenced to sandstone and dolomite can also be recorded.

The extensive use of the neutron-density combination may be due in part to the fact that they were among the first logging tools that could be physically combined and their data acquired in a single logging run. The response of the combination is such that for reconnaissance evaluation one can forego the crossplot and rely on recognition of the curve patterns (the position of the curves with respect to each other) to quickly determine the most likely predominant lithology and formation porosity.

Figure 4.8 illustrates the use of the neutron-density

combination to determine formation lithology and to estimate porosity. The reconnaissance technique works best with the following constraints:

- Both the neutron and density curves are in porosity (decimal or percent) referenced to limestone units.
- The formations are clean (no clays in the formations).
- There is no gas in the formations, only water or oil.

Using only the neutron-porosity and density-porosity curves, single lithologies can be predicted with little ambiguity. Adding the gamma ray may help, as in identifying dolomite from shale. In mixed lithologies, such as the sandy limestone and sandy dolomite shown, even the addition of the gamma ray does not help.

If the density log is of the newer litho or spectral type and a photoelectric curve (Pe) is available, the ambiguity can be further lessened, especially in the case of mixed lithologies. The value of the Pe curve in mixed lithologies falls between the single lithology value of each member, so some distinction can be made. Table 4.3 summarizes the patterns and values for common lithologies.

The estimation of porosity is equally straightforward: the formation porosity can be estimated to within about 2 porosity units (0.02) by taking the average of the neutron porosity and density porosity.

In areas of the world where sand and shale intervals predominate, the neutron and density are referenced to sandstone rather than limestone to eliminate the need for matrix conversion. (This also helps highlight the gas crossover effect described below.) While Figure

Table 4.3. Estimation of formation lithologies using the neutron-density combination (Campaign, W. J., personal communication).

Neutron and density are run with a limestone matrix; formation is water filled or oil filled

|  Lithology | φ_{N} and φ_{D} | P_{e}  |
| --- | --- | --- |
|  Sandstone | Neutron-density crossover (φ_{N} > φ_{D}) of 6 to 8 porosity units. | less than 2  |
|  Limestone | Neutron and density curves overlay (φ_{N} ~ φ_{D}). | about 5  |
|  Dolomite | Neutron-density separation (φ_{N} < φ_{D}) of 12 to 14 porosity units. | about 3  |
|  Anhydrite | Neutron porosity is greater than density porosity (φ_{N} > φ_{D}) by 14 porosity units or more. φ_{N} ~ zero. | about 5  |
|  Salt | Neutron porosity is slightly less than zero. Density porosity is 40 porosity units (0.40) or more. Watch for washed out hole (large caliper values) and bad density data. | 4.7  |
<!-- page 54 -->
Porosity Logs

43

4.8 focuses on lithology changes in clean (clay-free) formations with widely varying lithologies, Figure 4.9 illustrates neutron and density patterns in a variety of shaly sands, with both porosities referenced to sandstone. The effects of gas and clays are greater on the neutron measurement than on the density, with the neutron simultaneously being driven lower by gas and higher by clays in a shaly gassy formation. The exact location of the neutron curve with respect to the density curve is determined by the amounts of clay and gas present in the formation.

Table 4.12 shows the quick-look lithology determination in Figure 4.8 applied to the data in Figure 4.5.

## Neutron-density Combination: Gas Detection

Another technique using the neutron and density logs and the identification of curve patterns is that of gas identification. Gas in the pores causes the density porosity to be too high (gas has a lower density than oil or water) and causes the neutron porosity to be too low (there is a lower concentration of hydrogen atoms in gas than in oil or water). Figure 4.10 shows an example of a gas zone. In that zone, the neutron porosity is less than the density porosity, and the two porosity curves cross over each other. This is called crossover. The magnitude of the crossover (the amount of separation between the curves) is qualitatively related to the gas saturation, however, the crossover is more strongly influenced (again qualitatively) by the formation pressure. Low-pressure zones, either at shallow depths or depleted from production, tend to show large crossover.

Neutron-density crossover can also be caused by lithologic effects, as when the curves are displayed referenced to a lithology that is different from the actual lithology of the formation. Figure 4.8 illustrates this in the sandstone formations with the curves displayed referenced to limestone. It is important to check the log header for lithology-reference information as well as knowing the actual lithology of the formation in question before predicting the presence of gas from the log patterns only.

The porosity of a gas-bearing formation can be estimated by either form of the following equation:

$$\phi_{NDgas} = \sqrt{\frac{\phi_N^2 + \phi_D^2}{2}} \approx \frac{1}{3} \times \phi_N + \frac{2}{3} \times \phi_D \quad 4.8$$

where:

$\phi_{NDgas}$ = porosity of the gas-bearing formation

$\phi_N$ = neutron porosity

$\phi_D$ = density porosity

## Porosity Combinations: Crossplots

Crossplots are a graphical way to solve fairly complex relationships using two (or three) porosity measurements to estimate formation lithology and porosity. All these crossplots have the same general format: one measurement is displayed along the x-axis, and another is displayed along the y-axis. The measurements are either in porosity units referenced to limestone or, in the case of density and sonic logs, they can be in the original measurement units ($\rho_b$ in g/cm$^3$ or Kg/m$^3$ for the density, and $\Delta t$ in $\mu$sec/ft or $\mu$sec/m for the sonic). Superimposed on the plot (as an overlay) are pure lithology lines, usually sandstone, limestone, and dolomite. Porosity is indicated along each of these lines. See Figure 4.11 as an example.

In the interpretation, the values of the two measurements of interest are plotted on the crossplot. The intersection of those values on the plot determines both the porosity and the lithology of the point. If the point lies between two lithology lines, the lithology is taken as a mixture of those two lithologies (with the dominant lithology being that of the line closest to the point). The porosity is estimated by joining points of equal porosity on the two lithology lines and interpolating between the lines of equal porosity. Figure 4.11 illustrates the interpretive process.

It should be noted that not all interpretations are unique. In fact, the data often plot in such a way that there are two possible lithology pairs, and the decision of which to chose lies with the interpreter's knowledge of the area (or the application of other data). In some plots, as noted below and shown in the accompanying figures, the choice of lithologic pair significantly affects the predicted porosity value.

Other minerals can also be plotted on the crossplot, as distinct points (rather than lines indicating varying porosity). Figure 4.11 shows the location of halite and anhydrite. Log values for other pure minerals are available in the log interpretation chartbooks provided by most well log (wireline and MWD) acquisition companies. Although the existence of pure (and thick) beds of some minerals is very rare, the location of the mineral point on the crossplot (and the shift of the data toward that point) may sometimes give some indication that the mineral is present in the formation of interest.

Table 4.4 details the advantages and limitations of each of the four crossplots. The crossplots are listed in the order of preference of use, from top to bottom.

Figures 4.11 to 4.14 and Tables 4.13 to 4.15 illustrate the determination of porosity and lithology using the first three crossplot techniques in Table 4.4.
<!-- page 55 -->
44

ASQUITH AND KRYGOWSKI

Table 4.4. Comparison of porosity crossplots (in order of preference of use)

|  Crossplot | Advantages | Limitations  |
| --- | --- | --- |
|  Neutron Density (Figure 4.11) | Given two possible lithology pair solutions, the porosity remains relatively invariant between solutions. The combination of neutron and density is the most common of all porosity tool pairs. | In rough holes or in heavy drilling muds, the density data might be invalid.  |
|  Neutron Sonic (Figure 4.12) | Given two possible lithology pair solutions, the porosity remains relatively invariant between solutions. The sonic is less sensitive to rough holes than the density. | The combination of sonic and neutron data (without the density) is not common.  |
|  Spectral Density (bulk density-P_{e}) (Figure 4.13) | Both measurements are made with the same logging tool; both will be available in newer wells. | The choice of lithology pair will have a significant effect of the estimation of porosity. In rough holes or in heavy drilling mud, the data may be invalid. The P_{e} measurement will not be present in wells logged before about 1978.  |
|  Sonic Density (Figure 4.14) | Best for identifying radioactive reservoirs, rather than predicting lithology and porosity: Potential reservoirs plot along the closely spaced lithology lines while shales tend to fall toward the lower right of the plot. This can indicate the presence of radioactive reservoirs which are intermingled with shales (which tend to have high radioactivity). | The choice of lithology pair has a significant effect on the estimation of porosity. The lithology lines are closely spaced, so any uncertainty in the measurements produces large changes in the lithology and porosity estimates.  |

## Extending the Crossplot Technique

Given that the use of two porosity measurements can lead to the prediction of a more lithologically complex subsurface (i.e., the formation described as a two-mineral mixture), the natural extension is to use three measurements to estimate a ternary mixture. There are two different techniques, with one having two variations. Both techniques are more concerned with determining lithology than with determining porosity, the porosity having been determined from the previous two-measurement crossplots (usually the neutron-density).

## M-N Lithology Plots

This technique is the oldest of the three-measurement lithology techniques, and was based on combining the three porosity measurements in such a way so that two quantities could be used in a crossplot. The two calculated quantities are:

$$
M = \frac{\Delta t_{fl} - \Delta t}{\rho_b - \rho_{fl}} \times 0.01
$$

$$
\left( M = \frac{\Delta t_{fl} - \Delta t}{\rho_b - \rho_{fl}} \times 0.003 \text{ (metric)} \right) \tag{4.9}
$$
<!-- page 56 -->
Porosity Logs

45

Table 4.5. Values to be used with the chart in Figure 4.2 to determine the sonic porosity, SPHI.

|  Depth | Raw Data |   |   |   | SPHI (Wyllie) |   | SPHI (RHG) |   | DPHI |   | NPHI  |   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|   |  DT | RHOB | PE | NPHI | Lime | Dolo | Lime | Dolo | Lime | Dolo | Dolo | Sand  |
|  11,508 | 51 |  |  |  |  |  |  |  |  |  |  |   |
|  11,522 | 47 |  |  |  |  |  |  |  |  |  |  |   |
|  |   |   |   |   |   |   |   |   |   |   |   |   |
|  11,545 | 57 |  |  |  |  |  |  |  |  |  |  |   |
|  11,560 | 48 |  |  |  |  |  |  |  |  |  |  |   |
|  |   |   |   |   |   |   |   |   |   |   |   |   |
|  11,593 | 50 |  |  |  |  |  |  |  |  |  |  |   |
|  11,615 | 51 |  |  |  |  |  |  |  |  |  |  |   |
|  11,631 | 67 |  |  |  |  |  |  |  |  |  |  |   |
|  11,645 | 52 |  |  |  |  |  |  |  |  |  |  |   |
|  11,655 | 57 |  |  |  |  |  |  |  |  |  |  |   |
|  11,665 | 52 |  |  |  |  |  |  |  |  |  |  |   |
|  11,696 | 50 |  |  |  |  |  |  |  |  |  |  |   |

Table 4.6. Determination of sonic porosity by two methods.

|  Depth | Raw Data |   |   |   | SPHI (Wyllie) |   | SPHI (RHG) |   | DPHI |   | NPHI  |   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|   |  DT | RHOB | PE | NPHI | Lime | Dolo | Lime | Dolo | Lime | Dolo | Dolo | Sand  |
|  11,508 | 51 |  |  |  | 0.024 | 0.051 | 0.053 | 0.110 |  |  |  |   |
|  11,522 | 47 |  |  |  | 0.000 | 0.025 | 0.000 | 0.060 |  |  |  |   |
|  |   |   |   |   |   |   |   |   |   |   |   |   |
|  11,545 | 57 |  |  |  | 0.067 | 0.092 | 0.125 | 0.170 |  |  |  |   |
|  11,560 | 48 |  |  |  | 0.005 | 0.031 | 0.010 | 0.073 |  |  |  |   |
|  |   |   |   |   |   |   |   |   |   |   |   |   |
|  11,593 | 50 |  |  |  | 0.017 | 0.045 | 0.040 | 0.098 |  |  |  |   |
|  11,615 | 51 |  |  |  | 0.024 | 0.051 | 0.053 | 0.010 |  |  |  |   |
|  11,631 | 67 |  |  |  | 0.138 | 0.163 | 0.203 | 0.235 |  |  |  |   |
|  11,645 | 52 |  |  |  | 0.032 | 0.059 | 0.070 | 0.122 |  |  |  |   |
|  11,655 | 57 |  |  |  | 0.067 | 0.092 | 0.125 | 0.170 |  |  |  |   |
|  11,665 | 52 |  |  |  | 0.032 | 0.059 | 0.070 | 0.122 |  |  |  |   |
|  11,696 | 50 |  |  |  | 0.017 | 0.045 | 0.040 | 0.098 |  |  |  |   |
<!-- page 57 -->
46

ASQUITH AND KRYGOWSKI

Table 4.7. Values to be used with the chart in Figure 4.4 to determine the density porosity, DPHI.

|  Depth | Raw Data |   |   |   | SPHI (Wyllie) |   | SPHI (RHG) |   | DPHI |   | NPHI  |   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|   |  DT | RHOB | PE | NPHI | Lime | Dolo | Lime | Dolo | Lime | Dolo | Dolo | Sand  |
|  11,508 | 51 |  |  |  | 0.024 | 0.051 | 0.053 | 0.110 |  |  |  |   |
|  11,522 | 47 | 2.75 |  |  | 0.000 | 0.025 | 0.000 | 0.060 |  |  |  |   |
|  |   |   |   |   |   |   |   |   |   |   |   |   |
|  11,545 | 57 |  |  |  | 0.067 | 0.092 | 0.125 | 0.170 |  |  |  |   |
|  11,560 | 48 |  |  |  | 0.005 | 0.031 | 0.010 | 0.073 |  |  |  |   |
|  |   |   |   |   |   |   |   |   |   |   |   |   |
|  11,593 | 50 |  |  |  | 0.017 | 0.045 | 0.040 | 0.098 |  |  |  |   |
|  11,615 | 51 |  |  |  | 0.024 | 0.051 | 0.053 | 0.010 |  |  |  |   |
|  11,631 | 67 | 2.50 |  |  | 0.138 | 0.163 | 0.203 | 0.235 |  |  |  |   |
|  11,645 | 52 |  |  |  | 0.032 | 0.059 | 0.070 | 0.122 |  |  |  |   |
|  11,655 | 57 | 2.64 |  |  | 0.067 | 0.092 | 0.125 | 0.170 |  |  |  |   |
|  11,665 | 52 | 2.68 |  |  | 0.032 | 0.059 | 0.070 | 0.122 |  |  |  |   |
|  11,696 | 50 |  |  |  | 0.017 | 0.045 | 0.040 | 0.098 |  |  |  |   |

Table 4.8. Determination of density porosity.

|  Depth | Raw Data |   |   |   | SPHI (Wyllie) |   | SPHI (RHG) |   | DPHI |   | NPHI  |   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|   |  DT | RHOB | PE | NPHI | Lime | Dolo | Lime | Dolo | Lime | Dolo | Dolo | Sand  |
|  11,508 | 51 | 2.73 |  |  | 0.024 | 0.051 | 0.053 | 0.110 | -0.013 | 0.078 |  |   |
|  11,522 | 47 | 2.75 |  |  | 0.000 | 0.025 | 0.000 | 0.060 | -0.022 | 0.068 |  |   |
|  |   |   |   |   |   |   |   |   |   |   |   |   |
|  11,545 | 57 | 2.67 |  |  | 0.067 | 0.092 | 0.125 | 0.170 | 0.022 | 0.110 |  |   |
|  11,560 | 48 | 2.96 |  |  | 0.005 | 0.031 | 0.010 | 0.073 | < 0 | < 0 |  |   |
|  |   |   |   |   |   |   |   |   |   |   |   |   |
|  11,593 | 50 | 2.70 |  |  | 0.017 | 0.045 | 0.040 | 0.098 | 0.005 | 0.095 |  |   |
|  11,615 | 51 | 2.97 |  |  | 0.024 | 0.051 | 0.053 | 0.010 | < 0 | < 0 |  |   |
|  11,631 | 67 | 2.50 |  |  | 0.138 | 0.163 | 0.203 | 0.235 | 0.125 | 0.200 |  |   |
|  11,645 | 52 | 2.82 |  |  | 0.032 | 0.059 | 0.070 | 0.122 | < 0 | 0.030 |  |   |
|  11,655 | 57 | 2.64 |  |  | 0.067 | 0.092 | 0.125 | 0.170 | 0.042 | 0.125 |  |   |
|  11,665 | 52 | 2.68 |  |  | 0.032 | 0.059 | 0.070 | 0.122 | 0.020 | 0.105 |  |   |
|  11,696 | 50 | 2.76 |  |  | 0.017 | 0.045 | 0.040 | 0.098 | -0.028 | 0.063 |  |   |
<!-- page 58 -->
Porosity Logs

47

Table 4.9. Values will be used with the chart in Figure 4.4 to determine the neutron porosity, NPHI, referenced to other lithologies (dolomite and sandstone).

|  Depth | Raw Data |   |   |   | SPHI (Wyllie) |   | SPHI (RHG) |   | DPHI |   | NPHI  |   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|   |  DT | RHOB | PE | NPHI | Lime | Dolo | Lime | Dolo | Lime | Dolo | Dolo | Sand  |
|  11,508 | 51 | 2.73 |  |  | 0.024 | 0.051 | 0.053 | 0.110 | -0.013 | 0.078 |  |   |
|  11,522 | 47 | 2.75 |  | 0.090 | 0.000 | 0.025 | 0.000 | 0.060 | -0.022 | 0.068 |  |   |
|  |   |   |   |   |   |   |   |   |   |   |   |   |
|  11,545 | 57 | 2.67 |  |  | 0.067 | 0.092 | 0.125 | 0.170 | 0.022 | 0.110 |  |   |
|  11,560 | 48 | 2.96 |  |  | 0.005 | 0.031 | 0.010 | 0.073 | < 0 | < 0 |  |   |
|  |   |   |   |   |   |   |   |   |   |   |   |   |
|  11,593 | 50 | 2.70 |  |  | 0.017 | 0.045 | 0.040 | 0.098 | 0.005 | 0.095 |  |   |
|  11,615 | 51 | 2.97 |  |  | 0.024 | 0.051 | 0.053 | 0.010 | < 0 | < 0 |  |   |
|  11,631 | 67 | 2.50 |  | 0.290 | 0.138 | 0.163 | 0.203 | 0.235 | 0.125 | 0.200 |  |   |
|  11,645 | 52 | 2.82 |  |  | 0.032 | 0.059 | 0.070 | 0.122 | < 0 | 0.030 |  |   |
|  11,655 | 57 | 2.64 |  | 0.160 | 0.067 | 0.092 | 0.125 | 0.170 | 0.042 | 0.125 |  |   |
|  11,665 | 52 | 2.68 |  | 0.010 | 0.032 | 0.059 | 0.070 | 0.122 | 0.020 | 0.105 |  |   |
|  11,696 | 50 | 2.76 |  |  | 0.017 | 0.045 | 0.040 | 0.098 | -0.028 | 0.063 |  |   |

Table 4.10. Lithology conversions for the neutron log.

|  Depth | Raw Data |   |   |   | SPHI (Wyllie) |   | SPHI (RHG) |   | DPHI |   | NPHI  |   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|   |  DT | RHOB | PE | NPHI | Lime | Dolo | Lime | Dolo | Lime | Dolo | Dolo | Sand  |
|  11,508 | 51 | 2.73 |  | 0.005 | 0.024 | 0.051 | 0.053 | 0.110 | -0.013 | 0.078 | < 0 | 0.015  |
|  11,522 | 47 | 2.75 |  | 0.090 | 0.000 | 0.025 | 0.000 | 0.060 | -0.022 | 0.068 | 0.070 | 0.140  |
|  |   |   |   |   |   |   |   |   |   |   |   |   |
|  11,545 | 57 | 2.67 |  | 0.130 | 0.067 | 0.092 | 0.125 | 0.170 | 0.022 | 0.110 | 0.105 | 0.185  |
|  11,560 | 48 | 2.96 |  | -0.010 | 0.005 | 0.031 | 0.010 | 0.073 | < 0 | < 0 | < 0 | < 0  |
|  |   |   |   |   |   |   |   |   |   |   |   |   |
|  11,593 | 50 | 2.70 |  | 0.000 | 0.017 | 0.045 | 0.040 | 0.098 | 0.005 | 0.095 | < 0 | 0.015  |
|  11,615 | 51 | 2.97 |  | -0.010 | 0.024 | 0.051 | 0.053 | 0.010 | < 0 | < 0 | < 0 | < 0  |
|  11,631 | 67 | 2.50 |  | 0.290 | 0.138 | 0.163 | 0.203 | 0.235 | 0.125 | 0.200 | 0.250 | 0.365  |
|  11,645 | 52 | 2.82 |  | 0.140 | 0.032 | 0.059 | 0.070 | 0.122 | < 0 | 0.030 | 0.115 | 0.200  |
|  11,655 | 57 | 2.64 |  | 0.160 | 0.067 | 0.092 | 0.125 | 0.170 | 0.042 | 0.125 | 0.135 | 0.220  |
|  11,665 | 52 | 2.68 |  | 0.010 | 0.032 | 0.059 | 0.070 | 0.122 | 0.020 | 0.105 | < 0 | 0.030  |
|  11,696 | 50 | 2.76 |  | 0.010 | 0.017 | 0.045 | 0.040 | 0.098 | < 0 | 0.063 | < 0 | 0.030  |
<!-- page 59 -->
48

ASQUITH AND KRYGOWSKI

Table 4.11. Differences in neutron porosity using correct and incorrect charts for the specific neutron tool.

|  Zone | Log Values |   |   | NPHI (incorrect chart for the example data) |   | NPHI (incorrect chart for the example data)  |   |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  Depth | NPHI | RHOB | DT | dolo | sand | dolo | sand  |
|  11,508 |  |  |  |  |  |  |   |
|  11,631 | 0.29 | 2.50 | 67 | 0.250 | 0.365 | 0.210 | 0.335  |
|  11,645 |  |  |  |  |  |  |   |
|  11,655 | 0.16 | 2.64 | 57 | 0.135 | 0.220 | 0.080 | 0.210  |
|  11,665 | 0.01 | 2.68 | 52 | < 0 | 0.030 | < 0 | 0.040  |
|  11,696 |  |  |  |  |  |  |   |

Table 4.12. Lithology determination on the data from the intervals in Figure 4.5, using the curve patterns in Figure 4.8.

|  Depth | Zone range | Raw Data |   |   |   | ND Quicklook  |
| --- | --- | --- | --- | --- | --- | --- |
|   |   |  RHOB | DPHI | PE | NPHI | Lithology  |
|  11,508 | 11,490-11,518 | 2.73 | -0.013 | 5.0 | 0.005 | Limestone  |
|  11,522 | 11,518-11,528 | 2.75 | -0.022 | 3.2 | 0.090 | Dolomite  |
|   | 11,528-11,543 |  |  |  |  | Dolomite w/anhydrite  |
|  11,545 | 11,543-11,546 | 2.67 | 0.020 | 3.7 | 0.130 | Dolomite  |
|  11,560 | 11,546-11,570 | 2.96 | < 0 | 4.8 | -0.010 | Anhydrite  |
|   | 11,570-11,580 |  |  |  |  | Dolomite (w/anhydrite?)  |
|  11,593 | 11,580-11,598 | 2.70 | 0.005 | 5.6 | 0.000 | Limestone  |
|  11,615 | 11,598-11,625 | 2.97 | < 0 | 5.1 | -0.010 | Anhydrite  |
|  11,631 | 11,625-11,641 | 2.50 | 0.125 | 3.8 | 0.290 | Dolomite  |
|  11,645 | 11,641-11,649 | 2.82 | < 0 | 3.5 | 0.140 | Dolomite (w/anhydrite?)  |
|  11,655 | 11,649-11,659 | 2.64 | 0.042 | 3.5 | 0.160 | Dolomite  |
|  11,665 | 11,659-11,680 | 2.68 | 0.020 | 5.5 | 0.010 | Limestone  |
|  11,696 | > 11680 | 2.76 | -0.028 | 5.1 | 0.010 | Limestone w/anhydrite  |

$$N = \frac{\phi_{Nfl} - \phi_N}{\rho_b - \rho_{fl}} \tag{4.10}$$

where:

$\Delta t =$ interval transit time in the formation (from the log)

$\Delta t_{fl} =$ interval transit time in the fluid in the formation

$\rho_b =$ formation bulk density (from the log)

$\rho_{fl} =$ fluid density

$\phi_N =$ neutron porosity (in limestone units, from the log)

$\phi_{Nfl} =$ neutron porosity of the fluid of the formation (usually = 1.0)

Figure 4.15 shows the resulting plot. As in the two-mineral crossplots, a number of common mineral points are plotted. For the common minerals (lithologies) of interest (quartz [sandstone], calcite [limestone], and dolomite), each mineral is associated with a group of points. The open and closed circles connected by dashed lines indicate the location of the point in freshwater and saltwater muds, respectively. The groups of these connected points indicate ranges in porosity.
<!-- page 60 -->
Porosity Logs

49

Table 4.13. Log values from Figures 4.1, 4.3, and 4.5, used to determine porosity and lithology.

|  Depth | Raw Data |   |   |   | Neutron-Density Crossplot  |   |
| --- | --- | --- | --- | --- | --- | --- |
|   |  DT | RHOB | PE | NPHI | Lithology | PhiND  |
|  11,508 | 51 | 2.73 | 5.0 | 0.005 | Limestone | 0.000  |
|  11,522 | 47 | 2.75 | 3.2 | 0.090 | Dolomite | 0.070  |
|  |   |   |   |   |   |   |
|  11,545 | 57 | 2.67 | 3.7 | 0.130 | Dolomite | 0.110  |
|  11,560 | 48 | 2.96 | 4.8 | -0.010 | Anhydrite | 0.000  |
|  |   |   |   |   |   |   |
|  11,593 | 50 | 2.70 | 5.6 | 0.000 | Limestone | 0.000  |
|  11,615 | 51 | 2.97 | 5.1 | -0.010 | Anhydrite | 0.000  |
|  11,631 | 67 | 2.50 | 3.8 | 0.290 | Dolomite (w/anhydrite?) | 0.230  |
|  11,645 | 52 | 2.82 | 3.5 | 0.140 | Dolomite (w/anhydrite?) | 0.100  |
|  11,655 | 57 | 2.64 | 3.5 | 0.160 | Dolomite | 0.130  |
|  11,665 | 52 | 2.68 | 5.5 | 0.010 | Limestone | 0.010  |
|  11,696 | 50 | 2.76 | 5.1 | 0.010 | Dolomitic limestone | 0.005  |

Table 4.14. Log values from Figures 4.1, 4.3, and 4.5, used to determine porosity and lithology.

|  Depth | Raw Data |   |   |   | Neutron-Sonic Crossplot  |   |
| --- | --- | --- | --- | --- | --- | --- |
|   |  DT | RHOB | PE | NPHI | Lithology | PhiNS  |
|  11,508 | 51 | 2.73 | 5.0 | 0.005 | Sandy limestone | 0.000  |
|  11,522 | 47 | 2.75 | 3.2 | 0.090 | Dolomite | 0.070  |
|  |   |   |   |   |   |   |
|  11,545 | 57 | 2.67 | 3.7 | 0.130 | Limestone | 0.130  |
|  11,560 | 48 | 2.96 | 4.8 | -0.010 | Anhydrite | 0.000  |
|  |   |   |   |   |   |   |
|  11,593 | 50 | 2.70 | 5.6 | 0.000 | Limestone | 0.010  |
|  11,615 | 51 | 2.97 | 5.1 | -0.010 | Anhydrite? | 0.000  |
|  11,631 | 67 | 2.50 | 3.8 | 0.290 | Dolomite | 0.240  |
|  11,645 | 52 | 2.82 | 3.5 | 0.140 | Dolomite | 0.120  |
|  11,655 | 57 | 2.64 | 3.5 | 0.160 | Limy dolomite | 0.145  |
|  11,665 | 52 | 2.68 | 5.5 | 0.010 | Sandy limestone | 0.020  |
|  11,696 | 50 | 2.76 | 5.1 | 0.010 | Sandy limestone | 0.010  |
<!-- page 61 -->
50

ASQUITH AND KRYGOWSKI

Table 4.15. Log values from Figures 4.1, 4.3, and 4.5, used to determine porosity and lithology.

|  Depth | Raw Data |   |   |   | Spectral Density Crossplot  |   |
| --- | --- | --- | --- | --- | --- | --- |
|   |  DT | RHOB | PE | NPHI | Lithology | PhiSpD  |
|  11,508 | 51 | 2.73 | 5.0 | 0.005 | Limestone (w/anhydrite?) | 0.000  |
|  11,522 | 47 | 2.75 | 3.2 | 0.090 | Dolomite | 0.060  |
|  |   |   |   |   |   |   |
|  11,545 | 57 | 2.67 | 3.7 | 0.130 | Limy dolomite | 0.080  |
|  11,560 | 48 | 2.96 | 4.8 | -0.010 | Anhydrite | 0.000  |
|  |   |   |   |   |   |   |
|  11,593 | 50 | 2.70 | 5.6 | 0.000 | Limestone | 0.000  |
|  11,615 | 51 | 2.97 | 5.1 | -0.010 | Anhydrite | 0.000  |
|  11,631 | 67 | 2.50 | 3.8 | 0.290 | Limy dolomite | 0.160  |
|  11,645 | 52 | 2.82 | 3.5 | 0.140 | Limy dolomite | 0.010  |
|  11,655 | 57 | 2.64 | 3.5 | 0.160 | Limy dolomite | 0.100  |
|  11,665 | 52 | 2.68 | 5.5 | 0.010 | Limestone | 0.010  |
|  11,696 | 50 | 2.76 | 5.1 | 0.010 | Limestone (w/anhydrite?) | 0.000  |

Data plotted on this crossplot show the following patterns: For a single pure mineralogy, the data plot around the point representing that mineralogy. For binary mineral systems, the data plot along a line connecting the two mineralogical members, with the location of the points along the line indicative of the mineral mixture of each point. For ternary systems, the data plot in a triangle with the three member mineralogies as the vertices of the triangle, and with the location of each data point in the triangle indicative of the mineral mixture of that point. Note that porosity is not predicted from this plot but is determined from the earlier two-component crossplots.

Although two common mineral triangles are usually used as examples (either quartz/calcite/dolomite or calcite/dolomite/anhydrite), any three minerals that plot uniquely on the crossplot can be used. One need not see data clustered around a particular mineral endpoint to sense the presence of a mineral. The presence of small amounts of a mineral tend to draw the data away from the primary mineral (or mineral mixture) and toward the secondary mineral endpoint.

Table 4.16 shows the calculation of M and N values and the resulting lithology estimations from Figure 4.15.

### Mineral-identification Plots

These plots rely on the calculation of apparent matrix values as crossplot parameters. The apparent matrix values are determined (when done graphically) through what are essentially crossplots, created to emphasize matrix values rather than porosity. Apparent matrix density ($\rho_{maa}$) is determined from an equivalent of the neutron-density crossplot and is shown in Figure 4.16. Apparent matrix travel time ($\Delta t_{maa}$) is determined from an equivalent of the neutron-sonic crossplot and is shown in Figure 4.17. The calculation of apparent matrix values (Western Atlas, 1995) is:

$$\rho_{maa} = \frac{\rho_b - \phi_{ND} \times \rho_{fl}}{1 - \phi_{ND}} \tag{4.11}$$

$$\Delta t_{maa} = \frac{\Delta t - \phi_{NS} \times \Delta t_{fl}}{1 - \phi_{NS}} \tag{4.12}$$

where:

$\rho_b$ = bulk density (from the log)

$\rho_{fl}$ = fluid density

$\phi_{ND}$ = neutron-density crossplot porosity

$\Delta t$ = interval transit time (from the log)

$\Delta t_{fl}$ = fluid transit time
<!-- page 62 -->
Porosity Logs

51

Table 4.16. Log values from Figures 4.1, 4.3, and 4.5, lists of values of M and N calculated from the equations above, and lithology estimates from the M-N crossplot.

|  Depth | Raw Data |   |   |   | M-N Lithology Plot  |   |   |
| --- | --- | --- | --- | --- | --- | --- | --- |
|   |  DT | RHOB | PE | NPHI | M | N | Lithology  |
|  11,508 | 51 | 2.73 | 5.0 | 0.005 | 0.798 | 0.578 | Limestone (w/anhydrite?)  |
|  11,522 | 47 | 2.75 | 3.2 | 0.090 | 0.811 | 0.520 | Dolomite  |
|  |   |   |   |   |   |   |   |
|  11,545 | 57 | 2.67 | 3.7 | 0.130 | 0.790 | 0.521 | Dolomite  |
|  11,560 | 48 | 2.96 | 4.8 | -0.010 | 0.719 | 0.515 | Anhydrite  |
|  |   |   |   |   |   |   |   |
|  11,593 | 50 | 2.70 | 5.6 | 0.000 | 0.818 | 0.588 | Limestone  |
|  11,615 | 51 | 2.97 | 5.1 | -0.010 | 0.701 | 0.513 | Anhydrite  |
|  11,631 | 67 | 2.50 | 3.8 | 0.290 | 0.813 | 0.473 | Limy dolomite  |
|  11,645 | 52 | 2.82 | 3.5 | 0.140 | 0.753 | 0.473 | Dolomite  |
|  11,655 | 57 | 2.64 | 3.5 | 0.160 | 0.805 | 0.512 | Limy dolomite  |
|  11,665 | 52 | 2.68 | 5.5 | 0.010 | 0.815 | 0.589 | Limestone  |
|  11,696 | 50 | 2.76 | 5.1 | 0.010 | 0.790 | 0.563 | Dolomite  |

$\phi_{NS}$ = neutron-sonic crossplot porosity

The neutron and density data (through the neutron-density crossplot) produce an apparent matrix density (as well as a neutron-density crossplot porosity), and the neutron and sonic data (through the neutron-sonic crossplot) produce an apparent matrix travel time (as well as a neutron-sonic crossplot porosity).

These two apparent matrix values are then applied to a crossplot (Figure 4.18). In Figure 4.18, the three common lithologies, highlighted in the previous crossplots, occur on the plot as points which are connected to form a triangle. The location of the point on the plot, with respect to that mineral triangle, indicates the relative lithologic mixture. In practice, any three minerals that have unique values (with respect to each other) can be used as endpoints in a mineral triangle (e.g., a calcite, dolomite, and anhydrite choice is common in a known carbonate area). As with the M-N plot described previously, data from a single pure mineralogy plot around the point representing that mineralogy. For binary mineral systems, the data plot along a line connecting the two mineralogical members, with the location of the points along the line indicative of the mineral mixture of each point. Note that porosity is not predicted from this plot, but is determined from the earlier two-component crossplots.

Figures 4.16 and 4.17 and Tables 4.17 and 4.18

show the calculation of apparent matrix values. Figure 4.18 and Table 4.19 show the application of those apparent matrix values to determine lithology.

A variation on this technique was developed with the advent of the $P_e$ curve on the more recent density logs. Using the $P_e$ curve, the bulk-density curve, and the neutron porosity another matrix parameter, apparent matrix volumetric photoelectric factor ($U_{maa}$), can be determined (as shown in Figure 4.19), or its value can be calculated from (Western Atlas, 1995):

$$U_{maa} = \frac{(Pe \times \rho_N) - (\phi_{ND} \times U_{fl})}{1 - \phi_{ND}} \tag{4.13}$$

where:

$U_{fl}$ = fluid volumetric cross section (0.398 barns/cm$^3$ for fresh water, 1.36 barns/cm$^3$ for salt water)

$\phi_{ND}$ = porosity from the neutron-density crossplot

This apparent matrix crossplot then uses apparent matrix density, $\rho_{maa}$, and apparent matrix volumetric cross section, $U_{maa}$, to determine formation lithology (Figure 4.20). As with the $\rho_{maa} - \Delta t_{maa}$ crossplot, the three common lithologies are connected in a mineral triangle, but any three unique mineralogies can be used to estimate a three-mineral solution.

Figures 4.16 and 4.19, and Tables 4.17 and 4.20
<!-- page 63 -->
52

ASQUITH AND KRYGOWSKI

Table 4.17. Log values from Figures 4.1, 4.3, and 4.5, and a list of values of apparent matrix density determined from the crossplot.

|  Depth | Raw Data |   |   |   | Apparent Matrix Values |   |   | MID Plot Lithology  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|   |  DT | RHOB | PE | NPHI | DTmaa | Rhomaa | Umaa  |   |
|  11,508 | 51 | 2.73 | 5.0 | 0.005 |  | 2.74 |  |   |
|  11,522 | 47 | 2.75 | 3.2 | 0.090 |  | 2.89 |  |   |
|  |   |   |   |   |   |   |   |   |
|  11,545 | 57 | 2.67 | 3.7 | 0.130 |  | 2.88 |  |   |
|  11,560 | 48 | 2.96 | 4.8 | -0.010 |  | 2.97 |  |   |
|  |   |   |   |   |   |   |   |   |
|  11,593 | 50 | 2.70 | 5.6 | 0.000 |  | 2.70 |  |   |
|  11,615 | 51 | 2.97 | 5.1 | -0.010 |  | 2.99 |  |   |
|  11,631 | 67 | 2.50 | 3.8 | 0.290 |  | 3.07 |  |   |
|  11,645 | 52 | 2.82 | 3.5 | 0.140 |  | 3.15 |  |   |
|  11,655 | 57 | 2.64 | 3.5 | 0.160 |  | 2.91 |  |   |
|  11,665 | 52 | 2.68 | 5.5 | 0.010 |  | 2.70 |  |   |
|  11,696 | 50 | 2.76 | 5.1 | 0.010 |  | 2.77 |  |   |

Table 4.18. Log values from Figures 4.1, 4.3, and 4.5, and a list values of apparent matrix transit time determined from the crossplot.

|  Depth | Raw Data |   |   |   | Apparent Matrix Values |   |   | MID Plot Lithology  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|   |  DT | RHOB | PE | NPHI | DTmaa | Rhomaa | Umaa  |   |
|  11,508 | 51 | 2.73 | 5.0 | 0.005 | 51.0 | 2.74 |  |   |
|  11,522 | 47 | 2.75 | 3.2 | 0.090 | 43.0 | 2.89 |  |   |
|  |   |   |   |   |   |   |   |   |
|  11,545 | 57 | 2.67 | 3.7 | 0.130 | 47.5 | 2.88 |  |   |
|  11,560 | 48 | 2.96 | 4.8 | -0.010 | 48.0 | 2.97 |  |   |
|  |   |   |   |   |   |   |   |   |
|  11,593 | 50 | 2.70 | 5.6 | 0.000 | 50.0 | 2.70 |  |   |
|  11,615 | 51 | 2.97 | 5.1 | -0.010 | 52.0 | 2.99 |  |   |
|  11,631 | 67 | 2.50 | 3.8 | 0.290 | 43.0 | 3.07 |  |   |
|  11,645 | 52 | 2.82 | 3.5 | 0.140 | 44.0 | 3.15 |  |   |
|  11,655 | 57 | 2.64 | 3.5 | 0.160 | 45.5 | 2.91 |  |   |
|  11,665 | 52 | 2.68 | 5.5 | 0.010 | 51.0 | 2.70 |  |   |
|  11,696 | 50 | 2.76 | 5.1 | 0.010 | 49.5 | 2.77 |  |   |
<!-- page 64 -->
Porosity Logs

53

Table 4.19. Log values from Figures 4.1, 4.3, and 4.5, apparent matrix values from Figures 4.16 and 4.17, and a list of the estimates of lithology determined from the crossplot.

|  Depth | Raw Data |   |   |   | Apparent Matrix Values |   |   | NDS MID Plot  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|   |  DT | RHOB | PE | NPHI | DTmaa | Rhomaa | Umaa | Lithology  |
|  11,508 | 51 | 2.73 | 5.0 | 0.005 | 51.0 | 2.74 |  | Dolomitic sand  |
|  11,522 | 47 | 2.75 | 3.2 | 0.090 | 43.0 | 2.89 |  | Dolomite  |
|  |   |   |   |   |   |   |   |   |
|  11,545 | 57 | 2.67 | 3.7 | 0.130 | 47.5 | 2.88 |  | Dolomite (w/anhydrite?)  |
|  11,560 | 48 | 2.96 | 4.8 | -0.010 | 48.0 | 2.97 |  | Anhydrite  |
|  |   |   |   |   |   |   |   |   |
|  11,593 | 50 | 2.70 | 5.6 | 0.000 | 50.0 | 2.70 |  | Sandy limestone  |
|  11,615 | 51 | 2.97 | 5.1 | -0.010 | 52.0 | 2.99 |  | Anhydrite  |
|  11,631 | 67 | 2.50 | 3.8 | 0.290 | 43.0 | 3.07 |  | Dolomite?  |
|  11,645 | 52 | 2.82 | 3.5 | 0.140 | 44.0 | 3.15 |  | off chart  |
|  11,655 | 57 | 2.64 | 3.5 | 0.160 | 45.5 | 2.91 |  | Dolomite  |
|  11,665 | 52 | 2.68 | 5.5 | 0.010 | 51.0 | 2.70 |  | Sandy limestone (w/dolomite?)  |
|  11,696 | 50 | 2.76 | 5.1 | 0.010 | 49.5 | 2.77 |  | Sandy dolomite  |

Table 4.20. Log values from Figures 4.1, 4.3, and 4.5, and a list of values of apparent matrix transit time determined from the crossplot.

|  Depth | Raw Data |   |   |   | PhiND | Apparent Matrix Values |   |   | MID Plot  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|   |  DT | RHOB | PE | NPHI |   | DTmaa | Rhomaa | Umaa | Lithology  |
|  11,508 | 51 | 2.73 | 5.0 | 0.000 | 0.000 | 51.0 | 2.74 | 13.7 |   |
|  11,522 | 47 | 2.75 | 3.2 | 0.090 | 0.070 | 43.0 | 2.89 | 9.2 |   |
|  |   |   |   |   |   |   |   |   |   |
|  11,545 | 57 | 2.67 | 3.7 | 0.130 | 0.110 | 47.5 | 2.88 | 11.2 |   |
|  11,560 | 48 | 2.96 | 4.8 | -0.010 | 0.000 | 48.0 | 2.97 | 14.3 |   |
|  |   |   |   |   |   |   |   |   |   |
|  11,593 | 50 | 2.70 | 5.6 | 0.000 | 0.000 | 50.0 | 2.70 | 15.2 |   |
|  11,615 | 51 | 2.97 | 5.1 | -0.010 | 0.000 | 52.0 | 2.99 | 15.3 |   |
|  11,631 | 67 | 2.50 | 3.8 | 0.290 | 0.230 | 43.0 | 3.07 | 12.4 |   |
|  11,645 | 52 | 2.82 | 3.5 | 0.140 | 0.100 | 44.0 | 3.15 | 11.1 |   |
|  11,655 | 57 | 2.64 | 3.5 | 0.160 | 0.130 | 45.5 | 2.91 | 10.7 |   |
|  11,665 | 52 | 2.68 | 5.5 | 0.010 | 0.010 | 51.0 | 2.70 | 15.0 |   |
|  11,696 | 50 | 2.76 | 5.1 | 0.010 | 0.005 | 49.5 | 2.77 | 14.5 |   |
<!-- page 65 -->
54

ASQUITH AND KRYGOWSKI

Table 4.21. Log values from Figures 4.1, 4.3, and 4.5, apparent matrix values from Figures 4.16 and 4.19, and a list of the estimates of lithology determined from the crossplot.

|  Depth | Raw Data |   |   |   | PhiND | Apparent Matrix Values |   |   | MID Plot  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|   |  DT | RHOB | PE | NPHI |   | DTmaa | Rhomaa | Umaa | Lithology  |
|  11,508 | 51 | 2.73 | 5.0 | 0.005 | 0.000 | 51.0 | 2.74 | 13.7 | Limestone  |
|  11,522 | 47 | 2.75 | 3.2 | 0.090 | 0.070 | 43.0 | 2.89 | 9.2 | Dolomite  |
|  |   |   |   |   |   |   |   |   |   |
|  11,545 | 57 | 2.67 | 3.7 | 0.130 | 0.110 | 47.5 | 2.88 | 11.2 | Dolomite w/limestone and anhydrite  |
|  11,560 | 48 | 2.96 | 4.8 | -0.010 | 0.000 | 48.0 | 2.97 | 14.3 | Anhydrite  |
|  |   |   |   |   |   |   |   |   |   |
|  11,593 | 50 | 2.70 | 5.6 | 0.000 | 0.000 | 50.0 | 2.70 | 15.2 | Limestone  |
|  11,615 | 51 | 2.97 | 5.1 | -0.010 | 0.000 | 52.0 | 2.99 | 15.3 | Anhydrite  |
|  11,631 | 67 | 2.50 | 3.8 | 0.290 | 0.230 | 43.0 | 3.07 | 12.4 | ???  |
|  11,645 | 52 | 2.82 | 3.5 | 0.140 | 0.100 | 44.0 | 3.15 | 11.1 | ???  |
|  11,655 | 57 | 2.64 | 3.5 | 0.160 | 0.130 | 45.5 | 2.91 | 10.7 | Dolomite w/anhydrite  |
|  11,665 | 52 | 2.68 | 5.5 | 0.010 | 0.010 | 51.0 | 2.70 | 15.0 | Limestone  |
|  11,696 | 50 | 2.76 | 5.1 | 0.010 | 0.005 | 49.5 | 2.77 | 14.5 | Limestone w/anhydrite?  |

show the calculation of apparent matrix values. Figure 4.20 and Table 4.21 show the application of those apparent matrix values to determine lithology.

### Beyond the three-mineral model

For more complex mineralogical solutions, the use of other log measurements is required. These techniques go beyond the crossplotting techniques discussed here. Some techniques are deterministic in nature (as are the crossplot techniques) but rely on iterative computational techniques for a solution. Other techniques rely on the use of statistical techniques to estimate the most likely solution.

Figure 4.21 is an example of a deterministic solution. In this case, shale volume is calculated independently (the gamma ray was used for this example) and was used as one of the input curves. With the additional inputs of interval transit time, neutron porosity, bulk density, and Pe, the software solved for four minerals (beyond the shale volume): calcite, dolomite, anhydrite, and quartz. In the figure, porosity and fluid saturations (from the deep resistivity log) were also determined and are shown incorporated into the same display.

### Implications for Correlation and Mapping

Standard correlation (and mapping) practices use the raw logs (gamma ray, resistivity, etc.) to trace formation boundaries in the subsurface. With the existence of software that can easily and quickly estimate formation lithologies and porosities, the correlation process might be better served (and be more accurate) if correlations were made on the actual quantities of interest (like lithology), instead of on the raw logs, many of which respond to multiple properties of the formations in the subsurface.

This section summarizes the crossplot methods previously discussed.

### CONSISTENCY IN LITHOLOGY PREDICTION

Seven methods to determine lithology have been covered in this chapter. One is based on pattern recognition (quick-look neutron-density), three on the simultaneous use of two porosity tools, and three on the simultaneous use of three porosity tools. Table 4.22 compares the lithology prediction results of these methods. With some exceptions, the results are fairly consistent, but they are not identical. The variation in the results has many sources. Borehole conditions may
<!-- page 66 -->
Porosity Logs

55

Table 4.22: Comparison of lithology estimation from the various crossplot methods.

|  Depth | Zone range | Lithology  |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|   |   |  Neutron-Density Quicklook | Neutron-Density Crossplot | Neutron-Sonic Crossplot | Spectral-Density Crossplot | M-N Crossplot | Neutron-Density-Sonic MID Plot | Neutron-Spectral-Density MID Plot  |
|  11,508 | 11,490-11,518 | Limestone | Limestone | Sandy limestone | Limestone (with anhydrite?) | Sandy dolomite | Dolomitic sand | Limestone  |
|  11,522 | 11,518-11,528 | Dolomite | Dolomite | Dolomite | Dolomite | Limy dolomite | Dolomite | Dolomite  |
|   | 11,528-11,543 | Dolomite with anhydrite |  |  |  |  |  |   |
|  11,545 | 11,543-11,546 | Dolomite | Dolomite | Limestone | Limy dolomite | Dolomite | Dolomite (with anhydrite?) | Dolomite and with limestone anhydrite  |
|  11,560 | 11,546-11,570 | Anhydrite | Anhydrite | Anhydrite | Anhydrite | Anhydrite | Anhydrite | Anhydrite  |
|   | 11,570-11,580 | Dolomite (with anhydrite?) |  |  |  |  |  |   |
|  11,593 | 11,580-11,598 | Limestone | Limestone | Limestone | Limestone | Limestone | Sandy limestone | Limestone  |
|  11,615 | 11,598-11,625 | Anhydrite | Anhydrite | Anhydrite? | Anhydrite | Anhydrite | Anhydrite | Anhydrite  |
|  11,631 | 11,625-11,641 | Dolomite | Dolomite (with anhydrite?) | Dolomite | Limy dolomite | Dolomite | Dolomite? | off chart  |
|  11,645 | 11,641-11,649 | Dolomite (with anhydrite?) | Dolomite (with anhydrite?) | Dolomite | Limy dolomite | Dolomite? | off chart | off chart  |
|  11,655 | 11,649-11,659 | Dolomite | Dolomite | Limy dolomite | Limy dolomite | Dolomite | Dolomite with anhydrite | Dolomite with anhydrite  |
|  11,665 | 11,659-11,680 | Limestone | Limestone | Sandy limestone | Limestone | Dolomite | Sandy limestone (with dolomite?) | Limestone  |
|  11,696 | > 11680 | Limestone with anhydrite | Dolomitic limestone | Sandy limestone | Limestone (with anhydrite?) | Dolomite | Sandy dolomite | Limestone (with anhydrite?)  |
<!-- page 67 -->
56

ASQUITH AND KRYGOWSKI

play a part in the variation, especially since, in this case, the data were used directly from the logs with no attempt at environmental corrections. Formation thickness and, hence, the effect of adjacent beds on the measurement in the target bed also play a part.

The variability of the formations themselves probably has a more significant effect. In a geologic environment like this one (Figure 4.21), it can be expected that the lithologies encountered are not always pure. The response of the individual measurements to that mixture vary between measurements and contribute to the variation seen here.

The results of the crossplots, while not wildly variable, underscores the need for other data, in this case, samples of the formations themselves. Cores through the section would be ideal, but their cost would probably be prohibitive. Cuttings samples would be a good source of lithology information, even given the potential mixing and contamination problems. Sidewall cores, either in this well (if the log analysis could be completed quickly) or in subsequent wells in zones with questionable predicted lithology, would help to reconcile the results shown here.

# REVIEW

1. The three common types of porosity logs are:

- sonic
- density
- neutron

2. The sonic log is a porosity log that measures the interval transit time (delta t, or DT, or Δt) of a com-

pressional sound wave through the formation. The unit of measure is microseconds per foot (μsec/ft) or microseconds per meter (μsec/m). Interval transit time is related to formation porosity.

3. The density log is a porosity log that measures the electron density of a formation. The formation's electron density is related to a formation's bulk density (RHOB or ρb). Bulk density is measured in g/cm³ or Kg/m³. Bulk density, in turn, can be related to formation porosity.

4. Density logs made since about 1980 also have a photoelectric curve (Pe, PE, or PEF) that responds primarily to formation lithology and is affected in only a minor way by porosity and the type of fluids in the pore space.

5. The neutron log is a porosity log that measures the hydrogen concentration in a formation. In shale-free formations where porosity is filled with water, the neutron log can be related to water-filled porosity (PHIN, or NPHI, or φN).

6. In gas reservoirs, the neutron log records a lower porosity than the formation's true porosity because gas has a lower hydrogen concentration than oil or water (gas effect).

7. The neutron-density combination is the most widely used porosity measurement combination. Porosity, adjusted for lithology, can be determined from the neutron-density combination either by a crossplot chart or by formula.

8. Additional uses of the neutron-density combination are:

- detection of gas bearing zones
- determination of lithology
<!-- page 68 -->
Porosity Logs

57


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: 11500 м to 11700 м, increasing downward.

Track 1 (left):
- Curve: GR (gamma ray), scale 0–100 API units, solid line.
- Curve: CALI (caliper), scale 6–16 inches, dashed line.
- Curve behaviour:
  - GR: relatively low and stable (~30–40 API) from 11500 to 11680 м, then increases to ~60 API at 11680–11700 м.
  - CALI: stable at ~8 inches from 11500 to 11680 м, then increases to ~12 inches at 11680–11700 м, indicating borehole enlargement.

Track 2 (right):
- Curve: DT (sonic transit time), scale 40–140 μs/ft, solid line.
- Curve: SP (spontaneous potential), scale -0.1 to 0.3 v/v (decimal), dashed line.
- Curve behaviour:
  - DT: relatively high (~100–110 μs/ft) from 11500 to 11680 м, then drops sharply to ~60 μs/ft at 11680–11700 м.
  - SP: relatively flat near 0.0 v/v from 11500 to 11680 м, then shows a negative deflection to ~-0.05 v/v at 11680–11700 м.

Interval table:
| Интервал, м | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|-------------|------------------------|-------------------|------------------------------|
| 11500–11680 | Не определена          | GR: низкие, стабильные; CALI: стабильная; DT: высокие; SP: стабильная | Вероятно, глинистый или аргиллитовый интервал |
| 11680–11700 | Не определена          | GR: повышенные; CALI: увеличение; DT: резкое снижение; SP: отрицательная аномалия | Вероятно, песчаник или карбонат с высокой проницаемостью |

KEYWORDS: каротаж, ГК, КАЛИ, ПС, ГГК-П, интервал, глубина, аномалия, литология, интерпретация
----


Figure 4.1. Example sonic log with gamma ray log and caliper.

This example is shown to illustrate a common presentation format for sonic logs, and to be used in determining a porosity (SPH) from interval transit time (DT) in Figure 4.2.

Track 1: This track includes both the gamma ray (GR) and caliper (CALI) curves. Note that the gamma ray scale reads from 0 to 100 API units, increasing from left to right in increments of 10 units. The gamma ray curve is represented by a long-dashed line.

The caliper scale ranges from 6 to 16 inches from left to right in one-inch increments, and the curve is represented by a short-dashed line.

Tracks 2 and 3: Both the interval transit time (DT) scale and the porosity (SPH) scales are shown in these tracks. Sonic log interval transit time (DT) is represented by a solid line, on a scale ranging from 140 to 40 μsec/ft increasing from right to left. The sonic porosity measurement (calculated using a limestone matrix value, 47.6 μsec/ft) is shown by a long dashed line on a scale ranging from -0.10 to 0.30 (-10% to 30%) increasing from right to left.
<!-- page 69 -->
58

ASQUITH AND KRYGOWSKI


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
This is a crossplot of porosity (φ) versus interval transit time (Δt) for different lithologies, with two families of curves: "Time Average" (solid red lines) and "Empirical" (dashed black lines).

Axes:
- X-axis: Δt₀, Interval Transit Time (μs/ft), linear scale, range 40 to 140 μs/ft.
- Y-axis: φ, Porosity (%), linear scale, range 0 to 50%.
- The same axes are mirrored on the right side for the same quantities, with identical scale and range.

Curves:
- Solid red lines (Time Average):
  - Labeled curves for different lithologies: "Dolomite", "Coals", "Sandstone", "Limestone", "Shale".
  - Each curve is a smooth, upward-curving line from origin to upper right.
  - For example, at Δt₀ = 100 μs/ft, the "Sandstone" curve is at ~25% porosity; "Limestone" at ~20%; "Dolomite" at ~15%.
- Dashed black lines (Empirical):
  - Labeled curves for different lithologies: "Dolomite", "Coals", "Sandstone", "Limestone", "Shale".
  - These curves are steeper than the Time Average curves, especially at higher porosities.
  - For example, at Δt₀ = 100 μs/ft, the "Sandstone" empirical curve is at ~30% porosity; "Limestone" at ~25%; "Dolomite" at ~20%.

Reference Box:
- Contains two parameters:
  - ρₘ = 1.00 g/cc (1000 kg/m³)
  - Δtₘ = 189 μs/ft (620 μs/m)

Additional Features:
- A blue horizontal line is drawn at φ = 25% porosity, intersecting the "Sandstone" Time Average curve at Δt₀ ≈ 95 μs/ft.
- A blue vertical line is drawn at Δt₀ = 100 μs/ft, intersecting the "Sandstone" Time Average curve at φ ≈ 25%.
- The intersection point is labeled "Bₘ" (likely meaning "bulk" or "matrix" point).

> Тренд: Porosity increases with increasing interval transit time for all lithologies. The "Empirical" curves predict higher porosity than the "Time Average" curves for the same Δt₀, especially at higher porosities. The curves are lithology-specific, with shale having the highest porosity for a given Δt₀ and dolomite the lowest.

KEYWORDS: porosity, interval transit time, time average, empirical, lithology, sandstone, limestone, dolomite, shale, coals, crossplot, sonic log, Δt, ρₘ, Δtₘ
----


Courtesy Halliburton Energy Services, ©1994 Halliburton Energy Services

Figure 4.2. Chart for converting interval transit time (Δt) to sonic porosity (φz).

Procedure:

1. Find the interval transit time (DT) taken from the sonic log in Figure 4.1 on the scale at the bottom of the chart.
2. To calculate sonic limestone porosity using the Wyllie time-average equation (labeled "Time Average"), follow the DT value vertically until it intersects the calcite line, then move horizontally to intersect the y-axis and read the porosity value.
3. To calculate sonic dolomite porosity using the Wyllie time-average equation, follow the procedure in step 2 above, except intersect the dolomite line instead of the calcite line.
4. To calculate sonic limestone porosity using the Raymer-Hunt-Gardner (RHG) equation (curved lines, labeled "Empirical"), follow the DT value vertically until it intersects the curved calcite line, then move horizontally to intersect the y-axis and read the porosity value.
5. To calculate sonic dolomite porosity using the Raymer-Hunt-Gardner (RHG) equation, follow the procedure in step 4 above, except intersect the curved dolomite line instead of the curved calcite line.

NOTE: While the values in Table 4.6 are in decimal, the porosity values on the chart are in percent.
<!-- page 70 -->
Porosity Logs

59


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Глубина увеличивается вниз. Диапазон глубин: 11500–11700 м. Единицы глубины: м (MD — measured depth).

Треки слева направо:

1. **GR (Гамма-каротаж)**:
   - Шкала: 0–100 API units.
   - Кривая: сплошная линия.
   - Поведение: в интервале 11500–11700 м — колебания от ~40 до ~80 API units, с локальными пиками ~80–90 API units.

2. **CALI (Калибровка)**:
   - Шкала: 6–16 inches.
   - Кривая: пунктирная линия.
   - Поведение: в интервале 11500–11700 м — стабильная, ~8–9 inches, без значительных отклонений.

3. **PEF (Плотность электронов, фотоэлектрический фактор)**:
   - Шкала: 0–10 (без единиц, но по контексту — бор-единицы).
   - Кривая: сплошная линия.
   - Поведение: в интервале 11500–11700 м — колебания от ~3 до ~7, с локальными минимумами ~3–4 и максимумами ~6–7.

4. **DRHO (Плотность породы, измеренная по гамма-гамма методу)**:
   - Шкала: -0,05–0,45 g/cm³ (относительная шкала, вероятно, отклонение от эталона).
   - Кривая: сплошная линия.
   - Поведение: в интервале 11500–11700 м — колебания от ~0,15 до ~0,35 g/cm³, с локальными минимумами ~0,15–0,20 и максимумами ~0,30–0,35.

5. **RHOB (Плотность породы, измеренная по нейтронному методу)**:
   - Шкала: 0–3 g/cm³.
   - Кривая: сплошная линия.
   - Поведение: в интервале 11500–11700 м — колебания от ~2,0 до ~2,8 g/cm³, с локальными минимумами ~2,0–2,2 и максимумами ~2,6–2,8.

Интерпретация:
- Нет подписанных интервалов, контактов, перфораций или результатов петрофизической интерпретации (Кп, Кн, Кпр и т.д.).
- Кривые GR и PEF показывают изменчивость, что может указывать на изменение литологии (например, переходы между алевролитами, песчаниками и глинами).
- Кривые DRHO и RHOB демонстрируют схожую тенденцию, что свидетельствует о согласованности измерений плотности.
- CALI стабильна — бурение в стабильном диаметре, без значительных каверн.

KEYWORDS: каротаж, ГК, ПС, ГГК-П, НГК, калибровка, плотность породы, фотоэлектрический фактор, интервал 11500–11700 м, петрофизика, буровой журнал
----


Figure 4.3. Example density log with gamma ray and caliper.

This example is shown to illustrate a common presentation format for a density log, and to be used in determining a porosity (DPHI) from bulk density (RHOB) in Figure 4.4.

Track 1: This track includes both the gamma ray (GR) and caliper (CALI) curves. Both scales increase from left to right. The gamma ray values range from 0 to 100 API gamma ray units, and the caliper measures the borehole diameter from 6 to 16 inches.

Track 2: The density log correction curve (DRHO) ranges in value from $-0.05\mathrm{g/cm^3}$ to $+0.45\mathrm{g/cm^3}$ in increments of $0.05\mathrm{g/cm^3}$. It is shown as a light, dashed line. The photoelectric effect curve (PEF) ranges from 0 to $10\mathrm{b/e}$ and is shown as a heavy, dashed line. (The dashes on the PEF curve are longer than those on the DRHO curve.)

Tracks 2 and 3: The bulk-density (RHOB) scale ranges in value from $2.0\mathrm{g/cm^3}$ to $3.0\mathrm{g/cm^3}$ and the curve is a solid line.
<!-- page 71 -->
60

ASQUITH AND KRYGOWSKI


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
This is a crossplot of porosity versus bulk (log) density, used for lithology identification and porosity estimation from density logs.

- **X-axis**: ρ_b, Bulk (Log) Density (g/cc or 1000 kg/m³), linear scale, range from 1.9 to 2.9.
- **Y-axis**: Porosity (%), linear scale, range from -10 to 50.
- **Grid**: Fine grid with major divisions every 0.1 on x-axis and every 10% on y-axis.

Five diagonal lines are plotted, each representing a different matrix density (ρ_ma) for a specific mineral:

1. **ρ_ma = 2.644 g/cc or 2644 kg/m³ (Quartz)** — solid line, steepest slope.
2. **ρ_ma = 2.677 g/cc or 2677 kg/m³** — dashed line.
3. **ρ_ma = 2.71 g/cc or 2710 kg/m³ (Calcite)** — dash-dot line.
4. **ρ_ma = 2.835 g/cc or 2835 kg/m³** — dash-dot-dot line.
5. **ρ_ma = 2.877 g/cc or 2877 kg/m³ (Dolomite)** — dotted line, shallowest slope.

Each line represents the theoretical relationship between porosity and bulk density for a rock composed of that matrix mineral and pore space filled with fluid of density 1.00 g/cc (as indicated by the vertical dashed line at ρ_b = 1.00 g/cc, labeled "ρ_f = 1.00 (g/cc)").

The lines are labeled with their matrix density values and mineral names where applicable. The lines are arranged such that higher matrix density corresponds to a shallower slope.

> Тренд: As matrix density increases, the bulk density for a given porosity increases, resulting in a shallower slope on the porosity vs. bulk density plot. The lines allow estimation of porosity from measured bulk density and identification of lithology based on which line the data point falls closest to.

KEYWORDS: porosity, bulk density, lithology identification, crossplot, matrix density, quartz, calcite, dolomite, log interpretation, Schlumberger, Halliburton
----


Figure 4.4. Chart for converting bulk density ($\rho_b$, RH08) to density porosity ($\phi_b$, DPHI).

Procedure:

1. Find the bulk density (RH08) taken from the density log in Figure 4.3 on the scale at the bottom of the chart. Note that the scale is displayed from high values on the left to low values on the right.
2. Follow the RH08 value vertically until it intersects the proper matrix line [calcite (limestone) or dolomite] then move horizontally to intersect the y-axis representing the proper fluid density, in this case 1.00 g/cm³ (fresh water, the middle scale) to read the porosity (DPHI).

NOTE: The values in Table 4.8 are decimal fractions, the porosity values on the chart are in percent.
<!-- page 72 -->
Porosity Logs

61


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: increases downward, units: feet (MD), range: 11500 ft to 11700 ft.

Track 1 (leftmost):
- Curve: GR (gamma ray), scale: 0–100 API, units: API, line style: solid.
- Curve: CALI (caliper), scale: 40–16 in, units: inches, line style: dashed.
- Curve: "Delta" (likely Δt or sonic travel time), scale: 0–16, units: unspecified (likely μs/ft), line style: solid.

Track 2 (rightmost):
- Curve: PEF (photoelectric factor), scale: 0–10, units: no units specified, line style: solid.
- Curve: DRHO (density, bulk density), scale: 0.05–0.45 g/cm³, units: g/cm³, line style: solid.
- Curve: NPHI (neutron porosity), scale: 0.1–0.3 vs decimal, units: decimal fraction, line style: dashed.
- Curve: "vs decimal" (likely a duplicate or secondary scale for NPHI), scale: 0.1–0.3, units: decimal, line style: dashed.

Interval table:

| Интервал, ft | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|--------------|------------------------|-------------------|-------------------------------|
| 11500–11550  | Не определена          | GR: высокие показания (~80–100 API); CALI: узкий (~40 in); Δt: низкие (~10–12); PEF: ~5–6; DRHO: ~2.3–2.4 g/cm³; NPHI: ~0.15–0.20 | Вероятно, глина или аргиллит |
| 11550–11600  | Не определена          | GR: умеренные (~40–60 API); CALI: узкий (~40–42 in); Δt: ~12–14; PEF: ~4–5; DRHO: ~2.2–2.3 g/cm³; NPHI: ~0.20–0.25 | Вероятно, песчаник или алевролит |
| 11600–11650  | Не определена          | GR: низкие (~20–30 API); CALI: узкий (~40 in); Δt: ~14–16; PEF: ~3–4; DRHO: ~2.1–2.2 g/cm³; NPHI: ~0.25–0.30 | Вероятно, чистый песчаник |
| 11650–11700  | Не определена          | GR: умеренные (~40–60 API); CALI: узкий (~40–42 in); Δt: ~12–14; PEF: ~4–5; DRHO: ~2.2–2.3 g/cm³; NPHI: ~0.20–0.25 | Вероятно, песчаник с глинистым цементом |

No results panel (Кп, Кн, Кпр, etc.) is visible.

KEYWORDS: well log, gamma ray, caliper, sonic, density, neutron porosity, photoelectric factor, depth, feet, interpretation, lithology
----


Figure 4.5. Example combination neutron density log with gamma ray and caliper.

This example is shown to illustrate a common presentation format for a neutron density combination, to be used in applying a lithology conversion to the neutron porosity in Figure 4.6, and in determining lithology and crossplot porosity from the neutron-density crossplot in Figure 4.8.

Track 1: This track contains both gamma ray (GR) and caliper (CALI). Note that the gamma ray scale reads from 0 to 100 API units and the caliper measures a borehole size from 6 to 16 inches.

Track 2: The photoelectric effect (PEF) is displayed from 0 to 10 b/e. The density correction (DRHO) is displayed from -0.05 to +0.45 g/cm³.

Tracks 2 and 3: Both neutron porosity (NPHI) and density porosity (DPHI) are plotted across tracks 2 and 3. The scale for both is the same, ranging from -0.10 (-10%) to 0.30 (+30%), and is expressed in limestone porosity units. On this log the density porosity (DPHI) is represented by a solid line, and the neutron porosity (NPHI) is represented by a dashed line.
<!-- page 73 -->
62

ASQUITH AND KRYGOWSKI

Figure 4.6. Chart for correcting Halliburton DSN-II neutron-porosity curve for lithology.

NOTE: For neutron logs, the chart used to correct the logged porosity for lithology MUST correspond to the type of neutron log run, and the company used to acquire the log data. A mismatch between the actual log used and the chart used for the conversion can lead to significant errors in the determination of lithology.

# Procedure:

1. Find the neutron porosity (NPHI) taken from the neutron density log in Figure 4.2 on the scale at the bottom of the chart. The original neutron log data is referenced to limestone lithology.
2. Follow the NPHI value vertically until it intersects the proper matrix line (Dolomite or Sandstone) then move horizontally to intersect the y-axis the porosity, NPHI. Use the smallest value Σ_nna for each lithology to do the calculations.

NOTE: The values in the table are decimal fractions, but the porosity values on the chart are in percent.


----
━━━ FORMAT 7: NOMOGRAM / ПАЛЕТКА ━━━
Палетка для интерпретации пористости по данным нейтронного каротажа в зависимости от литологии.

График представляет собой номограмму с двумя осями:
- Ось абсцисс (горизонтальная): "Φₙ,ₗₛ, Neutron Limestone Porosity (%)", линейная шкала от -5 до 45.
- Ось ординат (вертикальная): "Φ, Porosity (%)", линейная шкала от -5 до 45.

На графике изображены три кривые, соответствующие различным литологическим типам:
1. Кривая "SANDSTONE" — для песчаника.
2. Кривая "DOLOSTONE" — для доломита.
3. Кривая "LIMESTONE" — для известняка.

Каждая кривая имеет маркировку "0% clay", "10% clay", "20% clay", "30% clay", "40% clay", "50% clay", что указывает на содержание глинистости как параметр семейства кривых.

Примеры ориентировочных точек (снято с графика, приблизительно):
- Для песчаника (SANDSTONE) при 0% глинистости: Φₙ,ₗₛ = 20% → Φ = 20%
- Для песчаника при 40% глинистости: Φₙ,ₗₛ = 20% → Φ ≈ 15%
- Для доломита (DOLOSTONE) при 0% глинистости: Φₙ,ₗₛ = 20% → Φ ≈ 25%
- Для доломита при 40% глинистости: Φₙ,ₗₛ = 20% → Φ ≈ 18%
- Для известняка (LIMESTONE) при 0% глинистости: Φₙ,ₗₛ = 20% → Φ = 20%
- Для известняка при 40% глинистости: Φₙ,ₗₛ = 20% → Φ ≈ 15%

Процедура чтения: по оси абсцисс задаётся значение нейтронной пористости в известняке (Φₙ,ₗₛ), затем по кривой, соответствующей литологии и глинистости, снимается истинная пористость (Φ) по оси ординат.

KEYWORDS: нейтронный каротаж, пористость, палетка, песчаник, доломит, известняк, глинистость, интерпретация, кривые, литология
----


Courtesy Halliburton Energy Services, ©1994 Halliburton Energy Services

Figure 4.7. Chart for correcting Schlumberger CNL thermal-neutron curves (NPHI and TNPH) for lithology.

NOTE: For neutron logs, the chart used to correct the logged porosity for lithology MUST correspond to the type of neutron log run, and the company used to acquire the log data. A mismatch between the actual log used and the chart used for the conversion can lead to significant errors in the determination of lithology.

In the example, the Halliburton neutron log from Figure 4.5, is corrected using a Schlumberger chart (NPHI curves). Note the difference in porosity results between the charts.


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
This is a crossplot of true porosity versus apparent limestone neutron porosity, used for neutron log interpretation in different lithologies.

- X-axis: φ_NL,apparent — apparent limestone neutron porosity (p.u.), linear scale, range 0 to 40.
- Y-axis: φ_t — true porosity for indicated matrix material, linear scale, range 0 to 40.
- The plot contains five curves, each representing a different matrix material:
  1. **Shale** — dashed red line, labeled "Shale" in red.
  2. **Sandstone** — dashed red line, labeled "Sandstone" in red.
  3. **Limestone** — solid black line, labeled "Limestone" in black.
  4. **Dolomite** — solid black line, labeled "Dolomite" in black.
  5. **Anhydrite** — solid black line, labeled "Anhydrite" in black.

- The curves are labeled with their respective matrix names. The shale and sandstone curves are dashed and red; the limestone, dolomite, and anhydrite curves are solid and black.
- The curve for limestone is the 1:1 diagonal line, indicating that for limestone, apparent limestone neutron porosity equals true porosity.
- The curve for dolomite lies below the limestone line, indicating that for a given true porosity, the apparent limestone neutron porosity is lower in dolomite.
- The curve for anhydrite lies below the dolomite curve, indicating even lower apparent porosity for a given true porosity.
- The curves for shale and sandstone lie above the limestone line, indicating that for a given true porosity, the apparent limestone neutron porosity is higher in these materials.

> Тренд: Для пород с матрицей, отличной от известняка, показания нейтронного каротажа (в единицах известняка) не равны истинной пористости. Для доломита и ангидрита показания ниже истинной пористости, для глины и песчаника — выше. Истинная пористость может быть определена по кривой, соответствующей матрице породы.

KEYWORDS: нейтронный каротаж, истинная пористость, кажущаяся пористость, известняковая шкала, глина, песчаник, доломит, ангидрит, кривые корреляции, интерпретация ГИС
----


Courtesy Schlumberger Wireline & Testing, ©1998 Schlumberger
<!-- page 74 -->
Porosity Logs

63


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: 8600 to 8700 feet, increasing downward. Depth units: feet (MD).

Tracks (left to right):

1. GR (Gamma Ray): Scale 0–100 API units. Curve is stepwise, with high values in shale intervals, low values in limestone, dolomite, anhydrite, salt, and coal. Specific values:
   - 8600–8610 ft: ~80 API (shale)
   - 8610–8620 ft: ~30 API (limestone)
   - 8620–8630 ft: ~40 API (dolomite)
   - 8630–8640 ft: ~80 API (shale)
   - 8640–8650 ft: ~30 API (sandstone)
   - 8650–8660 ft: ~30 API (sandstone)
   - 8660–8670 ft: ~30 API (anhydrite)
   - 8670–8680 ft: ~80 API (shale)
   - 8680–8690 ft: ~80 API (shale)
   - 8690–8700 ft: ~80 API (shale)

2. PEF (Photoelectric Factor): Scale 0–10 b/e. Curve is stepwise, with high values in shale and sandstone, low values in limestone, dolomite, anhydrite, salt, and coal. Specific values:
   - 8600–8610 ft: ~5 b/e (shale)
   - 8610–8620 ft: ~2 b/e (limestone)
   - 8620–8630 ft: ~3 b/e (dolomite)
   - 8630–8640 ft: ~5 b/e (shale)
   - 8640–8650 ft: ~5 b/e (sandstone)
   - 8650–8660 ft: ~5 b/e (sandstone)
   - 8660–8670 ft: ~3 b/e (anhydrite)
   - 8670–8680 ft: ~5 b/e (shale)
   - 8680–8690 ft: ~5 b/e (shale)
   - 8690–8700 ft: ~5 b/e (shale)

3. RHOB (Bulk Density): Scale 1.95–2.95 g/cm³. Curve is stepwise, with low values in shale and sandstone, high values in limestone, dolomite, anhydrite, and salt. Specific values:
   - 8600–8610 ft: ~2.5 g/cm³ (shale)
   - 8610–8620 ft: ~2.7 g/cm³ (limestone)
   - 8620–8630 ft: ~2.8 g/cm³ (dolomite)
   - 8630–8640 ft: ~2.5 g/cm³ (shale)
   - 8640–8650 ft: ~2.3 g/cm³ (sandstone)
   - 8650–8660 ft: ~2.3 g/cm³ (sandstone)
   - 8660–8670 ft: ~2.9 g/cm³ (anhydrite)
   - 8670–8680 ft: ~2.5 g/cm³ (shale)
   - 8680–8690 ft: ~2.1 g/cm³ (salt)
   - 8690–8700 ft: ~2.5 g/cm³ (shale)

4. PHIN (Neutron Porosity): Scale -0.15 to 0.45 v/v decimal. Curve is stepwise, with high values in shale and sandstone, low values in limestone, dolomite, anhydrite, salt, and coal. Specific values:
   - 8600–8610 ft: ~0.30 v/v (shale)
   - 8610–8620 ft: ~0.15 v/v (limestone)
   - 8620–8630 ft: ~0.15 v/v (dolomite)
   - 8630–8640 ft: ~0.30 v/v (shale)
   - 8640–8650 ft: ~0.35 v/v (sandstone)
   - 8650–8660 ft: ~0.35 v/v (sandstone)
   - 8660–8670 ft: ~0.15 v/v (anhydrite)
   - 8670–8680 ft: ~0.30 v/v (shale)
   - 8680–8690 ft: ~0.30 v/v (shale)
   - 8690–8700 ft: ~0.30 v/v (shale)

Lithology column (rightmost track) with interpreted intervals:

| Интервал, ft | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|--------------|------------------------|-------------------|-------------------------------|
| 8600–8610    | shale                  | GR: high (~80), PEF: ~5, RHOB: ~2.5, PHIN: ~0.30 | Shale interval |
| 8610–8620    | limestone              | GR: low (~30), PEF: ~2, RHOB: ~2.7, PHIN: ~0.15 | Limestone interval |
| 8620–8630    | dolomite               | GR: ~40, PEF: ~3, RHOB: ~2.8, PHIN: ~0.15 | Dolomite interval |
| 8630–8640    | shale                  | GR: high (~80), PEF: ~5, RHOB: ~2.5, PHIN: ~0.30 | Shale interval |
| 8640–8650    | sandstone              | GR: low (~30), PEF: ~5, RHOB: ~2.3, PHIN: ~0.35 | Sandstone interval |
| 8650–8660    | sandstone              | GR: low (~30), PEF: ~5, RHOB: ~2.3, PHIN: ~0.35 | Sandstone interval |
| 8660–8670    | anhydrite              | GR: ~30, PEF: ~3, RHOB: ~2.9, PHIN: ~0.15 | Anhydrite interval |
| 8670–8680    | shale                  | GR: high (~80), PEF: ~5, RHOB: ~2.5, PHIN: ~0.30 | Shale interval |
| 8680–8690    | salt                   | GR: ~30, PEF: ~3, RHOB: ~2.1, PHIN: ~0.30 | Salt interval |
| 8690–8700    | shale                  | GR: high (~80), PEF: ~5, RHOB: ~2.5, PHIN: ~0.30 | Shale interval |

Additional lithology labels below 8700 ft:
- 8700–8710 ft: coal (GR: ~80, PEF: ~5, RHOB: ~1.8, PHIN: ~0.30)
- 8710–8720 ft: shale (GR: ~80, PEF: ~5, RHOB: ~2.5, PHIN: ~0.30)
- 8720–8730 ft: limy dolomite (GR: ~40, PEF: ~3, RHOB: ~2.7, PHIN: ~0.20)
- 8730–8740 ft: sandy dolomite (GR: ~40, PEF: ~3, RHOB: ~2.6, PHIN: ~0.25)
- 8740–8750 ft: dolomitic sand (GR: ~30, PEF: ~5, RHOB: ~2.4, PHIN: ~0.30)
- 8750–8760 ft: shale (GR: ~80, PEF: ~5, RHOB: ~2.5, PHIN: ~0.30)

KEYWORDS: well log, gamma ray, photoelectric factor, bulk density, neutron porosity, lithology, shale, limestone, dolomite, sandstone, anhydrite, salt, coal, depth, feet, API units, g/cm³, v/v decimal
----


Figure 4.8. Example of the generalized lithologic response of the neutron and density logs, used as a quick-look lithology technique.

The gamma ray (GR) and photoelectric effect (PEF) are provided for additional information.

# Procedure:

The neutron-porosity and density-porosity curves are scanned for their relationship to each other and for their values. The relative position of the curves is an indicator of the lithology encountered, and the average of the two curves at any depth is a good approximation of the porosity (within two porosity units).

The gamma ray may be used to distinguish ambiguous patterns, like shale and dolomite patterns.

The photoelectric effect may be used to distinguish ambiguous patterns (sandy limestone from dolomitic sand) or to confirm the neutron-density interpretation.

# Assumptions:

- There is liquid in the pore space, either water or oil but not gas.
- The formations encountered do not contain clay (except for the shale).
- Both porosity curves are referenced to limestone.

Note the lithology interpretations listed on the log.
<!-- page 75 -->
64

ASQUITH AND KRYGOWSKI


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: increases downward, units: Feet (MD), range: 8500 to 8600 ft.

Track 1 (leftmost):
- Curve: GR (Gamma Ray)
- Scale: 0 to 150 API units
- Line style: solid black line
- Qualitative behaviour:
  - 8500–8510 ft: high GR (~140 API) — shale
  - 8510–8520 ft: low GR (~20 API) — salt
  - 8520–8530 ft: high GR (~140 API) — shale
  - 8530–8540 ft: moderate GR (~60 API) — shaly gas sand
  - 8540–8550 ft: moderate GR (~70 API) — shaly oil sand
  - 8550–8560 ft: moderate GR (~60 API) — shaly wet sand
  - 8560–8570 ft: low GR (~30 API) — clean wet sand
  - 8570–8580 ft: high GR (~140 API) — shale
  - 8580–8590 ft: moderate GR (~50 API) — dolomite
  - 8590–8600 ft: high GR (~140 API) — shale
  - Below 8600 ft: high GR (~140 API) — limestone, then shale

Track 2 (rightmost):
- Curves: PHIE (porosity, φ, decimal), PHID (density porosity, φ, decimal), PHIN (neutron porosity, φ, decimal)
- Scale: 0 to 0.6 (decimal)
- Line styles:
  - PHIE: solid line
  - PHID: dashed line
  - PHIN: dash-dotted line
- Qualitative behaviour:
  - 8500–8510 ft: all curves near 0 — shale
  - 8510–8520 ft: all curves near 0 — salt
  - 8520–8530 ft: all curves near 0 — shale
  - 8530–8540 ft: PHIE ~0.25, PHID ~0.25, PHIN ~0.25 — shaly gas sand
  - 8540–8550 ft: PHIE ~0.25, PHID ~0.25, PHIN ~0.25 — shaly oil sand
  - 8550–8560 ft: PHIE ~0.25, PHID ~0.25, PHIN ~0.25 — shaly wet sand
  - 8560–8570 ft: PHIE ~0.30, PHID ~0.30, PHIN ~0.30 — clean wet sand
  - 8570–8580 ft: all curves near 0 — shale
  - 8580–8590 ft: PHIE ~0.15, PHID ~0.15, PHIN ~0.15 — dolomite
  - 8590–8600 ft: all curves near 0 — shale
  - Below 8600 ft: PHIE ~0.15, PHID ~0.15, PHIN ~0.15 — limestone, then shale

Interval Table:
| Интервал, ft | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|--------------|--------------------------|-------------------|-------------------------------|
| 8500–8510    | shale                    | GR: высокие (~140), PHIE/PHID/PHIN: ~0 | шельфовая глина |
| 8510–8520    | salt                     | GR: низкие (~20), PHIE/PHID/PHIN: ~0 | соль |
| 8520–8530    | shale                    | GR: высокие (~140), PHIE/PHID/PHIN: ~0 | глина |
| 8530–8540    | shaly gas sand           | GR: ~60, PHIE/PHID/PHIN: ~0.25 | газоносный песчаник с глинистостью |
| 8540–8550    | shaly oil sand           | GR: ~70, PHIE/PHID/PHIN: ~0.25 | нефтеносный песчаник с глинистостью |
| 8550–8560    | shaly wet sand           | GR: ~60, PHIE/PHID/PHIN: ~0.25 | водонасыщенный песчаник с глинистостью |
| 8560–8570    | clean wet sand           | GR: ~30, PHIE/PHID/PHIN: ~0.30 | чистый водонасыщенный песчаник |
| 8570–8580    | shale                    | GR: ~140, PHIE/PHID/PHIN: ~0 | глина |
| 8580–8590    | dolomite                 | GR: ~50, PHIE/PHID/PHIN: ~0.15 | доломит |
| 8590–8600    | shale                    | GR: ~140, PHIE/PHID/PHIN: ~0 | глина |
| 8600–8610    | limestone                | GR: ~140, PHIE/PHID/PHIN: ~0.15 | известняк |
| 8610–8620    | shale                    | GR: ~140, PHIE/PHID/PHIN: ~0 | глина |

KEYWORDS: well log, gamma ray, porosity, PHIE, PHID, PHIN, shaly sand, clean sand, dolomite, limestone, salt, depth, feet, API units, decimal porosity, interpretation
----


Figure 4.9. Example of the generalized lithologic response of the neutron and density logs, used as a quick-look lithology technique. This example is primarily for showing log response in shaly formations, and when the porosity curves are referenced to sandstone.

Procedure:

The neutron-porosity and density-porosity curves are scanned for their relationship to each other, and for their values. The relative position of the curves is an indicator of the lithology encountered.

Assumptions:

- There is liquid in the pore space, either water or oil, but not gas, except in the intervals where noted.
- The formations encountered do not contain clay (except in the intervals where noted).
- The density and neutron-porosity curves (PHID and PHIN) are referenced to sandstone. PHIE is the effective porosity, calculated from PHIN and PHID.

The Interpretation:

The neutron and density measurements depend on the amount of clay present in the formation and the physical properties of that clay. In general, the presence of clay in a liquid-filled formation causes the neutron log to read higher than actual porosity, while the density log reads lower than actual porosity. In a liquid-filled sandstone (when the measurements are referenced to sandstone), the curves separate with the neutron higher than the density.

Gas in the formation drives the neutron value lower than actual porosity and the density value slightly higher than actual porosity, resulting in the neutron log reading lower than the density log, the classic crossover response.

With both gas and clays in the formation, the response is not fully predictable because the two effects simultaneously work in opposite ways on both measurements. In very shaly formations with low to medium gas saturations, the presence of gas may be noted only by a decrease in the crossover effect. In formations with medium gas saturations and small amounts of shale, there may be no noticeable gas effect, with the curves at approximately the same values.

The illustration here is but one of many possible examples of the log responses in shaly gas-bearing formations.
<!-- page 76 -->
Porosity Logs

65


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: increases downward, units: Feet MD. Depth range visible: approximately 14600–14650 ft.

Track 1 (left):
- Curve: GR (gamma ray), scale: 0–100 API units, line style: solid.
- Curve: CALI (caliper), scale: 6–16 inches, line style: dashed.
- Curve: Bit Size, scale: 6–16 inches, line style: dash-dotted.
- Qualitative behaviour:
  - GR: high values (~80–100 API) in upper interval, sharp drop to ~20–30 API at ~14620 ft, then fluctuates.
  - CALI: relatively stable at ~10–11 inches, then expands to ~14–16 inches below ~14620 ft.
  - Bit Size: constant at ~12 inches throughout.

Track 2 (right):
- Curve: DPHI (density porosity), scale: 0.45 to -0.15 vv decimal, line style: solid.
- Curve: NPHI (neutron porosity), scale: 0.45 to -0.15 vv decimal, line style: dashed.
- Qualitative behaviour:
  - DPHI: high (~0.40) in upper interval, drops sharply to ~0.20 at ~14620 ft, then fluctuates between 0.15–0.30.
  - NPHI: high (~0.40) in upper interval, drops to ~0.20 at ~14620 ft, then fluctuates between 0.15–0.30, often crossing DPHI.
  - Crossplot interpretation: DPHI > NPHI in upper interval (suggests gas or low-density matrix), DPHI ≈ NPHI below ~14620 ft (suggests water or mixed lithology).

Interval table:
| Интервал, м | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|-------------|-------------------------|-------------------|-------------------------------|
| ~14600–14620 | Не определена | GR: высокие, CALI: узкая, DPHI/NPHI: высокие, DPHI > NPHI | Вероятно, глинистый песчаник или аргиллит с газом |
| ~14620–14650 | Не определена | GR: низкие, CALI: расширенная, DPHI/NPHI: средние, DPHI ≈ NPHI | Вероятно, водонасыщенный песчаник или алевролит |

No results panel (Кп, Кн, Кпр, etc.) visible.

KEYWORDS: каротаж, ГК, КС, ПС, ГГК-П, плотность, нейтрон, пористость, интерпретация, колонка, глубина, фильтрация, калибр, бит
----


Figure 4.10. An example of neutron and density porosity response in a gas zone.

The interval from 14,601 ft to 14,624 ft shows the (low) gamma ray response of a reservoir and the neutron-density crossover (NPHI < DPHI) of a gas-bearing zone. The neutron- and density-porosity curves are referenced to the lithology of the zone.

NOTE: Curves recorded in apparent limestone units show a false crossover in a sandstone, because of the lithologic effect.
<!-- page 77 -->
66

ASQUITH AND KRYGOWSKI

Figure 4.11. Neutron-density crossplot.

Lithology and porosity can be determined from the neutron-density crossplot.

Procedure:

1. The point is located on the plot from the intersection of the neutron and density (limestone) values. Density may be bulk density (left axis of chart) or density porosity (right axis of chart).
2. The porosity of the point is determined by its location relative to lines connecting points of equal porosity on the two lithology lines between which it is plotted. Note that the neutron porosity (NPHI) values in Table 4.13 are decimal fractions, and the neutron limestone porosity values in Figure 4.11 are in percent. A value listed as 0.010 in the table is equal to a value of 1% on the figure.
3. The lithology of the point is determined by its location relative to the two lithology lines, with the proximity to each line on indication of the percentage of each of the mineral pairs. Note that the lithology determination can be ambiguous (e.g., a point lying between the calcite and dolomite lines also lies between the quartz and dolomite lines). Use the smallest value Σma for each lithology to do the calculations.


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
This is a crossplot of bulk (log) density versus neutron limestone porosity, used for lithology and porosity interpretation in well logging.

Left vertical axis: ρb, Bulk (Log) Density (g/cc or 1000 kg/m³), linear scale, range 3.0 to 1.9 (increasing downward).
Right vertical axis: φL.S., Limestone Porosity (%), linear scale, range 0 to 45 (increasing upward).
Horizontal axis: φN.L.S., Neutron Limestone Porosity (%), linear scale, range 0 to 45 (increasing rightward).

The plot contains three main diagonal reference lines for pure lithologies:
- Top line: Dolomite, with porosity labels 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100%.
- Middle line: Limestone, with porosity labels 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100%.
- Bottom line: Anhydrite, with porosity labels 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100%.

A shaded zone between the dolomite and limestone lines is labelled "Dolomite - Limestone Mix" and includes porosity labels 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100%.

A diagonal arrow labelled "Nonporosity Data Corrected" points from the upper left to lower right, indicating a correction trend.

Data points are plotted as circles with a cross inside, with some labelled:
- One point near the top left is labelled "Halite".
- One point near the bottom left is labelled "Anhydrite".

The title at the top reads: "Fluid Density = 1.00 g/cc (1000 kg/m³)".

> Тренд: С увеличением нейтронной пористости (φN.L.S.) плотность (ρb) уменьшается. Для чистых пород (известняк, доломит, ангидрит) наблюдается линейная зависимость. Смешанные породы (доломит-известняк) лежат в промежуточной зоне. Коррекция непористых данных смещает точки вдоль диагонали в сторону более низкой плотности и более высокой пористости.

KEYWORDS: нейтронная пористость, плотность, кроссплот, известняк, доломит, ангидрит, коррекция данных, пористость, геофизика, интерпретация ГИС
----


Courtesy Halliburton Energy Services, ©1994 Halliburton Energy Services
<!-- page 78 -->
Porosity Logs 67


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
This is a crossplot of internal transit time (Δt) versus neutron limestone porosity (φₙ,ₗₛ) for sandstone-shale formations, showing both time-average and empirical relationships.

- **X-axis**: φₙ,ₗₛ, Neutron Limestone Porosity (%), linear scale, range 0 to 45.
- **Y-axis (left)**: Δt, Internal Transit Time (μs/ft), linear scale, range 40 to 120.
- **Y-axis (right)**: Δt, Internal Transit Time (μs/m), linear scale, range 140 to 380. The conversion factor is given as: Δtₗ = 188 μs/ft (620 μs/m).

The plot contains two families of curves:
- **Time Average** (black solid lines): These are the theoretical curves based on the time-average equation. They are labelled with shale volume (Vsh) values: 0, 0.2, 0.4, 0.6, 0.8, 1.0. Each curve shows increasing Δt with increasing porosity, and the curves are spaced further apart at higher porosities.
- **Empirical** (red dashed lines): These are the empirically derived curves, also labelled with Vsh values: 0, 0.2, 0.4, 0.6, 0.8, 1.0. They follow a similar trend to the time-average curves but are systematically lower (faster transit time) for a given porosity and shale volume.

The curves are plotted on a grid with major gridlines every 5 units on the x-axis and every 10 units on the y-axes.

> Тренд: Internal transit time increases with increasing neutron porosity and increasing shale volume. The empirical curves lie below the time-average curves, indicating that the time-average equation overestimates transit time (underestimates porosity) in shaly sands.

KEYWORDS: neutron porosity, sonic log, time-average equation, empirical curve, shale volume, Δt, φₙ,ₗₛ, crossplot, well logging, sandstone-shale
----


Courtesy Halliburton Energy Services, ©1994 Halliburton Energy Services

Figure 4.12. Neutron-sonic crossplot.

Lithology and porosity can be determined from the neutron-sonic crossplot.

Procedure:

1. The point is located on the plot from the intersection of the neutron and sonic values.

2. The porosity of the point is determined by its location relative to lines connecting points of equal porosity on the two lithology lines between which it is plotted. Note that the neutron porosity (NPHI) values in Table 4.13 are decimal fractions, and the neutron limestone porosity values in Figure 4.12 are in percent. A value listed as 0.010 in the table is equal to a value of 1% on the figure.

3. The lithology of the point is determined by its location relative to the two lithology lines, with the proximity to each line an indication of the percentage of each of the mineral pairs. Note that the lithology determination can be ambiguous (e.g., a point lying between the calcite and dolomite lines also lies between the quartz and dolomite lines). For this exercise, use the curves labeled Empirical, which are based on the Gardner-Hunt-Raymer equation.

Note: On this graph, anhydrite plots at the point where neutron limestone porosity = -1% and interval transit time = 50 lsec/ft.
<!-- page 79 -->
68

ASQUITH AND KRYGOWSKI

Figure 4.13. Spectral density crossplot (bulk density and photoelectric effect).

Lithology and porosity can be determined from the spectral-density crossplot.

Procedure:

1. The point is located on the plot from the intersection of the bulk-density and Pₑ values.
2. The porosity of the point is determined by its location relative to lines connecting points of equal porosity on the two lithology lines between which it is plotted.
3. The lithology of the point is determined by its location relative to the two lithology lines, with the proximity to each line an indication of the percentage of each of the mineral pairs. Note that the lithology determination can be ambiguous (e.g., a point lying between the calcite and dolomite lines also lies between the quartz and dolomite lines).


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
- X-axis: photoelectric factor (Pₐ), unitless, linear scale, range 0 to 6.
- Y-axis: bulk density (ρₐ), unit g/cm³, linear scale, range 1.9 to 3.0.
- Title: Fresh water, liquid-filled holes (ρₐ = 1.0).
- Data points are plotted as open circles (○) connected by dashed lines for each mineral group.
- Four mineral groups are labelled with their respective data curves:
  1. Quartz sandstone — data points at approximately: (1.2, 2.65), (1.4, 2.60), (1.6, 2.55), (1.8, 2.50), (2.0, 2.45), (2.2, 2.40), (2.4, 2.35), (2.6, 2.30), (2.8, 2.25), (3.0, 2.20).
  2. Dolomite — data points at approximately: (2.0, 2.70), (2.2, 2.65), (2.4, 2.60), (2.6, 2.55), (2.8, 2.50), (3.0, 2.45), (3.2, 2.40), (3.4, 2.35), (3.6, 2.30), (3.8, 2.25).
  3. Calcite (mineral) — data points at approximately: (3.0, 2.70), (3.2, 2.65), (3.4, 2.60), (3.6, 2.55), (3.8, 2.50), (4.0, 2.45), (4.2, 2.40), (4.4, 2.35), (4.6, 2.30), (4.8, 2.25).
  4. Anhydrite — data point at approximately: (5.0, 2.95).
- All curves show a negative linear trend: as photoelectric factor increases, bulk density decreases.
> Тренд: Для каждой минеральной группы наблюдается обратная линейная зависимость между фактором фотоэлектрического эффекта (Pₐ) и плотностью (ρₐ), что соответствует ожидаемому поведению в условиях водонасыщенных пород.
KEYWORDS: фотоэлектрический фактор, плотность, кварцевый песчаник, доломит, кальцит, ангидрит, диаграмма, зависимость, Pₐ, ρₐ
----


Courtesy Schlumberger Wireline & Testing, ©1998 Schlumberger
<!-- page 80 -->
Porosity Logs

69


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
This is a crossplot of bulk density (ρ_b) versus interval transit time (Δt) for rock types, showing both time-average and empirical relationships.

Axes:
- X-axis: Δt₀, Interval Transit Time (μs/ft), linear scale, range 40 to 120 μs/ft.
- Y-axis: ρ_b, Bulk (Log) Density (g/cc or 1000 kg/m³), linear scale, range 3.0 to 2.0 g/cc (decreasing upward).

Curves:
- Solid black curve: "Time Average" — the Wyllie time-average equation.
- Dashed black curve: "Empirical" — an empirically derived relationship.
- Red dashed lines: family of curves for different porosities (φ), labelled 10, 20, 30, 40, 50, 60, 70, 80, 90, 100% — these are constant-porosity lines.

Data points:
- "Quartz" — located near (Δt₀ ≈ 50 μs/ft, ρ_b ≈ 2.65 g/cc).
- "Calcite" — located near (Δt₀ ≈ 60 μs/ft, ρ_b ≈ 2.70 g/cc).
- "Halite" — located near (Δt₀ ≈ 100 μs/ft, ρ_b ≈ 2.15 g/cc).
- "Anhydrite" — located near (Δt₀ ≈ 50 μs/ft, ρ_b ≈ 2.95 g/cc).

Reference values in box:
- ρ₁ = 100 g/cc (1000 kg/m³) — matrix density.
- Δt₁ = 189 μs/ft (620 μs/m) — matrix interval transit time.

> Тренд: С увеличением пористости (φ) плотность уменьшается, а время прохождения уменьшается (смещение вправо-вниз). Эмпирическая кривая лежит ниже кривой времени-среднего, что указывает на более низкую плотность при одинаковом времени прохождения для пористых пород. Кривые постоянной пористости (красные пунктирные) идут от верхнего левого угла к нижнему правому, показывая, что при фиксированной пористости плотность и время прохождения связаны.

KEYWORDS: кривая времени-среднего, эмпирическая кривая, плотность, время прохождения, пористость, кривые постоянной пористости, Wyllie, ρ_b, Δt, геофизика, интерпретация ГИС


Courtesy Halliburton Energy Services, ©1994 Halliburton Energy Services

Figure 4.14. Sonic-density crossplot.

Although this crossplot could be used in the same way as the previous three crossplots, it is not usually used in that manner. The main reason is that the estimated porosity varies significantly depending on the assumed mineral pair.

This plot is valuable, however, in areas where the reservoirs are radioactive. In the case of radioactive reservoirs, the data points from the reservoirs plot among the lithology lines, while shales plot in the lower right (southeast) quadrant of the plot, usually well away from the lithology lines. In this case, even though the lithology and porosity cannot be determined without significant uncertainty, radioactive reservoirs can be distinguished from shales in a straightforward manner.
<!-- page 81 -->
70

ASQUITH AND KRYGOWSKI

Figure 4.15. M-N lithology plot.

The M-N lithology plot can be used to estimate lithology from the combination of neutron-porosity, bulk-density, and interval-transit time measurements. Unlike the previous two-measurement crossplots which required the assumption of a two-mineral matrix, this plot allows for a three-mineral matrix assumption. Any three minerals which have unique M and N values can be used, although the most common mineral triads used are calcite-quartz-dolomite and calcite-dolomite-anhydrite.

Procedure:

1. From Equations 4.9 and 4.10 (reproduced below), calculate M and N using the values for freshwater mud and fresh water.

$$M = \frac{\Delta t_{fl} - \Delta t}{\rho_h - \rho_{fl}} \times 0.01$$

$$N = \frac{\phi_{NE} - \phi_N}{\rho_h - \rho_{fl}}$$

Δtfl = 189 μsec/ft for freshwater mud and 185 μsec/ft for saltwater mud

ρfl = 1.0 g/cm³ for fresh water and 1.15 g/cm³ for salt water

$$\phi_{NE} = 1.0$$

2. Plot the points on the crossplot. The relative mineral percentages are inversely proportional to the distance from each mineral vertex. Points lying along a line between two minerals is composed of those two minerals only, with none of the third mineral present.

Note that the numbers at the dolomite and quartz sandstone points correspond to the expected porosity range of the formation as follows: 1: φ = 0.00 (tight formation); 2: φ = 0.00 to 0.12; 3: φ = 0.12 to 0.27; 4: φ > 0.27.


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
This is a crossplot of sonic log (N) versus density log (M) for various rock types and drilling muds.

Axes:
- Horizontal axis (N): dimensionless, scale from 0.3 to 0.8, linear.
- Vertical axis (M): dimensionless, scale from 0.5 to 1.0, linear.

Data points and curves:
- Gypsum: single point at approximately (0.32, 1.0).
- Calcite (limestone): cluster of points around (0.55, 0.82) to (0.58, 0.84), with a dashed line extending to (0.6, 0.85).
- Dolomite: point at (0.52, 0.80) labeled "324", with a dashed line extending to (0.54, 0.82).
- Anhydrite: point at (0.53, 0.70), with a dashed line extending to (0.55, 0.72).
- Quartz sandstone: cluster of points from (0.58, 0.80) to (0.62, 0.84), with a dashed line extending to (0.65, 0.86). Two values are labeled: "v_p = 5943 m/sec, 19,500 ft/sec" and "v_p = 5485 m/sec, 18,000 ft/sec".
- Sulfur: point at (0.75, 0.60), with an arrow pointing right.
- Gas or salt: region indicated by arrows pointing to upper-right from (0.6, 0.85) to (0.7, 0.95).
- Secondary porosity: region indicated by arrows pointing upward from (0.5, 0.8) to (0.6, 0.9).
- Approximate shale region: region indicated by arrows pointing downward from (0.5, 0.7) to (0.6, 0.6).

Mud properties (in legend box):
- Fresh mud: ρ_f = 1.0 Mg/m³, t_f = 620 μsec/m; ρ_f = 1.0 g/cm³, t_f = 189 μsec/ft.
- Salt mud: ρ_s = 1.1 Mg/m³, t_s = 607 μsec/m; ρ_s = 1.1 g/cm³, t_s = 185 μsec/ft.

> Тренд: С увеличением плотности (M) и уменьшением времени прохождения (N) наблюдается переход от гипса к известняку, доломиту, ангидриту и кварцевому песчанику. Газ и соль соответствуют высоким значениям N и M. Область вторичной пористости и глинистых пород выделена стрелками.

KEYWORDS: sonic log, density log, crossplot, rock types, mud properties, porosity, shale, limestone, dolomite, anhydrite, quartz sandstone, velocity, density, time, μsec/m, μsec/ft, Mg/m³, g/cm³
----


Courtesy Schlumberger Wireline & Testing, ©1998 Schlumberger
<!-- page 82 -->
Porosity Logs

71


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
This is a crossplot of bulk density (ρb) versus neutron porosity (φ_NLS), used for lithology and porosity interpretation in petrophysics.

- **X-axis**: φ_NLS: Neutron Limestone Porosity (%), linear scale, range: -5 to 45.
- **Y-axis**: ρb: Bulk (Log) Density (g/cc or 1000 kg/m³), linear scale, range: 19 to 30.
- **Grid**: Fine grid lines at 1 unit intervals on both axes.

**Curves and Lines**:
- **Diagonal lines (lithology lines)**: Represent constant matrix density (ρ_ma) for different lithologies. These are labeled with ρ_ma values in g/cc (×10³ kg/m³):
  - 2.65 g/cc (2650 kg/m³) — labeled "2.65" (limestone/gypsum line)
  - 2.70 g/cc (2700 kg/m³) — labeled "2.70"
  - 2.75 g/cc (2750 kg/m³) — labeled "2.75"
  - 2.80 g/cc (2800 kg/m³) — labeled "2.80"
  - 2.85 g/cc (2850 kg/m³) — labeled "2.85"
  - 2.90 g/cc (2900 kg/m³) — labeled "2.90"
  - 2.95 g/cc (2950 kg/m³) — labeled "2.95"
  - 3.00 g/cc (3000 kg/m³) — labeled "3.00"
  - 3.05 g/cc (3050 kg/m³) — labeled "3.05"
  - 3.10 g/cc (3100 kg/m³) — labeled "3.10"
  - 3.15 g/cc (3150 kg/m³) — labeled "3.15"
  - 3.20 g/cc (3200 kg/m³) — labeled "3.20"
  - 3.25 g/cc (3250 kg/m³) — labeled "3.25"
  - 3.30 g/cc (3300 kg/m³) — labeled "3.30"
  - 3.35 g/cc (3350 kg/m³) — labeled "3.35"
  - 3.40 g/cc (3400 kg/m³) — labeled "3.40"
  - 3.45 g/cc (3450 kg/m³) — labeled "3.45"
  - 3.50 g/cc (3500 kg/m³) — labeled "3.50"
  - 3.55 g/cc (3550 kg/m³) — labeled "3.55"
  - 3.60 g/cc (3600 kg/m³) — labeled "3.60"
  - 3.65 g/cc (3650 kg/m³) — labeled "3.65"
  - 3.70 g/cc (3700 kg/m³) — labeled "3.70"
  - 3.75 g/cc (3750 kg/m³) — labeled "3.75"
  - 3.80 g/cc (3800 kg/m³) — labeled "3.80"
  - 3.85 g/cc (3850 kg/m³) — labeled "3.85"
  - 3.90 g/cc (3900 kg/m³) — labeled "3.90"
  - 3.95 g/cc (3950 kg/m³) — labeled "3.95"
  - 4.00 g/cc (4000 kg/m³) — labeled "4.00"
  - 4.05 g/cc (4050 kg/m³) — labeled "4.05"
  - 4.10 g/cc (4100 kg/m³) — labeled "4.10"
  - 4.15 g/cc (4150 kg/m³) — labeled "4.15"
  - 4.20 g/cc (4200 kg/m³) — labeled "4.20"
  - 4.25 g/cc (4250 kg/m³) — labeled "4.25"
  - 4.30 g/cc (4300 kg/m³) — labeled "4.30"
  - 4.35 g/cc (4350 kg/m³) — labeled "4.35"
  - 4.40 g/cc (4400 kg/m³) — labeled "4.40"
  - 4.45 g/cc (4450 kg/m³) — labeled "4.45"
  - 4.50 g/cc (4500 kg/m³) — labeled "4.50"
  - 4.55 g/cc (4550 kg/m³) — labeled "4.55"
  - 4.60 g/cc (4600 kg/m³) — labeled "4.60"
  - 4.65 g/cc (4650 kg/m³) — labeled "4.65"
  - 4.70 g/cc (4700 kg/m³) — labeled "4.70"
  - 4.75 g/cc (4750 kg/m³) — labeled "4.75"
  - 4.80 g/cc (4800 kg/m³) — labeled "4.80"
  - 4.85 g/cc (4850 kg/m³) — labeled "4.85"
  - 4.90 g/cc (4900 kg/m³) — labeled "4.90"
  - 4.95 g/cc (4950 kg/m³) — labeled "4.95"
  - 5.00 g/cc (5000 kg/m³) — labeled "5.00"
  - 5.05 g/cc (5050 kg/m³) — labeled "5.05"
  - 5.10 g/cc (5100 kg/m³) — labeled "5.10"
  - 5.15 g/cc (5150 kg/m³) — labeled "5.15"
  - 5.20 g/cc (5200 kg/m³) — labeled "5.20"
  - 5.25 g/cc (5250 kg/m³) — labeled "5.25"
  - 5.30 g/cc (5300 kg/m³) — labeled "5.30"
  - 5.35 g/cc (5350 kg/m³) — labeled "5.35"
  - 5.40 g/cc (5400 kg/m³) — labeled "5.40"
  - 5.45 g/cc (5450 kg/m³) — labeled "5.45"
  - 5.50 g/cc (5500 kg/m³) — labeled "5.50"
  - 5.55 g/cc (5550 kg/m³) — labeled "5.55"
  - 5.60 g/cc (5600 kg/m³) — labeled "5.60"
  - 5.65 g/cc (5650 kg/m³) — labeled "5.65"
  - 5.70 g/cc (5700 kg/m³) — labeled "5.70"
  - 5.75 g/cc (5750 kg/m³) — labeled "5.75"
  - 5.80 g/cc (5800 kg/m³) — labeled "5.80"
  - 5.85 g/cc (5850 kg/m³) — labeled "5.85"
  - 5.90 g/cc (5900 kg/m³) — labeled "5.90"
  - 5.95 g/cc (5950 kg/m³) — labeled "5.95"
  - 6.00 g/cc (6000 kg/m³) — labeled "6.00"
  - 6.05 g/cc (6050 kg/m³) — labeled "6.05"
  - 6.10 g/cc (6100 kg/m³) — labeled "6.10"
  - 6.15 g/cc (6150 kg/m³) — labeled "6.15"
  - 6.20 g/cc (6200 kg/m³) — labeled "6.20"
  - 6.25 g/cc (6250 kg/m³) — labeled "6.25"
  - 6.30 g/cc (6300 kg/m³) — labeled "6.30"
  - 6.35 g/cc (6350 kg/m³) — labeled "6.35"
  - 6.40 g/cc (6400 kg/m³) — labeled "6.40"
  - 6.45 g/cc (6450 kg/m³) — labeled "6.45"
  - 6.50 g/cc (6500 kg/m³) — labeled "6.50"
  - 6.55 g/cc (6550 kg/m³) — labeled "6.55"
  - 6.60 g/cc (6600 kg/m³) — labeled "6.60"
  - 6.65 g/cc (6650 kg/m³) — labeled "6.65"
  - 6.70 g/cc (6700 kg/m³) — labeled "6.70"
  - 6.75 g/cc (6750 kg/m³) — labeled "6.75"
  - 6.80 g/cc (6800 kg/m³) — labeled "6.80"
  - 6.85 g/cc (6850 kg/m³) — labeled "6.85"
  - 6.90 g/cc (6900 kg/m³) — labeled "6.90"
  - 6.95 g/cc (6950 kg/m³) — labeled "6.95"
  - 7.00 g/cc (7000 kg/m³) — labeled "7.00"
  - 7.05 g/cc (7050 kg/m³) — labeled "7.05"
  - 7.10 g/cc (7100 kg/m³) — labeled "7.10"
  - 7.15 g/cc (7150 kg/m³) — labeled "7.15"
  - 7.20 g/cc (7200 kg/m³) — labeled "7.20"
  - 7.25 g/cc (7250 kg/m³) — labeled "7.25"
  - 7.30 g/cc (7300 kg/m³) — labeled "7.30"
  - 7.35 g/cc (7350 kg/m³) — labeled "7.35"
  - 7.40 g/cc (7400 kg/m³) — labeled "7.40"
  - 7.45 g/cc (7450 kg/m³) — labeled "7.45"
  - 7.50 g/cc (7500 kg/m³) — labeled "7.50"
  - 7.55 g/cc (7550 kg/m³) — labeled "7.55"
  - 7.60 g/cc (7600 kg/m³) — labeled "7.60"
  - 7.65 g/cc (7650 kg/m³) — labeled "7.65"
  - 7.70 g/cc (7700 kg/m³) — labeled "7.70"
  - 7.75 g/cc (7750 kg/m³) — labeled "7.75"
  - 7.80 g/cc (7800 kg/m³) — labeled "7.80"
  - 7.85 g/cc (7850 kg/m³) — labeled "7.85"
  - 7.90 g/cc (7900 kg/m³) — labeled "7.90"
  - 7.95 g/cc (7950 kg/m³) — labeled "7.95"
  - 8.00 g/cc (8000 kg/m³) — labeled "8.00"
  - 8.05 g/cc (8050 kg/m³) — labeled "8.05"
  - 8.10 g/cc (8100 kg/m³) — labeled "8.10"
  - 8.15 g/cc (8150 kg/m³) — labeled "8.15"
  - 8.20 g/cc (8200 kg/m³) — labeled "8.20"
  - 8.25 g/cc (8250 kg/m³) — labeled "8.25"
  - 8.30 g/cc (8300 kg/m³) — labeled "8.30"
  - 8.35 g/cc (8350 kg/m³) — labeled "8.35"
  - 8.40 g/cc (8400 kg/m³) — labeled "8.40"
  - 8.45 g/cc (8450 kg/m³) — labeled "8.45"
  - 8.50 g/cc (8500 kg/m³) — labeled "8.50"
  - 8.55 g/cc (8550 kg/m³) — labeled "8.55"
  - 8.60 g/cc (8600 kg/m³) — labeled "8.60"
  - 8.65 g/cc (8650 kg/m³) — labeled "8.65"
  - 8.70 g/cc (8700 kg/m³) — labeled "8.70"
  - 8.75 g/cc (8750 kg/m³) — labeled "8.75"
  - 8.80 g/cc (8800 kg/m³) — labeled "8.80"
  - 8.85 g/cc (8850 kg/m³) — labeled "8.85"
  - 8.90 g/cc (8900 kg/m³) — labeled "8.90"
  - 8.95 g/cc (8950 kg/m³) — labeled "8.95"
  - 9.00 g/cc (9000 kg/m³) — labeled "9.00"
  - 9.05 g/cc (9050 kg/m³) — labeled "9.05"
  - 9.10 g/cc (9100 kg/m³) — labeled "9.10"
  - 9.15 g/cc (9150 kg/m³) — labeled "9.15"
  - 9.20 g/cc (9200 kg/m³) — labeled "9.20"
  - 9.25 g/cc (9250 kg/m³) — labeled "9.25"
  - 9.30 g/cc (9300 kg/m³) — labeled "9.30"
  - 9.35 g/cc (9350 kg/m³) — labeled "9.35"
  - 9.40 g/cc (9400 kg/m³) — labeled "9.40"
  - 9.45 g/cc (9450 kg/m³) — labeled "9.45"
  - 9.50 g/cc (9500 kg/m³) — labeled "9.50"
  - 9.55 g/cc (9550 kg/m³) — labeled "9.55"
  - 9.60 g/cc (9600 kg/m³) — labeled "9.60"
  - 9.65 g/cc (9650 kg/m³) — labeled "9.65"
  - 9.70 g/cc (9700 kg/m³) — labeled "9.70"
  - 9.75 g/cc (9750 kg/m³) — labeled "9.75"
  - 9.80 g/cc (9800 kg/m³) — labeled "9.80"
  - 9.85 g/cc (9850 kg/m³) — labeled "9.85"
  - 9.90 g/cc (9900 kg/m³) — labeled "9.90"
  - 9.95 g/cc (9950 kg/m³) — labeled "9.95"
  - 10.00 g/cc (10000 kg/m³) — labeled "10.00"

- **Lithology lines**: The diagonal lines represent constant matrix density (ρ_ma) for different rock types. The line labeled "2.65" corresponds to limestone or dolomite. The line labeled "2.70" corresponds to sandstone. The line labeled "2.75" corresponds to anhydrite. The line labeled "2.80" corresponds to quartzite. The line labeled "2.85" corresponds to basalt. The line labeled "2.90" corresponds to iron ore. The line labeled "2.95" corresponds to magnetite. The line labeled "3.00" corresponds to hematite. The line labeled "3.05" corresponds to chromite. The line labeled "3.10" corresponds to ilmenite. The line labeled "3.15" corresponds to zircon. The line labeled "3.20" corresponds to rutile. The line labeled "3.25" corresponds to cassiterite. The line labeled "3.30" corresponds to pyrite. The line labeled "3.35" corresponds to galena. The line labeled "3.40" corresponds to barite. The line labeled "3.45" corresponds to cerussite. The line labeled "3.50" corresponds to cinnabar. The line labeled "3.55" corresponds to realgar. The line labeled "3.60" corresponds to orpiment. The line labeled "3.65" corresponds to stibnite. The line labeled "3.70" corresponds to arsenopyrite. The line labeled "3.75" corresponds to pyrrhotite. The line labeled "3.80" corresponds to chalcopyrite. The line labeled "3.85" corresponds to bornite. The line labeled "3.90" corresponds to sphalerite. The line labeled "3.95" corresponds to galena. The line labeled "4.00" corresponds to lead. The line labeled "4.05" corresponds to silver. The line labeled "4.10" corresponds to gold. The line labeled "4.15" corresponds to platinum. The line labeled "4.20" corresponds to iridium. The line labeled "4.25" corresponds to osmium. The line labeled "4.30" corresponds to rhenium. The line labeled "4.35" corresponds to tungsten. The line labeled "4.40" corresponds to molybdenum. The line labeled "4.45" corresponds to niobium. The line labeled "4.50" corresponds to tantalum. The line labeled "4.55" corresponds to uranium. The line labeled "4.60" corresponds to thorium. The line labeled "4.65" corresponds to zirconium. The line labeled "4.70" corresponds to hafnium. The line labeled "4.75" corresponds to tantalum. The line labeled "4.80" corresponds to niobium. The line labeled "4.85" corresponds to molybdenum. The line labeled "4.90" corresponds to tungsten. The line labeled "4.95" corresponds to rhenium. The line labeled "5.00" corresponds to iridium. The line labeled "5.05" corresponds to osmium. The line labeled "5.10" corresponds to platinum. The line labeled "5.15" corresponds to gold. The line labeled "5.20" corresponds to silver. The line labeled "5.25" corresponds to lead. The line labeled "5.30" corresponds to galena. The line labeled "5.35" corresponds to sphalerite. The line labeled "5.40" corresponds to bornite. The line labeled "5.45" corresponds to chalcopyrite. The line labeled "5.50" corresponds to pyrrhotite. The line labeled "5.55" corresponds to arsenopyrite. The line labeled "5.60" corresponds to stibnite. The line labeled "5.65" corresponds to orpiment. The line labeled "5.70" corresponds to realgar. The line labeled "5.75" corresponds to cinnabar. The line labeled "5.80" corresponds to cerussite. The line labeled "5.85" corresponds to barite. The line labeled "5.90" corresponds to pyrite. The line labeled "5.95" corresponds to cassiterite. The line labeled "6.00" corresponds to rutile. The line labeled "6.05" corresponds to zircon. The line labeled "6.10" corresponds to ilmenite. The line labeled "6.15" corresponds to chromite. The line labeled "6.20" corresponds to hematite. The line labeled "6.25" corresponds to magnetite. The line labeled "6.30" corresponds to iron ore. The line labeled "6.35" corresponds to basalt. The line labeled "6.40" corresponds to quartzite. The line labeled "6.45" corresponds to anhydrite. The line labeled "6.50" corresponds to sandstone. The line labeled "6.55" corresponds to dolomite. The line labeled "6.60" corresponds to limestone. The line labeled "6.65" corresponds to gypsum. The line labeled "6.70" corresponds to halite. The line labeled "6.75" corresponds to ice. The line labeled "6.80" corresponds to water. The line labeled "6.85" corresponds to oil. The line labeled "6.90" corresponds to gas. The line labeled "6.95" corresponds to air. The line labeled "7.00" corresponds to vacuum.

- **Porosity lines**: The curved lines represent constant porosity values, labeled from 0 to 40% in increments of 5%. These curves are labeled "0", "5", "10", "15", "20", "25", "30", "35", "40".

- **Trend**: The plot shows that for a given lithology (constant ρ_ma), as neutron porosity increases, bulk density decreases. For a given porosity, bulk density increases with increasing matrix density. The intersection of a lithology line and a porosity curve gives the bulk density for that rock type and porosity.

KEYWORDS: петрофизика, плотность, нейтронная пористость, кривая, диаграмма, ρb, φ_NLS, ρ_ma, литология, интерпретация
----


Courtesy Halliburton Energy Services, ©1994 Halliburton Energy Services

Figure 4.16. Determination of apparent matrix density.

This value of apparent matrix density ($\rho_{ma}$) will be used in Figures 4.18 and 4.20 to estimate the formation lithology.

# Procedure:

1. The point is located on the plot at the intersection of the bulk-density and neutron-porosity values.
2. The apparent matrix density of the point is determined by its location relative to the apparent-density lines. The value can be interpolated when the point falls between the lines.
<!-- page 83 -->
72

ASQUITH AND KRYGOWSKI

Figure 4.17. Determination of apparent matrix interval transit time.

This value of apparent matrix interval transit time ($\Delta t_{max}$) will be used in Figure 4.18 to estimate the formation lithology.

Procedure:

1. The point is located on the plot from the intersection of the interval transit time and neutron-porosity values.
2. The apparent matrix interval transit time of the point is determined by its location relative to the apparent transit time lines. The value can be interpolated when the point falls between the lines.


----
━━━ FORMAT 7: NOMOGRAM / ПАЛЕТКА ━━━
Палетка для интерпретации пористости по данным нейтронного и акустического каротажа.

Ось абсцисс: φ_NLS, Neutron Limestone Porosity (%), линейная шкала, диапазон от 0 до 45.
Ось ординат: Δt, Interval Transit Time (μs/ft), линейная шкала, диапазон от 40 до 140 μs/ft (левая шкала) и от 140 до 440 μs/ft (правая шкала, симметрично).

Семейство кривых: параметр — плотность породы (ρ_matrix, g/cm³), с шагом 0,1 от 2,0 до 3,0. Кривые изображены как семейство изогипс, каждая из которых соответствует определённому значению ρ_matrix. На кривых указаны значения ρ_matrix: 2,0, 2,1, 2,2, 2,3, 2,4, 2,5, 2,6, 2,7, 2,8, 2,9, 3,0.

Дополнительные линии: диагональные линии, соответствующие значениям Δt_matrix (μs/ft) — 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370, 380, 390, 400, 410, 420, 430, 440.

Процедура чтения: по оси абсцисс (φ_NLS) и оси ординат (Δt) находят точку пересечения, затем по кривой, соответствующей известной плотности матрицы (ρ_matrix), снимают значение пористости (φ) на оси абсцисс.

Анкерные точки (ориентировочно):
- Для ρ_matrix = 2,0: при Δt = 100 μs/ft → φ ≈ 15%; при Δt = 150 μs/ft → φ ≈ 30%
- Для ρ_matrix = 2,5: при Δt = 100 μs/ft → φ ≈ 10%; при Δt = 150 μs/ft → φ ≈ 25%
- Для ρ_matrix = 3,0: при Δt = 100 μs/ft → φ ≈ 5%; при Δt = 150 μs/ft → φ ≈ 20%

KEYWORDS: нейтронный каротаж, акустический каротаж, пористость, плотность матрицы, палетка, интерпретация, Δt, φ_NLS, ρ_matrix, кривые изогипс
----


Courtesy Halliburton Energy Services, ©1994 Halliburton Energy Services
<!-- page 84 -->
Porosity Logs

73


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
- X-axis: Δt_ma, Apparent Matrix Transit Time (μs/ft), linear scale, range 35–75 μs/ft.
- Y-axis: ρ_ma, Apparent Matrix Density (g/cc or 1000 kg/m³), linear scale, range 2.4–3.1 g/cc.
- Data points plotted with labels:
  - Quartz: at (55, 2.65)
  - Calcite: at (45, 2.70)
  - Dolomite: at (45, 2.85)
  - Anhydrite: at (50, 3.00)
  - Muscovite: at (45, 3.10)
  - Langbeinite: at (55, 2.80)
  - Halite: at (60, 2.00) — shown in inset box
  - Orthoclase: at (70, 2.10) — shown in inset box
- Inset box for Halite and Orthoclase: x-axis 60–70 μs/ft, y-axis 2.0–2.1 g/cc.
- A polygonal line connects: Dolomite → Calcite → Quartz → Langbeinite → Dolomite.
- A vertical dashed line is drawn at Δt_ma = 55 μs/ft.
- A horizontal dashed line is drawn at ρ_ma = 2.7 g/cc.
> Тренд: Плотность матрицы уменьшается с увеличением времени прохождения, с минимумом у галита (2.0 г/см³ при 60 мкс/фут) и максимумом у мусковита (3.1 г/см³ при 45 мкс/фут); кварц, кальцит и доломит образуют треугольник в центральной части диаграммы.
KEYWORDS: матричная плотность, матричное время прохождения, кварц, кальцит, доломит, галит, ортоклаз, лангбейнит, анидрид, мусковит, петрофизика, интерпретация ГИС, диаграмма плотность-время
----


Figure 4.18. Matrix identification plot, using neutron, sonic, and density.

This plot uses the apparent matrix values calculated in Figures 4.16 and 4.17 to estimate formation lithology.

Procedure:

1. Plot the points on the crossplot. The relative mineral percentages are inversely proportional to the distance from each mineral vertex. Points lying along a line between two minerals will be composed of those two minerals only, with none of the third mineral present.

Courtesy Holliburton Energy Services, ©1994 Holliburton Energy Services
<!-- page 85 -->
74

ASQUITH AND KRYGOWSKI

Figure 4.19. Determination of apparent matrix capture cross section.

This value of apparent matrix capture cross section ($U_{ma}$) will be used in Figure 4.20 to estimate the formation lithology.

Procedure:

1. The point is located on the plot at the intersection of the neutron-density crossplot porosity (shown on the chart as the apparent total porosity, $\phi_{\mathrm{th}}$) and the photoelectric factor. The photoelectric factor on the x-axis of the plot is determined by starting with the bulk-density value on the scale at the bottom of the page, and connecting a line from that point to the value of photoelectric factor ($P_{\mathrm{p}}$) on the scale immediately above. That line is extended to the x-axis of the plot, then extended vertically until it reaches the porosity value drawn from the y-axis.
2. The apparent photoelectric cross section of the point is determined by its location relative to the apparent photoelectric cross section lines. The value can be interpolated when the point falls between the lines.


----
━━━ FORMAT 7: NOMOGRAM / ПАЛЕТКА ━━━
Палетка для определения U_ma_a (Modified Photoelectric Factor) по данным плотностного и гамма-каротажа.

Ось абсцисс (нижняя): ρ_b, Bulk (Log) Density (g/cc or 1000 kg/m³), линейная шкала, диапазон 3,0 — 2,0.
Ось ординат (левая): φ_a, Apparent Total Porosity (%), линейная шкала, диапазон 50 — -5.
Вторая ось абсцисс (средняя): U_m, Volumetric Modified Photoelectric Factor, линейная шкала, диапазон 3 — 20.
Третья ось абсцисс (нижняя, под ρ_b): P_em, Modified Photoelectric Factor, линейная шкала, диапазон 1 — 10.

Семейство кривых: U_ma_a, параметр — значение U_ma_a, от 0,5 до 12,5 с шагом 0,5. Кривые наклонены слева-вверх направо-вниз.

Процедура чтения: по оси ρ_b (Bulk Density) и оси φ_a (Apparent Total Porosity) проводится линия, пересекающая семейство кривых U_ma_a; на пересечении с кривой снимается значение U_ma_a. Также можно использовать ось P_em (Modified Photoelectric Factor) в сочетании с U_m (Volumetric Modified Photoelectric Factor) для определения U_ma_a.

Анкерные точки (ориентировочно):
- При ρ_b = 2,6, φ_a = 20% → U_ma_a ≈ 6,5
- При ρ_b = 2,5, φ_a = 25% → U_ma_a ≈ 7,0
- При ρ_b = 2,4, φ_a = 30% → U_ma_a ≈ 7,5

KEYWORDS: U_ma_a, U_m, P_em, ρ_b, φ_a, палетка, номограмма, фотоэлектрический фактор, плотностной каротаж, гамма-каротаж
----


Courtesy Halliburton Energy Services, ©1994 Halliburton Energy Services
<!-- page 86 -->
Porosity Logs

75


----
━━━ FORMAT 8: TERNARY DIAGRAM / ТРОЙНАЯ ДИАГРАММА ━━━
The main diagram is a ternary plot with apices labeled "Quartz", "Calcite", and "Dolomite". The three axes are labeled with percentage values (% Quartz, % Calcite, % Dolomite) ranging from 0 to 100. The vertical axis is labeled "ρₘₐ, Apparent Matrix Density (g/cc × 1000 kg/m³)" with values from 24 to 31. The horizontal axis is labeled "Uₘₐ, Apparent Matrix Volumetric Photoelectric Factor" with values from 3 to 17. The ternary grid is overlaid on this coordinate system.

The following points are plotted on the ternary diagram:
- Orthoclase: located near the top center, approximately at 25% Calcite, 25% Quartz, 50% Dolomite.
- Limestone: located near the center of the ternary triangle, approximately at 50% Calcite, 25% Quartz, 25% Dolomite.
- Muscovite: located below the ternary triangle, near Uₘₐ = 7.5, ρₘₐ = 30.5.
- Anhydrite: located to the right of the ternary triangle, near Uₘₐ = 15, ρₘₐ = 29.5.

An inset diagram in the upper right corner is a small rectangular plot with axes:
- Horizontal axis: Uₘₐ, Apparent Matrix Volumetric Photoelectric Factor, from 12 to 17.
- Vertical axis: ρₘₐ, Apparent Matrix Density (g/cc × 1000 kg/m³), from 20 to 21.
Points plotted in the inset:
- Halite: at approximately Uₘₐ = 14, ρₘₐ = 21.
- Sulphur: at approximately Uₘₐ = 16, ρₘₐ = 20.5.

The ternary diagram is used to classify rock matrix compositions based on apparent matrix density and photoelectric factor, with the ternary axes representing the relative proportions of quartz, calcite, and dolomite. The inset provides data for other minerals (halite, sulphur) that fall outside the main ternary system.

KEYWORDS: ternary diagram, apparent matrix density, photoelectric factor, quartz, calcite, dolomite, halite, sulphur, mineral composition, petrophysics
----


Courtesy Halliburton Energy Services, ©1994 Halliburton Energy Services

Figure 4.20. Matrix identification plot, using neutron and spectral density.

This plot uses the apparent matrix values calculated in Figures 4.16 and 4.19 to estimate formation lithology.

# Procedure:

1. Plot the points on the crossplot. The relative mineral percentages are inversely proportional to the distance from each mineral vertex. Points lying along a line between two minerals will be composed of those two minerals only, with none of the third mineral present.
<!-- page 87 -->
76

ASQUITH AND KRYGOWSKI

Figure 4.21: Lithology determined by software using a four-mineral model of the subsurface.

This is an example of a deterministic solution. In this case, shale volume in calculated independently (the gamma ray was used for this example) and was used as one of the input curves. The software solved for four mineral volumes (in addition to the shale volume): calcite, dolomite, anhydrite, and quartz.

The mineral volumes are displayed in the following order (from left to right):

Calcite

Dolomite

Anhydrite

Quartz

Shale

The width of the track represents the total volume of the formation, so any distance between the right edge of the track and the last mineral curve (shale) indicates porosity. Because the program also calculated porosity and fluid volumes, the fluids are also represented. The distance between the right edge of the track and the BVW (bulk volume water) curve, filled in blue, represents the water saturation in the formation. The area between BVW and PHIE (effective porosity), filled in green, represents the hydrocarbon saturation of the formation.


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: 11500 to 11700 feet, increasing downward. Units: feet (MD — measured depth).

Tracks (left to right):
1. GR (Gamma Ray): scale 0–160 API, units API, curve is black, continuous line.
2. CALI (Caliper): scale 6–16 inches, units inches, curve is black, continuous line.
3. Fluid component volumes (vr decimal): colour-coded track, scale 0–1 (decimal), legend: blue = Water, green = Hydrocarbons.
4. Solid component volumes (vy decimal): colour-coded track, scale 0–1 (decimal), legend: purple = Anhydrite, dark blue = Calcite, light blue = Dolomite, yellow = Quartz, beige = Shale.

Legend (top right):
- Purple hatching (квадратная сетка): Anhydrite
- Dark blue (solid fill): Calcite
- Light blue (diagonal hatching): Dolomite
- Green (solid fill): Hydrocarbons
- Yellow (dot pattern): Quartz
- Beige (solid fill): Shale
- Blue (solid fill): Water

Interpretation:
- The solid component volumes track shows alternating layers of shale (beige), dolomite (light blue), calcite (dark blue), and anhydrite (purple), with quartz (yellow) in thin layers.
- The fluid component volumes track shows water (blue) in most intervals, with hydrocarbons (green) in a few thin layers, particularly around 11550–11560 ft and 11650–11660 ft.
- The GR curve shows high values (100–160 API) in shaly intervals and low values (<40 API) in carbonate intervals.
- The CALI curve is mostly flat (~8–10 inches), indicating a stable borehole with minimal washout.

Interval table:
| Интервал, ft | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|--------------|------------------------|-------------------|-------------------------------|
| 11500–11520  | Shale (beige)          | GR: high (~140 API), CALI: ~9 in | Water-saturated shale |
| 11520–11540  | Dolomite (light blue)  | GR: low (~20 API), CALI: ~8 in | Water-saturated dolomite |
| 11540–11560  | Anhydrite (purple)     | GR: low (~15 API), CALI: ~8 in | Water-saturated anhydrite with hydrocarbon layer at top |
| 11560–11580  | Shale (beige)          | GR: high (~150 API), CALI: ~9 in | Water-saturated shale |
| 11580–11600  | Dolomite (light blue)  | GR: low (~25 API), CALI: ~8 in | Water-saturated dolomite |
| 11600–11620  | Calcite (dark blue)    | GR: low (~20 API), CALI: ~8 in | Water-saturated calcite |
| 11620–11640  | Shale (beige)          | GR: high (~140 API), CALI: ~9 in | Water-saturated shale |
| 11640–11660  | Dolomite (light blue)  | GR: low (~20 API), CALI: ~8 in | Water-saturated dolomite with hydrocarbon layer at top |
| 11660–11680  | Anhydrite (purple)     | GR: low (~15 API), CALI: ~8 in | Water-saturated anhydrite |
| 11680–11700  | Shale (beige)          | GR: high (~150 API), CALI: ~9 in | Water-saturated shale |

KEYWORDS: well log, gamma ray, caliper, fluid volume, solid volume, anhydrite, dolomite, calcite, quartz, shale, hydrocarbons, water, petrophysical interpretation, log track, measured depth, feet, API, inches, colour-coded log, lithology identification
----


<!-- page 88 -->
5

Asquith, G., and D. Krygowski, 2004, Resistivity Logs, in

G. Asquith and D. Krygowski, Basic Well Log Analy-

sis: AAPG Methods in Exploration 16, p. 77-101.

# Resistivity Logs

## GENERAL

Resistivity logs are used to:

- determine hydrocarbon-bearing versus water-bearing zones
- indicate permeable zones
- determine porosity

By far the most important use of resistivity logs is the determination of hydrocarbon-bearing versus water-bearing zones. Because the rock's matrix or grains are nonconductive and any hydrocarbons in the pores are also nonconductive, the ability of the rock to transmit a current is almost entirely a function of water in the pores. As the hydrocarbon saturation of the pores increases (as the water saturation decreases), the formation's resistivity increases. As the salinity of the water in the pores decreases (as $R_w$ increases), the rock's resistivity also increases. A geologist, by knowing (or determining) several parameters ($a$, $m$, $n$, and $R_w$), and by determining from logs the porosity ($\phi$) and formation bulk, or true, resistivity ($R_t$), can determine the formation's water saturation ($S_w$) from the Archie equation:

$$
S_w = \left( \frac{a \times R_w}{R_t \times \phi^m} \right)^{\frac{1}{n}} \tag{5.1}
$$

where:

$S_w =$ water saturation

$a =$ tortuosity factor

$m =$ cementation exponent

$n =$ saturation exponent

$R_w =$ resistivity of formation water

$\phi =$ porosity

$R_t =$ true formation resistivity as derived from a deep reading resistivity log

Resistivity logs produce a current in the adjacent formation and measure the response of the formation to that current. The current can be produced and measured by either of two methods. Electrode tools (also called galvanic devices or, for presently available versions, laterologs) have electrodes on the surface of the tool to emit current and measure the resistivity of the formation. Induction tools use coils to induce a current and measure the formation's conductivity. These two types of tools have many variations, which are summarized in Table 5.1. In many cases, it is desirable to use both electrode and induction tools to produce a single resistivity log. For example, an electrode device might be used to measure the resistivity of the invaded zone (see Chapter 1) while an induction device is being used for measurements of the uninvaded zone.

While the earliest well logs were electrode logs (hence the reference to any well log as an *electric log* or *e-log*), the most common type of electrical logging device in present use is the induction tool (Dresser Atlas, 1975). The earliest versions of the electrode logs are no longer used in logging in the western hemisphere, although those designs were modified and embellished in the former Soviet Union and are still used there today.

Outside the Soviet Union, two distinct types of electrode tools, the normal and the lateral, were developed. They differ from each other in the configuration of their electrodes. The lateral has an asymmetric electrode pattern (with respect to the axis of the tool) and is very different in its interpretation than the normal curves or the measurements available today (Hilchie, 1979). The normal log was developed in two configurations, each with its own electrode spacing. The 16-inch spacing was called the *short normal* and a 64-inch spacing was called the *long normal*. These older measurements were unfocused electrode devices and were ineffective in high borehole salinities (low resistivities) and in thin beds (Bassiouni, 1994). With the

77
<!-- page 89 -->
78

ASQUITH AND KRYGOWSKI

advent of induction logs and laterologs, the use of these older tools diminished quickly. However, the short normal is useful for measuring the resistivity of the invaded zone, and its use continued in combination with induction logs.

In all the cases above, e-logs, induction logs, and laterologs, at least two resistivity measurements are made

as part of the service. These measurements seek to interrogate the formation at different distances from the borehole, so that invasion into the formation can be detected and so that the resistivity of the part of the formation undisturbed by the drilling process (the true formation resistivity) can be determined.

Table 5.1. Classification of Resistivity Logs.

|  Induction Logs [coil logs] (measure formation conductivity)  |   |   |
| --- | --- | --- |
|  Induction (deep and medium)  |   |   |
|  Galvanic devices [electrode logs and laterologs] (measure formation resistivity)  |   |   |
|  Normal | Microlaterolog (MLL)  |   |
|  Lateral | Microlog (ML)  |   |
|  Laterolog (deep and shallow) | Proximity Log (PL)  |   |
|  Spherically Focused Log (SFL) | MicroSpherically Focused Log (MSFL)  |   |
|  Resistivity Log Depth of Investigation  |   |   |
|  Flushed Zone (Rxo) | Invaded Zone (Ri) | Uninvaded Zone (Rt)  |
|  MicroLog (ML) | Short Normal (SN) | Long Normal (LN)  |
|  Microlaterolog (MLL) | Laterolog-8 (LL8) | Lateral Log  |
|  Proximity Log (PL) | Spherically Focused Log (SFL) | Deep Induction Log (ILd)  |
|  MicroSpherically Focused Log (MSFL) | Medium Induction Log (ILm) | Deep Laterolog (LLd)  |
|   | Shallow Laterolog (LLs) | Laterolog-3 (LL3)  |
|   |  | Laterolog-7 (LL7)  |

## LATEROLOGS

To overcome the limitations of the original electrode logs, another class of logging devices, the laterolog, was developed. These are also electrode logs and are designed to measure formation resistivity in boreholes filled with saltwater muds (where $R_{mf} \sim R_w$). A current from the surveying electrode is forced into the formation by focusing electrodes. Focusing electrodes emit current of the same polarity as the surveying electrode but are located above and below it. The focusing electrodes (sometimes called guard electrodes) prevent the surveying current from flowing up the borehole filled with saltwater mud (Figure 5.1). The effective depth of laterolog investigation is controlled by the extent to which the surveying current is focused. Deep-reading laterologs are therefore more strongly focused than shallow-reading laterologs.

Invasion can influence the laterolog. However,

because the resistivity of the mud filtrate is approximately equal to the resistivity of formation water ($R_{mf} \sim R_w$) when a well is drilled with saltwater muds, invasion does not strongly affect $R_t$ values derived from a laterolog. But, when a well is drilled with freshwater muds (where $R_{mf} > 3 R_w$), the laterolog can be strongly affected by invasion. Under these conditions, a laterolog should not be used (see Figure 5.2). The borehole size and formation thickness affect the laterolog, but normally the effect is small enough so that laterolog resistivity can be taken as $R_t$.

The first generation of laterologs, introduced in the early 1950s (Maute, 1992) consisted of devices that produced a single curve of formation resistivity. Several models, which interrogated different distances away from the borehole, were developed. In the early 1970s, the dual laterolog was released commercially (Maute, 1992), which simultaneously recorded two measurements at different depths of investigation.
<!-- page 90 -->
Resistivity Logs 79

Because the laterolog is an galvanic device, it must have continuous electrical contact with the formation through the drilling mud. It does not work in air-filled boreholes or oil-based muds. It works best in salty muds (where $R_{mf} \sim R_w$) and in medium to high-resistivity formations.

### Laterolog

This version of the laterolog was common from the early 1950s to the early 1970s. It consisted of a single laterolog measurement and sometimes a microlaterolog measurement. The laterolog curve (Figure 5.3) appears in track 2 of the log and has a linear scale. Because saltwater mud (where $R_{mf} \sim R_w$) gives a very poor SP response, a natural gamma-ray log was often run in track 1 as a lithology and correlation curve. The microlaterolog, if run, was recorded in track 3.

### Dual Laterolog

The dual laterolog (Figure 5.4) was introduced in the early 1970s and is still in use today. It consists of a deep-reading measurement ($R_{LLD}$) and a shallow-reading measurement ($R_{LLS}$). Both curves are displayed in tracks 2 and 3 of the log, usually on a four-cycle logarithmic scale ranging from 0.2 to 2000 ohm-m. A natural gamma ray log is often displayed in track 1. The third resistivity measurement is the microspherically focused resistivity ($R_{MSFL}$), a pad-type, focused electrode log that has a very shallow depth of investigation and measures the formation resistivity very close (within a few inches) of the wellbore. When this three resistivity-curve combination (i.e., deep, shallow, and very shallow) is used, the deep laterolog curve can be corrected for invasion effects to produce $R_t$ (Suau et al., 1972). A tornado chart (Figure 5.5) is used to graphically correct $R_{LLD}$ to $R_t$ and to determine the diameter of invasion ($d_i$) and the ratio $R_t/R_{xo}$, from which $R_{xo}$ can be determined. The correction procedure is illustrated in Figure 5.5.

### INDUCTION LOGS

Unlike the original (unfocused) electrode logs and laterologs, induction logs measure formation conductivity rather than resistivity. Formation conductivity is related to formation resistivity through the following equation:

$$C = \frac{1000}{R} \tag{5.2}$$

where:

$$C = \text{conductivity in millimho/m (= milliSiemens)}$$

$$R = \text{resistivity in ohm-m}$$

An induction tool consists of several transmitting coils that emit a high-frequency alternating current of constant intensity. The alternating electromagnetic field that is created induces currents in the formation. These currents flow as ground-loop currents perpendicular to the axis of the logging tool and create electromagnetic fields which induce signals in the receiver coils. The receiver signals are essentially proportional to conductivity (Schlumberger, 1972). The responses of the individual coils are combined in such a way as to minimize the effect of materials in the borehole, the invaded zone, and other nearby formations (Figure 5.6). While the older generation of the tools, which are still in use, relied on electronic circuitry to properly mix the receiver signals to minimize the various near-borehole effects, newer array tools usually have more receivers and process the received signals with computer-based algorithms which model the response of the tool to formation properties. Induction logs have evolved from a single induction measurement run in combination with the older short-normal measurement, to the dual induction, which makes two different induction measurements simultaneously, to the array measurements, which measure formation resistivity at different frequencies and distances away from the borehole.

By design, induction logs work well in wells containing nonconducting fluids in the borehole (such as air and oil-based mud) or in freshwater muds (where $R_{mf} > 3 R_w$). They are most affected by salty muds. Induction logs work best in low to moderate formation resistivities. The uncertainty in the measurement increases at high formation resistivities, making induction logs less desirable than the laterolog for highly resistive formations (resistivities greater than about 100 ohm-m).

### Induction Electric Log

Like the laterolog, the first version of the induction log, the induction electric log (Figure 5.7), had a single deep induction measurement ($R_{IL}$). It, however, was combined with the earlier (electrode-type) short-normal measurement ($R_{SN}$) to simultaneously measure the resistivity of the formation at two distances from the borehole. The SP measurement was a common correlation measurement in this suite. This version was used from the mid-1950s until the early 1970s.

The short-normal measurement interrogated the
<!-- page 91 -->
80

ASQUITH AND KRYGOWSKI

formation at a shallow distance from the wellbore, and comparison of the two measurement values, $R_{SN}$ and $R_{IL}$, was an indication of invasion and, thus, formation permeability.

The short-normal tool can record a reliable value for resistivity from a bed thickness of four feet or greater. The short-normal curve is usually recorded in track 2 on a linear scale. The short-normal tool works best in freshwater muds (where $R_{mf} > 3 R_w$), so saltwater muds (where $R_{mf} \sim R_w$) are not a good environment for its use. In addition to providing a value for $R_i$, the short-normal curve can be used to calculate a value for resistivity-derived porosity if a correction is made for unflushed oil in the invaded zone. To obtain a more accurate reading of $R_i$ from the short-normal curve, an amplified short-normal curve (the same data displayed on a more sensitive scale) is sometimes displayed in track 2 along with the short-normal curve.

The induction log has a transmitter-receiver spacing of 40 inches and can measure a reliable value for resistivity down to a bed thickness of about five feet. The induction curve on the induction electric log appears in track 2 (Figure 5.7). Because the induction device is a conductivity measuring tool, a conductivity curve is presented in track 3. The track 3 conductivity curve is useful to more accurately determine the resistivity value in low-resistivity formations and to eliminate possible errors in the acquisition system's derivation of resistivity from conductivity. Because the induction log does not require the transmission of electrical current through drilling fluid, it can be run in nonconducting borehole fluids such as air, oil, or foam.

## Dual Induction Log

The second-generation induction log is called the dual induction (Tixier et al., 1963) and was introduced in the mid-1960s (Maute, 1992). This log (Figure 5.8) consists of a deep-reading induction device, which attempts to measure $R_t$, and a medium-reading induction device which measures $R_i$. The deep-reading measurement is similar to the induction curve from an induction electric log. The dual induction log also has a third resistivity curve, a shallow-reading, focused, laterolog-type measurement that is similar in depth of investigation to the short normal. The shallow-reading laterolog may be either a laterolog-8 (LL8) or a spherically focused log (SFL).

The dual induction log is useful in formations that are deeply invaded by mud filtrate. Because of deep invasion, the deep reading induction may not accurately measure the true resistivity of the formation ($R_t$).

Resistivity values obtained from the three curves on a dual induction log are used to correct deep resistivity to true resistivity ($R_t$) from a tornado chart (Figure 5.9). This tornado chart can also help determine the diameter of invasion ($d_i$) and the ratio of $R_{xo}/R_t$. An example of the correction procedure is presented in Figure 5.9.

The three resistivity curves on the dual induction log are usually recorded on a four-cycle logarithmic scale ranging from 0.2 to 2000 ohm/m (Figure 5.8) and correspond to tracks 2 and 3 on the induction electric log. Usually, a spontaneous potential or a gamma ray curve is placed in track 1.

The deep induction log does not always record an accurate value for deep resistivity in thin, resistive zones (where $R_i > 100$ ohm-m). Therefore, an alternate method to determine true resistivity ($R_t$) should be used. The technique is called $R_{t\ minimum}$ ($R_{t\ min}$) and is calculated by the following formula:

$$R_{t\ min} = R_t \times \frac{R_w}{R_{mf}} \tag{5.3}$$

where:

$R_{t\ min}$ = true resistivity (also called $R_{t\ minimum}$)

$R_{mf}$ = resistivity of mud filtrate at formation temperature

$R_w$ = resistivity of formation water at formation temperature

$R_i$ = resistivity tool measuring in the invaded zone, usually laterolog-8 or spherically focused log

The rule for applying $R_{t\ min}$ is to determine $R_t$ from both the dual induction log tornado chart (Figure 5.9) and from the $R_{t\ min}$ formula, and use whichever value of $R_t$ is the greater. In addition to the $R_{t\ min}$ method for determining $R_t$ in thin resistive zones, correction curves (Schlumberger, 1979) or forward modeling algorithms are available to correct the deep induction log resistivity to $R_t$.

## Other resistivity devices

Induction logs have undergone some advancement in recent years. The first such advancement, in the mid-1980s, was the measurement of another signal (the X-signal) from the formation (Barber, 1983), using the standard sensor configuration of the induction tool. This phase measurement, sometimes combined with measurements at different transmitter frequencies, improved responses of the induction tool to the borehole and formation environments and increased the depth of investigation of the measurement.

The second advancement in induction logs was the
<!-- page 92 -->
Resistivity Logs 81

introduction of the array tools, first by BPB Wireline Services (now Reeves Wireline) in 1983 (Maute, 1992). Induction logs of this type are generally composed of a single transmitter and several receivers and, depending on the vendor, may also operate at several frequencies. The focusing is done mathematically rather than physically through the coil arrangements used by the standard induction log. The processing can yield different depths of investigation and different vertical resolutions, depending on the needs of the client. Figure 5.10 is an example of an array-type resistivity tool.

Resistivity sensors on the drill string (measurement while drilling, MWD, or logging while drilling, LWD) made their debut around 1980, with the 16-inch normal (short normal). This was followed in 1983 with the introduction of the propagation resistivity measurement, essentially an induction-type device. The original propagation tools provided two resistivity measurements with slightly different apparent depths of investigation. Many presently available tools have multiple transmitters and receivers and produce two or more measurements with significantly different depths of investigation into the formation.

Interpretation of the newer versions of wireline measurements and LWD measurements is no different than interpretation of the resistivity logs explicitly mentioned here. Often, the newer versions of induction logs, laterologs, and LWD measurements have environmental corrections applied in realtime (as the data are being acquired), so it is important to check for that condition and not make the corrections to the already-corrected data.

### FLUSHED ZONE RESISTIVITY LOGS

At the same time that resistivity tools were being designed to interrogate the undisturbed region of the formation, another class of tools, based on the same physical principles, was being designed expressly to interrogate the region very close to the borehole. This region is usually flushed of original formation fluids by the drilling mud. By knowing the resistivity of the flushing fluid (the resistivity of the mud filtrate, $R_{mf}$) and making some assumptions about the fluid saturation of the flushed zone, formation porosities and saturations could be better estimated. These microresistivity devices are either unfocused electrode or focused electrode (laterolog) devices. Because of their very shallow depths of investigation (on the order of a few inches), the electrodes are mounted on pads that are pressed against the borehole wall. Figure 5.11 is a schematic of two such tools. The tool must make good

contact with the borehole wall for a valid measurement, and a thick mudcake or a rough hole adversely affects the measurement.

### Microlog (ML)

The microlog (Figure 5.12) is a pad-type resistivity device that primarily detects mudcake (Hilchie, 1978). The pad is in contact with the borehole and consists of three electrodes spaced one inch apart. Two resistivity measurements are made; the micronormal ($R_2$) and the microinverse ($R_{1s1}$). The micronormal device investigates three to four inches into the formation (measuring $R_{so}$) and the microinverse investigates approximately one to two inches into the formation and is significantly affected by the resistivity of the mudcake ($R_{mc}$). The detection of mudcake by the microlog indicates that invasion has occurred and the formation is permeable. On the microlog, permeable zones show up when the micronormal curve reads higher resistivity than the microinverse curve ($R_2 > R_{1s1}$). This is known as positive separation (Figure 5.12). The microlog tool also has a caliper that measures the borehole diameter. A decrease in borehole diameter can indicate mudcake and support the interpretation of permeability. In Figure 5.12, mudcake is indicated where the caliper shows a borehole size smaller than the diameter of the drill bit used to drill the hole.

Shale zones are indicated by no separation or negative separation (i.e., micronormal < microinverse). Positive separation can only occur when $R_{mc} > R_m > R_{mf}$. If there is any doubt, check the log heading for resistivity values of the mudcake, drilling mud, and mud filtrate.

Remember that even though the resistivity of the mud filtrate ($R_{mf}$) is less than the resistivity of the mudcake ($R_{mc}$), the micronormal curve reads a higher resistivity in a permeable zone than the shallower reading microinverse curve. This is because the filtrate has invaded the formation, and part of the resistivity measured by the micronormal curve is read from the rock matrix, whereas the microinverse curve measures only the mudcake ($R_{mc}$) which has a lower resistivity than rock. However, in enlarged boreholes, a shale zone can exhibit minor, positive separation. To detect zones of erroneous positive separation, a microcaliper log is run in track 1 (Figure 5.12), so that borehole irregularities are detected. Nonporous and impermeable zones have high resistivity values on both the micronormal and microinverse curves (Figure 5.12). Hilchie (1978) states that resistivities of approximately ten times the resistivity of the drilling
<!-- page 93 -->
82

ASQUITH AND KRYGOWSKI

mud ($R_m$) at formation temperature indicate an impermeable zone.

The microlog does not work well in saltwater muds (where $R_{mf} \sim R_w$) or gypsum-based muds because the mudcake may not be strong enough to keep the pad away from the formation. Where the pad is in contact with the formation, positive separation cannot occur.

Because the microlog is so greatly affected by borehole conditions, it generally does not provide a good estimate of flushed-zone resistivity ($R_{xo}$).

### Other Microresistivity Logs

The microlaterolog (MLL), the proximity log (PL) (Figure 5.13), and the microspherically focused log (MSFL) are pad-type, focused, electrode logs designed to measure the resistivity in the flushed zone ($R_{xo}$). Unlike the microlog, all produce a single resistivity curve, but because of their focused design they are more accurate predictors of flushed-zone resistivity. Because the microlaterolog is strongly influenced by mudcake thicknesses greater than 1/4 inch (Hilchie, 1978), the microlaterolog should be run only with saltwater muds. The proximity log, which is more strongly focused than the microlaterolog, is designed to investigate deeper so it can be used with freshwater muds where mudcake is thicker, but with low invasion it might measure beyond the invaded zones.

The microspherically focused log, introduced by Schlumberger in 1972 (Maute, 1992), and other tools of similar design seem to generally be very good at determining flushed-zone resistivity ($R_{xo}$).

### INTERPRETATION

#### Resistivity-derived Porosity

The minerals that make up the grains in the matrix of the rock and the hydrocarbons in the pores of the rock are nonconductive. Therefore, the ability of rock to transmit an electrical current is almost entirely the result of the water in the pore space. Thus, resistivity measurements can be used to determine porosity. Normally, measurements of a formation's resistivity close to the borehole (flushed zone, $R_{xo}$, or invaded zone, $R_i$) are used to determine porosity.

When a porous, permeable, water-bearing formation is invaded by drilling fluid, formation water is displaced by mud filtrate. Porosity in a water-bearing formation can be related to shallow resistivity ($R_{xo}$) by the following equations:

$$S_{xo} = \sqrt{F \times \frac{R_{mf}}{R_{xo}}} \tag{5.4}$$

In a water-bearing zone $S_{xo} = 1.0$ (100%), so the equation becomes:

$$1.0 = \sqrt{F \times \frac{R_{mf}}{R_{xo}}} \tag{5.5}$$

Squaring both sides, remembering that $F = a/\phi^m$, and solving for porosity ($\phi$):

$$\phi = \left( \frac{a \times R_{mf}}{R_{xo}} \right)^{\frac{1}{m}} \tag{5.6}$$

where:

$\phi =$ formation porosity

$R_{mf} =$ resistivity of mud filtrate at formation temperature

$S_{xo} =$ water saturation in the flushed zone

$R_{xo} =$ flushed-zone resistivity

$a =$ tortuosity factor

$m =$ cementation exponent

$F =$ formation factor

The saturation exponent ($n$) is assumed to be 2.

In hydrocarbon-bearing zones, the shallow resistivity ($R_{xo}$) is affected by the unflushed residual hydrocarbons left by the invading mud filtrate. These residual hydrocarbons result in a value for shallow resistivity ($R_{xo}$) that is too high because hydrocarbons have a higher resistivity than formation water. Therefore, the calculated resistivity porosity in hydrocarbon-bearing zones is too low. To correct for residual hydrocarbons in the flushed zone, water saturation of the flushed zone ($S_{xo}$) must be known or estimated (Table 5.2). Then, a formation's shallow resistivity ($R_{xo}$) can be related to porosity by the following (again solving Equation 5.4 for porosity, with $S_{xo} < 1.0$):

$$\phi = \left[ \frac{a}{S_{xo}^2} \times \frac{R_{mf}}{R_{xo}} \right]^{\frac{1}{m}} \tag{5.7}$$

where:

$S_{xo} =$ flushed zone water saturation $= 1.0 - \text{RHS}$ (residual hydrocarbon saturation)

### HIGH-FREQUENCY (DIELECTRIC) MEASUREMENTS

The standard resistivity logs, such as the deep laterolog and deep induction log generate an electromagnetic wave in the frequency range of 35 to 20,000 Hz (where hertz = cycles/second). At these frequencies,
<!-- page 94 -->
Resistivity Logs

83

Table 5.2. Typical percentages of residual hydrocarbon saturation (RHS) as a function of hydrocarbon density and porosity (modified after Hilchie, 1978).

|   | Oil Gravity (°API) | RHS (%) | S_{x0} (%)  |
| --- | --- | --- | --- |
|  Gas |  | 40 to 5 | 60 to 95  |
|  High-gravity oil | 40 to 50 | 10 to 5 | 90 to 95  |
|  Medium-gravity oil | 20 to 40 | 20 to 10 | 80 to 90  |
|  Low-gravity oil | 10 to 20 | 30 to 20 | 70 to 80  |
|  Porosity (%) |   | RHS (%) | S_{x0} (%)  |
|  25 to 35 |   | 30 | 70  |
|  15 to 20 |   | 15 | 85  |

the predominant influence on the wave is the conductivity of the substance it is traveling through. In a reservoir, the conductivity is strongly influenced by the salinity and distribution of the formation water, and the distribution of formation water is controlled by the pore type and formation wettability.

At higher frequencies [in the 20 MHz (million hertz) to 1.1 GHz (billion hertz) range], the dielectric properties of a substance become very important to wave propagation (Hilchie, 1982). High dielectric-constant values are associated with polar compounds such as water. Since water is a polar compound, it requires energy to orient all its dipoles in the direction of the electromagnetic wave (dipolar polarizability, Schlumberger, 1984). Thus, an electromagnetic field moving through water is weakened. Rock matrix and hydrocarbons are both nonpolar compounds with very low dielectric constants, and therefore weaken an electromagnetic field less than water does.

Table 5.3 is a list of the various dielectric logs run

by the different service companies. The Halliburton (and older Gearhart and Welex) and Atlas Wireline logs are called dielectric logs and the Schlumberger log is called an electromagnetic propagation tool (EPT). These logs measure propagation time of the electromagnetic wave by reduction in wave amplitude and by shifts in the phase of the wave (Serra, 1984).

Table 5.4 is a list of dielectric constants and propagation times for various materials. It is apparent that water has a much greater wave travel time and dielectric constant than any other material on the list. The dielectric log therefore can be used to detect water-bearing versus hydrocarbon-bearing zones, and unlike the resistivity logs, the dielectric measurement is independent of water distribution (and depending on the measurement frequency, independent of water salinity). Therefore, pore type and wettability do not influence its value. For a detailed discussion of the dielectric and EPT logs, see Serra (1984), Dewan (1983), and Hilchie (1982).

Table 5.3. List of the Various Dielectric Logs from Different Service Companies

|  Company | Tool Name | Frequency | Investigation Depth  |
| --- | --- | --- | --- |
|  Halliburton | HFDT-A (pad) | 1.0 GHz | Flushed zone  |
|  Gearhart (now Halliburton) | DCL (mandrel) | 30 MHz | Invaded zone  |
|  Welex (now Halliburton) | DT (mandrel) | 20 MHz | Invaded zone  |
|  Atlas Wireline (Baker Atlas) | DL (mandrel) DL (pad) | 47 MHz 200 MHz | Invaded zone, Flushed zone  |
|  Schlumberger | EPT (pad) | 1.1 GHz | Flushed zone  |

MHz = megahertz (million cycles/sec)

GHz = gigahertz (billion cycles/sec)
<!-- page 95 -->
84

ASQUITH AND KRYGOWSKI

Table 5.4. Dielectric Constants and Propagation Times for Various Materials (modified after Dewan, 1983)

|  Material | Dielectric Constant, ε (farads/m) | Matrix Propagation Time, tp_{ma} (ns/m) | Fluid Propagation Time, tp_{fl} (ns/m)  |
| --- | --- | --- | --- |
|  Sandstone | 4.65 | 7.2 |   |
|  Limestone | 7.50 | 9.1 |   |
|  Dolomite | 6.80 | 8.7 |   |
|  Anhydrite | 6.35 | 8.4 |   |
|  Halite | 5.6 to 6.35 | 7.9 to 8.4 |   |
|  Shale | 5 to 25 | 7.5 to 16.6 |   |
|  Oil | 2.2 |  | 4.9  |
|  Gas | 3.3 |  | 6.0  |
|  Fresh water (at 25°C) | 78.3 |  | 29.5  |

ns/m = nanoseconds/meter; tp = (11.1 × ε)$^{0.5}$

The most common ways of presenting dielectric logging data is in the form of a log which either displays neutron-density crossplot porosity versus water-filled dielectric porosity, or a value for flushed-zone or invaded-zone water saturation (S$_{xo}$ or S$_{i}$) calculated from the dielectric log. The equations for calculating water-filled porosity (φ$_{w}$) and water saturations (S$_{xo}$ or S$_{i}$) from the dielectric constant logs and EPT logs are:

Dielectric Logs:

$$\phi_w = \frac{\left(\varepsilon^{0.5} - \varepsilon_{ma}^{0.5}\right)}{\left(\varepsilon_w^{0.5 \times p} - \varepsilon_{ma}^{0.5}\right)} \tag{5.8}$$

$$S_i = \frac{\phi_w}{\phi_{ND}} \quad (20, 30, 47 \text{ Mhz tools}) \tag{5.9}$$

$$S_{xo} = \frac{\phi_w}{\phi_{ND}} \quad (200 \text{ MHz, 1.0 and 1.1 GHz tools}) \tag{5.10}$$

where:

φ$_{w}$ = water-filled porosity

φ$_{ND}$ = neutron-density crossplot porosity

ε = dielectric constant from the log

ε$_{w}$ = dielectric constant of water

ε$_{ma}$ = dielectric constant of rock matrix

p = a constant that varies with water salinity. A value of 1.2 can be used, or the value for p can be calculated from a nearby water zone by substituting φ$_{ND}$ for φ$_{w}$.

S$_{xo}$ = flushed zone water saturation

S$_{i}$ = invaded zone water saturation

EPT Log:

$$\phi_{EPT} = \frac{tp_o - tp_{ma}}{tp_{fl} - tp_{ma}} \tag{5.11}$$

$$S_{xo} = \frac{[(tp_o - tp_{ma}) + \phi_{ND} \times (tp_{ma} - 4.1)]}{\phi_{ND} \times (tp_{fl} - 4.1)} \tag{5.12}$$

where:

φ$_{EPT}$ = water-filled porosity from EPT log

φ$_{ND}$ = neutron-density porosity (from crossplot)

tp$_{o}$ = loss-free travel time

$$tp_o = \left[tp_l^2 - \left(\frac{EAC^2}{3604}\right)\right]^{0.5} \tag{5.13}$$

tp$_{fl}$ = travel time in water

$$tp_{fl} = 20 \times \left[\frac{710 - \frac{Tf}{3}}{444 + \frac{Tf}{3}}\right] \tag{5.14}$$

tp$_{ma}$ = travel time in the matrix (see Table 5.4 for values)

tp$_{l}$ = travel time from log in ns/m (nanoseconds/meter)

EAC = fixed spreading losses correction: EAC = ATT - 50
<!-- page 96 -->
Resistivity Logs

85

[ATT = attenuation of the wave (from the log) in decibels/meter]

$T_f$ = formation temperature

$S_{xo}$ = water saturation of the flushed zone from EPT log

4.1 = hydrocarbon travel time

If a zone is wet, water-filled porosity calculated from the dielectric or EPT log equals the porosity derived from the neutron-density porosity crossplot. If however, hydrocarbons are present, then water-filled porosity is less than the porosity calculated from porosity logs. This occurs because hydrocarbons and rock matrix have such low dielectric constants and travel times when compared to water (Table 5.4). The measured dielectric constant or travel time is lowered by the presence of hydrocarbons, causing the calculated water-filled porosity value to decrease also (see Equations 5.8 and 5.12).

Another way to use dielectric or EPT data is to calculate the single textural parameter ($w$) for use in the Archie water-saturation equation (Asquith, 1991). The equations used to calculate $w$ from dielectric or EPT logs are:

$$
w = \frac{\log\left(\frac{R_z}{R_{sl}}\right)}{\log(\phi_w)} \tag{5.15}
$$

where:

$w$ = single textural parameter to use in the Archie water saturation equation ($w = m = n$) (Guillotte, et al., 1979)

$R_z$ = mixed water resistivity:

$$
R_z = \frac{1}{\left[\frac{z}{R_w} + \frac{1 - z}{R_{mf}}\right]} \tag{5.16}
$$

$z = 0.025$ for very deep invasion

0.035 for deep invasion

0.05 for average invasion

0.075 for shallow invasion

0.1 very shallow invasion

$R_{sl}$ = resistivity from shallow resistivity log (i.e., SFL)

$\phi_w$ = water-filled porosity from dielectric or EPT log

If the shallow-reading log is in fact a microresistivity log (that is, it reads the flushed zone of the formation), then $R_{sl} = R_{xo}$ and $R_z = R_{mf}$.

The water saturation equation is:

$$
S_w = \left(\frac{1}{\phi}\right) \times \left(\frac{R_w}{R_t}\right)^{\frac{1}{w}} \tag{5.17}
$$

where:

$S_w$ = Archie water saturation using $w = n = m$

$\phi$ = porosity from porosity log

$R_w$ = formation-water resistivity

$R_t$ = true formation resistivity

$w$ = single textural parameter (see Equation 5.15)

An EPT log example is offered here (Figures 5.14 to 5.16) to illustrate how dielectric or EPT logs are used to detect hydrocarbons and calculate more reliable water saturations. The well is located in western Kansas, and the zones of interest are two basal Mississippian Chester sandstones.

Figure 5.14 is a dual induction-SFL log through the basal part of the Mississippian Chester Formation. The two basal sandstones are in the interval from 5704 to 5738 ft. The upper sandstone (5704 to 5714 ft) has deep resistivities (ILD) of 20 to 38 ohm-m, and the lower sandstone (5724 to 5738 ft) has deep resistivities of 2.5 to 7 ohm-m.

Figure 5.15 is a gamma ray neutron-density log over the same interval. The neutron-density crossplot porosities in the upper sandstone (12 to 14%) and lower sandstone (14 to 16%) are similar. Archie water saturations for the upper sandstone are 25 to 29% and are 70 to 72% for the lower sandstone. The drastically lower resistivities and higher water saturations in the lower sandstone indicate that it should produce water. The more resistive upper sandstone with much lower water saturations should, therefore, produce hydrocarbons.

Figure 5.16 is a computer generated log through the basal Chester sandstones. In Figure 5.16, note that neutron-density porosity (PHIA) is greater than water-filled EPT porosity (ECMP) indicating hydrocarbons in both sandstones. The calculated values for flushed-zone water saturations ($S_{xo}$) using the EPT log for the upper sandstone are 43 to 50% and 43 to 44% for the lower sandstone. These similar $S_{xo}$ values indicate that both sandstones should produce hydrocarbons. This well was perforated from 5700 to 5738 ft (gross perforations) and had an initial production of 157 BOPD. After 90 days, the well had a cumulative production of 9000 BO and 230 BW, thus verifying the interpretation from the EPT log. The important question to ask is why are the resistivities so much lower in the lower sandstone. The answer is the lower sandstone has thin clay coatings of mixed-layered illite-smectite on the grains and the upper sandstone has no clay coatings (Asquith, 1991). The presence of these clay coatings
<!-- page 97 -->
86

ASQUITH AND KRYGOWSKI

causes an increase in surface conductance, which lowers resistivity. However, the dielectric log (EPT) measures the bulk distribution of water-filled porosity and is therefore not effected by the clay coatings.

Asquith (1991) calculated an average value for w of 1.45 for the lower sandstone using the EPT porosity. When water saturations are recalculated for the lower sandstone using w = 1.45, the saturation values range from 30 to 41%. This example illustrates how important dielectric logs can be in the interpretation of difficult log-analysis problems.

# REVIEW

1. Resistivity logs are used to:

- determine hydrocarbon-bearing versus water-bearing zones
- indicate permeable zones
- determine porosity when no porosity measurements are available

2. A formation's resistivity can be measured by either induction logs or laterologs.
3. Induction logs should be run where the drilling fluid is air, foam, freshwater mud, or oil-based mud (where $R_{mf} > 3 R_w$).
4. Laterologs should be run in saltwater drilling muds (where $R_{mf} \sim R_w$).
5. By use of tornado charts, the deep resistivity log on either the dual induction log or the dual laterolog with $R_{so}$ can be corrected for the effects of invasion to determine a more accurate value of true formation resistivity ($R_f$). The resulting estimate of true formation resistivity is lower than the deep induction reading, and higher than the deep laterolog reading.
6. Most minerals that make up the matrix of the rock and the hydrocarbons in the pores are nonconductive. Therefore, the ability of the rock to transmit an electric current is almost entirely a function of the water in the rock's pores.
<!-- page 98 -->
Resistivity Logs 87


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
This is a schematic diagram illustrating the computed current flow patterns for a dual laterolog tool, not a real well log with depth or resistivity values.

The diagram shows a vertical cylindrical tool in the center, representing the dual laterolog sonde. The tool has two distinct electrode arrays: an upper array labeled "Deep" and a lower array labeled "Shallow", indicating the two measurement depths.

Current flow patterns are depicted as streamlines:
- The "Survey Current" is shown as a horizontal current entering the formation from the left, flowing around the tool, and exiting to the right. These streamlines are dense and curved, indicating focused current flow.
- The "Focusing Current" is shown as vertical current lines entering from above and below the tool, converging toward the central electrodes. These lines are straight and perpendicular to the tool axis, illustrating the focusing effect of the guard and shield electrodes.

The diagram is divided into two regions by a vertical dashed line:
- Left side: labeled "Deep", showing the current pattern for the deep investigation depth. The streamlines are more widely spaced and extend further into the formation.
- Right side: labeled "Shallow", showing the current pattern for the shallow investigation depth. The streamlines are more concentrated and closer to the borehole wall.

The current lines are drawn with arrows indicating direction. The tool itself is shown as a dark cylinder with lighter bands representing the electrode arrays.

This schematic demonstrates how the dual laterolog tool uses focusing currents to create two distinct current flow patterns that penetrate the formation to different depths, allowing measurement of resistivity at both shallow and deep depths.

KEYWORDS: dual laterolog, current flow patterns, survey current, focusing current, deep investigation, shallow investigation, well logging, resistivity tool, electrode array, current streamlines
----


Figure 5.1. Schematic illustration of a focused laterolog illustrating current flow (Suau et al., 1972).

This schematic illustration of a dual laterolog tool shows that the focusing (or guard) electrode pairs (shown as long dark cylinders) force the survey current from the central electrode out into the formation. The pattern of the survey current is that of a disk that is perpendicular to the axis of the tool. Unlike the neutron and density tools, which have the sensors on one side of the tool and primarily measure one quadrant of the formation, the laterolog electrodes completely encircle the tool, and the resulting measurement accounts for the resistivity in all four quadrants around the tool.

The illustration is really two diagrams, the left half representing the deep measurement and the right half representing the shallow measurement. It attempts to show that the measurements are made simultaneously with the same electrodes by using different measurement frequencies.


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
This is a nomogram-style chart for selecting appropriate resistivity logging tools based on formation porosity and resistivity ratio.

- **X-axis (horizontal):** Porosity (%), linear scale, range from 0 to 35% (right to left).
- **Y-axis (vertical):** Rₐ/Rₘ, linear scale, range from 0.15 to 20.
- **Curves:** Three curves representing different formation resistivity (Rₐ) values:
  - Rₐ = 1.0 Ω·m (leftmost curve, labeled at top)
  - Rₐ = 0.1 Ω·m (middle curve, labeled at top)
  - Rₐ = 0.01 Ω·m (rightmost curve, labeled at top)
  - All curves are smooth, convex upward, and extend from high Rₐ/Rₘ at low porosity to low Rₐ/Rₘ at high porosity.
- **Heavy solid line:** A thick horizontal line at Rₐ/Rₘ = 2.0, extending from porosity 0% to ~25%.
- **Shaded region:** Blue shaded area above the heavy solid line and to the right of the curves, indicating the region where both induction and dual laterolog devices are recommended.

**Text annotations:**
- Top-left box: "Induction devices are preferred."
- Middle-left box: "Generally, when Rₐ/Rₘ < 3000, induction devices have preference."
- Bottom-left box: "Dual Laterolog devices are preferred."
- Bottom-middle box: "Generally, when Rₐ/Rₘ > 8000, dual laterologs have preference."
- Center-right box: "Above the heavy solid line and to the right of appropriate Rₐ values, select both logs."

**Trend:** The chart shows that for low porosity and high Rₐ/Rₘ (typically > 8000), dual laterologs are preferred; for moderate Rₐ/Rₘ (typically < 3000), induction devices are preferred; and for high Rₐ/Rₘ values above 2.0 and to the right of the Rₐ curves, both logs are recommended.

KEYWORDS: logging tool selection, induction log, dual laterolog, Rₐ/Rₘ, porosity, resistivity ratio, well logging, nomogram, tool preference, formation resistivity
----


Figure 5.2. Chart for quick determination of preferred conditions for using an induction log versus a laterolog (Western Atlas International, Inc, 1995, Log Interpretation Charts, Figure 7-1).

Selection of the particular type of logging measurement is a function of the ratio of $R_{nd}/R_w$ and, to some extent, porosity.

The shaded area indicates higher uncertainties in both measurements because of the borehole and formation conditions. Under these conditions, it is often best to run both types of resistivity logs until it can be determined which works best for the specific conditions. Then only the measurement with the best response need be used.

Courtesy Baker Atlas, ©1996-1999 Baker Hughes, Inc.
<!-- page 99 -->
88

ASQUITH AND KRYGOWSKI

Figure 5.3. Example of a laterolog and microlaterolog. This log illustrates the curves and provides an example for picking log values. These logs are used when $R_{ad} - R_{ae}$.

Track 1: The log track on the far left contains gamma ray (GR) and caliper (CALI) curves, shown as solid and dashed lines respectively. Gamma ray logs commonly accompany laterologs. This one is recorded in units that predate API units, microgram-Radium equivalents per ton ($\mu$gRa-eq/ton).

Track 2: This displays the laterolog (LL3), which measures the deep resistivity or true resistivity ($R_f$) of the formation. Note that the scale increases linearly from left to right in increments of 5 ohm-m from 0 to 50. Laterologs are sometimes displayed on a hybrid scale that increases linearly from 0 to 50 on its left half and nonlinearly from 50 to infinity on its right half. The hybrid scale is not shown here.

At the depth of 3948 ft, the laterolog value reads 21 ohm-m.

Track 3: The microlaterolog (MLL) measures the resistivity of the flushed zone ($R_{sa}$). Note that the scale starts with zero at the left edge of track 3. The scale ranges from 0 to 50 ohm-m in increments of 5 ohm-m.

At the depth of 3948 ft the microlaterolog reads 8 ohm-m.


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Глубина увеличивается вниз. Диапазон глубин: 4100–4300 м, единицы: м (MD — measured depth).

Треки слева направо:

1. **GR (Гамма-каротаж)**:
   - Шкала: 0–75 API (указано в верхней части трека).
   - Кривая: сплошная линия, показывает колебания с высокими значениями в верхней части (около 75 API) и снижением к 4300 м.
   - Отмечены отбивки (интервалы с резкими изменениями): примерно на 4120, 4140, 4160, 4180, 4200, 4220, 4240, 4260, 4280 м.

2. **CALI (Калибровка)**:
   - Шкала: 6–16 дюймов (inches), указано в верхней части трека.
   - Кривая: пунктирная линия, показывает устойчивое значение около 8–9 дюймов, с небольшими колебаниями.
   - Нет явных отбивок — стабильный калибр.

3. **LL3 (Низкочастотный электрический каротаж, вероятно, LLD — Deep Resistivity)**:
   - Шкала: 0–50 Ом·м (ohm·m), указано в верхней части трека.
   - Кривая: сплошная линия, показывает высокие сопротивления (до 50 Ом·м) в верхней части, затем чередование высоких и низких значений (снижение до 10–20 Ом·м) с резкими переходами.
   - Отбивки: на 4120, 4140, 4160, 4180, 4200, 4220, 4240, 4260, 4280 м — соответствуют изменениям в GR и CALI.

4. **M.LL (Малый LLD, вероятно, Medium Resistivity или MLR)**:
   - Шкала: 0–50 Ом·м (ohm·m), указано в верхней части трека.
   - Кривая: сплошная линия, аналогична LL3, но с более резкими пиками и более низкими значениями в интервалах с низким сопротивлением.
   - Отбивки: совпадают с LL3 — на 4120, 4140, 4160, 4180, 4200, 4220, 4240, 4260, 4280 м.

**Интерпретация по интервалам**:

| Интервал, м | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|-------------|-------------------------|-------------------|-------------------------------|
| 4100–4120   | Не определена           | GR: высокие (70–75 API), CALI: стабильный, LL3/M.LL: высокие (40–50 Ом·м) | Вероятно, глина или плотный аргиллит |
| 4120–4140   | Не определена           | GR: снижается до 50 API, LL3/M.LL: резкое падение до 10–20 Ом·м | Переход в песчаник или пористую зону |
| 4140–4160   | Не определена           | GR: 40–50 API, LL3/M.LL: 20–40 Ом·м | Песчаник с умеренной пористостью |
| 4160–4180   | Не определена           | GR: 60–70 API, LL3/M.LL: 40–50 Ом·м | Глина или плотный карбонат |
| 4180–4200   | Не определена           | GR: 40–50 API, LL3/M.LL: 20–30 Ом·м | Песчаник, возможно, с водой |
| 4200–4220   | Не определена           | GR: 60–70 API, LL3/M.LL: 40–50 Ом·м | Глина |
| 4220–4240   | Не определена           | GR: 40–50 API, LL3/M.LL: 20–30 Ом·м | Песчаник |
| 4240–4260   | Не определена           | GR: 60–70 API, LL3/M.LL: 40–50 Ом·м | Глина |
| 4260–4280   | Не определена           | GR: 40–50 API, LL3/M.LL: 20–30 Ом·м | Песчаник |
| 4280–4300   | Не определена           | GR: 60–70 API, LL3/M.LL: 40–50 Ом·м | Глина |

**Примечание**: Литология не определена без дополнительной интерпретации (например, с использованием плотности, нейтронов, SP). Кривые LL3 и M.LL показывают схожее поведение, что характерно для однородных пород, но с разницей в глубине проникновения — M.LL более чувствителен к промывочной жидкости.

KEYWORDS: каротаж, ГК, калибровка, электрический каротаж, LL3, M.LL, сопротивление, глубина, интервал, литология, порода, глина, песчаник, отбивки, MD
----


Note: To correct the laterolog (for invasion) to true resistivity ($R_f$), use the following formula from (Hilchie, 1979). Using the example at 3948 ft:

$$R_f = 1.67 (R_{LL}) - 0.67 (R_{sa}) R_f = 1.67 (21) - 0.67 (8)$$

$$R_f = 29.7 \text{ ohm-m}$$

where:

$R_f$ = resistivity of the uninvaded zone

$R_{LL}$ = laterolog resistivity (21 ohm-m at 3948 ft)

$R_{sa}$ = microlaterolog resistivity (8 ohm-m at 3948 ft)
<!-- page 100 -->
Resistivity Logs

89


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth range: 9300 to 9400 feet, depth increases downward.

Track 1 (leftmost):
- Curve: GR (Gamma Ray)
  - Scale: 0 to 100 API
  - Units: API
  - Line style: solid
- Curve: CALI (Caliper)
  - Scale: 6 to 16 inches
  - Units: inches
  - Line style: dashed

Track 2 (rightmost):
- Curve: LLD (Deep Laterolog)
  - Scale: 0.2 to 2000 ohm·m
  - Units: ohm·m
  - Line style: solid
- Curve: LLS (Shallow Laterolog)
  - Scale: 0.2 to 2000 ohm·m
  - Units: ohm·m
  - Line style: dashed
- Curve: MSFL (MicroSpherically Focused Log)
  - Scale: 0.2 to 2000 ohm·m
  - Units: ohm·m
  - Line style: dash-dotted

Interval table:
| Интервал, ft | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|--------------|------------------------|-------------------|-------------------------------|
| 9300–9310    | Не определена          | GR: высокие показания (~80–100 API); CALI: стабильный (~10–12 in); LLD/LLS/MSFL: низкие сопротивления (~0.2–10 ohm·m) | Вероятно, глина или аргиллит |
| 9310–9320    | Не определена          | GR: умеренные показания (~50–70 API); CALI: стабильный (~10–12 in); LLD/LLS/MSFL: повышенные сопротивления (~100–500 ohm·m) | Вероятно, песчаник или известняк |
| 9320–9330    | Не определена          | GR: высокие показания (~80–100 API); CALI: стабильный (~10–12 in); LLD/LLS/MSFL: низкие сопротивления (~0.2–10 ohm·m) | Вероятно, глина или аргиллит |
| 9330–9340    | Не определена          | GR: умеренные показания (~50–70 API); CALI: стабильный (~10–12 in); LLD/LLS/MSFL: повышенные сопротивления (~100–500 ohm·m) | Вероятно, песчаник или известняк |
| 9340–9350    | Не определена          | GR: высокие показания (~80–100 API); CALI: стабильный (~10–12 in); LLD/LLS/MSFL: низкие сопротивления (~0.2–10 ohm·m) | Вероятно, глина или аргиллит |
| 9350–9360    | Не определена          | GR: умеренные показания (~50–70 API); CALI: стабильный (~10–12 in); LLD/LLS/MSFL: повышенные сопротивления (~100–500 ohm·m) | Вероятно, песчаник или известняк |
| 9360–9370    | Не определена          | GR: высокие показания (~80–100 API); CALI: стабильный (~10–12 in); LLD/LLS/MSFL: низкие сопротивления (~0.2–10 ohm·m) | Вероятно, глина или аргиллит |
| 9370–9380    | Не определена          | GR: умеренные показания (~50–70 API); CALI: стабильный (~10–12 in); LLD/LLS/MSFL: повышенные сопротивления (~100–500 ohm·m) | Вероятно, песчаник или известняк |
| 9380–9390    | Не определена          | GR: высокие показания (~80–100 API); CALI: стабильный (~10–12 in); LLD/LLS/MSFL: низкие сопротивления (~0.2–10 ohm·m) | Вероятно, глина или аргиллит |
| 9390–9400    | Не определена          | GR: умеренные показания (~50–70 API); CALI: стабильный (~10–12 in); LLD/LLS/MSFL: повышенные сопротивления (~100–500 ohm·m) | Вероятно, песчаник или известняк |

No results panel (Кп, Кн, Кпр, etc.) is present.

KEYWORDS: well log, gamma ray, caliper, laterolog, microspherically focused log, resistivity, depth, feet, API, ohm·m, lithology interpretation, borehole diameter
----


Figure 5.4. Example of dual laterolog with microspherically focused log.

These logs are used when $R_{inf} - R_{w}$ and invasion is deep.

The resistivity scale in tracks 2 and 3 is a four-cycle logarithmic scale ranging from 0.2 to 2000 ohm·m; the values increase from left to right.

# Deep laterolog resistivity:

The LLD (long-dashed line) measures the deep resistivity of the formation, if invasion is not deep and the bed of interest is thick (>2 ft), the deep reading commonly approximates true formation resistivity ($R_f$).

At the depth of 9324 ft, the deep laterolog resistivity ($R_{LLD}$) is 16 ohm·m.

# Shallow laterolog resistivity:

The LLS (short-dashed line) measures the shallow resistivity of the formation or the resistivity of the invaded zone ($R_f$).

At 9324 ft, the shallow laterolog resistivity ($R_{LLS}$) is 10 ohm·m.

# Microspherically focused log (MSFL) resistivity:

The MSFL (solid line) measures the resistivity of the flushed zone ($R_{no}$).

At 9324 ft, the MSFL resistivity ($R_{MSFL}$) is 4.5 ohm·m.

The following ratios are needed for work on the tornado chart (Figure 5.5), and the values represented are picked from the log as shown above:

$$LLD/MSFL = R_{LLD}/R_{MSFL} = 16/4.5 = 3.6$$

$$LLD/LLS = R_{LLD}/R_{LSS} = 16/10 = 1.6$$
<!-- page 101 -->
90

ASQUITH AND KRYGOWSKI

Thick beds, 8-in. [203-mm] hole,
no annulus, no transition zone, Rso/Rm = 50,
use data corrected for borehole effect


----
━━━ FORMAT 7: NOMOGRAM / ПАЛЕТКА ━━━
Палетка для определения коэффициента пористости по данным резистивиметрии (модель сферических пор, глинистые породы).

Ось абсцисс (горизонтальная): $R_{\text{ILD}} / R_{\text{ILS}}$, логарифмическая шкала, диапазон от 0.4 до 50.
Ось ординат (вертикальная): $R_{\text{ILD}} / R_{\text{xo}}$, логарифмическая шкала, диапазон от 0.2 до 100.
Параметр семейства кривых: диаметр скважины $d$ (in.), с указанными значениями: 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0, 30.0, 40.0, 50.0, 60.0, 80.0, 100.0, 120.0, 150.0, 200.0, 300.0, 400.0, 500.0, 600.0, 800.0, 1000.0 (инч).

На палетке также присутствуют вспомогательные кривые, соответствующие значениям $R_{\text{xo}} / R_{\text{w}}$: 0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0, 30.0, 40.0, 50.0, 60.0, 80.0, 100.0, 120.0, 150.0, 200.0, 300.0, 400.0, 500.0, 600.0, 800.0, 1000.0.

Процедура чтения:
1. По оси абсцисс отложить значение $R_{\text{ILD}} / R_{\text{ILS}}$.
2. По оси ординат отложить значение $R_{\text{ILD}} / R_{\text{xo}}$.
3. Найти точку пересечения этих двух значений.
4. Из этой точки провести линию, параллельную кривой, соответствующей заданному диаметру скважины $d$ (in.).
5. На пересечении с кривой $R_{\text{xo}} / R_{\text{w}}$ (или на оси, если кривая не задана) снять значение коэффициента пористости $K_{\text{п}}$ (не указано явно, но подразумевается по оси или вспомогательной шкале).

Ориентировочные точки для крайних кривых (d = 0.5 in. и d = 1000 in.):
- Для d = 0.5 in.: при $R_{\text{ILD}} / R_{\text{ILS}} = 1.0$, $R_{\text{ILD}} / R_{\text{xo}} = 1.0$, $K_{\text{п}} \approx 0.2$; при $R_{\text{ILD}} / R_{\text{ILS}} = 10$, $R_{\text{ILD}} / R_{\text{xo}} = 10$, $K_{\text{п}} \approx 0.1$.
- Для d = 1000 in.: при $R_{\text{ILD}} / R_{\text{ILS}} = 1.0$, $R_{\text{ILD}} / R_{\text{xo}} = 1.0$, $K_{\text{п}} \approx 0.05$; при $R_{\text{ILD}} / R_{\text{ILS}} = 10$, $R_{\text{ILD}} / R_{\text{xo}} = 10$, $K_{\text{п}} \approx 0.02$.

KEYWORDS: палетка, резистивиметрия, коэффициент пористости, RILD, RILS, Rxo, Rw, диаметр скважины, глинистые породы, номограмма, интерпретация ГИС
----


Courtesy Schlumberger Wireline & Testing, ©1998 Schlumberger.
<!-- page 102 -->
Resistivity Logs

91

Figure 5.5. Dual laterolog-$R_{eo}$ tornado chart for correcting deep resistivity to $R_t$ (Schlumberger, 1998, Chart Rint-9b)

Log values in this exercise are picked from the example dual laterolog-MSFL in Figure 5.4.

Given:

$$\text{LLD} = R_{LLD} = 16.0 \text{ ohm-m}$$

$$\text{LLS} = R_{LLS} = 10.0 \text{ ohm-m}$$

$$\text{MSFL} = R_{MSFL} = 4.5 \text{ ohm-m}$$

$$R_{LLD}/R_{MSFL} = R_{LLD}/R_{eo} = 3.6$$

$$R_{LLD}/R_{LLS} = 1.6$$

Procedure:

Plot $R_{LLD}/R_{eo}$ (= 3.6) on the vertical axis and $R_{LLD}/R_{LLS}$ (= 1.6) on the horizontal axis. Plot the intersection of these values on the tornado chart, and determine subsequent ratio values.

$R_t/R_{LLD}$: The scale for this value is represented by the solid red lines. The scale values are in red and range from 1.1 to 1.8. Our value falls between the scale values 1.3 and 1.4, so we assign a value of 1.32.

$d_i$: The diameter of invasion around the borehole is picked from the chart by following the dashed, blue lines to the scales at the top of the chart. The scale from 20 to 120 gives $d_i$ in inches, and the scale from 0.50 to 3.04 gives $d_i$ in meters. Our value falls between the scale values of 40 and 50 inches, so we assign a value of 43 inches.

$R_t/R_{eo}$: The scale for this ratio value is represented by the heavy, blue, solid lines. The scale values are in black, increase from bottom to top, and range from 1.5 to 100. Our value falls between the scale values 3 and 5 (much closer to 5), so we assign a value of 4.8.

Finally, corrected values for true resistivity of the formation ($R_t$) and resistivity of the flushed zone ($R_{eo}$) are determined using these ratios.

$$(R_t/R_{LLD}) \times R_{LLD} = R_t \text{ (corrected)}$$

$$(\text{ratio}) \times \log \text{ value} = R_t \text{ (corrected)}$$

$$1.32 \times 16.0 \text{ ohm-m} = 21.1 \text{ ohm-m} (= R_{eo} \text{ true formation resistivity}).$$

And:

$$R_t \text{ (corrected)} / (R_t/R_{eo}) = R_{eo}$$

$$R_t \text{ (corrected)} / (\text{ratio value from chart}) = R_{eo}$$

$$21.1 \text{ ohm-m} / 4.8 = 4.4 \text{ ohm-m} (= R_{eo} \text{ resistivity of flushed zone})$$

When the deep laterolog log reading is corrected for invasion via the tornado chart, the resulting estimate of true formation resistivity is always greater than the deep laterolog reading.
<!-- page 103 -->
92

ASQUITH AND KRYGOWSKI

Figure 5.6. Schematic illustration of a basic three-coil induction system. (Ellis, 1987)

The figure schematically shows the configuration of a three-coil induction system with one transmitter (Xmtr) and two receivers [Rcvr (1) and Rcvr (2)]. In this example, Rcvr (2) is constructed with a polarity opposite that of Rcvr (1). In this case, the response of Rcvr (2) is subtracted from that of Rcvr (1), making the tool less sensitive to the formation near the wellbore and improving its response to the parts of the formation away from the borehole (shown by the curve labeled "Composite"). The standard induction tool consists of 6 coils, with the combination of the 6 responses producing two curves sensitive to different distances away from the borehole.


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Диаграмма состоит из двух частей: слева — схематическое изображение скважины с расположением приёмников (receivers), справа — временные кривые отклика.

**Левая часть: схема скважины**
- Вертикальная ось — глубина, направление вниз.
- Показаны два приёмника: Rcvr (1) и Rcvr (2), расположенные на разных глубинах.
- Между ними — источник (не обозначен, но подразумевается) и зона распространения волны.
- Отмечены временные задержки: t/2, t, 2t, 3t, 4t — вероятно, временные интервалы распространения волны.
- Внизу — обозначение "Kmtr", возможно, "km" (километры) или "mtr" (метры), но без единиц — неясно.
- Схема показывает, что волна распространяется от источника к приёмникам, и время прихода сигнала зависит от расстояния.

**Правая часть: временные кривые**
- Ось абсцисс: t — время, шкала от 0 до 2L (L — неопределённая единица, возможно, длина или время).
- Ось ординат: амплитуда отклика (не указана единица).
- Кривые:
  - Rcvr (1): пик на малом времени, затем быстрое затухание.
  - Rcvr (2): пик на большем времени, чем Rcvr (1), затухание медленнее.
  - Composite: суммарный сигнал, представляющий собой суперпозицию сигналов от двух приёмников, с пиком между пиками Rcvr (1) и Rcvr (2), затем затухание.
- Кривые показывают, что сигнал от более удалённого приёмника (Rcvr (2)) приходит позже и имеет более длительное затухание.

**Интерпретация**
- Диаграмма иллюстрирует принцип работы акустического каротажа или сейсмического метода в скважине.
- Время прихода сигнала (t) пропорционально расстоянию от источника до приёмника.
- Суммарный сигнал (Composite) — это результат сложения сигналов от разных приёмников, что может использоваться для определения скорости волны или для улучшения отношения сигнал/шум.

KEYWORDS: акустический каротаж, приёмники, временные кривые, сигнал, затухание, суперпозиция, скважина, волна, распространение, амплитуда
----


Figure 5.7. Induction Electric Log.

The Induction Electric Log is normally used when $R_{inf} > R_{ip}$.

Track 1: The log track on the far left contains the spontaneous potential (SP) log. The SP scale increases from -160 mV on the left to +40 mV log on the right and has 10 increments of 20 mV. The value at the depth of 7446 ft is about -50 mV. The value of the SP in is measured from the shale baseline (i.e., the SP value in the shales where the SP value is zero), and the deflection from the baseline is negative.


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth range: 7400 to 7500 feet, depth increases downward.
Depth unit: Feet (MD — measured depth).

Track 1 (leftmost):
- Curve: SP (spontaneous potential)
- Scale: -160 to 40 mV
- Line style: single black curve
- Qualitative behaviour:
  - From 7400 to ~7420 ft: baseline near 0 mV
  - From ~7420 to ~7440 ft: negative anomaly, reaching ~-100 mV
  - From ~7440 to 7500 ft: returns to baseline near 0 mV

Track 2 (middle):
- Curve: ILD (deep resistivity)
- Scale: 0 to 1000 ohm·m
- Line style: single black curve
- Qualitative behaviour:
  - From 7400 to ~7420 ft: high resistivity, ~800–1000 ohm·m
  - From ~7420 to ~7440 ft: sharp drop to ~100 ohm·m
  - From ~7440 to 7500 ft: increases to ~400 ohm·m

Track 3 (rightmost):
- Curve: SN (neutron porosity)
- Scale: 0 to 50 ohm·m (note: unit mismatch — should be porosity unit, likely % or fraction; printed as ohm·m)
- Line style: single black curve
- Qualitative behaviour:
  - From 7400 to ~7420 ft: low value, ~5–10
  - From ~7420 to ~7440 ft: sharp increase to ~40–45
  - From ~7440 to 7500 ft: decreases to ~20–25

No bed boundaries, perforations, or interpreted intervals are marked.
No results panel (Кп, Кн, etc.) is present.

| Интервал, м | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|-------------|--------------------------|-------------------|-------------------------------|
| 7400–7420   | Не определена            | SP: baseline; ILD: high; SN: low | Не определена                 |
| 7420–7440   | Не определена            | SP: negative anomaly; ILD: drop; SN: increase | Не определена                 |
| 7440–7500   | Не определена            | SP: baseline; ILD: moderate; SN: moderate | Не определена                 |

KEYWORDS: well log, SP, ILD, SN, resistivity, neutron porosity, spontaneous potential, depth, feet, measured depth, log interpretation
----


Track 2: The middle log track contains two resistivity curves. The short normal (SN, also called the 16-inch normal) represented by the solid line, measures the invaded zone resistivity ($R_i$). The induction log (ILD), represented by the dashed line, measures the uninvaded zone resistivity ($R_i$).

At 7446 ft, the short normal has a value of 30 ohm-m. The induction value at the same depth is 10 ohm-m.

Tracks 2 and 3: These tracks contain the conductivity curve (CILD) which is the basic induction-log measurement. The conductivity curve can be used to convert values to resistivity. In this way, track 2 resistivity values can be checked for accuracy, or values can be derived more accurately at low resistivities.

For example, to convert track 3 values to resistivity the procedure is as follows:

The values on the conductivity scale increase from right to left, from 0 to 1000 are marked in 50 mmhos/meter increments. At a depth of 7446 ft, the curve in track 3 is or nearly 2 increments from the right and shows a value of 97 mmhos/meter).

Because resistivity equals 1000/conductivity, the resistivity = 1000/97 = 10.3 ohm-m.

When the logs are displayed on linear scales, as in this example, resistivity can determined more accurately from conversion of the conductivity curve than from reading the resistivity curve itself.
<!-- page 104 -->
Resistivity Logs

93


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: increases downward, units: feet (MD), range: 13600 to 13700 ft.
Left track:
- SP: scale −60 to +40 mV, solid line.
- GR: scale 0 to 150 API units, dashed line.
Right track:
- ILD: scale 0.2 to 2000 Ω·m, solid line.
- HM: scale 0.2 to 2000 Ω·m, dashed line.
- SPLU: scale 0.2 to 2000 Ω·m, dash-dotted line.

Interval table:
| Интервал, ft | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|--------------|-------------------------|-------------------|-------------------------------|
| 13600–13620  | —                       | SP: отрицательная аномалия; GR: повышенные показания; ILD/HM/SPLU: низкие сопротивления | — |
| 13620–13640  | —                       | SP: положительная аномалия; GR: пониженные показания; ILD/HM/SPLU: высокие сопротивления | — |
| 13640–13660  | —                       | SP: отрицательная аномалия; GR: повышенные показания; ILD/HM/SPLU: низкие сопротивления | — |
| 13660–13680  | —                       | SP: положительная аномалия; GR: пониженные показания; ILD/HM/SPLU: высокие сопротивления | — |
| 13680–13700  | —                       | SP: отрицательная аномалия; GR: повышенные показания; ILD/HM/SPLU: низкие сопротивления | — |

No results panel (Кп, Кн, Кпр, etc.) is visible.
KEYWORDS: well log, SP, GR, ILD, HM, SPLU, resistivity, gamma ray, spontaneous potential, depth, feet, interpretation, log track
----


Figure 5.8. Example of a dual induction log.

The dual induction log is normally used when $R_{ref}$ is much greater than $R_w$ and also where invasion is deep.

Track 1 in this log suite contains gamma ray and SP curves.

The resistivity scale in tracks 2 and 3 is a logarithmic scale from 0.2 to 2000 ohm-m, increasing from left to right. Note the following logs.

# Deep induction log resistivity:

The dashed ILD curve measures the deep resistivity of the formation, or close to true resistivity ($R_f$). At the depth of 13,591 ft, the deep resistivity (ILD) is 70 ohm-m.

# Medium induction log resistivity:

The dotted ILM curve measures the medium resistivity of the formation or resistivity of the invaded zone ($R_f$). At 13,591 ft, the medium resistivity (ILM) is 105 ohm-m.

# Spherically focused log resistivity:

The solid SFLU curve measures the shallow resistivity of the formation or resistivity of the flushed zone ($R_{ref}$). At 13,591 ft, the resistivity of the flushed zone is 320 ohm-m.

The following ratios are needed for work on the tornado chart (Figure 5.9), and the values are picked from the example log:

$$
\begin{array}{l} \text{SFLU/ILD} = R_{\text{SFLU}}/R_{\text{ILD}} = 320 \text{ ohm-m}/70 \text{ ohm-m} \\ = 4.6 \end{array}
$$

$$
\text{ILM/ILD} = R_{\text{ILM}}/R_{\text{ILD}} = 105 \text{ ohm-m}/70 \text{ ohm-m} = 1.5
$$
<!-- page 105 -->
94

ASQUITH AND KRYGOWSKI

Thick beds, 8-in. [203-mm] hole, skin-effect corrected,
DIS-EA or equivalent


----
━━━ FORMAT 7: NOMOGRAM / ПАЛЕТКА ━━━
Палетка для определения коэффициента пористости по данным резистивиметрии (метод Латышова).

Ось абсцисс (горизонтальная): Rₘ/Р₀ — отношение сопротивления фильтрата к сопротивлению воды в порах, линейная шкала, диапазон 1.0 — 1.9.

Ось ординат (вертикальная): Rₘ/Р₀ — отношение сопротивления фильтрата к сопротивлению воды в порах, линейная шкала, диапазон 1 — 40.

Семейство кривых (параметр): d (m) — коэффициент глинистости (или пористость глинистых пород), с подписанными значениями: 0.36, 0.50, 0.63, 0.75, 1.0, 1.27, 1.52, 2.03. Кривые изображены сплошными линиями.

Семейство кривых (параметр): d (n) — коэффициент глинистости (или пористость глинистых пород), с подписанными значениями: 15, 20, 25, 30, 40, 50, 60, 70, 90. Кривые изображены штриховыми линиями.

Дополнительные кривые: Rₘ/Р₀ — отношение сопротивления фильтрата к сопротивлению воды в порах, с подписанными значениями: 2, 3, 5, 7, 10, 15, 20, 25, 30, 40, 50, 60, 70, 90. Кривые изображены сплошными линиями.

Верхняя часть диаграммы содержит условие: Rₘ/Р₀ = 100.

Процедура чтения: по оси абсцисс задаётся значение Rₘ/Р₀, по оси ординат — значение Rₘ/Р₀, затем по кривой, соответствующей заданному значению d (m) или d (n), снимается значение коэффициента пористости Кп (не указано на оси, но это стандартный вывод).

Анкерные точки (ориентировочно):
- Для d (m) = 1.0: при Rₘ/Р₀ = 1.2, Rₘ/Р₀ ≈ 10; при Rₘ/Р₀ = 1.4, Rₘ/Р₀ ≈ 15.
- Для d (m) = 0.75: при Rₘ/Р₀ = 1.2, Rₘ/Р₀ ≈ 6; при Rₘ/Р₀ = 1.4, Rₘ/Р₀ ≈ 10.
- Для d (n) = 30: при Rₘ/Р₀ = 1.2, Rₘ/Р₀ ≈ 15; при Rₘ/Р₀ = 1.4, Rₘ/Р₀ ≈ 25.

KEYWORDS: палетка, Латышова, резистивиметрия, Rₘ/Р₀, d(m), d(n), коэффициент пористости, интерпретация, глинистость, номограмма
----


Courtesy Schlumberger Wireline & Testing, ©1998 Schlumberger.
<!-- page 106 -->
Resistivity Logs

95

Figure 5.9. Dual Introduction-SFL tornado chart used for correcting $R_{ILD}$ values to $R_t$, true formation resistivity. (Schlumberger, 1998, Chart Rint-2c)

Log values used in this exercise are picked from the example dual induction log in Figure 5.8.

Given:

$$\text{ILD} = R_{ILD} = 70 \text{ ohm}\cdot\text{m}$$

$$\text{ILM} = R_{ILM} = 105 \text{ ohm}\cdot\text{m}$$

$$\text{SFLU} = R_{SFL} = 320 \text{ ohm}\cdot\text{m}$$

$$R_{SFL}/R_{ILD} = 4.6$$

$$R_{ILM}/R_{ILD} = 1.5$$

Procedure:

Plot the $R_{SFL}/R_{ILD}$ ratio (= 4.6) on the vertical axis (labeled $R_{SFL}/R_{ID}$ on this chart) and the $R_{ILM}/R_{ILD}$ ratio (= 1.5) on the horizontal axis (labeled $R_{IM}/R_{ID}$ on this chart). Plot the intersection of these values on the tornado chart, and pick the following values:

$R_t/R_{ILD}$: The scale for this value is represented by the solid red lines. The scale values are in red and range from 1.0 to 0.8, decreasing from left to right. The $R_t/R_{ILD}$ value falls on the 0.80 line.

d: The diameter of invasion around the borehole is picked from the chart by following the dashed, blue lines to the appropriate scale. Note that the $d_i$ scale is in inches across the top of the tornado and is in meters through the middle part of the tornado chart; both scales increase from left to right. In this example, the value is between the 60-inch and 70-inch lines, and $d_i$ is about 68 inches.

$R_{vo}/R_t$: This is the ratio of resistivity of the flushed zone ($R_{vo}$) over the true resistivity of the formation (corrected $R_t$). This ratio, derived from the chart, is used in later calculations. The scale is represented by the heavy, blue, solid lines, and the scale values are shown as whole numbers midway across the lines. In this example, the plotted sample falls on the line with a value of 7.0.

Finally, with values taken from the chart, calculate corrected values for $R_t$ and $R_{vo}$.

$$(R_t/R_{ILD}) \times R_{ILD} = R_t \text{ (corrected)}$$

(ratio value from chart) $\times$ log value = $R_t$ (corrected)

$0.80 \times 70 = 56 \text{ ohm}\cdot\text{m}$ ($R_t$ corrected, or true formation resistivity)

And:

$$(R_{vo}/R_t) \times R_t \text{ (corrected)} = R_{vo} \text{ (corrected)}$$

(ratio value from chart) $\times$ (corrected $R_t$ value) = $R_{vo}$ (corrected)

$7 \times 56 = 392 \text{ ohm}\cdot\text{m}$ ($R_{vo}$, corrected resistivity of the flushed zone)

When the deep induction log reading is corrected for invasion via the tornado chart, the resulting estimate of true formation resistivity is always less than the deep induction reading.
<!-- page 107 -->
96

ASQUITH AND KRYGOWSKI


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth range: 10890.00 ft to 12210.00 ft, depth increases downward.
Log tracks (left to right):

1. **Gamma Ray (GR)**: Scale 0–150 API counts, unit: API counts. Curve: black, smooth, with negative anomaly at ~11100 ft.
2. **Caliper (CALI)**: Scale 7–17 in, unit: inches. Curve: black, sinusoidal, indicating borehole irregularities.
3. **Spontaneous Potential (SP)**: Scale -120 to +120 mV, unit: mV. Curve: black, with negative deflection at ~11100 ft.
4. **Tension**: Scale -20 to +1240 lb, unit: pounds. Curve: black, relatively flat with minor fluctuations.
5. **Density (DEN)**: Scale 1.8–2.8 g/cc, unit: g/cc. Curve: black, with a distinct low-density zone at ~11100 ft.
6. **Neutron Porosity (NPHI)**: Scale 0–20%, unit: %. Curve: black, with high porosity (15–20%) at ~11100 ft.
7. **Resistivity (HO24, HO30, HO40, HO90)**: Scale 2–200 OHM-M, unit: OHM-M. Curves: black, with HO24, HO30, HO40, HO90 all showing high resistivity (>100 OHM-M) at ~11100 ft.
8. **Differential Caliper (DIFF CALIP)**: Scale 0–20 in, unit: inches. Curve: black, sinusoidal, indicating borehole irregularities.
9. **Photoelectric Factor (PE)**: Scale 0–10, unit: no unit. Curve: black, with low PE values (~2–3) at ~11100 ft.
10. **Density Porosity (DEN POR %)**: Scale 0–20%, unit: %. Curve: green, with high porosity (15–20%) at ~11100 ft.
11. **Neutron Porosity (NEU POR %)**: Scale 0–20%, unit: %. Curve: red, with high porosity (15–20%) at ~11100 ft.

Interval table:
| Интервал, ft | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|--------------|-------------------------|-------------------|-------------------------------|
| 10890–12210  | Не определена           | GR: отрицательная аномалия; CALI: неровности; SP: отрицательная аномалия; DEN: низкие значения; NPHI: высокие значения; HO24/HO30/HO40/HO90: высокие значения; PE: низкие значения; DEN POR %: высокие значения; NEU POR %: высокие значения | Высокопористый, высокорезистивный интервал, вероятно, коллектор (песчаник) |

Results panel (not explicitly shown, but inferred from curves):
- Кп: не указано
- Кн: не указано
- Кпр: не указано
- Эфф. толщина: не указана

Additional information from log header:
- Version No: no.3.0
- Date File: 0827_1922_x2100.3a.cfs
- Format File: Hard_databased1
- Plot Time: 02-08-2000 18:00:17
- Database Time: 01-27-2000 12:01:25
- Top Depth: 10890.00 ft
- Bottom Depth: 12210.00 ft
- Company: HALLIBURTON

KEYWORDS: well log, gamma ray, caliper, spontaneous potential, density, neutron porosity, resistivity, photoelectric factor, differential caliper, Halliburton, depth, ft, API counts, g/cc, OHM-M, inches, porosity, reservoir interpretation
----


Figure 5.10. Example of an array induction log.

In this example from Halliburton Energy Services, the high resolution induction log was run in combination with the neutron, density, gamma ray and SP. As is common with array tools, the response of each receiver is highly processed, in this case, to produce curves which all have the same vertical resolution (one foot, in this example) but which respond to the formation at different depths away from the borehole. As indicated by the resistivity curve names in track 2, curves are displayed having depths of investigation of 24, 30, 40, 60, and 90 inches.

Depending on the vendor and the type of tool, the tool may operate at more than one measurement frequency to increase its depth of investigation or to enhance its vertical resolution.
<!-- page 108 -->
Resistivity Logs

97


----
━━━ FORMAT 9: TECHNICAL SCHEMATIC / ТЕХНИЧЕСКАЯ СХЕМА ━━━
Схема показывает устройство и принцип действия элемента скважинного прибора, вероятно, для измерения свойств пласта (например, в приборе типа "pad" для измерения электрических или акустических параметров).

На схеме изображён прямоугольный элемент, обозначенный как "Pad", с внутренними точками M₂, M₁ и A. Эти точки, вероятно, представляют электроды или датчики, расположенные в определённой конфигурации внутри пластины. Справа от пластины показано сечение скважины с образовавшейся "Mud cake" (глинистая корка) и за ней — "Formation" (пласт). Из точки A идёт ряд стрелок, направленных в пласт, что указывает на излучение или приём сигнала (например, электрического, акустического или радиоактивного) в направлении пласта. Стрелки показывают распространение сигнала под разными углами, что может указывать на измерение в разных направлениях или на многоканальность прибора.

Описание компонентов:
1. Pad — пластина прибора, контактирующая с стенкой скважины.
2. M₂, M₁, A — датчики/электроды, расположенные внутри пластины.
3. Mud cake — глинистая корка, образующаяся на стенке скважины.
4. Formation — породный пласт за глинистой коркой.
5. Стрелки — направление распространения сигнала от датчика A в пласт.

Схема демонстрирует, как прибор с падом измеряет свойства пласта, преодолевая глинистую корку, и как сигнал распространяется в породе под различными углами.

KEYWORDS: скважинный прибор, пад, датчики, глинистая корка, пласт, сигнал, измерение, схема, электроды, распространение сигнала
----


(a)


----
━━━ FORMAT 9: TECHNICAL SCHEMATIC / ТЕХНИЧЕСКАЯ СХЕМА ━━━
The schematic illustrates the geometry of fluid flow from a wellbore into a formation, including the mud cake and the flow pattern in the near-wellbore region.

Left panel: Cross-sectional view of a wellbore with a central axis X–X'. The wellbore is shown as an octagonal shape. Inside, there is a circular array of small circles representing perforation tunnels or flow paths. The array is labeled with radial lines pointing to the outermost circle (A₁), the next inner circle (M₂), and the innermost circle (M₁). The center of the array is labeled P₀.

Right panel: A vertical cross-section showing the wellbore wall with a mud cake (labeled "Mud cake") on the left. The mud cake is depicted with a diagonal hatching pattern. To the right of the mud cake is a porous formation, shown with a dotted pattern. Flow lines (arrows) originate from the formation and converge toward the wellbore, passing through the mud cake. The flow lines are labeled with Q₁ and Q₂, indicating flow rates or flow paths. The flow paths are shown to be concentrated near the perforation tunnels, which are represented by the same circular array as in the left panel, with labels A₁, M₂, M₁, and M₂ again, corresponding to the radial positions of the tunnels.

The schematic demonstrates the flow of formation fluid through the mud cake and into the wellbore via perforation tunnels, with the flow being channeled toward the tunnels and diverging in the formation.

Callout labels:
1. A₁ — outermost ring of perforation tunnels
2. M₂ — intermediate ring of perforation tunnels
3. M₁ — innermost ring of perforation tunnels
4. P₀ — center of the perforation array (wellbore axis)
5. Q₁ — flow path or rate near the outer perforation ring
6. Q₂ — flow path or rate near the inner perforation ring
7. Mud cake — the filter cake formed on the wellbore wall

KEYWORDS: wellbore, mud cake, perforation tunnels, fluid flow, flow lines, near-wellbore region, schematic, cross-section, flow convergence, filtration
----


(b)

Figure 5.11. Microresistivity tools (Hearst and Nelson, 2000)

This figure shows the configuration of electrodes on the pads of a microlag (a) and a spherically focused lag (b). It also illustrates the current flow from each tool into the formation. The electrodes on the microlag (A, M₁, M₂) are spaced one inch apart.
<!-- page 109 -->
98

ASQUITH AND KRYGOWSKI

Figure 5.12. Microlog with SP log and caliper.

This log demonstrates permeability two ways: by positive separation between the micronormal and microinverse logs (MNOR > MINV) in tracks 2 and 3 and by decreased borehole diameter due to mudcake, detected by the caliper log in track 1.

Examine the interval from 5147 to 5246 ft.

Track 1: The caliper measurement is shown by the long-dashed line in track 1. The short-dashed line shows the bit size (BS), which is 8.75 inches. Just above 5147 ft, the caliper shows a borehole diameter of approximately 11 inches, but the hole size decreases to about 8.5 inches from 5147 to 5224 ft, indicating the presence of mudcake and a permeable zone. Mudcake is also present at 5237 to 5245 ft. Note how the SP corresponds with these two mudcake intervals.

Tracks 2 and 3: The micronormal log (MNOR, shown by the dashed line) measures the resistivity of the flushed zone, and the microinverse (MINV, shown by the solid line) measures the resistivity of any mudcake that might be present. Mudcake and permeability are indicated by positive separation, which occurs where micronormal log shows a higher resistivity than the microinverse log. Note the positive separation from 5150 to 5224 ft and from 5237 to 5246 ft. The separation is about 0.5 ohm-m.

The fluid in the flushed zone is a combination of mud filtrate, formation water, and possibly residual hydrocarbons. The fluid in the mudcake is just mud filtrate, which has a higher resistivity than


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Глубина увеличивается вниз. Диапазон глубин: от 160 м до 166 м (отмечено на левой шкале).

Треки слева направо:
1. SP (спонтанное потенциал): шкала от -160 до +6 мВ (отмечено на левой шкале), кривая — сплошная черная линия. Поведение: в интервале 160–166 м — отрицательная аномалия, с плавными колебаниями, амплитуда до ~100 мВ.
2. CALI (калибровка, диаметр скважины): шкала от 6 до 40 дюймов (отмечено на правой шкале), кривая — пунктирная линия. Поведение: в интервале 160–166 м — стабильное значение ~8 дюймов, незначительные колебания.

Интервалы и интерпретация:
| Интервал, м | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|--------------|--------------------------|-------------------|-------------------------------|
| 160–166      | не определена            | SP: отрицательная аномалия, CALI: стабильный диаметр ~8 дюймов | нет подписи |

Результаты петрофизической интерпретации: не представлены.

KEYWORDS: SP, CALI, калибровка, спонтанное потенциал, каротажная диаграмма, глубина, дюймы, мВ, интервал, кривая
----


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: increases downward, units: Feet (MD — measured depth). Depth range: 5100 ft to 5200 ft.

Tracks (left to right):
- Leftmost track: two curves, solid and dashed, with scale 0–40 (MNOR and MINV). Units not specified, but typical for neutron logs (neutron porosity or count rate). Scale range: 0–40.
- Rightmost track: single curve, solid, with scale 0–40 (MNOR and MINV). Units not specified, but likely neutron porosity or count rate. Scale range: 0–40.

Curve behaviour per interval:
- 5100–5110 ft: Solid curve in left track shows a sharp drop from ~35 to ~15, dashed curve remains ~35. Right track curve remains ~35.
- 5110–5120 ft: Solid curve in left track rises to ~30, dashed curve drops to ~20. Right track curve drops to ~20.
- 5120–5130 ft: Solid curve in left track drops to ~15, dashed curve rises to ~30. Right track curve rises to ~30.
- 5130–5140 ft: Solid curve in left track rises to ~30, dashed curve drops to ~15. Right track curve drops to ~15.
- 5140–5150 ft: Solid curve in left track drops to ~10, dashed curve rises to ~30. Right track curve rises to ~30.
- 5150–5160 ft: Solid curve in left track rises to ~30, dashed curve drops to ~10. Right track curve drops to ~10.
- 5160–5170 ft: Solid curve in left track drops to ~10, dashed curve rises to ~30. Right track curve rises to ~30.
- 5170–5180 ft: Solid curve in left track rises to ~30, dashed curve drops to ~10. Right track curve drops to ~10.
- 5180–5190 ft: Solid curve in left track drops to ~10, dashed curve rises to ~30. Right track curve rises to ~30.
- 5190–5200 ft: Solid curve in left track rises to ~30, dashed curve drops to ~10. Right track curve drops to ~10.

Interpretation: No explicit interpretation or lithology labels are present. The curves show alternating high and low values, suggesting alternating lithologies (e.g., sandstone vs. shale). The solid and dashed curves in the left track may represent different neutron tools or corrections (e.g., compensated neutron vs. uncorrected). The right track curve is identical in shape to the solid curve in the left track, suggesting it may be a duplicate or a different tool with similar response.

No perforation intervals, fluid contacts, or results panel (Кп, Кн, etc.) are marked.

KEYWORDS: well log, neutron log, MNOR, MINV, measured depth, feet, curve interpretation, lithology, sandstone, shale, porosity
----


the fluids in the flushed zone. Based on this alone, we might expect the microinverse to show a higher resistivity than the micronormal over intervals of mudcake. Remember, however, that rock generally has a higher resistivity than the fluids in it or around it. The rock in the flushed zone is compacted and cemented, but the rock part of the mudcake (cuttings and mud solids) is not compacted or cemented. Mudcake contains much more fluid and much less rock than an equal volume of the formation in the flushed zone. The higher concentration of fluid in the mudcake gives the mudcake a lower resistivity than the flushed zone.
<!-- page 110 -->
Resistivity Logs

99


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: increases downward, units: inches (0 to 16 inches), scale: 0–16 inches per track.
Tracks (left to right):
- Track 1: CALI (caliper log), scale 0–16 inches, solid line.
- Track 2: MINV (micro-imagery or micro-resistivity), scale 0–10, dashed line.
- Track 3: MNOR (normal resistivity or micro-normal), scale 0–10, solid line.

Depth range: approximately 0 to 16 inches (track scale), but actual depth not labeled — only track scale is visible.

Curve behavior per interval (based on visual pattern):
| Интервал, дюймы | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|------------------|------------------------|-------------------|------------------------------|
| 0–2              | —                      | CALI: ~16, MINV: ~8, MNOR: ~8 | Повышенные показания, возможно, глина или плотный песчаник |
| 2–4              | —                      | CALI: ~16, MINV: ~6, MNOR: ~6 | Снижение, возможно, проницаемый интервал |
| 4–6              | —                      | CALI: ~16, MINV: ~8, MNOR: ~8 | Возврат к высоким значениям |
| 6–8              | —                      | CALI: ~16, MINV: ~6, MNOR: ~6 | Повторное снижение |
| 8–10             | —                      | CALI: ~16, MINV: ~8, MNOR: ~8 | Возврат к высоким значениям |
| 10–12            | —                      | CALI: ~16, MINV: ~6, MNOR: ~6 | Снижение, возможный проницаемый слой |
| 12–14            | —                      | CALI: ~16, MINV: ~8, MNOR: ~8 | Возврат к высоким значениям |
| 14–16            | —                      | CALI: ~16, MINV: ~6, MNOR: ~6 | Снижение, возможный проницаемый интервал |

No perforation intervals, fluid contacts, or interpreted porosity/permeability values are labeled.

KEYWORDS: каротажная диаграмма, калибр, микронормальный, микроволновой, кривые, интервалы, проницаемость, глина, песчаник, глубина, дюймы
----


Feet
MD
-
4100
-
4200


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: 0.2 to 2000, units not specified, depth increases downward.
Track: single track with one curve.
Curve: labeled "PROX", scale from 0.2 to 2000, units not specified.
Curve behavior: highly variable, with multiple peaks and troughs; no specific bed boundaries or interpreted intervals marked.
No lithology, porosity, saturation, or permeability results panel visible.
No well name, location, or date information.
No other curves or tracks present.
No qualitative description of curve behavior per interval provided.

KEYWORDS: PROX, well log, каротажная диаграмма, depth, curve, scale, no units, no interpretation
----


Figure 5.13. Example of a proximity log with a microlog and caliper.

The proximity log is designed to read the resistivity of the flushed zone ($R_{40}$). This particular log package includes a proximity log to read $R_{40}$, a microlog to determine permeable zones, and a caliper to determine the size of the borehole.

Examine the log curves at 4144 ft.

Track 1: Track 1 shows both a microlog and a caliper log. On this example, the resistivity values for micronormal and microinverse increase from right to left, so that the positive separation shows the same pattern with respect to the depth track as it does when displayed in track 2.

At the depth of 4144 ft, the micronormal (MNOR, shown by the dashed line) shows higher resistivity than microinverse (MINV, shown by the solid line). The microinverse has a value of about 1.5 ohm-m, and the micronormal has a value of about 3.0 ohm-m. The microlog indicates a permeable zone. The caliper log indicates a borehole slightly less than 9 inches.

Tracks 2 and 3: The proximity log measures resistivity of the flushed zone ($R_{40}$). In this example the scale is logarithmic, reading from left to right. At 4144 ft, we read a proximity curve value ($R_{40}$) of 18 ohm-m.
<!-- page 111 -->
100

ASQUITH AND KRYGOWSKI


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Глубина увеличивается вниз. Шкала глубины: футы (Feet MD), от 5700 до 5750 футов (приблизительно).

Лог-панель слева:
- Трек 1 (слева): SP — шкала от -160 до +40 мВ, сплошная кривая.
- Трек 2: GR — шкала от 0 до 150 API, сплошная кривая.
- Трек 3: CALI — шкала от 6 до 16 дюймов, сплошная кривая.

Лог-панель справа:
- Трек 1: ILD — шкала от 0.2 до 2000 Ом·м, сплошная кривая.
- Трек 2: ILM — шкала от 0.2 до 2000 Ом·м, пунктирная кривая.
- Трек 3: SFLU — шкала от 0.2 до 2000 Ом·м, штрихпунктирная кривая.

Интерпретация по интервалам (приблизительно, по кривым):
| Интервал, фут | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|---------------|------------------------|-------------------|-------------------------------|
| 5700–5710     | —                      | SP: отрицательная аномалия; GR: повышенные показания; CALI: умеренная каверна | Вероятно, глина или аргиллит |
| 5710–5720     | —                      | SP: положительная аномалия; GR: пониженные показания; CALI: узкий калибр | Вероятно, песчаник или известняк |
| 5720–5730     | —                      | SP: отрицательная аномалия; GR: повышенные показания; CALI: умеренная каверна | Вероятно, глина |
| 5730–5740     | —                      | SP: положительная аномалия; GR: пониженные показания; CALI: узкий калибр | Вероятно, песчаник или известняк |
| 5740–5750     | —                      | SP: отрицательная аномалия; GR: повышенные показания; CALI: умеренная каверна | Вероятно, глина |

На правой панели:
- ILD, ILM, SFLU: в интервалах 5710–5720 и 5730–5740 — высокие сопротивления (до 2000 Ом·м), что указывает на низкую проницаемость или водонасыщенность.
- В интервалах 5700–5710 и 5720–5730 — пониженные сопротивления (около 0.2–100 Ом·м), что указывает на высокую проницаемость или нефтенасыщенность.

Результаты интерпретации не указаны в панели.

KEYWORDS: каротаж, кривые, SP, GR, CALI, ILD, ILM, SFLU, сопротивление, глубина, футы, мВ, API, дюймы, Ом·м, интерпретация, литология, каверна
----


Figure 5.14. Dual induction/SFL log through two Mississippian Chester sandstones in western Kansas.

The Chester sandstones are from 5704 to 5718 ft and from 5724 to 5738 ft.


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth range: 5700–5700 м (single depth point shown), depth increases downward.
Depth units: Feet MD (marked on left side, but depth values are in meters — 5700 м is shown).

Left track:
- Curve: GR (Гамма-каротаж)
  - Scale: 0–100 API units
  - Line style: solid black line
  - Behaviour: Highly variable, with multiple peaks and troughs; shows high values (up to ~90 API) in upper part, then lower values (~40–60 API) in lower part.
- Curve: CALI (Калибровка)
  - Scale: 6–10 inches
  - Line style: dashed line
  - Behaviour: Relatively stable, slight fluctuations around 8–9 inches; no significant washouts or borehole irregularities indicated.

Right track:
- Curve: PEF (Плотность электронного захвата)
  - Scale: 0–10 be (barns/electron)
  - Line style: dashed line
  - Behaviour: Fluctuates between ~4–8 be; higher values in upper part, lower in lower part.
- Curve: DPHI (Диэлектрическая пористость)
  - Scale: 0–0.1 (dimensionless, fractional porosity)
  - Line style: solid black line
  - Behaviour: Highly variable, with multiple peaks and troughs; values range from ~0.02 to ~0.08.
- Curve: NPHI (Нейтронная пористость)
  - Scale: 0–0.1 (dimensionless, fractional porosity)
  - Line style: dashed line
  - Behaviour: Highly variable, with multiple peaks and troughs; values range from ~0.02 to ~0.08; generally parallel to DPHI but slightly offset.

Interval table:
| Интервал, м | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|-------------|--------------------------|-------------------|-------------------------------|
| 5700        | Не определена            | GR: высокие значения (~90 API); CALI: ~8–9 дюймов; PEF: ~4–8 be; DPHI: ~0.02–0.08; NPHI: ~0.02–0.08 | Нет подписи интерпретации |

No results panel (Кп, Кн, Кпр, эфф. толщина) is present.

KEYWORDS: ГК, НГК, ПС, Калибровка, ПЕФ, ДП, НП, пористость, плотность, гамма-каротаж, нейтронный каротаж, диэлектрический каротаж, керн, интерпретация, колонка, глубина
----


Figure 5.15. Neutron-density log through two Mississippian Chester sandstones in western Kansas.

The Chester sandstones are from 5704 to 5718 ft and from 5724 to 5738 ft. The gray shading indicates neutron-density crossover (NPHI < DPHI), indicating gas in the formation.
<!-- page 112 -->
Resistivity Logs

101


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: increases downward, units: feet (Feet), range: approximately 5700–5800 ft (based on visible scale and curve position). Depth scale is marked at 5700 ft.

Track 1 (leftmost):
- Curve: GR (Gamma Ray)
- Scale: 0–150 API units (marked as "API units" and "inches" — likely a misprint or dual scale; "inches" is not applicable to GR)
- Line style: single black curve
- Curve behavior: highly variable, with multiple peaks and troughs; no specific values marked on curve

Track 2 (middle):
- Curve: ILM (Induction Log — likely deep resistivity)
- Scale: 0.2–2000 ohm·m (marked as "ohm·m")
- Line style: single black curve
- Curve behavior: relatively smooth, with a general increase in resistivity downward; no specific values marked on curve

Track 3 (rightmost):
- Curve: PHIA (Porosity — likely from density or neutron log, labeled "PHIA")
- Scale: 0.1–0.8 (unit not specified, but typical for porosity — fractional or %)
- Sub-curves: 
  - PHIA (main curve)
  - ECM (Electrical Compensated Microlog — likely micro-resistivity)
- Line style: two curves — PHIA as solid line, ECM as dashed line
- Curve behavior: PHIA shows moderate variation; ECM shows higher values and more fluctuation; no specific values marked on curves

Interval table:
| Интервал, м | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|-------------|--------------------------|-------------------|-------------------------------|
| 5700–5800   | Не определена            | GR: высокие и низкие значения; ILM: резистивность растёт; PHIA: умеренные колебания | Нет подписи интерпретации |

No results panel (Кп, Кн, Кпр, etc.) is visible.

KEYWORDS: well log, GR, ILM, PHIA, ECM, resistivity, porosity, gamma ray, induction log, microlog, depth scale, feet, API units, ohm·m
----


Figure 5.16. Computer-generated neutron-density porosity (PHIA) and EPT porosity (ECMP) log through two Mississippian Chester sandstones in western Kansas.

The Chester sandstones are from 5704 to 5718 ft and from 5724 to 5738 ft. Note that in both the upper sand and the lower sand, the EPT porosity (ECMP) is less than neutron-density (PHIA) indicating that both sands should be productive. The gray shading shows depths where ECMP<PHIA.
<!-- page 113 -->
4
<!-- page 114 -->
6

Henderson, Steven, 2004, Nuclear Magnetic Resonance Logging, in G. Asquith and D. Krygowski, Basic Well Log Analysis: AAPG Methods in Exploration 16, p. 103-113.

# Nuclear Magnetic Resonance Logging

## GENERAL

At the time of publication of this book, nuclear magnetic resonance (NMR) logs are still not widely used, and their use in some geologic and drilling environments is still problematic. At present, while they create estimates of porosity that are equivalent to the other porosity logs (and have some advantages over those logs), they are most powerful when used in conjunction with that other data rather than instead of it. This chapter is focused on the interpretive applications of NMR logs.

## LIMITATIONS OF CONVENTIONAL LOGS

Conventional porosity and resistivity logs provide the geologist with a first look at the reservoir, but there are practical limits to the accuracy and usefulness of these data. Neutron, density, and sonic porosities are more sensitive to lithology than to reservoir fluids (this is not always the case in a gas-bearing formation). As a result, even small amounts of clay minerals may cause errors in porosity measurements. In addition, reservoirs commonly contain clay-bound, capillary-bound, and moveable water. Resistivity tools are sensitive to *all* water, and Archie water-saturation calculations can overestimate the amount of producible water. Thus, potential pay zones might remain elusive with conventional logs.

Porosity measurements with neutron-density combinations provide an estimate of *total porosity*, which is *all* the pore space in the reservoir whether the pores are interconnected or isolated. Still, with volume of shale ($V_{\text{shale}}$) corrections, it is possible to mostly eliminate the shale effect and arrive at an estimate of *effective porosity* or producible pore space. What remains to be resolved in this situation is the critical difference between any capillary-bound water and moveable water. Furthermore, porosity and resistivity logs pro

provide few clues about other petrophysical information such as hydrocarbon type (e.g., low-viscosity versus high-viscosity oils), pore-size and grain-size distributions, and permeability.

## NUCLEAR MAGNETIC RESONANCE APPLICATIONS

Nuclear magnetic resonance is rapidly gaining popularity in the petroleum industry as a means of overcoming the limitations of conventional logs. The primary advantages of NMR logging over conventional porosity measurements are that it uses no nuclear (radioactive) sources and it provides a lithology-independent measure of porosity. Much like the neutron tool, an NMR tool responds to the amount of hydrogen in the formation or *hydrogen index*. However, unlike the neutron measurement, hydrogen existing in matrix and clay minerals is transparent to the NMR porosity measurement. The result is a porosity measurement that is sensitive only to fluids occupying the pore space. Other petrophysical information may be deduced from the manner in which hydrogen protons react to magnetic fields created by the tool.

At the wellsite, NMR tools are capable of providing measures of both effective and clay-bound porosity (a combination of which yields total porosity), estimates of permeability, hydrocarbon type, pore size distribution, and information pertaining to the moveability of fluids. In many cases, the data obtained from NMR logs are in close agreement with core data. Post-processing of the data away from the well site, incorporating conventional logs and capillary pressure data from core analysis, may provide for a comprehensive evaluation of the uninvaded zone.

## PRINCIPLE OF NMR LOGGING

All formation fluids contain hydrogen protons that are randomly oriented throughout the pore space.

103
<!-- page 115 -->
104

HENDERSON

NMR tools use a strong permanent magnetic field to align, or polarize, the spin axes of these protons in a preferred orientation. For these protons to generate a measurable signal, they must be at a condition of resonance. Resonance is achieved by pulsing the formation with an oscillatory magnetic field which causes the spin axes of the protons to tip away from their preferred orientation. Once the oscillatory magnetic field is removed, the signal generated by the hydrogen protons decays rapidly.

A sequence of repetitive pulses is applied with the NMR tool so that the protons generate a series of measurable signals or echoes. The initial amplitude of the measurable signal represents the amount of hydrogen in the formation and is therefore proportional to porosity. The amplitude of each successive echo, however, never regains that of the previous echo. The result of the pulsing sequence is a series of measurable echoes which, through a process called relaxation, exhibit an exponential decay (Figure 6.1). After some period of time, the amplitude of the echo is too small to be of any use, and the hydrogen protons must be allowed to realign with the permanent magnetic field through a process called polarization.

The exponential decay of the measurable signal—represented by the time constant $T_2$, or relaxation time—is a composite of a number of individual fluid decays in the formation. Through processing, the relaxation time ($T_2$) of each fluid component can be determined. These relaxation times are a function of the petrophysical properties of those fluids and the pores that contain them. The key to understanding the applications of NMR logs lies in the relationship of this relaxation time ($T_2$) to pore size (and fluid properties).

## PORE SIZE AND FLUID MOVEABILITY

Mathematical modeling shows that the relaxation time ($T_2$) of a given fluid within a single pore is proportional to the size of that pore (Coates et al., 1999). Water occupying small pores exhibits short relaxation times because of the rapid attenuation of proton movement in close proximity to grain surfaces. In larger pores where protons are not in such close proximity to grain surfaces, water exhibits longer relaxation times. As a first approximation, the distribution of $T_2$ data within a reservoir (Figure 6.2) depicts the pore-size distribution. This may also be related to grain-size distribution of the reservoir.

Clay-bound water occupies micropores that are characterized by very fast relaxation times ($T_2$). With a specialized pulse sequence, NMR tools may be configured to identify clay-bound water. This provides an

accurate method of distinguishing clay-bound porosity from effective pore space that may contain both capillary-bound and moveable, or free, fluids.

In addition to identifying clay-bound fluids, a primary benefit of NMR logging is its ability to differentiate between producible fluids (free-fluid index, or FFI) and capillary-bound fluids (bulk volume irreducible, or BVI). Free fluids generally occupy larger pores, whereas smaller pores contain fluids mostly bound by high capillary pressures. Because the $T_2$ distribution of a reservoir reflects a distribution of pore sizes, it can be used to determine the relative amounts of producible fluids and capillary-bound fluids (Figures 6.3a and 6.3b). This is extremely valuable in shaly sands and other fine-grained sands where Archie water-saturation calculations overestimate the amount of producible water. When combined with conventional porosity and resistivity data, NMR logs can be used effectively to identify the proportions of free water, clay-bound water, capillary-bound water, and hydrocarbons in a reservoir.

## NMR PERMEABILITY

In theory, permeability increases with pore size and the amount of effective porosity. The larger the pores are and more interconnected the pore network is, the more capable a reservoir is of transmitting fluids. Because relaxation time ($T_2$) is related to pore-size distribution, it can also be used to investigate permeability. For a homogeneous pore network like that of sandstones, small pore sizes generally result in lower permeabilities, whereas larger pore sizes can be associated with higher permeabilities.

There is a variety of methods used to determine NMR permeability, depending upon preference, reservoir conditions, and service company. These methods resolve only matrix permeability and underestimate the permeability of a fractured formation. In many cases, NMR permeability estimates are comparable with core data (Figure 6.4). The two most common permeability models are the free-fluid (or Coates) model and the mean-$T_2$ (or SDR) model.

The free-fluid (Coates) model of permeability determination uses a form of the following equation:

$$k = \left( \frac{\Phi_{NMR}}{C} \right)^4 \left( \frac{FFI}{BVI} \right)^2 \tag{6.1}$$

where:

$k =$ NMR-derived permeability

$\phi_{NMR} =$ NMR-derived effective porosity

$C =$ constant, depending on formation
<!-- page 116 -->
Nuclear Magnetic Resonance Logging 105

$FFI =$ proportion of moveable fluids occupying effective porosity

$BVI =$ proportion of capillary-bound fluids occupying effective porosity

The free-fluid model uses the relative proportion of free-fluid to capillary-bound fluid within effective pore space to determine permeability. In a basic sense, smaller pores contain more capillary-bound fluid ($BVI$) and result in lower calculated permeability, while larger pores contain more free-fluid ($FFI$) and result in higher calculated permeability. This approach is satisfactory for sandstones where the pore network is rather homogeneous, but may be more problematic in carbonates where there is commonly a wider distribution of pore sizes. In carbonates, isolated vuggy pores contain a large quantity of free-fluid ($FFI$) with respect to capillary-bound fluid ($BVI$), but these pores might not contribute to permeability. As a result, permeability is overestimated. In reservoirs containing heavy oils, permeability can be underestimated because of the difficulty in distinguishing high-viscosity fluids from bound fluids on the basis of their fast relaxation times ($T_2$).

The free-fluid model is sensitive to the selection of a $T_2$ cutoff. For a given distribution of $T_2$ data (Figure 6.5), a cutoff may be determined to distinguish capillary-bound fluids from free fluids. For sandstones, this value is approximately 33 msec. Those pores with relaxation times ($T_2$) less than the selected cutoff are assumed to contain mostly capillary-bound fluids, and pores with relaxation times ($T_2$) greater than the cutoff are assumed to contain mostly free fluids. The $T_2$-cutoff selection depends upon lithology (carbonates may have a cutoff of as high as 100 msec) as well as capillary pressure. Therefore, conventional logs and core data can assist in determining a more accurate NMR permeability for a given reservoir.

An alternate method of permeability determination is the mean-$T_2$ (or SDR) model which uses a form of the following equation:

$$k = a \left( \Phi_{NMR} \right)^4 \left( T_{2gm} \right)^2 \tag{6.2}$$

where:

$k =$ NMR-derived permeability

$a =$ a constant, depending on formation

$\Phi_{NMR} =$ NMR-derived effective porosity

$T_{2gm} =$ geometric mean of the $T_2$ distribution

The mean-$T_2$ permeability model does not depend on the selection of a $T_2$ cutoff and, therefore, is not as sensitive to lithology or capillary pressure. Furthermore, in carbonates where there is a wider distribution of $T_2$ values (i.e., wider distribution of pore sizes), the

mean-$T_2$ model may provide a more accurate estimate of permeability through its use of the geometric mean of the $T_2$ distribution (Logan et al., 1997; Figure 6.5).

The presence of hydrocarbons influences the distribution of $T_2$ data, so permeability estimates can be slightly in error in oil-bearing and, particularly, gas-bearing zones. Both the free-fluid and mean-$T_2$ models tend to underestimate permeability in a gas-bearing reservoir. Because the NMR tool responds to the hydrogen index, it underestimates porosity just as the neutron tool does in a gas-bearing zone. To compensate for this effect, hydrogen index corrections can be performed on the NMR measurements to obtain a more accurate value of effective porosity ($\Phi_{NMR}$), or effective porosity may be taken from an alternate source.

### DIRECT HYDROCARBON TYPING

Reservoir fluids are characterized by different polarization times ($T_1$) and relaxation times ($T_2$) as illustrated in Table 1. NMR logging takes advantage of the differences in these time constants to provide several stand-alone methods of hydrocarbon typing. Specialized pulse sequences are required for successful direct hydrocarbon typing from NMR logs, and this requires careful planning before logging is started.

Table 6.1. Typical NMR Properties of Reservoir Fluids (modified after Coates et al., 1999).

|   | Polarization Time T1 (msec) | Relaxation Time T2 (msec) | Viscosity (cp)  |
| --- | --- | --- | --- |
|  Brine | 1 – 500 | 1 – 500 | 0.2 – 0.8  |
|  Oil | 3,000 – 4,000 | 300 – 1,000 | 0.2 – 1,000  |
|  Gas | 4,000 – 5,000 | 30 – 60 | 0.011 – 0.014 (methane)  |

The two most common methods of stand-alone hydrocarbon typing are time-domain analysis (TDA) and diffusion analysis. The basis for time-domain analysis is that brine and hydrocarbons require dramatically different polarization times ($T_1$). TDA data are acquired using a pulse sequence with two separate wait times (dual $T_w$): one short and one long. Brine is fully polarized after both the short $T_w$ and the long $T_w$; therefore, its signal amplitude on $T_2$ distributions for the two wait time measurements is almost the same (Figure 6.6a). Hydrocarbons, however, are fully polarized only after the long $T_w$. The difference in the two
<!-- page 117 -->
106

HENDERSON

$T_2$ distributions is used to detect the presence and determine the saturation of medium to light oils and gas (Figure 6.7 and Figure 6.8). Hydrogen index corrections can also be applied to the data to obtain more accurate values for porosity and permeability in oil-bearing and gas-bearing formations. A requirement of TDA is that there be sufficient $T_2$ contrast between reservoir fluids. If very light hydrocarbons exist, it might be difficult to distinguish them from brine and gas based on their similar relaxation times ($T_2$).

Rate of diffusion of hydrocarbons is related to the viscosity of the fluid that holds them, and diffusion analysis takes advantage of this diffusion contrast between hydrocarbons. Hydrogen in gas is more prone to diffusion than hydrogen in medium to heavy oils. Diffusion analysis data are acquired with a pulse sequence using two separate spacings between pulses, or interecho spacings ($T_e$): one short and one long. Brine and medium oil relax much faster during long-$T_e$ measurements than during short-$T_e$ measurements. Light oil exhibits a large difference in relaxation times ($T_2$) between the two interecho spacings, and heavy oils exhibit only a minor (if any) difference in $T_2$. Brine can be distinguished from medium to light oil by a shift in the $T_2$ distribution between the short and long interecho-spacing measurements (Figure 6.6b). An enhanced diffusion analysis method is also available that uses a long $T_e$ and dual $T_w$ to increase the signal generated by more viscous intermediate oils, and it is reliable over a wider range of viscosities (Akkurt et al., 1998). Neither diffusion-analysis method is useful for gas detection, however, because gas can experience such an extreme shift in the $T_2$ distribution that it is easily confused with capillary-bound water and clay-bound water.

In a more conventional sense, NMR data can be combined with density porosity data to provide a method of gas detection similar to neutron-density combinations. Because of the low hydrogen index of gas-bearing zones, they are characterized by underestimated NMR porosities. Gas-bearing zones can therefore be identified where density porosity is greater than NMR porosity.

### NMR APPLICATIONS IN CARBONATES

The majority of NMR applications were developed for sandstone reservoirs, but these applications have been expanded to carbonate reservoirs as well. Interpretation of NMR logs in carbonates may be more problematic than in sandstones, primarily because of the complex heterogeneous nature of the pore network. In carbonates, there is a weaker relationship between pore size and relaxation time ($T_2$). This might

require calibration of NMR data to core or conventional logs for more accurate results; however, NMR logs in carbonates provide much of the same information as in sandstones.

Though lithology plays little role in the NMR measurement, it still must be considered to configure the tool for obtaining accurate information. One source of difficulty involves the fact that carbonates have longer polarization times ($T_1$) than sandstones. If a pulse sequence is initiated before all hydrogen in the formation has been fully polarized, the NMR porosity would be underestimated. The potential underestimation of porosity can cause compounded errors in the determination of fluid moveability, permeability, and hydrocarbon type.

Carbonates generally require a pulse sequence with long wait times ($T_w$). While this may reduce the error in measurements, it may also translate into slower logging speeds or require additives to the drilling fluid. In addition, the wider pore-size distributions (i.e., $T_2$ distributions) of carbonates tend to introduce some problems into their interpretation. With information from conventional logs and core analysis, however, it is possible to determine cutoff parameters in carbonates that provide accurate estimates of fluid moveability, permeability, and hydrocarbon type.

### REVIEW

1. NMR logs provide lithology-independent measurements of effective porosity as well as total porosity, thus overcoming many of the limitations of conventional porosity measurements (i.e., neutron, density, and sonic).
2. A major advantage of NMR logs is the ability to differentiate between irreducible and moveable fluids in a reservoir. This, combined with effective porosity measurements, leads to more accurate estimates of the amount of producible water.
3. NMR logs provide estimates of permeability, grain-size and pore-size distributions, and even viscosity; all of which are problematic or impossible to determine with conventional porosity and resistivity logs.
4. Through a variety of direct hydrocarbon-typing methods, NMR logs are capable of identifying hydrocarbons and determining their saturations without incorporating data from conventional porosity and resistivity logs.
5. Although the NMR measurement is sensitive only to fluids, the best results are obtained when information about the lithology of a reservoir (e.g., core analysis or a conventional porosity log) is available.
<!-- page 118 -->
Nuclear Magnetic Resonance Logging

107


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
The plot shows a single exponential decay curve of echo amplitudes over time, characteristic of nuclear magnetic resonance (NMR) logging or core analysis.

- X-axis: Time, linear scale, range from 0 to approximately 10 units (no units specified).
- Y-axis: Amplitude, linear scale, range from 0 to the initial amplitude (no units specified).

Curves and features:
- A smooth, exponentially decaying curve starting at the "Initial amplitude" at time = 0.
- The initial amplitude is calibrated to porosity (as stated in the label).
- A series of discrete, vertically aligned "Echo" peaks are shown beneath the decay curve, each corresponding to a time point.
- The spacing between consecutive echoes is labeled as "Inter-echo spacing, Tₑ".
- The decay curve is annotated with "Rate of decay provides information about reservoir fluids and the pores that contain them".
- The time constant characterizing the rate of decay is labeled as "T₂", shown as the time interval from the initial amplitude to the point where the amplitude has decayed to 1/e (approximately 37%) of its initial value.

The plot includes:
- A vertical dashed line from the initial amplitude to the x-axis.
- A horizontal dashed line from the T₂ point on the decay curve to the x-axis.
- A pulse symbol at the origin, labeled "Pulse", indicating the start of the NMR excitation.

> Тренд: Амплитуда эха экспоненциально убывает с течением времени; постоянная времени T₂ характеризует скорость затухания и связана с пористостью и свойствами флюидов в порах.

KEYWORDS: NMR logging, exponential decay, T₂ time constant, echo amplitude, porosity calibration, inter-echo spacing, reservoir fluids, pore characterization
----


Series of Exponential Decays


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
- Horizontal axis: time, labeled as "T₁ Time constant characterizing rate of polarization", scale type linear, range not explicitly given but spans from 0 to beyond the last pulse.
- Vertical axis: amplitude or signal intensity, no units or scale provided, direction upward increasing.
- The plot shows a sequence of pulses (spikes) on the left, followed by a smooth exponential decay curve, then a period labeled "Wait time, T_W", and then another sequence of pulses on the right.
- The left pulse train: consists of multiple sharp, symmetric pulses of decreasing amplitude, spaced evenly in time, indicating a damped oscillation or relaxation process.
- The central curve: a smooth, upward-curving exponential rise from baseline to a plateau, representing the polarization or charging process. The curve is labeled with "T₁" as the time constant characterizing the rate of polarization.
- The right pulse train: identical in shape and spacing to the left, but occurring after a waiting period T_W, indicating a recovery or relaxation phase.
- The "Wait time, T_W" is marked as a horizontal bar above the central curve, spanning from the end of the first pulse train to the start of the second pulse train.
- The curve behavior: the exponential rise during T_W suggests a recovery process governed by the time constant T₁.
> Тренд: The signal recovers exponentially with time constant T₁ after a wait period T_W, following a damped pulse train.

KEYWORDS: T₁, time constant, polarization, exponential recovery, pulse sequence, relaxation, wait time, signal amplitude, NMR logging, well logging
----


Courtesy Halliburton Energy Services ©1999, Halliburton Energy Services

Figure 6.1. A sequence of oscillatory magnetic field pulses (induced by radio-frequency energy) generates echoes which exhibit an exponential decay in amplitude. This exponential decay is a composite of a number of individual fluid decays in the reservoir. The rate of decay—expressed as the time constant $T_{D}$ or relaxation time—is a function of the petrophysical properties of those fluids and the pores that contain them. Initial amplitude of the decay curve is calibrated to represent porosity.

Following a series of pulses, the amplitude of the signal becomes too small to measure and hydrogen protons must be allowed to repolarize with the permanent magnetic field. If the wait time $(T_{w})$ is not long enough, then underpolarization of hydrogen results in an underestimation of NMR porosity.

Pulse sequences can be customized, depending upon the type of data to be gathered. Variables in the pulse sequence that can be altered include wait time $(T_{w})$, the number of pulses, and the spacing between these pulses $(T_{e})$.


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
- Horizontal axis: T₂ Relaxation Time (ms), linear scale, range from 0.1 to 10,000 ms.
- Vertical axis: Porosity, linear scale, no numerical labels or units provided.
- The plot shows a single yellow-shaded curve representing the distribution of porosity as a function of T₂ relaxation time.
- The curve is unimodal, peaking at approximately 100 ms.
- The distribution is asymmetric: it rises steeply from 0.1 ms to the peak at ~100 ms, then declines gradually to ~1,000 ms, with a small tail extending to 10,000 ms.
- No data points are explicitly marked; the curve is smooth and continuous.
- No regression equation, R², or other annotations are present.
> Тренд: Пористость достигает максимума при T₂ ≈ 100 мс, что указывает на доминирование пор с средним временем релаксации; распределение асимметрично, с хвостом в сторону длинных T₂, что может соответствовать наличию крупных пор или трещин.
KEYWORDS: T₂ релаксация, пористость, распределение, NMR, ядерно-магнитный резонанс, геофизика, каротаж, кривая распределения, асимметричное распределение, время релаксации
----


Courtesy Halliburton Energy Services ©1999, Halliburton Energy Services

Figure 6.2. Inversion processing of the individual decay components in a reservoir yields a $T_{2}$ distribution. Calibration of the NMR tool insures that the area beneath the curve is porosity. If a reservoir is at $100\%$ water saturation, then the distribution of $T_{2}$ data reflects the pore size distribution of the reservoir.

Reservoirs with large amounts of irreducible fluids (short relaxation time, $T_{2}$) exhibit peaks to the left of the $T_{2}$ distribution. Reservoirs with a larger proportion of moveable fluids will exhibit peaks to the right of the $T_{2}$ distribution. With data from core and conventional logs, a $T_{2}$ cutoff can be established to differentiate between irreducible fluids and moveable fluids in a given reservoir.

In addition to whether the fluid present is irreducible or moveable, the presence of hydrocarbons will tend to skew the $T_{2}$ distribution, depending upon their type, viscosity, and relative amounts.
<!-- page 119 -->
108

HENDERSON

Figure 6.3a. Example of induction and neutron-density logs through a hydrocarbon-bearing shaly sand in the Gulf of Mexico, North America.

In this example, resistivity gradually decreases with depth through the zone of interest (XX160 – XX260). This decrease in resistivity might be the result of larger amounts of moveable water in the lower half of the zone. However, the gamma ray curve indicates a coarsening-upward sequence, so a great percentage of the water present in the lower half of the zone could be trapped by clays or within smaller pore throats and would not be produced.


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth range: 130 to 280 feet, depth increases downward.

Tracks (left to right):

1. **Caliper (IN)**:
   - Scale: 0 to 6 inches, linear.
   - Curve: Solid line, shows borehole diameter. Values fluctuate between ~4 and ~6 inches throughout the interval.

2. **Gamma Ray (GR)**:
   - Scale: 0 to 150 API, linear.
   - Curve: Solid line, shows natural gamma radiation. Values range from ~40 to ~120 API. A distinct peak near 150 ft, then lower values (~60–80 API) from 170 to 250 ft, followed by a rise to ~100 API near 280 ft.

3. **SP (Spontaneous Potential)**:
   - Scale: -150 to +150 mV, linear.
   - Curve: Dashed line, shows SP deflection. Shows a negative anomaly (below 0 mV) from 130 to 170 ft, then a positive anomaly (above 0 mV) from 170 to 250 ft, returning to near 0 mV at 280 ft.

4. **DEPTH FEET**:
   - Scale: 130 to 280 ft, linear.
   - Marked depths: 130, 150, 200, 250, 280 ft.

5. **Deep Res. (Deep Resistivity)**:
   - Scale: 0.2 to 2000 ohm·m, logarithmic.
   - Curve: Solid line, shows deep resistivity. Values are low (~1–10 ohm·m) from 130 to 170 ft, then increase to ~100–200 ohm·m from 170 to 250 ft, then drop to ~10 ohm·m near 280 ft.

6. **Shallow Res. (Shallow Resistivity)**:
   - Scale: 0.2 to 2000 ohm·m, logarithmic.
   - Curve: Dashed line, shows shallow resistivity. Values are low (~1–10 ohm·m) from 130 to 170 ft, then increase to ~100–200 ohm·m from 170 to 250 ft, then drop to ~10 ohm·m near 280 ft.

7. **Neutron Por. (Neutron Porosity)**:
   - Scale: 0 to 60%, linear.
   - Curve: Solid line, shows neutron porosity. Values are high (~30–40%) from 130 to 170 ft, then decrease to ~10–15% from 170 to 250 ft, then increase to ~25–30% near 280 ft.

8. **Density Por. (Density Porosity)**:
   - Scale: 0 to 60%, linear.
   - Curve: Dashed line, shows density porosity. Values are high (~30–40%) from 130 to 170 ft, then decrease to ~10–15% from 170 to 250 ft, then increase to ~25–30% near 280 ft.

Interval Table:

| Интервал, м (ft) | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|------------------|------------------------|-------------------|-------------------------------|
| 130–170          | Песчаник (по ГК и ПС)  | ГК: высокие; ПС: отрицательная аномалия; Рд: низкие; Рм: низкие; НП: высокие; ПП: высокие | Вероятно, водоносный песчаник |
| 170–250          | Глина/сланец (по ГК)   | ГК: низкие; ПС: положительная аномалия; Рд: высокие; Рм: высокие; НП: низкие; ПП: низкие | Вероятно, глинистый интервал |
| 250–280          | Песчаник (по ГК и ПС)  | ГК: средние; ПС: близко к 0; Рд: низкие; Рм: низкие; НП: средние; ПП: средние | Вероятно, водоносный песчаник |

No results panel (Кп, Кн, Кпр, etc.) is present.

KEYWORDS: каротажная диаграмма, ГК, ПС, Рд, Рм, НП, ПП, глубина, фильтрация, литология, интерпретация
----


Courtesy Halliburton Energy Services ©1999, Halliburton Energy Services
<!-- page 120 -->
Nuclear Magnetic Resonance Logging

109


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Глубина увеличивается вниз. Диапазон глубин: 1240–2500 FT (футов).

Треки слева направо:

1. **ГАММА-КАРТА (GAMMA RAY)**:
   - Масштаб: 0–150 API (единицы ГК)
   - Кривая: сплошная чёрная линия
   - Поведение: в интервале 1240–2500 FT — колебания от ~40 до ~120 API, с локальными пиками в 1300–1350 FT (~120 API) и 1800–1900 FT (~100 API), и минимумами в 1400–1500 FT (~50 API) и 2000–2200 FT (~60 API)

2. **КАЛИБР (CALIPER)**:
   - Масштаб: 0–18 дюймов
   - Кривая: сплошная чёрная линия
   - Поведение: в интервале 1240–2500 FT — колебания от ~8 до ~16 дюймов, с уширением в 1300–1350 FT (~16 дюймов) и 1800–1900 FT (~15 дюймов)

3. **СП (SP)**:
   - Масштаб: -200 до +50 мВ
   - Кривая: сплошная чёрная линия
   - Поведение: в интервале 1240–2500 FT — отрицательная аномалия, колебания от -100 до -200 мВ, с локальными минимумами в 1300–1350 FT и 1800–1900 FT

4. **T2-POROS**:
   - Масштаб: 0–100 (единицы T2-пористости)
   - Кривая: сплошная чёрная линия
   - Поведение: в интервале 1240–2500 FT — колебания от ~20 до ~80, с пиками в 1300–1350 FT (~80) и 1800–1900 FT (~70)

5. **SHAL. RES. (Поверхностное сопротивление)**:
   - Масштаб: 0–200 Ом·м
   - Кривая: сплошная красная линия
   - Поведение: в интервале 1240–2500 FT — колебания от ~50 до ~150 Ом·м, с пиками в 1300–1350 FT (~150) и 1800–1900 FT (~140)

6. **MED. RES. (Среднее сопротивление)**:
   - Масштаб: 0–200 Ом·м
   - Кривая: сплошная чёрная линия
   - Поведение: в интервале 1240–2500 FT — колебания от ~100 до ~180 Ом·м, с пиками в 1300–1350 FT (~180) и 1800–1900 FT (~170)

7. **DEEP. RES. (Глубокое сопротивление)**:
   - Масштаб: 0–250 Ом·м
   - Кривая: сплошная чёрная линия
   - Поведение: в интервале 1240–2500 FT — колебания от ~120 до ~220 Ом·м, с пиками в 1300–1350 FT (~220) и 1800–1900 FT (~210)

8. **M3IL PERM. (Пористость по методу M3IL)**:
   - Масштаб: 0–2000 мД (миллидарси)
   - Кривая: сплошная чёрная линия
   - Поведение: в интервале 1240–2500 FT — колебания от ~500 до ~1800 мД, с пиками в 1300–1350 FT (~1800) и 1800–1900 FT (~1700)

9. **T2 DIST. (Распределение T2)**:
   - Масштаб: 0–3200 мс (миллисекунд)
   - Кривая: цветная диаграмма (спектр T2-распределения)
   - Поведение: в интервале 1240–2500 FT — цветовая шкала от синего (низкие T2) до жёлтого (высокие T2), с максимумами в 1300–1350 FT и 1800–1900 FT

10. **MPH II (Метод оценки флюида)**:
    - Масштаб: 0–100 (единицы)
    - Кривая: сплошная чёрная линия
    - Поведение: в интервале 1240–2500 FT — колебания от ~20 до ~80, с пиками в 1300–1350 FT (~80) и 1800–1900 FT (~75)

11. **BVI (Индекс свободного флюида)**:
    - Масштаб: 0–100 (единицы)
    - Кривая: сплошная чёрная линия
    - Поведение: в интервале 1240–2500 FT — колебания от ~0 до ~60, с пиками в 1300–1350 FT (~60) и 1800–1900 FT (~55)

12. **CAPIL-BVI (Капиллярный BVI)**:
    - Масштаб: 0–100 (единицы)
    - Кривая: сплошная чёрная линия
    - Поведение: в интервале 1240–2500 FT — колебания от ~0 до ~40, с пиками в 1300–1350 FT (~40) и 1800–1900 FT (~35)

13. **FREE-FLUID (Свободный флюид)**:
    - Масштаб: 0–100 (единицы)
    - Кривая: сплошная чёрная линия
    - Поведение: в интервале 1240–2500 FT — колебания от ~0 до ~60, с пиками в 1300–1350 FT (~60) и 1800–1900 FT (~55)

**Интерпретация по интервалам**:
| Интервал, FT | Литология (по ГК и кривым сопротивления) | Кривые: поведение | Интерпретация |
|--------------|------------------------------------------|-------------------|---------------|
| 1240–1300    | Глина/слабо-песчанистая глина            | ГК: ~100 API, SP: -150 мВ, Р: ~100 Ом·м | Низкая пористость, низкая проницаемость |
| 1300–1350    | Песчаник                                 | ГК: ~120 API, SP: -200 мВ, Р: ~180 Ом·м, T2: высокие, BVI: ~60 | Высокая пористость, высокая проницаемость, свободный флюид |
| 1350–1800    | Глина/алеврит                            | ГК: ~80 API, SP: -120 мВ, Р: ~120 Ом·м | Средняя пористость, низкая проницаемость |
| 1800–1900    | Песчаник                                 | ГК: ~100 API, SP: -180 мВ, Р: ~170 Ом·м, T2: высокие, BVI: ~55 | Высокая пористость, высокая проницаемость, свободный флюид |
| 1900–2500    | Глина/алеврит                            | ГК: ~70 API, SP: -100 мВ, Р: ~100 Ом·м | Низкая пористость, низкая проницаемость |

**Результаты интерпретации (в верхней части трека T2 DIST)**:
- X150: 150 мс
- X200: 200 мс
- X250: 250 мс

KEYWORDS: каротажная диаграмма, ГК, СП, калибр, T2-пористость, сопротивление, проницаемость, свободный флюид, BVI, капиллярное давление, интерпретация колонки, песчаник, глина, пористость, проницаемость, флюидный режим
----


Courtesy Halliburton Energy Services ©1999, Halliburton Energy Services

Figure 6.3b. Example of Magnetic Resonance Imaging Log$^{100}$ through a hydrocarbon-bearing shaly sand in the Gulf of Mexico, North America.

This log is from the same well as illustrated in Figure 6.3a.

Track 1 contains gamma ray and caliper curves as well as partial porosities of each fluid decay component in the reservoir. The partial porosities may be ignored for the purpose of this discussion.

Track 2 contains resistivity curves measured by the induction log and a permeability curve (MRIL PERM) determined from the NMR measurements.

Track 3 displays the $T_2$ distribution resulting from the measured exponential decays. Notice that the shales above and below the zone of interest exhibit large peaks to the left of the distribution, indicating large amounts of irreducible fluids (for an explanation, see Figure 6.5).

Track 4: This track contains an effective porosity curve (MPHI) and a bulk volume irreducible curve (BVI). BVI represents the amount of capillary-bound fluid in the reservoir, and the yellow-shaded region between the MPHI and BVI curves represents the amount of moveable, or free, fluid in the reservoir.

A coarsening-upward sequence can be further confirmed by the increase of BVI with depth. Below a depth of X210, the NMR log indicates an increasing proportion of irreducible fluids (BVI, gray-shaded area) than moveable fluids (FFI, yellow-shaded area). If the moveable fluid present is hydrocarbons, the larger fraction of irreducible water would be responsible for the lower resistivities seen in the lower half of the zone of interest. The presence of hydrocarbons can be determined by incorporating the conventional resistivity data into the NMR processing (see Figure 6.8).
<!-- page 121 -->
110

HENDERSON

Figure 6.4. Example of Magnetic Resonance Imaging Log™ through a shaly sand in Egypt illustrating the comparison of NMR permeability (MPERM) to core permeability (CPERMH) and NMR porosity (MPHI) to core porosity (CPOR).


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Глубина увеличивается вниз. Диапазон глубин: от 0 до 300 м (отмечено как X000m, X010m, X020m, X030m).

Треки слева направо:

1. **Трек 1 (левый)**:
   - Кривая: MPERM (модульная проницаемость, вероятно, в мД)
   - Масштаб: 1:200 (вертикальный масштаб, 1 см = 200 м)
   - Единицы: М. (метры)
   - Кривая: зелёная, спиралевидная, с отклонениями вправо и влево.
   - На кривой нанесены красные звёздочки — вероятно, точки измерения или интерпретационные маркеры.
   - Видимые значения: кривая колеблется, но не имеют чётких числовых меток. Видны отклонения в интервалах X000–X010 м и X020–X030 м.

2. **Трек 2 (центральный)**:
   - Кривая: CPERM (проницаемость, вероятно, в мД)
   - Масштаб: 1000/30 (вероятно, 1000 мД на 30 делений)
   - Единицы: MD (миллидарси)
   - Кривая: тонкая чёрная, спиралевидная, с высокой амплитудой колебаний.
   - Видимые значения: не читаются, но кривая показывает резкие колебания, особенно в интервалах X000–X010 м и X020–X030 м.

3. **Трек 3 (правый)**:
   - Кривая: MPH (скорость прохождения, вероятно, в м/с или м/мин)
   - Масштаб: 1000/30 (вероятно, 1000 единиц на 30 делений)
   - Единицы: DEC (десятичные единицы, не уточнены)
   - Кривая: чёрная, спиралевидная, с высокой амплитудой колебаний.
   - Видимые значения: не читаются, но кривая показывает резкие колебания, особенно в интервалах X000–X010 м и X020–X030 м.

4. **Трек 4 (правый край)**:
   - Кривая: CROS (вероятно, кросс-корреляция или кривая сопротивления)
   - Масштаб: 0 (не определён)
   - Единицы: DEC (десятичные единицы)
   - Кривая: чёрная, спиралевидная, с высокой амплитудой колебаний.
   - Видимые значения: не читаются, но кривая показывает резкие колебания, особенно в интервалах X000–X010 м и X020–X030 м.

Интерпретация:
- В интервалах X000–X010 м и X020–X030 м наблюдается повышенная активность на всех кривых, что может указывать на зоны с изменёнными физическими свойствами (например, проницаемость, скорость прохождения, сопротивление).
- Кривые MPERM и CPERM показывают схожую тенденцию, что может указывать на корреляцию между модульной и измеренной проницаемостью.
- Кривые MPH и CROS также демонстрируют схожие колебания, что может указывать на связь с геомеханическими или электрическими свойствами.

Интервалы и поведение кривых:

| Интервал, м | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|-------------|--------------------------|-------------------|-------------------------------|
| 0–100       | Не определена            | MPERM: колебания с красными звёздочками; CPERM: высокие колебания; MPH: высокие колебания; CROS: высокие колебания | Зона с изменёнными физическими свойствами |
| 100–200     | Не определена            | MPERM: спад; CPERM: спад; MPH: спад; CROS: спад | Зона с уменьшением свойств |
| 200–300     | Не определена            | MPERM: колебания с красными звёздочками; CPERM: высокие колебания; MPH: высокие колебания; CROS: высокие колебания | Зона с изменёнными физическими свойствами |

KEYWORDS: каротажная диаграмма, MPERM, CPERM, MPH, CROS, проницаемость, скорость прохождения, сопротивление, глубина, интервал, колебания, звёздочки, интерпретация
----


Courtesy Halliburton Energy Services ©1999, Halliburton Energy Services
<!-- page 122 -->
Nuclear Magnetic Resonance Logging

111


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
The image contains two separate XY plots, each representing a T₂ distribution model.

**Top Plot: Coates Model**
- X-axis: T₂ (transverse relaxation time), scale type linear, range not specified.
- Y-axis: Amplitude (unlabelled), scale type linear, range not specified.
- Two distinct peaks are shown:
  - Left peak (blue, shaded): labelled "BVI" (Bound Fluid Volume).
  - Right peak (yellow, shaded): labelled "FFI" (Free Fluid Index).
- A vertical red line is drawn at the boundary between the two peaks, marked "T₂cutoff".
- The plot shows a bimodal distribution with a clear separation between bound and free fluid components.

**Bottom Plot: SDR Model**
- X-axis: T₂ (transverse relaxation time), scale type linear, range not specified.
- Y-axis: Amplitude (unlabelled), scale type linear, range not specified.
- Two overlapping peaks are shown, both shaded yellow:
  - Left peak: unlabelled, represents bound fluid.
  - Right peak: unlabelled, represents free fluid.
- A vertical red line is drawn at the boundary between the two peaks, marked "T₂gm" (T₂ geometric mean).
- The plot shows a bimodal distribution with overlapping components, and the cutoff is defined at the geometric mean of the distribution.

> Тренд: The Coates Model uses a fixed T₂cutoff to separate bound and free fluid, while the SDR Model uses the T₂gm (geometric mean) as the cutoff, which is calculated from the entire distribution.

KEYWORDS: T₂ distribution, Coates Model, SDR Model, BVI, FFI, T₂cutoff, T₂gm, NMR logging, fluid typing, pore size distribution


Courtesy Halliburton Energy Services ©1999, Halliburton Energy Services

Figure 6.5. T₂ distributions illustrating the free-fluid (Coates) and mean-T₂ (SDR) methods of permeability estimation from NMR logs.

The free-fluid (Coates) permeability model uses the ratio of moveable fluid (FFI) to irreducible fluid (BVI) to estimate permeability. With information from core and/or conventional logs, a T₂ cutoff may be established. The pore space beneath the curve and to the right of the T₂ cutoff is assumed to contain free, or moveable, fluids (FFI). The pore space beneath the curve and to the left of the T₂ cutoff is assumed to contain irreducible fluids (BVI).

The mean-T₂ (SDR) permeability model uses the geometric mean of the T₂ distribution to differentiate between moveable fluid and irreducible fluid. Pore space beneath the curve and to the right of the mean-T₂ is assumed to contain moveable fluid (FFI). The pore space beneath the curve and to the left of the mean-T₂ is assumed to contain irreducible fluid (BVI).

You can use the information on this page to interpret track 3 of Figure 6.3b.


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
This is a pair of T₂ distribution plots (NMR logs) for two different echo spacing (TW) conditions: Long TW and Short TW.

The horizontal axis is T₂ (ms), with a logarithmic scale ranging from 1 to 1,000 ms. The vertical axis is not labelled but represents the amplitude or frequency of the T₂ distribution (often called "T₂ amplitude" or "NMR signal intensity").

There are two panels:
- Top panel: labelled "Long TW"
- Bottom panel: labelled "Short TW"

In both panels, the T₂ distribution is shown as a blue curve with three distinct peaks:
- A small peak on the left (short T₂, ~1–10 ms)
- A large central peak (medium T₂, ~100 ms)
- A smaller peak on the right (long T₂, ~1,000 ms)

In the top panel ("Long TW"), the central peak is split into two components:
- A red component (medium T₂, ~100 ms)
- A green component (long T₂, ~1,000 ms)

In the bottom panel ("Short TW"), the red and green components are not separated; they appear as a single broad blue peak centred around ~100 ms, with the long T₂ component (green) being suppressed or not resolved.

This illustrates the effect of echo spacing (TW) on NMR T₂ distribution: long TW suppresses short T₂ components (e.g., bound fluid) and enhances the resolution of medium and long T₂ components (e.g., free fluid), while short TW captures all components but with less resolution between medium and long T₂.

> Тренд: При увеличении TW (от Short к Long) подавляются короткие T₂ компоненты (связанная жидкость), а компоненты средних и длинных T₂ (свободная жидкость) становятся более разрешёнными.

KEYWORDS: T₂ распределение, NMR, Long TW, Short TW, эхо-интервал, логарифмическая шкала, амплитуда сигнала, связанная жидкость, свободная жидкость, пик T₂, NMR логирование
----


(a) Dual TW Logging: T₁-Weighted


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
This is a T₂ distribution plot, commonly used in NMR logging, showing two separate distributions for Short TE and Long TE.

- **X-axis**: T₂ (ms), logarithmic scale, range from 1 to 1,000 ms.
- **Y-axis**: Not labelled, but represents relative amplitude or distribution density (arbitrary units).

Two panels are shown:

**Top panel: Short TE**
- Contains two distinct peaks:
  - Left peak: blue, centred around 10 ms.
  - Right peak: green, centred around 100 ms.
- The green peak is taller and broader than the blue peak.

**Bottom panel: Long TE**
- Contains two distinct peaks:
  - Left peak: blue, centred around 10 ms.
  - Right peak: green, centred around 100 ms.
- The blue peak is significantly larger (higher amplitude) than in the top panel, while the green peak is smaller.

> Тренд: With increasing TE (from Short to Long), the amplitude of the short-T₂ component (blue) increases relative to the long-T₂ component (green), indicating that the short-T₂ component has a longer T₂ relaxation time than initially apparent, or that the long-T₂ component is more affected by T₂ decay.

KEYWORDS: NMR logging, T₂ distribution, Short TE, Long TE, relaxation time, pore size distribution, log interpretation, nuclear magnetic resonance, well logging, fluid typing
----


(b) Dual TE Logging: D-Weighted


Courtesy Halliburton Energy Services ©1999, Halliburton Energy Services

Figure 6.6. Changes in T₂ distributions for different methods of NMR direct hydrocarbon typing.

6a: Time-domain analysis uses a combination of short and long wait times (Tₘ) to detect and determine the saturations of medium to light oils and gas. After the short wait time, the water signal is at a maximum amplitude while oil and gas have only been partially polarized. After the long wait time, the oil and gas have been fully polarized and there is no change in the amplitude of the water signal. The difference in T₂ distributions between the two wait time measurements can be used to determine the saturations of oil and gas.

6b: Diffusion analysis uses a combination of short and long inter-echo spacings (Tₑ) to detect and determine the saturations of oil. Relaxation times (T₂) of water and medium to heavy oils are much faster using long-Tₑ measurements than when using short-Tₑ measurements. The shift in peaks of the T₂ distributions may be used to detect and determine the saturations of these fluids. Diffusion analysis is not effective for detecting gas because gas may exhibit such a dramatic shift in T₂ that it is confused with the irreducible water signal.
<!-- page 123 -->
112

HENDERSON

Figure 6.7. Example of dual-$T_w$ Magnetic Resonance Imaging Log™ through an oil-bearing shaly sand in the Gulf of Mexico, North America.

Track 1 illustrates gamma ray and caliper curves. Track 2 shows the NMR permeability curve (MRL PERM). Track 3 displays the $T_2$ distribution of the long-$T_w$ measurement ($T_w = 8$ sec) and Track 4 displays the $T_2$ distribution for the short-$T_w$ measurement ($T_w = 1$ sec). Tracks 5 and 6 display effective porosity (MPHI) and irreducible fluid (BVI) as determined from both the long- and short-$T_w$ measurements, respectively. In Tracks 5 and 6, the yellow-shaded region represents the proportion of moveable fluid (FFI) for the different $T_w$ measurements.

Comparison of BVI and FFI values between the long-$T_w$ (track 5) and short-$T_w$ (track 6) measurements may be used as a quick-look indicator of hydrocarbons. Gas and light oil have longer polarization times ($T_1$) and require a longer wait time ($T_w$) for full polarization than does water. Water, either bound or free, is fully polarized after the short-$T_w$. Light oil and gas (requiring longer polarization), is polarized only after the long-$T_w$. Therefore, if hydrocarbons are present, the long-$T_w$ should show a larger FFI than the short-$T_w$. Note that the yellow-shaded region (FFI) in track 5 (long-$T_w$) is wider than the yellow-shaded region (FFI) in track 6 (short-$T_w$), indicating the presence of light oil or gas. Heavy oils, with very short relaxation times ($T_2$), might appear as an increase in BVI between the short and long wait times.

For this example, integration of resistivity measurements from the induction lag showed that all of the moveable fluid occupying the zone of interest from XX690 to XX865 is oil. The reservoir is therefore determined to be at irreducible water saturation ($S_{air}$). NMR permeability data (track 2) also indicate that there is sufficient permeability to produce this oil.


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Глубина увеличивается вниз. Диапазон глубин: 300700–300900 м.

Треки слева направо:

1. **ГАММА-КАРТА (GAMMA RAY)** — шкала 0–100 API, единицы API. Кривая: волнообразная, с пиками в интервалах 300700–300720 м и 300880–300890 м, минимумы в 300730–300750 м и 300850–300870 м. Цвет: зелёный.

2. **КАЛИЙ (K)** — шкала 0–5%, единицы %. Кривая: волнообразная, с максимумами в 300700–300720 м и 300880–300890 м, минимумы в 300730–300750 м и 300850–300870 м. Цвет: серый.

3. **КАЛЬЦИЙ (CAL)** — шкала 0–100%, единицы %. Кривая: волнообразная, с максимумами в 300700–300720 м и 300880–300890 м, минимумы в 300730–300750 м и 300850–300870 м. Цвет: серый.

4. **ПС (SP)** — шкала -100 до +100 мВ, единицы мВ. Кривая: волнообразная, с отрицательными аномалиями в 300700–300720 м и 300880–300890 м, положительными в 300730–300750 м и 300850–300870 м. Цвет: серый.

5. **МПН, РЕЗИСТИВИМЕТРИЯ (MPH, RESISTIVITY)** — шкала 0–1000 Ом·м, единицы Ом·м. Кривая: волнообразная, с максимумами в 300700–300720 м и 300880–300890 м, минимумы в 300730–300750 м и 300850–300870 м. Цвет: жёлтый.

6. **Т2-DIST** — шкала 0–2000 мкс, единицы мкс. Кривая: волнообразная, с максимумами в 300700–300720 м и 300880–300890 м, минимумы в 300730–300750 м и 300850–300870 м. Цвет: жёлтый.

7. **Т2-DIST** — шкала 0–2000 мкс, единицы мкс. Кривая: волнообразная, с максимумами в 300700–300720 м и 300880–300890 м, минимумы в 300730–300750 м и 300850–300870 м. Цвет: синий.

8. **МРМАХ (MPMAX)** — шкала 0–1000 Ом·м, единицы Ом·м. Кривая: волнообразная, с максимумами в 300700–300720 м и 300880–300890 м, минимумы в 300730–300750 м и 300850–300870 м. Цвет: жёлтый.

9. **МРМИН (MPMIN)** — шкала 0–1000 Ом·м, единицы Ом·м. Кривая: волнообразная, с максимумами в 300700–300720 м и 300880–300890 м, минимумы в 300730–300750 м и 300850–300870 м. Цвет: жёлтый.

10. **СОПР-ВОД (COPR-WD)** — шкала 0–100%, единицы %. Кривая: волнообразная, с максимумами в 300700–300720 м и 300880–300890 м, минимумы в 300730–300750 м и 300850–300870 м. Цвет: жёлтый.

11. **СОПР-НЕФ (COPR-NEF)** — шкала 0–100%, единицы %. Кривая: волнообразная, с максимумами в 300700–300720 м и 300880–300890 м, минимумы в 300730–300750 м и 300850–300870 м. Цвет: жёлтый.

12. **СВОБ-ВОД (FREE-FLUID)** — шкала 0–100%, единицы %. Кривая: волнообразная, с максимумами в 300700–300720 м и 300880–300890 м, минимумы в 300730–300750 м и 300850–300870 м. Цвет: жёлтый.

13. **СВОБ-НЕФ (FREE-FLUID)** — шкала 0–100%, единицы %. Кривая: волнообразная, с максимумами в 300700–300720 м и 300880–300890 м, минимумы в 300730–300750 м и 300850–300870 м. Цвет: жёлтый.

Интервальные таблица:

| Интервал, м | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|-------------|------------------------|-------------------|-------------------------------|
| 300700–300720 | Не определена | ГК, K, CAL, SP, MPH, T2-DIST, MPMAX, MPMIN, COPR-WD, COPR-NEF, FREE-FLUID — максимумы | Высокие значения ГК, K, CAL, SP, резистивиметрия, T2-DIST, MPMAX, MPMIN, COPR-WD, COPR-NEF, FREE-FLUID |
| 300730–300750 | Не определена | ГК, K, CAL, SP, MPH, T2-DIST, MPMAX, MPMIN, COPR-WD, COPR-NEF, FREE-FLUID — минимумы | Низкие значения ГК, K, CAL, SP, резистивиметрия, T2-DIST, MPMAX, MPMIN, COPR-WD, COPR-NEF, FREE-FLUID |
| 300850–300870 | Не определена | ГК, K, CAL, SP, MPH, T2-DIST, MPMAX, MPMIN, COPR-WD, COPR-NEF, FREE-FLUID — минимумы | Низкие значения ГК, K, CAL, SP, резистивиметрия, T2-DIST, MPMAX, MPMIN, COPR-WD, COPR-NEF, FREE-FLUID |
| 300880–300890 | Не определена | ГК, K, CAL, SP, MPH, T2-DIST, MPMAX, MPMIN, COPR-WD, COPR-NEF, FREE-FLUID — максимумы | Высокие значения ГК, K, CAL, SP, резистивиметрия, T2-DIST, MPMAX, MPMIN, COPR-WD, COPR-NEF, FREE-FLUID |

KEYWORDS: каротажная диаграмма, ГК, SP, резистивиметрия, T2-DIST, MPMAX, MPMIN, COPR-WD, COPR-NEF, FREE-FLUID, глубина, интервал, кривые, аномалии, волнообразная форма
----


Courtesy Halliburton Energy Services ©1999, Halliburton Energy Services
<!-- page 124 -->
Nuclear Magnetic Resonance Logging 113


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Глубина увеличивается вниз. Диапазон глубин: от 1240 м до 2500 м (по шкале F1).

Треки слева направо:

1. **GAMMA RAY (ГК)**:
   - Шкала: 0–200 API (с подписью "SP -200 — +200" и "12-POHOS").
   - Кривая: тонкая черная линия, показывает колебания с пиками и впадинами.
   - Подпись: "X150" — вероятно, масштаб или коэффициент для кривой.

2. **CALIPER (Калибр)**:
   - Шкала: 0–200 (единицы не указаны, но по контексту — дюймы или см).
   - Кривая: тонкая черная линия, показывает колебания, соответствующие диаметру скважины.

3. **SHAL. RES. (ПС, низкое сопротивление)**:
   - Шкала: 200–2000 Ом·м (логарифмическая).
   - Кривая: тонкая черная линия, показывает резкие изменения, особенно в интервале 1240–1300 м.

4. **MED. RES. (ПС, среднее сопротивление)**:
   - Шкала: 200–2000 Ом·м (логарифмическая).
   - Кривая: тонкая черная линия, аналогична SHAL. RES., но с более гладким поведением.

5. **DEEP. RES. (ПС, глубокое сопротивление)**:
   - Шкала: 200–2000 Ом·м (логарифмическая).
   - Кривая: тонкая черная линия, показывает более плавные изменения, чем SHAL. RES.

6. **MIL. PERM. (Миллисопротивление, вероятно, для перфорации)**:
   - Шкала: 200–2000 Ом·м (логарифмическая).
   - Кривая: тонкая черная линия, аналогична DEEP. RES.

7. **T2 DIST. (T2-распределение, NMR)**:
   - Шкала: 3000–4 (единицы не указаны, вероятно, мс).
   - Кривая: цветная шкала (желтый, зеленый, красный), показывает распределение T2, с высокими значениями (желтый) в интервале 1240–1300 м.

8. **DIP. SPEC. (Спецификация падения, вероятно, для бокового каротажа)**:
   - Шкала: 0–100 (единицы не указаны).
   - Кривая: черно-белые пятна, вероятно, отображают амплитуду или интенсивность сигнала.

9. **RQAS (Резистивиметрия, вероятно, для оценки качества пласта)**:
   - Шкала: 0–8 (единицы не указаны).
   - Кривая: тонкая черная линия, показывает колебания.

10. **BOIL (Бол, вероятно, для оценки насыщенности)**:
    - Шкала: 0–8 (единицы не указаны).
    - Кривая: тонкая черная линия, показывает колебания.

11. **RWTR (Вода, вероятно, для оценки насыщенности)**:
    - Шкала: 0–8 (единицы не указаны).
    - Кривая: тонкая черная линия, показывает колебания.

12. **RVIA (Вероятно, для оценки насыщенности)**:
    - Шкала: 0–8 (единицы не указаны).
    - Кривая: тонкая черная линия, показывает колебания.

13. **NPHI (Нейтронная пористость)**:
    - Шкала: 0–8 (единицы не указаны, вероятно, %).
    - Кривая: тонкая черная линия, показывает колебания.

14. **RVI (Вероятно, для оценки насыщенности)**:
    - Шкала: 0–8 (единицы не указаны).
    - Кривая: тонкая черная линия, показывает колебания.

15. **CSVNE (Вероятно, для оценки насыщенности)**:
    - Шкала: 0–8 (единицы не указаны).
    - Кривая: тонкая черная линия, показывает колебания.

16. **MPHI (Пористость, вероятно, по методу NMR)**:
    - Шкала: 0–8 (единицы не указаны, вероятно, %).
    - Кривая: тонкая черная линия, показывает колебания.

17. **MSIG (Сигнал, вероятно, для оценки насыщенности)**:
    - Шкала: 0–8 (единицы не указаны).
    - Кривая: тонкая черная линия, показывает колебания.

Верхняя часть диаграммы содержит легенду для цветов:
- **TDA-RVI**: цветная шкала (желтый, зеленый, красный).
- **PHI-CLAY**: цветная шкала (желтый, зеленый, красный).
- **TDA-WATER**: синий.
- **HYDROCARBON**: черный.
- **TDA-OIL**: коричневый.
- **FRES-WTR**: синий.
- **TDA-GAS**: серый.
- **CAPL-RVI**: серый.

В левой части диаграммы присутствует вертикальная шкала глубин с отметками 1240, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500 м.

Интервалы и интерпретация:
- В интервале 1240–1300 м: высокие значения T2 DIST. (желтый цвет), повышенные показания ГК, низкие значения резистивиметрии (SHAL. RES., MED. RES., DEEP. RES.).
- В интервале 1300–1400 м: снижение T2 DIST. (зеленый цвет), уменьшение ГК, рост резистивиметрии.
- В интервале 1400–1500 м: устойчивые значения T2 DIST. (зеленый), умеренные значения ГК, умеренные резистивиметрия.
- В интервале 1500–1600 м: резкое снижение T2 DIST. (красный), резкое снижение ГК, резкое увеличение резистивиметрии — указывает на возможный газоносный интервал.
- В интервале 1600–1700 м: устойчивые значения T2 DIST. (красный), умеренные ГК, умеренные резистивиметрия.
- В интервале 1700–1800 м: рост T2 DIST. (желтый), рост ГК, снижение резистивиметрии — указывает на возможный водонасыщенный интервал.
- В интервале 1800–1900 м: устойчивые значения T2 DIST. (желтый), умеренные ГК, умеренные резистивиметрия.
- В интервале 1900–2000 м: снижение T2 DIST. (зеленый), снижение ГК, рост резистивиметрии.
- В интервале 2000–2100 м: устойчивые значения T2 DIST. (зеленый), умеренные ГК, умеренные резистивиметрия.
- В интервале 2100–2200 м: рост T2 DIST. (желтый), рост ГК, снижение резистивиметрии.
- В интервале 2200–2300 м: устойчивые значения T2 DIST. (желтый), умеренные ГК, умеренные резистивиметрия.
- В интервале 2300–2400 м: снижение T2 DIST. (зеленый), снижение ГК, рост резистивиметрии.
- В интервале 2400–2500 м: устойчивые значения T2 DIST. (зеленый), умеренные ГК, умеренные резистивиметрия.

KEYWORDS: каротажная диаграмма, ГК, ПС, T2 DIST, NMR, резистивиметрия, пористость, насыщенность, интерпретация, глубина, скважина
----


Courtesy Halliburton Energy Services ©1999, Halliburton Energy Services

Figure 6.8. Example of time domain analysis of Magnetic Resonance Imaging Log™ data incorporating resistivity measurements through a hydrocarbon-bearing shaly sand in the Gulf of Mexico, North America.

This log is from the same well as illustrated in Figures 6.3a and 6.3b.

Track 2 contains resistivity measurements from the induction log and the NMR permeability curve (MRIL PERM). Track 4 illustrates a differential spectrum (DIF SPEC) representing the different between T₂ distributions obtained during the long-Tw and short-Tw measurements. In subtracting the short-Tw distribution from the long-Tw distribution, the water signal cancels out and only the hydrocarbon signal remains in the differential spectrum. Track 5 displays the results of incorporating resistivity measurements with NMR measurements.

By combining resistivity measurements from the induction log, it becomes apparent that the moveable fluid (FFI) indicated in 6.3b is actually a combination of oil (shaded green) and water (shaded blue). This well was drilled with a water-based drilling fluid, and the free water indicated from XX160 to XX240 is nothing more than invaded mud filtrate. Because of the large proportion of irreducible fluid (BVI) and high NMR permeability, this formation is likely at irreducible water saturation (Sair) and would produce water free.
<!-- page 125 -->

<!-- page 126 -->
7

Asquith, G., and D. Krygowski, 2004, Log Interpretation, in G. Asquith and D. Krygowski, Basic Well Log Analysis: AAPG Methods in Exploration 16, p. 115-135.

# Log Interpretation

## GENERAL

As shown in the previous chapters, determining the porosity and true resistivity of a zone is the first step in converting the raw log data into estimated quantities of oil, gas, and water in a formation. These estimated quantities are used to evaluate a zone and to determine whether a well completion attempt is warranted. This chapter covers some of the different methods from which these estimates are derived. The methods discussed are: Archie water saturations ($S_w$ and $S_{xo}$) and the ratio method, quick-look technique, bulk volume water ($BVW$), and saturation crossplots (Pickett plots and Hingle plots). Determination of log-derived permeability ($K_e$) and shaly sand analysis are also discussed.

As important as this log-derived information is, however, it should not be applied without the inclusion of other data. This statement is, perhaps, obvious to the reader, but it can't be overemphasized. A geologist should always consider every item of relevant data, such as drill stem tests, sample shows, mud-log analysis, nearby production, etc., before making a decision to set pipe.

## SCANNING THE LOGS: A RECONNAISSANCE TECHNIQUE

It is an exceedingly rare log that contains more reservoir than nonreservoir, and when one is unfamiliar with an area or wants to broadly reconnoiter an area, a scanning technique that sorts reservoir from nonreservoir can be helpful, even with access to computer-aided processing. A good scanning technique not only identifies the reservoirs, but can also give the geologist hints as to potential pay and wet zones. Remember that in the interpretive process, the identification of wet zones is as important as the discovery of those containing hydrocarbons, because the com

comparison of the two helps clearly identify both the presence and amount of the hydrocarbons.

Figure 7.1 is a flowchart for one such scanning technique. Note that it has two paths, one for clastics and one for carbonates. In the clastic case, the resistivity log is the primary reconnaissance measurement because clastics tend to consist of reservoirs surrounded by shales of slowly varying resistivity. The changes in resistivity due to changes in fluid content of the reservoirs tend to stand out against this relatively constant background. On the carbonate path, on the other hand, formation resistivities tend to vary widely with changing rock types, and commonly there are few shales against which to measure changes. In this case, the porosity log is the primary reconnaissance measurement. By first finding the porous zones, those with the capacity to hold fluids (of any type) can be identified.

Figure 7.2 shows the details of a log interpretation, once zones of interest are identified, with references to the chapters in which the information is discussed.

## ARCHIE WATER SATURATIONS: $S_W$ AND $S_{XO}$

Water saturation ($S_w$) of a reservoir's uninvaded zone is calculated by the Archie (1942) formula:

$$
S_w = \left( \frac{a \times R_w}{R_t \times \phi^m} \right)^{\frac{1}{n}} \tag{7.1}
$$

where:

$S_w =$ water saturation of the uninvaded zone

$R_w =$ resistivity of formation water at formation temperature

$R_t =$ true formation resistivity (i.e., deep induction or deep laterolog corrected for invasion)

$\phi =$ porosity

$a =$ tortuosity factor (Table 1.1; Chapter 1)

115
<!-- page 127 -->
116

ASQUITH AND KRYGOWSKI

$m =$ cementation exponent (Table 1.1; Chapter 1)

$n =$ saturation exponent

The uninvaded zone's water saturation ($S_w$), determined by the Archie equation, is the most fundamental quantity used in log evaluation. But merely knowing a zone's water saturation ($S_w$) does not provide enough information to completely evaluate a zone's potential productivity. A geologist must also determine if:

- the water saturation is low enough for a water-free completion
the hydrocarbons are moveable
the zone is permeable
- there is an commercial volume of recoverable hydrocarbon reserves

Water saturation of a formation's flushed zone ($S_{xo}$) is also based on the Archie equation, but two variables are changed: mud filtrate resistivity ($R_{mf}$) in place of formation water resistivity ($R_w$) and flushed zone resistivity ($R_{xo}$) in place of uninvaded zone resistivity ($R_t$).

$$
S_{xo} = \left( \frac{a \times R_{mf}}{R_{xo} \times \phi^m} \right)^{\frac{1}{n}} \tag{7.2}
$$

where:

$S_{xo} =$ water saturation of the flushed zone

$R_{mf} =$ resistivity of the mud filtrate at formation temperature

$R_{xo} =$ shallow resistivity from a very shallow reading device, such as laterolog-8, microspherically focused log, or microlaterolog

$\phi =$ porosity

$a =$ tortuosity factor (Table 1.1; Chapter 1)

$m =$ cementation exponent (Table 1.1; Chapter 1)

$n =$ saturation exponent

Water saturation of the flushed zone ($S_{xo}$) can be used as an *indicator of hydrocarbon moveability*. For example, if the value of $S_{xo}$ is much larger than $S_w$, then hydrocarbons in the flushed zone have probably been moved or flushed out of the zone nearest the borehole by the invading drilling fluids ($R_{mf}$).

## Ratio Method

The ratio method identifies hydrocarbons from the difference between water saturations in the flushed zone ($S_{xo}$) and the uninvaded zone ($S_w$). When the uninvaded zone form of Archie's equation (Equation 7.1) is divided by the flushed zone form (Equation 7.2), the following results:

$$
\left( \frac{S_w}{S_{xo}} \right)^2 = \frac{R_{xo} / R_t}{R_{mf} / R_w} \tag{7.3}
$$

where:

$S_w =$ water saturation in the uninvaded zone

$S_{xo} =$ water saturation in the flushed zone

$R_{xo} =$ formation's shallow resistivity from a measurement such as laterolog-8, microspherically focused log, or microlaterolog

$R_t =$ true formation resistivity (i.e., deep induction or deep laterolog corrected for invasion)

$R_{mf} =$ resistivity of the mud filtrate at formation temperature

$R_w =$ resistivity of formation water at formation temperature

When $S_w$ is divided by $S_{xo}$, the formation factor ($F = a/\phi^m$) is cancelled out of the equation because the same formation factor is used to calculate both $S_w$ and $S_{xo}$. This can be very helpful in log analysis because, from the ratio $(R_{xo}/R_t)/(R_{mf}/R_w)$, the geologist can determine a value for both the moveable hydrocarbon index ($S_w/S_{xo}$) and water saturation by the ratio method without knowing porosity. Therefore, a geologist can still derive useful formation evaluation log parameters even though porosity logs are unavailable.

The moveable hydrocarbon index by the ratio method is:

$$
\frac{S_w}{S_{xo}} = \left( \frac{R_{xo} / R_t}{R_{mf} / R_w} \right)^{\frac{1}{2}} \tag{7.4}
$$

where:

$S_w/S_{xo} =$ moveable hydrocarbon index

$R_{xo} =$ shallow resistivity from measurements such as laterolog-8, microspherically focused log, or microlaterolog

$R_t =$ true formation resistivity (i.e., deep induction or deep laterolog corrected for invasion)

$R_{mf} =$ resistivity of mud filtrate at formation temperature

$R_w =$ resistivity of formation water at formation temperature

The cementation exponent ($n$) is assumed to be 2.0

If the ratio $S_w/S_{xo}$ is equal to or greater than 1.0, then hydrocarbons were not moved during invasion. This is true regardless of whether or not a formation contains hydrocarbons. Whenever the ratio $S_w/S_{xo}$ is less than 0.7 for sandstones or less than 0.6 for carbonates, moveable hydrocarbons are indicated (Schlumberger, 1972).

To determine water saturation by the ratio method
<!-- page 128 -->
Log Interpretation 117

$(S_{wr})$, you must know the flushed zone's water saturation. In the flushed zone of formations with moderate invasion and average residual hydrocarbon saturation, the following relationship normally works well:

$$S_{xo} = (S_w)^{\frac{1}{2}} \tag{7.5}$$

where:

$S_{xo}$ = water saturation of the flushed zone

$S_w$ = water saturation of the uninvaded zone

Substituting Equation 7.5 in Equation 7.4 and solving for $S_w$, the ratio method water saturation ($S_{wr}$) is:

$$S_{wr} = \left( \frac{R_{xo} / R_t}{R_{mf} / R_w} \right)^{\frac{5}{8}} \tag{7.6}$$

or:

$$S_{wr} = \left( \frac{R_{xo} / R_t}{R_{mf} / R_w} \right)^{0.625} \tag{7.7}$$

where:

$S_{wr}$ = moveable hydrocarbon index

$R_{xo}$ = shallow resistivity from measurements such as laterolog-8, microspherically focused log, or microlaterolog

$R_t$ = true formation resistivity (i.e., deep induction or deep laterolog corrected for invasion)

$R_{mf}$ = resistivity of mud filtrate at formation temperature

$R_w$ = resistivity of formation water at formation temperature

To use the ratio method in an interpretation process, the water saturation of the uninvaded zone should be calculated by both the Archie equation ($S_{wa}$) and the ratio method ($S_{wr}$). The following observations can be made:

1. If $S_{wa} \sim S_{wr}$, the assumption of a step-contact invasion profile is indicated to be correct, and all values determined ($S_w$, $R_t$, $R_{xo}$, and $d_t$) are correct.

2. If $S_{wa} > S_{wr}$, then the value for $R_{xo}/R_t$ is too low. $R_{xo}$ is too low because invasion is very shallow, or $R_t$ is too high because invasion is very deep. Also, a transition-type invasion profile might be indicated and $S_{wa}$ is considered a good value for the zone's actual water saturation.

3. If $S_{wa} < S_{wr}$, then the value for $R_{xo}/R_t$ is too high. $R_{xo}$ is too high because of the effect of adjacent, high-resistivity beds, or $R_t$ estimated from the deep resistivity measurement is too low because $R_{xo}$ is less than $R_t$. Also, an annulus-type invasion profile might be indicated and/or $S_{xo} < S_w^{1/5}$ (from Equation 7.5). In this case, a more accurate value for water saturation

can be estimated using the following equation (from Schlumberger, 1977):

$$(S_w)_{COR} = S_{wa} \times \left( \frac{S_{wa}}{S_{wr}} \right)^{0.25} \tag{7.8}$$

where:

$(S_w)_{COR}$ = corrected water saturation of the uninvaded zone

$S_{wa}$ = water saturation of the uninvaded zone (Archie method)

$S_{wr}$ = water saturation of the uninvaded zone (ratio method)

4. If $S_{wa} < S_{wr}$, the reservoir might be a carbonate with moldic (i.e., oomoldic, fossil-moldic, etc.) porosity and low permeability.

### QUICK-LOOK METHODS

#### General

Quick-look methods are helpful to the geologist because they provide flags, or indicators, that point to possible hydrocarbon zones requiring further investigation. The four quick-look methods discussed here are:

- $R_{xo}/R_t$
- apparent water resistivity ($R_{wa}$)
- conductivity-derived porosity
- Wet resistivity ($R_o$)

#### $R_{xo}/R_t$

The $R_{xo}/R_t$ technique relies on the comparison of the resistivity ratio, plotted as a curve on the log display, to the SP curve.

#### Procedure

1. Calculate the $R_{xo}/R_t$ ratio from the deep and shallow reading resistivity measurements;
2. Plot the ratio in the same track as the SP, and look for the following patterns.

#### Patterns to observe

1. In a shale, the ratio is relatively constant, like the SP, and usually close to 1.
2. In a water-bearing zone, the $R_{xo}/R_t$ ratio tracks the SP.
3. In a hydrocarbon-bearing zone, the $R_{xo}/R_t$ ratio moves away from the SP [a deflection to the right for the case of a normal (negative) SP].
<!-- page 129 -->
118

ASQUITH AND KRYGOWSKI

Basis for the technique

From Chapter 2, the equation relating the SP to fluid resistivities is:

$$SP = -K \times \log\left(\frac{R_{mf}}{R_w}\right) \tag{7.9}$$

In water-bearing zones:

$$R_{xo} = F \times R_{mf} \quad (\text{flushed zone}) \tag{7.10}$$

$$R_o = F \times R_w \quad (\text{uninvaded zone}) \tag{7.11}$$

Solving Equations 7.2 and 7.3 for $R_{mf}$ and $R_w$ respectively, and substituting the results in Equation 7.1 yields:

$$SP = -K \times \log\left(\frac{R_{xo}}{R_o}\right) \tag{7.12}$$

The $R_{xo}/R_o$ ratio is then related to the SP through a constant. Since $R_o$ is just a special case of $R_t$ ($R_o$ is the resistivity in the undisturbed, water-bearing zone), $R_t$ can be substituted for $R_o$ for the more general case. In water-bearing intervals, the $R_{xo}/R_t$ ratio parallels the response of the SP, and both curves move in the same direction from their respective baseline values. In a hydrocarbon-bearing interval, while the SP still responds to the differences in connate water and mud filtrate resistivities and moves accordingly, the $R_{xo}/R_t$ ratio decreases (because of increasing $R_t$) and the $R_{xo}/R_t$ curve moves away from the SP.

The $R_{xo}$ curve usually used for the ratio is derived from a shallow-reading measurement, such as a microspherically focused log or a microlaterolog. The $R_t$ curve is derived from a deep-reading measurement such as the deep induction log or deep laterolog. In practice, especially when the ratio is calculated and displayed as part of the logging job, the measurements are normally used without any environmental corrections being applied.

### Apparent water resistivity ($R_{wa}$)

The $R_{wa}$ technique relies on the comparison of calculated values of water resistivity between intervals in a well. This comparison can be made between different zones or within the same zone if a water-hydrocarbon contact is suspected in that zone. The assumption is that this lowest value of $R_{wa}$ is the closest approximation to the true formation water resistivity ($R_w$) and that values of $R_{wa}$ greater than the minimum value are indicative of the presence of hydrocarbons. A water saturation can also be calculated from the values of $R_{wa}$.

Procedure

1. Calculate an apparent water resistivity ($R_{wa}$) from the porosity and uninvaded zone resistivity measurements.
2. Look for the lowest value of $R_{wa}$ in a porous and permeable zone and compare it to the values of $R_{wa}$ calculated in the other zones.
3. If desired, an Archie water saturation can be calculated from the $R_{wa}$ values in the compared zones.

Patterns to observe

1. The zone with the lowest value of $R_{wa}$ is the most likely to be water-bearing, and the value of $R_{wa}$ is closest to the actual value of $R_w$ in the formation.
2. Zones with values of $R_{wa}$ greater than the minimum observed are likely to have some hydrocarbon saturation.

Interpretation pitfalls

The $R_w$ values in the zones that are compared are assumed to be the same.

In low-porosity zones (less than about 10% porosity), the $R_{wa}$ value is lower than the actual $R_w$ value.

Basis for the technique

Recall from Chapter 1 that

$$R_o = F \times R_w \tag{7.13}$$

and

$$F = \frac{a}{\phi^m} \tag{7.14}$$

Combining Equations 7.5 and 7.6, and solving for $R_w$ yields:

$$R_w = \frac{R_o \times \phi^m}{a} \tag{7.15}$$

From Equation 7.7 above, define apparent water resistivity ($R_{wa}$) as:

$$R_{wa} = \frac{R_t \times \phi^m}{a} \tag{7.16}$$

When a given zone is water bearing, $R_t$ reverts to the water-bearing resistivity ($R_o$) and $R_{wa}$ equals $R_w$. If the zone contains hydrocarbons, $R_t$ is greater than $R_o$, and $R_{wa}$ is greater than $R_w$. By comparing a number of zones (or different depths in the same zone, where a water-hydrocarbon contact is suspected) and assuming the zone with the lowest value of $R_{wa}$ is wet, the minimum value of $R_{wa}$ can be used as an estimate for the value of $R_w$ in all the zones being considered. If the zone with the minimum $R_{wa}$ value actually contains
<!-- page 130 -->
Log Interpretation

119

some hydrocarbons, then the other zones contain even more hydrocarbons than anticipated.

In practice, especially when calculated and displayed as a curve during a logging job, the following values are used for simplicity: $a = 1.0$, $m = 2.0$. The deep induction log or deep laterolog is used as $R_t$, usually without any environmental corrections. Porosity is usually derived from the sonic or density log using the proper matrix and fluid parameters for the formations to be encountered. If available in real time during logging, the neutron-density crossplot porosity should be used for the best estimate of porosity.

An Archie water saturation can also be calculated from the ratio of the $R_{wa}$ values.

$$S_w = \sqrt{\frac{R_{wa\ minimum}}{R_{wa\ zone}}} \tag{7.17}$$

where the cementation exponent ($n$) in the equation above is assumed to be 2.

A shortcut to the saturation calculation, used as a scanning aid, is:

- ($R_{wa\ zone}/R_{wa\ minimum}$) = 3 yields $S_w = 0.58$;
- ($R_{wa\ zone}/R_{wa\ minimum}$) = 4 yields $S_w = 0.50$;
- ($R_{wa\ zone}/R_{wa\ minimum}$) = 5 yields $S_w = 0.45$.

Where $a = 1.0$ and $m = 2.0$.

### Conductivity-derived porosity (also referred to as resistivity-porosity)

Although this technique originated with the use of the conductivity curve (Dresser Atlas, 1975), the conductivity curve is now rarely presented on log displays, and the technique is described here using the resistivity measurement.

This technique calculates a porosity from Archie's equation, using the form of the equation for water-bearing zones ($S_w = 1$). The porosity values are generated as a curve and are normally displayed in the same track as the SP, scaled from high porosity values on the left to low porosity values on the right.

### Procedure

1. Calculate the porosity from Archie's equation (assuming $S_w = 1.0$), using the uninvaded zone resistivity measurement.
2. Compare the curve values and the relative position of the curve in porous and permeable zones.
3. If desired, an Archie water saturation can be calculated by comparing the conductivity-derived porosity

ty to porosity from one of the porosity measurements (sonic, density, or neutron).

### Patterns to observe

1. In water-bearing zones, the conductivity-derived porosity is high and approximately equal to the true formation porosity.
2. In zones that contain hydrocarbons, the conductivity-derived porosity is low, lower than the true formation porosity.

### Interpretation pitfalls

The choice of an incorrect value for $R_w$ would change the value of conductivity-derived porosity, and might make its comparison to true formation porosity inaccurate. It would not, however, change the results of comparison of the curve values in different zones.

### Basis for the technique

From Chapter 1, Archie's equation can be solved for porosity:

$$\phi = \left(\frac{a \times R_w}{R_t \times S_w^n}\right)^{\frac{1}{m}} \tag{7.18}$$

If the water-bearing case is considered, where $S_w = 1$, the equation reduces to:

$$\phi = \left(\frac{a \times R_w}{R_t}\right)^{\frac{1}{m}} \tag{7.19}$$

By using the form of the equation above (7.19), the water-filled porosity is determined. Where the formation is actually water filled, $R_t$ reverts to the water-bearing resistivity ($R_o$). The porosity calculated from this equation is close to the actual formation porosity, assuming that the parameters in the equation are close to the actual formation parameters. When the formation contains hydrocarbons, $R_t$ is greater than $R_o$, and the calculated porosity is less than the actual formation porosity.

Traditionally this curve has been plotted in the same log track as the SP curve, and its movement compared to the SP. It can also be plotted in the same track as a porosity curve from one of the porosity tools, where decreases in conductivity-derived porosity with respect to the porosity curve indicate the presence of hydrocarbons.

Water saturation can be estimated by the following equation:

$$S_w = \frac{\phi_{conductivity}}{\phi_{actual}} \tag{7.20}$$
<!-- page 131 -->
120

ASQUITH AND KRYGOWSKI

### Wet resistivity ($R_o$)

The wet-resistivity curve ($R_o$) is one of the oldest quick-look techniques. Unlike the other curves, which tend to be compared to the SP curve, it is plotted as an overlay on the resistivity curve.

### Procedure

1. Calculate $R_o$ from the porosity and an estimate of formation water resistivity ($R_w$).
2. Plot $R_o$ as a curve at the same scale as the resistivity curves and compare the values to the value of the deep-resistivity measurement.
3. If desired, an Archie water saturation can be calculated in any zone from the values of $R_o$ and the deep resistivity measurement.

### Patterns to observe

1. In water-bearing zones, $R_o$ and the deep resistivity should overlay.
2. In hydrocarbon-bearing zones, the deep resistivity is higher than $R_o$, with the separation increasing with increasing hydrocarbon saturation.

### Interpretation pitfalls

If the value of $R_w$ chosen to calculate $R_o$ is incorrect, the curves would not align in water-bearing zones.

### Basis for the technique

Recall from chapter 1 that:

$$R_o = F \times R_w = \frac{a \times R_w}{\phi^m} \tag{7.21}$$

$R_o$ is then calculated from a porosity measurement, usually the sonic or density, with an estimate of $R_w$, $a$, and $m$. The curve can be generated and displayed during the logging job.

### BULK VOLUME WATER

The product of a formation's water saturation ($S_w$) and its porosity ($\phi$) is the bulk volume of water ($BVW$).

$$BVW = S_w \times \phi \tag{7.22}$$

where:

$BVW$ = bulk volume water

$S_w$ = water saturation of uninvaded zone

$\phi$ = porosity

If values for bulk volume water, calculated at several depths in a formation, are constant or very close to

constant, they indicate that the zone is of a single rock type and at irreducible water saturation ($S_{w\ irr}$). When a zone is at irreducible water saturation, water in the uninvaded zone ($S_w$) does not move because it is held on grains by capillary pressure. Therefore, hydrocarbon production from a zone at irreducible water saturation should be water free (Morris and Biggs, 1967).

A formation not at irreducible water saturation ($S_{w\ irr}$) exhibits wide variations in bulk volume water values. The Buckles plot (Buckles, 1965) is a graph of porosity ($\phi$) versus $S_w$. Points of equal $BVW$ form hyperbolic curves across this plot. Figure 7.3 illustrates Buckles plots using data from three wells in the Ordovician Red River B-zone, Beaver Creek Field, North Dakota. If $BVW$ is plotted using data from a formation at irreducible water saturation, the points fall along a single hyperbolic curve (Figure 7.3a). If the data come from reservoirs with higher percentages of produced water, the points are more scattered (Figures 7.3b and 7.3c).

Because the amount of water a formation can hold by capillary pressure increases with decreasing grain size, the bulk volume water also increases with decreasing grain size. Table 7.1 illustrates the relationship of bulk volume water values to decreasing grain size and lithology.

Table 7.1. Bulk volume water ($BVW$) as a function of grain size and lithology. A comparative chart.

|  Lithology | Grain Size (millimeters) | Bulk Volume Water ($BVW$)  |
| --- | --- | --- |
|  *Clastics*  |   |   |
|  Coarse | 1.0 to 0.5 | 0.02 to 0.025  |
|  Medium | 0.5 to 0.25 | 0.025 to 0.035  |
|  Fine | 0.25 to 0.125 | 0.035 to 0.05  |
|  Very Fine | 0.125 to 0.062 | 0.05 to 0.07  |
|  Silt | < 0.062 | 0.07 to 0.09  |
|  *Carbonates*  |   |   |
|  Vuggy |   | 0.005 to 0.015  |
|  Vuggy and intercrystalline (intergranular) |   | 0.015 to 0.025  |
|  Intercrystalline |   | 0.025 to 0.04  |
|  Chalky |   | 0.05  |

The bulk volume water values for carbonates should be used only as a very general guide to different types of porosity.
<!-- page 132 -->
Log Interpretation 121

# SATURATION CROSSPLOTS

Saturation crossplots, also called resistivity-porosity crossplots (or specifically, Pickett plots and Hingle plots) are similar to the porosity crossplots discussed in Chapter 4. They are x-y plots of log data from which quantities of interest are derived; in this case, that quantity is water saturation ($S_w$). Both the Pickett and Hingle methods are essentially graphical solutions to the Archie saturation equation. They were created before the use of computers to aid log interpretation. These techniques minimize the number of calculations that must be done and aid the comparison of potentially productive zones. With the advent of early (mostly nongraphic) log-interpretation software, their use declined, but this decline was reversed as people realized the power of the techniques to use the ability of the human mind to recognize patterns in data. These techniques are currently regarded as necessary components of full-functioned computer-based log-interpretation systems.

## Pickett Crossplot Method

The Pickett plot (Pickett, 1966, 1973) is one of the simplest and most effective crossplot methods in use. This technique estimates water saturation and can also help determine:

- formation water resistivity ($R_w$)
- cementation factor ($m$)
- matrix parameters for sonic and density logs ($\Delta t_{ma}$ and $\rho_{ma}$)

The Pickett method is based on the observation that true resistivity ($R_t$) is a function of porosity ($\phi$), water saturation ($S_w$), and cementation exponent ($m$). It is actually a graphical solution of Archie's equation in terms of resistivity. Archie's equation (Equation 7.1) is solved for resistivity:

$$R_t = \frac{a \times R_o}{\phi^m \times S_w^n} \tag{7.23}$$

Taking the logarithm of the equation produces:

$$\log(R_t) = \log(a \times R_w) - m \log(\phi) - n \log(S_w) \tag{7.24}$$

If the zone is water-bearing, $S_w = 1$, $\log(S_w) = 0$, and the equation reduces to:

$$\log(R_t) = \log(a \times R_w) - m \log(\phi) \tag{7.25}$$

This form of the equation ($y = b + mx$) indicates that by plotting $R_t$ on the y-axis (on a logarithmic scale) against porosity ($\phi$) on the x-axis (on a logarith-

mic scale), one can determine the product ($a \times R_w$) from intercept of the line (b), and the cementation exponent ($m$) from the slope of the line ($m$). In practice, the resistivity ($R_t$) is usually plotted on the x-axis and the porosity ($\phi$) on the y-axis (Figure 7.4). This convention stems from the availability of full-logarithmic graph paper (both scales logarithmic) at the time Pickett developed the technique. The best format to use (for the best data resolution) is two decades for porosity (0.01 to 1.0, or 1% to 100%) and three decades for the resistivity (0.1 to 100, or 1 to 1000). The only 2-by-3 full-logarithmic paper available was constructed with 2 decades on the y-axis and 3 decades on the x-axis so the plot was modified to fit the paper (G. R. Pickett, personal communication).

Using the convention driven by graph-paper availability, the equation becomes:

$$\log(\phi) = \log(a \times R_w) - \frac{1}{m} \log(R_t) - n \log(S_w) \tag{7.26}$$

Plotting a mixture of water-bearing and hydrocarbon-bearing points on a Pickett plot results in the following attributes (as shown in Figure 7.4):

- Water-bearing points of different porosities plot along a straight line with a slope of ($-1/m$) and an intercept (at porosity = 1.0) of ($a \times R_w$). From this line, the cementation exponent ($m$) can be determined, and if the tortuosity factor ($a$) is known (or can be estimated), $R_w$ can be predicted. This is the water-bearing, or $R_o$, line.
- Hydrocarbon-bearing points lie away from the line, moved horizontally to the right from the water-bearing line by their increased resistivity. The horizontal distance of a point from the water-bearing line depends on the water saturation ($S_w$) of that point. If the saturation exponent ($n$) is known (or can be estimated), the water saturation can be determined. Lines of constant water saturation lie parallel to the water-bearing line.

The power in the Pickett plot is that water resistivity ($R_w$) and cementation exponent ($m$) can be estimated from the data, rather than having to be derived from local knowledge or from expensive core measurements.

Although porosity is now normally plotted on the Pickett plot, Pickett originally used two other quantities:

($\rho_b - \rho_{ma}$) instead of the density porosity

where:

$\rho_b$ = formation bulk density (from the log)

$\rho_{ma}$ = formation matrix density
<!-- page 133 -->
122

ASQUITH AND KRYGOWSKI

and:

$$(\Delta t - \Delta t_{ma})$$ instead of the sonic porosity where:

$$\Delta t =$$ formation sonic travel time (from the log)

$$\Delta t_{ma} =$$ formation matrix travel time

Both quantities are the numerators in porosity equations $$(\rho_b - \rho_{ma})$$ from the density porosity equation (Chapter 4, Equation 4.7), and $$(\Delta t - \Delta t_{ma})$$ from the Wyllie time-average sonic equation (Chapter 4, Equation 4.1). The quantities are plotting shortcuts to avoid the calculation of porosity, but they serve another purpose as well. If there is a range of porosities in the zones defining the water-bearing line on the Pickett plot, and if the matrix value is chosen correctly, the line is straight. If the chosen matrix value is either too high or too low, the line is curved. Thus, with a spread of good data in the water-bearing zone, the proper matrix value can be chosen by trial and error by modifying the matrix value until the water-bearing line is straight and not curved.

The water saturation of a point plotting away from the water-bearing line can be determined by the equation:

$$S_w = \left(\frac{R_o}{R_t}\right)^{\frac{1}{n}} \tag{7.27}$$

In practice, this means reading the resistivity of the point $$(R_t)$$ and the resistivity of the water-bearing line $$(R_o)$$ at the same porosity value as the point, estimating a value for saturation exponent (n) and making the calculation.

The table below can be used to draw saturation lines on a Pickett plot, as a reference. The technique is:

- At some value of porosity (0.10 is often convenient), note the resistivity value of the $$R_o$$ line.
- Multiply that resistivity value by the factors below, and plot those values on the Pickett plot at the same porosity.
- Draw the saturation lines parallel to the water-bearing line, with each line going through the calculated points.
- Those parallel lines can be labeled with the value of water saturation shown. Note that the lines are for a saturation exponent (n) of 2.0.

In its fullest use, then, the Pickett plot can be used to determine formation water resistivity ($$R_w$$), cementation exponent (m), and formation matrix values ($$\rho_{ma}$$ or $$\Delta t_{ma}$$). As expected, there are assumptions to the interpretation. The prime assumption is that in the zones being compared, all the parameters (matrix value, a, m, n, and $$R_w$$) do not change.

Table 7.2. Factors for positioning water-saturation lines on Pickett and Hingle plots.

|  Multiplier | $$S_w$$ (for n = 2.0)  |
| --- | --- |
|  1.56 | 0.80  |
|  2.04 | 0.70  |
|  2.78 | 0.60  |
|  4 | 0.50  |
|  6.25 | 0.40  |
|  11.11 | 0.30  |
|  25 | 0.20  |

### Hingle Crossplot Method

The oldest of the resistivity-porosity crossplot methods that can be used to determine water saturation ($$S_w$$) is the Hingle (1959) plot. As in other crossplot techniques, a significant benefit of Hingle's technique is that a value for water saturation ($$S_w$$) can be determined even if matrix properties ($$\rho_{ma}$$ or $$\Delta t_{ma}$$) of a reservoir are unknown. This is also true if a reservoir's water resistivity ($$R_w$$) is unknown.

As with the Pickett plot, the Hingle plot seeks to plot resistivity against porosity. Plotting resistivity against porosity on linear scales produces a family of nonlinear trends. By solving Archie's equation (Equation 7.1) in the following form, the nonlinear trends become straight lines (Bassiouni, 1994):

$$\left(\frac{a}{R_t}\right)^{\frac{1}{m}} = \left(\frac{S_w^n}{R_w}\right)^{\frac{1}{m}} \times \phi \tag{7.28}$$

While porosity is plotted on a linear scale, the resistivity is plotted on a very nonlinear scale. In practice, the resistivity is plotted on a grid that has been constructed for specific values of tortuosity factor (a) and cementation exponent (m). The grid constructed using a = 1.0 and m = 2.0 is usually used for sandstones (Figure 7.5), and the grid constructed using a = 0.62 and m = 2.15 is used for carbonates (Figure 7.6). Using the constructed grids, resistivity values can be plotted directly on the graph without the need for any calculations.

Plotting a mixture of water-bearing and hydrocarbon-bearing points on a Hingle plot results in the following attributes (as shown in Figure 7.7):

- Water-bearing points of different porosities plot along a straight line. The x-intercept of the line (where conductivity is zero and resistivity is infinite) occurs at the point where porosity is
<!-- page 134 -->
Log Interpretation

123

zero. If the bulk density or acoustic travel time of the formation, instead of the porosity, is plotted along the x-axis, the x-intercept predicts the matrix value (matrix density or matrix travel time) of the formation. The line extends to the northeast quadrant (i.e., upper right) from its x-intercept.

- Hydrocarbon-bearing points lie below the line of 100% water saturation, moved downward from the water-bearing line by their increased resistivity. The vertical distance from a point to the water-bearing line depends on the water saturation ($S_w$) of that point. If the saturation exponent ($n$) is known (or can be estimated), the water saturation can be determined. Lines of decreasing water saturation radiate from the x-axis intercept and spread like a fan toward the right side of the chart.

As with the Pickett plot, the Hingle plot allows the interpreter to predict some of the parameters from the logs rather than estimating them by other methods. The formation water resistivity ($R_w$) can be estimated by choosing any point along the water-bearing line. The point's resistivity ($R_o$) and porosity can be read from the plot, and values of tortuosity factor ($a$) and cementation exponent ($m$) are assumed based on the chart that is chosen. Formation water resistivity is then:

$$R_w = \frac{R_o \times \phi^m}{a} \tag{7.29}$$

By plotting the bulk density ($\rho_b$) or sonic travel time ($\Delta t$) values on the x-axis, rather than the porosity, the matrix density or matrix travel time ($\rho_{ma}$ or $\Delta t_{ma}$) can be estimated. If there is a sufficient range of porosities used to determine the water-bearing line, the line can be extrapolated to the zero-conductivity value (the bottom of the chart). The value of this intercept is the matrix value for the porosity equation. On Figure 7.5 or Figure 7.6, the placement of the zero porosity point is arbitrary. If porosity is plotted on the x-axis, setting the zero porosity point at the left side of the plot makes the most sense. If $\rho_b$ or $\Delta t$ is used, the anticipated zero porosity point (the anticipated matrix value) could be displaced from the lower left corner if the matrix value is different than the expected matrix value. Regardless of the values used on the x-axis (porosity, $\rho_b$, or $\Delta t$), the values increase from left to right.

The water saturation of a point plotting away from the water-bearing line can be determined by Equation 7.26. In practice, this means reading the resistivity of the point ($R_t$) and the resistivity of the water-bearing line ($R_o$) at the same porosity value as the point, esti-

mating a value for saturation exponent ($n$), and making the calculation.

Table 7.2, previously used for the Pickett plot, can be used to draw saturation lines on a Hingle plot. The technique is:

- At some value of porosity (0.10 is often convenient), note the resistivity value of the $R_o$ line.
- Multiply that resistivity value by the factors in Table 7.2, and plot those values on the Hingle plot at the same porosity.
- Draw the saturation lines to intersect the water-bearing line at the zero porosity point on the x-axis, with each line going through the calculated points.
- Those lines can be labeled with the value of water saturation shown. Note that the lines are for a saturation exponent ($n$) of 2.0.

In routine analyses, many people favor one of the crossplots over the other, as a matter of personal preference or experience. Bassiouni (1994), however, describes an iterative technique using both plots to refine the estimates of the matrix values and cementation exponents in areas where both are unknown. Table 7.3 lists advantages and limitations of both plots.

### PERMEABILITY FROM LOGS

Log-derived permeability formulas are only valid for estimating permeability in formations at irreducible water saturation (Schlumberger, 1977). When a geologist evaluates a formation by using log-derived permeability formulas, the permeability values, if possible, should be compared with values of nearby producing wells from the same formation. Productivity estimates can be based on log-derived permeabilities if the formation evaluated is compared with both good and poor production histories in these nearby wells. By using comparisons of log-derived permeabilities from several wells, a geologist is not using an absolute value for log-derived permeability.

Four methods for calculating log-derived permeability are discussed here. Before these formulas can be applied, a geologist must first determine whether or not a formation is at irreducible water saturation. Whether or not a formation is at irreducible water saturation depends upon bulk volume water values ($BVW = S_w \times \phi$). When the bulk volume water values of a formation are constant (Figure 7.3a), the zone is at irreducible water saturation. If the values are not constant, a zone is not at irreducible water saturation (Figures 7.3b and 7.3c), and the estimates of permeability are suspect.
<!-- page 135 -->
124

ASQUITH AND KRYGOWSKI

Table 7.3. Advantages and Limitations of Pickett and Hingle plots (after Bassiouni, 1994).

|   | *Pickett plots* | *Hingle plots*  |
| --- | --- | --- |
|  Advantages | Water saturation can be predicted without prior knowledge of $R_w$, $a$, or $m$. $R_w$ is directly predicted (if tortuosity factor ($a$) is known or estimated) from the intercept of the water-bearing line at a porosity of 1 ($\phi = 100\%$). Cementation exponent ($m$) is directly predicted from the slope of the water-bearing line. When using the plot by hand, the graph paper to be used (full logarithmic) is readily available. | Water saturation can be predicted without prior knowledge of $R_w$, $\rho_{ma}$ or $\Delta t_{ma}$, $\rho_{ma}$ or $\Delta t_{ma}$ can be directly predicted from the intercept of the water-bearing line at a conductivity of zero (a resistivity of infinity).  |
|  Limitations | Values for $\rho_{ma}$ and $\Delta t_{ma}$ must be assumed (although in cases with a wide range of porosities in the water-bearing zone, the matrix values can be estimated from the water-bearing line). | Values for tortuosity factor ($a$) and cementation exponent ($m$) must be assumed. To use the plot, the resistivity parameter has to be calculated or a special graph paper used.  |
|  Limitations for both techniques | A wide range of porosity must be present to positively determine a water-bearing line. Formation lithology and water resistivity must be constant over the intervals compared in the plot.  |   |

Table 7.4. Data for use with Pickett plot (Figure 7.4) and Hingle plot (Figure 7.7). Morrow Sandstone, Cimarron County, Oklahoma.

|  Zone number | Depth (ft) | $\rho_b$ (g/cm³) | $\phi_D$ (decimal) | $R_t$ (ohm-m)  |
| --- | --- | --- | --- | --- |
|  1 | 4400 | 2.38 | 0.163 | 1.7  |
|  2 | 4402 | 2.44 | 0.127 | 2.1  |
|  3 | 4410 | 2.35 | 0.181 | 1.3  |
|  4 | 4414 | 2.42 | 0.139 | 1.6  |
|  5 | 4426 | 2.42 | 0.139 | 1.8  |
|  6 | 4430 | 2.33 | 0.194 | 1.0  |
|  7 | 4438 | 2.30 | 0.212 | 0.9  |
|  8 | 4536 | 2.30 | 0.212 | 40  |
|  9 | 4540 | 2.30 | 0.212 | 45  |
|  10 | 4546 | 2.30 | 0.212 | 40  |

## Wyllie and Rose (1950)

This method for determining permeability utilizes a chart (Figure 7.8) or the two forms of the following formula:

$$
K = \left( 250 \times \frac{\phi^3}{S_{\text{wirr}}} \right)^2 \text{ (medium-gravity oils)} \tag{7.30}
$$

$$
K = \left( 79 \times \frac{\phi^3}{S_{\text{wirr}}} \right)^2 \text{ dry gas)} \tag{7.31}
$$

where:

$K =$ permeability in millidarcys

$\phi =$ porosity

$S_{\text{wirr}} =$ water saturation ($S_w$) of a zone at irreducible water saturation

## Timur (1968)

$$
K = \left( \frac{93 \times \phi^{2.2}}{S_{\text{wirr}}} \right)^2 \tag{7.32}
$$

## Coates and Dumanoir (1973)

A more complex method for calculating permeability is the Coates and Dumanoir (1973) formula. Unlike the Wyllie and Rose (1950) formulas, hydrocarbon density is explicitly part of the equation, instead of being indirectly accounted for by changing a constant. The following data are required to calculate permeability by the Coates and Dumanoir formula.

$R_w =$ formation water resistivity at formation temperature

$R_{t\,irr} =$ true formation resistivity from a formation at irreducible water saturation
<!-- page 136 -->
Log Interpretation

125

$\rho_{h} =$ hydrocarbon density in $\mathrm{g / cm^3}$

$\phi =$ porosity

A first step in the Coates and Dumanoir permeability formula is calculation of values for two constants: $C$ and $W$.

$$
C = 23 + 465 \times \rho_{h} - 188 \times \rho_{h}^{2} \tag{7.33}
$$

where:

$C =$ constant in Coates and Dumanoir permeability formula

$\rho_{h} =$ hydrocarbon density in $\mathrm{g / cm^3}$

$$
W = \left\{(3.75 - \phi) + \left[ \frac{(\log(R_{w} / R_{t \text{ irr}}) + 2.2)^{2}}{2.0} \right] \right\}^{\frac{1}{2}} \tag{7.34}
$$

where:

$W =$ constant in Coates and Dumanoir permeability formula

$\phi =$ porosity

$R_{w} =$ formation water resistivity at formation temperature

$R_{t \text{ irr}} =$ deep resistivity from a zone at irreducible water saturation ($S_{w \text{ irr}}$)

Once determined, the constants $C$ and $W$ can be used to calculate permeability.

$$
K = \left[ \frac{C \times \phi^{2W}}{W^{4} \times (R_{w} / R_{t \text{ irr}})} \right]^{2} \tag{7.35}
$$

where:

$K =$ permeability in millidarcys (md)

$C =$ constant based on hydrocarbon density

$W =$ constant

$\phi =$ porosity

$R_{t \text{ irr}} =$ deep resistivity from a zone at irreducible water saturation ($S_{w \text{ irr}}$)

$R_{w} =$ formation water resistivity at formation temperature

## SHALY SAND ANALYSIS

Not long after the work of Archie and others in devising a method to quantify water saturation from logs, it became clear that there were limitations to the method, especially in formations containing shale and/or clay and commonly referred to as *shaly sands*. The early literature tended to refer to the formations as containing *shale*, and a number of modifications were made to Archie’s equation using shale volume (among

other parameters) to account for those effects. As our understanding of geological processes matured, it became understood that *shale* and *clay* are different and that shaly sands are usually not just sands with shales mixed in but sands that contain clays. These clays could be very different from the clays present in the shales near those sands of interest. Again, the literature and our interpretive techniques commonly use the terms *shale volume* and *clay volume* interchangeably. Most of the shaly sand techniques developed over the years concern themselves with shale volume, but a few, notably the Waxman-Smits and dual water methods, seek to use the electrical properties of the clays in the formations to predict an accurate water saturation.

Beginning in the late 1960s, the work of Waxman and Smits (1968) and Waxman and Thomas (1974) helped to better understand the physical causes of the responses of logging measurements to shaly sands and to develop interpretive models to better approximate the physical reality of formations. Clavier et al. (1977) built on the work of Waxman and his colleagues with the introduction of the dual water model for the determination of water saturation. The dual water model postulates two different types of water in a shaly formation, a immovable water layer next to the clay surfaces (bound water) and movable water that can be displaced by hydrocarbons (free water). This technique, while more complex in its use, continues to gain popularity because of its closer approximation to the responses of shaly sands in a wide variety of conditions.

The presence of shale or clay minerals in a reservoir can cause erroneous values for water saturation and porosity derived from logs. These erroneous values are not limited to sandstones but also occur in limestones and dolomites.

Essentially all measurements, then, are affected in some way by the presence of clays and/or shales. Hilchie (1978) notes that the most significant effect of shale in a formation is to reduce the resistivity contrast between oil or gas, and water. The net result is that if enough shale is present in a reservoir, it may be very difficult, or perhaps impossible, to determine if a zone is productive. Hilchie (1978) suggests that for shale to significantly affect log-derived water saturations, shale content must be greater than 10 to \(15\%\).

Remember that all shaly sandstone formulas reduce the water saturation value from the value that would be calculated if shale effect were ignored. However, this lowering of water saturation can be a problem in log evaluation, because, if a geologist overestimates shale content, a water-bearing zone might appear to be a hydrocarbon-bearing zone.
<!-- page 137 -->
126

ASQUITH AND KRYGOWSKI

Table 7.5. Effects of clays and shales on logging measurements.

|  Measurement | Effect  |
| --- | --- |
|  Spontaneous potential, SP | SP is decreased in magnitude with respect to the shale baseline.  |
|  Gamma ray | Increased radioactivity is apparent as less movement away from the nearby shale values than an equivalent clean sand.  |
|  Sonic | Sonic porosity is higher than the actual formation porosity due to the higher travel time of the clays/shales.  |
|  Neutron | Neutron porosity is higher than the actual formation porosity due to the water that is part of the clay structure and is adsorbed on the clay surfaces.  |
|  Density | Density porosity is higher than the actual formation porosity due to the generally lower matrix densities of most clay minerals. If the matrix density of the clay is close to that of the formation matrix, there is little or no effect on porosity.  |
|  Resistivity | Resistivity is less than that in an equivalent clean formation due to the conductivity of the clay. This produces a calculated water saturation greater than the actual formation water saturation. (Archie's equation assumes that all conductivity is from the formation water and that the formation matrix is completely nonconducting.)  |

### Determining Shale/Clay Volume

The first step in shaly sand analysis is to determine the volume of shale. There are several techniques available, the most common being those from the SP, gamma ray, and neutron-density crossplot. Perhaps the most widely used log is the gamma ray, in part because there are several (empirical) relationships between the response of the measurement and shale or clay volume (Chapter 3).

Once shale volume, $V_{shale}$, is determined, the available porosity logs can be corrected for shale effects:

Sonic log (Dresser Atlas, 1979):

$$\phi_{Se} = \left( \frac{\Delta t_{log} - \Delta t_{ma}}{\Delta t_{fl} - \Delta t_{ma}} \times \frac{100}{\Delta t_{sh}} \right) - V_{shale} \left( \frac{\Delta t_{sh} - \Delta t_{ma}}{\Delta t_{fl} - \Delta t_{ma}} \right) \quad 7.36$$

or (from Dewan, 1983):

$$\phi_{Se} = \phi_S - V_{shale} \times \phi_{Ssh} \quad 7.37$$

where:

$\phi_{Se}$ = effective (shale-corrected) sonic porosity

$\phi_S$ = sonic porosity

$\phi_{Ssh}$ = sonic porosity in a nearby shale

$V_{shale}$ = shale volume

$\Delta t_{log}$ = interval transit time of the formation (from the sonic log)

$\Delta t_{ma}$ = matrix interval transit time

$\Delta t_{fl}$ = fluid interval transit time

$\Delta t_{sh}$ = interval transit time in a nearby shale

The neutron and density logs (Schlumberger, 1975):

$$\phi_{Ne} = \phi_N - \left[ \left( \frac{\phi_{Nshale}}{0.45} \right) \times 0.03 \times V_{shale} \right] \quad 7.38$$

$$\phi_{De} = \phi_D - \left[ \left( \frac{\phi_{Nshale}}{0.45} \right) \times 0.13 \times V_{shale} \right] \quad 7.39$$

or, from Dewan (1983):

$$\phi_{Ne} = \phi_N - V_{shale} \times \phi_{Nsh} \quad 7.40$$

$$\phi_{De} = \phi_D - V_{shale} \times \phi_{Dsh} \quad 7.41$$

and, using either of the single porosity measurement pairs above:

$$\phi_{ND} = \sqrt{\frac{\phi_{Ne}^2 + \phi_{De}^2}{2}} \quad 7.42$$

where:

$\phi_{ND}$ = neutron-density shale-corrected porosity

$\phi_N$ = neutron porosity

$\phi_{Ne}$ = shale-corrected neutron porosity

$\phi_D$ = density porosity

$\phi_{De}$ = shale-corrected density porosity

$\phi_{Nsh}$ = neutron porosity of a nearby shale
<!-- page 138 -->
Log Interpretation

127

$\phi_{Dsh} =$ density porosity of a nearby shale

$V_{shale} =$ shale volume

### Determining Water Saturation

After the shale-corrected porosity has been determined, the water saturation can be calculated. A variety of techniques are briefly introduced below, but the methodology for their use is beyond the scope of this book and is not detailed. The reader is referred to Asquith (1991), Bassiouni (1994), or Dewan (1983) for details of usage of the individual techniques.

A technique popular in the 1950s was the automatic compensation technique (Dewan, 1983). It used the resistivity and sonic logs with Archie's equation. Since the presence of shale caused the porosity ($\phi_S$) to read too high and the resistivity ($R_t$) to read too low, one compensated for the other in the saturation equation:

$$S_w \approx 0.9 \frac{\sqrt{R_w / R_t}}{\phi_S} \tag{7.43}$$

In the 1960s, with the advent of the density log, the dispersed-clay model gained popularity (Dewan, 1983). In this model, the density was assumed to respond only to the liquid-filled porosity, while the sonic was affected by the clays with the difference ($q$) being the fraction of the intergranular space filled with clay:

$$q = \frac{\phi_S - \phi_D}{\phi_S} \tag{7.44}$$

and the saturation given by:

$$S_w = \frac{\left[ \sqrt{\frac{0.8 \times R_w}{\phi_S^2 \times R_t} + \left(\frac{q}{2}\right)^2} - \frac{q}{2} \right]}{(1-q)} \tag{7.45}$$

A number of $V_{shale}$-based methods became popular in the late 1960s and 1970s, and many of these are still being used. These include:

Fertl, 1975:

$$S_w = \frac{1}{\phi} \times \left[ \sqrt{\frac{R_w}{R_t} + \left(\frac{a \times V_{shale}}{2}\right)^2} - \frac{a \times V_{shale}}{2} \right] \tag{7.46}$$

where:

$a = 0.25$ in the Gulf Coast and $a = 0.35$ in the Rocky Mountains.

Schlumberger, 1975:

$$S_w = \frac{\sqrt{\left(\frac{V_{shale}}{R_{sh}}\right)^2 + \frac{\phi^2}{0.2 \times R_w \times R_t \times (1 - V_{shale})} - \frac{V_{shale}}{R_{sh}}}}{\frac{\phi^2}{0.4 \times R_w \times (1 - V_{shale})}} \tag{7.47}$$

Simandoux, 1963:

$$S_w = \left(\frac{0.4 \times R_w}{\phi^2}\right) \times \left[ \sqrt{\left(\frac{V_{shale}}{R_{sh}}\right)^2 + \frac{5 \times \phi^2}{R_t \times R_w}} - \frac{V_{shale}}{R_{sh}} \right] \tag{7.48}$$

The dual water method is perhaps the most widely used of the techniques that go beyond the shale-volume methods. This method is more fully described in Dewan (1983) and Bassiouni (1994). It faces the reality that there is no way to measure cation-exchange capacity (CEC) directly from logs and that CEC measurements on cores are rare, so $V_{shale}$ methods are used to correct porosity for clay content and to calculate the bound-water saturation ($S_{wb}$). The bound-water and free-water resistivities are determined from nearby shales and clean sands, and the apparent water resistivity ($R_{wa}$) in the sand of interest is calculated.

The total (shale-corrected) water saturation of the formation is:

$$S_{wt} = b + \sqrt{b^2 + \frac{R_w}{R_{wa}}} \tag{7.49}$$

where:

$$b = \frac{S_{wb}(1 - (R_w / R_b))}{2} \tag{7.50}$$

The effective water saturation of the formation is:

$$S_{wa} = \frac{S_{wt} - S_{wb}}{1 - S_{wb}} \tag{7.51}$$

and the volumetric fraction of hydrocarbons is:

$$\phi_h = \phi_t(1 - S_{wt}) \tag{7.52}$$

where $\phi_t =$ total porosity (from the neutron and density).

A major problem encountered in shaly sand analysis is determining a resistivity value for shale/clay in a formation. The percentage of shale is not the critical factor, rather it is clay's cation-exchange capacity (Hilchie, 1978) because cation-exchange capacity greatly affects resistivity of the clay. Kaolinite and
<!-- page 139 -->
128

ASQUITH AND KRYGOWSKI

chlorite have extremely low cation-exchange values; illite and montmorillonite have high cation-exchange values. Therefore, montmorillonite and illite decrease resistivity much more than kaolinite and chlorite. In shaly sand analysis, a geologist must make an assumption that resistivity of an adjacent shale ($R_{sh}$) is the same as resistivity of shale in the formation. This assumption is not always correct.

Most shaly sand interpretation problems occur in formations with $R_w$ values that are not too salty [NaCl < 20,000 ppm or $R_w > 0.3$ ohm-m at 80°F (Hilchie, 1978)]. Where formation water is very salty, shale has less effect on the formation's resistivity. Therefore, calculated water saturations without correction for shale are close to true formation water saturation.

This chapter discussed several log-interpretation techniques. These techniques are based on many of the formulas already presented in the text. What the formulas are, and where they are found is summarized on the log-interpretation flow chart included at the end of this chapter (Figure 7.2).

# REVIEW

1. The Archie equation is used to calculate a formation's water saturation in both the invaded ($S_{xo}$) and uninvaded ($S_w$) zones.

2. The ratio method for determining water saturation ($S_w$) does not require a value for porosity ($\phi$).

3. The ratio between the water saturations in the invaded ($S_{xo}$) and uninvaded ($S_w$) zones (i.e., $S_w/S_{xo}$) can be used as an index for the degree of hydrocarbon moveability.

4. Bulk volume water ($BVW$) is important because it indicates when a reservoir is at irreducible water saturation ($S_{w\ irr}$).

5. Quick-look methods are important because they provide flags that indicate zones of potential interest.

6. Hingle and Pickett crossplot techniques are simple and rapid methods for determining a formation's:

- water saturation ($S_w$)
- water resistivity ($R_w$)
- cementation factor ($m$)
- matrix values (travel time or density)

7. Log-derived data can be used to estimate permeability of a formation, but only if the formation is at irreducible water saturation.

8. The flow charts included in this chapter (Figures 7.1 and 7.2) will help you review the steps used in log interpretation and will also provide an index of where different pieces of information are located.
<!-- page 140 -->
Log Interpretation

129


----
━━━ FORMAT 11: FLOW / PROCESS DIAGRAM ━━━
```mermaid
graph TD
    A[Look for clean zones] --> B{Classics}
    A --> C{Carbonates}
    B --> D[Look for resistivity]
    C --> E[Look for porosity]
    D -->|LOW| F[Water zone e<br>Use as baseline (wet)<br>comparison.]
    D -->|HIGH| G[Check porosity]
    E -->|LOW| H[Tight.<br>Unlikely pay.]
    E -->|HIGH| I[Check resistivity]
    F --> J[Zone of interest]
    G -->|LOW| K[Tight.<br>Unlikely pay.]
    G -->|HIGH| L[Zone of interest]
    H --> L
    I -->|LOW| M[Water zone<br>Use as baseline (wet)<br>comparison.]
    I -->|HIGH| N[Zone of interest]
    M --> L
    L --> O[Begin detailed analysis]
    N --> O
```
----
KEYWORDS: flowchart, reservoir evaluation, pay zone identification, clean zones, resistivity, porosity, baseline comparison, tight zones, detailed analysis


Figure 7.1. Flowchart for scanning logs to identify zones of interest (both pay and wet). The scanning flowchart has two paths, one for clastics and one for carbonates.

# **Clastics:**

The resistivity log is the primary reconnaissance measurement because clastics tend to consist of reservoirs surrounded by shales whose resistivities vary gradually with depth. Differences in the fluid content of the reservoirs tend to produce reservoir resistivities that stand out against the relatively constant resistivity of the surrounding shales.

# **Carbonates:**

Formation resistivities tend to vary widely with changing rock types, and commonly there are few shales against which to measure changes. In this case, the porosity log is the primary reconnaissance measurement. By first finding the porous zones, the zones with the capacity to hold fluids (of any type) can be identified.

Using this scanning technique in combination with the neutron-density quick-look technique discussed in Chapter 4 (if those logs are available) allows one to identify lithology (and sometimes fluid type) in the course of identifying the zones of interest.

¹ Zones that appear to be shales might be radioactive productive zones.
² Shaly zones might produce oil or gas even if they have low resistivity.


----
━━━ FORMAT 11: FLOW / PROCESS DIAGRAM ━━━
```mermaid
graph TD
    A[Data Source] --> B[Deep-reading resistivity (ILD, LL D)]
    A --> C[Shallow-reading resistivity (MSFL, MLL, Prox)]
    A --> D[Density]
    A --> E[Neutron]
    A --> F[Sonic]
    A --> G[Magnetic Resonance]
    A --> H[SP]
    A --> I[Gamma Ray]
    A --> J[Wellsite measurements]
    A --> K[Laboratory measurements]
    A --> L[Local knowledge]

    B -->|Ch.5| M[Ri]
    C -->|Ch.5| N[R40]
    D -->|Ch.4| O[Φ]
    E -->|Ch.7| O
    F -->|Ch.6| O
    G -->|Ch.6| P[Vshale]
    H -->|Ch.2| Q[Rw]
    I -->|Ch.5| R[Roof]
    J -->|Ch.4| S[σ]
    K -->|Ch.4| S
    L -->|Ch.4| S

    M --> T[Sw]
    N --> T
    O --> T
    P --> T
    Q --> T
    R --> T
    S --> T

    T --> U[Sw]
    T --> V[Sxo]
    T --> W[Movable hydrocarbons]
    T --> X[HW]
    T --> Y[Permeability]
    T --> Z[Reserves]
```
----
KEYWORDS: well logging, data flow, petrophysical interpretation, input parameters, output quantities, resistivity, density, neutron, sonic, magnetic resonance, SP, gamma ray, wellsite measurements, laboratory measurements, local knowledge, water saturation, movable hydrocarbons, permeability, reserves


Figure 7.2. Flowchart for interpretation.

The sources of raw data, both well logs and other well-bore information, are shown in the left column. In many cases, the information generated from that raw data (shown in the center column) is used in computations to produce the quantities of interest (shown in the right column).

The chart shows that there are several ways to calculate porosity ($\phi$) and shale volume ($V_{shale}$) from the raw data.

The chapters that explain the calculations are listed in the flowchart.
<!-- page 141 -->
130

ASQUITH AND KRYGOWSKI


Figure 7.3. Buckles plots (porosity vs. water saturation).

Because production of water in a well can affect a prospect's economics, it is important to know the bulk volume water and whether the formation is at irreducible water saturation ($S_{W\text{irr}}$).

These Buckles plots are taken from the Ordovician Red River B-zone, Beaver Creek Field, Golden Valley County, North Dakota (after Jaafar, 1980).

With $S_{W}$ and porosity plotted on linear scales, points of equal bulk volume water (BVW) plot as hyperbolic curves. A series of points plotting along a particular hyperbolic curve indicates that the bulk volume water is constant and that the formation is close to irreducible water saturation. A reservoir in that condition would not produce water. As the amount of formation water increases, the bulk volume water values become scattered from the hyperbolic curves and the formation has more water than it can hold by capillary pressure. The water saturation is no longer at, or near, irreducible, so more water is produced relative to oil.

Figure 7.3a is an example of nearly constant BVW. The formation shown produces 96% oil. Note that all the points plot between 0.04 and 0.05 BVW. The formation is very close to, or at, irreducible water saturation.

Figure 7.3b shows a well producing 68% oil. About half the points cluster around a BVW value of 0.04, but the other half have higher values of BVW, indicating moveable water.

Figure 7.3c shows a well producing no oil (all water). Note the scatter of BVW values from the hyperbolic curves, indicating that the formation is not at irreducible water saturation.
<!-- page 142 -->
Log Interpretation

131


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
- X-axis: True resistivity, Rt, logarithmic scale, range 0.10 to 100.00 (Ω·m).
- Y-axis: Density porosity, DPHI, logarithmic scale, range 0.01 to 1.00 (fractional porosity).
- Plot contains 5 diagonal lines (family of curves) labelled with values: 5, 10, 20, 50, 100, 200, 500, 1000 (units not specified, likely ppm or mg/L, as per standard Schlumberger CP palettes).
- Data points: 7 black dots plotted on the chart, distributed between Rt = 1.00 and 10.00, DPHI = 0.10 and 0.50.
- The curves are interpreted as lines of constant formation water salinity (or similar parameter) in a crossplot of resistivity vs. density porosity.
- The data points lie primarily along the curve labelled "100", with one point near "50" and one near "200".
> Тренд: С увеличением истинного сопротивления (Rt) плотностная пористость (DPHI) уменьшается; данные точек сосредоточены вдоль кривой, соответствующей значению 100 на семействе кривых.
KEYWORDS: DPHI, Rt, кривые постоянной солености, кроссплот, плотностная пористость, истинное сопротивление, логарифмическая шкала, интерпретация ГИС
----


Figure 7.4. Pickett plot (saturation crossplot or resistivity-porosity crossplot) illustrating water-bearing and hydrocarbon-bearing zones in a well.

Data are from the Morrow Sandstone, Cimarron County, Oklahoma (Table 7.4).

Density porosity was calculated assuming a matrix density of $2.65\mathrm{g/cm^3}$ and a fluid density of $1.0\mathrm{g/cm^3}$. The water-bearing line ($S_w = 100\%$) was drawn through the cluster of points with a slope of $-1/2$ ($m = 2$). (Because of the limited porosity range of the points and their scatter, other values of $m$ from 1.8 to 2.15 could be justified.)

The intercept of the water-bearing line at $100\%$ porosity ($\mathrm{DPHI} = 1.0$) is $a \times R_{a}$. If the intercept were not off the plot in this illustration, the value could be read directly from the plot. In cases such as this, the value for $a \times R_{a}$ can be determined from $R_{a}$ by using Equation 7.28.

$$
R _ {w} = \frac {R _ {a} \times \phi^ {m}}{a}
$$

Remember that $R_{a}$ is the resistivity in the undisturbed, water-bearing zone, and for all points on the water-bearing line $R_{i} = R_{a}$.

Procedure to calculate $R_{a}$:

For some porosity value, read the value of $R_{a}$ from the water-bearing line on the crossplot. In this case, for a porosity of $10\%$ ($\mathrm{DPHI} = 0.10$), $R_{a} = 4.6$ ohm-m.

Assume a value of tortuosity factor ($a$). In this case, $a = 1.0$.

The value of cementation exponent ($m$) is determined from the crossplot. In this case, $m = 2.0$.

By substitution in the above equation,

$$
R _ {w} = \frac {4 . 6 \times 0 . 1 0 ^ {3 . 0}}{1 . 0}
$$

$R_{w} = 0.046$ ohm-m at formation temperature

The water saturation lines are constructed on the plot from the value for $R_{a}$ and the multipliers from Table 7.2. The multipliers are for a saturation exponent ($n$) of 2.0. For each line to be plotted, multiply $R_{a}$ by the multiplier to get the $y$-intercept and draw a line from the $y$-intercept parallel to the water-bearing line. To plot the line for $50\%$ water saturation, for example, if $R_{a}$ (at $\mathrm{DPHI} = 0.10$) is 4.6 and the multiplier (from Table 7.2) is 4, the $y$-intercept for the $50\%$ water saturation line (at $\mathrm{DPHI} = 0.10$) is 18.4.

To determine the water saturation of the anomalous points (with more accuracy than estimating the values from the crossplot), the following equation can be used:

$$
S _ {w} = \left(\frac {R _ {a}}{R _ {r}}\right) ^ {\frac {1}{n}}
$$

In this case, the value for $R_{a}$ is the value at the water-bearing line at the same porosity as the point of interest. For the two points of interest (both having the same porosity), $R_{a} = 0.80$ ohm-m. For the point who's resistivity is 40 ohm-m, the saturation is found by:

$$
S _ {w} = \left(\frac {0 . 8}{4 0}\right) ^ {\frac {1}{2 . 0}}
$$

$$
S _ {w} = 0. 1 4
$$

For comparison interpretation, Figure 7.7 is a Hingle plot with the same data shown.
<!-- page 143 -->
132

ASQUITH AND KRYGOWSKI


----
━━━ FORMAT 7: NOMOGRAM / ПАЛЕТКА ━━━
Палетка для определения пористости по удельной проводимости и удельному сопротивлению.

Ось абсцисс (горизонтальная): Пористость, φ — линейная шкала, диапазон от 0 до 1 (не указано, но по структуре палетки — доля, безразмерная).

Ось ординат (левая вертикальная): Проводимость, Ca — логарифмическая шкала, диапазон от 0 до 2000 (mmho/m), с делениями: 0, 5, 10, 20, 50, 100, 200, 500, 1000, 1500, 2000.

Ось ординат (правая вертикальная): Удельное сопротивление, R — логарифмическая шкала, диапазон от 0.5 до ∞ (Ω·m), с делениями: 0.5, 0.6, 0.7, 0.8, 1, 1.2, 1.5, 2, 2.5, 3, 5, 10, 15, 20, 50, 100, 200, 500, 1000, ∞.

Семейство кривых: не указано, но по структуре — это палетка для определения пористости φ по Ca и R, предположительно для различных значений параметра водонасыщенности (например, m, n, a) или для различных типов пород. На палетке нет явно промаркированных кривых, но присутствуют горизонтальные линии, соответствующие значениям φ, и вертикальные линии, соответствующие значениям Ca и R.

Процедура чтения: по оси ординат (Ca или R) найти значение, затем по горизонтальной линии, проходящей через это значение, определить пористость φ на оси абсцисс. Поскольку Ca и R связаны обратно (Ca = 1/R), палетка представляет собой одну и ту же зависимость, отображённую с двух сторон.

Ориентировочные точки (для крайних кривых, если бы они были параметризованы):
- При φ = 0.1 (10%) и Ca = 100 mmho/m → R = 0.01 Ω·m (не на шкале, но по обратной связи).
- При φ = 0.1 и Ca = 10 mmho/m → R = 0.1 Ω·m.
- При φ = 0.1 и Ca = 1 mmho/m → R = 1 Ω·m.
- При φ = 0.1 и Ca = 0.1 mmho/m → R = 10 Ω·m.

Примечание: палетка не содержит явных параметров (например, m, n, a), но её структура соответствует стандартным палеткам для определения пористости по удельной проводимости (или сопротивлению) в предположении постоянных параметров Арчи.

KEYWORDS: палетка, удельная проводимость, удельное сопротивление, пористость, логарифмическая шкала, интерпретация ГИС, Арчи, Ca, R, φ
----


Figure 7.5. Hingle plot (saturation crossplot or resistivity-porosity crossplot) generally used for sandstones. (Western Atlas International, Inc., 1995, Chart 7-79)
The y-axis is constructed with tortuosity factor (a) = 1.0 and cementation exponent (m) = 2.0.
<!-- page 144 -->
Log Interpretation

133


----
━━━ FORMAT 7: NOMOGRAM / ПАЛЕТКА ━━━
Палетка для определения удельного сопротивления и проводимости.

Ось абсцисс (горизонтальная): не указана, но предполагается, что это ось для ввода параметра (например, пористости, глинистости или другого параметра, используемого в интерпретации).

Ось ординат (вертикальная, левая): Conductivity, C, (mmho/m) — логарифмическая шкала, диапазон от 0 до 100, с делениями: 0, 0.5, 1, 2, 5, 10, 15, 20, 25, 30, 40, 50, 60, 80, 100.

Ось ординат (вертикальная, правая): Resistivity, R, (Ω • m) — логарифмическая шкала, диапазон от ∞ до 10, с делениями: ∞, 20,000, 5000, 1000, 500, 200, 100, 50, 25, 20, 15, 10.

Семейство кривых: не указано, но предполагается, что это семейство кривых, соответствующих различным значениям глинистости, пористости или другого параметра, используемого для интерпретации. В данном изображении кривые не нанесены — показана только сетка координат.

Процедура чтения: по оси абсцисс задаётся значение параметра (например, пористость), по соответствующей кривой (для заданной глинистости) снимается значение проводимости (C) по левой оси или удельного сопротивления (R) по правой оси.

Анкерные точки (ориентировочно, для крайних кривых, если бы они были):
- При C = 1 mmho/m → R = 1000 Ω·m
- При C = 10 mmho/m → R = 100 Ω·m
- При C = 100 mmho/m → R = 10 Ω·m

Примечание: в данном изображении отсутствуют кривые, поэтому палетка не может быть использована для интерпретации без дополнительных данных.

KEYWORDS: палетка, удельное сопротивление, проводимость, логарифмическая шкала, интерпретация, ГИС, C, R, Ω·m, mmho/m
----


Figure 7.6. Hingle plot (saturation crossplot or resistivity-porosity crossplot) generally used for carbonates. (Western Atlas International, Inc., 1995, Chart 7-80) The y-axis is constructed with tortuosity factor (a) = 0.62 and cementation exponent (m) = 2.15
<!-- page 145 -->
134

ASQUITH AND KRYGOWSKI

Figure 7.7. Hingle plot (saturation crossplot or resistivity-porosity crossplot) illustrating water-bearing and hydrocarbon-bearing zones in a well. Data are from the Morrow Sandstone, Cimarron County, Oklahoma (Table 7.4).

The Hingle grid using a = 1.0 and m = 2.0 was chosen as the common parameters for sandstones.

The x-axis has been scaled in bulk density, and the points plotted accordingly. The water-bearing line drawn through the cluster of points intersects the y-axis at 2.65 g/cm³, the matrix-density value for the formation. (Given the limited porosity range and the scatter of those points, other values for matrix density could also be justified.)

R_w is determined using Equation 7.28:

$$R_w = \frac{R_c \times \phi^m}{a}$$

For some porosity value, read the value of R_a from the water-bearing line on the crossplot. In this case, for a porosity of 10% (bulk density = 2.485 g/cm³), R_a = 4.1 ohm-m.

The values of tortuosity factor (a) and cementation exponent (m) were assumed by choice of the particular crossplot grid.

By substitution in the above equation,

$$R_w = \frac{4.1 \times 0.10^{2.0}}{1.0}$$

R_w = 0.041 ohm-m at formation temperature

The water saturation lines are constructed on the plot from the value for R_a and the multipliers from Table 7.2. The multipliers are for a saturation exponent (n) of 2.0.


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
This is a crossplot of bulk density versus conductivity (or resistivity) with water saturation contours.

Left Y-axis: Conductivity, C, in mmho/m, linear scale, range 0 to 2000.
Right Y-axis: Resistivity, R, in (Ω·m), linear scale, range 0.5 to 500 (logarithmic scale implied by tick marks: 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500).
X-axis: Bulk density, in g/cm³, linear scale, range 2.25 to 2.65.

The plot contains a family of curves representing constant water saturation (Sw), labelled: 30, 50, 70, 100. These curves are straight lines radiating from the origin (0,0) in the lower-left corner. The Sw=100 curve is the steepest, Sw=30 is the shallowest.

Data points are shown as black filled circles. There are 10 data points plotted. Their approximate coordinates (Bulk density, Conductivity) are:
- (2.35, 50)
- (2.35, 100)
- (2.38, 200)
- (2.40, 300)
- (2.42, 400)
- (2.44, 500)
- (2.46, 700)
- (2.48, 1000)
- (2.50, 1200)
- (2.52, 1500)

The data points lie approximately along the Sw=50 curve, suggesting a water saturation of around 50% for these samples.

The plot is a standard interpretation chart used in petrophysics to estimate water saturation from bulk density and resistivity (or conductivity) measurements.

> Тренд: С увеличением плотности породы (с 2.25 до 2.65 г/см³) проводимость уменьшается, а удельное сопротивление увеличивается. Кривые постоянной водонасыщенности (Sw) идут от начала координат, и данные точки лежат вблизи кривой Sw=50, что указывает на среднюю водонасыщенность.

KEYWORDS: проводимость, удельное сопротивление, плотность, водонасыщенность, Sw, кривые постоянной водонасыщенности, петрофизика, интерпретация, керн, ГИС
----


For each line to be plotted, multiply R_a by the multiplier and plot that line so that it intersects the water-bearing line at infinite resistivity. In this example, R_a (at bulk density = 2.485 g/cm³) is 4.1. The intercept for the 50% water-saturation line (at bulk density = 2.485 g/cm³) is 16.4.

To determine the water saturation of the anomalous points (with more accuracy than estimating the values from the crossplot), the following equation can be used:

$$S_w = \left(\frac{R_a}{R_s}\right)^{\frac{1}{n}}$$

In this case, the value for R_a is the value at the water-bearing line at the same porosity as the point of interest. For the two points of interest (both having the same porosity), R_a = 0.83 ohm-m. For the point who's resistivity is 40 ohm-m, the saturation is found by:

$$S_w = \left(\frac{0.83}{40}\right)^{\frac{1}{2.0}}$$

$$S_w = 0.144$$

For comparison of interpretation, Figure 7.4 is a Pickett plot with the same data shown.
<!-- page 146 -->
Log Interpretation

135


----
━━━ FORMAT 7: NOMOGRAM / ПАЛЕТКА ━━━
Палетка для определения насыщенности воды в зоне перехода выше водоносного горизонта (S_w, water saturation above transition zone) в зависимости от пористости (φ, porosity) и проницаемости (k, permeability).

Ось абсцисс (горизонтальная): φ, porosity (p.u.), линейная шкала, диапазон 0–40.
Ось ординат (вертикальная): S_w, water saturation above transition zone (%), линейная шкала, диапазон 0–60.

Семейство кривых: параметр — проницаемость k, permeability (md), с подписями: 0.01, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.2, 0.5, 1.0, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000.

Процедура чтения: по оси абсцисс задаётся пористость φ, по кривой, соответствующей заданной проницаемости k, снимается значение S_w на оси ординат.

Анкерные точки (ориентировочно):
- Для k = 0.01 md: при φ = 5 p.u. → S_w ≈ 50%; при φ = 10 p.u. → S_w ≈ 35%
- Для k = 100 md: при φ = 15 p.u. → S_w ≈ 20%; при φ = 25 p.u. → S_w ≈ 10%
- Для k = 5000 md: при φ = 30 p.u. → S_w ≈ 10%; при φ = 35 p.u. → S_w ≈ 8%

> Тренд: с увеличением проницаемости при фиксированной пористости насыщенность воды в зоне перехода уменьшается; при фиксированной проницаемости с ростом пористости S_w снижается.

KEYWORDS: палетка, насыщенность воды, пористость, проницаемость, зона перехода, ВНК, интерпретация ГИС, S_w, k, φ, номограмма, петрофизика


Figure 7.8. Chart of porosity ($\phi$) versus irreducible water saturation ($S_{wi}$ in) for estimating permeability and determining bulk volume water. (Schlumberger, 1998, Chart K-3)

Given: Porosity ($\phi$) = 0.25 (= 25 porosity units, p.u.) and irreducible water saturation ($S_{wi}$ in) = 40% for an oil-bearing sandstone. The chart is constructed with the assumption of a medium-gravity oil.

Procedure:

1. Find porosity ($\phi$ = 25 p.u.) on the bottom horizontal scale, and find irreducible water saturation ($S_{wi}$ in = 40%) on the left vertical scale.

Note that irreducible water saturation is labeled $S_{wi}$ on this chart.

Follow the two values into the chart to the point where they intersect.

2. The heavy curve on which this point falls represents permeability. In this case, permeability, K = 130 md.
3. The light hyperbolic curves ($C = S_{wi} \times \phi$) represent lines of equal value for bulk volume water. In this example, the bulk volume water equals 0.10 (BVW = 0.10).

Note: It is important to remember that this chart is only valid for estimating permeability (K) in zones at irreducible water saturation ($S_{wi}$ in).

Zones at irreducible water saturation have bulk volume water values that are fairly constant. On the chart, data points from different intervals in a zone at irreducible saturation plot in a coherent pattern, on or parallel to one of the hyperbolic curves. Data points from zones not at $S_{wi}$ in scatter from this pattern.
<!-- page 147 -->
10
<!-- page 148 -->
8

Asquith, G., and D. Krygowski, 2004, Petrophysical Techniques, in G. Asquith and D. Krygowski, Basic Well Log Analysis: AAPG Methods in Exploration 16, p. 137-149.

# Petrophysical Techniques

## GENERAL

Petrophysical techniques provide most of the subsurface data available to an exploration geologist. Besides their importance in completion decisions, they are also invaluable methods for mapping and identifying lithologies. Presented here are nine techniques that can assist geologists with lithologic determination and mapping. They are:

- Neutron-density lithology plot
- Neutron-sonic lithology plot
Density-sonic lithology plot
- \(M - N\) lithology plot
- Matrix identification plot \((\rho_{maa}\) vs. \(\Delta t_{maa})\)
- Matrix identification plot \((\rho_{maa}\) vs. \(U_{maa})\)
Alpha mapping from the SP log
- Clean sand or carbonate from gamma ray log
- Rock typing and facies mapping.

These techniques are especially important to a geologist when lithologic data from core or samples are unavailable.

Figures 8.1 and 8.2 are logs through the Silurian Fusselman Formation in West Texas. The log suite for this well consists of a dual induction-SFL, SP, gamma ray, and neutron-lithodensity log (Figure 8.1), and a sonic log with gamma ray (Figure 8.2). Using data from these logs, we will illustrate how lithologies are determined using the first six methods listed above. It is important to mention that the porosity zone (9088 to 9126 ft) in the Fusselman has a combination of vuggy and intercrystalline porosity. How the presence of vuggy porosity affects the different lithology plots will be discussed in the text below. The software used to generate the results from the original log data is called CBA (Carbonate Advisor; The Logic Group, 1994). The various lithology plots and crossplots were rendered in PetroWorks, from Landmark Graphics, a Halliburton company.

## NEUTRON-DENSITY LITHOLOGY PLOT

The gamma ray log (Chapter 3) measures the natural radiation of a formation and primarily functions as a lithology log. It helps differentiate shales (high radioactivity) from sands, carbonates, and anhydrites (low radioactivity). The neutron log is a porosity device that is used to measure the amount of hydrogen in a formation, which is assumed to be related to porosity (Chapter 4). The density log is a porosity device that measures electron density, and from that, formation bulk density (Chapter 4). When these three logs are used together, lithologies can be determined. Figure 4.8 is a schematic illustration of how responses from the gamma ray, neutron, and density logs are related to lithology.

Figure 8.3 is a neutron-density lithology plot of the data from the Fusselman Formation (Figures 8.1 and 8.2). On the lithology plot (Figure 8.3), the Fusselman data cluster between the lithology lines of dolomite and limestone. The amounts of each lithology are illustrated in the column next to the lithology plot. As a quick-look method, where there are a limited number of lithologies, this plot works well for basic lithologic and facies mapping. The problem is how the geologist determines if the Fusselman is a mixture of dolomite and limestone or a mixture of dolomite and sandstone.

## NEUTRON-SONIC LITHOLOGY PLOT

The sonic log is a porosity device (Chapter 3) that measures the speed of a compressional sound wave through the formation. Figure 8.4 is neutron-sonic plot for the Fusselman Formation. The Fusselman data from the porous zone (9088 to 9126 ft) cluster along the dolomite lithology line, and the data from the nonporous zone above 9088 ft cluster along the limestone lithology line (Figure 8.4). The amounts of each lithology are illustrated in the column next to the lithology

137
<!-- page 149 -->
138

ASQUITH AND KRYGOWSKI

plot. A comparison of Figures 8.3 and 8.4 reveals that the neutron-sonic plot indicates a much more dolomitic lithology compared to the neutron-density plot. This difference is due to the presence of vuggy porosity from 9088 to 9126 ft. Remember that the sonic log measures only matrix porosity (intergranular and intercrystalline) and the nuclear logs (neutron and density) measure total porosity. Therefore, when vuggy porosity is present sonic porosity is less than total (neutron-density) porosity and the data cluster lower on the neutron-sonic plot (i.e., more dolomitic; Figure 8.4).

## DENSITY-SONIC LITHOLOGY PLOT

Figure 8.5 is a density-sonic plot of the Fusselman interval illustrated in Figures 8.1 and 8.2. The calculated lithologies are displayed in the column next to the lithology plot. The density-sonic plot is the least desirable of the lithology plots because the lines representing the different lithologies (i.e., sandstone, limestone, and dolomite) are much closer together. Therefore, it is harder to differentiate the different lithologies. An examination of the lithology for the vuggy zone (9088 to 9126 ft) reveals that the lithology is now limestone (Figure 8.5). The presence of the vuggy porosity causes the sonic log to underestimate porosity, which shifts the data to the left of the plot so that the lithology appears to be limestone. It is important to remember that all lithology plots that require a sonic log may be unreliable if there is a large amount of vuggy porosity. However, as can be observed in Figures 8.4 and 8.5, this confusion about lithology in the interval from 9088 to 9126 ft informs the log analyst that the reservoir has vuggy porosity. Or to state it another way, if all the porosity were intergranular or intercrystalline, all the lithology plots would indicate similar lithologies.

## M-N LITHOLOGY PLOT

The M-N plot requires a sonic log, neutron log, and density log, of which are all necessary to calculate the lithology-dependent variables M and N. M and N values are largely independent of matrix porosity (intergranular and intercrystalline). A crossplot of these two variables makes lithology more apparent. M and N values are calculated by the following equations (Schlumberger, 1972):

$$M = \frac{\Delta t_{fl} - \Delta t}{\rho_b - \rho_{fl}} \times 0.01 \left( M = \frac{\Delta t_{fl} - \Delta t}{\rho_b - \rho_{fl}} \times 0.003 \text{ (metric)} \right)$$

$$N = \frac{\phi_{spl} - \phi_N}{\rho_b - \rho_{fl}}$$

where:

$\Delta t$ = interval-transit time in the formation (from the log)

$\Delta t_{fl}$ = interval-transit time in the fluid in the formation

$\rho_b$ = formation bulk density (from the log)

$\rho_{fl}$ = fluid density

$\phi_N$ = neutron porosity (in limestone units, from the log)

$\phi_{Nfl}$ = neutron porosity of the fluid of the formation (usually = 1.0)

When the matrix parameters ($\Delta t_{ma}$, $\rho_{ma}$, $\phi_{Nma}$; Table 8.1) are used in the M and N equations instead of formation parameters, M and N values can be obtained for the various minerals (Table 8.2). Note that the quantities M and N above are related to lithology and have no relation to the cementation exponent (m) and the saturation exponent (n) in Archie's equation.

Figure 8.6 is an M-N plot of data from the Silurian Fusselman Formation illustrated in Figures 8.1 and 8.2. The data above a depth of 9088 ft plot in the sand-calcite-dolomite triangle. The calculated lithologies are illustrated in the column next to the M-N plot. The data from the porous vuggy interval (9088 to 9126 ft) plot above the tie line between calcite and dolomite, indicating the presence of vuggy porosity. If only matrix intercrystalline or intergranular porosity were present, the data would have plotted on or below the calcite-dolomite tie line. Remember, that the presence of vuggy porosity results in an underestimation of sonic interval transit time and therefore an overestimation of M. Because the data from the interval from 9088 to 9126 ft plot out of the lithology triangle, the calculated lithologies are not reliable.

## MATRIX IDENTIFICATION PLOT ($\rho_{maa}$ VS. $\Delta t_{maa}$)

The matrix identification plot, like the M-N plot, is a crossplot technique that helps identify lithology and secondary porosity. As with the M-N plot, the matrix-identification plot requires data from neutron, density, and sonic logs.

The first step in constructing a matrix identification plot is to determine values for the apparent matrix parameters, apparent matrix density ($\rho_{maa}$) and apparent matrix traveltime ($\Delta t_{maa}$). These values are calculated from neutron ($\phi_N$), density ($\rho_b$) and sonic ($\Delta t$) data using the following equations (Western Atlas, 1995):
<!-- page 150 -->
Petrophysical Techniques

139

Table 8.1. Matrix Coefficients of Several Minerals and Types of Porosity (Liquid-filled Boreholes).

|  Minerals | Δt_{ma} μsec/ft | ρ_{ma} g/cm³ | φ_{SNPma}^{*} (decimal) | CNLma^{*} (decimal) | P_{e} (b/e)  |
| --- | --- | --- | --- | --- | --- |
|  Sandstone (1): V_{ma} = 18,000 ft/sec; φ > 0.10 | 55.5 | 2.65 | -0.035^{a} | -0.05^{a} | 1.81  |
|  Sandstone (2): V_{ma} = 19,500 ft/sec; φ < 0.10 | 51.2 | 2.65 | -0.035^{a} | -0.005 | 1.81  |
|  Limestone | 47.5 | 2.71 | 0.00 | 0.00 | 5.08  |
|  Dolomite (1): φ = 0.055 to 0.30 | 43.5 | 2.87 | 0.035^{a} | 0.085^{a} | 3.14  |
|  Dolomite (2): φ = 0.015 to 0.055 and φ > 0.30 | 43.5 | 2.87 | 0.02^{a} | 0.065^{a} | 3.14  |
|  Dolomite (3): φ = 0.0 to 0.015 | 43.5 | 2.87 | 0.005^{a} | 0.04^{a} | 3.14  |
|  Anhydrite | 50.0 | 2.98 | -0.005 | -0.002 | 5.06  |
|  Gypsum | 52.0 | 2.35 | 0.49^{b} | 0.6 | 3.99  |
|  Salt | 67.0 | 2.03 | 0.04 | -0.01 | 4.65  |
|  ^{a} Average values  |   |   |   |   |   |
|  ^{b} Based on hydrogen-index computation  |   |   |   |   |   |
|  ^{*}φ_{SNPma} and φ_{CNLma} values are specific to Schlumberger neutron tools.  |   |   |   |   |   |

From Schlumberger (1972). Courtesy Schlumberger Well Services.

Table 8.2. Values of M and N lithology parameters, calculated for common minerals.

|  Minerals | Fresh mud ρ = 1.0 g/cm³ |   | Salt mud ρ = 1.1 g/cm³  |   |
| --- | --- | --- | --- | --- |
|   |  M | N | M | N  |
|  Sandstone (1): V_{ma} = 18,000 ft/sec; φ > 0.10 | 0.810 | 0.628 | 0.835 | 0.669  |
|  Sandstone (2): V_{ma} = 19,500 ft/sec; φ < 0.10 | 0.835 | 0.628 | 0.862 | 0.669  |
|  Limestone | 0.827 | 0.585 | 0.854 | 0.621  |
|  Dolomite (1): φ = 0.055 to 0.30 | 0.778 | 0.516 | 0.800 | 0.544  |
|  Dolomite (2): φ = 0.015 to 0.055 and φ > 0.30 | 0.778 | 0.524 | 0.800 | 0.554  |
|  Dolomite (3): φ = 0.0 to 0.015 | 0.778 | 0.532 | 0.800 | 0.561  |
|  Anhydrite | 0.702 | 0.505 | 0.718 | 0.532  |
|  Gypsum | 1.015 | 0.378 | 1.064 | 0.408  |
|  Salt |  |  | 1.269 | 1.032  |

From Schlumberger Log Interpretation Principles, © 1972 Schlumberger. Courtesy Schlumberger Well Services.
<!-- page 151 -->
140

ASQUITH AND KRYGOWSKI

$$\rho_{maa} = \frac{\rho_b - (\phi_{ND} \times \rho_{fl})}{1 - \phi_{ND}} \tag{8.3}$$

$$\Delta t_{maa} = \frac{\Delta t - (\phi_{SN} \times \Delta t_{fl})}{1 - \phi_{SN}} \tag{8.4}$$

where:

$\rho_{maa}$ = apparent grain density in g/cm$^3$ or Kg/m$^3$

$\Delta t_{maa}$ = apparent matrix interval transit time in $\mu$sec/ft or $\mu$sec/m

$\rho_b$ = bulk density from the log

$\rho_{fl}$ = density of fluid

$\Delta t$ = interval transit time from the log

$\Delta t_{fl}$ = interval transit time of fluid

$\phi_{ND}$ = neutron-density crossplot porosity

$\phi_{SN}$ = sonic-neutron crossplot porosity

When matrix parameters ($\Delta t_{ma}$, $\rho_{ma}$, and $\phi_{Nma}$; Table 8.1) are used in the matrix identification equations instead of formation parameters, $\Delta t_{maa}$ and $\rho_{maa}$ values can be obtained for the various minerals (Table 8.3).

Table 8.3. Apparent matrix values for calculated for common minerals

|  Mineral | $\rho_{maa}$ (g/cm$^3$) | $\Delta t_{maa}$ ($\mu$sec/ft) | $U_{maa}$ (barns/cm$^3$)  |
| --- | --- | --- | --- |
|  Sandstone | 2.65 | 55.5 | 4.78  |
|  Limestone | 2.71 | 47.5 | 13.80  |
|  Dolomite | 2.87 | 43.5 | 8.98  |
|  Anhydrite | 2.98 | 50.0 | 14.90  |
|  Gypsum | 2.35 | 52.0 | 13.97  |
|  Salt | 2.03 | 67.0 | 9.68  |

Figure 8.7 is a matrix identification plot of data from the Silurian Fusselman Formation illustrated in Figures 8.1 and 8.2. The data above a depth of 9088 ft plot in the quartz-calcite-dolomite triangle with the calculated lithologies presented in the column to the right of the matrix identification plot. The porous interval with vuggy porosity (9088 to 9126 ft) plots above the quartz-calcite-dolomite triangle as it did on the $M-N$ plot (Figure 8.6). The calculated lithologies are illustrated in the column to the right of the lithology plot (Figure 8.7). Therefore, as with the $M-N$ plot (Figure 8.6), the lithologies determined for the porosity zone (9088 to 9126 ft) from the matrix identification plot (Figure 8.7) are unreliable.

## MATRIX-IDENTIFICATION PLOT ($U_{maa}$ VS. $\rho_{maa}$)

The third-generation density logs provide not only a bulk density ($\rho_b$) measurement but also a photoelectric absorption ($P_e$) measurement. The photoelectric measurement reflects the average atomic number of the formation and is therefore a good indicator of the formation's lithology (Dewan, 1983). The measurements of $\rho_b$ and $P_e$ are made from the same density tool at the long-spaced detector using energy selection (high energy for $\rho_b$ and low energy for $P_e$) of the incoming gamma rays. On the log (Figure 8.1), the $P_e$ curve is displayed with the neutron and density curves in track 3. The units for the $P_e$ curve are barns/electron. $P_e$ values for some of the common minerals are listed in Table 8.1.

The matrix-identification ($U_{maa}$ vs. $\rho_{maa}$) plot uses apparent matrix density ($\rho_{maa}$) and apparent volumetric cross section ($U_{maa}$) in barns/cm$^3$ (Table 8.3). $U_{maa}$ is calculated from the $P_e$, $\phi_N$, and $\rho_b$ values using the following equation (Western Atlas, 1995):

$$U_{maa} = \frac{(P_e \times \rho_b) - (\phi_{ND} \times U_{fl})}{1 - \phi_{ND}} \tag{8.5}$$

where:

$U_{maa}$ = apparent volumetric cross section in barns/electron

$P_e$ = photoelectric absorption in barns/electron

$\rho_b$ = bulk density

$\phi_{ND}$ = neutron-density porosity

$U_{fl}$ = photoelectric absorption of fluid

When matrix parameters ($\rho_{ma}$, $P_e$ and $\phi_{Nma}$; Table 8.1) are used in the matrix identification equations instead of formation parameters, $U_{maa}$ and $\rho_{maa}$ values can be obtained for the various minerals (Table 8.3).

Figure 8.8 is a matrix identification plot ($U_{maa}$ vs. $\rho_{maa}$) of data from the Silurian Fusselman Formation illustrated in Figures 8.1 and 8.2. The data above a depth of 9088 ft and the data from the vuggy porosity zone (9088 to 9126 ft) all plot in the quartz-calcite-dolomite triangle with the calculated lithologies presented in the column to the right of the matrix identification plot. Because the $P_e$ measurement is insensitive to the presence of vuggy porosity, the lithologies are all reliable.

Therefore, if only two lithologies are present in a vuggy reservoir the preferred lithology plots are neutron-density and matrix identification ($U_{maa}$ vs. $\rho_{maa}$); however, if three lithologies are present in a vuggy reservoir the preferred lithology plot is the matrix identification plot ($U_{maa}$ vs. $\rho_{maa}$). If the porosity is matrix intergranular or intercrystalline the neutron-
<!-- page 152 -->
Petrophysical Techniques 141

density, neutron-sonic, and density-sonic plots work for two lithologies and the M-N and both matrix identification plots work for three lithologies.

Figure 8.9 is a plot of the lithologies from the matrix identification plot ($U_{maa}$ vs. $\rho_{maa}$) (Figure 8.8) and neutron-density porosities for the Silurian Fusselman Formation. The digital lithology and porosity data together with depths can be used in a mapping program for further analysis.

### ALPHA MAPPING FROM THE SP LOG

The spontaneous potential (SP) log (Chapter 2) can be used to map clean (shale-free) sands vs. shaly sands. The technique is called alpha ($\alpha$) mapping (Dresser Atlas, 1974) and is based on the observation that the presence of shale in a formation decreases the SP response.

The alpha method can be extremely valuable in mapping because it can more narrowly define desirable zones. Alpha values from nearby wells can be used to construct clean-sand (high-energy) maps (in effect, mapping isoalpha values).

To construct an alpha map, the static spontaneous potential (SSP) that a sand would have, if it were completely shale-free and unaffected by bed thickness, is calculated. The equation for SSP is:

$$SSP = -K \times \log\left(\frac{R_{mf}}{R_w}\right) \tag{8.6}$$

where:

SSP = static spontaneous potential

$K = 60 + [0.133 \times \text{formation temperature (}^{\circ}\text{F)}]$

$R_{mf}$ = resistivity of mud filtrate at formation temperature

$R_w$ = resistivity of formation water at formation temperature

The SSP must be calculated for the formation in each well, so that variations in $R_{mf}$ and $R_w$ can be accounted for. Next, the alpha values are determined by the method shown in Figure 8.10. The alpha cutoff (0.75$\alpha$, 0.50$\alpha$, or whatever value chosen) is arbitrary, but should be based on production histories in the area.

The resulting alpha ($\alpha$) map delineates clean sand environments. In the above example (Figure 8.10), the greater alpha thickness for a given alpha cutoff (i.e., 0.75$\alpha$ or 0.50$\alpha$) indicates a greater thickness of higher energy, low-shale sandstones. Also, because the presence of shale in a sandstone can decrease its permeability, an alpha map indicates better reservoir conditions.

The problem with alpha mapping from an SP log is that SP response is decreased, not only by shale, but also by thin beds (less than 10 ft) and the presence of hydrocarbons (Chapter 2). Bed thickness problems are minimized by making an SP log bed thickness correction (Chapter 2). But the SP log can't be corrected for hydrocarbons.

### CLEAN SAND OR CARBONATE MAPS FROM GAMMA RAY LOG

The gamma ray log can be used to map clean (shale-free) sandstones or carbonates vs. shaly sandstones and carbonates. Because shales are more radioactive than clean sandstones or carbonates (Chapter 3), when the percentage of shale increases in these rock types, the gamma ray reading also increases.

Figure 8.11 is a gamma ray density neutron log through the Mississippian, upper Mission Canyon Formation in Roosevelt County, Montana. In this interval, crinoid and fenestrate-bryozoan bioherms are commonly developed. Because the bioherm facies is composed of clean carbonate relative to the facies that is not bioherm, the gamma ray log can be used to map the bioherm facies. The procedure for obtaining a clean carbonate cutoff from a gamma ray log is described in Figure 8.10.

A gamma ray value of 20 API units on the gamma ray log (Figure 8.11) represents clean carbonate with a volume of shale ($V_{shale}$) equal to or less than 0.05 (5%). By drawing a vertical line on the gamma ray log equal to 20 API units (Figure 8.10), the geologist can identify and map the clean carbonate (or sand).

Figure 8.12 is an isopach map of clean carbonate for the upper Mission Canyon Formation in Roosevelt County, Montana. Because the relationship between clean carbonate and the crinoid fenestrate-bryozoan bioherm facies is already established, the map (Figure 8.12) delineates the distribution of the bioherm facies. Clean carbonate maps have also been used to map the Pennsylvanian banks (bioherms) of north central Texas (Wermund, 1975).

### ROCK TYPING AND FACIES MAPPING

An important contribution to subsurface analysis of carbonate rocks has been the attempt to establish relationships between log responses and carbonate facies. Pickett (1977), Asquith (1979), and Watney (1979, 1980) used crossplots to identify the relationship of log response to rock type. Table 8.4 is a list of the crossplots applied by these authors.
<!-- page 153 -->
142

ASQUITH AND KRYGOWSKI

Table 8.4. Types of Carbonate Rock-identification Crossplots (after Pickett, 1977; Asquith, 1979; and Watney, 1979 and 1980).

|  Δt (interval transit time) | vs. | φ_{N} (neutron porosity)  |
| --- | --- | --- |
|  ρ_{b} (bulk density) | vs. | φ_{N} (neutron porosity)  |
|  ρ_{b} (bulk density) | vs. | Δt (interval transit time)  |
|  R_{t} (deep resistivity) | vs. | φ_{N} (neutron porosity)  |
|  GR (gamma ray) | vs. | φ_{N} (neutron porosity)*  |
|  Rt (deep resistivity) | vs. | φ_{S} (sonic porosity)  |

*Watney (1979 and 1980) also uses neutron log readings measured in counts/second.

To date, crossplots have been used to establish log vs. lithology relationships only when petrographic data are available from cores or cuttings in selected wells. Petrographic analysis from selected wells is essential to firmly establish rock type.

When establishing log/lithology relationships, log responses from control wells (i.e., wells with petrographic analysis) are crossplotted. Next, areas that delineate rock-type clusters are outlined (see Figure 8.13) on the crossplot. Finally, log responses from wells without cores or cuttings are added to the crossplot. The carbonate rock type and depositional environment of wells without petrographic analysis can then be determined by the cluster in which each occurs on the crossplot chart (see Figure 8.13).

In Figure 8.13, the solid black circles and squares represent data from wells where petrographic analysis was used to determine carbonate rock type and depositional environment. The open circles represent data from wells without petrographic analysis. The carbonate rock types and depositional environments were determined by the cluster in which the open circles were plotted.

Figure 8.14 is a crossplot of deep resistivity (R$_{t}$) vs. sonic porosity (φ$_{S}$) for the Lower Permian, Council

Grove B-zone in Ochiltree County, Texas. Clusters for the three carbonate rock types (oolite grainstone, oolitic wackestone, and argillaceous bioclastic wackestone) were established by petrographic analysis of cores and cuttings (open circles). The solid circles represent data from wells with only log control. Figure 8.15 is a facies map of the Council Grove B-zone based on the percentage distribution of the three carbonate rock types established by the resistivity/sonic-porosity crossplot (Figure 8.14).

The advantage of log crossplot techniques is that they maximize use of available information. Cores and cuttings are required from only a few control wells rather than all wells. This is very important in subsurface facies mapping because of the difficulty in obtaining cores and cuttings from every well in an area. Also, because petrographic analysis of every well is unnecessary, a great deal of time can be saved.

However, it should be emphasized that petrographic analysis of cores or cuttings from control wells is an essential first step to firmly establish the rock-type cluster used in the crossplots.

## REVIEW

1. Neutron and density logs can be used in a crossplot to determine lithology when a limited number of rock types are present.
2. Where lithology is more complex, a sonic log or a P$_{e}$ curve used in conjunction with the neutron and density curves is necessary to construct M-N lithology or matrix identification crossplots.
3. Spontaneous potential (SP) and gamma ray logs can be used to map shaly vs. nonshaly carbonates or sandstones.
4. Crossplotting of multiple log responses can be used to establish relationships between log responses and rock types, provided some petrographic data from cores or cuttings are available.
<!-- page 154 -->
Petrophysical Techniques

143


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: increases downward, units: Feet MD (measured depth), range: 9100 ft to 9150 ft (inferred from grid spacing and visible depth mark).

Left panel (SP and GR):
- Track 1: SP (spontaneous potential), scale: -160 mV to +40 mV, curve: solid line.
- Track 2: GR (gamma ray), scale: 0 to 150 API units, curve: solid line.
- Depth grid: 50 ft per major grid line, 10 ft per minor grid line.
- Curve behaviour:
  - SP: shows a negative deflection (anomaly) from ~9100 ft to ~9130 ft, then returns to baseline.
  - GR: shows a low reading (clean zone) from ~9100 ft to ~9130 ft, then increases sharply to high values (~120–150 API) from ~9130 ft to ~9150 ft.

Right panel (SFL, ILM, ILD, PEF, NPHI, DPHI):
- Track 1: SFL (shallow laterolog), scale: 0.2 to 200 ohm·m, curve: solid line.
- Track 2: ILM (intermediate laterolog), scale: 0.2 to 200 ohm·m, curve: dashed line.
- Track 3: ILD (deep laterolog), scale: 0.2 to 200 ohm·m, curve: dash-dotted line.
- Track 4: PEF (photoelectric factor), scale: 10 to 200 (unit not specified, likely "be"), curve: solid line.
- Track 5: NPHI (neutron porosity), scale: -0.1 to 0.3 (v/v decimal), curve: solid line.
- Track 6: DPHI (density porosity), scale: -0.1 to 0.3 (v/v decimal), curve: solid line.
- Curve behaviour:
  - Resistivity curves (SFL, ILM, ILD): show a high-resistivity zone from ~9100 ft to ~9130 ft (values ~100–200 ohm·m), then a sharp drop to low resistivity (~0.2–0.5 ohm·m) from ~9130 ft to ~9150 ft.
  - PEF: shows a low value (~10–12) in the high-resistivity zone, then increases to ~15–18 in the low-resistivity zone.
  - NPHI and DPHI: show low porosity (~0.1–0.15) in the high-resistivity zone, then increase to ~0.25–0.3 in the low-resistivity zone.

Interpretation:
- Interval 9100–9130 ft: high resistivity, low GR, low porosity, low PEF — suggests a clean, non-shaly sandstone reservoir.
- Interval 9130–9150 ft: low resistivity, high GR, high porosity, higher PEF — suggests shaly sand or shale.

No perforation intervals, fluid contacts, or interpreted results (Kp, Kn, Kpr) are marked on the log.

KEYWORDS: well log, SP, GR, SFL, ILM, ILD, PEF, NPHI, DPHI, resistivity, porosity, gamma ray, spontaneous potential, photoelectric factor, measured depth, feet, log interpretation, sandstone, shale
----


Figure 8.1. Induction, neutron, and density log through the Silurian Fusselman Formation, West Texas.


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: increases downward, units: Feet MD (measured depth), range: 9100 ft to 9150 ft (inferred from grid spacing and visible depth mark).

Track 1 (left):
- Curve: GR (Gamma Ray)
- Scale: 0 to 150 API units
- Line style: solid line
- Curve behaviour:
  - From 9100 ft to 9140 ft: relatively high and stable GR values (~120–130 API units), indicating shaly or clay-rich interval.
  - At ~9140 ft: sharp drop to ~40 API units, suggesting transition to clean sandstone or limestone.
  - From 9140 ft to 9150 ft: low and stable GR (~40 API units), indicating clean, non-shaly interval.

Track 2 (right):
- Curve: DT (Transit Time, sonic log)
- Scale: 80 to 40 μs/ft (note: scale is inverted, higher values at bottom)
- Line style: solid line
- Curve behaviour:
  - From 9100 ft to 9140 ft: high DT values (~80–85 μs/ft), indicating low velocity, likely shaly or low-density rock.
  - At ~9140 ft: sharp decrease to ~50 μs/ft, indicating transition to higher-velocity, denser rock (e.g., sandstone or limestone).
  - From 9140 ft to 9150 ft: relatively low and stable DT (~50–55 μs/ft), consistent with clean sandstone or carbonate.

Interpretation:
- The interval from 9100 ft to 9140 ft shows high GR and high DT, typical of shaly or clay-rich formations.
- The interval from 9140 ft to 9150 ft shows low GR and low DT, typical of clean sandstone or limestone.
- The sharp transition at ~9140 ft suggests a lithological boundary (e.g., shale to sandstone).

| Интервал, ft | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|--------------|------------------------|-------------------|-------------------------------|
| 9100–9140    | Глина / аргиллит       | GR: высокие (~120–130 API), DT: высокие (~80–85 μs/ft) | Шелеватый или глинистый интервал |
| 9140–9150    | Песчаник / известняк   | GR: низкие (~40 API), DT: низкие (~50–55 μs/ft) | Чистый, неглинистый интервал |

KEYWORDS: well log, gamma ray, sonic log, GR, DT, measured depth, lithology interpretation, shale, sandstone, transition zone, API units, μs/ft, depth scale, log curve behavior
----


Figure 8.2. Sonic log through the Silurian Fusselman Formation, West Texas.
<!-- page 155 -->
144

ASQUITH AND KRYGOWSKI


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
- X-axis: Neutron Porosity, NPHI, linear scale, range 0.00 to 0.30.
- Y-axis: Bulk Density, RHOB, linear scale, range 2.20 to 3.00.
- Data points: black filled circles, distributed in three main clusters.
  - Cluster 1 (left, low porosity): RHOB ~2.78–2.80, NPHI ~0.00–0.05.
  - Cluster 2 (middle, moderate porosity): RHOB ~2.55–2.65, NPHI ~0.10–0.20.
  - Cluster 3 (bottom right, high porosity): RHOB ~2.60–2.70, NPHI ~0.20–0.25.
- Reference curves (diagonal lines) with labelled porosity values (0, 5, 10, 15, 20, 25, 30) for:
  - Sandstone: upper curve, from (NPHI=0.00, RHOB=2.65) to (NPHI=0.30, RHOB=2.20).
  - Limestone: middle curve, from (NPHI=0.00, RHOB=2.70) to (NPHI=0.30, RHOB=2.25).
  - Dolomite: lower curve, from (NPHI=0.00, RHOB=2.75) to (NPHI=0.30, RHOB=2.30).
- The data points lie mostly between the limestone and dolomite curves, with some points near the sandstone curve at low porosity.
- The plot shows a general trend of decreasing bulk density with increasing neutron porosity, with the majority of points falling within the limestone and dolomite porosity trends.
> Тренд: с увеличением нейтронной пористости (NPHI) плотность (RHOB) уменьшается; данные преимущественно соответствуют карбонатным породам (известняк, доломит), с некоторыми точками в области песчаника при низкой пористости.

KEYWORDS: нейтронная пористость, плотность, кривые пористости, песчаник, известняк, доломит, кроссплот, ГИС, петрофизика, интерпретация
----


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: FEET, increases downward. Depth range: 9100 ft to 9200 ft (approximate top). Scale: 10 ft per major grid interval.

Tracks:
- Left track: Depth scale (FEET MD), with 10 ft grid spacing.
- Right track: Lithology column, labelled "Lithology", with two ornament types:
  1. Brick pattern (кирпичный крап) — occupies most of the column from 9100 ft to 9190 ft.
  2. Horizontal hatching (горизонтальная штриховка) — occupies the upper part from ~9190 ft to 9200 ft, and a thin layer at the bottom (~9100 ft).

Interpretation:
- The brick pattern is interpreted as a single lithology unit (likely sandstone or limestone, but lithology not specified in legend).
- The horizontal hatching represents a different lithology (likely shale or siltstone, but not specified).
- The boundary between the two units is irregular and wavy, suggesting a transition zone or interbedding.
- The bottom of the column shows a thin layer of the hatched lithology at 9100 ft, possibly a basal shale.

Interval table:
| Интервал, ft | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|--------------|--------------------------|-------------------|-------------------------------|
| 9100–9190    | кирпичный крап          | —                 | —                             |
| 9190–9200    | горизонтальная штриховка | —                 | —                             |
| 9100–9100    | горизонтальная штриховка | —                 | —                             |

No other curves or interpretation panels are present.

KEYWORDS: well log, lithology column, brick pattern, horizontal hatching, depth scale, feet, MD, lithology interpretation
----


Figure 8.3. Neutron-density crossplot and resulting lithology estimation, Fusselman Formation, West Texas. Data are from Figures 8.1 and 8.2. A lithology key is shown in Figure 8.6.


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
- X-axis: Neutron Porosity, NPHI, linear scale, range 0.00 to 0.30.
- Y-axis: Acoustic Wave Travel Time, DT, linear scale, range 40 to 80 (units not specified, typically μs/ft or μs/m).
- Data points: 50+ black dots, scattered across the plot, forming a general trend from lower-left to upper-right.
- Three curved reference lines (labeled "Sandstone", "Limestone", "Dolomite") are drawn from lower-left to upper-right, each with numerical labels (0, 5, 10, 15, 20) along the curve, indicating porosity values (likely % or fraction) corresponding to the DT values for each rock type.
- The "Sandstone" curve is the uppermost, "Limestone" is in the middle, and "Dolomite" is the lowermost.
- The data points cluster primarily along the "Limestone" curve, with some spread toward the "Sandstone" curve at higher porosities.
- The plot has a grid with major ticks every 0.05 on X and every 10 on Y.
- No regression equation or R² is printed.
> Тренд: Повышение нейтронной пористости (NPHI) коррелирует с увеличением времени прохождения акустической волны (DT), что соответствует увеличению пористости; данные преимущественно лежат вдоль кривой для известняка, с некоторым смещением к песчанику при высоких значениях пористости.

KEYWORDS: акустическое время прохождения, нейтронная пористость, NPHI, DT, песчаник, известняк, доломит, кривые пористости, кроссплот, интерпретация ГИС
----


Figure 8.4. Neutron-sonic crossplot and resulting lithology estimation, Fusselman Formation, West Texas. Data are from Figures 8.1 and 8.2. A lithology key is shown in Figure 8.6.
<!-- page 156 -->
Petrophysical Techniques

145


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
- Horizontal axis: Acoustic Wave Travel Time, DT, in μs/ft, linear scale, range 40 to 80.
- Vertical axis: Bulk Density, RHOB, in g/cm³, linear scale, range 2.00 to 3.00.
- Data points: black filled circles, scattered across the plot, with higher density in the lower-left region (DT ~50–65 μs/ft, RHOB ~2.60–2.80 g/cm³).
- Curves: five dashed lines labelled 0, 5, 10, 15, 20, 25, representing porosity (%) contours. These lines are straight and increasing from lower-left to upper-right, with slope decreasing as porosity increases.
- The curve labelled "0" starts at (DT=40, RHOB=2.00) and ends at (DT=80, RHOB=2.40).
- The curve labelled "5" starts at (DT=40, RHOB=2.10) and ends at (DT=80, RHOB=2.50).
- The curve labelled "10" starts at (DT=40, RHOB=2.20) and ends at (DT=80, RHOB=2.60).
- The curve labelled "15" starts at (DT=40, RHOB=2.30) and ends at (DT=80, RHOB=2.70).
- The curve labelled "20" starts at (DT=40, RHOB=2.40) and ends at (DT=80, RHOB=2.80).
- The curve labelled "25" starts at (DT=40, RHOB=2.50) and ends at (DT=80, RHOB=2.90).
- The data points cluster primarily between the 5% and 20% porosity curves, with a concentration near the 10–15% curve.
- There is a distinct cluster of points at DT ~75–78 μs/ft and RHOB ~2.80–2.85 g/cm³, lying near the 20–25% porosity curve.
- The overall trend is that as acoustic travel time increases, bulk density decreases, consistent with increasing porosity.
> Тренд: с увеличением времени прохождения акустической волны (DT) плотность (RHOB) уменьшается, что соответствует росту пористости — данные лежат вдоль кривых пористости 5–25%.

KEYWORDS: акустический импеданс, плотность, пористость, кривые пористости, DT, RHOB, кроссплот, геофизические данные, интерпретация ГИС, пористость по кроссплоту
----


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: FEET, increases downward. Depth range: 9100 ft to top of section (not fully visible). Depth scale: marked at 9100 ft, with tick marks at approximately 100-ft intervals.

Tracks:
- Left track: Depth scale (FEET MD), with major tick marks every 100 ft, minor ticks every 20 ft.
- Right track: Lithology column, with ornamentation and numerical scale from 0 to 1.

Lithology column details:
- Scale: 0 to 1, with 0 at right edge and 1 at left edge.
- Ornamentation:
  - White brick pattern (horizontal lines) — occupies most of the column, interpreted as sandstone or clean reservoir rock.
  - Diagonal hatching (косая штриховка) — appears in two irregular, lens-shaped zones near the top, interpreted as shale or clay interbeds.
  - Bottom section (below ~9100 ft) — dense stipple pattern (точечный крап), interpreted as shale or tight rock.
- No explicit legend provided within the image; lithology assignment is based on common log interpretation conventions for such ornamentation.

Interval table:
| Интервал, ft | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|--------------|--------------------------|-------------------|-------------------------------|
| 9100 — ~9200 | Средняя часть: белый кирпичный крап; верхняя часть: косая штриховка; нижняя часть: точечный крап | — | Нижняя часть — глина; средняя часть — песчаник с глинистыми прослоями; верхняя часть — песчаник с глинистыми линзами |

No other curves or interpretation panels (Кп, Кн, Кпр, etc.) are present.

KEYWORDS: well log, lithology column, depth scale, FEET MD, ornamentation, brick pattern, diagonal hatching, stipple, sandstone, shale, interbedded
----


Figure 8.5. Density-sonic crossplot and resulting lithology estimation, Fusselman Formation, West Texas. Data are from Figures 8.1 and 8.2. A lithology key is shown in Figure 8.6.


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
- X-axis: Lithology N, linear scale, range 0.30 to 0.80.
- Y-axis: Lithology M, linear scale, range 0.50 to 1.00.
- Data points: black dots, clustered into four groups.
- Group 1 (labelled "Calcite"): cluster at approximately (0.55, 0.80) to (0.58, 0.83).
- Group 2 (labelled "Sand"): cluster at approximately (0.58, 0.80) to (0.62, 0.82).
- Group 3 (labelled "Dolomite"): cluster at approximately (0.45, 0.70) to (0.50, 0.75).
- Group 4 (labelled "Anhydrite"): cluster at approximately (0.40, 0.60) to (0.45, 0.65).
- The clusters are separated by a curved boundary line drawn between the groups.
- No regression line, equation, or R² value is printed.
- The plot has a grid with major ticks every 0.10 on both axes.
> Тренд: Разделение литологических классов (Calcite, Sand, Dolomite, Anhydrite) по двум литологическим параметрам N и M, с визуальной границей между группами.
KEYWORDS: литология, диаграмма, кластеризация, параметр N, параметр M, кальцит, песок, доломит, ангидрит, разделяющая кривая
----


----
━━━ FORMAT 13: LEGEND / УСЛОВНЫЕ ОБОЗНАЧЕНИЯ ━━━
1 — кирпичный крап — Limestone
2 — косая штриховка — Dolomite
3 — точечный крап — Sandstone
4 — горизонтальная штриховка — Shale

KEYWORDS: литология, условные обозначения, кирпичный крап, косая штриховка, точечный крап, горизонтальная штриховка, известняк, доломит, песчаник, глина
----
━━━ FORMAT 4: CROSS-SECTION / РАЗРЕЗ ━━━
Ориентация: вертикальный разрез, глубина увеличивается вниз.
Глубинный диапазон: от 9100 до >9100 футов (FEET MD), единица — футы (FEET), MD — measured depth.
Вертикальная шкала: не указана, но интервалы между метками — 100 футов.
Литология по легенде:
- Кирпичный крап — известняк (Limestone)
- Косая штриховка — доломит (Dolomite)
- Точечный крап — песчаник (Sandstone)
- Горизонтальная штриховка — глина (Shale)

Стратиграфическая колонка (сверху вниз):
- Верхняя часть: тонкие слои доломита (косая штриховка) в известняке (кирпичный крап), с небольшими включениями песчаника (точечный крап).
- Интервал 9100 футов: мощный пласт известняка (кирпичный крап), с небольшими прослоями доломита и песчаника.
- Нижняя часть: переход к глине (горизонтальная штриховка) с включениями песчаника и доломита.

Нет данных о разломах, контактах ВНК/ГНК/ГВК, или других структурных элементах.

KEYWORDS: разрез, литология, глубина, футы, MD, известняк, доломит, песчаник, глина, кирпичный крап, косая штриховка, точечный крап, горизонтальная штриховка
----


Figure 8.6. M-N lithology crossplot and resulting lithology estimation, Fusselman Formation, West Texas. Data are from Figures 8.1 and 8.2.
<!-- page 157 -->
146

ASQUITH AND KRYGOWSKI


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
- X-axis: Apparent Matrix Travel Time, DTₘₐₓ, range 30–60, unit not specified, linear scale.
- Y-axis: Apparent Matrix Density, Rhoₘₐₓ, range 2.50–3.00, unit not specified, linear scale.
- Data points: black dots distributed in clusters, with no individual point labels.
- Four labelled points forming a quadrilateral: Quartz (top-right), Calcite (top-left), Dolomite (bottom-left), Anhydrite (bottom-right).
- Lines connect the four labelled points: Quartz–Calcite–Dolomite–Anhydrite–Quartz, forming a convex quadrilateral enclosing the data points.
- The data points lie within the quadrilateral, with clusters near Calcite, Dolomite, and Anhydrite.
- No regression lines, equations, or R² values are printed.
- No grid labels or tick marks are annotated beyond the axis ranges.
> Тренд: Плотность и время прохождения матрицы коррелируют с минералогией; данные группируются вблизи точек, соответствующих кварцу, кальциту, доломиту и ангидриту.
KEYWORDS: apparent matrix density, apparent matrix travel time, mineralogy, quartz, calcite, dolomite, anhydrite, crossplot, petrophysics, rock physics
----


Figure 8.7. Matrix identification plot (apparent matrix density vs. apparent matrix traveltime) and resulting lithology estimation, Fusselman Formation, West Texas. Data are from Figures 8.1 and 8.2. A lithology key is shown in Figure 8.6.


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
- X-axis: Apparent Matrix Cross Section, U_max, linear scale, range 4.00 to 16.00 (unit not specified).
- Y-axis: Apparent Matrix Density, Rb_max, linear scale, range 2.50 to 3.00 g/cm³ (unit inferred from context).
- Data points: 30–40 black dots scattered across the plot, concentrated in the central region (U_max ≈ 8.0–12.0, Rb_max ≈ 2.70–2.85).
- Overlay: a triangular ternary diagram with vertices labeled "Quartz", "Calcite", "Dolomite", and a fourth point labeled "Anhydrite" at the bottom right.
  - The ternary diagram has contour lines labeled 20, 40, 60, 80, representing percentage composition.
  - The "Quartz" vertex is at top-left (U_max ≈ 5.0, Rb_max ≈ 2.65), "Calcite" at top-right (U_max ≈ 14.0, Rb_max ≈ 2.65), "Dolomite" at bottom-center (U_max ≈ 8.0, Rb_max ≈ 2.90).
  - A separate point labeled "Illite" is located near (U_max ≈ 10.0, Rb_max ≈ 2.85), with a small square symbol.
  - The "Anhydrite" label is placed outside the triangle, near (U_max ≈ 15.0, Rb_max ≈ 2.95).
- The data points lie mostly within the quartz-calcite-dolomite triangle, with a few extending toward the illite point.
- The plot shows a negative correlation between U_max and Rb_max: as apparent matrix cross section increases, apparent matrix density decreases.
> Тренд: Увеличение U_max сопровождается уменьшением Rb_max, что соответствует переходу от кварца к кальциту и доломиту; данные точек лежат в пределах треугольника, что указывает на смешанную минералогию.

KEYWORDS: apparent matrix density, apparent matrix cross section, ternary diagram, quartz, calcite, dolomite, illite, anhydrite, mineral composition, petrophysical analysis
----


Figure 8.8. Matrix identification plot (apparent matrix density vs. apparent matrix capture cross section) and resulting lithologic estimation. Fusselman Formation, West Texas. Data are from Figures 8.1 and 8.2. A lithology key is shown in Figure 8.6.
<!-- page 158 -->
Petrophysical Techniques

147


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: FEET, increases downward. Depth range: 9100 ft to 0 ft (top of section at 0 ft, bottom at 9100 ft).

Tracks:
- Leftmost track: Lithology column with three distinct ornaments.
  - Top unit (from 0 ft to ~7000 ft): white background with horizontal brick-like hatching — ornament 1.
  - Middle unit (from ~7000 ft to ~8500 ft): grey background with diagonal hatching (косая штриховка) — ornament 2.
  - Bottom unit (from ~8500 ft to 9100 ft): grey background with dotted pattern (точечный крап) — ornament 3.

No other log curves or tracks are present.

Interval table:
| Интервал, ft | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|--------------|--------------------------|-------------------|-------------------------------|
| 0 — ~7000    | белый фон с горизонтальной кирпичной штриховкой | — | литология не определяется без легенды |
| ~7000 — ~8500| серый фон с косой штриховкой | — | литология не определяется без легенды |
| ~8500 — 9100 | серый фон с точечным крапом | — | литология не определяется без легенды |

KEYWORDS: well log, lithology column, depth scale, feet, ornament, кирпичная штриховка, косая штриховка, точечный крап, lithology interpretation, stratigraphic column
----


Figure 8.9. Lithologies from the matrix identification plot and porosities from the neutron-density crossplot, Fusselman Formation, West Texas.

$$
\alpha = 100\% (-130 \mathrm{mV})
$$

$$
\alpha = 75\% (-98 \mathrm{mV})
$$

$$
\alpha = 50\% (-65 \mathrm{mV})
$$

$$
\text{Shale baseline (0 mV)}
$$


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
This is a spontaneous potential (SP) log curve plotted against depth, with depth increasing downward. The curve is displayed on a grid with scale multipliers x100 (upper portion) and x200 (lower portion), indicating the vertical scale changes along the log.

The SP curve shows a negative deflection (anomaly) relative to the baseline, with the maximum negative value labeled as SSP = -130 mV. The curve shape is asymmetric: it begins with a gradual negative deflection, then steepens into a sharp trough, followed by a gradual return to baseline.

Two angles are marked on the curve:
- α₂₅ = 27° — the angle of the curve's slope at the 25% point of the deflection (likely measured from the baseline to the curve at 25% of the total deflection amplitude).
- α₅₀ = 45° — the angle of the curve's slope at the 50% point of the deflection.

Additional data provided in the figure:
- Rwf = 2.0 @ 120 °F — formation water resistivity at 120 °F.
- Ro = 0.04 @ 120 °F — mud filtrate resistivity at 120 °F.
- Tf = 120 °F — formation temperature.

The SP curve is interpreted as indicating a permeable zone with a negative anomaly, typical of a water-bearing sand in a shaly formation. The angles α₂₅ and α₅₀ are used for qualitative assessment of the SP curve shape, which relates to the formation's permeability and shale content.

> Тренд: Отрицательная аномалия SP с амплитудой -130 мВ, с уменьшающимся углом наклона от 45° (50% амплитуды) до 27° (25% амплитуды), указывает на проницаемый интервал с высоким содержанием глины.

KEYWORDS: SP, спонтанное потенциал, SSP, Rwf, Ro, Tf, α₂₅, α₅₀, кривая, аномалия, проницаемость, глина, каротаж, кривая SP, углы наклона, каротажная диаграмма


SP scale is \(20\mathrm{mV}\) /division

Figure 8.10. Determining alpha $(\alpha)$ from an SP log.

Two different cutoffs are demonstrated: $50\%$ alpha $(\alpha < 0.50)$ and $75\%$ alpha $(\alpha < 0.75)$. The alpha percentage is determined as an inverse function of shallowness [100% alpha $(1.0\alpha)$ is shale-free; $50\%$ alpha $(0.50\alpha)$ is shaly].

Given: You must first determine SSP. From Chapter 2:

$$
SSP = -K \times \log(R_{inf} / R_w) \tag{2.2}
$$

where:

$$
K = (0.133 \times T_f) + 60 \tag{2.3}
$$

and:

$$
R_{inf} = 2.0 \text{ at } 120^\circ\mathrm{F},
$$

$$
R_w = 0.04 \text{ at } 120^\circ\mathrm{F},
$$

$$
T_f = 120^\circ\mathrm{F}
$$

$$
SSP = -130 \mathrm{mV}
$$

Procedure:

1. From the formulas above, we determine that \( \mathrm{SSP} = -130 \, \mathrm{mV} \). Plot a scale of \( 130 \, \mathrm{mV} \) on the SP log, using the shale baseline as the zero point; then use the SP scale to establish the value of your scale increments (in this case, each increment is \( 20 \, \mathrm{mV} \)).
2. In this exercise, a thickness and depth will be determined for both \(\alpha < 0.50\) and \(\alpha < 0.75\), so draw vertical lines through the SSP scale approximately halfway (50%) and three-quarters of the way (75%) across, and draw vertical lines to intersect the SP curve at the desired depth range.
3. From the intersections, follow the values horizontally to the depth scale on the log. From this log-depth scale you can count depth increments to determine alpha thickness, as well as the top and bottom boundaries of the given alpha zone.

In this example $\alpha < 0.75$ is the thinner of the two, and measures 27 ft, from approximately x125 ft to x152 ft; whereas $\alpha < 0.50$ is thicker and measures 45 ft, from approximately x121.5 ft to x166.5 ft.
<!-- page 159 -->
148

ASQUITH AND KRYGOWSKI

Figure 8.11. Neutron-density-gamma ray log in the Mission Canyon Formation, Montana

Given: The volume of shale ($V_{shale}$) cutoff is arbitrarily set at 5% ($V_{shale} = 0.05$).

Next, determine the gamma ray index from the chart in Figure 3.2, Chapter 3

Gamma ray index, $I_{GR} = 0.10$ when $V_{shale} = 0.05$

Determine gamma ray cutoff (see log and Figure 3.2).

Remember:

$$I_{GR} = \frac{GR_{log} - GR_{min}}{GR_{max} - GR_{min}} \quad 3.1$$

where:

$GR_{log}$ = gamma ray log

$GR_{max}$ = gamma ray maximum (shale)

$GR_{min}$ = gamma ray minimum (shale-free sandstone or carbonate)

From the log:

$GR_{max}$ = 90 API units (from shale zone on log)

$GR_{min}$ = 12 API units (from clean carbonate zone on log)

$I_{GR} = 0.10$ ($I_{GR}$ for $V_{shale} = 0.05$; given)


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: increases downward, units not specified (assumed meters or feet, not labeled).
Track 1 (left): Gamma Ray (GR), scale 0–100 API units, linear scale, curve shown as a black line with irregular fluctuations.
- Curve behavior: 
  - From top to bottom: initial high reading (~80 API units), then a sharp drop to ~20 API units, followed by a gradual increase to ~40–50 API units, then a series of oscillations with amplitude varying between ~20–60 API units.
  - A dashed vertical line is drawn at approximately 20 API units, labeled "20 API Units", indicating a reference threshold or cut-off.
- No other tracks or curves are present.
- No interpreted intervals, bed boundaries, or perforation zones are marked.
- No results panel (Кп, Кн, etc.) is present.

KEYWORDS: ГК, API units, каротажная диаграмма, гамма-каротаж, кривая, порог 20 API, глубина, вертикальная шкала
----


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: increases downward, from 8600 to 8700 feet (MD — measured depth).
Tracks:
- Left track: depth scale in feet (MD), with grid lines every 10 feet.
- Right track: neutron porosity log (NPHI), scale from 0.1 to 0.3 (fractional porosity), with grid lines every 0.01.
  Curve: smooth, continuous, with multiple peaks and troughs; overall trend shows increasing porosity with depth.
  Marked interval: from approximately 8620 to 8680 ft, labelled "Interval of Mission Canyon bioherm development".
  Within this interval, a vertical dashed line marks "6 percent porosity" (0.06), which corresponds to the lower end of the NPHI scale.
  The curve remains above 0.06 throughout the interval, with values ranging from ~0.06 to ~0.25.

Interpretation:
- The NPHI curve indicates variable porosity, with higher values (up to 0.25) in the upper part of the interval and lower values near the base.
- The interval of Mission Canyon bioherm development is interpreted as a zone of interest with porosity consistently above 6%.
- No other curves or logs are present.

Interval table:
| Интервал, ft | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|--------------|------------------------|-------------------|-------------------------------|
| 8620–8680    | не определена          | NPHI: колебания от ~0.06 до ~0.25 | Interval of Mission Canyon bioherm development, porosity > 6% |

KEYWORDS: well log, neutron porosity, NPHI, Mission Canyon, bioherm, porosity, depth, measured depth, interval, interpretation
----


Then, rearranging the equation above to solve for $GR_{log}$:

$GR_{log} = 19.8$ (round off to 20 API units)

20 API units represents clean carbonate where the volume of shale is equal to (or less than) 5%.

Draw a vertical line from the scale value of 20 API units and determine the thickness and limits of the clean carbonate formation (bioherm) much as you determined alpha values in Figure 8.10.

Figure 8.12. Isopach map of clean carbonates from the Mississippian Mission Canyon Formation, Roosevelt County, Montana, described in the text and in Figure 8.11.


----
━━━ FORMAT 3: MAP / КАРТА ━━━
Тип карты: изолинейная карта (вероятно, изопахитовая или структурная), с изолиниями, обозначающими значения от 0 до 6.
Направление: север указан стрелкой "N" справа, северо-восточное направление (N–E) подтверждается метками "R 55 E" вверху и "T 29 N" справа.
Масштаб: не указан.
Сечение изолиний: не указано, но значения на изолиниях: 0, 1, 2, 3, 4, 5, 6.
Значения изолиний: 0, 1, 2, 3, 4, 5, 6 — расположены по часовой стрелке от центра, с максимальным значением 6 в центре.
Географические метки: "R 55 E" (вероятно, линия меридиана или координатная сетка), "T 29 N" (вероятно, параллель или координатная сетка).
Сетка: квадратная сетка с плюсами (+) в узлах, без указания масштаба или единиц.
Структурные элементы: изолинии образуют эллиптическую форму, сжатую с севера на юг, с центром в нижней части карты. Максимум (6) расположен в центре, минимум (0) — на периферии.
Контур: внешняя изолиния 0 — граница области с нулевым значением.
Нет обозначенных скважин, разломов, контуров нефтеносности или других геологических объектов.
Нет легенды.
KEYWORDS: карта, изолинии, изопахит, структурная карта, координатная сетка, R 55 E, T 29 N, изолинии 0-6
----


<!-- page 160 -->
Petrophysical Techniques

149


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
Ось абсцисс: φₕ, без единиц, линейная шкала, диапазон от 0 до 24.
Ось ординат: R, без единиц, логарифмическая шкала, диапазон от 10 до 10,000.
На графике изображены два областных контура, обозначенные пунктирной линией.
Внутри верхнего контура: надпись "INTERSTITIAL MICROCRYSTALLINE ANHYDRITE DOLOMITE", внутри него размещены точки (•) и квадраты (▪).
Внутри нижнего контура: надпись "SUBIDIAL POROSITEROUS SUCROSE DOLOMITE", внутри него размещены точки (•) и квадраты (▪).
Вдоль правой границы графика — вертикальная шкала с надписью "SUBSTITUTIONAL ANHYDRITE" и "SUBSTITUTIONAL ANHYDRITE", с отметками от 0 до 100, с шагом 20.
Точки и квадраты распределены в двух областях: верхняя область — при φₕ от 0 до 8, R от 100 до 10,000; нижняя область — при φₕ от 0 до 12, R от 10 до 100.
> Тренд: Две группы данных, соответствующие различным типам доломита, с различными значениями пористости φₕ и сопротивления R; верхняя группа — интерстициальный микрокристаллический ангидритовый доломит, нижняя — субидиальный пористый сахаровидный доломит.
KEYWORDS: пористость, сопротивление, доломит, ангидрит, микрокристаллический, сахаровидный, интерстициальный, субидиальный, логарифмическая шкала, XY-график
----


Figure 8.13. Example crossplot of formation resistivity, $R_{f}$ (in this case from a deep laterolog) vs. neutron porosity.

This comparison of log response to facies helps the geologist develop rock-type clusters. This example is from the Ordovician Red River C and D zones and Richland and Roosevelt Counties, Montana (after Asquith, 1979).

Solid squares and circles represent wells with core or cuttings available, in addition to log response. Open circles represent wells with log control only. Facies classifications are first confirmed by core or cuttings analysis, but once clusters are established only log control is necessary for facies prediction.


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
Ось абсцисс: β₃, безразмерная величина, линейная шкала, диапазон от 0 до 28.
Ось ординат: ε, безразмерная величина, логарифмическая шкала, диапазон от 1 до 10,000.
На графике изображены три областных кластера точек, каждый с подписью:
- "OOLITE GRAINSTONE" — эллипсоидальная область, расположенная при β₃ ≈ 20–24, ε ≈ 10–100.
- "ARCOILACEOUS BIOCLASTIC WACKESTONES" — эллипсоидальная область, расположенная при β₃ ≈ 8–12, ε ≈ 1–10.
- "OOLITIC WACKESTONES" — вытянутая областная форма, расположенная при β₃ ≈ 0–6, ε ≈ 10–1000.
Точки внутри областей обозначены кружками с точками (••••••••••).
> Тренд: С увеличением β₃ наблюдается уменьшение ε, при этом различные типы карбонатных пород группируются в отдельные кластеры на плоскости β₃–ε.
KEYWORDS: β₃, ε, оолитовые зернистые породы, аркоилакеозные биокластические ваккестоны, оолитовые ваккестоны, карбонатные породы, диаграмма рассеяния, логарифмическая шкала, кластеризация, литология
----


Figure 8.14. Example crossplot of formation resistivity ($R_{f}$) (in this case from deep induction) with sonic porosity ($\phi_{s}$).

As with Figure 8.13, the rock-type clusters are developed by core or cuttings analysis, but well logs are all that's necessary once the relationship is defined. This example comes from the Lower Permian Council Grove B-zone, Ochiltree County, Texas. After Asquith (1979).

Open circles represent wells with both core/cuttings analysis and log control. Solid black circles represent wells with only log control.


----
━━━ FORMAT 3: MAP / КАРТА ━━━
Тип карты: геологическая карта распределения литологических фаций (песчаники, известняки) в нефтяном месторождении.
Масштаб: 1:100 000 (по линейке — 1 дюйм = 2 мили, что соответствует ~1:126 720, но в карте указано "MILES", и линейка 0–2 мили).
Направление: север указан стрелкой "N" в правом верхнем углу.
Легенда (условные обозначения):
- Кирпичный крап — >60% DOLOLITE GRAINSTONE (доломитовый гравелит)
- Точечный крап — >65% DOLOLITE WACKESTONE (доломитовый ваккестон)
- Косая штриховка — >65% ARGILLACEOUS WACKESTONE (глинистый ваккестон)
- Пунктирная линия — LOG CONTROL (контроль по данным ГИС)
- Тонкая сплошная линия — CORE + LOG CONTROL (контроль по керну и ГИС)
- Толстая сплошная линия — CUTTINGS + LOG CONTROL (контроль по керну и ГИС)

На карте отмечены:
- Границы штатов: OKLAHOMA, TEXAS.
- Границы округов: Hensford County, Ochiltree County.
- Названия населённых пунктов: Perryton, Farnsworth, Waka.
- Сетка скважин: обозначены точки (скважины) по всей площади месторождения.
- Литологические зоны:
  - Центральная зона — >60% DOLOLITE GRAINSTONE (кирпичный крап).
  - Внешняя зона — >65% DOLOLITE WACKESTONE (точечный крап).
  - Южная и западная части — >65% ARGILLACEOUS WACKESTONE (косая штриховка).
- Контур месторождения: обозначен толстой сплошной линией (CUTTINGS + LOG CONTROL).

Структурные элементы:
- Нет изогипс, нет указания структурных высот.
- Нет разрывов или сбросов.
- Нет внешнего или внутреннего контура нефтеносности.

KEYWORDS: геологическая карта, литологические фации, доломитовый гравелит, доломитовый ваккестон, глинистый ваккестон, контроль по керну, контроль по ГИС, месторождение, Оклахома, Техас
----


Figure 8.15. Example facies map of the Lower Permian Council Grove B-zone, Ochiltree County, Texas.

The map was prepared from the facies clusters established by crossplotted log data in Figure 8.13. After Asquith (1979). The legend defines the position of core, cuttings, and log-only control.
<!-- page 161 -->

<!-- page 162 -->
9

Hurley, Neil, 2004, Borehole Images, in G. Acquith and D. Krygowski, Basic Well Log Analysis: AAPG Methods in Exploration 16, p. 151-163.

# Borehole Images

## GENERAL

Borehole images are electronic pictures of the rocks and fluids encountered by a wellbore. Such images are made by electrical, acoustic, or video devices which have been lowered into the well. Images are oriented, they have high vertical and lateral resolution, and they provide critical information about bedding dip, fractures, faults, unconformities, paleocurrent directions, vuggy and fracture porosity, and other geological features. Case studies have shown that borehole images are best used in conjunction with other available wellbore data, such as other logs, cuttings, cores, and production data.

Because of the high expense and risk, relatively few wells are now being cored. Cores taken are generally short, so they may miss all or part of the target formation. In exploration wells, the depth to the target formation may even be unknown. Some lithologies tend to have poor core recovery, such as unconsolidated sands, and fractured, vuggy, or brecciated intervals. In some cores, the electrical or acoustic contrast between different lithologies may be more significant than the contrast apparent to the human eye. In recent years, all of these factors have led to the increased use of borehole images to characterize subsurface sedimentary rocks. This chapter provides a guide to the acquisition, processing, and interpretation of borehole images.

## ELECTRICAL BOREHOLE IMAGES

Electrical borehole images are based on dipmeter technology that has been commercially available since the 1950s (Bigelow, 1985a, b, c, d, e; Gilbreath, 1987; Adams et al., 1987). Figure 9.1 is an illustration of the tool configuration and basic principles behind dipmeter logs. Electrical borehole-imaging tools are, in essence, sophisticated dipmeters. The imaging tools have microresistivity electrodes arranged around the

wellbore on pads that are pressed against the borehole wall. The evolutionary trend from dipmeters to borehole images has been from a few electrodes to a complex array of electrodes on multiple pads (Figure 9.2).

*Data Acquisition*—Tools are first run into the hole with the pads closed. At the start of the log run, either four, six, or eight pads are pressed against the borehole wall. The number of pads depends on the logging device which is being used (Table 9.1). Electrical current is forced into the rock through the electrodes, and remote sensors measure the current after it interacts with the formation (Figure 9.3). Raw data include multiple electrode readings, caliper readings from individual pads or pairs of pads, and $x$-, $y$-, and $z$-axis accelerometer and magnetometer readings. Borehole deviation and pad 1 (tool) orientation are determined from the magnetometers.

The sample rate for electrode and accelerometer data is very high, normally 120 samples/ft (400 samples/m). Because of this, digital file size can be quite large. In fact, it is common to record tens to hundreds of megabytes of data from one log run. Areal coverage of the borehole face is a function of width of the electrode arrays, number of pads, and borehole diameter. In general, 40 to 80% of the borehole face is imaged in typical boreholes. Unimaged parts of the borehole appear as blank strips between the pads. Depth of investigation is small, generally less than 1 in (2.5 cm) into the formation (Williams et al., 1997). Logging rate, which is comparable to other openhole logs, is 1,600 to 1,800 ft/hr (500 to 550 m/hr). Because they are electrical devices, the drilling mud must be conductive. Mud resistivities higher than 50 ohm-m are unsuitable for most electrical borehole images, although commercial tools are now available for oil-based muds. The best images are acquired when the ratio between formation and mud resistivity is less than 1,000 (Grace and Newberry, 1998). Pressure and temperature limitations are comparable to those placed

151
<!-- page 163 -->
152

HURLEY

Table 9.1. Electrical Borehole-Imaging Tools

|  Company | Trade Name | Number of Pads | Number of Electrodes | Useful References  |
| --- | --- | --- | --- | --- |
|  Halliburton | EMI (Electrical Micro Imaging Tool) | 6 | 150 | Seiler et al. (1994)  |
|  Schlumberger | FMS (Formation MicroScanner) | 4 | 64 | Ekstrom et al. (1986)  |
|  Schlumberger | FMI (Formation MicroImager) | 8 | 192 | Grace and Newberry (1998)  |
|  Baker Atlas | STAR (SimulTaneous Acoustic and Resistivity Imager) | 6 | 144 | Lacazette (1996)  |

on conventional logging tools. For example, the EMI tool is designed to withstand 350° F (177° C) temperature and 20,000 psi (137,900 kPa) pressure. Electrical borehole images can only be acquired openhole. Currently, there are no cased-hole applications.

### Data Processing

A processed electrical borehole image is basically a map of rock resistivity at the borehole face. Because it is more difficult to examine borehole images in 3-D, it is common to split the borehole along true north, then unroll the cylinder until it becomes a 2-D view (Figure 9.4). In highly deviated and horizontal wells, it is common to split the borehole image along the top of the hole (Figure 9.5). Planar features that intersect the cylindrical borehole appear as sine waves in the 2-D view.

Data processing is done by service companies or individuals on workstation, PC, or mainframe computers using commercially available or proprietary software. Processing steps involve correcting the directional data, that is, pad 1 azimuth (tool orientation) and hole azimuth, for magnetic declination. Some programs also correct for magnetic inclination. Note that magnetic declination varies with time and space. Charts and computer programs are available to compute magnetic declination for any location in the world on any logging date. Next, accelerometer corrections are applied, making sure that the accelerometer curve is on depth with the resistivity traces. The accelerometer accounts for differential sticking, speed variations, and resonant vibrations that occur as the tool moves up the hole (Figure 9.6). Finally, resistivity traces must be depth shifted using physical tool specifications, so that different rows of buttons are in line where the same slice of the borehole, perpendicular to the tool, was imaged. At very small scales (less than 6 in; 15 cm), nonlinear depth shifts occur that may not be correctable by conventional data-processing algorithms.

As a result, not every surface that shows electrical contrast is exactly on depth.

Borehole images are created by assigning color maps to different bins or ranges of resistivity values. Colored pixels are then arranged in their proper geometric position around the wellbore. By convention, low-resistivity features, such as shales or fluid-filled fractures, are displayed as dark colors. High-resistivity features, such as sandstones and limestones, are displayed as shades of brown, yellow, and white (Figures 9.7 and 9.8).

Two main types of processed borehole images are available: static and dynamic (Figure 9.9). Static images are those which have had one contrast setting applied to the entire well. They provide useful views of relative changes in rock resistivity throughout the borehole. Static images can be calibrated in ohm-m to devices such as the LLS (Shallow Latero-log), a shallow-reading resistivity log. With normal processing, borehole images are uncalibrated. Images can be corrected for EMEX voltage, a background voltage that is adjusted on the logging truck to improve image quality. Dynamic images, which have had variable contrast applied in a moving window, provide enhanced views of features such as vugs, fractures, and bed boundaries. Dynamic images bring out subtle features in rocks that have very low resistivities, such as shales, and very high resistivities, such as carbonates and crystalline rocks.

### ACOUSTIC BOREHOLE IMAGES

Acoustic borehole images, also known as borehole televiewers, are based on technology first developed in the 1960s (Zemanek et al., 1970). In these tools, which are centralized in the well, a rotating transducer emits and records sound waves which bounce off of the borehole wall (Figure 9.10). Both acoustic amplitude and travel time are recorded and processed into images.
<!-- page 164 -->
Borehole Images

153

## Data Acquisition

The tool is run into the hole with a stiff, spring-like centralizer. It is very important that the transducer is in the center of the well because reflections must strike the borehole wall and return to the tool at the proper reflection angle (Figure 9.11). The transducer rotates as it emits and records signals. The frequency of the emitted signal is generally in the several hundred kilohertz range. The CBIL tool, for example, rotates at a rate of 6 revolutions/s, and has a sample rate of 250 samples/rotation. Vertical resolution is about 0.3 in (0.8 cm) at a logging speed of 1200 ft/hr (365 m/hr). Commercially available tools and the associated service companies are listed in Table 9.2. Acoustic borehole images basically acquire a spiral trace of first-arrival amplitude and travel time to and from the borehole face. Acoustic caliper readings can be extracted from the logs. Orientation and borehole deviation are computed from an attached orientation device with x-, y-, and z-axis magnetometers. Accelerometer readings may or may not be recorded.

Table 9.2. Acoustic Borehole-Imaging Tools

|  Company | Trade Name | Useful References  |
| --- | --- | --- |
|  Halliburton | CAST (Circumferential Acoustic Scanning Tool) | Seiler et al. (1990)  |
|  Schlumberger | UBI (Ultrasonic Borehole Imager) | Schlumberger (1993)  |
|  Baker Atlas | CBIL (Circumferential Borehole Imaging Log) | Baker Atlas Web Page  |
|  Baker Atlas | STAR (SimulTaneous Acoustic and Resistivity Imager) | Lacazette (1996)  |

Again, because the sample rate is high, digital file size can be large. As with electrical images, it is common to record tens to hundreds of megabytes of data from one log run. Depth of investigation is zero, because this logging tool truly images the exposed borehole face. Areal coverage of the borehole face is 100%, which is a significant advantage of these tools. Vertical resolution is a function of logging rate, which is generally slower than other openhole logs. Maximum resolution (100 samples/in) for the openhole

CAST, for example, requires a rate of 1200 ft/hr (365 m/hr). Because these devices do not depend on electrical conductivity, they can be run in nonconducting muds. In fact, the ability to run in oil-based mud has been a major advantage of this tool. Because of signal dispersion, acoustic imaging logs do not work well with mud weights in excess of 12 pounds/gallon (1.44 kg/l). Also, because of increased travel time, the tools do not perform well if borehole diameter exceeds 12 in (30 cm). Pressure and temperature limitations are comparable to the those placed on conventional logging tools. The CAST tool, for example, is designed to withstand 350° F (177° C) temperature and 20,000 psi (137,900 kPa) pressure. Acoustic images are useful in both cased and openhole applications.

## Data Processing

Acoustic borehole images are basically compressed helical ultrasonic travel time or amplitude maps of the borehole wall. Data processing is normally done by service companies or individuals on workstation, PC, or mainframe computers using commercially available or proprietary software packages. Logging companies generally provide files in which the images have been corrected to true north. Individual amplitude and travel-time measurements are assigned colors based upon their different ranges of values. Colored pixels are arranged in their proper geometric position around the wellbore. By convention, low-amplitude or high travel-time features, such as shales, borehole irregularities (breakouts, washouts), and fluid-filled fractures are shown as dark colors (Figure 9.12). High-amplitude or low travel-time features, such as sandstones and limestones, are shown as shades of brown, yellow, and white. Accelerometer corrections are applied if they are available.

Acoustic borehole images have the cylinder split into 2-D views along true north, or along the top of the hole in deviated wells, in a manner illustrated in Figures 9.4 and 9.5. Planar features which intersect the borehole appear as sine waves in the 2-D view. Static and dynamic images can be created, as with electrical borehole images.

## DOWNHOLE VIDEO IMAGES

Downhole photographic images have been available since the 1960s (Mullins, 1966). However, limitations on the strength of the light source, maximum temperatures allowed, and data-transmission capabilities prevented them from gaining widespread acceptance. In recent years, however, better light sources,
<!-- page 165 -->
154

HURLEY

more robust tools, oil-resistant coatings on lenses, and fiber-optic logging cables (Lau et al., 1987; Cobb and Schultz, 1992) have allowed these tools to emerge as viable options in the field of borehole imaging (Figure 9.13).

## Data Acquisition and Processing

The downhole video tool is run into the hole with a centralizer. A light source can be placed above or below the camera. Mirrors are generally placed so the operator has a fish-eye view of the well. Some devices allow the operator to have a sideways view of the well. The video is seen in real time and recorded at the surface. Borehole coverage is 100%; depth of investigation is zero because this logging tool images only the exposed borehole face. Logging rate is chosen by the operator at the surface. Because the images are processed instantly, it is possible to stop the tool to watch fluid flow, or to revisit the same depth a number of times. The tool works in liquid-filled or gas-filled wells, but borehole fluids must be relatively clear. A common misconception is that the tool does not work in flowing or pumping oil wells. If the well has any deviation and water cut, oil flows along the top of the hole, and the video can be acquired in the water-filled part of the hole (Whittaker and Linville, 1996). As an alternative, the well can be shut in and filled with water. The video can record what happens as the well is put on production. Temperature and pressure limitations on Halliburton's downhole video tool, for example, are 225° F (107° C) and 10,000 psi (69,000 kPa). Video images are more widely used in cased-hole studies, although they have important openhole applications.

## EMERGING TECHNOLOGIES: OTHER BOREHOLE IMAGES

With the demonstrated success of conventional borehole images, the oilfield service industry continues to try to generate images using other types of logging tools. Azimuthal resistivity images, obtained from a segmented laterolog-type device, have been described by Davies et al. (1992), Al-Waheed et al. (1994), and Smits et al. (1995). Resistivity images acquired at the bit using a measurement-while-drilling approach have been described by Rosthal et al. (1995) and Bonner et al. (1996). Azimuthal density images, also obtained while drilling, have been described by Bornemann et al. (1998).

## BOREHOLE-IMAGE INTERPRETATION

In practice, the log interpreter scrolls through the processed log on a computer workstation or PC, viewing static or dynamic images while fitting sine waves to observed bed boundaries, fractures, and other geologic features. Automated dip-picking programs are available, and the interpreter can choose to edit dips that have already been picked by various computer algorithms. This section outlines the most important uses of borehole images. A steadily increasing number of studies have used these tools. A set of reprints edited by Paillet et al. (1990) provides a good historical reference volume. In addition, a bibliography of borehole-image articles is maintained by S. Prensky on the SPWLA website.

## Fracture and Fault Occurrence and Orientation

The most obvious use of borehole images is in the area of structural interpretation, especially detecting and orienting fractures and faults (Figures 9.7 and 9.8). In some cases, a fault plane can be imaged and oriented. This is especially true for microfaults, which may have offset amounts of only a few inches (or cm). In other cases, faults correspond to washouts and may be poorly imaged. If this happens, the interpreter can look at nearby fractures, which may relate to fault orientation. Changes in bedding orientation may indicate that the borehole has crossed a fault or a fold axis (Bengsten, 1981, 1982; Bigelow, 1985d; Koepsell et al., 1989a, b; Hurley et al., 1994; Knight, 1999). Boundaries between bedding-plane dip domains, or consistent groups of dips, might be faults or unconformities (Hurley, 1994). For dip-slip faults, stereonet analysis of deformed beds above and below the fault can be used to determine the fault's strike azimuth.

Fracture analysis is typically done using stereonets which show various fracture sets (Younes et al., 1998). One can use borehole images to differentiate open fractures from healed fractures. Because the mud is conductive, an open fracture appears as a dark trace on an electrical borehole image. Note that shale-filled fractures could also appear as dark traces on electrical borehole images. Other logs, such as the gamma ray, can help resolve such situations. If the fracture is filled with cement such as calcite, anhydrite, or quartz, the fracture might appear as a resistive (white) trace on the electrical borehole image. Healed fractures in acoustic logs might appear on the amplitude but not the travel-time images.

Natural and induced fractures can be differentiated
<!-- page 166 -->
Borehole Images

155

in some cases. Natural fractures can occur as one or more fracture sets, each with a distinct orientation. Induced fractures (Figure 9.12) are commonly near vertical, have a well defined strike azimuth, can cut across beds of different lithology (for example, sands and shales), and have a strike azimuth that is perpendicular to borehole breakouts, or oval elongations of the borehole. In deviated holes, induced tensile-wall fractures can occur as en echelon sets that do not cross the entire width of the borehole image (Barton et al., 1997).

## Fracture Aperture

In the parallel-plate model for fluid flow in fractures (Brown, 1987), permeability is proportional to the square of fracture-aperture width (Figure 9.14). Because fractures are not truly parallel plates, flow estimates must be modified to account for asperities, or irregularities, along the fracture walls (Brown, 1987). Because of the important relationship between permeability and aperture width, geologists and engineers are interested in aperture widths in boreholes.

Luthi and Souhaite (1990) modeled fracture aperture widths as recorded by electrical borehole images. They derived a method for aperture-width calculation using mud resistivity as the main input parameter. Based upon their technique, commercial software (available from Schlumberger) calculates aperture widths from electrical borehole images. Svor and Meehan (1991a, b) used this approach to create a grading system for fractures, and they related this to ultimate recovery in Austin Chalk horizontal wells.

## Borehole Breakouts, In Situ Stress Interpretation

Borehole breakouts (Figure 9.12), which can be measured using the caliper logs from electrical or acoustic borehole-imaging tools, commonly indicate the orientation of present-day *in situ* stress (Bell and Gough, 1979; Zoback et al., 1985; Plumb and Hickman, 1985; Springer, 1987; Parker and Heffernan, 1993; Barton et al., 1997). Borehole breakouts, when combined with the orientation of inferred natural and induced fracture sets, may be related to directional permeability in the subsurface (Heffer and Lean, 1993; Haws and Hurley, 1992). This information has considerable application to optimizing the orientation of horizontal wells and configuring injection patterns in secondary and tertiary recovery schemes. Also, the orientation of artificially induced fractures is generally parallel to the orientation of present-day maximum horizontal *in situ* stress.

## Stratigraphic Interpretation

Conventional stratigraphic interpretation from dipmeters (Bigelow, 1985e; Gilbreath, 1987), involves looking for steepening upward or shallowing upward patterns in bedding dips. Combined with core, other log signatures, and isopach maps, such interpretations can lead to new well locations (Grace and Newberry, 1998).

Authors such as Bourke et al. (1989), Höcker et al. (1990), and Bourke (1992) have shown that sedimentologic and stratigraphic interpretations from core and other logs can be combined with dipmeter results to improve reservoir characterization in clastic rocks.

Hurley (1994) showed that boundaries between dip domains can be subtle angular discordances between overlying and underlying sedimentary strata. Dip domains are groups of consistent dips that may be structural blocks or sequences at seismic scale. Berg (1998) used synthetic deviation plots with a similar objective. The recognition of unconformities can be important in detecting reservoir compartments and in making sequence-stratigraphic interpretations. In horizontal wells, borehole images combined with deviation surveys and other logs can provide powerful tools for the interpretation of fine scale (cm to m) microstratigraphy (Hurley et al., 1994)

In cyclic, well-bedded units, borehole images can be used to construct modified Fischer plots for parasequence-scale correlations (Hurley, 1996; Witton, 1999). The resulting curve has a distinctive shape which is based on changes in cycle thickness. This curve can be used like a well log to correlate cycles between wells, look for missing section, and hypothesize about changes in sea level or channel migration.

## Sedimentologic Interpretation

Sedimentologic interpretations are aided by the fact that the intrinsic lower resolution limit of borehole images is on the order of 0.2 in (5 mm). With electrical images, one can image conductive fractures in resistive rock that are fractions of a millimeter in width. Although grain types generally cannot be discerned, features such as burrows (Figure 9.15), clasts, vugs, and breccias are common. Vug shape can be diagnostic for certain fossils.

Vug quantification from borehole images using pixel-counting techniques has led to the recognition of flow units and bypassed pay in some reservoirs (Newberry et al., 1996; Martin et al., 1997; Hurley et al., 1998).

Baseline color shifts in static images can indicate
<!-- page 167 -->
156

HURLEY

changes in the type or amount of matrix porosity. Cemented versus open-fracture and breccia porosity can commonly be imaged. Sedimentary structures, such as fluid-escape features, ripples, cross beds, and imbricated clasts can be apparent (Figure 9.16). The observation of such structures may yield paleocurrent, facies, and depositional environment interpretations (Luthi and Banavar, 1988; Carr et al., 1997; Witton, 1999).

Thinly bedded sands and shales have bedding thicknesses on the scale of 2 to 20 in (5 to 50 cm). Such beds are below the resolution limits of most logging tools. Thin beds have been successfully resolved and quantified using borehole images (Sovich et al., 1996). Such analyses have led to better estimates of net reservoir thickness to gross reservoir thickness and improved volumetric calculations (Reid and Enderlin, 1998).

## REVIEW

1. The three most common types of borehole images are electrical, acoustic, and downhole video. The advantage of these tools is that they give high-resolution pictures of the geologic features that occur in the borehole. Borehole images are best used in combination with other logs and rock information to allow more definitive interpretations of the downhole log signatures.

2. Electrical borehole-imaging logs are sophisticated dipmeters. Arrays of electrodes occur on 4, 6, or 8

pads which are pressed against the borehole wall. Images are resistivity maps of the borehole face.

3. Electrical images are generally run in conducting mud. They work because there is resistivity contrast between various lithologies, like sands and shales, and mud-filled fractures.

4. Acoustic borehole images have a rotating transducer which emits a high-frequency sound signal that bounces off of the borehole wall. Processed images are helical maps of acoustic amplitude and travel time for the reflected sound waves.

5. Acoustic images can be run in oil-based mud. They work because there is commonly acoustic contrast between different lithologies, mud-filled fractures, and borehole irregularities such as washouts or breakouts.

6. Downhole video logs have seen significant technological improvements, especially in the form of fiber-optic cables. They provide real-time, dynamic images of the well and flowing fluids. They are useful for casing inspection, fluid-flow documentation, fracture detection, and other applications, assuming the borehole fluid is relatively clear.

7. Borehole images have been used to document fracture and fault occurrence and orientation, fracture aperture widths, borehole breakouts and *in situ* stress orientation. They are also commonly used for stratigraphic and sedimentologic interpretations, including paleocurrent analysis, vug quantification, and thin-bed detection.
<!-- page 168 -->
Borehole Images

157


----
━━━ FORMAT 9: TECHNICAL SCHEMATIC / ТЕХНИЧЕСКАЯ СХЕМА ━━━
This schematic illustrates the internal components and operational principle of a borehole imaging tool, likely a micro-resistivity or micro-imagery tool (e.g., micro-resistivity array or FMS-type tool), showing the arrangement of sensors and the direction of electrical current flow from the pads to the detector.

The central cylindrical body represents the tool string, suspended by a wireline at the top. The tool contains the following components, arranged vertically from top to bottom:
- 3-Axis Accelerometer — located near the upper part of the tool body.
- 3 Magnetometers — located below the accelerometer.
- A central detector (not explicitly named, but implied as the receiver for electrical current) — positioned at the lower end of the tool body.

At the bottom of the tool, four pads (Pad 1, Pad 2, Pad 3, Pad 4) are radially deployed outward from the tool body. Each pad is connected to the central detector via dashed lines, which represent the lines of electrical current moving from the pads to the detector. The direction of current flow is indicated by arrows along these dashed lines, showing that current flows from each pad toward the central detector.

The pads are arranged symmetrically around the tool, with Pad 1 at the right, Pad 2 at the bottom, Pad 3 at the left, and Pad 4 at the top (from the viewer's perspective). The schematic emphasizes the radial deployment of the pads and the electrical circuitry connecting them to the central sensor array.

The diagram also includes a note: "Arrows Show Lines of Electrical Current Moving from Pads to Detector", clarifying the function of the dashed lines and arrows.

This schematic demonstrates the physical layout and electrical measurement principle of a borehole imaging tool, where current is injected from the pads into the formation and measured at the central detector to create resistivity images of the borehole wall.

KEYWORDS: буровой инструмент, микрорезистивиметр, FMS, пады, ускорометр, магнитометр, электрический ток, схема, изображение скважины, каротаж
----


Figure 9.1. Basic principles of electrical dipmeter tools are illustrated by this diagram of Schlumberger's SHDT (Stratigraphic High Resolution Dipmeter Tool), which became commercially available in 1982. Two measuring electrodes on each of four pads generate eight raw electrode traces, as shown at the bottom. Magnetometers measure borehole deviation. Accelerometers record high-frequency tool-speed variations which occur as the tool is being run. Formation dip is computed from planes that are fit through correlative peaks and troughs on the speed-corrected electrode traces. Caliper logs record borehole diameter between pads 1 and 3 and between pads 2 and 4. After Schlumberger (1983) and Häcker et al. (1990).


----
━━━ FORMAT 9: TECHNICAL SCHEMATIC / ТЕХНИЧЕСКАЯ СХЕМА ━━━
The schematic illustrates the evolution of electrical borehole imaging tools, showing the number of pads, button count per pad, button diameter, and total buttons for four generations: SHDT (1982), FMS (1988), EMI (1991), and STAR (1996). Each tool is represented by a top-down view of the pad array and a side view of the sonde.

For SHDT (1982):
- 4 Pads (top-down view: circular with cross-hatching indicating four quadrants)
- Side view: cylindrical sonde with two buttons shown
- 10 mm/diameter
- 8 buttons total

For FMS (1988):
- 4 Pads (top-down view: circular with cross-hatching indicating four quadrants)
- Side view: cylindrical sonde with 16 buttons shown (arranged in two rows of 8)
- 6.7 mm/diameter
- 64 buttons total

For EMI (1991):
- 4 Flaps, 4 Pads (top-down view: circular with cross-hatching indicating four quadrants, with flaps shown as extensions)
- Side view: cylindrical sonde with 24 buttons shown (arranged in three rows of 8)
- 5 mm/diameter
- 192 buttons total

For EMI (1994):
- 6 Pads (top-down view: circular with six radial segments)
- Side view: cylindrical sonde with 25 buttons shown (arranged in five rows of 5)
- 5 mm/diameter
- 150 buttons total

For STAR (1996):
- 6 Pads (top-down view: circular with six radial segments)
- Side view: cylindrical sonde with 24 buttons shown (arranged in four rows of 6)
- 4 mm/diameter
- 144 buttons total

KEYWORDS: буровой имиджер, электрический имиджер, SHDT, FMS, EMI, STAR, пад, кнопка, диаметр, количество кнопок, сонд, схема инструмента
----


Figure 9.2. Schematic illustration of pad and electrode configurations for one commercially available dipmeter and all of the common electrical borehole-imaging logs. Numbers in parentheses represent the year in which the tool was released. Refer to Table 9.1 for tool and company names. Modified from Grace and Newberry (1998).
<!-- page 169 -->
158

HURLEY

Figure 9.3. Basic elements of electrical borehole-imaging tools. Electrical currents pass through button arrays into the formation. Current drop is recorded at a remote detector. Magnetometers record borehole deviation, and accelerometers record speed variations. The processed borehole image is a speed-corrected resistivity map of the borehole well. Modified from Williams et al. (1997).


----
━━━ FORMAT 9: TECHNICAL SCHEMATIC / ТЕХНИЧЕСКАЯ СХЕМА ━━━
The schematic illustrates the design and operational principle of a formation resistivity logging tool, likely a microresistivity or microimager tool, with emphasis on the pad contact mechanism and current flow path.

The left panel shows a cross-sectional view of the tool in the borehole:
- A central wireline extends vertically through the tool.
- The tool body is shown with an "Insulated Section" near the bottom, which isolates the lower part from the borehole fluid.
- Current flows from the tool into the formation through a "Pad" at the bottom, with the direction indicated by an arrow and a dashed arc.
- The "Current Return" path is shown as returning through the borehole fluid and the upper part of the tool.
- The tool length is specified as ±10 m, indicating the depth interval over which the measurement is taken or the tool's operational range.

The right panel shows a 3D perspective of the tool's lower end:
- The tool has a central body with 4, 6, or 8 pads mounted on sprung arms, as labeled.
- The pads are designed to press against the borehole wall to ensure good electrical contact.

The bottom panel shows a detailed view of a single pad:
- It is labeled "Pad" and has a "Button Array" on its face.
- The pad width is specified as ±10 cm.
- The button array is depicted as a grid of small contacts, suggesting a multi-electrode design for high-resolution resistivity or imaging.

The schematic demonstrates the physical arrangement of the tool components, the electrical current path for resistivity measurement, and the mechanical design of the pad contact system for stable and consistent formation contact during logging.

KEYWORDS: logging tool, microresistivity, pad, sprung arms, button array, current flow, wireline, formation resistivity, borehole contact, tool length
----


Figure 9.4. Schematic diagram of a vertical, cylindrical borehole intersected by a planar feature such as a steeply dipping fracture. The intersection between the plane and the cylinder is either a circle or an oval. To view the borehole in two dimensions, the cylinder is generally cut along a line with an azimuth of true north (N). When the cylinder is flattened, the line of intersection of an oval trace becomes a sinusoidal curve. Modified from Serra (1989).


----
━━━ FORMAT 12: CONCEPTUAL DIAGRAM / КОНЦЕПТУАЛЬНАЯ СХЕМА ━━━
The figure presents a conceptual representation of a fracture plane in three different visual formats: a 3-D view, an unrolled cylinder, and an azimuthal image.

Left panel (3-D VIEW):
- A 3-D block diagram showing a fracture plane intersecting a cylindrical borehole.
- The fracture plane is depicted as an oval-shaped, shaded surface.
- The fracture is oriented with a labeled "Strike" direction (horizontal line across the plane) and a "Dip of Fracture Plane" (angle of inclination from horizontal).
- The borehole is shown as a vertical cylinder intersecting the fracture.

Middle panel (UNROLL CYLINDER):
- A cylindrical surface unrolled into a flat rectangle.
- The top edge of the rectangle is labeled "N" (North), indicating the azimuthal orientation.
- The fracture trace is shown as a curved line that starts near the top left, dips downward, and curves back up toward the right, representing the intersection of the fracture with the borehole wall.
- The curve is continuous and symmetric, suggesting a planar fracture intersecting the borehole at an angle.

Right panel (AZIMUTHAL IMAGE):
- A rectangular plot with a horizontal axis labeled with cardinal directions: N, E, S, W, N.
- A bell-shaped curve is centered on the "N" axis, peaking at the top and tapering symmetrically toward the E and W ends.
- This represents the azimuthal distribution of the fracture trace, with maximum intensity (or amplitude) aligned with North.

The diagram illustrates how a single fracture plane, when intersected by a borehole, can be visualized in 3-D space, then projected onto a cylindrical surface, and finally represented as an azimuthal distribution curve. The azimuthal image is commonly used in borehole image logs to identify fracture orientation and dip.

KEYWORDS: fracture plane, borehole imaging, 3-D view, unrolled cylinder, azimuthal image, strike, dip, fracture orientation, borehole wall, fracture trace
----


<!-- page 170 -->
Borehole Images

159


Figure 9.5. Schematic diagram of a horizontal, cylindrical borehole intersected by a planar feature such as a bedding plane. The intersection between the plane and the cylinder is either a circle or an oval. To view the borehole in two dimensions, the cylinder is generally cut along the top of the borehole. When the cylinder is flattened, the line of intersection of an oval trace becomes a sinusoidal curve. Modified from Serra (1989).


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth range: 7846 м to 7852 м, depth increases downward.

Tracks (left to right):

1. **GR (API)** — Gamma Ray, scale 0–200 API, curve: black line, shows a general increase from ~80 API at 7846 м to ~120 API at 7850 м, then a sharp drop to ~40 API at 7852 м.
2. **C13, C24 (in)** — Caliper, scale 6–16 in, two curves: C13 (red line), C24 (blue line). Both show a narrow borehole (~6 in) from 7846 м to 7848 м, then a sudden expansion to ~14 in at 7848 м, remaining expanded to 7852 м.
3. **AZ (m/s²)** — Accelerometer, scale 7.5–12 m/s², curve: red line. Shows a relatively flat response (~10 m/s²) from 7846 м to 7848 м, then a sharp drop to ~7.5 m/s² at 7848 м, remaining low to 7852 м.

4. **Accelerometer Corrected** — Borehole image log, 360° unrolled, azimuth axis: N–S–N (top to bottom), depth interval 7846–7852 м. Colour scale: light yellow to dark brown, indicating conductivity or resistivity. Two vertical tracks: North (N) and South (S). Features:
   - Interval 7846–7848 м: uniform light yellow, no distinct sinusoids.
   - Interval 7848–7852 м: dark brown band (S1) with broken sinusoids, indicating fractures or faults. A vertical black dashed line runs through the band, possibly a tool mark or borehole axis.
   - Label "V1" at 7848 м, marking the top of the dark band.

5. **Not Accelerometer Corrected** — Borehole image log, same format as above. Two vertical tracks: North (N) and South (S). Features:
   - Interval 7846–7848 м: uniform light yellow.
   - Interval 7848–7852 м: dark brown band (S2) with broken sinusoids, similar to S1 but with more pronounced vertical streaks. Label "V2" at 7848 м.

Interpretation:
- The caliper expansion at 7848 м indicates borehole enlargement, likely due to a fracture or fault.
- The accelerometer (AZ) drop coincides with the borehole enlargement.
- The borehole image logs show a distinct dark band (S1/S2) starting at 7848 м, interpreted as a fracture zone or fault, with broken sinusoids indicating offset or discontinuity.
- The "Accelerometer Corrected" image appears cleaner and more continuous than the "Not Accelerometer Corrected" image, suggesting better data quality after correction.

KEYWORDS: буровой имидж, калибр, гамма-каротаж, ускорение, коррекция, трещина, разлом, синусоида, буровой инструмент, интерпретация
----


Figure 9.6. Illustration of the benefits of speed correction. FMI images on the left have been accelerometer (AZ) corrected; images on the right have not. The vugs (V1) are compressed on the right-hand image (V2) because of a negative acceleration (decreasing AZ) at this depth. The shale (S2) has been stretched because of a fast acceleration (increasing AZ) at its top. Vertical scale is in ft. Note the washout (enlarged calipers C13 and C24) and increased GR corresponding to shale (S1). N-S-N refers to the true-north reference shown in Figure 9.4.
<!-- page 171 -->
160

HURLEY


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Бороздчатый (microimage) лог, представленный как развернутая 360° поверхность скважины. Глубина увеличивается вниз. Глубинный диапазон: 2197–2200 м. Ось глубины слева, с отметками 2197, 2198, 2199, 2200 м. Ось азимута вверху: N–S–N, что указывает на ориентацию с севера на юг и обратно, соответствующую 360° развертке (0°–180°–360°). Цветовая шкала не указана, но видны темные и светлые участки, соответствующие различной проводимости/отражательной способности стенки скважины.

На изображении видны три вертикальные полосы (секции), разделенные белыми промежутками — это фрагменты развертки. На каждой полосе видны темные линии, идущие по диагонали, которые интерпретируются как плоскости слоистости (bedding planes), поскольку они образуют полные синусоиды. Также видны разрывы и смещения синусоид — это признаки трещин или разрывов. На глубине ~2197,5 м и ~2199,5 м видны темные изогнутые линии, пересекающие все три секции — это, вероятно, трещины или разломы, проходящие по всей окружности скважины.

На изображении нет подписей, указывающих на конкретные значения дипа или азимута, но видны характерные синусоидальные формы, соответствующие наклонным слоям. Нет подписанных интервалов, литологии или интерпретации.

KEYWORDS: бороздчатый лог, микроимиджер, развертка скважины, синусоиды, слоистость, трещины, азимут, глубина, 360°, проводимость
----


Figure 9.7. FMI display in a sandstone of partially healed fractures, which appear as discontinuous conductive segments. Conductive features are imaged as dark colors. Red sine waves show fracture traces. Vertical scale is in ft. N-S-N refers to the true-north reference shown in Figure 9.4. After Knight (1999).


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Это бокс-лог (borehole image log) — 360° развертка стенки скважины, представленная в виде пяти вертикальных полос, соответствующих азимутальным секторам. Азимутальная ось: N–S–N (север–юг–север), что указывает на развертку по 360° с севера. Глубина увеличивается вниз. Глубинный диапазон: 2435–2437 м.

На изображении видны цветовые градации, соответствующие электрической проводимости или другому параметру, но шкала не указана. Визуально: верхняя часть (2435–2436 м) — светло-оранжево-желтая, средняя часть (около 2436 м) — темно-коричневая, нижняя часть (2436,5–2437 м) — темно-коричневая с более темными включениями.

На логе отмечены две горизонтальные линии:
- Зеленая линия на глубине 2437 м — обозначена буквой B.
- Красная изогнутая линия, проходящая на глубине ~2436 м, с меткой M — вероятно, интерпретированная граница или контакт.

Нет подписей к кривым, нет легенды, нет шкалы. Нет информации о типе изображения (акустический, электрический, микрорезистивиметр и т.д.).

Интерпретация: красная кривая M — возможно, граница пласта или выклинивание. Зеленая линия B — может быть кровлей или подошвой пласта. Цветовые переходы могут указывать на изменение литологии или пористости, но без шкалы и легенды точная интерпретация невозможна.

KEYWORDS: бокс-лог, развертка стенки скважины, азимут, глубина, интерпретация контакта, цветовая шкала, электрическая проводимость, микрорезистивиметр, акустический имиджер, 360°
----


Figure 9.8. Small-scale fault, or microfault (M), and bed boundaries (B) in a sand and shale interval. The shales occur in the lower part of the section. Vertical offset on the microfault is approximately 0.25 ft (8 cm). Vertical scale is in ft. N-S-N refers to the true-north reference shown in Figure 9.4. After Knight (1999).

Figure 9.9. Comparison between static (left) and dynamic (right) images in a sandstone interval that appears massive and nonlaminated when the core is viewed in visible light. Note the fine-scale bedding and the truncation surface (T). Dynamic processing, in which the image contrast is normalized in a moving S-ft window, sharpens the image and makes geologic features easier to see. Vertical scale is in ft. N-S-N refers to the true-north reference shown in Figure 9.4. The green line is a sine wave fit to a bedding plane. After Knight (1999).


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: Log Depth (ft), increases downward. Range: 2067–2069 ft. Depth scale marked at 2067, 2068, 2069 ft.

Two side-by-side panels, each showing a 360° unrolled borehole image log (microimage or acoustic image) with vertical white lines indicating tool caliper or tool position. The left panel shows a relatively uniform, light-yellow to tan background with subtle horizontal layering. The right panel shows more pronounced horizontal layering with color variation from light tan to dark brown and reddish-brown, with a distinct dark band labeled "T" near the top of the interval. A green curved line is drawn across both panels at approximately 2069 ft, likely indicating a bedding plane or interpreted horizon.

The image does not contain any curve tracks (ГК, ПС, etc.), only the borehole image. No scale for conductivity or resistivity is provided. No dip or azimuth values are printed. The white vertical lines are likely tool caliper or tool position markers.

The image is a borehole image log (microimage or acoustic image) showing the borehole wall with bedding planes and possible fractures. The left panel shows less contrast and fewer features, while the right panel shows more distinct bedding and a dark band labeled "T". The green line at 2069 ft is a marked horizon.

KEYWORDS: бороздчатый каротаж, микроимиджер, акустический имиджер, 360°, борозды, слоистость, горизонт T, глубина, фут, изображение скважины, интерпретация
----


<!-- page 172 -->
Borehole Images

161


----
━━━ FORMAT 9: TECHNICAL SCHEMATIC / ТЕХНИЧЕСКАЯ СХЕМА ━━━
The schematic shows a downhole tool assembly for borehole wall imaging or acoustic logging, consisting of a central cylindrical sonde with three main components: a Flux-Gate Magnetometer at the top, a Motor in the middle, and a Spinning Piezoelectric Transducer at the bottom. The sonde is shown inside a cylindrical borehole, with dashed lines indicating the borehole wall. A callout labeled "Signal Bounces off of Borehole Wall" points to the transducer, indicating that it emits and receives acoustic signals that reflect off the borehole wall. The motor is likely responsible for rotating the transducer to achieve 360° coverage. The entire assembly is designed to acquire acoustic or electromagnetic data from the borehole wall for imaging or formation evaluation purposes.

Callout labels:
1. Flux-Gate Magnetometer — located at the top of the sonde, likely for measuring magnetic field orientation or tool rotation.
2. Motor — positioned in the middle section, presumably to rotate the lower transducer.
3. Spinning Piezoelectric Transducer — located at the bottom, emits and receives acoustic signals that bounce off the borehole wall.
4. Signal Bounces off of Borehole Wall — indicates the acoustic reflection path from the transducer to the borehole wall and back.

The schematic demonstrates the principle of a rotating acoustic or electromagnetic imaging tool used in borehole logging to map the borehole wall geometry and detect fractures or bedding planes.

KEYWORDS: буровой инструмент, акустический имиджер, пьезоэлектрический преобразователь, мотор, флюкс-гейт магнитометр, отражение сигнала, буровая скважина, схема устройства, логирование, изображение ствола скважины
----


Figure 9.10. Schematic illustration of the basic operating principles behind acoustic borehole-imaging logs. A rotating transducer emits and records sound pulses. First-arrival amplitudes and travel times are recorded and mapped into processed logs. Tool names and companies are shown in Table 9.2. Modified from Zemanek et al. (1970).


----
━━━ FORMAT 9: TECHNICAL SCHEMATIC / ТЕХНИЧЕСКАЯ СХЕМА ━━━
Схема представляет модель гидродинамического взаимодействия между инструментом (Tool) и скважиной (Borehole). Центральный элемент — серый круг, обозначенный как "Tool", символизирующий логгинг-инструмент или зонд. Вокруг него — большой круг, обозначенный как "Borehole", представляющий скважину. 

Из центра инструмента вверх и вниз направлены прямые стрелки, указывающие на вертикальное движение или поток. С обеих сторон инструмента, вдоль горизонтальных линий, изображены изогнутые стрелки с пунктирными линиями, указывающие на боковое распределение или отражение/дифракцию энергии (например, акустической или электромагнитной) от стенок скважины. 

Схема демонстрирует принцип действия инструмента, который излучает энергию в скважину, и эта энергия взаимодействует со стенками, создавая отражённые или рассеянные сигналы, которые регистрируются инструментом. Это типично для акустических или электромагнитных логгинг-методов, таких как акустический имиджер или микрокаверномер.

KEYWORDS: Tool, Borehole, гидродинамическое взаимодействие, акустический логгинг, электромагнитный зонд, отражение, дифракция, скважина, инструмент, схема
----


Figure 9.11. This diagram, which is a view looking down on a borehole, shows the reason the acoustic borehole-imaging tool needs to be centralized. If the tool is off-center, the travel times may be too long (top) or too short (bottom). Some parts of the borehole are not even imaged because the reflected sound wave does not return to the transducer (left and right sides).


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: 8280 м to 8295 м, increasing downward. Depth scale: 15 м total, marked at 8280, 8285, 8290, 8295.

Track 1 (left): Gamma-ray log (GR), unit: API. Scale: 0 to 300 API, linear. Curve: smooth, continuous, with negative anomaly (low readings) in the upper part (8280–8285 м), then increasing to a peak near 8290 м, followed by a decrease. No other curves in this track.

Track 2 (right): Borehole image log (microimage or acoustic image), 360° unrolled view. Azimuth axis: top of image is North (N), bottom is South (S), with N and S labels at top and bottom. Depth range: 8280–8295 м. Image shows a yellowish-brown borehole wall with dark, irregular, horizontal and sub-horizontal linear features (bedding planes or fractures). Four labelled zones are marked with white boxes and letters:
- Zone "Г" at ~8282 м: dark, continuous horizontal band.
- Zone "Р" at ~8287 м: dark, continuous horizontal band.
- Zone "П" at ~8291 м: dark, discontinuous, patchy band.
- Zone "Д" at ~8293 м: dark, discontinuous, patchy band.

No dip or azimuth values are printed on the image. No colour scale or conductivity scale is provided. No interpretation panel (Кп, Кн, etc.) is present.

The image does not contain a legend for the image log features. The dark features are interpreted as bedding planes or fractures based on their geometry, but lithology cannot be determined without a legend.

| Интервал, м | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|-------------|--------------------------|-------------------|-------------------------------|
| 8280–8285   | —                        | GR: низкие значения (отрицательная аномалия) | — |
| 8285–8290   | —                        | GR: рост к пиковому значению | — |
| 8290–8295   | —                        | GR: снижение после пика | — |

KEYWORDS: каротажная диаграмма, гамма-каротаж, изображение скважины, интервал 8280–8295 м, зоны Г, Р, П, Д, азимут, глубина, API, борозды, трещины, слоистость
----


Figure 9.12. Example of an amplitude image from a CBIL log in a fractured sand and shale interval. Note the open fracture (F). This fracture, which terminates (T) at a shale bed, is thought to be drilling induced. Borehole breakouts (B), which occur as dark patches $180^{\circ}$ from each other, are well imaged by this log. Depth is in ft. N-S-N refers to the true-north reference shown in Figure 9.4.
<!-- page 173 -->
162

HURLEY


----
━━━ FORMAT 15: PHOTOGRAPH / ФОТОГРАФИЯ ━━━
Subject class: оборудование (equipment photograph)
Scale reference: none visible
Visually verifiable features:
- Central dark circular object with printed text "2.527.1'" on its surface.
- Bright, irregularly shaped reflections on the right and upper portions of the image, suggesting metallic surfaces or lenses.
- The object appears to be part of a larger apparatus, possibly a tool or instrument, with a dark background.
- The image is monochrome (black and white) and grainy, typical of older photographic or scanned documentation.
- The label "(a)" is present in the top-left corner, indicating this is part of a multi-panel figure.
- No annotations, arrows, or additional markings are visible on the photograph itself.

KEYWORDS: оборудование, фотография, инструмент, метка, 2.527.1', (a)
----


----
━━━ FORMAT 15: PHOTOGRAPH / ФОТОГРАФИЯ ━━━
Фотография, вероятно, изображающая поверхность керна или обнажения. На изображении видны неровности, трещины и текстуры, характерные для породы. В правой части изображения присутствует масштабная линейка с надписью "2 см", что указывает на масштаб. В левом верхнем углу имеется обозначение "(c)", вероятно, указывающее на подпункт или часть рисунка. Цветовая гамма — чёрно-белая, с высоким контрастом. На поверхности видны линейные и криволинейные трещины, а также участки с различной отражательной способностью, что может указывать на разные минералогические составы или степени выветривания. Никаких подписей, названий пород, минералов или идентификационных меток на изображении нет. Условия съёмки (например, плоскополяризованный свет, крестообразные поляризаторы) не указаны.

KEYWORDS: керн, обнажение, фотография, масштабная линейка, трещины, текстура, чёрно-белое изображение, (c)
----


----
━━━ FORMAT 15: PHOTOGRAPH / ФОТОГРАФИЯ ━━━
Subject class: буровой керн / внутренняя поверхность скважины (вид из бурового инструмента, вероятно, буровой камеры или бурового телевизора).

Описание:
- Изображение представляет собой круглый вид внутренней поверхности скважины, снятый снизу вверх (или наоборот, в зависимости от ориентации инструмента).
- Поверхность стенки скважины имеет неровную, шероховатую текстуру с видимыми вмятинами, трещинами и участками разрушения.
- В правой верхней части виден крупный участок разрушения или выкрошенного куска породы, прикреплённого к стенке.
- В нижней части изображения присутствует цифровой текст: "9926.1" и "108 F".
- "9926.1" — вероятно, глубина в футах (ft), так как "F" внизу может означать "feet" (в контексте буровых измерений).
- "108 F" — вероятно, температура в градусах Фаренгейта (°F), что соответствует 42,2 °C.
- В левом верхнем углу — метка "(b)", указывающая, что это часть серии изображений (например, (a), (b), (c)).

Масштаб: не указан. Нет видимых масштабных меток, линеек или объектов для масштабирования.

Условия съёмки: не указаны. Судя по качеству и виду, это изображение с бурового телевизора (Borehole Televiewer) или камеры, установленной на буровом инструменте.

KEYWORDS: буровой керн, внутренняя поверхность скважины, буровой телевизор, глубина, температура, разрушение стенки, трещины, шероховатость, изображение скважины
----


----
━━━ FORMAT 15: PHOTOGRAPH / ФОТОГРАФИЯ ━━━
Subject class: фотография внутренней поверхности скважины (внутренний вид бурового ствола, вид снизу вверх).
Scale reference: не виден.
Visually verifiable features:
- Круглый буровой ствол с видимыми стенками.
- На внутренней поверхности стенки наблюдается неровность, шероховатость и возможные следы коррозии или отложений.
- В центре изображения — тёмное отверстие, уходящее вглубь (перспективный вид).
- На правой стороне ствола видна вертикальная трещина или разлом, идущий от верхней части изображения вниз.
- В нижней части изображения нанесена надпись: "5793.8" и "118°F".
- В левом верхнем углу — обозначение "(d)".
- Изображение чёрно-белое, с высоким контрастом, характерным для буровых видеокамер или инспекционных камер.
- Нет видимых цветовых оттенков, текстур, кроме градаций серого.
- Нет дополнительных аннотаций, стрелок или масштабных меток.

Подписано на изображении: "5793.8", "118°F", "(d)".

KEYWORDS: фотография скважины, внутренний вид бурового ствола, трещина, коррозия, температура, глубина, инспекционная камера, буровой ствол, шероховатость стенки, 118°F, 5793.8
----


Figure 9.13. Examples of downhole video still shots. (a) Top of a tubing fish. (b) Hole in casing. (c) Production deposits (scale) with oil flow (black bubbles). (d) Openhole fractures. From Halliburton (1996).

Figure 9.14. Simple parallel-plate model for fluid flow in a fracture. $L =$ length; $d =$ aperture width; $Q =$ flow rate; $p =$ pressure; $\mu =$ viscosity; $K =$ permeability. The Darcy equation for linear flow (upper equation), when applied to this geometry, suggests that permeability $(k)$ is proportional to the square of the aperture width ( $d$ , lower equation). Modified from Brown (1987).


----
━━━ FORMAT 9: TECHNICAL SCHEMATIC / ТЕХНИЧЕСКАЯ СХЕМА ━━━
Схема представляет модель плоскопараллельного потока жидкости через горизонтальный слой пористой среды. На рисунке изображён прямоугольный слой толщиной d, длиной Lx и шириной Ly. Ось x направлена вдоль длины слоя, ось y — вдоль ширины, ось z — вертикально вверх. Поток Qx направлен вдоль оси x. Справа от схемы приведены уравнения:

- Qx = Ly * (d³ / 12μ) * (dp/dx) = (K * A / μ) * (dp/dx)
- K = d² / 12

где Qx — объёмный расход вдоль оси x, Ly — ширина слоя, d — толщина слоя, μ — вязкость жидкости, dp/dx — градиент давления, K — коэффициент проницаемости, A — площадь поперечного сечения (Ly * d), d² — квадрат толщины слоя.

Схема иллюстрирует вывод формулы для коэффициента проницаемости K в рамках модели плоскопараллельного потока (закон Дарси для плоского слоя), где проницаемость пропорциональна квадрату толщины слоя.

KEYWORDS: плоскопараллельный поток, закон Дарси, коэффициент проницаемости, модель слоя, гидродинамика, фильтрация, уравнение, толщина слоя, вязкость, градиент давления
----


<!-- page 174 -->
Borehole Images

163


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
This is a borehole image log (microimage or acoustic image) displayed as a 360° unrolled view of the borehole wall.

- Depth axis: labeled "Depth (m)", increases downward, range from 2280 to 2283 m.
- Azimuth axis: oriented N–S–N, with N at left and right edges, S at center — indicating a 360° wraparound.
- The image shows a continuous log with color variations representing borehole wall conductivity or acoustic impedance.
- A feature labeled "Burrows" is indicated by arrows pointing to a zone of irregular, dark, worm-like structures within a lighter-colored layer at approximately 2280.5–2281.0 m depth.
- A small square box labeled "B" is placed over the burrow zone, likely marking a specific point of interest or a borehole break.

The log displays bedding planes as relatively continuous, horizontal bands of color, with the burrowed zone showing disrupted, chaotic patterns indicative of bioturbation.

KEYWORDS: буровой имидж, микроразрез, биотурбация, буровые следы, глубина, азимут, цветовая шкала, буровой разрез, буровой снимок, биогенные структуры
----


Figure 9.15. Static FMI image of interbedded sands (light color) and shales (dark color). Based on core studies, the sandy laminated sediments represent storm deposits. Shaly bioturbated sediments (B) represent fair-weather deposits. Vertical scale is in ft. N-S-N refers to the true-north reference shown in Figure 9.4. After Knight (1999).


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
(a) — 360° unrolled borehole image log. Depth axis increases downward. Azimuth axis oriented N–E–S–W–N (0°–90°–180°–270°–360°). Colour scale: dark grey/black to orange/yellow, representing conductivity or resistivity (scale not calibrated). The log shows a continuous sinusoidal pattern with full sinusoids indicating bedding planes. No dip or azimuth values are printed. The top of the log is a solid black band, possibly representing a casing or tool collar.

(b) — Series of six vertical strips, each representing a 60° sector of the borehole wall (360°/6). Each strip shows a similar colour pattern (dark to orange/yellow) with sinusoidal features. The central strip (third from left) contains a prominent vertical black line, possibly a fracture or tool mark. No depth scale, no azimuth labels, no dip/azimuth values printed. The strips are arranged side-by-side, suggesting a segmented view of the borehole wall.

KEYWORDS: боковой каротаж, микроимиджер, 360°, синусоидальная геометрия, слоистость, трещина, цветовая шкала, азимут, глубина, интерпретация
----


Figure 9.16. STAR electrical images in a deep-water sandstone show climbing ripple laminations in a 3-D view (above), and flame structures, or fluid-escape structures (below). The height of each image is 6 in (15 cm). After Witton (1999).
<!-- page 175 -->
1
<!-- page 176 -->
10

Asquith, G., and D. Krygowski, 2004, Log Interpretation Case Studies, in G. Asquith and D. Krygowski, Basic Well Log Analysis: AAPG Methods in Exploration 16, p. 165-239.

# Log Interpretation Case Studies

## INTRODUCTION

A major hurdle for geologists is learning how the theory and the many formulas of log interpretation are translated into practice. The learning process is slow, and takes place only after a good deal of repetitive effort is supported by actual experience with logs. There are absolutely no shortcuts. Memorizing log patterns and curve values just doesn’t work, and can, in fact, prove disastrous. However, to assist the process of changing what’s done into how it’s done, case studies can be an invaluable asset. The ones presented here cover several geographical areas, geologic ages, lithologies and log packages. This variety is not necessarily a classic representation of any of the categories. The reader will need to engage his or her intellect in finding appropriate solutions for each problem, and will also need to apply material already learned from thorough study of the preceding text.

In these case studies, the authors are trying to:

- show examples of evaluation under a range of conditions: clastic rocks and carbonate rocks, oil and gas;
show examples with ranges of data, from minimal to substantial, from old to new; and
- move the reader from observing an illustration of an interpretation to interpretation as a self-directed exercise (with a solution provided, to verify the reader's conclusions).

Although all the case studies are based on actual field examples, in some studies the amount of log data analyzed would be superfluous in practice. In many instances, to set pipe or not doesn’t require a complete log analysis. *The unusual amount of detail is offered here for use in a learning experience.* Nevertheless, careful study of a log almost always yields information that furthers the development of expertise.

These case studies are a progressive series of problems. In solution of the first example the reader is

asked to do very little, but to solve the final example the reader should be prepared to work almost independently. An effort is made to define variables and terms in the case studies, even though they may have been defined earlier in the text.

No matter how significant log interpretation is to a geologist as an exploration method, it must also be viewed in the larger context of exploration decision-making. That’s why each case study includes a volumetric calculation of reserves. In several studies, the reader is asked to determine a rate of return on investment. As everyone intimately connected with petroleum exploration knows, wells can be geologic successes but economic failures. In a successful exploration program, petrophysical log interpretation is used as a way to tip the risk scale toward economically successful wells.

The list of equations that follows is an important part of petroleum exploration. Derivation of variables is included in this listing, although in most instances the reader is not asked to solve them. Instead, the values will be given, for use in the formulas.

## Items of note

In all the case studies, only a small number of representative depths is used in the Work Tables to illustrate reading the raw-curve data and making the calculations, whereas the graphical displays (crossplots and log plots) show data from every half-foot of the intervals of interest.

In the solutions to these case studies, the values of the raw log data—resistivity, bulk density, neutron porosity, and so on—were determined from visual inspection of the data and verified with the digital data, which itself was derived from paper copies of the logs. In that process, the number of significant digits determined in the visual inspection was retained. Those numbers were believed to be more representa-

165
<!-- page 177 -->
166

ASQUITH AND KRYGOWSKI

tive of the results of the reader's efforts to determine the log values than reversion to the digitally derived data, which is displayed to an arbitrary number of digits to the right of the decimal point. The reader will note that some types of data—neutron porosity and sonic porosity, for example—are shown to the same number of significant digits, whereas other data, notably resistivity, vary in the number of significant digits shown; this practice is based on the ability of the analyst to read that data from logarithmic scales. Computations were done with a variety of machine-assisted methods, rather than by hand; therefore the computations tend to reflect an arbitrary number of values to the right of the decimal point. The values that the reader determines should be close to those in the solutions tables, but they probably will not match exactly. In general, if the reader has read the original log values to the best of his/her ability and made the calculations properly, the decisions derived from those calculations will agree with the solutions to the case studies.

### Equations useful for the following case studies

The equations are presented in most, if not all, the case studies. They are reproduced here and referenced from those studies. Equations specific to each study will appear in the corresponding text.

Archie Water Saturation:

$$S_{wa} = \left[ \frac{a \times R_w}{\phi^m \times R_t} \right]^{\frac{1}{n}} \quad 10.1 \text{ (Equation 7.1)}$$

Flushed-zone Water Saturation (Archie Equation):

$$S_{xo} = \left[ \frac{a \times R_{mf}}{\phi^m \times R_{xo}} \right]^{\frac{1}{n}} \quad 10.2 \text{ (Equation 7.2)}$$

Ratio Water Saturation:

This equation can be used to estimate water saturation when no porosity logs are available, but in the case study, the solution of this equation will be compared with calculations of the Archie water saturation.

$$S_{wr} = \left[ \frac{R_{xo} / R_t}{R_{mf} / R_w} \right]^{0.625} \quad 10.3 \text{ (Equation 7.7)}$$

Moveable Hydrocarbon Index (MHI):

This form of the equation is derived from the ratio water saturation method, above.

$$MHI = S_w / S_{xo} = \left[ \frac{R_{xo} / R_t}{R_{mf} / R_w} \right]^{\frac{1}{2}} \quad 10.4 \text{ (Equation 7.4)}$$

Bulk Volume Water:

The proportion of water in the total formation is referred to as bulk volume water. It can be an indicator that the formation is at irreducible water saturation.

$$BVW = \phi \times S_w \quad 10.5 \text{ (Equation 7.22)}$$

Residual Oil Saturation:

$$ROS = 1.0 - S_{xo} \quad 10.6$$

Moveable Oil Saturation:

$$MOS = S_{xo} - S_w \quad 10.7$$

### Equations used for calculating volumetric producible hydrocarbon reserves

Oil-bearing formations:

$$N_f = \frac{7758 \times A \times h \times \phi \times S_h \times RF}{B_{oi}} \quad 10.8$$

where:

$N_f$ = volumetric recoverable oil reserves in stock-tank barrels (STB)

7758 = barrels per acre-foot

A = drainage area in acres

h = reservoir thickness in feet

$\phi$ = porosity (decimal fraction)

$S_h$ = hydrocarbon saturation (1.0 - $S_w$) (decimal fraction)

RF = recovery factor

$B_{oi}$ = oil volume factor, or reservoir barrels per stock-tank barrel

$$B_{oi} = 1.05 + 0.5 \times \left( \frac{GOR}{100} \right) \quad 10.9$$

where:

$$GOR \text{ (gas - oil ratio)} = \frac{\text{gas in cubic feet}}{\text{oil in barrels}} \quad 10.10$$

Gas-bearing formations:

$$G_f = 43,560 \times A \times h \times \phi \times S_h \times B_{gi} \times RF \quad 10.11$$
<!-- page 178 -->
Log Interpretation Case Studies

167

where:

$G_{f} =$ volumetric recoverable gas reserves in standard cubic feet (SCF)

$43,560 =$ area of 1 acre, in square feet

$A =$ drainage area in acres

$h =$ reservoir thickness in feet

$\phi =$ porosity, decimal

$S_{h} =$ hydrocarbon saturation $(1.0 - S_{w})$, decimal

$RF =$ recovery factor

$B_{gi} =$ gas volume factor (in SCF/cu ft)

$$
\begin{array}{l} B_{gi} = \frac{T_{sc}}{P_{sc}} \times \frac{P}{Z \times T_{f}} \\ = \left[ \frac{459.7 + 60}{15} \times \frac{P}{Z \times (459.7 + T_{f})} \right] \tag{10.12} \end{array}
$$

where:

$T_{sc} =$ temperature $(^{\circ}\mathrm{F})$ at standard conditions

$P_{sc} =$ surface pressure (psi) at standard conditions

$P =$ reservoir pressure (psi)

$Z =$ gas compressibility factor

$T_{f} =$ formation temperature $(^{\circ}\mathrm{F})$

Equation 10.12 can be solved also by the form below, where $B_{gi}$ is approximated by the ratio of surface pressure and formation pressures:

$$
G_{f} = 43,560 \times A \times h \times \phi \times S_{h} \times \left(\frac{Pf_{2}}{Pf_{1}}\right) \times RF \tag{10.13}
$$

where:

$G_{f} =$ volumetric recoverable gas reserves in standard cubic feet (SCF)

$43,560 =$ area of 1 acre, in square feet

$A =$ drainage area in acres

$h =$ reservoir thickness in feet

$\phi =$ porosity, decimal

$S_{h} =$ hydrocarbon saturation $(1.0 - S_{w})$, decimal

$RF =$ recovery factor

$Pf_{1} =$ surface pressure (psi) (atmospheric, approximately 15 psi)

$Pf_{2} =$ reservoir pressure (psi)

$$
\frac{Pf_{2}}{Pf_{1}} = \frac{0.43 \times depth}{15} \tag{10.14}
$$

where:

0.43 is the average pressure gradient (in psi/ft), and depth is in feet.

*Estimation of formation pressure:*

Static mud column pressure

$= \text{depth} \times \text{mud weight} \times 0.052.$ 10.15

Rule of thumb for static bottom-hole pressure:

$$
P_{ws} = P_{wh} + 0.25 \times \left(\frac{P_{wh} \times depth}{100}\right) \tag{10.16}
$$

where:

$P_{ws} =$ static bottom hole pressure (psi)

$P_{wh} =$ well-head pressure (psi)

*Estimation of geothermal gradient:*

$$
g = \frac{(T_{f} - T_{s}) \times 100}{depth} \tag{10.17}
$$

where:

$g =$ temperature gradient in $^{\circ}\mathrm{F}/100$ ft

$T_{f} =$ formation temperature in $^{\circ}\mathrm{F}$

$T_{s} =$ mean surface temperature in $^{\circ}\mathrm{F}$

depth = formation depth in feet

As you begin trying the formulas in case studies, keep in mind the fact that many values such as water saturation $(S_{w})$ and porosity $(\phi)$ may be expressed in percentages, especially on older logs and in older calculations. So, even though this will be immediately obvious to you, remember to change percentages to decimal fractions before doing the calculations.
<!-- page 179 -->
168

ASQUITH AND KRYGOWSKI

# Case Study 1:

# PENNSYLVANIAN ATOKA SANDSTONE, PERMIAN BASIN, U.S.A.:

The Problem.

Case Study 1 illustrates the evaluation of a clean, gas-bearing sandstone. Because this is the first case study, the interpretation is largely done for the reader, with only minor calculations required of the reader. Two terms are defined here:

- A gas chromatograph is a device that samples the gases from the circulating drilling mud and analyzes them for the presence of methane (C₁H₄) and heavier hydrocarbons. The instrument alerts the geologist to a show of hydrocarbons from a formation.
- A drilling break is an increase in the rate of penetration of the drill bit, which indicates a difference in the rock. For example, penetration rate commonly increases when the bit goes from a shale into porous sandstone. A reverse drilling break, when the rate of penetration slows, may indicate passage of the bit from sandstone into shale, or the drilling of a highly cemented, low-porosity formation. Penetration rate is measured in minutes/foot rather than feet/minute, so the larger the number the slower the penetration rate. For example, a penetration rate of 20 min/ft is slower penetration than 10 min/ft.

# Background

Your company has just finished drilling a 15,900-ft wildcat well in the Permian Basin of Texas. The primary target was Morrowan sandstones. They are not developed sufficiently for commercial production and you face these alternatives: declare the well dry and abandoned (D&A), or find another zone, one that would produce hydrocarbons at an exceptional profit.

Samples of bit cuttings indicated that at 14,600 ft the Atoka Sandstone (Figure 10.1) is predominantly loose, subrounded, coarse to very coarse, quartzose sandstone with minor amounts of arkosic sandstone that is tan, medium grained to coarse grained, poorly sorted, and friable. This information leads to the inference that the Atoka Sandstone might be permeable, because the rock is coarse grained and accordingly, pore spaces should be large. Poor cementation and good permeability are indicated, because the sandstone is friable.

Other information about the Atoka Sandstone—information that you consider to be favorable—is the emission of a few gas bubbles from sample cuttings and gas recorded on the mud logger's gas chromatograph. During drilling of the bottom 4 ft of the sandstone, total gas background on the chromatograph increased from 10 units to 40 units of gas with a trace of C₂ and C₃ hydrocarbons, a significant change. The neutron-density log (Figure 10.2) shows evidence that supports your conclusions.

Even though you are optimistic about the potential of good production from the Atoka Sandstone—because of the nature of the sample cuttings and the gas shows—you are concerned about a reverse drilling break that occurred as the sandstone was penetrated. Strata that directly overlie and underlie the Atoka Sandstone were penetrated at 8 to 10 min/ft. However, the penetration rate through most of the sandstone was 15.5 min/ft; it slowed to 20 min/ft through the bottom 10 ft. The slower drilling times may mean that the sandstone is not as porous and permeable as sample-examination suggested.

Now, inspect the logs, calculate the important quantitative attributes of the sandstone, assess the log-derived information, and decide whether the Atoka Sandstone should produce oil and gas in sufficiently profitable quantities.

# Well site information and other pertinent information:

- Total depth (TD) = 15,962 ft
- bottom hole temperature (BHT): 197°F
- bit diameter = 8.5 in.
- fluid in the hole: "freshwater mud"
- mud filtrate resistivity (Rₘf): 1.34 ohm-m at 87°F
- mean annual surface temperature = 75°F (estimated by the well site geologist)
- temperature of the formation (Tf) = 187°F, estimated from formation temperature chart (Chapter 1)
- resistivity of formation water (Rw) = 0.065 ohm-m at Tf from local information (water produced nearby, water recovered during drill-stem tests, or a formation-water catalogue)
- resistivity of mud filtrate (Rₘf) = 0.65 ohm-m at Tf from the log header, corrected to formation temperature by the Arps equation (see Chapter 1)
- Archie parameters: a = 0.81, m = n = 2, for use in Equations 10.1 and 10.2
<!-- page 180 -->
Log Interpretation Case Studies

169

## Helpful equations

Neutron-density porosity in a gas zone:

Values for neutron porosity and density porosity are read from the neutron-density log and evaluated jointly:

$$\phi_{ND_{gas}} = \sqrt{\frac{\phi_D^2 + \phi_N^2}{2}} \tag{10.18 (Equation 4.8)}$$

$R_t$ Minimum, to determine true formation resistivity, $R_f$: This technique approximates $R_f$ in thin resistive zones; it is an alternate (approximate) approach to the use of a variety of correction charts.

$$R_{t \min} = LL8 \times \frac{R_w}{R_{mf}} \tag{10.19 (Equation 5.3)}$$

where LL8 is shallow resistivity, read by the laterolog 8.

Static SP:

The value of the SP in a clean (“shale-free”) formation is the Static SP.

$$SSP = -K \times \log\left(\frac{R_{mf}}{R_w}\right) \tag{10.20 (Equation 8.6)}$$

On the Work Table (Table 10.1), points were selected to illustrate a range of resistivities and porosities. Notice that the log values recorded at each depth actually may be peak or trough values from as much as 1 ft above or below the listed depths. This is a reasonable approach, for two reasons: (1) the logs have different vertical resolutions, and (2) because a suite of logs generally requires more than one logging “run” out of the borehole, some logs differ slightly in depth-registry of beds. This approach also allows the interpreter to provide data for the most optimistic interpretation that can be made, in the context of the given data values.
<!-- page 181 -->
170

ASQUITH AND KRYGOWSKI

Table 10.1. Case Study 1: Atoku Sandstone, Permian Basin, U.S.A.: Work table.

The work table shows values of the raw data—extracted from Figures 10.1 and 10.2—and sample calculations for several depths. You should verify this operating assumption: your reading of the logs produces the "some" values for the original data, and for the calculated quantities. The values may differ, but they should be close. As you work through the problem, do the calculations, to ensure that you understand the mechanics of the computations and of the plots. The symbol "v/v" indicates volume-for-volume decimal fraction.

|  Parameters  |   |   |   |
| --- | --- | --- | --- |
|  Ann. Mean Surf. Temp: 75°F |   |   | Rw (measured): (not given)  |
|  Total Depth: 15,962 ft |   |   | Rw @ fm. temp.: 0.065 ohm-m @ °F  |
|  Bottom Hole Temp: 197°F |   |   | Rmf (measured): 1.34 ohm-m @ 87°F  |
|  Formation Depth: 14,600 ft |   |   | Rmf @ fm. temp.: 0.65 ohm-m @°F  |
|  Formation Temperature: 187°F |   |   |   |
|  GRclean: 15 API |   |   | GRshale: 65 API  |
|   | a: 0.81 | m: 2 | n: 2  |

|  Raw data  |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- |
|  Depth feet | ILD ohm-m | ILM ohm-m | LL8 ohm-m | DPHI v/v decimal | NPHI v/v decimal  |
|  14,604 | 130 | 260 | 510 | 0.180 | 0.068  |
|  14,607 | 160 | 240 | 1100 | 0.214 | 0.064  |
|  14,609 | 190 | 210 | 1300 | 0.185 | 0.070  |
|  14,613 | 300 | 410 | 1500 | 0.260 | 0.085  |
|  14,618 | 160 | 250 | 520 | 0.245 | 0.100  |
|  14,622 | 110 | 100 | 190 | 0.215 | 0.115  |

|  Rt from tornado chart  |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- |
|  Depth feet | ILM/ILD | LL8/ILD | Rt/ILD | Rt ohm-m | Rt min ohm-m  |
|  14,604 | 2.00 | 3.92 | 0.46 | 59.8 | 51  |
|  14,607 |  |  |  |  |   |
|  14,609 |  |  |  |  |   |
|  14,613 | 1.37 | 5.00 | 0.92 | 266.8 | 150  |
|  14,618 |  |  |  |  |   |
|  14,622 | 0.91 | 1.73 | 1.00 | 110.0 | 19  |

|  Calculations  |   |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  Depth feet | PhiNDgas v/v decimal | Swa v/v decimal | Sxo v/v decimal | BVW | ROS v/v decimal | MOS v/v decimal | MHI  |
|  14,604 | 0.136 | 0.242 | 0.262 | 0.033 | 0.738 | 0.020 | 0.924  |
|  14,607 |  |  |  |  |  |  |   |
|  14,609 |  |  |  |  |  |  |   |
|  14,613 | 0.193 | 0.081 | 0.108 | 0.016 | 0.892 | 0.027 | 0.750  |
|  14,618 |  |  |  |  |  |  |   |
|  14,622 | 0.172 | 0.141 | 0.339 | 0.024 | 0.661 | 0.198 | 0.416  |
<!-- page 182 -->
Log Interpretation Case Studies

171


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Глубина увеличивается вниз. Диапазон глубин: 14600–20000 футов (MD — measured depth).

Лог-панель слева:
- Трек 1: ГК (Гамма-каротаж), шкала 0–150 API, единицы API.
- Трек 2: ПС (Потенциал спонтанного), шкала −80–+80 мВ, единицы мВ.
- Трек 3: GB (Гамма-каротаж, вероятно, другой канал или калибровка), шкала 0–150, единицы не указаны (возможно, API).

Лог-панель справа:
- Трек 1: ILD (Индукционный каротаж, глубокий), шкала 0,2–2000 Ом·м, единицы Ом·м.
- Трек 2: ILM (Индукционный каротаж, средний), шкала 0,2–2000 Ом·м, единицы Ом·м.
- Трек 3: LL8 (Лог-лог-каротаж, вероятно, резистивиметрия), шкала 0,2–2000 Ом·м, единицы Ом·м.
- Трек 4: шкала 0,2–2000, единицы не указаны (возможно, дополнительный резистивиметрический канал или плотность).

Интервалы и поведение кривых:
| Интервал, фут | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|---------------|------------------------|-------------------|------------------------------|
| 14600–15000   | Не определена          | ГК: повышенные показания; ПС: отрицательная аномалия; ILD/ILM/LL8: низкие сопротивления | Вероятно, глинистый интервал |
| 15000–17000   | Не определена          | ГК: умеренные показания; ПС: положительная аномалия; ILD/ILM/LL8: резкое увеличение сопротивления | Вероятно, коллектор (песчаник/карбонат) |
| 17000–18000   | Не определена          | ГК: умеренные показания; ПС: положительная аномалия; ILD/ILM/LL8: умеренные сопротивления | Коллектор с возможной глинистостью |
| 18000–20000   | Не определена          | ГК: повышенные показания; ПС: отрицательная аномалия; ILD/ILM/LL8: низкие сопротивления | Вероятно, глинистый интервал |

Результаты интерпретации не указаны в панели.

KEYWORDS: каротаж, ГК, ПС, ILD, ILM, LL8, резистивиметрия, глубина, мВ, Ом·м, API, MD, интервал, литология, коллектор, глина
----


Environmental information:

Total depth = 15,962 ft

bottom hole temperature (BHT) = 197°F (maximum recorded temperature)

bit diameter = 8½in.

type of fluid in hole = freshwater mud

$R_{mf}$ at measured temperature = 1.34 ohm-m at 87°F

$R_{ms}$ at measured temperature = 3.34 ohm-m at 87°F

$R_{st}$ at measured temperature = 1.67 ohm-m at 87°F

Note the following attributes of the logs in the interval from 14,600 ft to 14,625 ft.

1) Resistivity curves in tracks 2 and 3 show high resistivities.
2) Gamma ray count in the Atoka Sandstone interval (track 1, dashed line) is less than that in shales above and below.
3) The SP curve (track 1, solid line) shows evidence of hydrocarbon suppression, especially in the upper part of the zone. (If water saturation were \(100\%\), the shape of the SP curve would be strongly similar to the shape of the gamma ray curve. If the zone were shaly and water saturation were \(100\%\), the gamma ray curve would mimic the shape of the SP curve shown here.)

Figure 10.1. Dual induction laterolog 8 with spontaneous potential log and gamma ray log, Atoka Sandstone, Permian Basin, U.S.A.

This log, and those that follow in this and the other case studies, are displayed in what is commonly referred to as a "standard API format." The format, from the American Petroleum Institute, is described from left to right as:

Track 1, generally displaying correlation logs (SP, gamma ray, and caliper);

Depth Track, showing the depths of the log readings;

Track 2, which shows the main measurements, such as resistivity; and

Track 3, which also shows main measurements, such as porosity.

Commonly, as in this figure and in Figure 10.2, tracks 2 and 3 are combined for a single display. In this figure the tracks show resistivity over four decades of values, with no physical distinction made of the boundary between tracks 2 and 3. Even when this type of combined display is used, it is common practice to reference the combined track to the right of the depth track as "tracks 2 and 3."

In this log, and in the other logs shown in this chapter, depth is indicated by a fine line every 2 ft, a medium-thick line every 10 ft, and a heavy line every 50 ft.
<!-- page 183 -->
172

ASQUITH AND KRYGOWSKI


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Глубина увеличивается вниз. Диапазон глубин: от ~14500 до ~14650 футов (MD — measured depth).

Трек 1 (слева):
- Кривая: GR (гамма-каротаж), шкала: 0–150 API, единицы: API.
- Кривая: CALI (калибровка), шкала: 6–16 дюймов, единицы: inches.
- Кривая: BitSize (диаметр долота), шкала: 6–16 дюймов, единицы: inches.
- Визуальное поведение: GR — колебания, в интервале ~14550–14600 футов — повышенные показания (до ~100 API), затем снижение. CALI и BitSize — почти совпадают, показывают стабильный диаметр ~8–9 дюймов, с небольшими колебаниями.

Трек 2 (справа):
- Кривая: DPHI (пористость по плотности), шкала: 0.45–0.15 (десятичные), единицы: v/v decimal.
- Кривая: NPHI (пористость по нейтронам), шкала: 0.45–0.15 (десятичные), единицы: v/v decimal.
- Визуальное поведение: DPHI и NPHI — в основном совпадают, с небольшими расхождениями. В интервале ~14550–14600 футов — пористость ~0.25–0.30 (25–30%). Ниже ~14600 футов — пористость снижается до ~0.15–0.20 (15–20%). В интервале ~14500–14550 футов — пористость ~0.20–0.25 (20–25%).

Интервалы и отбивки:
| Интервал, фут | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|----------------|--------------------------|-------------------|-------------------------------|
| 14500–14550    | Не определена            | GR: умеренные, DPHI/NPHI: ~0.20–0.25 | Песчаник/песчанистый алеврит? |
| 14550–14600    | Не определена            | GR: повышенные (~100 API), DPHI/NPHI: ~0.25–0.30 | Вероятно, коллектор, возможно, с глинистым цементом |
| 14600–14650    | Не определена            | GR: снижение, DPHI/NPHI: ~0.15–0.20 | Уменьшение пористости, возможно, глина или плотный песчаник |

Результаты петрофизической интерпретации не представлены в данном фрагменте.

KEYWORDS: каротаж, ГК, калибровка, пористость, DPHI, NPHI, глубина, фут, API, v/v decimal, интервал, коллектор
----


Figure 10.2. Combination neutron-density log with gamma ray log and caliper log, Atoka Sandstone, Permian Basin, U.S.A.

Neutron and density porosities were recorded in sandstone-porosity units.

Note the following attributes of the logs in the stratigraphic interval from 14,600 ft to 14,625 ft.

1) Mudcake is shown by the caliper curve (CALI) in track 1; the hole diameter is smaller than the diameter of the bit \((8\frac{1}{2}\) in.).
2) Strong gas effect is shown in tracks 2 and 3. The density-porosity curve (DPHI) shows much higher porosities than the neutron-porosity curve (NPHI), and both logs show high porosity.
<!-- page 184 -->
Log Interpretation Case Studies 173

# Case Study 1:

# **PENNSYLVANIAN ATOKA SANDSTONE, PERMIAN BASIN, U.S.A.:**

# *The Solution.*

Information from the well site produced the following positive indicators: (1) Probable permeability, due to the coarseness and friability of the formation, and (2) gas bubbles in the bit cuttings and gas indicated by the mudlogger's chromatograph. The information also produced this negative indicator: decrease in the drilling rate through the sandstone, which might indicate that porosity and permeability are less than assumed from inspection of the cuttings.

Careful examination of the logs recorded through the Atoka Sandstone provided the following information:

- The gamma ray curve (Figure 10.1) shows a fairly consistent low value (slightly greater than 15 API units) through the sandstone, which indicates that the sandstone is clean.
- The SP curve (Figure 10.1) is deflected less in the upper part of the formation than in the lower part. This could be due to shaliness, hydrocarbon suppression, or both. Because the gamma ray curve is fairly constant and at low values, hydrocarbon suppression is the most likely cause.
- Resistivity curves all show high values. In this borehole, mud filtrate resistivity is greater than formation water resistivity; the invasion pattern of resistivity curves is characteristic of hydrocarbon-bearing rock (ILD < ILM < LL8). (Compare Figure 10.1 with Figure 1.8.)
- The caliper curve (Figure 10.2), shows mudcake. Opposite the Atoka Sandstone, the diameter of the borehole is markedly smaller than above or below, and the diameter of the hole is less than the diameter of the drill bit (see BitSize line). This mudcake is important evidence: it formed by accumulation of solid particles on walls of the borehole, as drilling mud invaded porous and permeable rock.
- The neutron-log and density-log responses (NPHI and DPHI) through the sandstone support the presumption that the hydrocarbons are gas; the density curve reads much higher porosity than the neutron log—"crossover," due to gas in the formation. (See Figure 4.10.)
- Visual examination of the neutron-porosity and density-porosity curves indicates porosity of

about 0.15 (15%), which should be sufficient for production of gas.

To derive more information from the data, calculations can be made. The Static SP (SSP) can be calculated by Equation 10.20:

$$\begin{aligned} SSP &= -K \times \log \left( \frac{R_{wf}}{R_w} \right) \\ &= -(60 + (0.133 \times 187)) \times \log \left( \frac{0.65}{0.065} \right) \\ &= -84.87 \text{ mV} \end{aligned}$$

The maximal SP in the sandstone, near the bottom of the zone, is about -30 mV. Comparison of the recorded SP with the Static SP leads to the conclusion that the SP curve is suppressed throughout the Atoka Sandstone. This suppression denotes the presence of hydrocarbons.

Next, calculate porosity from the neutron and density logs. Because gas in the formation is indicated by the porosity-curve crossover, Equation 10.18 should be used to calculate gas-corrected porosity, (PhiND-gas). In the six intervals to be analyzed, calculated porosity ranges from slightly less than 14% to approximately 19% (Table 10.2).

Water saturation is the next calculation, but before Archie's equation is used, resistivity should be corrected for effects of invasion. A tornado chart (Figure 10.3) is used to determine true formation resistivity ($R_f$) from the deep induction, medium induction, and laterolog-8 measurements of resistivity. The section in the work table (Table 10.1) labeled "Rt from tornado chart" shows ratios to be calculated, ratios to be read from the chart, and the resulting value of $R_f$. The caption of Figure 10.3 explains how to use the chart.

An alternate method to determine true formation resistivity is to calculate $R_{tmin}$ (Equation 10.19). As explained in Chapter 5, $R_{tmin}$ is compared to $R_f$ from tornado-chart calculations, and at any depth the greater of the two is used as the best estimate of $R_f$. In this case, for all depths, the value of $R_f$ from the tornado charts is greater than $R_{tmin}$, so the tornado-chart values are used (Table 10.2).

The Archie equation (Equation 10.1) is used to calculate water saturation (noted here as $S_{wa}$, to distinguish it from water saturation estimated by the ratio method, $S_{wr}$). $R_f$ is used for the measurement of resistivity, and PhiNDgas (derived from the neutron and density porosity logs) is used for the quantity of porosity. The values for $R_w$ and the Archie parameters are listed above, under the topic "Well site information
<!-- page 185 -->
174

ASQUITH AND KRYGOWSKI

and other pertinent information." The estimates of water saturation are consistently low (Table 10.2), which is an indication that the reservoir may be at irreducible water saturation. The flushed zone water saturation ($S_{xo}$) is also calculated from Archie's equation, with $R_{mf}$ substituted for $R_w$, and $R_{xo}$ substituted for $R_t$. For the calculations in this case study, the laterolog 8 (LL8) values should be used for $R_{xo}$.

Bulk volume water (BVW) is calculated from Equation 10.5. It shows low, fairly consistent values for all the zones, suggesting—as do the water saturations—that the formation is at irreducible water saturation. Figure 10.4 shows BVW graphically, by the plot of water saturation ($S_{wa}$) versus porosity (PhiNDgas). A large sample of points plots near the line that is equivalent to BVW of 0.02. Clustering of points around a constant BVW line supports the conclusion that the reservoir is at irreducible water saturation.

Another crossplot that provides supportive information is Figure 10.5. Porosity is plotted against water saturation, with estimates of permeability (derived from Equation 7.31) superimposed on the data. The plot indicates that permeability of the sandstone may be very good, especially if the reservoir is at irreducible water saturation, as indicated by water saturations and BVW values (Table 10.2 and Figure 10.4).

The increase in penetration rate downward through the Atoka was unfavorable information; there is additional negative information. Residual oil saturations (ROS), calculated by Equations 10.2 and 10.6, are high (Table 10.2). This fact is anomalous because other evidence, discussed above, supports the conclusion that the reservoir has high porosity and permeability. Ordinarily, under these conditions of porosity and permeability, mobility of hydrocarbons would be expected. Furthermore, calculations of moveable oil saturation (MOS) (Equation 10.7), produce low values (Table 10.2). Initially, this is puzzling; in a reservoir with high porosity and permeability, moveable oil saturation should be high. Additional anomalous information is produced by calculation of the moveable hydrocarbon index (MHI) (Equation 10.4 and Table 10.2). Most values are greater than 0.7, but in the general case, movable hydrocarbon indices of productive reservoirs are less than 0.7. Analyses of ROS, MOS, and the moveable hydrocarbon index MHI suggest that hydrocarbons will not move. Indeed, all these factors give notice that most of the hydrocarbons would remain in place, in the reservoir.

In the initial evaluation of logs, information about inadequate moveability of hydrocarbons should not be ignored; however, sometimes evidence of deficient moveability can be explained in the following way. In

the case at hand, what is significant is the high residual gas saturation in the flushed zone (1.0 - $S_{xo}$ = residual hydrocarbon saturation, (ROS) (Equation 10.6)). High residual gas saturation is the result of bypassing of gas by drilling fluids during invasion of a reservoir. Residual gas saturation can be read and interpreted erroneously by the logs as being the consequence of stationary hydrocarbons.

You were justifiably concerned about negative information from the drill-penetration rate, and the pessimistic moveability data. Nevertheless, you decided that when considered altogether, evidence of shows in bit cuttings, gas shows recorded by the mud logger, and qualitative and quantitative log interpretation overrode the negative evidence and supported the decision to set pipe. Log-interpretation information that was especially significant to your decision included:

- high porosities shown on the neutron-density logs;
- strong gas effect on the display of the neutron-density logs;
- low water saturation, calculated by the Archie equation;
- high log-derived permeabilities, from cross-plots; and
- low bulk-volume-water values.

Although you believe that the well penetrated a gas-filled reservoir, you are quite interested in whether the well would be a commercial success. Equation 10.11 is used to calculate volumetric gas reserves. Estimated gas recovery of 11 BCF is calculated by using the following parameters:

- geothermal gradient = 0.014°/ft × formation depth;
- pressure gradient = 0.35 psi/ft × formation depth;
- drainage area = 560 acres;
- reservoir thickness = 15 ft;
- effective porosity = 0.15 (15%);
- water saturation = 0.13 (13%);
- gas gravity = 0.65;
- recovery factor = 0.85;
- formation temperature = 205°F;
- initial bottom hole pressure = 5,117 psi; and the
- Z factor = 0.988.

The Atoka Sandstone was perforated from 14,610 ft to 14,615 ft. The calculated absolute open flow (CAOF) was 21,900,000 cu ft of gas per day (21,900
<!-- page 186 -->
Log Interpretation Case Studies

175

mcfgpd) with a high shut-in tubing pressure (SITP) of 3758 pounds per square inch (psi) and a high initial bottom hole pressure (IBHP) of 5556 psi. The gas gravity was 0.599 at bottom hole temperature of 219°F. The well’s first-year cumulative production was 3,268,129 mcf plus 95,175 barrels of condensate.

Figure 10.6 is a computer-derived log of the Atoka Sandstone. It shows calculated porosity (PhiNDgas)

and water saturation ($S_{wg}$), among other calculated values. Log displays containing both raw and calculated values are available at the well site, either during or immediately after data acquisition. The same calculations and displays can be made by commercially available software packages; however, the calculated results are only as accurate and reliable as the log data and the parameters that are used for computations.
<!-- page 187 -->
176

ASQUITH AND KRYGOWSKI

Table 10.2. Case Study 1: Atoka Sandstone, Permian Basin, U.S.A.: Solution table. The symbol "v/v" indicates volume-for-volume decimal fraction.

|  Parameters  |   |   |   |
| --- | --- | --- | --- |
|  Ann. Mean Surf. Temp: 75°F |   |   | Rw (measured): (not given)  |
|  Total Depth: 15,962 ft |   |   | Rw @ fm. temp.: 0.065 ohm-m @ °F  |
|  Bottom Hole Temp: 197°F |   |   | Rmf (measured): 1.34 ohm-m @ 87°F  |
|  Formation Depth: 14,600 ft |   |   | Rmf @ fm. temp.: 0.65 ohm-m @ °F  |
|  Formation Temperature: 187°F |   |   |   |
|  GRclean: 15 API |   |   | GRshale: 65 API  |
|   | a: 0.81 | m: 2 | n: 2  |

|  Raw data  |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- |
|  Depth feet | ILD ohm-m | ILM ohm-m | LL8 ohm-m | DPHI v/v decimal | NPHI v/v decimal  |
|  14,604 | 130 | 260 | 510 | 0.180 | 0.068  |
|  14,607 | 160 | 240 | 1100 | 0.214 | 0.064  |
|  14,609 | 190 | 210 | 1300 | 0.185 | 0.070  |
|  14,613 | 300 | 410 | 1500 | 0.260 | 0.085  |
|  14,618 | 160 | 250 | 520 | 0.245 | 0.100  |
|  14,622 | 110 | 100 | 190 | 0.215 | 0.115  |

|  Rt from tornado chart  |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- |
|  Depth feet | ILM/ILD | LL8/ILD | Rt/ILD | Rt ohm-m | Rt min ohm-m  |
|  14,604 | 2.00 | 3.92 | 0.46 | 59.8 | 51  |
|  14,607 | 1.50 | 6.88 | 0.88 | 140.8 | 110  |
|  14,609 | 1.11 | 6.84 | 0.99 | 188.1 | 150  |
|  14,613 | 1.37 | 5.00 | 0.92 | 266.8 | 150  |
|  14,618 | 1.56 | 3.25 | 0.70 | 112.0 | 52  |
|  14,622 | 0.91 | 1.73 | 1.00 | 110.0 | 19  |

|  Calculations  |   |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  Depth feet | PhiNDgas v/v decimal | Swa v/v decimal | Sxo v/v decimal | BVW | ROS v/v decimal | MOS v/v decimal | MHI  |
|  14,604 | 0.136 | 0.242 | 0.262 | 0.033 | 0.738 | 0.020 | 0.924  |
|  14,607 | 0.158 | 0.122 | 0.138 | 0.019 | 0.862 | 0.016 | 0.884  |
|  14,609 | 0.140 | 0.120 | 0.144 | 0.017 | 0.856 | 0.024 | 0.832  |
|  14,613 | 0.193 | 0.081 | 0.108 | 0.016 | 0.892 | 0.027 | 0.750  |
|  14,618 | 0.187 | 0.116 | 0.170 | 0.022 | 0.830 | 0.054 | 0.681  |
|  14,622 | 0.172 | 0.141 | 0.339 | 0.024 | 0.661 | 0.198 | 0.416  |
<!-- page 188 -->
Log Interpretation Case Studies 177


----
━━━ FORMAT 7: NOMOGRAM / ПАЛЕТКА ━━━
Palette name: THICK BEDS, 8" HOLE, NO ANNULUS, NO TRANSITION ZONE, INDUCTION LOG IS SKIN-EFFECT CORRECTED

Axes:
- Horizontal axis (abscissa): R_ILm / R_ILD, linear scale, range 1.0 to 2.2
- Vertical axis (ordinate): R_ILD / R_LLd, linear scale, range 1.0 to 40.0 (depth axis increases upward)

Family parameter: R_x0 / R_t, with labelled values: 10, 20, 30, 40, 50, 60, 70, 80, 90, 100 (in % or dimensionless ratio — not specified)

Auxiliary scales:
- Diagonal lines: labelled with angles (in degrees) from 0° to 90°, representing the angle of the invasion front or resistivity contrast.
- Curved lines: represent constant R_x0 / R_t ratios, forming a family of curves from the origin to the top-right.

Reading procedure:
- Locate the measured value of R_ILm / R_ILD on the horizontal axis.
- Locate the measured value of R_ILD / R_LLd on the vertical axis.
- The intersection point lies on a curve corresponding to a specific R_x0 / R_t ratio.
- The angle of the diagonal line passing through the point gives the invasion angle or resistivity contrast angle.

Anchor points (approximate, for extreme curves only):
- For R_x0 / R_t = 10: at R_ILm/R_ILD = 1.2, R_ILD/R_LLd ≈ 2.0
- For R_x0 / R_t = 100: at R_ILm/R_ILD = 1.8, R_ILD/R_LLd ≈ 35.0

Note: The grid is fine and dense; the curves are smooth and concave upward. The origin is at (1.0, 1.0). The top-right corner is approximately (2.2, 40.0).

> This nomogram is used to interpret induction log responses in thick beds with no transition zone, correcting for skin effect, to estimate formation resistivity (R_t) and invaded zone resistivity (R_x0) from deep and medium induction log readings.

KEYWORDS: индукционный каротаж, палетка, R_ILm, R_ILD, R_x0, R_t, skin-effect, thick beds, 8" hole, no annulus, no transition zone, номограмма, интерпретация ГИС, каротажная палетка
----


Figure 10.3. Tornado chart, for determination of true formation resistivity ($R_f$) from measurements of induction resistivity and the laterolog 8.

Procedure for using this chart is as follows. The numbers were extracted from Table 10.1, at 14,613 ft.

1. Calculate two ratios from the raw resistivity data:

a. ILM/ILD = 410/300 = 1.37, and
b. LL8/ILD = 1500/300 = 5.

2. Plot the ratios on the tornado chart: ILM/ILD on the X-axis, and LL8/ILD on the Y-axis.
3. At the intersection point, read and record the following values:

a. From the heavy, solid black lines (nearly horizontal), $R_{xo}/R_f = 7.8$.
b. From the light, dashed black lines (nearly vertical), diameter of invasion, $d_l = 42$ in.
c. From the light, solid red lines (nearly vertical), $R_f/R_{ILd} = 0.94$.

4. From the ratios that were recorded from the tornado chart:

a. $R_f = (R_o/R_{ILd}) \times \text{ILD} = 0.94 \times 300 = 282$ ohm·m.
b. $R_{xo} = (R_{xo}/R_f) \times R_f = 7.8 \times 282 = 2200$ ohm·m.

5. Diameter of invasion at that point, $d_l = 42$ in.

The tornado chart for the induction log assumes that invasion follows a step profile, and that neither transition zones nor an annulus exist. In practice, invasion corrections using the tornado chart are often applied even when a transition zone is apparent. In this well, attempting to apply an invasion correction over the interval from 14,600 to 14,603 ft will result in points that plot outside the tornado chart. In this example, the maximum correction on the chart ($R_o/ILd = 0.4$) was applied to the deep induction log. Also, the tornado-chart readings could be ignored and the deep-induction reading used, because of the anomalous pattern of the curves. From 14,603 to 14,607 ft, invasion caused a significant difference between $R_{ILd}$ and $R_o$, whereas below 14,607 ft, the differences were minimal. This is shown in Figure 10.6
<!-- page 189 -->
178

ASQUITH AND KRYGOWSKI

Figure 10.4. Bulk-volume-water crossplot ($S_{\text{air}}$ vs. $P_{\text{ib}}$), Atoka Sandstone, Permian Basin, U.S.A.


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
- X-axis: Porosity, PhiNDgas, linear scale, range 0.00 to 0.40.
- Y-axis: Water Saturation, Swa, linear scale, range 0.00 to 0.60.
- Data: 25 black circular data points scattered across the plot. The points show a general trend of decreasing water saturation with increasing porosity, but with significant scatter.
- Curve: One smooth black curve is drawn through the data points, starting at (0.10, 0.40) and curving downward to (0.35, 0.02). The curve is labeled "0.02" at its right end, indicating the water saturation value at high porosity.
- The curve appears to represent a trend line or a model fit (possibly a capillary pressure or saturation-height relationship), with the data points showing actual measured values.
- The plot has a grid with major gridlines every 0.10 on both axes.
- No regression equation or R² is printed.
> Тренд: Уменьшение водонасыщенности (Swa) с ростом пористости (PhiNDgas), с заметной дисперсией данных; кривая показывает убывающую экспоненциальную или степенную зависимость, достигающую Swa = 0.02 при PhiNDgas ≈ 0.35.

KEYWORDS: водонасыщенность, пористость, кривая тренда, диаграмма рассеяния, Swa, PhiNDgas, геофизические данные, петрофизика, интерпретация, зависимость
----


Figure 10.5. Crossplot, water saturation ($S_{\text{air}}$) versus porosity ($P_{\text{ib}}$), for estimating permeability, Atoka Sandstone, Permian Basin, U.S.A.

The estimate of permeability is valid only if water saturation is irreducible. Permeability lines were extracted from Timur (1968). Permeability is scaled in millidarcies.


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
This is a crossplot of water saturation (Sw) versus porosity (PhiNDgas), with permeability (mD) as a family parameter.

- **X-axis**: Porosity, PhiNDgas, range 0.00 to 0.40, linear scale.
- **Y-axis**: Water Saturation, Swa, range 0.00 to 1.00, linear scale.
- **Curves**: Four lines representing constant permeability values: 10 mD, 25 mD, 50 mD, and 100 mD. These are smooth, upward-curving lines from left to right, indicating that for a given porosity, higher permeability corresponds to lower water saturation.
- **Data points**: Approximately 20–25 black circular data points scattered across the plot, mostly concentrated in the lower-left quadrant (porosity 0.10–0.25, water saturation 0.20–0.60), with a few outliers at higher porosity and lower saturation.
- **Trend**: The data points generally follow the trend of increasing permeability with increasing porosity and decreasing water saturation. Most points lie near or above the 10 mD curve, with a few falling near the 25–50 mD curves. There is no clear regression line or equation provided.

> Тренд: С увеличением пористости (PhiNDgas) и уменьшением водонасыщенности (Swa) наблюдается рост проницаемости (mD), что соответствует положению точек вдоль кривых 10, 25, 50, 100 mD.

KEYWORDS: водонасыщенность, пористость, проницаемость, кривые постоянной проницаемости, кроссплот, Sw, PhiNDgas, mD, петрофизика, интерпретация ГИС
----


<!-- page 190 -->
Log Interpretation Case Studies

179


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: increases downward, units: feet (MD), range: approximately 14600 ft to 14700 ft (based on visible scale and curve position).

Left panel:
- Track 1: GR (gamma ray), scale: 0–150 API, unit: API, curve: solid line. 
  - Curve shows a high background (~100 API) with a distinct negative anomaly (drop to ~50 API) centered at ~14600 ft, followed by a return to high values.
- Track 2: Vshale (volumetric shale), scale: 0–1, unit: v/v (volume fraction), curve: solid line. 
  - Curve is mostly flat at ~0.2–0.3, with a slight dip to ~0.1 at the same interval as the GR anomaly.

Right panel:
- Track 1: Rt (true resistivity), scale: 0.2–2000 Ω·m, unit: Ω·m, curve: solid line. 
  - Curve shows a high resistivity (~1000–2000 Ω·m) above 14600 ft, then a sharp drop to ~0.2 Ω·m at the 14600 ft interval, followed by a rise back to high values.
- Track 2: ILD (deep induction resistivity), scale: 0.2–2000 Ω·m, unit: Ω·m, curve: solid line. 
  - Curve behavior is similar to Rt: high above 14600 ft, sharp drop to ~0.2 Ω·m at 14600 ft, then rise.
- Track 3: Ro (resistivity of formation water), scale: 0.2–20 Ω·m, unit: Ω·m, curve: solid line. 
  - Curve is flat at ~0.2 Ω·m across the entire visible interval.
- Track 4: Swa (water saturation), scale: 0–1, unit: v/v (volume fraction), curve: solid line. 
  - Curve is flat at ~0.95–1.0 above 14600 ft, then drops sharply to ~0.2 at 14600 ft, then rises back to ~1.0.
- Track 5: Sat (saturation), scale: 0–1, unit: v/v (volume fraction), curve: solid line. 
  - Curve is flat at ~1.0 above 14600 ft, then drops sharply to ~0.2 at 14600 ft, then rises back to ~1.0.
- Track 6: BVW (bulk volume water), scale: 0–20, unit: % (percent), curve: solid line. 
  - Curve is flat at ~20% above 14600 ft, then drops sharply to ~4% at 14600 ft, then rises back to ~20%.
- Track 7: Bitical (bitumen or hydrocarbon indicator), scale: 0–20, unit: inches (likely arbitrary or scaled), curve: solid line. 
  - Curve is flat at ~0 above 14600 ft, then shows a sharp rise to ~20 at 14600 ft, then drops back to ~0.

Interpretation:
- The interval around 14600 ft shows a clear hydrocarbon-bearing zone: low GR, low Rt/ILD, low Swa/Sat/BVW, and high Bitical.
- The zone is interpreted as a clean, high-resistivity hydrocarbon (likely oil or gas) sand.
- The surrounding zones are shaly or water-saturated.

Interval table:
| Интервал, ft | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|--------------|------------------------|-------------------|-------------------------------|
| 14600–14610 | Песчаник (по кривым)   | GR: отрицательная аномалия; Rt/ILD: резкое падение; Swa/Sat/BVW: резкое падение; Bitical: резкий рост | Нефтеносный пласт (гидрокарбонатный) |

KEYWORDS: well log, gamma ray, resistivity, water saturation, hydrocarbon indicator, depth, feet, interpretation, oil zone, sandstone
----


Figure 10.6. Computer-processed evaluation log, Atoka Sandstone, Permian Basin, U.S.A.

In the interval from 14,600 ft to 14,625 ft, note:

1) In track 1, volume of shale (Vshale) was calculated from the gamma ray log. These criteria were the basis for calculation: GR_drea = 15 API units; GR_shale = 65 API units.
2) In track 2, shading emphasizes the separation between resistivity of the sandstone at water saturation of 100% (R_s) and true formation resistivity (R_f), as derived from the deep resistivity (ILD), which shows the presence of hydrocarbons. The greater the separation, the greater the hydrocarbon saturation.
3) In track 3, these five important quantities are shown, in order from left to right: (1) water saturation of the uninvaded zone, computed by the ratio method (S_wr); (2) water saturation of the uninvaded zone, computed by the Archie method (S_wr); (3) the differential caliper log (DiffCal), which is the caliper value minus the bit size; (4) porosity (PhiNDgas); and (5) bulk volume water (BVW). The black area (between PhiNDgas and BVW) shows the proportion of pore space occupied by hydrocarbons (in this instance, gas). The gray area (between BVW and zero, at the track edge) shows the proportion of pore space occupied by water.
<!-- page 191 -->
180

ASQUITH AND KRYGOWSKI

## Case Study 2:

### MISSISSIPPIAN MISSION CANYON FORMATION, WILLISTON BASIN, U.S.A.:

*The Problem.*

Case Study 2 illustrates the interpretation of mixed-lithology carbonate rock. Some lithology-porosity crossplots are used to confirm the types of rock seen in a core. For the various crossplots the stratigraphic interval is divided into two zones, based on the production potential estimated from observation of the logs.

# **Background**

A wildcat well is in progress in the Williston Basin, to be drilled to the Ordovician Red River Formation. As drilling proceeds, two zones are encountered that have hydrocarbon shows—the Mississippian Mission Canyon and the Devonian Duperow. The well has just penetrated the Devonian Duperow, the second “show” zone. A decision is made to stop and drill-stem test (DST) the Duperow. Unfortunately, the drill-stem-test tool is stuck in the borehole. Several attempts are made to remove the tool but none succeed. Meanwhile, collapse of the borehole wall (caving) begins.

Now you face the choice of either halting drilling—with hope that the first show zone, the Mississippian Mission Canyon Formation, might be a productive reservoir—or continuing efforts to remove the DST tool. If the “fish” (the stuck DST tool) is removed from the hole successfully, the Duperow can be tested and the hole can be deepened to the Red River Formation. However, more attempts to recover the fish undoubtedly will lead to further deterioration of the hole, and logging measurements taken when walls of the borehole are enlarged may be unreliable. Also, the DST tool might not be dislodged.

Because the well is a wildcat, you made a decision several weeks ago to core the Mission Canyon. The Mission Canyon is at approximately 9297 ft to 9409 ft. Rock was cored from 9302 ft to 9358 ft. Twenty-five feet of oil-stained, fractured, microcrystalline dolomite was recovered; the remaining core consisted of microcrystalline limestone and anhydrite. After coring, several drill-stem tests were tried; when none were successful, drilling was resumed.

You decided that information from coring is favorable enough to halt drilling, to log to the top of the fish while hole conditions seem still to be reasonably good, and then to assess the potential of the Mission Canyon

for production of oil and gas. Your company agrees with your suggestion to run a very complete log package, because the well is exploratory and carbonate rocks commonly are more difficult to evaluate than sandstones. The logs are shown in Figures 10.7, 10.8, and 10.9.

# **Well site information and other pertinent information:**

- mean annual surface temperature = 40°F
- formation temperature ($T_f$) = 207°F
- formation water resistivity ($R_w$) at $T_f$ = 0.023 ohm-m
- mud filtrate resistivity ($R_{mf}$) at $T_f$ = 0.017 ohm-m
- $Dt_{fl}$ = 185 μsec/ft, the acoustic-wave fluid transit time of saltwater mud filtrate
- $RHO_{fl}$ = 1.1 gm/cc, which is the density of saltwater mud filtrate
- tortuosity factor ($a$) = 1, cementation exponent ($m$) = 2, and saturation exponent ($n$) = 2

Preliminary examination of the logs indicates that several zones in the Mission Canyon are quite porous. Log data and core data indicate that the zone is potentially productive. A reliable estimate of the amount of oil in place is needed; but first, verify the quality of the log data, confirm the estimate of formation water resistivity, and calculate porosity and fluid saturations.

# **Tasks required for interpretation of the logs**

- General comparison of lithologies described from the core with lithologies predicted from the logs would give you some opinion about whether the logging tools operated properly. The neutron porosity-density porosity and neutron porosity-sonic interval transit time crossplots would provide the necessary information. In addition, a mineral identification (“MID”) plot (apparent matrix density, $RHO_{maa}$, vs. apparent matrix traveltime, $DT_{maa}$) and an M-N lithology plot would test the proposition that the rock is composed of more than two significant minerals. Also, neutron-density crossplot porosity can be estimated from the neutron-density crossplot. This quantity (shown in the crossplots as $PHIE$, effective porosity) will be used in later calculations.

- To confirm the estimate of formation water saturation ($R_w$) several methods could be used. Apparent water resistivity ($R_{wa}$) generally is dependable, but in this case the most useful
<!-- page 192 -->
Log Interpretation Case Studies

181

method is a Pickett plot, a plot of formation resistivity against porosity. Not only would it indicate the water saturations of the zones of interest, it also would evaluate the number that was used for formation water resistivity ($R_w$), and the estimated cementation exponent ($m$). (Again, both methods are shown in the answer section for completeness.)

- Calculate water saturation of the formation ($S_w$), and use $S_w$ and PHIE to calculate bulk volume water (BVW) and create a BVW plot.
- Other useful quantities are moveable hydrocarbon index (MHI), moveable hydrocarbon saturation (MOS), and residual hydrocarbon saturation (ROS), all of which are indicators of producibility.
- Finally, calculate the volume of oil in place; use Equation 10.8.

Because information about porosity is required for the Pickett plot, and because the neutron-density crossplot porosity is the best choice, start with lithology-porosity crossplots. Work tables 10.3a, 10.3b, and 10.3c provide a start for measuring the log values.

Useful equations:

Apparent matrix density, RHOmaa:

$$\rho_{maa} = \frac{\rho_b - \phi_{ND} \times \rho_{fl}}{1 - \phi_{ND}} \quad 10.21 \text{ (Equation 4.11)}$$

Apparent matrix traveltime, DTmaa:

$$\Delta t_{maa} = \frac{\Delta t - \phi_{NS} \times \Delta t_{fl}}{1 - \phi_{NS}} \quad 10.22 \text{ (Equation 4.12)}$$

Lithology $M$:

$$M = \frac{\Delta t_{fl} - \Delta t}{\rho_b - \rho_{fl}} \times 0.01$$

$$\left( M = \frac{\Delta t_{fl} - \Delta t}{\rho_b - \rho_{fl}} \times 0.003 \text{ (metric)} \right) \quad \text{(Equation 4.9)} \quad 10.23$$

Lithology $N$:

$$N = \frac{\phi_{Nfl} - \phi_N}{\rho_b - \rho_{fl}} \quad 10.24 \text{ (Equation 4.10)}$$

Apparent water resistivity, $R_{wa}$:

$$R_{wa} = \frac{R_s \times \phi^m}{a} \quad 10.25 \text{ (Equation 7.16)}$$

Table 10.3a. Case Study 2: Mission Canyon Formation, Williston Basin, U.S.A.: Raw data work table. The symbol "v/v" indicates volume-for-volume decimal fraction.

|  **Parameters**  |   |   |   |   |
| --- | --- | --- | --- | --- |
|  Ann. Mean Surf. Temp: 40°F |   |   |   | Rw (measured): (not given)  |
|  Total Depth: 11,122 ft |   |   |   | Rw @ fm. temp.: 0.023 ohm-m @ 207°F  |
|  Bottom Hole Temp: (thermometer failed) |   |   |   | Rmf (measured): 0.046 ohm-m @ 74°F  |
|  Formation Depth: 9,300 ft |   |   |   | Rmf @ fm. temp.: 0.017 ohm-m @ 207°F  |
|  Formation Temperature: 207°F |   |   |   |   |
|  DT matrix (Wyllie): 47.6 μsec/ft |   |   |   | DT fluid (Wyllie): 185 μsec/ft  |
|  RHO matrix: 2.71 g/cm³ |   |   |   | RHO fluid: 1.1 g/cm³  |
|  PHIN fluid: 1 |   |   |   |   |
|   | a: 1 | m: 2 | n: 2 |   |
<!-- page 193 -->
182

ASQUITH AND KRYGOWSKI

Table 10.3a. Case Study 2: Mission Canyon Formation, Williston Basin, U.S.A.: Raw data work table. The symbol "v/v" indicates volume-for-volume decimal fraction. (Cont'd.)

|  Raw data  |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- |
|  Depth feet | ILD ohm-m | ILS ohm-m | MSFL ohm-m | DT μsec/ft | DPHI v/v decimal | NPHI v/v decimal  |
|  9,310 | 26 | 20.5 | 1.2 | 63 | 0.090 | 0.260  |
|  9,322 |  |  |  |  |  |   |
|  9,326 | 17 | 8.3 | 3.8 | 53.5 | 0.030 | 0.120  |
|  9,332 | 9 | 6.1 | 2.4 | 58 | 0.050 | 0.140  |
|  9,335 |  |  |  |  |  |   |
|  9,347 |  |  |  |  |  |   |
|  9,353 |  |  |  |  |  |   |
|  9,362 |  |  |  |  |  |   |
|  9,367 | 22 | 16 | 8.8 | 52.5 | -0.015 | 0.125  |
|  9,373 | 11 | 7.7 | 3.5 | 53.5 | 0.000 | 0.155  |
|  9,376 |  |  |  |  |  |   |
|  9,383 |  |  |  |  |  |   |
|  9,387 |  |  |  |  |  |   |
|  9,398 |  |  |  |  |  |   |
|  9,406 | 5.1 | 3.5 | 2.2 | 55 | 0.030 | 0.150  |

Table 10.3b. Case Study 2: Mission Canyon Formation, Williston Basin, U.S.A.: Work table for determination of lithology. The symbol "v/v" indicates volume-for-volume decimal fraction.

|  Lithology Calculations  |   |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  Depth feet | RHOB g/cm³ | PhiNDxpt v/v decimal | RHOmaa g/cm³ | PhiNSxpt v/v decimal | DTmaa μsec/ft | M | N  |
|  9,310 | 2.57 | 0.170 | 2.865 | 0.145 | 42.3 | 0.833 | 0.505  |
|  9,322 |  |  |  |  |  |  |   |
|  9,326 | 2.66 | 0.075 | 2.788 | 0.065 | 44.4 | 0.842 | 0.563  |
|  9,332 | 2.63 | 0.095 | 2.790 | 0.090 | 45.4 | 0.830 | 0.562  |
|  9,335 |  |  |  |  |  |  |   |
|  9,347 |  |  |  |  |  |  |   |
|  9,353 |  |  |  |  |  |  |   |
|  9,362 |  |  |  |  |  |  |   |
|  9,367 | 2.73 | 0.060 | 2.838 | 0.060 | 44.0 | 0.811 | 0.535  |
|  9,373 | 2.71 | 0.085 | 2.860 | 0.070 | 43.6 | 0.817 | 0.525  |
|  9,376 |  |  |  |  |  |  |   |
|  9,383 |  |  |  |  |  |  |   |
|  9,387 |  |  |  |  |  |  |   |
|  9,398 |  |  |  |  |  |  |   |
|  9,406 | 2.66 | 0.090 | 2.816 | 0.075 | 44.5 | 0.832 | 0.544  |
<!-- page 194 -->
Log Interpretation Case Studies

183

Table 10.3c. Case Study 2: Mississippian Mission Canyon Formation, Williston Basin, U.S.A.: Work table for calculation of water saturation and other estimators. The symbol "v/v" indicates volume-for-volume decimal fraction.

|  Saturation and other calculations  |   |   |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  Depth feet | Rwa ohm-m | Ro ohm-m | Sw v/v decimal | Sxo v/v decimal | MHI v/v decimal | MOS v/v decimal | ROS v/v decimal | BVW  |
|  9,310 | 0.751 | 0.8 | 0.166 | 0.700 | 0.237 | 0.534 | 0.300 | 0.028  |
|  9,322 |  |  |  |  |  |  |  |   |
|  9,326 | 0.096 | 4.1 | 0.490 | 0.892 | 0.550 | 0.401 | 0.108 | 0.037  |
|  9,332 | 0.081 | 2.5 | 0.532 | 0.886 | 0.601 | 0.354 | 0.114 | 0.051  |
|  9,335 |  |  |  |  |  |  |  |   |
|  9,347 |  |  |  |  |  |  |  |   |
|  9,353 |  |  |  |  |  |  |  |   |
|  9,362 |  |  |  |  |  |  |  |   |
|  9,367 | 0.079 | 6.4 | 0.539 | 0.733 | 0.736 | 0.194 | 0.267 | 0.032  |
|  9,373 | 0.079 | 3.2 | 0.538 | 0.820 | 0.656 | 0.282 | 0.180 | 0.046  |
|  9,376 |  |  |  |  |  |  |  |   |
|  9,383 |  |  |  |  |  |  |  |   |
|  9,387 |  |  |  |  |  |  |  |   |
|  9,398 |  |  |  |  |  |  |  |   |
|  9,406 | 0.041 | 2.8 | 0.746 | 0.977 | 0.764 | 0.231 | 0.023 | 0.067  |
<!-- page 195 -->
184

ASQUITH AND KRYGOWSKI


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth range: 9300 to 9400 feet, depth increases downward.
Depth units: feet.

Left track:
- Curve: GR (gamma ray)
  - Scale: 0 to 100 API units
  - Line style: solid line
  - Behaviour: high values (80–100 API) in upper interval, sharp decrease to ~20 API at ~9320 ft, then fluctuating between 20–60 API
- Curve: CALI (caliper)
  - Scale: 6 to 16 inches
  - Line style: dashed line
  - Behaviour: relatively stable at ~8 inches, minor fluctuations, no significant washouts

Right track:
- Curve: LLD (deep laterolog)
  - Scale: 0.2 to 2000 ohm·m
  - Line style: solid line
  - Behaviour: high resistivity (>1000 ohm·m) from 9300 to 9315 ft, then drops to ~100 ohm·m, fluctuates between 50–200 ohm·m, with a peak near 9370 ft
- Curve: ILS (laterolog 7, shallow)
  - Scale: 0.2 to 2000 ohm·m
  - Line style: dashed line
  - Behaviour: similar to LLD but with higher values in low-resistivity zones, indicating invasion
- Curve: MSFL (microspherically focused log)
  - Scale: 0.2 to 2000 ohm·m
  - Line style: dash-dot line
  - Behaviour: closely follows ILS, with slightly higher values, indicating shallow invasion zone

Interpretation:
- Interval 9300–9315 ft: high GR, high resistivity — likely non-reservoir (shale or tight sand)
- Interval 9315–9370 ft: low GR, moderate resistivity — possible reservoir sand
- Interval 9370–9400 ft: moderate GR, resistivity peaks — possible thin sand or gas zone

No perforation intervals or interpreted porosity/saturation panels are visible.

KEYWORDS: well log, gamma ray, caliper, laterolog, microspherically focused log, resistivity, depth, feet, API, ohm·m, interpretation, reservoir
----


Figure 10.7. Dual laterolog-MSFL with gamma ray log and caliper log, Mission Canyon Formation, Williston Basin, U.S.A.

From 9308 ft to 9408 ft: Note the separation of the three resistivity logs, which read the following resistivities: lowest resistivity, MSFL ($R_{op}$), intermediate resistivity, LLS ($R_i$), and highest resistivity, LLD ($R_i$). On a Dual Laterolog-MSFL this type of resistivity profile indicates presence of hydrocarbons (see Chapter 1).
<!-- page 196 -->
Log Interpretation Case Studies

185


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: increases downward, from 9300 to 9400 feet (MD — measured depth).
Track 1 (leftmost): GR (gamma ray), scale 0–100 API, units: API, line style: solid curve. Curve shows high values (≈80–100 API) in upper interval, then a sharp drop to low values (≈20–30 API) in lower interval. A dashed line marks a boundary at ~9340 ft.
Track 2: CALI (caliper), scale 6–16 inches, units: inches, line style: solid curve. Curve shows relatively stable values around 8–9 inches, with minor fluctuations. A dashed line marks a boundary at ~9340 ft.
Track 3 (rightmost): DRHO (density), scale -0.05 to 0.63 g/cm³, units: g/cm³, line style: solid curve. Curve shows high values (~0.60–0.63 g/cm³) in upper interval, then a sharp drop to lower values (~0.45–0.50 g/cm³) in lower interval. A dashed line marks a boundary at ~9340 ft.
Track 4: DPHI (density porosity), scale -0.15 to 0.45 (sv-decimal), units: sv-decimal, line style: solid curve. Curve shows low values (~0.05–0.15) in upper interval, then a sharp increase to higher values (~0.30–0.40) in lower interval. A dashed line marks a boundary at ~9340 ft.
Track 5: NPHI (neutron porosity), scale -0.15 to 0.45 (sv-decimal), units: sv-decimal, line style: solid curve. Curve shows low values (~0.05–0.15) in upper interval, then a sharp increase to higher values (~0.30–0.40) in lower interval. A dashed line marks a boundary at ~9340 ft.

Interval table:
| Интервал, ft | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|--------------|------------------------|-------------------|-------------------------------|
| 9300–9340    | Верхняя часть — высокие GR, низкие DPHI/NPHI, высокие DRHO | GR: высокие, CALI: стабильный, DRHO: высокие, DPHI/NPHI: низкие | Вероятно, глина или плотный аргиллит |
| 9340–9400    | Нижняя часть — низкие GR, высокие DPHI/NPHI, низкие DRHO | GR: низкие, CALI: стабильный, DRHO: низкие, DPHI/NPHI: высокие | Вероятно, пористый песчаник или известняк |

No results panel (Кп, Кн, Кпр, etc.) is visible.
KEYWORDS: well log, gamma ray, caliper, density, neutron porosity, measured depth, lithology interpretation, GR, CALI, DRHO, DPHI, NPHI, API, g/cm³, sv-decimal, feet
----


Figure 10.8. Combination neutron-density log with gamma ray log and caliper log, Mission Canyon Formation, Williston Basin, U.S.A.

From 9308 ft to 9408 ft, porosities recorded by the neutron (NPHI) and density (DPHI) curves are high. Both are recorded in limestone units, in tracks 2 and 3. The neutron log reads higher porosity than the density log, indicating that the rock is dolomite.


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth increases downward. Depth axis: measured depth (MD), units: feet, range: 9300–9400 ft.

Track 1 (left):
- Curves: GR (gamma ray), CALI (caliper)
- GR scale: 0–100 API units, linear
- CALI scale: 6–16 inches, linear
- GR curve: irregular, high-amplitude fluctuations, multiple peaks and troughs, no specific values marked
- CALI curve: smooth, mostly flat near 12 inches, slight variations

Track 2 (right):
- Curve: DT (sonic transit time)
- DT scale: 40–80 μs/ft, linear
- DT curve: highly variable, multiple sharp peaks and troughs, no specific values marked

No bed boundaries, perforation intervals, or interpreted intervals are marked.
No results panel (Кп, Кн, Кпр, etc.) is present.

KEYWORDS: well log, GR, CALI, DT, sonic log, gamma ray, caliper, measured depth, feet, API, μs/ft
----


Figure 10.9. Sonic log with gamma ray log and caliper log, Mission Canyon Formation, Williston Basin, U.S.A.

From 9308 ft to 9408 ft, note that zones of porous rock are numerous. (They are indicated by increase of interval transit time (DT) in tracks 2 and 3.)
<!-- page 197 -->
186

ASQUITH AND KRYGOWSKI

## Case Study 2:

### MISSISSIPPIAN MISSION CANYON FORMATION, WILLISTON BASIN, U.S.A.:

#### The Solution.

Information from the logs and cores produced the following positive indicators: (1) 25 ft of oil-stained core, (2) porous zones, indicated on the neutron-density and sonic logs, and (3) separation of curves on resistivity logs, indicative of invasion in the porous zones. The information also produced this negative indicator: evidence that water saturation is greater in the lower part of the logged interval.

In this case, there is no significant conflicting information; all information points to the presence of hydrocarbons in the rock. Therefore, the task is composed of two parts: (1) to assess the quality of the logs and of the well site processing, so that a confident estimate of the oil in place can be made, and then (2) to judge whether the Mission Canyon is a reservoir that will produce oil and gas in volumes sufficient for a suitable return on investment.

#### Information from the logs

The log package run in this well is complete; it includes a suite for measurement of resistivity, and a combination neutron-density log and a sonic log for measurement of porosity and estimation of lithology.

Because walls of the borehole have caved, your assessment begins with a careful check of the caliper curve, CALI (Figure 10.8). The caliper log shows relatively constant hole diameter and no significant, differential enlargement. Consistency of the hole diameter indicates that log measurements should be reliable.

The next step in evaluation includes examination of the resistivity logs (Figure 10.7). The salt-saturated drilling mud ($R_{mf} \sim R_w$) necessitated using a dual laterolog with a microspherically focused log (MSFL). The MSFL measures resistivity of the flushed zone ($R_{xo}$), whereas the shallow laterolog (LLS) and deep laterolog (LLD) measure resistivities of the invaded ($R_i$) and uninvaded ($R_i$) zones, respectively.

Next, scrutinize the resistivity curves to identify invasion profiles; they are useful for location of zones that merit detailed analysis.

Between 9308 ft and 9409 ft, the resistivity curves (MSFL, LLS, and LLD) show different values of $R_{xo}$, $R_i$, and $R_i$; the curves are separated. The separation suggests that the rock is invaded, and that hydrocarbons are in the porous and permeable zones. (If the

curves were not separated you could conclude that either the formation wasn't invaded, or that hydrocarbons were not present.)

Also, note that the zones of porous rock low in the formation (9370 ft to 9409 ft) show less separation between the MSFL and the deep laterolog, LLD. The lessening of separation in the lower zones indicates higher water saturations. (Remember: Higher water saturations mean lower hydrocarbon saturations.)

Porous and permeable zones in the interval from 9308 ft to 9409 ft are identified by inspecting the neutron-density log (Figure 10.8) and the sonic log (Figure 10.9); more than eleven zones of porous and permeable rock can be identified. On the neutron-density log (Figure 10.8), the zones of porosity and permeability are evident as concurrent increase in neutron porosity (NPHI) and density porosity (DPHI). They are identified on the sonic log by increase in the interval transit time (DT).

#### Information from crossplots

As evaluation of the Mission Canyon continues, you decide to compare your observations of the core lithologies with inferences about lithology, derived from log data. Study of the core indicates that the rock is microcrystalline dolomite, limestone and anhydrite. To compare this information with log data, construct a neutron-density porosity crossplot, a neutron-sonic porosity crossplot, a matrix identification plot, and an M-N lithology plot. (Ordinarily only one or two of the crossplots described here would be created, but all are discussed here for experience in learning.) On the basis of observations from the logs, you divide the zone into two intervals on the crossplots: the "Upper MC," from 9308 ft to 9370 ft, and the "Lower MC," from 9370 ft to 9409 ft.

The first crossplot is a neutron-density crossplot (Figure 10.10). It is consistent with the core description, showing a mixture of lithologies ranging from limestone to dolomite. The scatter of rock types in the crossplot is more than the rock types described in the core, because the limits of vertical resolution of the logging tools introduce averaging ("smearing") of lithologic effects on signals, especially among thin beds. From Figure 10.10, neutron-density crossplot porosity ($PhiNDxpt$) can be estimated; it is determined from the location of each point with respect to the porosity indications on each lithology line. These numbers will be used to construct a Pickett plot, to calculate apparent water resistivity ($R_{wa}$), and to estimate water saturation ($S_w$). Neutron-density crossplot porosity also will be used to calculate apparent matrix
<!-- page 198 -->
Log Interpretation Case Studies 187

density, RHOmaa, for use in a matrix identification plot.

The second crossplot is a neutron-sonic crossplot (Figure 10.11). It too is consistent with core data, showing scatter of points between the limestone and dolomite lines. Neutron-sonic crossplot porosity (PhiNSxpt) can be estimated in the same manner as neutron-density crossplot porosity was estimated; it will be used to calculate apparent matrix density, DTmaa, one of the variables in the matrix identification plot.

The third crossplot augments results of the first two. In the matrix identification (MID) plot (Figure 10.12) apparent matrix density and apparent matrix traveltime (estimated from Figures 10.10 and 10.11, and Equations 10.21 and 10.22) are used to display a complex model of the rock. Figure 10.12 shows that most of the points are of limestone or dolomite (or a mixture) with fewer points that tend slightly toward anhydrite.

The fourth crossplot is the M-N plot (Figure 10.13). Like the MID plot, it is a complex model of lithology, based on the plotting of two calculated parameters, M, a function of sonic and bulk density, and N, a function of bulk density and neutron porosity (Equations 10.23 and 10.24). The M-N plot (Figure 10.13) shows that the Mission Canyon Formation consists of limestone and dolomite.

Calculations to determine porosities, apparent matrix values, and M and N are based on raw log data shown in Table 10.4a. Porosities, apparent matrix density, matrix interval transit time, and the lithology-dependent variables M and N are shown in Table 10.4b.

The next step is to verify the estimate of formation water resistivity. Although a single method usually is sufficient, two are shown here for aid in learning. The methods are described in detail in Chapter 7. The first method is calculation of Rwa (apparent water resistivity) from the LLD and neutron-density crossplot porosity (Equation 10.25). As shown in the Solution Table (Table 10.4c) the two lowest values of Rwa, hence the best estimates of Rw, are 0.033 ohm-m (at 9387 ft) and 0.041 ohm-m (at 9406 ft). These numbers are only a bit higher than the reported Rw of 0.023 ohm-m. The difference could be due to the manner in which logs were read, the effects of properties of adjacent beds on log readings, or to residual hydrocarbons. Rwa also is presented in a log format (Figure 10.14), plotted in the same logarithmic track as the deep laterolog, LLD. In some cases, Rwa plotted in this format allows for a better estimate of Rw.

The second method to approximate formation-

water resistivity is a Pickett plot (Figure 10.15). The deep laterolog (LLD) is used for plotting resistivity along the X-axis. Neutron-density crossplot porosity (PHIE: “effective porosity”), is plotted on the Y-axis. The water-bearing line—drawn through the lower part of the lowest cluster of points—estimates formation water resistivity (Rw) to be 0.023 ohm-m, in agreement with the published value. From the slope of the Ro line—the line signifying that water saturation is 100%—data on the Pickett plot also indicate that the cementation exponent (m) is 2.

As discussed previously, deep induction resistivity of the stratigraphic section from 9370 ft to 9409 ft is less than that of the upper Mission Canyon (Figure 10.7). The likelihood of production of water from strata at 9370 ft to 9409 ft also is indicated by evidence from the Pickett crossplot (Figure 10.15). Most data points that show water saturations greater than 0.75 (75%) are of the “Lower MC” zone.

Saturation lines on the Pickett plot (Figure 10.15) are based on the saturation exponent (n) of 2.

At this juncture in your evaluation of the Mission Canyon from 9308 ft to 9409 ft, you have reason to be optimistic about the potential of the well. The interval shows evidence of porosity and invasion, it comprises interbedded permeable strata and “tight” strata, and the rock type, dolomite, generally is a good reservoir. However, you should be concerned about whether completion of the lower Mission Canyon should be attempted, especially from 9370 ft to 9409 ft. The well site log calculation, the diminished separation of resistivity curves with depth, and high water saturations on the Pickett crossplot (Figure 10.15) all strongly support your judgment that fluid from the lower Mission Canyon will not be water-free. How much water these zones will produce, relative to oil, is not known.

In order to support the decision to not perforate the lower Mission Canyon, a bulk-volume-water (BVW) crossplot is constructed (Figure 10.16). On the bulk-volume-water plot, data points above 0.035 are mostly from porosity zones of the lower Mission Canyon; these zones are not at irreducible water saturation, and they will produce some water.

The positions of data points on a bulk-volume-water crossplot can indicate differences in types of carbonate-rock porosity. Points that are below 0.035 generally represent rock with vuggy porosity, with some intercrystalline porosity (Table 7.1).

One of the last log evaluation procedures is finding values for the moveable hydrocarbon index (MHI), for moveable oil saturation (MOS), and for residual-oil saturation (ROS). Most of the moveable hydrocarbon index values are less than 0.7, and these are concen-
<!-- page 199 -->
188

ASQUITH AND KRYGOWSKI

trated in the upper Mission Canyon (Table 10.4c); so oil in these beds is moveable. Moveability of oil also is apparent from the high values of moveable oil saturation and low values of residual oil saturation (Table 10.4c).

A log of water saturation, porosity, and bulk volume water is shown in Figure 10.17.

Your log evaluation of this well has been uncommonly detailed. In part, the extensive evaluation was necessary; the well is a wildcat well, and visual inspection of logs of the lower Mission Canyon suggested that water would be produced. Fortunately, because of the log package used for this well a large amount of data was available for analysis.

Rather early in the evaluation the fact was apparent that the data seemed to support a decision to set pipe. Nevertheless, to know the correct interval for perforating was important, so that production of water could be minimized.

For the gross interval from 9308 ft to 9357 ft, the

estimated recovery of oil from the Mission Canyon Formation is 376,650 stock-tank barrels (STB) (Equation 10.8). This number is based on the following parameters:

- drainage area = 160 acres;
- reservoir thickness = 28 ft;
- average porosity = 0.11 (11%);
- average water saturation = 0.49 (49%);
- recovery factor = 0.20; and
- $B_{oi}$ (estimated) = 1.35.

The Mission Canyon Formation was perforated selectively from 9308 ft to 9357 ft. After a light acid clean-up, the well's production was 569 barrels of oil per day (BOPD), 31 barrels of water a day (BWPD), and 700,000 cubic feet of gas per day (700 mcfgpd); the gas/oil ratio was 1230:1. During the first five months the well produced 56,495 barrels of oil and 5,802 barrels of water.
<!-- page 200 -->
Log Interpretation Case Studies

189

Table 10.4a. Case Study 2: Mission Canyon Formation, Williston Basin, U.S.A.: Raw data solution table. The symbol "v/v" indicates volume-for-volume decimal fraction.

|  Parameters  |   |   |   |   |
| --- | --- | --- | --- | --- |
|  Ann. Mean Surf. Temp: 40°F |   |   | Rw (measured): ohm-m @ °F  |   |
|  Total Depth: 11,122 ft |   |   | Rw @ fm. temp.: 0.023 ohm-m @ 207°F  |   |
|  Bottom Hole Temp: (thermometer failed) |   |   | Rmf (measured): 0.46 ohm-m @ 74°F  |   |
|  Formation Depth: 9,300 ft |   |   | Rmf @ fm. temp.: 0.017 ohm-m @ 207°F  |   |
|  Formation Temperature: 207°F |   |   |   |   |
|  DT matrix (Wyllie): 47.6 μsec/ft |   |   | DT fluid (Wyllie): 185 usec/ft  |   |
|  RHO matrix: 2.71 g/cm³ |   |   | RHO fluid: 1.1 g/cm³  |   |
|  PHIN fluid: 1 |   |   |   |   |
|   | a: 1 | m: 2 | n: 2 |   |

|  Raw data  |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- |
|  Depth feet | ILD ohm-m | ILS ohm-m | MSFL ohm-m | DT μsec/ft | DPHI v/v decimal | NPHI v/v decimal  |
|  9,310 | 26 | 20.5 | 1.2 | 63 | 0.090 | 0.260  |
|  9,322 | 18 | 10 | 5.7 | 52 | 0.020 | 0.060  |
|  9,326 | 17 | 8.3 | 3.8 | 53.5 | 0.030 | 0.120  |
|  9,332 | 9 | 6.1 | 2.4 | 58 | 0.050 | 0.140  |
|  9,335 | 32 | 6.8 | 13 | 52.5 | 0.035 | 0.085  |
|  9,347 | 4.8 | 2.4 | 0.8 | 61.5 | 0.100 | 0.230  |
|  9,353 | 4.7 | 2.3 | 1.6 | 61.5 | 0.045 | 0.250  |
|  9,362 | 40 | 17 | 11 | 53 | -0.015 | 0.135  |
|  9,367 | 22 | 16 | 8.8 | 52.5 | -0.015 | 0.125  |
|  9,373 | 11 | 7.7 | 3.5 | 53.5 | 0.000 | 0.155  |
|  9,376 | 5.1 | 3.3 | 2.1 | 57.5 | 0.075 | 0.165  |
|  9,383 | 3.3 | 1.5 | 1.2 | 62 | 0.090 | 0.220  |
|  9,387 | 3.3 | 1.5 | 1.3 | 62 | 0.080 | 0.135  |
|  9,398 | 6.4 | 3.2 | 2.2 | 58 | 0.055 | 0.135  |
|  9,406 | 5.1 | 3.5 | 2.2 | 55 | 0.030 | 0.150  |
<!-- page 201 -->
190

ASQUITH AND KRYGOWSKI

Table 10.4b. Case Study 2: Mission Canyon Formation, Williston Basin, U.S.A.: Work table for determination of lithology. The symbol "v/v" indicates volume-for-volume decimal fraction.

|  Lithology Calculations  |   |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  Depth feet | RHOB g/cm³ | PhiNDxpt v/v decimal | RHOmaa g/cm³ | PhiNSxpt v/v decimal | DTmaa μsec/ft | M | N  |
|  9,310 | 2.57 | 0.170 | 2.865 | 0.145 | 42.3 | 0.833 | 0.505  |
|  9,322 | 2.68 | 0.040 | 2.744 | 0.035 | 47.2 | 0.843 | 0.596  |
|  9,326 | 2.66 | 0.075 | 2.788 | 0.065 | 44.4 | 0.842 | 0.563  |
|  9,332 | 2.63 | 0.095 | 2.790 | 0.090 | 45.4 | 0.830 | 0.562  |
|  9,335 | 2.65 | 0.055 | 2.744 | 0.075 | 41.8 | 0.853 | 0.589  |
|  9,347 | 2.55 | 0.160 | 2.825 | 0.125 | 43.9 | 0.852 | 0.531  |
|  9,353 | 2.64 | 0.140 | 2.888 | 0.130 | 43.0 | 0.803 | 0.488  |
|  9,362 | 2.73 | 0.065 | 2.848 | 0.065 | 43.8 | 0.808 | 0.529  |
|  9,367 | 2.73 | 0.060 | 2.838 | 0.060 | 44.0 | 0.811 | 0.535  |
|  9,373 | 2.71 | 0.085 | 2.860 | 0.070 | 43.6 | 0.817 | 0.525  |
|  9,376 | 2.59 | 0.120 | 2.792 | 0.095 | 44.1 | 0.856 | 0.561  |
|  9,383 | 2.57 | 0.150 | 2.824 | 0.125 | 44.4 | 0.840 | 0.532  |
|  9,387 | 2.58 | 0.100 | 2.746 | 0.105 | 47.6 | 0.830 | 0.584  |
|  9,398 | 2.62 | 0.090 | 2.772 | 0.090 | 45.4 | 0.835 | 0.569  |
|  9,406 | 2.66 | 0.090 | 2.816 | 0.075 | 44.5 | 0.832 | 0.544  |

Table 10.4c. Case Study 2: Mission Canyon Formation, Williston Basin, U.S.A.: Calculations for solution table. The symbol "v/v" indicates volume-for-volume decimal fraction.

|  Saturation and other calculations  |   |   |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  Depth feet | Rwa ohm-m | Ro ohm-m | Sw v/v decimal | Sxo v/v decimal | MHI v/v decimal | MOS v/v decimal | ROS v/v decimal | BVW  |
|  9,310 | 0.751 | 0.8 | 0.166 | 0.700 | 0.237 | 0.534 | 0.300 | 0.028  |
|  9,322 | 0.029 | 14.4 | 0.894 | 1.000 | 0.894 | 0.106 | 0.000 | 0.036  |
|  9,326 | 0.096 | 4.1 | 0.490 | 0.892 | 0.550 | 0.401 | 0.108 | 0.037  |
|  9,332 | 0.081 | 2.5 | 0.532 | 0.886 | 0.601 | 0.354 | 0.114 | 0.051  |
|  9,335 | 0.097 | 7.6 | 0.487 | 0.657 | 0.741 | 0.170 | 0.343 | 0.027  |
|  9,347 | 0.123 | 0.9 | 0.433 | 0.911 | 0.475 | 0.478 | 0.089 | 0.069  |
|  9,353 | 0.092 | 1.2 | 0.500 | 0.736 | 0.679 | 0.237 | 0.264 | 0.070  |
|  9,362 | 0.169 | 5.4 | 0.369 | 0.605 | 0.610 | 0.236 | 0.395 | 0.024  |
|  9,367 | 0.079 | 6.4 | 0.539 | 0.733 | 0.736 | 0.194 | 0.267 | 0.032  |
|  9,373 | 0.079 | 3.2 | 0.538 | 0.820 | 0.656 | 0.282 | 0.180 | 0.046  |
|  9,376 | 0.073 | 1.6 | 0.560 | 0.750 | 0.746 | 0.190 | 0.250 | 0.067  |
|  9,383 | 0.074 | 1.0 | 0.557 | 0.793 | 0.701 | 0.237 | 0.207 | 0.083  |
|  9,387 | 0.033 | 2.3 | 0.835 | 1.000 | 0.835 | 0.165 | 0.000 | 0.083  |
|  9,398 | 0.052 | 2.8 | 0.666 | 0.977 | 0.682 | 0.311 | 0.023 | 0.060  |
|  9,406 | 0.041 | 2.8 | 0.746 | 0.977 | 0.764 | 0.231 | 0.023 | 0.067  |
<!-- page 202 -->
Log Interpretation Case Studies

191


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
This is a crossplot of Bulk Density (RHOB) versus Neutron Porosity (NPHI), commonly used in petrophysical interpretation to estimate lithology and porosity.

- **X-axis**: Neutron Porosity, NPHI — linear scale, range 0.00 to 0.30 (dimensionless, typically in fraction or %).
- **Y-axis**: Bulk Density, RHOB — linear scale, range 2.40 to 3.00 g/cm³ (or kg/m³, but units are standard as g/cm³ in logging).

The plot contains three labeled lithology trend lines:
- **Limestone**: a straight diagonal line from (NPHI=0.00, RHOB=2.60) to (NPHI=0.30, RHOB=2.40), with porosity labels 0, 5, 10, 15, 20 along the line.
- **Sandstone**: a straight diagonal line from (NPHI=0.00, RHOB=2.60) to (NPHI=0.30, RHOB=2.40), with porosity labels 0, 5, 10, 15, 20 along the line. This line is parallel to the limestone line and appears to be identical in slope and intercept — likely a mislabel or duplication in the figure.
- **Dolomite**: a curved line starting at (NPHI=0.00, RHOB=2.70) and curving downward to (NPHI=0.30, RHOB=2.40), with porosity labels 0, 5, 10, 15, 20 along the curve.

Data points are plotted as:
- Solid black squares (■) — likely representing one set of measurements (e.g., from a specific well or zone).
- Open squares (□) — likely representing another set of measurements (e.g., different well or zone).

The data points cluster primarily between the limestone and dolomite trends, with a concentration near the 10–15% porosity range on the limestone line. Some points lie above the limestone line (lower NPHI, higher RHOB), suggesting possible dolomite or anhydrite content, or shale effects. Points below the limestone line (higher NPHI, lower RHOB) may indicate gas or low-density minerals.

> Тренд: Плотность и нейтронная пористость коррелируют отрицательно; точки группируются вдоль линий лимонита и доломита, с некоторыми отклонениями, указывающими на глинистость, газ или другие минералы.

KEYWORDS: RHOB, NPHI, crossplot, lithology, porosity, limestone, sandstone, dolomite, petrophysics, well log interpretation
----


Figure 10.10. Mission Canyon Formation, Williston Basin, U.S.A.: Crossplot, bulk density (RHOB) versus neutron porosity (NPHI), for determining apparent matrix density (RtOmoa), a variable for the matrix identification plot (Figure 10.12). See Chapter 4 for detailed information about interpretation of the crossplot.

- Upper MC
Lower MC


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
- Vertical axis: Acoustic Travel Time, DT, range 40–80 μs/ft, linear scale.
- Horizontal axis: Porosity, φ, range 0.00–0.30, linear scale.
- Three curved lines (envelopes) are drawn, each labelled with a rock type and a value (5, 10, 15, 20):
  · Leftmost curve: sandstone, with labels 5, 10, 15, 20 along the curve.
  · Middle curve: limestone, with labels 10, 15, 20 along the curve.
  · Rightmost curve: dolomite, with labels 15, 20 along the curve.
- Data points are plotted as:
  · Solid black circles (•) — 50+ points, mostly clustered between φ = 0.10 and 0.25, DT = 50–65.
  · Open squares (□) — 10+ points, mostly in the same region, with a few extending to φ = 0.25–0.30, DT = 55–65.
  · Open circles (○) — 5+ points, mostly near φ = 0.10–0.15, DT = 50–55.
- The curves represent theoretical or empirical relationships between porosity and acoustic travel time for the respective rock types, with the numbers likely indicating porosity values (e.g., at φ=0.10, sandstone curve has DT≈55, limestone≈58, dolomite≈60).
- The data points lie within the region bounded by the sandstone and dolomite curves, with most falling closer to the limestone curve.
> Тренд: С увеличением пористости (φ) акустическое время прохождения (DT) возрастает; данные для различных пород (песчаник, известняк, доломит) образуют разные тренды, с песчаником имеющим наименьшее DT при данной пористости, а доломитом — наибольшее.
KEYWORDS: акустическое время прохождения, пористость, песчаник, известняк, доломит, кривые зависимости, петрофизика, интерпретация ГИС, DT, φ


Neutron Porosity, NPHI

Figure 10.11. Mission Canyon Formation, Williston Basin, U.S.A.: Crossplot, interval transit time (DT) versus neutron porosity (NPHI), for determining apparent matrix transit time (DTmoa), a variable for the matrix identification plot (Figure 10.12). See Chapter 4 for detailed information about interpretation of the crossplot.

- Upper MC
Lower MC
<!-- page 203 -->
192

ASQUITH AND KRYGOWSKI

Figure 10.12. Matrix identification plot, Mission Canyon Formation, Williston Basin, U.S.A.: Values for apparent matrix density (RHOmaa) and apparent matrix traveltime (DTmaa) were recorded from Figure 10.10 and Figure 10.11. Two mineral triangles are shown: quartz-calcite-dolomite, and calcite-dolomite-anhydrite. Scatter of points in the plot suggests that most of the rock is a mixture of calcite and dolomite.


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
- X-axis: Apparent Matrix Traveltime, DTmaa, linear scale, range 40 to 55 (units: μs/ft, implied by context).
- Y-axis: Apparent Matrix Density, RHOMaa, linear scale, range 2.60 to 3.00 (units: g/cm³, implied by context).
- Plot type: scatter plot with data points (black squares) and a triangular ternary diagram overlay connecting three end-member minerals.
- End-member points:
  - Calcite: at approximately (45.5, 2.70)
  - Dolomite: at approximately (43.0, 2.85)
  - Anhydrite: at approximately (50.0, 2.95)
  - Quartz: at approximately (48.0, 2.65) — connected to Calcite and Anhydrite to form a quadrilateral, but the main ternary triangle is Dolomite–Calcite–Anhydrite.
- Data points: scattered cluster primarily between Dolomite and Calcite, with a few extending toward Anhydrite and Quartz.
- The data points lie within the Dolomite–Calcite–Anhydrite triangle, suggesting a mixture of these minerals.
- No regression lines, equations, or R² values are printed.
- No specific data point labels or curve annotations are present.
> Тренд: Данные распределены в области, ограниченной точками Dolomite, Calcite и Anhydrite, что указывает на матрицу, состоящую из смеси этих минералов; точка Quartz лежит вне основного треугольника, но соединена с Calcite и Anhydrite, возможно, для расширения диапазона.

KEYWORDS: apparent matrix density, apparent matrix traveltime, ternary diagram, calcite, dolomite, anhydrite, quartz, scatter plot, well logging, petrophysics
----


- Upper MC
- Lower MC

Figure 10.13. M-N lithology crossplot for identification of matrix and secondary porosity, Mission Canyon Formation, Williston Basin, U.S.A. Lithology indicators were calculated from porosity logs: M from acoustic and density, and N from neutron and density. Two mineral triangles are shown: quartz-calcite-dolomite, and calcite-dolomite-anhydrite. Most points indicate a mixture of calcite and dolomite.


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
Cartesian scatter plot with two lithology indicators on axes.

X-axis: Lithology indicator, N, linear scale, range 0.40 to 0.70.
Y-axis: Lithology indicator, M, linear scale, range 0.70 to 0.95.

Data points:
- Approximately 100 black circular data points scattered across the plot.
- Points cluster primarily between N = 0.50 and 0.60, M = 0.80 and 0.88.
- A few points extend to N = 0.45–0.48, M = 0.75–0.80.

Classification field boundaries (polygonal regions):
- A triangle defined by three vertices:
  - Vertex 1: near (N=0.50, M=0.80), labelled "Dolomite"
  - Vertex 2: near (N=0.60, M=0.85), labelled "Calcite"
  - Vertex 3: near (N=0.55, M=0.72), labelled "Anhydrite"
- A fourth point at (N=0.65, M=0.85) labelled "Quartz", connected by a line to the "Calcite" vertex, suggesting an extension or adjacent field.

The data points are distributed across the fields, with:
- Most points falling within or near the triangle defined by Dolomite, Calcite, and Anhydrite.
- A few points lie outside this triangle, particularly towards the Quartz region.

> Тренд: Data points cluster in the central region of the plot, indicating a mixture of carbonate and evaporite lithologies; the classification fields suggest a ternary-like lithology discrimination based on indicators N and M.

KEYWORDS: lithology indicator, scatter plot, carbonate, anhydrite, dolomite, calcite, quartz, classification field, petrophysical analysis, rock typing
----


- Upper MC
- Lower MC
<!-- page 204 -->
Log Interpretation Case Studies

193


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth range: 9300–9400 ft, depth increases downward.

Tracks (left to right):

1. GR (gamma ray): scale 0–100 API, units API, solid line.
2. RHObas (bulk density): scale 2–3 g/cm³, units g/cm³, solid line.
3. LLD (deep resistivity): scale 0.1–1000 ohm·m, units ohm·m, solid line.
4. Rwa (water resistivity): scale 0.1–1000 ohm·m, units ohm·m, dashed line.
5. PHE (photoelectric factor): scale 0.1–0.4, units "ar. decimal", solid line.
6. NPHI (neutron porosity): scale 0.1–0.4, units "ar. decimal", solid line.
7. DPHI (density porosity): scale 0.1–0.4, units "ar. decimal", dashed line.

Interval table:

| Интервал, м | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|-------------|--------------------------|-------------------|-------------------------------|
| 9300–9400   | Не определена            | GR: колебания в пределах 40–80 API; RHObas: 2.5–2.7 g/cm³; LLD: 10–100 ohm·m; Rwa: 10–100 ohm·m; PHE: 0.2–0.3; NPHI: 0.2–0.3; DPHI: 0.2–0.3 | Нет подписанных интерпретаций |

No results panel (Кп, Кн, Кпр, эфф. толщина) is present.

KEYWORDS: well log, gamma ray, bulk density, resistivity, neutron porosity, density porosity, photoelectric factor, depth scale, feet, API, ohm·m, g/cm³, ar. decimal
----


Figure 10.14. Mission Canyon Formation, Williston Basin, U.S.A.: Log of apparent water resistivity (Rwa) with gamma ray log, apparent matrix density log (RHOmaa), deep resistivity laterolog, neutron-porosity log, density-porosity log, and effective porosity log.

Apparent matrix density (RHOmaa) is plotted in track 1 with the gamma ray (GR). Apparent water resistivity (Rwa) is plotted in track 2 with the deep laterolog. Neutron-density crossplot porosity, indicated by PHIE (effective porosity) is plotted in track 3, with the original neutron and density porosities.


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
- X-axis: Deep Resistivity, LLD, logarithmic scale, range 0.10 to 100 (unit not specified, assumed ohm·m).
- Y-axis: Effective porosity, PHIE, logarithmic scale, range 0.01 to 1.00 (unit: fraction, no % symbol).
- Grid: logarithmic grid with major ticks every decade and minor ticks at 0.2, 0.5, 2, 5.
- Data points: two sets — solid black circles (●) and open circles (○), scattered across the plot.
- Reference lines: five diagonal lines of constant water saturation (Sw), labelled 0.25, 0.50, 0.75, 1.0, and 1.0 (the last two are nearly coincident). These lines are straight on the log-log plot, indicating a power-law relationship between resistivity and porosity for fixed Sw.
- The lines are interpreted as Archie’s equation curves: $ R = \frac{a \cdot R_w}{\phi^m \cdot S_w^n} $, where $ R $ is resistivity, $ \phi $ is porosity, $ S_w $ is water saturation, and $ a, m, n $ are constants.
- The data points cluster primarily between the Sw = 0.50 and Sw = 0.75 lines, with a few extending to Sw = 0.25 and Sw = 1.0.
- The solid black circles are more numerous and appear to represent the main population; the open circles are fewer and scattered similarly.
- No regression equation or R² is printed.
- The plot demonstrates the use of deep resistivity and effective porosity to estimate water saturation in a reservoir using the Archie model.

> Тренд: С увеличением эффективной пористости (PHIE) и уменьшением глубокой сопротивляемости (LLD) водонасыщенность (Sw) возрастает, что соответствует стандартной интерпретации по методу Арчи.

KEYWORDS: Archie equation, water saturation, effective porosity, deep resistivity, log-log plot, Sw, PHIE, LLD, reservoir interpretation, petrophysics
----


Figure 10.15. Mission Canyon Formation, Williston Basin, U.S.A.: Pickett crossplot of deep laterolog resistivity vs. neutron-density crossplot porosity. Note that the "Lower MC" zones generally have the higher water saturations; they define the water-bearing line ($Sw = 1.0$). See Chapter 7 for detailed information about interpretation of the Pickett crossplot.

Upper MC
Lower MC
<!-- page 205 -->
194

ASQUITH AND KRYGOWSKI

Figure 10.16. Bulk-volume-water crossplot (effective porosity, PHIE, vs. water saturation, $S_{\mathrm{w}}$), Mission Canyon Formation, Williston Basin, U.S.A.


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
- Vertical axis: Water saturation, Sw, linear scale, range 0.00 to 1.00.
- Horizontal axis: Porosity, PHE, linear scale, range 0.00 to 0.30.
- Data points:
  - Solid black circles: Upper MC.
  - Open squares: Lower MC.
- Fitted curve: Black solid line, labelled "BVV = 0.035", representing the water saturation trend as a function of porosity.
- The curve shows a decreasing trend in water saturation with increasing porosity, starting near Sw=1.0 at low porosity and approaching Sw=0.2 at porosity ~0.20.
- Anchor points on the curve (read from grid, approximately):
  - Porosity 0.05 → Sw ≈ 0.75
  - Porosity 0.10 → Sw ≈ 0.50
  - Porosity 0.15 → Sw ≈ 0.30
  - Porosity 0.20 → Sw ≈ 0.20
- The data points are scattered around the curve, with Upper MC points generally below the curve and Lower MC points generally above it.
> Тренд: Водонасыщенность уменьшается с ростом пористости по экспоненциальному типу, описываемому кривой BVV = 0.035.
KEYWORDS: водонасыщенность, пористость, BVV, кривая насыщения, корреляция, петрофизика, Sw, PHE, Upper MC, Lower MC
----


Figure 10.17. Mission Canyon Formation, Williston Basin, U.S.A. Final results in log format.

Apparent water resistivity ($R_{\mathrm{ws}}$) is plotted in track 1 with the gamma ray log.

Resistivity of rock at 100% water saturation (Ro) is plotted in track 2, with the deep laterolog. Separation of the two curves (shaded) indicates hydrocarbons in the rock.

Track 3 shows water saturation (Sw), effective porosity (PHIE), and bulk volume water (BVW). The dark shaded area between the porosity curve (left-hand) and the bulk-volume-water curve indicates the proportion of pore space that is occupied by hydrocarbons, whereas the light shaded area between the bulk-volume-water curve and the right margin of the track (scale value of zero) indicates the proportion that is occupied by water. DiffCal is the differential caliper (caliper minus bit size). Negative values indicate the presence of mudcake.


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Глубина увеличивается вниз. Диапазон глубин: от 0 до 100 м (по шкале на левой стороне, но числовые метки отсутствуют — только сетка). Шкала глубины: 10 м на 10 клеток (предположительно, 1 клетка = 1 м).

Треки слева направо:
1. GR (Гамма-каротаж): шкала 0–100 API, линейная. Кривая: волнообразная, с пиками и впадинами. Видны отбивки на глубинах, где кривая резко меняется (например, на глубине ~20 м, ~40 м, ~60 м, ~80 м — по сетке). Поведение: в интервалах с высокими значениями GR — вероятно, глинистые породы; в интервалах с низкими значениями — песчаники или известняки.
2. Ров (Плотность породы): шкала 0–0,1 г/см³ (или 0–1000 кг/м³, но по подписи — 0–0,1). Кривая: волнообразная, с плавными изменениями. В интервалах с низкими значениями — вероятно, пористые песчаники; с высокими — плотные глины или карбонаты.

Интервалы и поведение кривых:
| Интервал, м | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|-------------|------------------------|-------------------|------------------------------|
| 0–20        | —                      | GR: высокие значения, Ров: средние | Вероятно, глинистые породы |
| 20–40       | —                      | GR: низкие значения, Ров: низкие | Вероятно, пористый песчаник |
| 40–60       | —                      | GR: высокие значения, Ров: высокие | Вероятно, плотные глины |
| 60–80       | —                      | GR: низкие значения, Ров: низкие | Вероятно, пористый песчаник |
| 80–100      | —                      | GR: высокие значения, Ров: средние | Вероятно, глинистые породы |

На кривой Ров видны пунктирные линии, возможно, это интерпретационные границы или кривая с учетом коррекции.

KEYWORDS: гамма-каротаж, плотность породы, каротажная диаграмма, интервал, литология, пористость, глинистость, кривая, глубина, интерпретация


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Глубина: 9300–9400 футов, MD (Measured Depth), увеличивается вниз.
Треки слева направо:
1. ПС (Потенциал Спонтанного): шкала 0–1000 мВ, линейная, кривая — черная сплошная.
2. ГК (Гамма-каротаж): шкала 0–100 API, линейная, кривая — черная сплошная.
3. НГК (Нейтрон-Гамма-Каротаж): шкала 0–20 %, линейная, кривая — черная сплошная.
4. ННК-Т (Нейтрон-Нейтрон-Каротаж, тепловые нейтроны): шкала 0–20 %, линейная, кривая — черная сплошная.
5. ГГК-П (Гамма-Гамма-Каротаж, плотность): шкала 0–20 г/см³, линейная, кривая — черная сплошная.
6. АК (Акустический каротаж): шкала 0–20 мкс/фут, линейная, кривая — черная сплошная.
7. КС (Каверномер): шкала 0–20 дюймов, линейная, кривая — черная сплошная.
8. БК (Боковой каротаж): шкала 0–20 Ом·м, логарифмическая, кривая — черная сплошная.
9. ИК (Индукционный каротаж): шкала 0–20 Ом·м, логарифмическая, кривая — черная сплошная.
10. БКЗ (Боковой каротаж, зональный): шкала 0–20 Ом·м, логарифмическая, кривая — черная сплошная.
11. МКЗ (Микрокаротаж, зональный): шкала 0–20 Ом·м, логарифмическая, кривая — черная сплошная.
12. МБК (Микробоковой каротаж): шкала 0–20 Ом·м, логарифмическая, кривая — черная сплошная.
13. ДС (Дифференциальный спонтанно-потенциал): шкала 0–20 мВ, линейная, кривая — черная сплошная.
14. Резистивиметрия (сопротивление): шкала 0–20 Ом·м, логарифмическая, кривая — черная сплошная.
15. SP (Spontaneous Potential): шкала 0–1000 мВ, линейная, кривая — черная сплошная.
16. GR (Gamma Ray): шкала 0–100 API, линейная, кривая — черная сплошная.
17. RHOB (Bulk Density): шкала 0–20 г/см³, линейная, кривая — черная сплошная.
18. NPHI (Neutron Porosity): шкала 0–20 %, линейная, кривая — черная сплошная.
19. DT (Transit Time): шкала 0–20 мкс/фут, линейная, кривая — черная сплошная.
20. ILD (Deep Resistivity): шкала 0–20 Ом·м, логарифмическая, кривая — черная сплошная.
21. CALI (Caliper): шкала 0–20 дюймов, линейная, кривая — черная сплошная.

Интервалы и поведение кривых:
| Интервал, фут | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|---------------|-------------------------|-------------------|-------------------------------|
| 9300–9310     | —                       | ПС: отрицательная аномалия; ГК: повышенные показания; НГК: повышенные показания; ННК-Т: повышенные показания; ГГК-П: пониженные показания; АК: повышенные показания; КС: увеличение; БК: пониженные показания; ИК: пониженные показания; БКЗ: пониженные показания; МКЗ: пониженные показания; МБК: пониженные показания; ДС: отрицательная аномалия; Резистивиметрия: пониженные показания; SP: отрицательная аномалия; GR: повышенные показания; RHOB: пониженные показания; NPHI: повышенные показания; DT: повышенные показания; ILD: пониженные показания; CALI: увеличение | — |
| 9310–9320     | —                       | ПС: положительная аномалия; ГК: пониженные показания; НГК: пониженные показания; ННК-Т: пониженные показания; ГГК-П: повышенные показания; АК: пониженные показания; КС: уменьшение; БК: повышенные показания; ИК: повышенные показания; БКЗ: повышенные показания; МКЗ: повышенные показания; МБК: повышенные показания; ДС: положительная аномалия; Резистивиметрия: повышенные показания; SP: положительная аномалия; GR: пониженные показания; RHOB: повышенные показания; NPHI: пониженные показания; DT: пониженные показания; ILD: повышенные показания; CALI: уменьшение | — |
| 9320–9330     | —                       | ПС: отрицательная аномалия; ГК: повышенные показания; НГК: повышенные показания; ННК-Т: повышенные показания; ГГК-П: пониженные показания; АК: повышенные показания; КС: увеличение; БК: пониженные показания; ИК: пониженные показания; БКЗ: пониженные показания; МКЗ: пониженные показания; МБК: пониженные показания; ДС: отрицательная аномалия; Резистивиметрия: пониженные показания; SP: отрицательная аномалия; GR: повышенные показания; RHOB: пониженные показания; NPHI: повышенные показания; DT: повышенные показания; ILD: пониженные показания; CALI: увеличение | — |
| 9330–9340     | —                       | ПС: положительная аномалия; ГК: пониженные показания; НГК: пониженные показания; ННК-Т: пониженные показания; ГГК-П: повышенные показания; АК: пониженные показания; КС: уменьшение; БК: повышенные показания; ИК: повышенные показания; БКЗ: повышенные показания; МКЗ: повышенные показания; МБК: повышенные показания; ДС: положительная аномалия; Резистивиметрия: повышенные показания; SP: положительная аномалия; GR: пониженные показания; RHOB: повышенные показания; NPHI: пониженные показания; DT: пониженные показания; ILD: повышенные показания; CALI: уменьшение | — |
| 9340–9350     | —                       | ПС: отрицательная аномалия; ГК: повышенные показания; НГК: повышенные показания; ННК-Т: повышенные показания; ГГК-П: пониженные показания; АК: повышенные показания; КС: увеличение; БК: пониженные показания; ИК: пониженные показания; БКЗ: пониженные показания; МКЗ: пониженные показания; МБК: пониженные показания; ДС: отрицательная аномалия; Резистивиметрия: пониженные показания; SP: отрицательная аномалия; GR: повышенные показания; RHOB: пониженные показания; NPHI: повышенные показания; DT: повышенные показания; ILD: пониженные показания; CALI: увеличение | — |
| 9350–9360     | —                       | ПС: положительная аномалия; ГК: пониженные показания; НГК: пониженные показания; ННК-Т: пониженные показания; ГГК-П: повышенные показания; АК: пониженные показания; КС: уменьшение; БК: повышенные показания; ИК: повышенные показания; БКЗ: повышенные показания; МКЗ: повышенные показания; МБК: повышенные показания; ДС: положительная аномалия; Резистивиметрия: повышенные показания; SP: положительная аномалия; GR: пониженные показания; RHOB: повышенные показания; NPHI: пониженные показания; DT: пониженные показания; ILD: повышенные показания; CALI: уменьшение | — |
| 9360–9370     | —                       | ПС: отрицательная аномалия; ГК: повышенные показания; НГК: повышенные показания; ННК-Т: повышенные показания; ГГК-П: пониженные показания; АК: повышенные показания; КС: увеличение; БК: пониженные показания; ИК: пониженные показания; БКЗ: пониженные показания; МКЗ: пониженные показания; МБК: пониженные показания; ДС: отрицательная аномалия; Резистивиметрия: пониженные показания; SP: отрицательная аномалия; GR: повышенные показания; RHOB: пониженные показания; NPHI: повышенные показания; DT: повышенные показания; ILD: пониженные показания; CALI: увеличение | — |
| 9370–9380     | —                       | ПС: положительная аномалия; ГК: пониженные показания; НГК: пониженные показания; ННК-Т: пониженные показания; ГГК-П: повышенные показания; АК: пониженные показания; КС: уменьшение; БК: повышенные показания; ИК: повышенные показания; БКЗ: повышенные показания; МКЗ: повышенные показания; МБК: повышенные показания; ДС: положительная аномалия; Резистивиметрия: повышенные показания; SP: положительная аномалия; GR: пониженные показания; RHOB: повышенные показания; NPHI: пониженные показания; DT: пониженные показания; ILD: повышенные показания; CALI: уменьшение | — |
| 9380–9390     | —                       | ПС: отрицательная аномалия; ГК: повышенные показания; НГК: повышенные показания; ННК-Т: повышенные показания; ГГК-П: пониженные показания; АК: повышенные показания; КС: увеличение; БК: пониженные показания; ИК: пониженные показания; БКЗ: пониженные показания; МКЗ: пониженные показания; МБК: пониженные показания; ДС: отрицательная аномалия; Резистивиметрия: пониженные показания; SP: отрицательная аномалия; GR: повышенные показания; RHOB: пониженные показания; NPHI: повышенные показания; DT: повышенные показания; ILD: пониженные показания; CALI: увеличение | — |
| 9390–9400     | —                       | ПС: положительная аномалия; ГК: пониженные показания; НГК: пониженные показания; ННК-Т: пониженные показания; ГГК-П: повышенные показания; АК: пониженные показания; КС: уменьшение; БК: повышенные показания; ИК: повышенные показания; БКЗ: повышенные показания; МКЗ: повышенные показания; МБК: повышенные показания; ДС: положительная аномалия; Резистивиметрия: повышенные показания; SP: положительная аномалия; GR: пониженные показания; RHOB: повышенные показания; NPHI: пониженные показания; DT: пониженные показания; ILD: повышенные показания; CALI: уменьшение | — |

Результаты интерпретации:
- Кп (пористость): не указано.
- Кн (насыщенность нефтью): не указано.
- Кпр (насыщенность водой): не указано.
- Эффективная толщина: не указано.

KEYWORDS: well log, logging, wireline, resistivity, density, neutron, gamma ray, spontaneous potential, caliper, porosity, saturation, depth, feet, MD, interpretation, curve behavior, lithology, formation evaluation
----


<!-- page 206 -->
Log Interpretation Case Studies 195

### Case Study 3:

# **EOCENE WILCOX SANDSTONE, GULF COAST, U.S.A.:**

# *The Problem.*

Case Study 3 reflects the logging technology available when the well was drilled. At the time, logging tools could be combined in single tool strings in limited ways. The neutron and density tools could be combined, as could the induction and sonic tools. In the U.S. Gulf Coast, the induction-sonic log was the tool string of choice for the first entry in a well on any run, especially in difficult boreholes, because if no other logging data could be acquired, the acquisition of resistivity and porosity at the same time allowed a reasonable evaluation of the formation. Although current technology permits the simultaneous acquisition of more wireline data, the analysis in this exercise is a good example of the approach that can be used in older wells with this limited suite of data, or other similarly limited suites of data. Techniques shown here are very effective in looking for bypassed pay.

# **Background**

Assume that you are assigned to evaluate the logs of a lower Wilcox sandstone in South Texas. A fairly typical Gulf Coast log package was used to document the well. It consists of an induction electric log with an SP log, a sonic log, and an $R_{wa}$ quick-look curve. The induction electric log has a deep induction curve, IL, to measure resistivity in the uninvaded zone ($R_t$), and a short normal (SN) to measure resistivity in the invaded zone ($R_i$). The log package was run on a single tool string, and because it required only one run in the well, it saved your company rig time and money. The log is shown as Figure 10.18.

Drilling operations halted at 10,936 ft after penetration of a sandstone. Gas in the drilling mud increased suddenly and by a large amount: 3200 units over background on the chromatograph. In response to this, mud weight was increased from 14.8 lbs/gal to 15.4 lbs/gal, to confine the gas within the formation. When drilling operations were resumed, gas continued to cut the mud; mud weight was 15.4 lbs/gal going into the hole and 15.2 lbs/gal coming out. Also, the mud logger's chromatograph maintained about 100 units of gas, even when the well was deepened beyond the zone of initial gas show.

# **Well site information and other pertinent information:**

- $R_w = 0.022$ ohm-m at $T_f$ (from other sources)
- Archie parameters: a = 0.62; m = 2.15; n = 2.0
- $R_{mf} = 0.222$ ohm-m at $T_f$
- formation temperature, $T_f = 260^\circ\text{F}$
- $\Delta t_{sh} = 116$ $\mu$sec/ft
- surface temperature = 80$^\circ$F

Recoverable reserves of gas are to be calculated from the gas volumetric equation (Equation 10.11). The following parameters are needed:

- drainage area = 320 acres
- reservoir thickness (to be determined from the calculations)
- porosity (to be determined from the calculations)
- water saturation (to be determined from the calculations)
- recovery factor = 0.6
- bottom hole pressure (estimated) = 8,100 psi
- Z factor = 1.229
- surface pressure = 15 psi

Your company has purchased a 25% working interest (WI) in the well, which has a net revenue interest (NRI) of 82.5 percent. (Net revenue interest is the total interest of 100% minus royalties, such as an interest granted to a mineral-rights owner.)

Estimated cost of the well is $1,800,000. Use a product price of $1.90 per mcf to find the return your company can expect on its investment.

# **Useful equations**

The only porosity tool at your disposal is the sonic log, so porosity can be calculated either by the Wyllie time-average equation or the Raymer-Hunt-Gardner equation (see Chapter 4). Because of your knowledge of the geology of the area, you decide that the Wyllie time-average equation (Equation 4.3) will yield the better estimate of porosity:

$$PHIS = \left( \frac{\Delta t_{log} - \Delta t_{ma}}{\Delta t_{fl} - \Delta t_{ma}} \right) \times \frac{1}{Cp} \tag{10.26}$$

where:

$$Cp = \frac{\Delta t_{sh} \times C}{100}$$
<!-- page 207 -->
196

ASQUITH AND KRYGOWSKI

$\Delta t_{ma} = 55.5 \text{ \textmu sec/ft}$ for Wilcox sandstones in this province

$$
\Delta t_{fl} = 189 \text{ \textmu sec/ft}
$$

$$
\Delta t_{sh} = 116 \text{ \textmu sec/ft}
$$

$$
C = 1
$$

Because the sonic log is strongly affected by gas, correction of sonic porosity is necessary.

$$
\phi_{S \text{ gas corrected}} = 0.7 \times \phi_S \tag{10.27}
$$

## Tasks required for interpretation of the logs

Eleven depths (or points) within the Wilcox sandstone interval are selected, in the interval from 10,925 ft to 10,982 ft. Depths are picked on the basis of an approximately even distribution through the interval being evaluated.

Table 10.5 is designed to assist you with your work. Some of the log values have been recorded, to guide you in reading the log and completing the array of data.

As you approach this problem, think about the parameters and calculations necessary to determine porosity and water saturation. Also, consider some of the plots done in the first two case studies that may help you understand the formation better.
<!-- page 208 -->
Log Interpretation Case Studies

197

Table 10.5. Case Study 3: Eocene Wilcox sandstone, Gulf Coast, U.S.A.: Work table. Depths in italics indicate data from the lower part of the Wilcox, the "B" zone. The symbol "v/v" indicates volume-for-volume decimal fraction.

|  Parameters  |   |   |   |
| --- | --- | --- | --- |
|  Ann. Mean Surf. Temp: 80°F |   |   | Rw (measured): (not given)  |
|  Total Depth: 12,186 ft |   |   | Rw @ fm. temp.: 0.022 ohm-m @ 260°F  |
|  Bottom Hole Temp: 280°F |   |   | Rmf (measured): 0.77 ohm-m @ 70°F  |
|  Formation Depth: 10,950 ft |   |   | Rmf @ fm. temp.: 0.222 ohm-m @ 260°F  |
|  Formation Temperature: 260°F |   |   |   |
|  DT matrix (Wyllie): 55.5 μsec/ft |   |   | DT fluid (Wyllie): 189 μsec/ft  |
|  DT shale: 116 μsec/ft |   |   | Compaction Correction, Cp: 1.16  |
|   | a: 0.62 | m: 2.15 | n: 2  |

|  Data |  |  |  |  |   |
| --- | --- | --- | --- | --- | --- |
|  Depth feet | IL ohm-m | SN ohm-m | DT μsec/ft | PHIS v/v decimal | Phia v/v decimal  |
|  10,925 | 1.8 | 3.1 | 88 | 0.210 | 0.147  |
|  10,930 |  |  |  |  |   |
|  10,935 |  |  |  |  |   |
|  10,942 |  |  |  |  |   |
|  10,947 | 2.3 | 4.0 | 91 | 0.229 | 0.160  |
|  10,954 |  |  |  |  |   |
|  10,960 |  |  |  |  |   |
|  10,966 | 1.0 | 2.5 | 96 | 0.262 | 0.183  |
|  10,970 | 0.8 | 2.5 | 95 | 0.255 | 0.179  |
|  10,974 |  |  |  |  |   |
|  10,978 |  |  |  |  |   |

|  Calculations  |   |   |   |   |
| --- | --- | --- | --- | --- |
|  Depth feet | Rwa ohm-m | Swa v/v decimal | Sxo v/v decimal | BVW  |
|  10,925 | 0.047 | 0.684 | >1.0 | 0.101  |
|  10,930 |  |  |  |   |
|  10,935 |  |  |  |   |
|  10,942 |  |  |  |   |
|  10,947 | 0.073 | 0.550 | >1.0 | 0.088  |
|  10,954 |  |  |  |   |
|  10,960 |  |  |  |   |
|  10,966 | 0.042 | 0.725 | >1.0 | 0.133  |
|  10,970 | 0.032 | 0.832 | >1.0 | 0.149  |
|  10,974 |  |  |  |   |
|  10,978 |  |  |  |   |
<!-- page 209 -->
198

ASQUITH AND KRYGOWSKI


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Глубина увеличивается вниз. Диапазон глубин: 10900–11000 футов (MD — measured depth).

Треки слева направо:

1. Трек 1 (левый):
   - Кривая: Rwa (сопротивление, вероятно, в омах, но единицы не указаны)
     - Масштаб: 0–30 (левая шкала), 0–20 (правая шкала)
     - Линия: толстая сплошная
   - Кривая: SP (спонтанный потенциал)
     - Масштаб: 0–0,1 (в единицах, вероятно, мВ)
     - Линия: пунктирная

2. Трек 2 (центральный):
   - Кривая: IL (индукционное сопротивление, вероятно, в омах·м)
     - Масштаб: 0,2–20 (левая шкала), 0,2–20 (правая шкала)
     - Линия: толстая сплошная
   - Кривая: SN (вероятно, сопротивление нейтронное или нормализованная кривая)
     - Масштаб: 0,2–20 (левая шкала), 0,2–20 (правая шкала)
     - Линия: пунктирная

3. Трек 3 (правый):
   - Кривая: DT (время прохождения, в мкс/фут)
     - Масштаб: 150–50
     - Линия: толстая сплошная

Интервалы и поведение кривых:

| Интервал, фут | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|---------------|------------------------|-------------------|-------------------------------|
| 10900–10920   | Не определена          | Rwa: резкое падение; SP: отрицательная аномалия; IL: резкое падение; SN: резкое падение; DT: резкое падение | Вероятно, песчаник, высокая пористость, водонасыщенность |
| 10920–10940   | Не определена          | Rwa: резкое увеличение; SP: положительная аномалия; IL: резкое увеличение; SN: резкое увеличение; DT: резкое увеличение | Вероятно, глина или аргиллит |
| 10940–10960   | Не определена          | Rwa: падение; SP: отрицательная аномалия; IL: падение; SN: падение; DT: падение | Вероятно, песчаник, высокая пористость |
| 10960–10980   | Не определена          | Rwa: увеличение; SP: положительная аномалия; IL: увеличение; SN: увеличение; DT: увеличение | Вероятно, глина |
| 10980–11000   | Не определена          | Rwa: падение; SP: отрицательная аномалия; IL: падение; SN: падение; DT: падение | Вероятно, песчаник, высокая пористость |

Результаты петрофизической интерпретации не представлены в данном фрагменте.

KEYWORDS: каротаж, Rwa, SP, IL, SN, DT, сопротивление, спонтанное потенциал, индукционный каротаж, нейтронный каротаж, время прохождения, глубина, фут, MD, интерпретация, песчаник, глина
----


Figure 10.18. Induction electric fog with SP lag, sonic lag, and Rwa curve, Wilcox sandstone, Gulf Coast, U.S.A.

Note:

(1) In the upper part of the Wilcox (10,923 to 10,958 ft), deflection of the Rwa quick-look curve (track 1) to the right, opposite general deflection of the SP curve. The deflection indicates the presence of oil or gas. Based on the mudlogger's report, gas is present.
(2) In track 2, increase of resistivity in the upper part of the Wilcox (10,923 to 10,958 ft). Increase of resistivity also indicates the presence of gas.
(3) In the lower part of the Wilcox (10,958 to 10,982 ft), low resistivities and deflection of the Rwa curve to the left indicate a probable water-bearing zone.
<!-- page 210 -->
Log Interpretation Case Studies 199

### Case Study 3:

# **EOCENE WILCOX SANDSTONE, GULF COAST, U.S.A.:**

# *The Solution.*

Evaluation of the logs (Figure 10.18) begins with assessment of the quality of sandstone through the Wilcox interval, because this is where a good gas show was recorded. You discern the following attributes of the formation:

- Porous and permeable sandstone is documented by the SP curve from 10,923 to 10,982 ft, evident by leftward deflection of the curve from the shale baseline.
- Porosity of sandstone over that interval is almost uniform, as shown by small variation of the sonic (DT) curve.
- In the upper part of the Wilcox (10,923 to 10,958 ft), the $R_{wa}$ quick-look curve is deflected rightward from the SP curve. Such a deflection is evidence of hydrocarbons in the sandstone—in this case, gas.
- In the same interval, induction log (IL) resistivity increases, indicating that the sandstone contains hydrocarbons.
- Fairly abrupt decrease of resistivity into the lower zone (10,958 to 10,982 ft) and leftward deflection of the $R_{wa}$ curve means higher water saturation. These observations alert you that the lower zone may be water productive.

In order to establish whether the lower Wilcox zone would produce water, you decide that a rather detailed log evaluation is necessary. The evaluation will include use of the $R_{wa}$ quick-look curve, a Pickett crossplot (to verify the value of $R_w$ estimated from $R_{wa}$, and to estimate water saturations), water saturations calculated from the Archie equation, and a crossplot for estimation of bulk volume water. The following calculations will be needed:

- Gas-corrected sonic porosity, from Equations 10.26 and 10.27, for use in the Pickett plot, and for calculation of $S_w$ and $S_{xo}$ by the Archie equation.
- $S_w$, and $S_{xo}$, to calculate moveable oil saturation (MOS), bulk volume water (BVW), and the moveable hydrocarbon index (MHI).

Note that the short normal resistivity (SN) will be used to calculate $S_{xo}$. The short normal curve actually measures resistivity of the invaded zone ($R_i$), and in the strictest sense, water saturation calculated from

that measurement would be $S_i$, the invaded-zone saturation, not $S_{xo}$, the flushed-zone saturation. Because there is no $R_{xo}$ measurement available, the short normal is used as an approximate $R_{xo}$ measurement; the resulting estimate of “$S_{xo}$” is somewhat lower than $S_{xo}$ based on an actual $R_{xo}$ measurement. However, the approximation usually is sufficient for analyses like the one dealt with here.

Results of calculations are shown in Table 10.6. In the various plots, the lower Wilcox was divided into two zones: the “lower Wilcox A,” from 10,923 to 10,958 ft, and the “lower Wilcox B,” from 10,958 to 10,982 ft. In the table, depths in italics denote points in the “lower Wilcox B” zone.

Examination of the gas-corrected sonic-log porosity (Table 10.6, *Phia*, apparent porosity) reveals that porosity ranges from almost 0.15 to approximately 0.20 (15% to 20%), with average porosity of 0.18. These sonic porosities are used in the $R_{wa}$ calculation, the Archie water saturation equation, and in making crossplots.

The apparent water resistivity curve, $R_{wa}$ (Figure 10.18), can be used in a quick-look technique for comparison with the SP. It can also be used to determine formation water resistivity, $R_w$. From study of Chapter 7, you will remember that the minimal value of $R_{wa}$ in an interval can be considered as the “best estimate” of $R_w$. In the Wilcox in this well, the minimal value of $R_{wa}$, from 10,970 to 10,980 ft, is 0.028 ohm-m (Table 10.6). From independent evidence, $R_w$ of the Wilcox in this province is known to be 0.022 ohm-m; therefore, the log-derived value indicates that hydrocarbons probably are in the interval, although not as much as are in the overlying part of the Wilcox.

A Pickett crossplot (Figure 10.19; see also Chapter 7) of deep-induction log resistivities (IL) versus corrected sonic porosity (*Phia*) (i.e., porosity corrected for gas effect) shows a water-saturated sandstone line constructed with an $R_w$ of 0.022 ohm-m. Water saturations range from about 90% to less than 50%. Water saturations greater than 75% are from samples of the lower Wilcox B zone. This supports your suspicions about the potential for water production from the lower Wilcox B.

Compare bulk volume water and water saturations of the upper part, “A,” and lower part, “B,” of the Wilcox sandstone (Figure 10.20). The lower bulk-volume-water values and lower water saturations of the Wilcox A indicate that only the Wilcox A is above a gas/water transition zone. Most of the bulk-volume-water values that are much greater than 0.1 (Figure 10.20) are in the Wilcox B, from 10,958 to 10,982 ft (Figure 10.18; Table 10.6). In this interval, the volume
<!-- page 211 -->
200

ASQUITH AND KRYGOWSKI

of pore water is greater than irreducible water saturation.

Values of $S_{xo}$ are needed to calculate the moveable hydrocarbon index, MHI, and moveable oil saturation, MOS. Unfortunately the $S_{xo}$ values calculated for all zones are greater than 1.0, making the MHI and MOS calculations of no value. There are two likely causes for the calculations' being greater than is physically possible. The first is an incorrectly measured or recorded value of $R_{mf}$. This is a rare occurrence, but given the nature of work on an active rig, it cannot be dismissed. For values of $S_{xo}$ to be around 1.0, the actual $R_{mf}$ value would be about half the recorded value. The second probable cause would be use of the short normal as an $R_{xo}$ measurement. If the formation were invaded, the short normal would read formation fluid resistivity that is a mix of $R_w$ and $R_{mf}$; in this case, the value would be greater than $R_w$ but less than $R_{mf}$. For the values of $S_{xo}$ to be around 1.0, short-normal resistivity measurements would necessarily be three times the recorded values. Given the information at hand, the cause for the unreasonable $S_{xo}$ calculations can't be determined with certainty.

All data produced by your evaluation support the early assessment of a reservoir with gas above water. You were alerted immediately to a potential problem after you examined the $R_{wa}$ quick-look curve and saw leftward deflection through the lower Wilcox zone, and also when you saw the fairly abrupt decrease of resistivity in the lower Wilcox.

By volumetric calculations (Equations 10.11 and 10.12) estimated recoverable reserves are 3.1 BCF, based on the following parameters:

- drainage area = 320 acres
- reservoir thickness = 15 ft
- porosity = 0.18 (18%)
- water saturation = 0.67 (67%)
- recovery factor = 0.6 (estimated conservatively)
- formation temperature (estimated) = 260°F
- bottom-hole pressure (estimated) = 8,100 psi
- Z factor = 1.229
- surface pressure = 15 psi

Return on investment of the Wilcox sandstone is estimated as follows:

1: Working-interest well cost
= Total well cost × Working interest.
10.28
Working-interest well cost
= $1,800,000 × 0.25 = $450,000.

2: Net-revenue working interest
= Net-revenue interest (lease)
× Working interest.
10.29
Working interest = 0.825 × 0.25
= 0.20625 (20.6%).

3: Gross revenue = Reserves × Product price.
10.30

Gross revenue = 3,100,000 mcf ×
$1.90 / mcf = $5,890,000.

4: Net-revenue (working interest) = Gross revenue
× Net-revenue working interest.
10.31

Net-revenue (working interest) =
= $5,890,000 × 0.20625 = $1,205,812.50

5: Return on investment (before taxes and expenses)

= Net revenue (working interest)
Working-interest well costs.

10.32

Return on investment
= $1,214,812.50
$450,000
≅ 2.7 : 1.

The relatively poor return (2.7 to 1) on your company's investment is weighed with your judgment about the reservoir's high water saturations. The conclusion is that gas could be produced only at fairly low levels, so that production of water from the lower zone can be kept under control. However, in conjunction with your company's management, a decision is made to set pipe, because of hope for increase in gas prices. (This decision may be questioned by readers who conclude that the rate of return doesn't meet their economic criteria—even with the assumed price increases.)

The Wilcox sandstone was perforated from 10,962
<!-- page 212 -->
Log Interpretation Case Studies

201

to 10,963 ft. Gas flowed 11 hours on a 10/64-in. choke at 1584 mcfgpd, with 5 barrels of condensate per day (BCPD) and 1090 barrels of water per day (BWPD). The interval (10,962 to 10,963 ft) was squeezed (i.e., cemented off) and sandstone from 10,925 to 10,933 ft was perforated. Results were as follows:

- calculated absolute open flow (CAOF) of 7000 mcfgpd and 7.8 BC/mmcf,
- SITP = 7130 psi;
- IBHP = 8480 psi;

- BHT = 283°F;
- gas gravity = 0.657; and
- liquid gravity = 46.7 degAPI.

The well produced 350 mmcf during the first 10 months.

Figure 10.21 shows results of evaluation of the interval by petrophysical software. Parameters described in this case study were used and calculations were made at the sample intervals defined for recording of the original data—one sample every 0.5 ft.
<!-- page 213 -->
202

ASQUITH AND KRYGOWSKI

Table 10.6. Case Study 3: Eocene Wilcox sandstone, Gulf Coast U.S.A.: Solution table. Depths in italics indicate data from the lower part of the Wilcox, the "B" zone. The symbol "v/v" indicates volume-for-volume decimal fraction.

|  Parameters  |   |   |   |
| --- | --- | --- | --- |
|  Ann. Mean Surf. Temp: 80°F |   |   | Rw (measured): (not given)  |
|  Total Depth: 12,186 ft |   |   | Rw @ fm. temp.: 0.022 ohm-m @ 260°F  |
|  Bottom Hole Temp: 280°F |   |   | Rmf (measured): 0.77 ohm-m @ 70°F  |
|  Formation Depth: 10,950 ft |   |   | Rmf @ fm. temp.: 0.222 ohm-m @ 260°F  |
|  Formation Temperature: 260°F |   |   |   |
|  DT matrix (Wyllie): 55.5 μsec/ft |   |   | DT fluid (Wyllie): 189 μsec/ft  |
|  DT shale: 116 μsec/ft |   |   | Compaction Correction, Cp: 1.16  |
|   | a: 0.62 | m: 2.15 | n: 2  |

|  Data |  |  |  |  |   |
| --- | --- | --- | --- | --- | --- |
|  Depth feet | IL ohm-m | SN ohm-m | DT μsec/ft | PHIS v/v decimal | Phia v/v decimal  |
|  10,925 | 1.8 | 3.1 | 88 | 0.210 | 0.147  |
|  10,930 | 1.3 | 3.0 | 98 | 0.274 | 0.192  |
|  10,935 | 1.8 | 3.0 | 96 | 0.262 | 0.183  |
|  10,942 | 1.5 | 3.2 | 97 | 0.268 | 0.188  |
|  10,947 | 2.3 | 4.0 | 91 | 0.229 | 0.160  |
|  10,954 | 1.3 | 3.1 | 100 | 0.287 | 0.201  |
|  10,960 | 1.1 | 2.9 | 94 | 0.249 | 0.174  |
|  10,966 | 1.0 | 2.5 | 96 | 0.262 | 0.183  |
|  10,970 | 0.8 | 2.5 | 95 | 0.255 | 0.179  |
|  10,974 | 0.8 | 2.2 | 93 | 0.242 | 0.170  |
|  10,978 | 0.9 | 2.1 | 92 | 0.236 | 0.165  |

|  Calculations  |   |   |   |   |
| --- | --- | --- | --- | --- |
|  Depth feet | Rwa ohm-m | Swa v/v decimal | Sxo v/v decimal | BVW  |
|  10,925 | 0.047 | 0.684 | >1.0 | 0.101  |
|  10,930 | 0.060 | 0.603 | >1.0 | 0.116  |
|  10,935 | 0.075 | 0.540 | >1.0 | 0.099  |
|  10,942 | 0.066 | 0.576 | >1.0 | 0.108  |
|  10,947 | 0.073 | 0.550 | >1.0 | 0.088  |
|  10,954 | 0.067 | 0.574 | >1.0 | 0.116  |
|  10,960 | 0.041 | 0.730 | >1.0 | 0.127  |
|  10,966 | 0.042 | 0.725 | >1.0 | 0.133  |
|  10,970 | 0.032 | 0.832 | >1.0 | 0.149  |
|  10,974 | 0.029 | 0.864 | >1.0 | 0.146  |
|  10,978 | 0.030 | 0.854 | >1.0 | 0.141  |
<!-- page 214 -->
Log Interpretation Case Studies

203


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
- X-axis: Induction log, IL — логарифмическая шкала, диапазон 0.10–100 (единицы не указаны, предположительно мОм·м или мкСм/м).
- Y-axis: Gas-corrected sonic porosity, Pha — логарифмическая шкала, диапазон 0.01–1.00 (единицы — доля, безразмерная).
- Три кривые, соответствующие значениям водонасыщенности Sw = 50, 75, 100 — прямые линии, наклонённые вниз справа налево.
- Данные представлены двумя типами маркеров:
  - Чёрные кружки — Lower Wilcox A
  - Белые кружки с чёрной окантовкой — Lower Wilcox B
- Все точки данных расположены в области между кривыми Sw = 50 и Sw = 75, ближе к Sw = 75.
- Нет явных уравнений регрессии или R².
- Нет подписей к отдельным точкам.
- Тренд: с увеличением значения индукционного лога (IL) пористость Pha уменьшается; точки данных из двух интервалов (Lower Wilcox A и B) группируются вдоль кривой Sw ≈ 75, что указывает на высокую водонасыщенность в этих пластах.

KEYWORDS: индукционный лог, пористость, водонасыщенность, кривые Sw, логарифмическая шкала, Lower Wilcox, петрофизика, интерпретация ГИС, кроссплот, Pha, IL
----


Figure 10.19. Pickett crossplot of resistivity, IL, versus porosity from the sonic log, corrected for gas effect (Phia), Eocene Wilcox sandstone, Gulf Coast, U.S.A.

Saturation lines are placed on the basis of $R_{\mathrm{p}} = 0.022$ ohm-m at formation temperature; a widely accepted value for the Wilcox in this area.


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
- X-axis: Gas-corrected sonic porosity, Phi_a, linear scale, range 0.00 to 0.30.
- Y-axis: Archie water saturation, Swa, linear scale, range 0.00 to 1.00.
- Data points:
  - Solid black circles: Lower Wilcox A.
  - Open squares: Lower Wilcox B.
- A smooth curve is drawn on the plot, labelled "BVW = 0.10", representing a water saturation trend for a given bound water volume.
- The curve starts at approximately (Phi_a = 0.10, Swa = 0.90) and decreases to (Phi_a = 0.20, Swa = 0.40).
- Data points are clustered between Phi_a = 0.15 and 0.22, Swa = 0.40 to 0.85.
- The curve lies below the data points, indicating that the BVW = 0.10 model underestimates water saturation for the observed data.
> Тренд: С увеличением газокорректированной сейсмической пористости (Phi_a) арчиевская водонасыщенность (Swa) уменьшается по кривой BVW = 0.10; наблюдаемые данные (Lower Wilcox A и B) лежат выше этой кривой, что указывает на более высокую водонасыщенность, чем предсказывает модель.
KEYWORDS: Archie water saturation, gas-corrected sonic porosity, BVW, Lower Wilcox, crossplot, water saturation trend, porosity-saturation relationship, petrophysical model, Swa, Phi_a


Figure 10.20. Bulk volume water crossplot (apparent porosity, Phi vs. water saturation, $S_{\mathrm{wa}}$), Eocene Wilcox sandstone, Gulf Coast, U.S.A.

Bulk-volume-water values (BVW) plotted above the 0.1 hyperbolic line are from samples of the lower ("B") part of the Wilcox sandstone; in this part of the reservoir the volume of pore water is greater than irreducible water saturation.
<!-- page 215 -->
204

ASQUITH AND KRYGOWSKI


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: increases downward, from 10900 to 11000 feet (MD — measured depth).

Track 1 (leftmost):
- Curve: SP (spontaneous potential), scale: -80 to +20 mV, units: mV, line style: solid.
- Curve: Rwa (resistivity, water zone), scale: 0 to 0.1 ohm·m, units: ohm·m, line style: dashed.
- Curve: Rwa (resistivity, water zone), scale: 0 to 0.1 ohm·m, units: ohm·m, line style: dotted (possibly a second resistivity curve or a different interpretation).

Track 2 (middle):
- Curve: IL (induction log), scale: 0.2 to 20 ohm·m, units: ohm·m, line style: solid.
- Curve: Swa (water saturation), scale: 0 to 1.0 (decimal), units: v/v decimal, line style: solid.

Track 3 (rightmost):
- Curve: BVW (bulk volume water), scale: 0.25 to 0.825 (decimal), units: v/v decimal, line style: solid.
- Curve: Phia (effective porosity), scale: 0 to 0.825 (decimal), units: v/v decimal, line style: solid.
- Bar chart: black-filled bar representing BVW or Phia (likely BVW, as it is the only bar chart), with values ranging from 0.25 to 0.825.

Interval table:
| Интервал, м (feet) | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|--------------------|------------------------|-------------------|------------------------------|
| 10900–11000        | Не определена          | SP: отрицательная аномалия; Rwa: низкие значения; IL: низкие значения; Swa: высокие значения; BVW: высокие значения; Phia: высокие значения | Высокая водонасыщенность, возможно, водоносный пласт |

Results panel (not explicitly shown as a separate panel, but values are plotted):
- BVW: 0.25 to 0.825 (decimal)
- Phia: 0 to 0.825 (decimal)

KEYWORDS: каротажная диаграмма, SP, IL, Rwa, Swa, BVW, Phia, водонасыщенность, пористость, измеренная глубина, мВ, ом·м, десятичные единицы
----


Figure 10.21. Computer-processed interpretation, Eocene Wilcox sandstone, Gulf Coast, U.S.A.

Track 1 shows the SP curve and an Rwa curve calculated from the induction curve, IL.

Track 2 shows the induction log, IL.

Track 3 shows Archie water saturation, Swa, calculated from gas-corrected sonic porosity from the sonic log (Phia) and bulk volume water (BVW). The dark shaded area between the porosity curve (left-hand) and the bulk-volume-water curve indicates the proportion of pore space that is occupied by gas, whereas the light shaded area between the bulk-volume-water curve and the right margin of the track (scale value of zero) indicates the proportion that is occupied by water.
<!-- page 216 -->
Log Interpretation Case Studies 205

# Case Study 4:

# **PENNSYLVANIAN UPPER MORROW SANDSTONE, ANADARKO BASIN, U.S.A.:**

# *The Problem.*

Although the location of this well is in a depositional basin that is a significant distance from that of Case Study 3, the similarity of data, of lithology (sandstone), and of the interpreted depositional environment lead to the use of the same techniques. In Case Study 3, the scenario was that of a drilling well with significant gas shows. In this case study, the task is one of mapping existing data. If one is alert to the data at hand, a more robust prospect can be developed; the prospect includes not only geologic data of the area, but also description of opportunities missed by other operators.

# **Background**

An area covering several counties in the Anadarko Basin has been assigned to you. Your responsibility is to map and develop hydrocarbon prospects and to oversee all company activity in these counties.

As you pursue the assignment, many well logs are reviewed; some of the wells are producing and some are dry and abandoned. One particular dry-and-abandoned well captures your attention. The well wasn't tested before abandonment. However, it was logged with an induction electric log (Figure 10.22) to determine resistivities of the invaded ($R_i$) and uninvaded ($R_t$) zones, and with a sonic log (Figure 10.23) to determine porosity. The induction log shows high resistivities and the sonic log indicates that the sandstone has "good" porosity.

# **Well site information and other pertinent information:**

- $R_{mf} = 0.527$ ohm-m at $T_f$
- $R_w = 0.11$ ohm-m at $T_f$ (a questioned value)
- $T_f = 130^{\circ}\text{F}$
- Archie parameters: $a = 0.81$; $m = n = 2$
- surface temperature = $70^{\circ}\text{F}$

Volumetric recoverable oil reserves are calculated from the following parameters:

- drainage area = 160 acres;
- $B_{oi} = 1.3$;
- recovery factor ($RF$) = 0.15;

- porosity = (to be determined);
- water saturation ($S_w$) = (to be determined); and
- thickness ($h$) = 8 ft.

An analysis by the company's engineering department leads to a judgment that the well can be re-entered if evidence supports the inference that the well would be productive and profitable. Estimated cost of re-entry and completion of the well is $275,000. With a gross product price of $32.00 per barrel and a lease that has a 3/16th royalty, what would you estimate as an expectable return on investment?

# **Useful equations**

The sonic porosity formula (Wyllie time-average equation 4.1) is:

$$\phi_S = \frac{\Delta t_{log} - \Delta t_{ma}}{\Delta t_{fl} - \Delta t_{ma}} \tag{10.33}$$

For calculating $R_w$ from the SP:

$$R_w = 10^{(K \times \log(R_{mf}) + SP) / K} \tag{10.34}$$

Where: $K = 61 + 0.133 \times T_f$, and where SP is a negative number. 10.35

In this older log-display format (Figure 10.22), resistivity is displayed on a linear scale; conductivity is also shown. In parts of formations where resistivity is low, the accuracy of estimated formation resistivity can be improved by reading the conductivity (which normally is recorded on a more sensitive scale); the reciprocal is formation resistivity. The equation is:

$$R_{ILD} = \frac{1000}{C_{ILD}} \tag{10.36}$$

# **Tasks required for interpretation of the logs**

The key variable in determining whether this well will be successful is the estimated effect of water. You have an estimate of $R_w$ (shown above), but its accuracy is questioned and the estimate is regarded as being unreliable. You will need to determine $R_w$ before calculating water saturation ($S_w$); use the SP log and charts (see "Formation Water Resistivity ($R_w$), Determination," Chapter 2, or Equations 10.34 and 10.35, above). Also, you may want to calculate $R_{wa}$ to corroborate the estimate of $R_w$ from the SP curve.

Use the upper Morrow Sandstone log evaluation table (Table 10.7) to complete the evaluation.
<!-- page 217 -->
206

ASQUITH AND KRYGOWSKI

Table 10.7. Case Study 4: Upper Morrow Sandstone, Anadarko Basin, U.S.A.: work table. The symbol "v/v" indicates volume-for-volume decimal fraction.

|  Parameters  |   |   |   |
| --- | --- | --- | --- |
|  Ann. Mean Surf. Temp: 70°F |   |   | Rw (measured): (not given)  |
|  Total Depth: 8,007 ft |   |   | Rw @ fm. temp.: 0.140 ohm-m @ 130°F  |
|  Bottom Hole Temp: 135°F |   |   | Rmf (measured): (not given)  |
|  Formation Depth: 7,441 ft |   |   | Rmf @ fm. temp.: 0.527 ohm-m @ 130°F  |
|  Formation Temperature: 130°F |   |   |   |
|  DT matrix (Wyllie): 55.5 μsec/ft |   |   | DT fluid (Wyllie): 189 μsec/ft  |
|   | a: 0.81 | m: 2 | n: 2  |

|  Data and Calculations  |   |   |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  Depth feet | CILD mmho | IL ohm-m | SN ohm-m | DT μsec/ft | SPHI v/v decimal | Rwa | Swa v/v decimal | BVW  |
|  7442 |  |  |  |  |  |  |  |   |
|  7446 |  |  |  |  |  |  |  |   |
|  7349 |  |  |  |  |  |  |  |   |
|  7453 |  |  |  |  |  |  |  |   |
|  7455 |  |  |  |  |  |  |  |   |
|  7459 |  |  |  |  |  |  |  |   |
<!-- page 218 -->
Log Interpretation Case Studies

207


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth range: 7400–7500 ft, depth increases downward.
Depth unit: Feet (FT).

Track 1 (leftmost):
- Curve: SP (Spontaneous Potential)
- Scale: -160 to +40 mV
- Line style: solid black line
- Curve behaviour:
  - From 7400 to ~7480 ft: relatively flat, near 0 mV
  - At ~7480 ft: negative deflection (anomaly) to ~-80 mV
  - From ~7480 to 7500 ft: returns to near 0 mV

Track 2 (rightmost, multi-curve):
- Curve 1: IL (Induction Log — deep resistivity)
  - Scale: 0 to 1000 Ω·m (labelled as "Ωm" with "ohm m" below)
  - Line style: dashed line
- Curve 2: SN (Shallow Resistivity — shallow resistivity)
  - Scale: 0 to 50 Ω·m (labelled as "Ωm" with "ohm m" below)
  - Line style: solid line
- Curve 3: CILD (Compensated Induction Log — deep resistivity, likely same as IL)
  - Scale: 0 to 50 S/m (Siemens per meter)
  - Line style: solid line (rightmost curve)

Curve behaviour per interval:
- From 7400 to ~7480 ft:
  - IL: ~100 Ω·m
  - SN: ~10 Ω·m
  - CILD: ~10 S/m
- At ~7480 ft:
  - IL: drops sharply to ~10 Ω·m
  - SN: drops to ~5 Ω·m
  - CILD: drops to ~5 S/m
- From ~7480 to 7500 ft:
  - IL: ~10 Ω·m
  - SN: ~5 Ω·m
  - CILD: ~5 S/m

Interpretation:
- The negative SP anomaly at ~7480 ft suggests a permeable zone (likely sandstone) with formation water of higher salinity than drilling mud.
- The resistivity drop (IL, SN, CILD) at the same depth indicates a water-saturated permeable interval.
- The IL and SN curves show a resistivity contrast, suggesting possible invasion or a thin bed.

No perforation intervals, fluid contacts, or interpreted lithology are marked on the log.

KEYWORDS: well log, SP, induction log, resistivity, spontaneous potential, depth, feet, Ω·m, S/m, permeable zone, negative anomaly
----


Figure 10.22. Induction electric log with spontaneous potential, upper Morrow Sandstone, Anadarko Basin, U.S.A.

Note:

1. Deflection of the SP curve leftward in track 1, away from the shale baseline (7441 to 7452 ft), opposite the upper Morrow Sandstone.
2. Separation of the short normal resistivity curve (SN) and the induction resistivity curve (IL) in track 2; this indicates that the sandstone was invaded by mud filtrate.
3. At the depth of the upper Morrow Sandstone, leftward deflection of the SP curve and separation of the SN and induction resistivity curves are collateral evidence that leads to this conclusion: the sandstone is porous and permeable.
4. Looking at all the logs together, the resistivity logs (IL and SN) show the formation to be from 7441 to 7460 ft, whereas the SP shows the formation to be from 7441 to 7452 ft. Close inspection of the SP shows very slight deflection from the shale baseline over the bottom 8 ft of formation (7452 to 7460). The logs indicate that this interval is very shaly (SP response) and impermeable (IL and SN read the same, except for minor variation that is due to differences in vertical resolution of the measurements.).
<!-- page 219 -->
208

ASQUITH AND KRYGOWSKI

Figure 10.23. Sonic log with spontaneous potential, upper Morrow Sandstone, Anodarko Basin, U.S.A.

Note:

The relatively high interval transit time at 7446 ft (DT = 81 μsec./ft) indicates that porosity of the sandstone is high. (See Track 2 between 7441 and 7460 ft.)


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Глубина увеличивается вниз. Диапазон глубин: 7400–7500 футов (Feet MD).

Треки слева направо:
1. SP (спонтанного потенциала): шкала от -160 до 40 мВ, линейная. Кривая показывает отрицательную аномалию в интервале 7420–7430 футов, затем возвращается к базовому уровню.
2. DT (время прохождения упругой волны): шкала от 140 до 40 мкс/фут, линейная. Кривая имеет высокие значения (низкая скорость) в интервале 7420–7430 футов, что указывает на пористые или глинистые интервалы. В остальных интервалах — более низкие значения (высокая скорость), характерные для плотных пород.

Интервалы и интерпретация:
| Интервал, фут | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|---------------|--------------------------|-------------------|-------------------------------|
| 7400–7420     | Не определена            | SP — базовый уровень; DT — низкие значения | Плотная порода (например, глина или плотный известняк) |
| 7420–7430     | Не определена            | SP — отрицательная аномалия; DT — высокие значения | Пористый интервал (например, песчаник) |
| 7430–7500     | Не определена            | SP — базовый уровень; DT — низкие значения | Плотная порода |

Результаты интерпретации: не указаны.

KEYWORDS: well log, SP, DT, spontaneous potential, sonic log, depth, feet, log track, interpretation, porosity, lithology
----


<!-- page 220 -->
Log Interpretation Case Studies 209

209

### Case Study 4:

### PENNSYLVANIAN UPPER MORROW SANDSTONE, ANADARKO BASIN, U.S.A.:

The Solution.

#### Information from the logs

The upper Morrow sandstone is in the interval from 7441 to 7460 ft as shown by the response of the logs (Figure 10.22). The logs show that the top 11 ft (from 7441 to 7452) is permeable, by leftward deflection of the SP from the shale baseline, and by separation between the short normal curve, SN ($R_t$), and the induction resistivity curve, IL ($\sim R_t$). Separation between the SN and IL indicates that the rock was invaded by mud filtrate. Porosity of the sand from 7441 to 7460 ft is apparent from the comparatively high interval transit time (DT, 70 to 81 $\mu$sec/ft, Figure 10.23). The interval from 7452 to 7460 ft is not permeable, as shown by the lack of SP response and by the SN and IL curves' having the same values (indicating no invasion).

The SP is read from Figure 10.22 as -45 mV. Remember that the shale baseline is assumed to have a value of zero, and that in this display the scale sensitivity is 20 mV per scale division. From Equations 10.34 and 10.35:

$$K = 61 + (0.133 \times T_f).$$

$$K = 61 + (0.133 \times 130).$$

$$K = 78.3$$

$$R_w = 10^{(K \times \log(R_{wf}) + SP)/K}$$

$$R_w = 10^{(78.3 \times \log(0.527) - 45)/78.3}$$

$$R_w = 0.140 \text{ ohm-m}$$

The calculated $R_w$ value is close to the suspect one (0.11 ohm-m at formation temperature).

Acoustic (sonic) porosity, SPHI, is calculated from the Wyllie time-average equation, Equation 10.33. Use the accepted values for matrix and fluid parameters: $\Delta t_{ma} = 55.5 \text{ } \mu\text{sec/ft}$; $\Delta t_{fl} = 189 \text{ } \mu\text{sec/ft}$.

Apparent water resistivity ($R_{wa}$) (see Chapter 7) is calculated from the induction log and the sonic porosity. The low value at the top of the formation (Table 10.8, 7442 ft) probably is due to boundary effects of shale on the induction log, which produce a lower-than-actual resistivity value. The other low value, 0.028 ohm-m at 7455 ft, is higher than the value calculated from the SP (0.014 ohm-m), and probably indicates residual hydrocarbons in that very shaly interval. In

general, the $R_{wa}$ results are consistent with the calculated value of $R_w$. The value of $R_w$ calculated from the SP (0.14 ohm-m) is considered to be the estimate most likely to be true; therefore it is used in the water saturation equation.

Archie water saturation ($S_{wa}$) is calculated using this estimate of $R_w$ and values of porosity determined above, and the other parameters noted previously.

#### Information from crossplots

As suspected, water saturation ($S_{wa}$) values in the interval of porous sandstone (7441-7452 ft) are high (Table 10.8), ranging from 40 to 80 percent, and so are bulk volume water values (Figure 10.24). On the bulk volume water crossplot, the scatter of data points around the hyperbolic line is minor; this indicates that the reservoir may be at or near irreducible water saturation, but the points cluster around a value higher than the normal Morrow production cutoff. Therefore, water-production potential of the well remains in question.

You have completed assessment of the log and you should be encouraged by evidence of good porosities on the sonic log and good indications of permeability on the resistivity log. Also, you are aware that the low cost of re-entry of the well enhances the economics of the prospect.

However, you weigh the positive aspects of the prospect against the relatively thin zone and the few data points that you have used. The limited number of points calls into question the statistical accuracy of the information, and in turn, conclusions based on such limited data. Also, fine-grained reservoirs are not as permeable as coarse-grained reservoirs. Estimated recoverable oil is 78,000 stock-tank barrels (STB). Estimated return on investment is:

$$Return = \frac{\text{stock tank barrels (STB)}}{\times \text{product price}} \times \frac{\text{net revenue interest (NRI)}}{\text{total cost}} \tag{10.37}$$

$$Return = \frac{78,000 \times \$32.00 \times 0.8125}{\$275,000} = 7.4:1.$$

The ratio 7.4:1 is an excellent return on investment; the company accepts your recommendation to re-enter the well. (Note that the $32.00 per barrel price of oil used in this example was the value at the time the well was evaluated.)

The upper Morrow Sandstone was perforated from 7443 to 7451 ft. Initial production flowing (IPF) was
<!-- page 221 -->
210

ASQUITH AND KRYGOWSKI

100 barrels of oil per day (BOPD) and 6 barrels of salt water per day (BSWPD), with oil gravity of 38.3. During the first four months, production averaged 75 BOPD, and after six months, production stabilized at 50 BOPD. Two years after completion, an offset well was drilled 1320 ft away. The second well had initial

production flowing (*IPF*) of 336 BOPD and no water, from a 19-ft upper Morrow sandstone. The sandstone was 13 ft higher than Morrow sandstone in the well that was the subject of this analysis.

Figure 10.25 Shows the results of detailed processing of data over the interval.
<!-- page 222 -->
Log Interpretation Case Studies

211

Table 10.8. Case Study 4: Upper Morrow Sandstone, Anadarko Basin, U.S.A.: Solution table. The symbol "v/v" indicates volume-for-volume decimal fraction.

|  Parameters  |   |   |   |
| --- | --- | --- | --- |
|  Ann. Mean Surf. Temp: 70°F |   |   | Rw (measured): (not given)  |
|  Total Depth: 8,007 ft |   |   | Rw @ fm. temp.: 0.140 ohm-m @ 130°F  |
|  Bottom Hole Temp: 135°F |   |   | Rmf (measured): (not given)  |
|  Formation Depth: 7,441 ft |   |   | Rmf @ fm. temp.: 0.527 ohm-m @ 130°F  |
|  Formation Temperature: 130°F |   |   |   |
|  DT matrix (Wyllie): 55.5 μsec/ft |   |   | DT fluid (Wyllie): 189 μsec/ft  |
|   | a: 0.81 | m: 2 | n: 2  |

|  Data and Calculations  |   |   |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  Depth feet | CILD mmho | IL ohm-m | SN ohm-m | DT μsec/ft | SPHI v/v decimal | Rwa | Swa v/v decimal | BVW  |
|  7442 | 120 | 8.3 | 20 | 60 | 0.034 | 0.012 | >1.0 | 0.034  |
|  7446 | 90 | 11.1 | 30 | 81 | 0.191 | 0.500 | 0.529 | 0.101  |
|  7349 | 95 | 10.5 | 24 | 73 | 0.131 | 0.223 | 0.792 | 0.104  |
|  7453 | 130 | 7.7 | 8 | 97 | 0.311 | 0.918 | 0.391 | 0.121  |
|  7455 | 140 | 7.1 | 8 | 63 | 0.056 | 0.028 | >1.0 | 0.056  |
|  7459 | 120 | 8.3 | 11 | 84 | 0.213 | 0.469 | 0.546 | 0.117  |
<!-- page 223 -->
212

ASQUITH AND KRYGOWSKI

Figure 10.24. Bulk-volume-water crossplot (SPHI vs. Swa), upper Morrow Sandstone, Anadarko Basin, U.S.A.


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
This is a crossplot of Archie water saturation (Swa) versus acoustic porosity (SPHI).

- X-axis: Acoustic porosity, SPHI, linear scale, range 0.00 to 0.40.
- Y-axis: Archie water saturation, Swa, linear scale, range 0.00 to 1.00.

The plot contains:
- 20 data points (black dots) scattered across the plot area, primarily between SPHI 0.10 and 0.35, and Swa 0.30 to 0.80.
- Two smooth curves:
  - Lower curve: labelled "Normal Morrow Production Cutoff", passes through points approximately (0.10, 0.20), (0.20, 0.10), (0.30, 0.04). The value 0.04 is marked at SPHI ≈ 0.30.
  - Upper curve: labelled "Bulk volume, BVW", passes through points approximately (0.10, 0.80), (0.20, 0.60), (0.30, 0.30), (0.35, 0.25). The value 0.10 is marked at SPHI ≈ 0.35.

The data points lie between the two curves, with a general trend of decreasing Swa with increasing SPHI.

> Тренд: Archie water saturation (Swa) decreases as acoustic porosity (SPHI) increases, with the data points falling between the "Normal Morrow Production Cutoff" and "Bulk volume, BVW" curves.

KEYWORDS: Archie water saturation, acoustic porosity, crossplot, Swa, SPHI, production cutoff, bulk volume water, Morrow, petrophysics, log interpretation
----


Figure 10.25. Upper Morrow Sandstone, Anadarko Basin, U.S.A. Computer-processed log.

In track 3 the dark shaded area between the porosity curve (SPHI) and the bulk-volume-water curve (BVW) indicates the proportion of pore space that is occupied by oil, whereas the light shaded area between the bulk-volume-water curve and the right margin of the track (scale value of zero) indicates the proportion that is occupied by water.


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Глубина увеличивается вниз. Диапазон глубин: 7400–7500 м, единицы: MD (Measured Depth).

Треки слева направо:

1. **SP** — потенциал спонтанного поля, шкала: −160 до +40 мВ, линейная, кривая: тонкая черная линия.  
   Поведение: в интервале 7400–7500 м — отрицательная аномалия, амплитуда ~100 мВ, симметричная, плавная форма.

2. **Fest** — не указано, но по расположению и шкале — вероятно, резистивиметрия (например, IL или R).  
   Шкала: 0,2–20 Ом·м, логарифмическая, кривая: тонкая черная линия.  
   Поведение: в интервале 7400–7500 м — резкое падение с ~10 Ом·м до ~0,5 Ом·м, затем резкое увеличение до ~10 Ом·м.

3. **IL** — индукционный лог (или резистивиметрия), шкала: 0,2–20 Ом·м, логарифмическая, кривая: тонкая черная линия.  
   Поведение: аналогично Fest — резкое падение, затем резкое увеличение.

4. **Swa** — водонасыщенность, шкала: 0–1 (в десятичных долях), линейная, кривая: тонкая черная линия.  
   Поведение: в интервале 7400–7500 м — резкое падение с ~0,9 до ~0,3, затем резкое увеличение до ~0,9.

5. **EYW** — вероятно, эффективная водонасыщенность или параметр, связанный с водой.  
   Шкала: 0–0,5 (в десятичных долях), линейная, кривая: тонкая черная линия.  
   Поведение: в интервале 7400–7500 м — резкое падение с ~0,4 до ~0,1, затем резкое увеличение до ~0,4.

6. **SPH** — не указано, но по расположению и шкале — вероятно, параметр, связанный с пористостью или насыщенностью.  
   Шкала: 0–0,5 (в десятичных долях), линейная, кривая: тонкая черная линия.  
   Поведение: в интервале 7400–7500 м — резкое падение с ~0,4 до ~0,1, затем резкое увеличение до ~0,4.

Интерпретационные интервалы:
- Интервал 7400–7500 м: интерпретируется как коллектор с высокой пористостью и низкой водонасыщенностью в центральной части (Swa ~0,3), что указывает на наличие нефти.  
- Кривые SP, IL, Fest показывают резкое изменение — характерно для границы коллектора/не-коллектора.

Результаты панель не присутствует.

KEYWORDS: каротажная диаграмма, SP, IL, Fest, Swa, EYW, SPH, резистивиметрия, водонасыщенность, пористость, коллектор, нефть, глубина, MD, мВ, Ом·м, десятичные доли
----


<!-- page 224 -->
Log Interpretation Case Studies 213

213

# Case Study 5:

# **CRETACEOUS PICTURED CLIFFS SANDSTONE, SAN JUAN BASIN, U.S.A.:**

# *The Problem.*

Case Study 5 introduces a shaly sand interpretation, with equations for shale volume, effective porosities, and the Simandoux (1963) form of Archie's equation for shaly sands. The effective porosity and water saturation equations require the volume of shale ($V_{\text{shale}}$), calculated from the gamma ray log. Entering the equations into a spreadsheet program may be the most efficient way to do these somewhat-complex calculations.

# **Background**

The company that you work for has purchased a large block of acreage in the San Juan Basin, much of it with gas production. The company is pursuing an active development-drilling program of infilling new Pictured Cliffs Sandstone wells on 80-acre units, rather than on the 160-acre units required under previous rules of spacing.

You are presented with logs of a new infill well and are asked to evaluate them. In this well, the depth of the Pictured Cliffs Sandstone is from 1920 to 1964 ft. The log package includes an induction log with a spherically focused log (SFL) and an SP log (Figure 10.26). (Note that the induction log plot shows the spherically focused log as "SFLA," for Spherically Focused Log, Averaged. The SFL has been averaged so that its response resembles more closely the older short normal log. This allows better comparison of this new log with logs of older wells in the field.) A combination neutron-density log (recorded in sandstone porosity units) with a gamma ray log (Figure 10.27) also was run.

From experience you know that shale in sandstone can affect logging measurements adversely. Water saturations calculated by the Archie formula tend to be too high (see Chapter 7, Log Interpretation), because shale affects porosity logs and resistivity logs. Furthermore, shale in the reservoir tends to reduce permeability.

Careful examination of the neutron porosity log (NPHI) density porosity log (DPHI) and gamma ray log (GR) (Figure 10.27) convinces you that the Pictured Cliffs sandstone is shaly. A shaly sand analysis will be necessary. However, before following this investigative path, you decide to check the $R_w$ value

given for the area against a log-calculated $R_w$. (See Table 2.1 for $R_w$ formulas, and charts in Figures 2.3 to 2.5.)

# **Well site information and other pertinent information:**

- $BHT = 89^{\circ}\text{F}$ at 2145 ft
- surface temperature = $65^{\circ}\text{F}$
- formation temperature, $T_f = 87^{\circ}\text{F}$
- $R_{mf} = 2.26$ ohm-m at $65^{\circ}\text{F}$

Because of the infill-drilling program, your company is particularly interested in recoverable reserves based on 80-acre units. Reservoir depletion will not be a problem, because Pictured Cliffs Sandstone wells normally don't drain 160 acres. Volumetric recoverable gas reserves are estimated from the following parameters:

- drainage area ($DA$) = 80 acres
- reservoir thickness ($h$) (to be determined)
- effective porosity ($\phi_e$) (to be determined)
- water saturation ($S_w$) (to be determined)
- recovery factor ($RF$) = 0.75
- gas gravity (estimated) = 0.51
- reservoir temperature (estimated) = $87^{\circ}\text{F}$
- bottom hole pressure—estimated ) = 770 PSI
- Z factor = 0.928

# **Helpful equations**

In this older log-display format, resistivity is recorded on a linear scale, but conductivity is also shown, on a more sensitive scale. In strata where resistivity is low, a more accurate estimate of resistivity can be made by reading conductivity and reciprocating the number to get formation resistivity. The equation is shown in Case Study 4 (Equation 10.36):

$$R_{ILD} = \frac{1000}{C_{ILD}}$$

For shaly sand analysis of a formation, formulas for these calculations are required: volume of shale, corrected neutron and density porosity, and water saturation, corrected for the effect of shale.

Formulas for this shaly sand analysis are:

$$V_{shale} = I_{GR} = \frac{GR_{log} - GR_{clean}}{GR_{shale} - GR_{clean}} \tag{10.38}$$

$$NPHIc = NPHI - V_{shale} \times NPHI_{shale} \tag{10.39}$$
<!-- page 225 -->
214

ASQUITH AND KRYGOWSKI

$$DPHIc = DPHI - V_{shale} \times DPHI_{shale} \tag{10.40}$$

$$PHI = \sqrt{\frac{DPHIc^2 + NPHIc^2}{2}} \tag{10.41}$$

$$S_w = \frac{0.4 \times R_w}{PHI^2} \times \left[ \left( \frac{5 \times PHI^2}{R_t \times R_w} + \left( \frac{V_{shale}}{R_{shale}} \right)^2 \right)^{\frac{1}{2}} - \frac{V_{shale}}{R_{shale}} \right] \tag{10.42}$$

where (formula variables):

$V_{shale}$ = calculated volume of shale

$GR_{log}$ = gamma ray reading from several positions in Pictured Cliffs Sandstone

$GR_{clean}$ = gamma ray reading of the cleanest part of the sandstone

$GR_{shale}$ = average gamma ray reading in a nearby shale

$NPHIc$ = neutron porosity corrected for shale

$NPHI_{shale}$ = neutron porosity of a nearby shale

$DPHIc$ = density porosity corrected for shale

$DPHI_{shale}$ = density porosity of a nearby shale

$PHI$ = effective porosity: neutron-density porosity corrected for shale and gas

$R_{shale}$ = deep resistivity reading of a nearby shale

Use Table 10.9 for the evaluation.

Table 10.9. Case Study 5: Pictured Cliffs Sandstone, San Juan Basin, U.S.A.: Work table. The symbol "v/v" indicates volume-for-volume decimal fraction.

|  **Parameters**  |   |   |   |   |
| --- | --- | --- | --- | --- |
|  Ann. Mean Surf. Temp: 65°F |   |   |   | Rw (measured): ohm-m @ °F  |
|  Total Depth: 2145 ft |   |   |   | Rw @ fm. temp.: 0.24 ohm-m @ 87°F  |
|  Bottom Hole Temp: 89°F |   |   |   | Rmf (measured): 2.26 ohm-m @ 65°F  |
|  Formation Depth: 1930 ft |   |   |   | Rmf @ fm. temp.: 1.73 ohm-m @ 87°F  |
|  Formation Temperature: 87°F |   |   |   |   |
|  DT matrix (Wyllie): 55.5 μsec/ft |   |   |   | DT fluid (Wyllie): 189 μsec/ft  |
|  RHO matrix: 2.65 g/cm³ |   |   |   | RHO fluid: 1.0 g/cm³  |
|  GRclean : 63 API |   |   |   | GRshale: 120 API  |
|  DPHIshale: 0.14 |   |   |   | NPHIshale: 0.4  |
|  Rshale: 4.2 ohm-m |   |   |   |   |
|   | a: 1 | m: 2 | n: 2 |   |

|  **Raw Data**  |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- |
|  Depth feet | GR API | CILD mmho/m | ILD ohm-m | SFLA ohm-m | DPHI v/v decimal | NPHI v/v decimal  |
|  1,928 | 70 | 90 | 11.1 | 16 | 0.175 | 0.275  |
|  1,935 |  |  |  |  |  |   |
|  1,942 |  |  |  |  |  |   |
|  1,945 | 75 | 72 | 13.9 | 16 | 0.150 | 0.225  |
|  1,949 |  |  |  |  |  |   |
|  1,953 |  |  |  |  |  |   |
|  1,958 |  |  |  |  |  |   |
|  1,962 | 83 | 100 | 10.0 | 10 | 0.120 | 0.260  |
<!-- page 226 -->
Log Interpretation Case Studies

215

Table 10.9. Case Study 5: Pictured Cliffs Sandstone, San Juan Basin, U.S.A.: Work table. The symbol "v/v" indicates volume-for-volume decimal fraction. (Cont'd.)

|  Porosity calculations  |   |   |   |   |
| --- | --- | --- | --- | --- |
|  Depth feet | Vshale v/v decimal | DPHIc v/v decimal | NPHIc v/v decimal | PHI v/v decimal  |
|  1,928 | 0.123 | 0.158 | 0.226 | 0.195  |
|  1,935 |  |  |  |   |
|  1,942 |  |  |  |   |
|  1,945 | 0.211 | 0.121 | 0.141 | 0.131  |
|  1,949 |  |  |  |   |
|  1,953 |  |  |  |   |
|  1,958 |  |  |  |   |
|  1,962 | 0.351 | 0.071 | 0.120 | 0.098  |

|  Saturation and other indicators  |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- |
|  Depth feet | Swa v/v decimal | Sw v/v decimal | Sxo v/v decimal | MHI | MOS | BVW  |
|  1,928 | 0.754 | 0.605 | >1.0 | 0.604 | 0.396 | 0.118  |
|  1,935 |  |  |  |  |  |   |
|  1,942 |  |  |  |  |  |   |
|  1,945 | >1.0 | 0.660 | 1.000 | 0.660 | 0.341 | 0.086  |
|  1,949 |  |  |  |  |  |   |
|  1,953 |  |  |  |  |  |   |
|  1,958 |  |  |  |  |  |   |
|  1,962 | >1.0 | 0.806 | >1.0 | 0.805 | 0.195 | 0.079  |
<!-- page 227 -->
216

ASQUITH AND KRYGOWSKI


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: increases downward, units: Feet (MD), range: 0 to 1900 ft (visible portion).

Track 1 (left):
- Curve: SP (Spontaneous Potential)
- Scale: −100 to 0 mV
- Line style: solid black line
- Curve behavior:
  - From top to ~1900 ft: relatively flat, slight negative deflection
  - Below 1900 ft: large negative anomaly (deep trough), then gradual recovery upward

Track 2 (right):
- Depth scale: Feet MD (same as left track)
- Contains three curves:
  1. IL (Induction Log — resistivity)
     - Scale: 0 to 400 ohm·m (logarithmic scale implied by tick marks)
     - Line style: solid black line
     - Behavior: high resistivity at top, sharp drop at ~1900 ft, then fluctuating with multiple peaks and troughs
  2. SELA (Sonic Log — acoustic travel time)
     - Scale: 0 to 160 μs/ft (μs/ft)
     - Line style: dashed line
     - Behavior: relatively low and stable at top, sharp increase at ~1900 ft, then fluctuating with multiple peaks and troughs
  3. CL.D (Caliper Log — borehole diameter)
     - Scale: 0 to 100 in (inches)
     - Line style: solid black line (rightmost curve)
     - Behavior: relatively stable at top, sharp increase at ~1900 ft, then fluctuating with multiple peaks and troughs

Marked interval:
- At ~1900 ft: a horizontal line with arrow labeled "2" spans across the IL and SELA curves, indicating a specific interval or boundary.

No lithology interpretation, porosity, saturation, or fluid contacts are marked on the log.

KEYWORDS: well log, SP, IL, SELA, CL.D, resistivity, spontaneous potential, sonic log, caliper log, depth, feet, mV, ohm·m, μs/ft, in, induction log, acoustic travel time, borehole diameter
----


Figure 10.26. Induction-SFL log with spontaneous potential, Pictured Cliffs Sandstone, San Juan Basin, U.S.A.

Note:

SP deflection (negative, track 1) and resistivity (tracks 2 and 3) increase upward through the Pictured Cliffs Sandstone (1970 to 1924 ft), the result of decrease of shale within the sandstone.
<!-- page 228 -->
Log Interpretation Case Studies

217


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Глубина увеличивается вниз. Диапазон глубин: от 0 до 16 м (по шкале на левой стороне, с шагом 2 м). Шкала глубин — линейная, единицы — метры.

Треки (слева направо):
1. GR — гамма-каротаж. Шкала: 0–200 API. Единицы: API. Кривая: сплошная линия. Поведение: высокие показания (до 200 API) в верхней части, затем резкое снижение до ~100 API, далее колебания с амплитудой ~50 API, с небольшими пиками.
2. CALI — калиброметрия. Шкала: 6–16 дюймов. Единицы: дюймы. Кривая: сплошная линия. Поведение: стабильная, ~8 дюймов, с небольшими колебаниями.
3. ПС — потенциал спонтанного. Шкала: -6 до +6 мВ. Единицы: мВ. Кривая: сплошная линия. Поведение: отрицательная аномалия в верхней части (~-4 мВ), затем переход к нулевому значению, далее колебания с амплитудой ~2 мВ.

Интервалы и интерпретация:
| Интервал, м | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|-------------|--------------------------|-------------------|-------------------------------|
| 0–2         | —                        | GR: ~200 API; CALI: ~8"; ПС: ~-4 мВ | —                             |
| 2–4         | —                        | GR: снижается до ~150 API; CALI: ~8"; ПС: ~-2 мВ | —                             |
| 4–16        | —                        | GR: колебания 100–150 API; CALI: ~8"; ПС: колебания ±2 мВ | —                             |

Результаты панель не присутствует.

KEYWORDS: каротаж, гамма-каротаж, калиброметрия, потенциал спонтанного, GR, CALI, ПС, мВ, API, дюймы, глубина, лог, кривые, интервал
----


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: Feet MD, increases downward. Depth range: 1800–2000 ft (visible portion).

Tracks (left to right):
1. DPH (Density Porosity) — scale: 0.4 to 0.25 (unit: g/cm³), solid line.
2. DRHO (Density Log — bulk density) — scale: 0 to 0.25 (unit: g/cm³), solid line.
3. NPHI (Neutron Porosity) — scale: 0.4 to 0.25 (unit: fraction), dashed line.
4. Wv decal (Water volume decimal) — scale: 0.4 to 0.25 (unit: fraction), dashed line.
5. Wv decal (Water volume decimal) — scale: 0.4 to 0.25 (unit: fraction), dashed line (duplicate track or mislabelled).

Curves:
- DPH: Solid curve, shows high values (~0.25) in upper interval, decreases to ~0.20, then fluctuates.
- DRHO: Solid curve, shows low values (~0.25) in upper interval, increases to ~0.30, then fluctuates.
- NPHI: Dashed curve, shows high values (~0.25) in upper interval, decreases to ~0.20, then fluctuates.
- Wv decal (two tracks): Dashed curves, show high values (~0.25) in upper interval, decrease to ~0.20, then fluctuate.

Interpretation:
- The curves DPH, DRHO, NPHI, and Wv decal show consistent behavior: high values in upper section, decreasing with depth, then fluctuating.
- No marked bed boundaries or interpreted intervals are visible.
- No results panel (Кп, Кн, Кпр, etc.) is present.

Interval table:
| Интервал, м | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|-------------|--------------------------|-------------------|-------------------------------|
| 1800–2000   | Не определена            | DPH, DRHO, NPHI, Wv decal — высокие значения в верхней части, затем снижение и колебания | Не подписана |

KEYWORDS: well log, DPH, DRHO, NPHI, Wv decal, density porosity, neutron porosity, bulk density, water volume, feet MD, log track, curve behavior
----


Figure 10.27. Combination neutron-density log with gamma ray and caliper logs, Pictured Cliffs Sandstone, San Juan Basin, U.S.A.

Note:

1) Neutron and density readings are recorded in units relative to sandstone.
2) On the caliper log (track 1), decrease of hole diameter in the interval 1926 to 1958 ft indicates mudcake, and therefore indicates that the sandstone is permeable.
3) Neutron porosity, NPHI, is greater than density porosity, DPHI (tracks 2 and 3), which is anomalous, for this reason: Sandstone-calibrated neutron and density logs in a clean, gas-bearing sandstone should show neutron porosity that is less than density porosity, because of gas effect ("crossover"). This explanation is justified by the evidence at hand: High neutron porosity of the Pictured Cliffs formation is the result of shale in the sandstone. Concentration of hydrogen in clay minerals of shale is high; consequently neutron porosity is recorded as being greater than the actual porosity.
<!-- page 229 -->
218

ASQUITH AND KRYGOWSKI

### Case Study 5:

### CRETACEOUS PICTURED CLIFFS SANDSTONE, SAN JUAN BASIN, U.S.A.:

*The Solution.*

#### *Visual evaluation of the logs*

The combination neutron-density log (Figure 10.27) was run on a sandstone matrix; the general configuration of the gamma ray curve and the mutual disposition of the neutron- and density-porosity curves alert you to the likelihood of shale in the reservoir. The gamma ray curve is only about 40 API units leftward from the shale baseline, on the average. Moreover, you know that in shale-free sandstone that contains oil or water, if the neutron and density logs were recorded on the basis of a sandstone matrix, one curve should approximately overlie the other. If the sandstone is shale-free and contains gas, the density-porosity reading should be greater than the neutron-porosity reading—the curves should show “crossover.” However, your examination of the Pictured Cliffs indicates that neutron porosity is greater than density porosity, except in the uppermost 4 ft. The absence of crossover and the high neutron porosity are indicative of shaly sandstone. In this case, response of the neutron and density logs to abundant shale has masked any response to gas.

Although the mudlog data is not available to verify the interpretation, you interpret the top 4 ft of the Pictured Cliffs to be coal. Your hypothesis is based on the following observations (Figure 10.27):

- (a) neutron porosity, NPHI, greater than 0.4;
- (b) density porosity, DPHI, greater than 0.4;
- (c) caliper curve in gauge—at hole diameter—except for topmost 1 ft; and
- (d) DRHO-curve average is almost zero.

If the hole were washed out, then neutron and density porosity should show large amounts of porosity—and they do, but caliper curve should show evidence of a washout and DRHO should show evidence of correction—but they don’t. The log signature could be explained with convergence of these four lines of evidence and one other—the resistivity spike at 1920-1924 ft. The weight of evidence is in favor of a 4-ft bed of coal. Following this line of reasoning, coal is also indicated at 1820-1824 ft, 1846-1850 ft and 1900-1908 ft—low density of coal: high density-porosity; cleat with high content of water: high neutron porosity.

Presumably the high carbon content of coal would

be manifest as high resistivity. Over the intervals that you estimate to be coal, in the uppermost two, the resistivity increases only slightly (Figure 10.26), but this is probably due to the thinness of the coal beds and the fact that the induction log has a vertical resolution of at the least 4 ft (depending on formation and borehole properties). The induction log is affected by the adjacent shales, even around the thickest of the coal beds.

Note that from 1923 to 1957 ft the caliper log (Figure 10.27) shows that the diameter of the borehole is less than the diameter of the drill bit. The reduced hole diameter indicates mudcake, which means that the sandstone has been invaded by mud filtrate.

#### *Calculations*

First, calculate $R_w$. Equations in Table 2.1 (Chapter 2) or charts in Figures 2.3 to 2.5 are appropriate. The SP of -57 mV at 1935 ft (Figure 10.26; measured from the shale baseline, which is assumed to have an SP value of zero) yields these values:

$$R_{mf} \text{ at } T_f: R_{mf} = 1.73 \text{ ohm-m};$$

equivalent formation-water resistivity: $R_{we} = 0.284$ ohm-m; and

$$R_w \text{ at } T_f: R_w = 0.24 \text{ ohm-m}.$$

Next, calculate effective porosity, PHI (average neutron-density porosity, shale- and gas-corrected), using Equations 10.39 to 10.41, and calculate the shaly sand water saturation using Equation 10.42. To do so, first calculate shale volume, $V_{shale}$, from the gamma ray log (Figure 10.27), by Equation 10.38: $GR_{clean} = 63$ API units (at 1953 ft) and $GR_{shale} = 120$ API units (at 1909 and 1915 ft).

Also, inspect the following parameters of clay, at 1897 ft (Figure 10.27): $NPHI_{shale} = 0.40$, $DPHI_{shale} = 0.14$, and $R_{shale} = 4.2$ ohm-m, all to be used in computing porosities and water saturation.

The resistivity can be determined more accurately if conductivity (CILD) is read (Figure 10.26), and resistivity is calculated from those values by use of Equation 10.36. Calculations of shale volume, effective porosity, and water saturation are shown in Table 10.10 (calculated by the Archie equation and by the method for shaly sand, from Equation 10.42).

Water saturation calculated by the standard Archie equation ($S_{wa}$) ranges from 0.66 to 1.0 (66% to 100%) (Table 10.10). These high water saturation values are a result of shale in the reservoir; $V_{shale}$ ranges from 0.0 to 0.35 (0% to 35%). By using the Simandoux (1963) shaly sand equation to correct for the effect of shale, water saturation estimates ($S_w$) are reduced to the range
<!-- page 230 -->
Log Interpretation Case Studies

219

of 0.52 to 0.81 (52% to 81%). Such a substantial modification illustrates the importance of shaly sand analysis in the evaluation of some sandstone reservoirs.

The bulk-volume-water plot (Figure 10.28) shows deviation of points from a constant BVW value, indicating the potential for some water production.

Below 1956 ft the caliper log (Figure 10.27) shows no evidence of mudcake, indicating that permeability of the strata may be so low as to preclude production of water. Also, resistivity curves below 1956 ft (Figure 10.26) are almost of the same value, showing no attributes of an invasion profile.

Volumetric calculations yield a production estimate of approximately 0.19 BCF, based on the following parameters:

- drainage area (DA) = 80 acres
- reservoir thickness (h) = 30 ft
- effective porosity ($\phi_e$) = 0.15 (15%)
- water saturation ($S_w$) = 0.60 (60%)
- recovery factor (RF) = 0.75
- gas gravity (estimated) = 0.51
- reservoir temperature (estimated) = 87°F
- bottom hole pressure (estimated) = 770 PSI
- Z factor = 0.928

The information you have developed, the shallow reservoir, the low cost of drilling and production, and

the very low level of risk are altogether a compelling basis to recommend completion of the well.

Consider the writing of a report on the Pictured Cliffs Sandstone infill well: Summarize all of the favorable indicators. First, the formation is approximately 30 ft thick. Second, it is permeable, as shown by the mudcake (caliper log, Figure 10.27). Permeability also is indicated by the moveable hydrocarbon estimators (MHI and MOS, Table 10.10). Third, porosity that ranges from 10% to about 20% is documented by the neutron and density logs (Table 10.10).

The Pictured Cliffs was perforated from 1926 to 1954 ft. After an acid treatment and a sand frac, the well produced 350 mcfgpd with no water, on a 3/4-in. choke. During the first year of production, the well produced approximately 60 million cubic feet (60,000 mcf) of gas.

Figure 10.29 shows a computer-processed log of the Pictured Cliffs interval. Track 3 shows water saturation computed on the basis of the Simandoux (1963) shaly sand equation, corrected porosity, and bulk volume water. The dark shaded area between the porosity curve (left-hand) and the bulk-volume-water curve indicates the proportion of pore space that is occupied by gas; the light shaded area between the bulk-volume-water curve and the right margin of the track (scale value of zero) indicates the proportion occupied by water.
<!-- page 231 -->
220

ASQUITH AND KRYGOWSKI

Table 10.10. Case Study 5: Pictured Cliffs Sandstone, San Juan Basin, U.S.A.: Solution table. The symbol "v/v" indicates volume-for-volume decimal fraction.

|  Parameters  |   |   |   |
| --- | --- | --- | --- |
|  Ann. Mean Surf. Temp: 65°F |   |   | Rw (measured): ohm-m @ °F  |
|  Total Depth: 2145 ft |   |   | Rw @ fm. temp.: 0.24 ohm-m @ 87°F  |
|  Bottom Hole Temp: 89°F |   |   | Rmf (measured): 2.26 ohm-m @ 65°F  |
|  Formation Depth: 1930 ft |   |   | Rmf @ fm. temp.: 1.73 ohm-m @ 87°F  |
|  Formation Temperature: 87°F |   |   |   |
|  DT matrix (Wyllie): 55.5 μsec/ft |   |   | DT fluid (Wyllie): 189 μsec/ft  |
|  RHO matrix: 2.65 g/cm³ |   |   | RHO fluid: 1.0 g/cm³  |
|  GRclean : 63 API |   |   | GRshale: 120 API  |
|  DPHIshale: 0.14 |   |   | NPHIshale: 0.4  |
|  Rshale: 4.2 ohm-m |   |   |   |
|   | a: 1 | m: 2 | n: 2  |

|  Raw Data  |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- |
|  Depth feet | GR API | CILD mmho/m | ILD ohm-m | SFLA ohm-m | DPHI v/v decimal | NPHI v/v decimal  |
|  1,928 | 70 | 90 | 11.1 | 16 | 0.175 | 0.275  |
|  1,935 | 74 | 70 | 14.3 | 19 | 0.160 | 0.240  |
|  1,942 | 72 | 60 | 16.7 | 20 | 0.170 | 0.230  |
|  1,945 | 75 | 72 | 13.9 | 16 | 0.150 | 0.225  |
|  1,949 | 70 | 65 | 15.4 | 19 | 0.180 | 0.260  |
|  1,953 | 63 | 87 | 11.5 | 15 | 0.120 | 0.220  |
|  1,958 | 82 | 95 | 10.5 | 12 | 0.155 | 0.240  |
|  1,962 | 83 | 100 | 10.0 | 10 | 0.120 | 0.260  |
<!-- page 232 -->
Log Interpretation Case Studies

221

Table 10.10. Case Study 5: Pictured Cliffs Sandstone, San Juan Basin, U.S.A.: Solution table. The symbol "v/v" indicates volume-for-volume decimal fraction. (Cont'd.)

|  Porosity calculations  |   |   |   |   |
| --- | --- | --- | --- | --- |
|  Depth feet | Vshale v/v decimal | DPHIc v/v decimal | NPHIc v/v decimal | PHI v/v decimal  |
|  1,928 | 0.123 | 0.158 | 0.226 | 0.195  |
|  1,935 | 0.193 | 0.133 | 0.163 | 0.149  |
|  1,942 | 0.158 | 0.148 | 0.167 | 0.158  |
|  1,945 | 0.211 | 0.121 | 0.141 | 0.131  |
|  1,949 | 0.123 | 0.163 | 0.211 | 0.188  |
|  1,953 | 0.000 | 0.120 | 0.220 | 0.177  |
|  1,958 | 0.333 | 0.108 | 0.107 | 0.108  |
|  1,962 | 0.351 | 0.071 | 0.120 | 0.098  |

|  Saturation and other indicators  |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- |
|  Depth feet | Swa v/v decimal | Sw v/v decimal | Sxo v/v decimal | MHI | MOS | BVW  |
|  1,928 | 0.754 | 0.605 | >1.0 | 0.604 | 0.396 | 0.118  |
|  1,935 | 0.872 | 0.605 | 0.878 | 0.689 | 0.273 | 0.090  |
|  1,942 | 0.761 | 0.551 | 0.924 | 0.596 | 0.373 | 0.087  |
|  1,945 | >1.0 | 0.660 | 1.000 | 0.660 | 0.341 | 0.086  |
|  1,949 | 0.663 | 0.519 | 0.973 | 0.534 | 0.454 | 0.098  |
|  1,953 | 0.815 | 0.729 | >1.0 | 0.729 | 0.272 | 0.129  |
|  1,958 | >1.0 | 0.760 | 0.955 | 0.796 | 0.195 | 0.082  |
|  1,962 | >1.0 | 0.806 | >1.0 | 0.805 | 0.195 | 0.079  |
<!-- page 233 -->
222

ASQUITH AND KRYGOWSKI

Figure 10.28. Bulk-volume-water crossplot (porosity, PHI vs. water saturation, Sw), Pictured Cliffs Sandstone, San Juan Basin, U.S.A.


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
This is a scatter plot with two fitted curves, showing the relationship between water saturation (Sw) and porosity (PHI).

- **X-axis (horizontal):** Porosity, PHI. Range: 0.00 to 0.30. Scale: linear.
- **Y-axis (vertical):** Water saturation, Sw. Range: 0.00 to 1.00. Scale: linear.

The plot contains:
- **Data points:** Approximately 40–50 black circular data points scattered across the plot area, primarily between PHI = 0.10 and 0.25, and Sw = 0.30 to 0.80.
- **Two fitted curves (smooth lines):**
  - Upper curve: Labeled "0.12" at its right end. It starts near (PHI=0.10, Sw=0.90) and curves downward to (PHI=0.25, Sw≈0.50).
  - Lower curve: Labeled "0.08" at its right end. It starts near (PHI=0.10, Sw=0.80) and curves downward to (PHI=0.28, Sw≈0.30).

The curves appear to represent water saturation trends for different values of a parameter (likely permeability or another rock property), with 0.12 and 0.08 being the values of that parameter.

> Тренд: Water saturation decreases with increasing porosity, with higher saturation values for the curve labeled 0.12 compared to 0.08 at the same porosity.

KEYWORDS: water saturation, porosity, scatter plot, fitted curve, petrophysics, Sw, PHI, relative permeability, capillary pressure, reservoir characterization
----


<!-- page 234 -->
Log Interpretation Case Studies

223


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Глубина увеличивается вниз. Диапазон глубин: от 0 до 100 м (или условных единиц, не указано в метрах).

Треки слева направо:
- Трек 1: GR (гамма-каротаж). Шкала: 0–200 API. Кривая: сплошная линия. Поведение: в верхней части (0–20 м) — низкие показания (~30 API), затем резкое увеличение до ~180 API на глубине ~40 м, после чего снижение до ~100 API на глубине ~60 м, затем снова рост до ~180 API на глубине ~80 м и снижение к концу.
- Трек 2: SP (потенциал самопроизвольный). Шкала: -100 до +100 мВ. Кривая: сплошная линия. Поведение: в верхней части — отрицательная аномалия (~-50 мВ), затем переход к положительной аномалии (~+50 мВ) на глубине ~30 м, после чего резкое падение до ~-80 мВ на глубине ~40 м, затем постепенное увеличение до ~0 мВ на глубине ~60 м, и снова резкое падение до ~-80 мВ на глубине ~80 м.

Отбивки (маркированные границы):
- На глубине ~20 м: вертикальная линия, обозначающая границу.
- На глубине ~40 м: вертикальная линия, обозначающая границу.
- На глубине ~60 м: вертикальная линия, обозначающая границу.
- На глубине ~80 м: вертикальная линия, обозначающая границу.

Интерпретация (если подписана): не подписана.

Результаты панель (Кп, Кн, Кпр и т.д.): отсутствуют.

Интервалы:
| Интервал, м | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|-------------|--------------------------|-------------------|-------------------------------|
| 0–20        | не определена            | GR: низкие (~30 API), SP: отрицательная аномалия (~-50 мВ) | — |
| 20–40       | не определена            | GR: резкое увеличение до ~180 API, SP: переход к положительной аномалии (~+50 мВ), затем резкое падение до ~-80 мВ | — |
| 40–60       | не определена            | GR: снижение до ~100 API, SP: постепенное увеличение до ~0 мВ | — |
| 60–80       | не определена            | GR: рост до ~180 API, SP: резкое падение до ~-80 мВ | — |
| 80–100      | не определена            | GR: снижение, SP: рост | — |

KEYWORDS: каротаж, ГК, ПС, гамма-каротаж, потенциал самопроизвольный, кривые, интервалы, отбивки, глубина, аномалия, литология, интерпретация


Feet MD


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Глубина увеличивается вниз. Диапазон глубин: не указан, но по шкале видны значения от ~0,2 до ~200 (единицы не указаны, предположительно метры).

Треки слева направо:

1. Трек 1 (левый):  
   - Кривая: ILD (индукционный лог, глубокий)  
   - Шкала: 0,2 — 200 ohm·m (ом·м)  
   - Линия: сплошная  
   - Кривая: SRLA (сопротивление, вероятно, латеральный или средний)  
   - Шкала: 0,2 — 200 ohm·m  
   - Линия: пунктирная  
   - Поведение: обе кривые показывают высокие значения (выше 100 ом·м) в верхней части, затем резкое падение до ~10 ом·м в нижней части. В нижней части наблюдается узкая зона с повышенным сопротивлением (~50 ом·м).

2. Трек 2 (правый):  
   - Кривая: BVW (объёмная влажность, вероятно, из нейтронного лога)  
   - Шкала: 0 — 0,5 v/v decimal (объёмная доля, десятичные)  
   - Линия: сплошная  
   - Кривая: PH (пористость, вероятно, из нейтронного или плотностного лога)  
   - Шкала: 0 — 0,5 v/v decimal  
   - Линия: пунктирная  
   - Поведение: кривая BVW показывает низкие значения (~0,1) в верхней части, затем резкое увеличение до ~0,45 в нижней части. Кривая PH также показывает низкие значения в верхней части, затем резкое увеличение до ~0,45 в нижней части.  
   - В нижней части трека присутствует заштрихованная область (чередующиеся чёрные и белые полосы), вероятно, обозначающая интервал с высокой пористостью и влажностью.

Интерпретационные интервалы (по кривым):

| Интервал, м | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|-------------|--------------------------|-------------------|-------------------------------|
| Верхняя часть | Не определена | ILD, SRLA: высокие значения (>100 ом·м); BVW, PH: низкие значения (~0,1) | Вероятно, непроницаемый слой (глина, плотный известняк) |
| Нижняя часть | Не определена | ILD, SRLA: низкие значения (~10 ом·м); BVW, PH: высокие значения (~0,45) | Вероятно, пористый и проницаемый слой, насыщенный водой (водонасыщенный коллектор) |

Результаты петрофизической интерпретации (в нижней части трека 2):
- Заштрихованная область: вероятно, интервал с высокой водонасыщенностью (Sw ≈ 1,0), что соответствует BVW ≈ 0,45 и PH ≈ 0,45.

KEYWORDS: каротажная диаграмма, ILD, SRLA, BVW, PH, сопротивление, пористость, влажность, водонасыщенность, интерпретация коллектора, глубина, ом·м, v/v decimal
----


Figure 10.29. Pictured Cliffs Sandstone, San Juan Basin, U.S.A. Computer-processed log.

Track 3: The dark shaded area between the porosity curve (left-hand) and the bulk-volume-water curve indicates the proportion of pore space that is occupied by gas. The light-shaded area between the bulk-volume-water curve and the right-hand margin of the track (scale value of zero) indicates the proportion of pore space that is occupied by water.
<!-- page 235 -->
224

ASQUITH AND KRYGOWSKI

# Case Study 6:

# **ORDOVICIAN-SILURIAN CHIMNEYHILL SUBGROUP, HUNTON GROUP, ANADARKO BASIN, U.S.A.:**

# *The Problem.*

The well that is the subject of Case Study 6 is in a carbonate-rock province. Logs of this well show information that can be attributed to variation in both lithology and formation fluid. Because this case study is in the latter part of the sequence of case studies, interpretation is left almost entirely to the reader.

# **Background**

A well owned by your company has just reached final depth after penetration of the target zone, carbonate rocks of the Hunton Group, in the Anadarko Basin. The top of the zone is at 16,303 ft. The well was drilled because subsurface geologic maps indicated an updip fault and a structurally low well that produced gas and water. When the log evaluation is finished, you will make a decision about whether to set casing and test the well for its production potential. If the well is to be tested, then you will be responsible for selecting depths for perforations.

# **Well site information and other pertinent information**

- Logs of this well were correlated with logs of the offset well, which produced gas and water. This well is 40 ft structurally high to the offset well.
- When this well penetrated the Chimneyhill Subgroup of the Hunton Group (Figures 10.30, 10.31), a drilling break was recorded. The penetration rate decreased from 10 min/ft to 5 min/ft, and the mud logger's chromatograph increased by 20 gas units.
- Examination of the bit cuttings showed that this part of the Hunton is dolomite, with minor amounts of chert. The dolomite is gray to gray-brown, medium crystalline, and sucrosic with vuggy porosity.

- Samples collected through the interval of the drilling break did not show evidence of fluorescence or oil-cut.
- Formation temperature, $T_f$, is 221°F; mean surface temperature is 70°F; $R_{mf}$ is 0.249 ohm-m at $T_f$.
- Recoverable volumetric gas reserves are calculated with these parameters:

- drainage area (DA) = 640 acres
- gas gravity = 0.63 (estimated)
- reservoir temperature (estimated) = 221°F
- bottom-hole pressure (BHP, estimated) = 7,260 psi
- recovery factor (RF) = 0.75
- Z factor = 1.165

# **Tasks required for interpretation of the logs**

To complete the calculation of reserves, the following information is needed: porosity ($\phi$), water saturation ($S_w$), and reservoir thickness ($h$).

In deep, hot wells—generally, wells deeper than 12,000 ft—correction of the neutron log usually is required for effects of temperature, and possibly, for effects of pressure. In Chapter 4, the influence of environmental conditions on the neutron log was explained. Of all the conditions, pressure and temperature were described as being the basis for the greatest correction of the neutron log. Also explained was the fact that charts used for correction must correspond to the service company and the type of neutron tool that was used.

A shortcut for computation—which will provide accuracy sufficient for this evaluation—is to determine the amount of correction needed for a high porosity value and a low porosity value in the formation, average the corrections, and apply the average correction to each neutron-log porosity value before using that measurement in additional calculations of porosity. In this well, that correction is +0.015 (an additional 1.5% porosity) to be added to each value of neutron porosity read from the log.

Table 10.11 will help you organize the information. A list of depths is provided, but you are free to determine your own depths for analysis.
<!-- page 236 -->
Log Interpretation Case Studies

225

Table 10.11. Case Study 6: Chimneyhill Subgroup, Hunton Group, Anadarko Basin, U.S.A.: Work table. The symbol "v/v" indicates volume-for-volume decimal fraction.

|  Parameters |   |   |   |   |
| --- | --- | --- | --- | --- |
|  Ann. Mean Surf. Temp: 70°F |   |   |   | Rw (measured):  |
|  Total Depth: 16490 ft |   |   |   | Rw @ fm. temp.:  |
|  Bottom Hole Temp: 222°F |   |   |   | Rmf (measured): 0.70 ohm-m @ 74°F  |
|  Formation Depth: 16320 ft |   |   |   | Rmf @ fm. temp.: 0.249 ohm-m @ 22°F  |
|  Formation Temperature: 221°F |   |   |   |   |
|  a: 1 | m: 2 | n: 2 |  |   |

|  Raw data  |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- |
|  Depth feet | ILD ohm-m | SFL ohm-m | DPHI v/v decimal | NPHI v/v decimal | NPHIc v/v decimal  |
|  16,305 |  |  |  |  |   |
|  16,308 |  |  |  |  |   |
|  16,310 |  |  |  |  |   |
|  16,315 |  |  |  |  |   |
|  16,321 |  |  |  |  |   |
|  16,325 |  |  |  |  |   |
|  16,330 |  |  |  |  |   |
|  16,339 |  |  |  |  |   |
|  16,345 |  |  |  |  |   |
|  16,351 |  |  |  |  |   |
|  16,357 |  |  |  |  |   |
|  16,361 |  |  |  |  |   |
|  16,367 |  |  |  |  |   |
|  16,371 |  |  |  |  |   |
|  16,376 |  |  |  |  |   |
|  16,382 |  |  |  |  |   |
|  16,389 |  |  |  |  |   |
|  16,400 |  |  |  |  |   |
|  16,410 |  |  |  |  |   |
<!-- page 237 -->
226

ASQUITH AND KRYGOWSKI

Table 10.11. Case Study 6: Chimneyhill Subgroup, Hunton Group, Anadarko Basin, U.S.A.: Work table. The symbol "v/v" indicates volume-for-volume decimal fraction. (Cont'd.)

|  Saturation and other calculations  |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- |
|  Depth feet | Phia v/v decimal | Sw v/v decimal | Sxo v/v decimal | BVW | MHI | MOS  |
|  16,305 |  |  |  |  |  |   |
|  16,308 |  |  |  |  |  |   |
|  16,310 |  |  |  |  |  |   |
|  16,315 |  |  |  |  |  |   |
|  16,321 |  |  |  |  |  |   |
|  16,325 |  |  |  |  |  |   |
|  16,330 |  |  |  |  |  |   |
|  16,339 |  |  |  |  |  |   |
|  16,345 |  |  |  |  |  |   |
|  16,351 |  |  |  |  |  |   |
|  16,357 |  |  |  |  |  |   |
|  16,361 |  |  |  |  |  |   |
|  16,367 |  |  |  |  |  |   |
|  16,371 |  |  |  |  |  |   |
|  16,376 |  |  |  |  |  |   |
|  16,382 |  |  |  |  |  |   |
|  16,389 |  |  |  |  |  |   |
|  16,400 |  |  |  |  |  |   |
|  16,410 |  |  |  |  |  |   |
<!-- page 238 -->
Log Interpretation Case Studies

227


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Глубина увеличивается вниз. Шкала глубины: MD (Measured Depth), единицы — футы (Feet), диапазон 16300–16400 футов.

Лог-панель слева:
- Трек 1: SP (спонтанное потенциал)
  - Шкала: -160 мВ до +40 мВ, линейная.
  - Кривая: тонкая сплошная линия.
  - Поведение: отрицательная аномалия в интервале 16300–16400 футов, с плавным уменьшением амплитуды к нижней границе.

Лог-панель справа:
- Трек 2: ILD (длинная индукция, deep resistivity)
  - Шкала: 0,2 до 2000 Ом·м, логарифмическая.
  - Кривая: тонкая сплошная линия.
- Трек 3: ILM (средняя индукция, medium resistivity)
  - Шкала: 0,2 до 2000 Ом·м, логарифмическая.
  - Кривая: пунктирная линия.
- Трек 4: SIL (короткая индукция, shallow resistivity)
  - Шкала: 0,2 до 2000 Ом·м, логарифмическая.
  - Кривая: штрихпунктирная линия.

Интерпретация по кривым:
| Интервал, фут | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|---------------|------------------------|------------------|------------------------------|
| 16300–16400   | Не определена          | SP — отрицательная аномалия; ILD, ILM, SIL — высокие сопротивления, схожие между собой | Вероятно, водоносный или низкопроницаемый пласт; отсутствие фильтрационной зоны (ILD ≈ ILM ≈ SIL) |

Результаты петрофизической интерпретации не указаны.

KEYWORDS: каротаж, SP, ILD, ILM, SIL, сопротивление, глубина, мВ, Ом·м, логарифмическая шкала, аномалия, интерпретация
----


Figure 10.30. Dual induction-SFL with spontaneous potential log and Rxo/Rt curve, Chimneyhill Subgroup, Hunton Group, Anadarko Basin, U.S.A.

Note:

1) In track 1, from 16,300 ft to 16,390 ft, deflection of the Rxo/Rt curve rightward from the SP curve indicates the presence of hydrocarbons.
2) In tracks 2 and 3, from 16,325 ft to 16,370 ft, resistivities are markedly lower than resistivities of strata above and below. This is evidence of a water-bearing zone or of a substantial difference in the type of carbonate rock.
<!-- page 239 -->
228

ASQUITH AND KRYGOWSKI


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: increases downward, units: Feet MD (measured depth), range: 16300 to 16400 ft.

Left track:
- GR (gamma ray): scale 0–150 API, curve is solid line, shows high values (~120–150 API) in upper interval, then decreases to ~40–60 API in lower interval.
- CALI (caliper): scale 6–16 inches, curve is dashed line, shows relatively stable borehole diameter (~8–9 inches) with minor fluctuations.
- BitSize (bit size): scale 6–16 inches, curve is dotted line, appears constant at ~8.5 inches.

Right track:
- DRHO (density log): scale 2.25–0.3 g/cm³, curve is solid line, shows values ~2.3–2.4 g/cm³ in upper interval, then drops to ~2.0–2.1 g/cm³ in lower interval.
- NPHI (neutron porosity): scale 0.3–0.01 (v/v decimal), curve is dashed line, shows low porosity (~0.05–0.10) in upper interval, then increases to ~0.20–0.30 in lower interval.
- DPHI (density porosity): scale 0.3–0.01 (v/v decimal), curve is dotted line, shows low porosity (~0.05–0.10) in upper interval, then increases to ~0.20–0.30 in lower interval.

Interval table:
| Интервал, м | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|-------------|------------------------|-------------------|-------------------------------|
| 16300–16350 | Не определена          | GR: высокие значения (~120–150 API); DRHO: высокие (~2.3–2.4 g/cm³); NPHI/DPHI: низкие (~0.05–0.10) | Вероятно, плотный глинистый слой или известняк |
| 16350–16400 | Не определена          | GR: низкие значения (~40–60 API); DRHO: пониженные (~2.0–2.1 g/cm³); NPHI/DPHI: повышенные (~0.20–0.30) | Вероятно, пористый песчаник или карбонат |

No results panel (Кп, Кн, Кпр, etc.) is visible.

KEYWORDS: каротажная диаграмма, ГК, ПС, ГГК-П, КС, НГК, ННК-Т, плотность, нейтронная пористость, глубина, измеренная глубина, кривые, интервал, литология, интерпретация
----


Figure 10.31. Combination neutron-density lag with gamma ray and caliper, Chimneyhill Subgroup, Hunton Group, Anadarko Basin, U.S.A.

Note:

(1) In Track 1, the decrease in hole diameter on the caliper curve, CALI, from 16,303 ft to 16,384 ft.: In this interval the thick mudcake is evidence of permeable rock.
(2) From 16,303 ft to 16,384 ft, neutron porosity, NPHI, and density porosity, DPHI, are greater than in strata above and below. Also, the neutron and density porosity are approximately equal. Because the Chimneyhill is dolomite, if the rock were water saturated or oil bearing, apparent neutron porosity should be greater than density porosity (the lithology effect of dolomite). This explanation would account for the facts: Because the Chimneyhill is gas bearing, the neutron-density porosities are recorded as being approximately equal; gas effect compensated for the effect of dolomite.
<!-- page 240 -->
Log Interpretation Case Studies 229

## Case Study 6:

### ORDOVICIAN-SILURIAN CHIMNEYHILL SUBGROUP, HUNTON GROUP, ANADARKO BASIN, U.S.A.:

*The Solution.*

#### *Information from logs*

- On the neutron-density log (Figure 10.31) the caliper curve (CALI) shows reduction of hole diameter from 16,303 ft to 16,384 ft, an indication of invasion. Also, the density correction (DRHO) is high over that interval, due to thick mudcake.
- Samples of bit cuttings indicated that the formation is dolomite, but the neutron and density curves are approximately overlain, which is a response suggestive of limestone (Figure 10.31). In dolomite, the neutron log should read more porosity than the density log, but in a gas zone the recorded neutron response tends to be decreased, in some cases to the point of being less than the density reading. The pattern that you are observing probably is that of gas-bearing dolomite. This inference would be in agreement with the well site observation that the mud-logger's instrument detected gas from the formation. (The fact is interesting to note that below the invaded zone, the neutron-density pattern is that of dolomite (Figure 10.31).)
- On the dual induction log (Figure 10.30), The SP shows negative deflection over the invaded interval, but boundaries of the negative salient are poorly defined (a common pattern in carbonate rock). The SP is deflected away from the Rxo/Rt curve by about four chart divisions; this pattern is indicative of the presence of hydrocarbons.
- Resistivities of strata from 16,303 ft to 16,324 ft (Figure 10.30) are greater than resistivities of strata in the underlying zone (16,324 to 16,362 ft) by approximately a factor of 10; from 16,362 ft to 16,384 ft resistivity increases. The pattern could be explained by increase of water saturation in the middle part of the stratigraphic section analyzed, by distinct differences in lithology, or by both.

As the analysis is begun, you decide to define these three zones in the invaded interval, and one zone directly below (from 16,384 ft to 16,412 ft, Figure 10.30), to decide whether differences will affect your

interpretation significantly. You've chosen the zones on the basis of distinct variation in log response. The zones, and provisional explanations of them are:

- Chimneyhill A: 16,303 ft to 16,324 ft (Figures 10.30, 10.31): High resistivity, neutron and density logs almost overlain; perhaps a dolomite response is masked by gas effect.
- Chimneyhill B: 16,324 ft to 16,362 ft: Comparatively low resistivity, neutron and density logs almost overlain and showing approximately the same porosity; possibly a zone of higher water saturation.
- Chimneyhill C: 16,362 ft to 16,384 ft: Porosity slightly greater than that of zone B, but higher resistivity. The higher resistivity is attributed more plausibly to difference in lithology than to lower water saturation—especially in consideration of its lower structural position, and the apparent vertical continuity of porous rock.
- Lower Zone: 16,384 ft to 16,412 ft: Higher resistivity than the zone directly above, but a distinct dolomite response of the porosity logs—low neutron porosity and negative density porosity; tight dolomite, probably with anhydrite (given the density log's excursion into negative porosities).

#### *Calculations and interpretation*

Your first decision is to determine formation water resistivity, $R_w$, from the SP. Connect the apparent shale baselines above and below the Chimneyhill; at about 16,350 ft the SP is approximately -95 mV, as measured from the baseline. By use of formulas in Table 2.1 (or charts in Figures 2.4 and 2.5), $R_w$ is determined as being 0.021 ohm-m.

Next, calculate "apparent" porosity, Phia, by using the equation for neutron-density porosity in a gas zone (Case Study 1, Equation 10.18), with the neutron porosity corrected for temperature and pressure effects. On the basis of the calculated porosity, interpret $R_w$ from the Pickett plot (Figure 10.32) and compare it to $R_w$ calculated from the SP. Scatter of the points makes selection of a slope (from which to determine "m") difficult, but a slope of 2, consistent with "m" of carbonate rocks in general, is a reasonable fit. The Ro line (the line that depicts porosities and resistivities of dolomite at 100% water saturation) is set among the lowest group of points, at porosity of about 4%. (You will find this fact to be interesting: The group of points by which the 100%-water-saturation line is set was recorded from the Chimneyhill B zone,
<!-- page 241 -->
230

ASQUITH AND KRYGOWSKI

rather than the underlying “C” zone. Because the logs show no evidence of a permeability barrier between the zones, a reasonable assumption is that lithology of the “C” zone is markedly different from lithology of zones A and B. Note that most of the points recorded from the highest zone, Chimneyhill A, show evidence of low water saturation.)

$R_w$ determined from the Pickett plot (Figure 10.32) is 0.04 ohm-m at formation temperature, somewhat different from the 0.021 ohm-m calculated from the SP. You decide to use the higher value of $R_w$, based on your confidence in the Pickett plot and the fact that the SP is unreliable in some carbonate-rock environments; also, the SP is affected by hydrocarbons. The choice of 0.04 ohm-m will produce pessimistic results ($S_w$ values will be higher than with an $R_w$ of 0.021), but if the analysis using this value is favorable, you should have more confidence in the production potential of the well.

Using the results of the calculations for porosity and $R_w$, calculate $S_w$ and $S_{xo}$ from the Archie equation (Equations 10.1 and 10.2); then calculate the moveable oil saturation, MOS, moveable hydrocarbon index, MHI, and bulk volume water.

Now, consider the results (Table 10.12): In the Chimneyhill A and B zones (16,303 ft to 16,362 ft), all MHI values are less than 0.7; MOS values are high. The implication of these quantities is that hydrocarbons in zones A and B were moved by invading mud filtrate.

The bulk-volume-water crossplot (Figure 10.33) confirms that the “A” zone is at irreducible water saturation; BVW values are clustered around a line of about 0.008. This fact indicates that the formation is vuggy (Chapter 7, Table 7.1), consistent with the sample descriptions. Some data points of the Chimneyhill C zone lie along the 0.015 line (Figure 10.33), indicating a mix of vuggy and intergranular porosity, but a significant number of points are plotted distant from that line, indicating that the zone would produce water. However, interpretation of the Chimneyhill B zone is indistinct. Some of the points lie along a line of higher BVW (Figure 10.33), perhaps because of a different

lithology, or perhaps the zone is not at irreducible water saturation. Scatter of the points (Figure 10.33), as well as low resistivities, tend to indicate that water would be produced.

Zone A of the Chimneyhill (16,303 ft to 16,324 ft) has several favorable indicators. First, porosity ranges from about 4% to about 9% (Figure 10.31); it is intercrystalline and vuggy. Water saturations and bulk-volume-water values are low (Table 10.12). This evidence supports your decision to set pipe and to perforate the zone. In zone B (16,324 ft to 16,362 ft) water saturations and bulk-volume-water values are higher (Table 10.12); zone B may be water-productive. Because subsurface geologic maps indicate down-dip water, zone B might be avoided in perforating; however, in comparison to zone A, the higher water saturation and bulk-volume-water values of zone B may be due to a distinct difference in lithology. Evidence of different rock is the apparent reduction in vuggy porosity, indicated by the increase in bulk volume water from 16,324 ft to 16,362 ft (Table 10.12). If, in fact, the abrupt transition to lower resistivities in zone B (Table 10.12) is due to diminished vuggy porosity, then zone B may be at irreducible water saturation—zone B may be productive. Unfortunately, with no core to analyze, this explanation could be tested only by perforating the interval from 16,324 ft to 16,362 ft. This decision is made: do not perforate the Chimneyhill B interval.

Estimated recovery of gas is 3.27 BCF. Parameters employed to arrive at this figure are:

- porosity ($\phi$) = 0.06 (6%);
- water saturation ($S_w$) = 0.17 (17%); and
- reservoir thickness ($h$) = 8 ft.

The Chimneyhill was perforated from 16,306 to 16,314 ft with 27 holes. Completion was natural and the calculated open flow (CAOF) of the well was 67,023 mcfgpd; shut-in tubing pressure was 4,639 psi. During the first six months of production, the well produced 0.455 BCF and 2,030 barrels of condensate.

Figure 10.34 shows a computer-processed log of the Chimneyhill interval.
<!-- page 242 -->
Log Interpretation Case Studies

231

Table 10.12. Case Study 6: Chimneyhill Subgroup, Hunton Group, Anadarko Basin, U.S.A.: Solution table. The symbol "v/v" indicates volume-for-volume decimal fraction.

|  Parameters |   |   |   |   |
| --- | --- | --- | --- | --- |
|  Ann. Mean Surf. Temp: 70°F |   |   |   | Rw (measured):ohm-m @ °F  |
|  Total Depth: 16490 ft |   |   |   | Rw @ fm. temp.: 0.04 ohm-m @ 221°F  |
|  Bottom Hole Temp: 222°F |   |   |   | Rmf (measured): 0.70 ohm-m @ 74°F  |
|  Formation Depth: 16320 ft |   |   |   | Rmf @ fm. temp.: 0.249 ohm-m @ 221°F  |
|  Formation Temperature: 221°F |   |   |   |   |
|   | a: 1 | m: 2 | n: 2 |   |

|  Raw data  |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- |
|  Depth feet | ILD ohm-m | SFL ohm-m | DPHI v/v decimal | NPHI v/v decimal | NPHIc v/v decimal  |
|  16,305 | 600 | 610 | 0.000 | 0.035 | 0.050  |
|  16,308 | 600 | 600 | 0.040 | 0.070 | 0.085  |
|  16,310 | 600 | 510 | 0.005 | 0.050 | 0.065  |
|  16,315 | 320 | 320 | 0.065 | 0.075 | 0.090  |
|  16,321 | 500 | 530 | 0.100 | 0.060 | 0.075  |
|  16,325 | 100 | 170 | 0.010 | 0.080 | 0.095  |
|  16,330 | 33 | 60 | 0.045 | 0.060 | 0.075  |
|  16,339 | 70 | 280 | 0.080 | 0.080 | 0.095  |
|  16,345 | 20 | 39 | 0.090 | 0.080 | 0.095  |
|  16,351 | 30 | 63 | 0.035 | 0.040 | 0.055  |
|  16,357 | 15 | 32 | 0.060 | 0.090 | 0.105  |
|  16,361 | 12 | 17 | 0.075 | 0.125 | 0.140  |
|  16,367 | 51 | 90 | 0.010 | 0.060 | 0.075  |
|  16,371 | 43 | 68 | 0.075 | 0.110 | 0.125  |
|  16,376 | 210 | 120 | 0.120 | 0.110 | 0.125  |
|  16,382 | 100 | 100 | 0.090 | 0.110 | 0.125  |
|  16,389 | 170 | 160 | -0.060 | 0.025 | 0.040  |
|  16,400 | 200 | 370 | -0.070 | 0.015 | 0.030  |
|  16,410 | 210 | 330 | -0.035 | 0.010 | 0.025  |
<!-- page 243 -->
232

ASQUITH AND KRYGOWSKI

Table 10.12. Case Study 6: Chimneyhill Subgroup, Hunton Group, Anadarko Basin, U.S.A.: Solution table. The symbol "v/v" indicates volume-for-volume decimal fraction. (Cont'd.)

|  Saturation and other calculations  |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- |
|  Depth feet | Phia v/v decimal | Sw v/v decimal | Sxo v/v decimal | BVW | MHI | MOS  |
|  16,305 | 0.035 | 0.231 | 0.571 | 0.008 | 0.404 | 0.340  |
|  16,308 | 0.066 | 0.123 | 0.306 | 0.008 | 0.401 | 0.183  |
|  16,310 | 0.046 | 0.177 | 0.479 | 0.008 | 0.370 | 0.302  |
|  16,315 | 0.079 | 0.142 | 0.355 | 0.011 | 0.401 | 0.213  |
|  16,321 | 0.088 | 0.101 | 0.245 | 0.009 | 0.413 | 0.144  |
|  16,325 | 0.068 | 0.296 | 0.566 | 0.020 | 0.523 | 0.270  |
|  16,330 | 0.062 | 0.563 | 1.001 | 0.035 | 0.562 | 0.438  |
|  16,339 | 0.088 | 0.272 | 0.339 | 0.024 | 0.802 | 0.067  |
|  16,345 | 0.093 | 0.483 | 0.863 | 0.045 | 0.560 | 0.379  |
|  16,351 | 0.046 | 0.792 | 1.001 | 0.037 | 0.791 | 0.209  |
|  16,357 | 0.086 | 0.604 | 1.001 | 0.052 | 0.603 | 0.397  |
|  16,361 | 0.112 | 0.514 | 1.001 | 0.058 | 0.514 | 0.487  |
|  16,367 | 0.054 | 0.523 | 0.982 | 0.028 | 0.533 | 0.459  |
|  16,371 | 0.103 | 0.296 | 0.587 | 0.030 | 0.504 | 0.291  |
|  16,376 | 0.123 | 0.113 | 0.371 | 0.014 | 0.303 | 0.259  |
|  16,382 | 0.109 | 0.184 | 0.458 | 0.020 | 0.401 | 0.274  |
|  16,389 | -0.010 | 1.001 | 1.001 | 0.000 | 1.000 | 0.000  |
|  16,400 | -0.020 | 0.707 | 1.001 | 0.000 | 0.706 | 0.294  |
|  16,410 | -0.005 | 1.001 | 1.001 | 0.000 | 1.000 | 0.000  |
<!-- page 244 -->
Log Interpretation Case Studies

233


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
- X-axis: Deep induction log, ILD, logarithmic scale, range 1 to 1000 (unit not specified, assumed ohm·m or mΩ·m).
- Y-axis: Apparent porosity, Phi_a, logarithmic scale, range 0.01 to 1.00 (unit: fraction, dimensionless).
- Plot type: Crossplot of apparent porosity vs. deep induction log response.
- Data points: Four distinct datasets, each marked with a different symbol:
  - Solid circle (●): Chimney Hill A
  - Open square (□): Chimney Hill B
  - Solid triangle (▲): Chimney Hill C
  - Star (*): Lower Zone
- Reference lines: Diagonal lines of constant water saturation (Sw), labelled 25, 50, 75, 100 (Sw = 100% corresponds to 100% water saturation).
- Data distribution:
  - Chimney Hill A (●): Clustered near ILD = 100–200, Phi_a = 0.10–0.25, mostly below Sw=50 line.
  - Chimney Hill B (□): Scattered from ILD=10 to 100, Phi_a=0.05 to 0.20, mostly below Sw=50 line.
  - Chimney Hill C (▲): Clustered near ILD=10–50, Phi_a=0.05–0.15, mostly below Sw=50 line.
  - Lower Zone (*): Clustered near ILD=100–200, Phi_a=0.10–0.20, mostly below Sw=50 line.
- Trend: Higher ILD values (lower resistivity) correspond to higher water saturation (Sw), as expected for water-bearing formations. The data points for all zones lie predominantly below the Sw=50% line, indicating generally oil-wet or mixed-wet conditions with significant hydrocarbon saturation.

> Тренд: С увеличением ILD (уменьшением сопротивления) наблюдается рост водонасыщенности Sw; все зоны демонстрируют преимущественно низкую водонасыщенность (Sw < 50%), что указывает на наличие нефти или газа.

KEYWORDS: crossplot, apparent porosity, deep induction log, water saturation, Sw, ILD, hydrocarbon saturation, reservoir evaluation, log interpretation, petrophysics
----


Figure 10.32. Pickett plot, Chimneyhill Subgroup, Hunton Group, Anadarko Basin, U.S.A.

The Ra line (where water saturation is 100%) is interpreted from a group of points from the Chimney Hill B interval (Figure 10.30, at 16,324 ft to 16,362 ft). From the Ra line, Rw is interpreted as 0.04 ohm-m. The Archie cementation exponent, "m," is deduced from the plot as being 2, from measurement of the slope of the line.


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
- X-axis: Apparent porosity, Phi_a, linear scale, range 0.00 to 0.30.
- Y-axis: Water Saturation, S_w, linear scale, range 0.00 to 1.00.
- Data points grouped by zone:
  - ● Chimney Hill A: 15 points, clustered in the lower-left quadrant (Phi_a ≈ 0.02–0.08, S_w ≈ 0.05–0.60), with a concentration near (0.05, 0.15).
  - ○ Chimney Hill B: 30 points, distributed from (Phi_a ≈ 0.05, S_w ≈ 0.40) to (Phi_a ≈ 0.12, S_w ≈ 0.80), forming a broad cloud.
  - ▲ Chimney Hill C: 10 points, mostly in the upper-middle region (Phi_a ≈ 0.07–0.10, S_w ≈ 0.50–0.80).
  - × Lower Zone: 5 points, located at higher porosity and lower saturation (Phi_a ≈ 0.08–0.12, S_w ≈ 0.10–0.30).
- A smooth black curve is drawn through the data, starting at (Phi_a = 0.00, S_w = 1.00) and asymptotically approaching S_w = 0.015 as Phi_a increases.
- The curve passes near the lower envelope of the Chimney Hill A data points and intersects the Lower Zone points.
- The curve is labelled with the value "0.015" at its right end, indicating the residual water saturation asymptote.
> Тренд: С увеличением кажущейся пористости водонасыщенность уменьшается по экспоненциальному закону, приближаясь к асимптоте S_w = 0.015.
KEYWORDS: водонасыщенность, кажущаяся пористость, кривая насыщения, зоны Chimney Hill, Lower Zone, экспоненциальная зависимость, S_w, Phi_a
----


Figure 10.33. Bulk-volume-water (BVW) crossplot (porosity, Phia vs. water saturation, Sw), Chimneyhill Subgroup, Hunton Group, Anadarko Basin, U.S.A.
<!-- page 245 -->
234

ASQUITH AND KRYGOWSKI


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Глубина увеличивается вниз. Диапазон глубин: 16300–16400 футов (MD).

Треки слева направо:

1. **GR (Гамма-каротаж)**:
   - Шкала: 0–160 API (внизу), 0–100 API (вверху)
   - Единицы: API
   - Кривая: сплошная линия, показания снижаются с 16300 до 16400 футов, затем резко возрастают к 16400 футам.

2. **SP (Потенциал самопроизвольный)**:
   - Шкала: -160 до +40 мВ
   - Единицы: мВ
   - Кривая: пунктирная линия, показывает отрицательную аномалию в интервале 16300–16400 футов, с плавным уменьшением амплитуды к концу интервала.

3. **ILD (Индукционный каротаж, глубокий)**:
   - Шкала: 0,2–2000 ом·м
   - Единицы: ом·м
   - Кривая: сплошная линия, показания резко возрастают в интервале 16300–16350 футов, затем снижаются до 16400 футов.

4. **SFL (Индукционный каротаж, поверхностный)**:
   - Шкала: 0,2–2000 ом·м
   - Единицы: ом·м
   - Кривая: пунктирная линия, поведение аналогично ILD, но с меньшими значениями; отклонение от ILD указывает на инвазию.

5. **Sw (Обводнённость породы)**:
   - Шкала: 0–1 (десятичные дроби)
   - Единицы: десятичные дроби
   - Кривая: сплошная линия, показывает снижение Sw с 16300 до 16350 футов, затем рост к 16400 футам.

6. **BVW (Объёмная влажность)**:
   - Шкала: 0–0,25 (десятичные дроби)
   - Единицы: десятичные дроби
   - Кривая: сплошная линия, показывает рост BVW с 16300 до 16350 футов, затем снижение к 16400 футам.

7. **Phin (Пористость по нейтронному каротажу)**:
   - Шкала: 0–0,25 (десятичные дроби)
   - Единицы: десятичные дроби
   - Кривая: штрихпунктирная линия, показывает снижение пористости с 16300 до 16350 футов, затем рост к 16400 футам.

8. **Фильтр (черно-белый столбик)**:
   - Шкала: 0–0,25 (десятичные дроби)
   - Единицы: десятичные дроби
   - Визуализация: черно-белый столбик, где черный цвет соответствует высоким значениям (возможно, водонасыщенность или пористость), белый — низким. В интервале 16300–16350 футов — черный, затем постепенно светлеет к 16400 футам.

Интервальные таблица:

| Интервал, фут | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|---------------|------------------------|-------------------|-------------------------------|
| 16300–16350   | Не определена          | GR: снижается, SP: отрицательная аномалия, ILD/SFL: рост, Sw: снижается, BVW/Phin: рост | Возможный коллектор с высокой пористостью и низкой водонасыщенностью |
| 16350–16400   | Не определена          | GR: резко растёт, SP: аномалия уменьшается, ILD/SFL: снижаются, Sw: растёт, BVW/Phin: снижаются | Переход в менее проницаемые породы, возможно, глина или аргиллит |

Результаты петрофизической интерпретации не указаны.

KEYWORDS: каротаж, ГК, ПС, ИК, ILD, SFL, Sw, BVW, Phin, пористость, водонасыщенность, коллектор, глубина, фут
----


Figure 10.34. Chimneyhill Subgroup, Hunton Group, Anadarko Basin, U.S.A. Computer-processed log.

Track 1 shows the SP curve and the gamma ray curve.

Track 2 shows the deep induction log and the spherically focused log.

Track 3 shows Archie water saturation, calculated from apparent (corrected) porosity. Also shown in track 3 are apparent porosity and bulk volume water. The dark shaded area between the porosity curve (left-hand) and the bulk-volume-water curve indicates the proportion of pore space that is occupied by gas. The light-shaded area between the bulk-volume-water curve and the right-hand margin of the track (scale value of zero) indicates the proportion that is occupied by water.
<!-- page 246 -->
Log Interpretation Case Studies 235

# Case Study 7:

# **PENNSYLVANIAN CANYON LIMESTONE, NEW MEXICO, U.S.A.:**

# *The Problem.*

This case study illustrates the advantage of having a measurement of lithology that is largely independent of porosity and fluid saturation: the photoelectric effect (Pe) from the spectral density log. Because this case study is the final one of the sequence, the interpretation is left largely up to the reader to plan and complete. As with the other case studies, solutions are provided for validation of the reader's efforts.

If you decide to make an invasion correction of the dual laterolog, this equation will provide accuracy that is sufficient for this case study:

$$R_t = (2 \times LLD) - LLS \tag{10.43}$$

# **Background**

In the late 1990s an independent oil company drilled a 7150-ft well in southeastern New Mexico that

penetrated Precambrian basement. The well was drilled on a small faulted anticline. After the well was at total depth (TD), it was logged with this saltwater-mud logging suite: Dual Laterolog-Rxo and Gamma Ray-Neutron-Spectral Density (Figure 10.35). Your task is to determine whether the zone is potentially productive, and if so, how much hydrocarbon is in place.

# **Well site information and other pertinent information**

These facts pertain to the porous Canyon zone from 6758 to 6772 ft (Figure 10.35):

- The neutron and density porosities (PHIN and PHID, respectively) are quantified with reference to limestone.
- From samples of bit cuttings, the zone was described as light tan to gray ooid grainstone with abundant oomoldic porosity.
- $R_w = 0.03$ ohm-m at formation temperature.
- $R_{mf} = 0.0406$ ohm-m at formation temperature.

The Work Table, Table 10.13, shows depths of zones suggested for interpretation; entries in the Solution Table (Table 10.14) are based on these depths.

Table 10.13. Canyon Sandstone, New Mexico, U.S.A.: Work table. The symbol "v/v" indicates volume-for-volume decimal fraction.

|  Parameters |   |   |   |   |
| --- | --- | --- | --- | --- |
|  Rw (measured): 0.03 ohm-m @ Tf |   |   |   | Rmf @ fm. temp.: 0.041 ohm-m @ Tf  |
|   | a: 1 | m: 2 | n: 2 |   |

|  Data  |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- |
|  Depth feet | LLD ohm-m | LLS ohm-m | MSFL ohm-m | Pe b/electron | PHID v/v decimal | PHIN v/v decimal  |
|  6760 |  |  |  |  |  |   |
|  6763 |  |  |  |  |  |   |
|  6768 |  |  |  |  |  |   |

|  Calculations  |   |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  Depth feet | Rt ohm-m | PhiNDgas v/v decimal | Swa v/v decimal | Sxo v/v decimal | Swr v/v decimal | MHI | BVW  |
|  6760 |  |  |  |  |  |  |   |
|  6763 |  |  |  |  |  |  |   |
|  6768 |  |  |  |  |  |  |   |
<!-- page 247 -->
236

ASQUITH AND KRYGOWSKI


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: increases downward, units: Feet MD (measured depth), visible range: approximately 6800–6900 ft.

Track 1 (leftmost):
- Curve: GR (Гамма-каротаж)
- Scale: 0–100 API
- Line style: solid black line
- Curve behaviour: shows multiple peaks and troughs; notable high-amplitude peaks at ~6805 ft, ~6820 ft, ~6835 ft, ~6850 ft, ~6870 ft, ~6890 ft; low-amplitude zones between peaks.

Track 2 (rightmost group, leftmost within group):
- Curves: LLD (Deep Laterolog), LLS (Shallow Laterolog), MSFL (MicroSpherically Focused Log)
- Scale: 0.2–2000 ohm·m (for LLD and LLS), 0.2–2000 ohm·m (for MSFL)
- Line styles: LLD — solid line; LLS — dashed line; MSFL — dash-dot line
- Curve behaviour: 
  - LLD: relatively smooth, high-resistivity zones (~1000–2000 ohm·m) at ~6805–6815 ft, ~6830–6840 ft, ~6855–6865 ft, ~6880–6890 ft; low-resistivity zones (~100–200 ohm·m) between.
  - LLS: similar to LLD but with slightly lower values and more noise; shows invasion effects in low-resistivity zones.
  - MSFL: closely follows LLS, indicating shallow invasion; shows high-resistivity zones in same intervals as LLD/LLS.

Track 3 (rightmost group, rightmost within group):
- Curves: Pe (Photoelectric Factor), PHID (Density Porosity), PHIN (Neutron Porosity)
- Scale: Pe — 0–10 b/e (barns/electron); PHID — 0.3–0.01 (fractional porosity); PHIN — 0.3–0.01 (fractional porosity)
- Line styles: Pe — solid line; PHID — dashed line; PHIN — dash-dot line
- Curve behaviour:
  - Pe: relatively flat at ~4–5 b/e, with slight increases in high-resistivity zones.
  - PHID: low values (~0.1–0.2) in high-resistivity zones, higher values (~0.2–0.3) in low-resistivity zones.
  - PHIN: similar to PHID, but slightly higher in low-resistivity zones, indicating possible gas effect or lithology difference.

Interval table:
| Интервал, ft | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|--------------|--------------------------|-------------------|-------------------------------|
| 6800–6815    | Песчаник (по высокой резистивности и низкой пористости) | LLD/LLS/MSFL: высокие значения (~1000–2000 ohm·m); PHID/PHIN: низкие (~0.1–0.2); Pe: ~4–5 | Вероятно, водонасыщенный песчаник |
| 6815–6830    | Глина/аргиллит (по высокой ГК и низкой резистивности) | GR: высокие значения (~80–100 API); LLD/LLS/MSFL: низкие (~100–200 ohm·m); PHID/PHIN: высокие (~0.2–0.3) | Глинистый интервал |
| 6830–6840    | Песчаник | LLD/LLS/MSFL: высокие (~1000–2000 ohm·m); PHID/PHIN: низкие (~0.1–0.2); Pe: ~4–5 | Водонасыщенный песчаник |
| 6840–6855    | Глина/аргиллит | GR: высокие; LLD/LLS/MSFL: низкие; PHID/PHIN: высокие | Глинистый интервал |
| 6855–6865    | Песчаник | LLD/LLS/MSFL: высокие; PHID/PHIN: низкие; Pe: ~4–5 | Водонасыщенный песчаник |
| 6865–6880    | Глина/аргиллит | GR: высокие; LLD/LLS/MSFL: низкие; PHID/PHIN: высокие | Глинистый интервал |
| 6880–6890    | Песчаник | LLD/LLS/MSFL: высокие; PHID/PHIN: низкие; Pe: ~4–5 | Водонасыщенный песчаник |
| 6890–6900    | Глина/аргиллит | GR: высокие; LLD/LLS/MSFL: низкие; PHID/PHIN: высокие | Глинистый интервал |

No results panel (Кп, Кн, Кпр, etc.) is visible.

KEYWORDS: well log, ГК, ПС, ГГК-П, резистивиметрия, плотностная каротаж, нейтронный каротаж, интерпретация, песчаник, глина
----


Figure 10.35. Dual laterolog-Rxo. Canyon Limestone, New Mexico, U.S.A. Vertical scale: 2 ft per chart division. Gamma ray curve scaled in API units. Resistivity curves scaled in ohms-m. Density porosity and neutron porosity scaled in porosity units, 0.04 per chart division.

Dual laterolog-Rxo. Canyon Limestone, New Mexico, U.S.A.

In the interval 6758 to 6772 ft note the following facts:

1. The dual laterolog exhibits a salt-mud hydrocarbon invasion profile. (See Chapter 1, Figure 1.5 for an example.)
2. The neutron and density porosity curves show crossover (φ d > φ n) in the zone described from cutting samples as limestone; the crossover is indicative of the presence of gas.
3. Average value of the Pe curve is about 5, which confirms that the zone is limestone.
<!-- page 248 -->
Log Interpretation Case Studies

237

### Case Study 7:

### PENNSYLVANIAN CANYON LIMESTONE, NEW MEXICO, U.S.A.:

### The Solution.

From Figure 10.35 the following attributes of the Canyon interval (6758 to 6772 ft) can be discerned:

- The dual laterolog shows a profile consistent with invasion in a hydrocarbon-bearing zone.
- Neutron porosity is less than the density porosity (“crossover”). Because the formation is described as a limestone, and because the porosity curves are referenced to limestone, one would expect the porosity curves to be overlain directly if the formation were liquid-filled (oil or water). The crossover indicates gas in the formation.
- The Pe curve averages about 5 units, confirming that the zone is limestone, and that the neutron-density crossover is a pore-fluid effect (i.e. gas).

The following conclusions should be drawn from your calculations:

- The zone is porous, with gas-zone, neutron-density porosity (Equation 10.18) showing from 0.10 to 0.18 (10 to 18 %) (Table 10.14).
- Archie water saturations (Equation 10.1) range from 0.07 to 0.12 (7 to 12 %).
- Estimates of bulk volume water, BVW (Figure 10.36, and Table 10.14) range between 0.011 and 0.013; they are below the carbonate cutoff value of 0.015 (Chapter 7, Table 7.1), indicating

that the formation should produce water-free.

- The values for moveable hydrocarbon index (MHI) are under the carbonate cutoff of 0.6, also indicating that the Canyon should produce hydrocarbons.
- The Archie water saturation values ($S_{wa}$) are less than the ratio water saturation values ($S_{wr}$)—which is expected—because porosity of the Canyon zone is oomoldic (see pg. 117), as described from inspection of the bit-cutting samples.

The Canyon was perforated from 6760 to 6770 ft; initial potential flowing (IPF) was 918 mcfgpd plus 3 bopd and NO water. If you assume that this well will drain 160 acres, the original gas in place (OGIP), estimated from the equation below (from Equation 10.12), is 1.74 BCF (billion cubic feet).

$$OGIP = 43,560 \times PhiNDgas \times (1 - S_w) \times thickness \times ((0.43 \times depth)/14.7) \times area$$

where:

- $PhiNDgas = 0.14$ (average)
- $S_w = 0.10$ (average)
- thickness = 10 ft
- depth = 6766 ft (average)
- area = 160 acres

With the average recovery factor for this formation in this area of 0.70 (70%), the well could produce 1.21 bcf of gas. At a price of $2.00 per mcf, the production would be worth approximately $2,400,000.

See the sample calculations in Table 10.14, and results computed from samples spaced at one-half-foot intervals, shown in Figure 10.37.
<!-- page 249 -->
238

ASQUITH AND KRYGOWSKI

Table 10.14. Case Study 7: Canyon Sandstone, New Mexico, U.S.A.: Solution table. The symbol "v/v" indicates volume-for-volume decimal fraction.

|  Parameters |   |   |   |   |
| --- | --- | --- | --- | --- |
|  Rw (measured): 0.03 ohm-m @ Tf |   |   |   | Rmf @ fm. temp.: 0.041 ohm-m @ Tf  |
|   | a: 1 | m: 2 | n: 2 |   |

|  Data  |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- |
|  Depth feet | LLD ohm-m | LLS ohm-m | MSFL ohm-m | Pe b/electron | PHID v/v decimal | PHIN v/v decimal  |
|  6760 | 170 | 150 | 80 | 5.0 | 0.135 | 0.050  |
|  6763 | 200 | 130 | 40 | 4.6 | 0.125 | 0.065  |
|  6768 | 130 | 95 | 35 | 4.9 | 0.230 | 0.115  |

|  Calculations  |   |   |   |   |   |   |   |
| --- | --- | --- | --- | --- | --- | --- | --- |
|  Depth feet | Rt ohm-m | PhiNDgas v/v decimal | Swa v/v decimal | Sxo v/v decimal | Swr v/v decimal | MHI | BVW  |
|  6760 | 190 | 0.102 | 0.123 | 0.222 | 0.479 | 0.555 | 0.013  |
|  6763 | 270 | 0.100 | 0.106 | 0.321 | 0.249 | 0.329 | 0.011  |
|  6768 | 165 | 0.182 | 0.074 | 0.188 | 0.312 | 0.394 | 0.013  |
<!-- page 250 -->
Log Interpretation Case Studies

239


----
━━━ FORMAT 6: XY PLOT / CHART WITH DATA ━━━
- X-axis: Porosity, PhiNDgas, linear scale, range 0.00 to 0.30.
- Y-axis: Archie water saturation, Swa, linear scale, range 0.00 to 0.60.
- Data points: 14 black dots plotted at the following approximate coordinates (x, y):
  (0.00, 0.60), (0.00, 0.40), (0.00, 0.38), (0.04, 0.20), (0.05, 0.18), (0.06, 0.15), (0.07, 0.14), (0.08, 0.13), (0.09, 0.12), (0.10, 0.11), (0.11, 0.10), (0.13, 0.09), (0.17, 0.07), (0.20, 0.015).
- Fitted curve: smooth black curve passing through the data points, starting at (0.00, 0.60) and asymptotically approaching Swa = 0.015 as porosity increases.
- The curve is labeled at its right end with the value "0.015" on the y-axis, indicating the asymptotic minimum water saturation.
- The plot shows a strong inverse relationship between porosity and water saturation, with Swa decreasing rapidly at low porosities and leveling off at higher porosities.

> Тренд: С увеличением пористости (PhiNDgas) водонасыщенность (Swa) по закону Арчи уменьшается, асимптотически приближаясь к значению 0.015.

KEYWORDS: Archie water saturation, porosity, PhiNDgas, Swa, crossplot, inverse relationship, asymptote, petrophysics, log interpretation, saturation model
----


Figure 10.36. Bulk-volume-water (BVW) plot, Canyon Limestone, New Mexico, U.S.A.


----
━━━ FORMAT 2: WELL LOG / КАРОТАЖНАЯ ДИАГРАММА ━━━
Depth axis: increases downward, units: feet (MD), range: 0 to 6800 ft.

Left panel (tracks 1–3):
- Track 1: Pe (photoelectric effect), scale: 0–100, unit: arbitrary units (no explicit unit given), curve: solid line.
- Track 2: GR (gamma ray), scale: 0–100, unit: API, curve: solid line.
- Track 3: APT (acoustic travel time), scale: 0–100, unit: μs/ft, curve: solid line.
- Track 4: Resistivity (not labelled, but appears as dashed line), scale: 0–100, unit: ohm·m (inferred from context), curve: dashed line.

Right panel (tracks 5–8):
- Track 5: Rt (true resistivity), scale: 0–62, unit: ohm·m, curve: solid line.
- Track 6: LLD (deep laterolog), scale: 0–62, unit: ohm·m, curve: solid line.
- Track 7: Swa (water saturation), scale: 0–1.0, unit: decimal, curve: solid line.
- Track 8: PhiNDgas (porosity from neutron-density, gas-corrected), scale: 0–0.3, unit: decimal, curve: solid line.
- Track 9: RvW (resistivity of water), scale: 0–0.03, unit: ohm·m, curve: solid line.

Interpreted intervals (based on curve behaviour and marked boundaries):
| Интервал, ft | Литология (по колонке) | Кривые: поведение | Интерпретация (если подписана) |
|--------------|-------------------------|-------------------|------------------------------|
| 0–6800       | Не определена           | Pe: колебания; GR: колебания; APT: колебания; Rt: колебания; LLD: колебания; Swa: колебания; PhiNDgas: колебания; RvW: колебания | Нет явной интерпретации на диаграмме |

No perforation intervals, fluid contacts, or results panel (Кп, Кн, Кпр) are marked.

KEYWORDS: well log, ГИС, Pe, GR, APT, Rt, LLD, Swa, PhiNDgas, RvW, depth, feet, resistivity, porosity, water saturation, photoelectric effect, gamma ray, acoustic travel time
----


Figure 10.37. Canyon Limestone, New Mexico, U.S.A. Computer-processed log.

Note:

1. True formation resistivity, Rt, calculated from LLD and LLS, is shown in Track 2 with the deep laterolog, LLD.
2. Archie water saturation, Swa, is shown as the light-shaded area from Swa = 1.0, on the left-hand side of Track 3.
3. Hydrocarbon-filled pore space is shown as the dark shaded area on the right-hand side of Track 3, between the porosity, PhiNDgas, and the bulk volume water, BVW. Water-filled pore space is shown as the light shaded area between BVW and the right-hand margin of the track (scale value of zero).
<!-- page 251 -->
240

ASQUITH AND KRYGOWSKI

# References

Adams, J., L. Bourke, and R. Frisinger, 1987, Strategies for dipmeter interpretation: Part 2: The Technical Review, v. 35, p. 20–31.

Alger, R. P., 1980, Geological use of wireline logs (p. 207–222) in G. D. Hobson, ed., Developments in Petroleum–2: London, Applied Science Publishers, Ltd., 345 p.

Al-Waheed, H. H., T. M. Audah, and C. Cao Minh, 1994, Application of the azimuthal resistivity imager tool in Saudi Arabia: Society of Petroleum Engineers, Annual Conference and Exhibition, p. 811–818, paper SPE-28439.

Akkurt, R., D. Mardon, J. S. Gardner, D. M. Marschall, and F. Solanet, 1998, Enhanced diffusion: expanding the range of NMR direct hydrocarbon-typing applications: Society of Professional Well Log Analysts, 39th Annual Logging Symposium, Transactions, paper GG.

Archie, G. E., 1942, The electrical resistivity log as an aid in determining some reservoir characteristics: Journal of Petroleum Technology, v. 5, p. 54–62.

Asquith, G. B., 1979, Subsurface carbonate depositional models: a concise review: Tulsa, Oklahoma, PennWell Books, 121 p.

Asquith, G. B., 1980, Log analysis by microcomputer: Tulsa, Oklahoma, PennWell Books, 105 p.

Asquith, G. B., 1991, Log Evaluation of Shaly Sandstone Reservoirs: A Practical Guide: AAPG Course Notes Series, no. 31, 59 p.

Barber, T. D., 1983, Introduction to the Phasor dual induction tool; Society of Petroleum Engineers, 58th Annual Technical Conference, paper SPE-12049.

Barton, C. A., D. Moos, P. Peska, and M. D. Zoback, 1997, Utilizing wellbore image data to determine the complete stress tensor: Application to permeability anisotropy and wellbore stability: The Log Analyst, v. 38, p. 21–33.

Bassiouni, Z., 1994, Theory, Measurement, and Interpretation of Well Logs: Richardson, Texas, Society of Petroleum Engineers, 372 p.

Bateman, R. M., and C. E. Konen, 1977, The log analyst and the programmable pocket calculator: The Log Analyst, v. 18, p. 3–11.

Bell, J. S., and D. I. Gough, 1979, Northeast-southwest compressive stress in Alberta: Evidence from oil wells: Earth and Planetary Science Letters, v. 45, p. 475–482.

Bengsten, C. A., 1981, Statistical curvature analysis techniques for structural interpretation of dipmeter data: AAPG Bulletin, v. 65, p. 312–332.

Bengsten, C. A., 1982, Structural and stratigraphic uses of dip profiles in petroleum exploration, in M. T. Halbouty (ed.), The Deliberate Search for the Subtle Trap: AAPG Memoir 32, p. 31–45.

Berg, C. R., 1998, Synthetic deviation: A new dipmeter interpretation method: AAPG Bulletin, v. 82, p. 1133–1139.

Bigelow, E. L., 1985a, Making more intelligent use of log derived dip information. Part 1, Suggested guidelines: The Log Analyst, v. 26, no. 1, p. 41–53.

Bigelow, E. L., 1985b, Making more intelligent use of log derived dip information. Part 2, Well site data gathering considerations: The Log Analyst, v. 26, no. 2, p. 25–41.

Bigelow, E. L., 1985c, Making more intelligent use of log derived dip information. Part 3, Computer processing considerations: The Log Analyst, v. 26, no. 3, p. 18–31.

Bigelow, E. L., 1985d, Making more intelligent use of log derived dip information. Part 4, Structural interpretation: The Log Analyst, v. 26, no. 4, p. 21–43.

Bigelow, E. L., 1985e, Making more intelligent use of log derived dip information. Part 5, Stratigraphic interpretation: The Log Analyst, v. 26, no. 5, p. 25–64.

Bonner, S., M. Fredette, J. Lovell, B. Montaron, R. Rosthal, J. Tabanou, P. Wu, B. Clark, R. Mills, R. Williams, 1996, Resistivity while drilling—images from the string: Schlumberger Oilfield Review, v. 8, no. 1, p. 4–19.

Bornemann, E., T. Bourgeois, K. Bramlett, K. Hodenfield, and D. Maggs, 1998, The application and accuracy of geological information from a logging-while-drilling density tool: Society of Professional Well Log Analysts, 39th Annual Logging Symposium, Paper L, 14 p.

Bourke, L. T., P. Delfiner, J. C. Trouiller, T. Fett, M. Grace, S. Luthi, O. Serra, and E. Standen, 1989, Using Formation MicroScanner images: The Technical Review, v. 37, no. 1, p. 16–40.

Bourke, L. T., 1992, Sedimentological borehole image analysis in clastic rocks: A systematic approach to interpretation, in A. Hurst, C. M. Griffiths, and P. F. Worthington (eds.), Geological Applications of Wireline Logs II: London, The Geological Society, Special Publication 65, p. 31–42.

Brown, S. R., 1987, Fluid flow through rock joints: The effect of surface roughness: Journal of Geophysical Research, v. 92, no. B2, p. 1337–1347.
<!-- page 252 -->
References

241

Buckles, R. S., 1965, Correlating and averaging connate water saturation data, Journal of Canadian Petroleum Technology, v. 9, no. 1, p. 42–52.

Carothers, J. E., 1968, A statistical study of the formation factor relation to porosity: The Log Analyst, v. 9, p. 38–52.

Carothers, J. E., and C. R. Porter, 1970, Formation factor-porosity relation from well log data, Society of Professional Well Log Analysts, 11th Annual Logging Symposium, Transactions, paper D.

Carr, D. L., R. A. Johns, R.Y. Elphick, and L. S. Foulk, 1997, High-resolution reservoir characterization of midcontinent sandstones using wireline resistivity imaging, Boonsville (Bend Conglomerate) gas field, Fort Worth Basin, Texas: The Log Analyst, v. 38, no. 6, p. 54–70.

Clavier, C., G. Coates, and J. Dumanoir, 1977, Theoretical and experimental bases for the dual-water model for interpretation of shaly sands: Society of Petroleum Engineers, Annual Meeting, paper SPE-6859.

Clavier, C., W. R. Hoyle, and D. Meunier, 1971, Quantitative interpretation of thermal neutron decay time logs: Part 1. Fundamentals and techniques: Journal of Petroleum Technology, v. 23, p. 743–755.

Coates, G., and J. L. Dumanoir, 1973, A new approach to improve log-derived permeability: Society of Professional Well Log Analysts, 14th Annual Logging Symposium, Transactions, paper R.

Coates, G. R., L. Xiao, and M. G. Prammer, 1999, NMR Logging Principles and Applications: Houston, Texas, Halliburton Energy Services, 232 p.

Cobb, C. C., and P. K. Schultz, 1992, Real-time electro-fiber-optic downhole video system: presented at the Offshore Technology Conference, Houston, TX, p. 575–582, paper SPE 25137.

Davies, D. H., O. Faivre, M-T. Gounot, B. Seeman, J-C. Troullier, D. Benimeli, A. E. Ferreira, D. J. Pittman, J-W. Smits, M. Randrianavony, B. I. Anderson, and J. Lovell, 1992, Azimuthal resistivity imaging—a new generation laterolog: Society of Petroleum Engineers, Annual Conference and Exhibition, p. 143–153, SPE-24676.

Dewan, J., 1983, Essentials of Modern Open-Hole Log Interpretation: Tulsa, Oklahoma, PennWell Publishing Company, 361 p.

Doll, H. G., 1948, The SP log, theoretical analysis and principles of interpretation: Transactions, AIME, v. 179, p. 146–185.

Dresser Atlas, 1974, Log Review 1: Houston, Texas, Dresser Industries, Inc.

Dresser Atlas, 1975, Log interpretation fundamentals: Houston, Texas, Dresser Industries, Inc.

Dresser Atlas, 1979, Log interpretation charts: Houston, Texas, Dresser Industries, Inc., 107 p.

Dresser Atlas, 1981, Spectralog, Houston, Texas, Dresser Industries, Inc.

Ekstrom, M. P., C. A. Dahan, M. Chen, P. M. Lloyd, and D. J. Rossi, 1986, Formation imaging with microelectrical scanning arrays: Society of Professional Well Log Analysts, 27th Annual Logging Symposium, Transactions, Paper BB, 21 p.

Ellis, D. V., 1987, Well Logging for Earth Scientists: New York, Elsevier, 532 p.

Fertl, W. H., 1975, Shaly sand analysis in development wells, Society of Professional Well Log Analysts, 16th Annual Logging Symposium Transactions, Paper A.

Fertl, W. H., 1978, Rwa Method-fast formation evaluation, in Practical log analysis-8: Oil and Gas Journal, v. 76, no. 37, p. 73–76.

Fertl, W. H., and W. C. Vercellino, 1978, Predict water cut from well logs, in Practical log analysis-4: Oil and Gas Journal, v. 76, no. 25, p. 111–116.

Gilbreath, J. A., 1987, Strategies for dipmeter interpretation: Part I: The Technical Review, v. 35, no. 3, p. 28–41.

Grace, L. M., and B. Newberry, 1998, Geological applications of electrical images and dipmeter: Short Course Notes, Schlumberger Oilfield Services, v. 8.1.

Guillotte, J. G., J. Schrank, and E. Hunt, 1979, Smackover reservoir: interpretation case study of water saturation versus production: Gulf Coast Association of Geological Societies, Transactions, v. 29, p. 121–126.

Halliburton Energy Services, 1994, Log Interpretation Charts (third printing): Houston, Texas, Halliburton Company.

Halliburton, 1996, Downhole video services: Applications and well preparation: Best Practices Series, Document H00023, Houston, Texas, Halliburton Company, 20 p.

Haws, G. W., and N. F. Hurley, 1992, Applications of pressure-interference data in reservoir characterization studies, Big Horn basin, Wyoming: Society of Petroleum Engineers, Annual Conference and Exhibition, p. 53–62, paper SPE 24668.

Hearst, J. R., P. H. Nelson, and F. L. Paillet, 2000, Well Logging for Physical Properties (second edition): Chichester, England, John Wylie and Sons, 106 p.

Heffer, K. J., and J. C. Lean, 1993, Earth stress orientation—a control on, and guide to, flooding directionality in a majority of reservoirs: in W. Linville
<!-- page 253 -->
242

ASQUITH AND KRYGOWSKI

(ed.), Reservoir Characterization III, Tulsa, Oklahoma, PennWell, p. 799–822.

Hilchie, D. W., 1978, Applied openhole log interpretation: Golden, Colorado, D. W. Hilchie, Inc., 309 p.

Hilchie, D. W., 1979, Old electric log interpretation: Golden, Colorado, D. W. Hilchie, Inc., 161 p.

Hilchie, D. W., 1982, Advanced Well Log Interpretation: Golden, Colorado, D. W. Hilchie, Inc., 300 p.

Hingle, A. T., 1959, The use of logs in exploration problems: Society of Exploration Geophysicists, 29th Meeting.

Höcker, C., K. M. Eastwood, J. C. Herweijer, and J. T. Adams, 1990, Use of dipmeter data in clastic sedimentological studies: AAPG Bulletin, v. 74, p. 105–118.

Hurley, N. F., 1994, Recognition of faults, unconformities, and sequence boundaries using cumulative dip plots: AAPG Bulletin, v. 78, p. 1173–1185.

Hurley, N. F., D. R. Thorn, J. L. Carlson, and S. L. W. Eichelberger, 1994, Using borehole images for target zone evaluation in horizontal wells: AAPG Bulletin, v. 78, p. 238–246.

Hurley, N. F., 1996, Parasequence-scale stratigraphic correlations in deep-marine sediments using borehole images, in J. A. Pacht, R. E. Sheriff, and R. F. Perkins (eds.), Stratigraphic Analysis Utilizing Advanced Geophysical, Wireline, and Borehole Technology for Petroleum Exploration and Production: Gulf Coast Section SEPM, 17th Annual Research Conference, p. 147–152.

Hurley, N. F., R. A. Zimmermann, D. Pantoja, 1998, Quantification of vuggy porosity in a dolomite reservoir from borehole images and core, Dagger Draw Field, New Mexico: Society of Petroleum Engineers, Annual Conference and Exhibition, 14 p., paper SPE 49323.

Jaafar, I. B., 1980, Depositional and diagenetic history of the B-zone of the Red River Formation (Ordovician) of the Beaver Creek Field, Golden Valley County, North Dakota: M.S. thesis, West Texas State University, Canyon, Texas, 68 p.

Knight, C. N., 1999, Structural and stratigraphic controls on Mesaverde reservoir performance: North La Barge field, Sublette County, Wyoming: Unpublished Ph.D. dissertation, Colorado School of Mines, Golden, Colorado, 217 p.

Kobesh, F. P. and R. B. Blizard, 1959, Geometric factors in sonic logging: Geophysics, v. 24, p. 64–76.

Koepsell, R. J., F. E. Jenson, and R. L. Langley, 1989a, Formation imaging—1, Formation imaging yields precise fault orientation, minimizes dry offsets: Oil & Gas Journal, v. 87, no. 49, p. 55–58.

Koepsell, R. J., F. E. Jenson, and R. L. Langley, 1989b, Formation imaging—2, Imaging aids visualization of faults: Oil & Gas Journal, v. 87, no. 50, p. 85–86.

Lacazette, A., 1996, The STAR (SimulTaneous Acoustic and Resistivity) Imager: London Petrophysical Society, Borehole Imaging Seminar, 3 p.

Larionov, V. V., 1969, Borehole Radiometry: Moscow, U.S.S.R., Nedra.

Lau, J. S. O., L. F. Auger, and J. G. Bisson, 1987, Subsurface fracture surveys using a borehole television camera and acoustic televiewer: Canadian Geotechnical Journal, v. 24, p. 499–508.

Logan, W. D., J. P. Horkowitz, R. Laronga, and D. Cromwell, 1997, Practical application of NMR logging in carbonate reservoirs: Society of Petroleum Engineers, Annual Technical Conference and Exhibition, Proceedings (Formation evaluation and reservoir geology), p. 203–215, Paper SPE 38740.

Luthi, S. M., and J. R. Banavar, 1988, Application of borehole images to three-dimensional geometric modeling of eolian sandstone reservoirs, Permian Rotliegende, North Sea: AAPG Bulletin, v. 72, p. 1074–1089.

Luthi, S. M., and P. Souhaite, 1990, Fracture apertures from electrical borehole scans: Geophysics, v. 55, p. 821–833.

Maute, R. E., 1992, Electrical Logging: State-of-the-Art: The Log Analyst, v. 33, p. 206–227.

Martin, A. J., S. T. Solomon, and D. J. Hartmann, 1997, Characterization of petrophysical flow units in carbonate reservoirs: AAPG Bulletin, v. 81, p. 734–759.

Morris, R. L., and W. P. Biggs, 1967, Using log-derived values of water saturation and porosity: Society of Professional Well Log Analysts, 8th Annual Logging Symposium, Transactions, Paper O.

Mullins, J. E., 1966, Stereoscopic deep well photography in opaque fluids: Society of Professional Well Log Analysts, 7th Annual Logging Symposium Transactions, Paper N, 9 p.

Newberry, B. M., L. M. Grace, and D. D. Stief, 1996, Analysis of carbonate dual porosity systems from borehole electrical images: Society of Petroleum Engineers, Permian Basin Oil And Gas Recovery Conference, p. 123–129, paper SPE-35158.

Paillet, F. L., C. Barton, S. Luthi, F. Rambow, and J. Zemanek (eds.), 1990, Borehole imaging: Society of Professional Well Log Analysts Reprint Volume, 472 p.

Parker, D. L., and P. D. Heffernan, 1993, Methods of determining induced fracture orientation—Ferrier
<!-- page 254 -->
References

243

field application: Canadian Well Logging Society Annual Journal, p. 284–298.

Pickett, G. R., 1966, A review of current techniques for determination of water saturation from logs: Journal of Petroleum Technology, v. 18, no. 11, p. 1425–1433.

Pickett, G. R., 1973, Pattern recognition as a means of formation evaluation, Society of Professional Well Log Analysts, 14th Annual Logging Symposium, Transactions, Paper A.

Pickett, G. R., 1977, Recognition of environments and carbonate rock type identification: in Formation evaluation manual unit II, section exploration wells: Tulsa, Oklahoma, Oil and Gas Consultants International, Inc., p. 4–25.

Plumb, R. A., and S. H. Hickman, 1985, Stress-induced borehole elongation—a comparison between the four-arm dipmeter and the borehole televiewer in the Auburn geothermal well: Journal of Geophysical Research, v. 90, no. B7, p. 5513–5521.

Poupon, A., and J. Leveaux, 1971, Evaluation of water saturation in shaly formations: The Log Analyst, v. 12, no. 4, p. 3–8.

Raymer, L. L., E. R. Hunt, and J. S. Gardner, 1980, An improved sonic transit time-to-porosity transform: Society of Professional Well Log Analysts, 21st Annual Logging Symposium, Transactions, Paper P.

Reid, R. R., and M. B. Enderlin, 1998, True pay thickness determination of laminated sand and shale sequences using borehole resistivity image logs: Society of Professional Well Log Analysts, 39th Annual Logging Symposium, Transactions, Paper GGG, 9 p.

Rosthal, R. A., R. A. Young, J. R. Lovell, L. Buffington, and C. L. Arceneaux Jr., 1995, Formation evaluation and geological interpretation from the resistivity-at-the-bit tool: Society of Petroleum Engineers, Annual Conference and Exhibition, p. 187–199, paper SPE 30550.

Schlumberger, 1972, Log Interpretation, Vol. I—Principles: New York, Schlumberger Limited, 112 p.

Schlumberger, 1974, Log Interpretation, Vol. II—Applications: New York, Schlumberger Limited, 116 p.

Schlumberger, 1975, A guide to wellsite interpretation for the Gulf Coast: Schlumberger Offshore Services, 58 p.

Schlumberger, 1979, Log Interpretation Charts: Houston, Texas, Schlumberger Limited, 97 p.

Schlumberger, 1983, Stratigraphic high resolution dipmeter tool: Paris, Schlumberger Limited, Document No. M-08630, 23 p.

Schlumberger, 1984, Electromagnetic Propagation Tool: Houston, Texas, Schlumberger Well Services.

Schlumberger, 1993, Ultrasonic Imaging—USI, Ultrasonic Imager; UBI, Ultrasonic Borehole Imager: Houston, Texas, Schlumberger Wireline and Testing, Document No. SMP-9230, 28 p.

Schlumberger, 1998, Log Interpretation Charts: Sugar Land, Texas, Schlumberger Wireline and Testing, SMP-7006.

Seiler, D., C. Edmiston, D. Torres, and J. Goetz, 1990, Field performance of a new borehole televiewer tool and associated image processing techniques: Society of Professional Well Log Analysts, 31st Annual Logging Symposium, Transactions, Paper H, 20 p.

Seiler, D., G. King, and D. Eubanks, 1994, Field test results of a six arm microresistivity borehole imaging tool: Society of Professional Well Log Analysts, 35th Annual Logging Symposium, Transactions, Paper W, 21 p.

Serra, O., 1984, Fundamentals of Well-log Interpretation: New York, Elsevier, 423 p.

Serra, O., 1989, Formation MicroScanner image interpretation: Houston, Texas, Schlumberger Educational Services, 117 p.

Sethi, D. K., 1979, Some considerations about the formation resistivity factor-porosity relationships: Society of Professional Well Log Analysts, 20th Annual Logging Symposium, Transactions, paper L.

Society of Professional Well Log Analysts, 1984, Glossary of terms and expressions used in well logging: Houston, Texas, Society of Professional Well Log Analysts, 116 p.

Simandoux, P., 1963, Mesures dielectriques en milieu poreux, application a mesure des saturations en eau: Etude du Comportement des Massifs Argileux, Revue de l'institut Francais du Petrole, Supplementary Issue.

Smits, J. W., D. Benimeli, I. Dubourg, O. Faivre, D. Hoyle, V. Tourillon, J-C. Troullier, and B. I. Anderson, 1995, High resolution from a new laterolog with azimuthal imaging: Society of Petroleum Engineers, Annual Conference and Exhibition, p. 563–576, paper 30584.

Sovich, J., J. Klein, and N. Gaynor, 1996, A thin bed model for the Kuparuk A sand, Kuparuk River field, North Slope, Alaska: Society of Professional Well Log Analysts, 37th Annual Logging Symposium, Transactions, Paper D, 13 p.
<!-- page 255 -->
244

ASQUITH AND KRYGOWSKI

Springer, J., 1987, Stress orientations from wellbore breakouts in the Coalinga area: Tectonics, v. 6, p. 667–676.

Steiber, S. J., 1970, Pulsed neutron capture log evaluation in the Louisiana Gulf Coast: Society of Petroleum Engineers, 45th Annual Meeting, paper SPE-2961.

Suau, J., P. Grimaldi, A. Poupon, and G. Souhaite, 1972, Dual Laterolog—Rxo tool: Society of Petroleum Engineers, 47th Annual Meeting, paper SPE-4018.

Svor, T. R., and D. N. Meehan, 1991a, Quantifying horizontal well logs in naturally fractured reservoirs—I: Society of Petroleum Engineers, Annual Conference and Exhibition, p. 469–480., paper SPE 22704.

Svor, T. R., and D. N. Meehan, 1991b, Quantifying horizontal well logs in naturally fractured reservoirs—II: Society of Petroleum Engineers, Annual Conference and Exhibition, p. 471–480, paper SPE 22932.

Timur, A., 1968, An investigation of permeability, porosity, and residual water saturation relationships for sandstone reservoirs: The Log Analyst, v. 9, p. 8–17.

Tittman, J., and J. S. Wahl, 1965, The physical foundations of formation density logging (Gamma-Gamma): Geophysics, v. 30, p. 284–294.

Tixier, M. P., R. P. Alger, and C. A. Doh, 1959, Sonic logging, Journal of Petroleum Technology, v. 11, no. 5., p. 106–114.

Tixier, M. P., R. P. Alger, W. P. Biggs, and B. N. Carpenter, 1963, Dual induction-laterolog—a new tool for resistivity analysis: Society of Petroleum Engineers, 38th Annual Meeting, paper SPE-713.

Truman, R., R. P. Alger, J. Connell, and R. L. Smith, 1972, Progress report on interpretation of the dual spacing neutron log (CNL): Society of Professional Well Log Analysts, 13th Annual Logging Symposium, Transactions, paper U.

Watney, W. L., 1979, Gamma ray-Neutron cross-plots as an aid in sedimentological analysis (p. 81–100), in D. Gill and D. F. Merriam (eds.), Geomathematical and petrophysical studies in sedimentology: New York, Pergamon Press, 266 p.

Watney, W. L., 1980, Cyclic sedimentation of the Lansing-Kansas City groups in northwestern Kansas and southwestern Nebraska: Kansas Geological Survey Bulletin 220, 72 p.

Waxman, M. H., and L. J. M. Smits, 1968, Electrical conductivities in oil-bearing shaly sands: Society of Petroleum Engineers Journal, v. 245, p. 107–122.

Waxman, M. H., and E. C. Thomas, 1974, Electrical conductivity in shaly sands—I: Journal of Petroleum Technology, v. 257, p. 213–225.

Wermund, E. G., 1975, Upper Pennsylvanian limestone banks, north central Texas: University of Texas, (Austin), Bureau of Economic Geology Circular 75-3, 34 p.

Western Atlas International, Inc., 1995, Log Interpretation Charts, Houston, Texas, Western Atlas, 300 p.

Whittaker, J. L., and G. D. Linville, 1996, Well preparation—essential to successful video logging: Society of Petroleum Engineers, 66th Western Region Meeting, p. 297–308, paper SPE 35680.

Williams, C. G., P. D. Jackson, M. A. Lovell, and P. K. Harvey, 1997, Assessment and interpretation of electrical borehole images using numerical simulations: The Log Analyst, v. 38, no. 6, p. 34–44.

Witton, E. M., 1999, Outcrop and subsurface characterization of the Lewis Shale, Carbon County, Wyoming: Unpublished M.S. thesis, Colorado School of Mines, Golden, Colorado, 214 p.

Wyllie, M. R. J., and W. D. Rose, 1950, Some theoretical considerations related to the quantitative evaluations of the physical characteristics of reservoir rock from electric log data: Journal of Petroleum Technology, v. 189, p. 105–110.

Wyllie, M. R. J., A. R. Gregory, and G. H. F. Gardner, 1958, An experimental investigation of the factors affecting elastic wave velocities in porous media: Geophysics, v. 23, p. 459–493.

Younes, A. I., T. Engelder, and W. Bosworth, 1998, Fracture distribution in faulted basement blocks: Gulf of Suez, Egypt, in M. P. Coward, T. S. Daltaban, and H. Johnson, (eds.), Structural Geology in Reservoir Characterization: London, The Geological Society, Special Publication 127, p. 167–190.

Zemanek, J., E. E. Glenn, L. J. Norton, and R. L. Caldwell, 1970, Formation evaluation by inspection with the borehole televiewer: Geophysics, v. 35, p. 254–269.

Zoback, M. D., D. Moos, L. Mastin, and R. N. Anderson, R. N., 1985, Well bore breakouts and in situ stress: Journal of Geophysical Research, v. 90, no. B7, p. 5523–5530.
<!-- page 256 -->
Basic Well Log Analysis is a general introduction to common openhole logging measurements, both wire line and MWD/LWD, and the interpretation of those measurements to determine the traditional analytical goals of porosity, fluid saturation, and lithology/mineralogy. It is arranged by the interpretation goals of the data, rather than by the underlying physics of the measurements.

The accompanying CD-ROM contains digital versions of the data from the case studies, a summary guide to the measurements and their interpretation, and a simple spreadsheet containing some of the more common interpretation algorithms.

This Second Edition of Basic Well Log Analysis delivers a great impact on training and self-training along with superior workbook exercises, newer measurements, borehole imaging, and nuclear magnetic resonance in separate chapters, all directed to provide a guide through the lengthy and sometimes ambiguous terminology of well logging and petrophysics. It provides readers with interpretation examples (and solutions) so that the techniques described here can be practiced.


American Association of Petroleum Geologists

P.O. Box 979

Tulsa OK 74119

USA

www.aapg.org

