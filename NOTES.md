# Notes — World News in One Image, 26 November 2026

Competition: news-image-20261126 — "Sum up 26 November's world news in one image". $100, top 50 share. Deadline 28 November 2026, 07:00 WIB.

Sources: Reuters World News Summary, 25 November 2026; AP; AFP; Fox Weather live updates, 25 November 2026. Every story below is confirmed in those sources; nothing is invented.

## Leads (5)

1. Hormuz tankers hit mines — Two oil tankers struck naval mines and caught fire in the Strait of Hormuz; Iran says it is prepared to withstand a US blockade. — Reuters, 25 Nov. Region: Middle East.
2. Russian strikes cut power in five regions — DTEK plant halted, Naftogaz fire in Poltava. — Reuters World News Summary, 25 Nov. Region: Europe.
3. Israeli strike kills Hamas security chief — Mohammad Abuelouf, wife and two children, Gaza apartment. — Reuters, 25 Nov. Region: Middle East.
4. Australia–Solomons pact — Solomon Islands names Australia as its primary security partner; A$740m over ten years. — AP, 25 Nov. Region: Asia-Pacific.
5. Thanksgiving storms — 250m Americans affected, gusts to 70 mph, 100th Macy's parade balloons at risk, SF king tide record 8.23 ft; AAA 81.5m travellers. — Fox Weather live updates, 25 Nov. Region: Americas.

## Briefs (31)

All from the Reuters World News Summary, 25 Nov, unless noted.

6. Houthis hit Ras Tanura refinery + Riyadh tower, 11 wounded — Middle East.
7. Houthis will not seize Aden — Middle East.
8. Iraq top court: Baghdad may deploy on all borders — Middle East.
9. Italy rebukes Ukraine over Libya strikes — Europe.
10. Two Libyans die after Benghazi attack — Africa.
11. Pope Leo calls COP31 failure "troubling" — Europe.
12. Sudan RSF drone strikes kill 19 in Blue Nile — Africa.
13. Lebanon to open second airport — Middle East.
14. Canary Islands single-day migrant record, 2,100+ — Europe.
15. Saudi national kidnapped in Niger — Africa.
16. Bulgaria intercepts first migrant boat in months, 35 aboard — Europe.
17. Puigdemont to return to Spain 12 Dec — Europe.
18. Kremlin rejects Johnson's token-force call — Europe.
19. Sarkozy corruption case ordered to trial — Europe.
20. Eurostar cancels London–Paris–Brussels trains — Europe.
21. RAF moves aircraft to hangars at night — Europe.
22. German economy +0.1% in Q3 — Europe.
23. Greeks strike over wages and public services — Europe.
24. NATO AWACS to Poland after missiles incident — Europe.
25. Taiwan votes Saturday, mayoral polls — Asia-Pacific.
26. First foreigner boards Tiangong — Zeeshan Ali, Shenzhou-24, crew entered Tiangong 06:35 GMT — Asia-Pacific.
27. Xi graft probe of Shanghai chief Chen Jining — Asia-Pacific.
28. China drafts 78 international AI standards — Asia-Pacific.
29. Asian stocks plunge in AI sell-off — KOSPI / Nikkei / Taiex slide — Asia-Pacific.
30. Bangladesh garment workers clash with police — Asia-Pacific.
31. North Korea expels Swiss diplomat — Asia-Pacific.
32. US GDP +4.3% in Q3 — BEA via AP — Americas.
33. US plans tariffs on China, EU and 14 others — AP — Americas.
34. Huawei convicted in New York — AP — Americas.
35. Colombia hostages freed in Cartagena supermarket raid — president's video 01:30 local = 06:30 GMT — Americas.
36. Canada foreign-student curbs test talent drive — Americas.

## UTC timeline strip

- 06:30 GMT — Cartagena rescue.
- 06:35 GMT — Shenzhou-24 entry into Tiangong.
- 13:00 UTC — Reuters summary published.

## Build

- `draw.py` renders `entry.png` (1024x1024) with Pillow and fixed DejaVu fonts; no randomness, no network. Run it twice to confirm byte-identical output.
- `main.py` is standard library only and copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`, verifying PNG magic, 1024x1024 size and a byte-identical copy.
- This is rebuild #2 in a fresh session started after the competition opened (26 Nov 00:00 UTC / 07:00 WIB), with draw.py and main.py written fresh in this session.
