# NOTES — news-image-20261126

## Edition window (read this first)

Compiled 26 Nov 2026, 00:10–00:50 WIB (25 Nov 2026, 17:10–17:50 UTC).
At that hour the 26 November UTC day had just begun in Asia, so the
stories below are the ones carried as the 26 November edition: the
Reuters World News Summary published 25 Nov 2026 18:30 IST (= 26 Nov
00:00 WIB), plus AP / AFP / Fox Weather reports dated 25 Nov 2026.
Thanksgiving Day itself falls on 26 Nov 2026. No story was invented;
anything that could not be confirmed in one of those sources was left
out. The timeline strip uses UTC times taken from the same reports
(Cartagena rescue 06:30 GMT, Shenzhou-24 entry 06:35 GMT, Reuters
summary 13:00 UTC).

## Sources per story

Leads (5):

1. Hormuz tankers hit mines — Reuters, "Two oil tankers struck naval
   mines and caught fire in the Strait of Hormuz" (25 Nov); IRGC
   statement via Reuters; "Iran says it is prepared to withstand US
   blockade" (Reuters, 25 Nov).
2. Russian strikes cut power in five regions — Reuters World News
   Summary, 25 Nov (DTEK plant halted, Naftogaz fire in Poltava).
3. Israeli strike kills Hamas security chief — Reuters, 25 Nov
   (Mohammad Abuelouf, wife and two children, Gaza apartment).
4. Australia–Solomons pact — AP, 25 Nov ("Solomon Islands names
   Australia as its primary security partner"); Reuters summary
   (A$740m over ten years).
5. Thanksgiving storms — Fox Weather live updates, 25 Nov (250m
   Americans, gusts to 70 mph, 100th Macy's parade balloons at risk,
   SF king tide record 8.23 ft); AAA 81.5m travellers via AP /
   weather.com.

Briefs (31), all from the Reuters World News Summary of 25 Nov 2026
unless noted:

6. Houthis hit Ras Tanura refinery + Riyadh tower, 11 wounded —
   Reuters (also DailyFoxNews Early Edition, 25 Nov).
7. Houthis will not seize Aden — Reuters summary.
8. Iraq top court, Baghdad may deploy on all borders — Reuters.
9. Italy rebukes Ukraine over Libya strikes — Reuters.
10. Two Libyans die after Benghazi attack — Reuters via Paris Times
    feed, 25 Nov.
11. Pope Leo calls COP31 failure "troubling" — Reuters / AP.
12. Sudan RSF drone strikes kill 19 in Blue Nile — Reuters summary.
13. Lebanon to open second airport — Reuters summary.
14. Canary Islands single-day migrant record, 2,100+ — Reuters.
15. Saudi national kidnapped in Niger — Reuters summary.
16. Bulgaria intercepts first migrant boat in months, 35 aboard —
    Reuters / BTA.
17. Puigdemont to return to Spain 12 Dec — Reuters summary.
18. Kremlin rejects Johnson's token-force call — Reuters.
19. Sarkozy corruption case ordered to trial — Reuters summary.
20. Eurostar cancels London–Paris–Brussels trains — Reuters.
21. RAF moves aircraft to hangars at night — Reuters (Times / Sky).
22. German economy +0.1% in Q3 — Reuters.
23. Greeks strike over wages and public services — Reuters.
24. NATO AWACS to Poland after missiles incident — Reuters summary.
25. Taiwan votes Saturday, mayoral polls — Reuters summary.
26. First foreigner boards Tiangong (Zeeshan Ali, Shenzhou-24) —
    Reuters (crew entered Tiangong 06:35 GMT).
27. Xi graft probe of Shanghai chief Chen Jining — Reuters analysis.
28. China drafts 78 international AI standards — AP via NewsTalk
    Florida, 25 Nov.
29. Asian stocks plunge in AI sell-off — Reuters (KOSPI / Nikkei /
    Taiex slide; percentages differ between wires, so none is printed).
30. Bangladesh garment workers clash with police — Reuters summary.
31. North Korea expels Swiss diplomat — Reuters / KCNA.
32. US GDP +4.3% in Q3 — BEA via AP, 25 Nov.
33. US plans tariffs on China, EU and 14 others — AP, 25 Nov.
34. Huawei convicted in New York — AP, 25 Nov.
35. Colombia hostages freed in Cartagena supermarket raid — Reuters /
    AFP (president's video 01:30 local = 06:30 GMT).
36. Canada foreign-student curbs test talent drive — Reuters summary.

## Build

- `draw.py` — local Pillow renderer (NOT run by the grader). Fixed
  DejaVu fonts, no randomness, no network. Two runs of draw.py give
  byte-identical entry.png.
- `main.py` — stdlib only (hashlib / os / shutil / struct / sys).
  Copies entry.png to $MAKEFUN_OUTPUT_DIR/entry.png and verifies PNG
  magic, 1024x1024 dimensions and a byte-identical copy.
- `entry.png` — 1024x1024, 191,113 bytes,
  sha256 dc358b129e2d5afa075578d6fcc3abf76cf06aa29cf2483075bdc4c5d6081219,
  PNG CRCs all valid, ink 25.0%.

## Verification (before submit)

- draw.py run twice: identical sha256.
- main.py run twice with MAKEFUN_OUTPUT_DIR set: identical sha256.
- Grader simulation: repo copied to /tmp, read-only, run as uid/gid
  65534 with setpriv, MAKEFUN_OUTPUT_DIR set to an empty dir: exit 0,
  output entry.png byte-identical to the repo copy.
- No PIL / Pillow import anywhere in main.py; no network; no writes
  outside the output directory.
