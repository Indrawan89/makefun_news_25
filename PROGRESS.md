# News-image 20261125 — dense poster build

Competition: news-image-20261125 — "Sum up 25 November's world news in one image"
($100, deadline 2026-11-27T00:00:00Z / 27 Nov 07:00 WIB). Repo: Indrawan89/makefun_news_25.

## Poster

`main.py` — pure Python stdlib, written fresh in this session (own 5x7 bitmap
font, own canvas, own PNG encoder with zlib+CRC32). No file from any earlier
edition was read, copied, or re-typed. 1024x1024, masthead "THE WORLD TODAY —
Wednesday 25 November 2026".

- Lead: Trump tariff threat sinks world markets (USTR to unveil findings on
  China and 16 partners; Nasdaq -1.5%, Nvidia -6% after +31% Monday; Asia
  tumbles Wed: KOSPI -5.3%, Taiwan -5.1%, Nikkei -2.9%) + market bar panel.
- Panel: WAR AT SEA — Zelensky confirms Ukraine sank a Russian corvette off
  Benghazi and hit a cargo ship in the Gulf of Finland.
- 8 boxes, 32 dated stories: Europe 5, Middle East 4, Asia 5, Americas 4,
  Africa 4, Oceania 3, Sport & Tech 3, Also today 4. Total 34 stories.

## Tests

- Determinism: main.py run 3x in the entry folder — byte-identical
  (32,834 bytes, sha256
  `2f08fef317f750fd47664899a331595e21f9c1956f7ddddb8d9cecd3826c4fae`).
- Clean-room run: main.py copied to a fresh dir, run from that dir and
  from `/` — same sha256 both times (guards against the 22 Nov Acute
  Mirror grader failure: no dependency on the entry folder or cwd).
- Visual check 2x: full poster + zoomed crops (masthead/lead/market
  panel/war strip, bottom boxes). No overlaps, no clipping, all 34
  stories legible, dates right-aligned in red, footer present. Two
  bugs fixed during the build: 7 headlines over the 32-char limit
  (shortened) and one lowercase deck (uppercased). One stray
  `__pycache__/main.cpython-312.pyc` was committed by mistake, then
  removed (`git rm --cached` + delete + `.gitignore`, commit 1e55f54).
- Bundle v1: `~/workspace/makefun/token-radar-01-rebuild5-transcripts-v1.tar.gz`
  is NOT this entry's bundle. This entry's bundle v1:
  `~/workspace/makefun/news-image-20261125-dense-transcripts-v1.tar.gz`
  (170,182 bytes, sha256
  `05600da4a7e238967c1c89436c90e0b0b12336584793eaadfc63a653b810a258`).
  Check v1: fails ONLY `thinking_priced` (0 usage rows — this session
  had not ended yet); `thinking_reproduces` PASS 96.5% (396/410
  authored, 0 copied, 0 pasted), `thinking_own_work` PASS,
  `thinking_in_window` PASS. Parent must re-bundle after this session
  ends with the session's usage row (agent
  `b307fa40-201d-4dd6-a9a2-82e3bde5f617`) to clear `thinking_priced`.
- Local HEAD: `1e55f54` (6 tracked files, no stray files).
- NO push, NO submit, NO GitHub repo touched. Ready for EVAL.

## Story list (date = day the event happened or was first reported)

Lead — 25 Nov — Trump administration poised to release USTR findings on
excess industrial capacity in China, the EU and 14 other economies; new
tariffs could follow within days. Nasdaq -1.5%, S&P 500 -0.5% on 24 Nov;
Nvidia -6% after +31% Monday on Huang's return; Asian stocks tumble 25 Nov
(KOSPI -5.3%, Taiwan -5.1%, Nikkei -2.9%).
Sources: Reuters via DailyFoxNews 24 Nov; Reuters via 93-5 The Lloyd 25 Nov;
CoinGape 24 Nov; CryptoBriefing 24 Nov.

War at sea — 24 Nov — Zelensky confirms Ukraine struck a Russian cargo ship
(Sparta II) in the Gulf of Finland and sank a Russian corvette off Benghazi,
Libya, with seven naval drones (also a helicopter and a cargo ship hit).
Sources: Reuters world summary 25 Nov; RFE/RL 25 Nov; AP via SouthPolitics
24 Nov.

Europe (5)
- 24 Nov — Russian Kh-101 missiles fell in Poland; Warsaw summoned Russia's
  ambassador. Source: Pollar News conflicts 24 Nov.
- 23 Nov — Russia warns Estonia of open war as Tallinn prepares to close its
  Russian border crossings from 1 Dec. Source: Pollar News 24 Nov.
- 24 Nov — MI5 and the Ministry of Defence warn UK arms suppliers to Ukraine
  of Russian sabotage. Source: Pollar News 24 Nov.
- 25 Nov — EU warns 11 countries over budget rules, seeks tougher action on
  Hungary. Source: HigmedPoland 25 Nov 01:13 UTC.
- 24 Nov — French officials order ex-president Sarkozy and his wife Carla
  Bruni to trial in a corruption case; pre-trial hearing 1 Apr 2027.
  Source: Reuters world summary 25 Nov.

Middle East (4)
- 24 Nov — Houthis hit Riyadh's tallest tower with a drone; 11 wounded.
  Source: Reuters world summary 25 Nov; Saudi civil defence.
- 24 Nov — Israeli strike kills Hamas internal security chief Naeem Abu Nahal
  in Gaza City; six others killed. Source: Pollar News 24 Nov; AP 24 Nov.
- 24 Nov — Three tankers set ablaze in the Strait of Hormuz after hitting
  sea mines, IRGC says; claim not independently confirmed.
  Source: Pollar News 24 Nov.
- 24 Nov — US Treasury sanctions more than two dozen Iran-linked exchange
  houses. Source: AP via SouthPolitics 24 Nov.

Asia (5)
- 24 Nov — China investigates Shanghai party chief Chen Jining, a Politburo
  member — the fourth Politburo member to fall since 2025.
  Source: Xinhua via CNA 24 Nov.
- 24 Nov — Huawei found guilty of stealing trade secrets in a US criminal
  trial, acquitted of racketeering. Source: Reuters 24 Nov.
- 24 Nov — Russian warplanes enter South Korea's air defence zone near
  Ulleung Island; Seoul scrambles fighters and issues a civilian alert.
  Source: WH News 24 Nov.
- 24 Nov — Death toll from the Indonesia factory fire (Cikande, Banten)
  rises to 26, dozens still missing. Source: CNA 24 Nov.
- 24 Nov — ICJ finds Myanmar committed genocide against the Rohingya;
  Singapore studying the implications. Source: CNA 24 Nov.

Americas (4)
- 24 Nov — Trump awards Rudy Giuliani the Presidential Medal of Freedom.
  Source: Reuters world summary 25 Nov.
- 24 Nov — US CIA and ODNI suffer a cybersecurity breach involving some
  unclassified information, source says. Source: Reuters 24 Nov.
- 24 Nov — Fort Hood shooter Nidal Hasan seeks a stay of his execution,
  set for next week. Source: Reuters world summary 25 Nov.
- 24 Nov — US consumer confidence jumps to its highest level in nearly
  two years. Source: Reuters via DailyFoxNews 24 Nov.

Africa (4)
- 24 Nov — MSF suspends all activities in South Sudan's Yei River county
  following an abduction. Source: Panapress 24 Nov.
- 23 Nov — Heavy fighting in Ituri traps DR Congo Ebola responders.
  Source: Panapress 23 Nov.
- 24 Nov — ECOWAS ministerial committee reviews preparations for the 2027
  single currency launch. Source: Panapress 24 Nov.
- 24 Nov — Gambia intercepts 491 would-be irregular migrants.
  Source: Panapress 24 Nov.

Oceania (3)
- 25 Nov — Solomon Islands ends its Beijing security pact and pivots to an
  Australia treaty, expected to be signed 25 Nov. Source: PINA 25 Nov;
  Reuters 24 Nov.
- 25 Nov — Fiji shuts all schools for five days as the El Nino drought
  crisis deepens; emergency could stretch into 2027. Source: PINA 25 Nov.
- 24 Nov — Australian coalition opposes the Vanuatu treaty deal over
  climate provisions. Source: PINA 24 Nov.

Sport & Tech (3)
- 24 Nov — Senegal reinstated as AFCON 2025 champions after a successful
  CAS appeal overturning CAF's decision. Source: IANS 24 Nov.
- 24 Nov — Sooryavanshi, 15, smashes the fastest List A double hundred:
  204 off 53 balls. Source: Newsmriti 25 Nov 06:00 IST.
- 24 Nov — England beat Australia by eight wickets in the second T20I,
  chasing 185 to level the series. Source: JagranJosh 25 Nov.

Also today (4)
- 24 Nov — China's Shenzhou-24 space flight takes off with a Pakistani
  national as the first foreign astronaut. Source: CNA 24 Nov.
- 25 Nov — US October PCE inflation data and the second reading of Q3 GDP
  due today. Source: Reuters via DailyFoxNews 24 Nov.
- 24 Nov — Russia's own figures show almost 500,000 deaths in the war in
  Ukraine. Source: BBC 24 Nov.
- 24 Nov — Trump pardons turkeys Freedom and Feathers for Thanksgiving.
  Source: Reuters world summary 25 Nov.
