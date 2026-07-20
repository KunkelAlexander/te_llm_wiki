# Source enrichment log (historical — the initial backfill batch only)

This file records the initial backfill effort that added a hand-written `## Summary` section (key
quantitative findings first, then bullet points) to the oldest 10 `wiki/sources/*.md` pages, sourced
from the fulltext in `output/metadata_with_fulltext.parquet` (matched by each page's `doc_ids`).

**This is no longer required reading for ongoing work.** Adding this summary to every new source
page is now a standing part of the regular update workflow — see "Quantitative-findings summary"
and update-workflow step 2 in `AGENT_INSTRUCTIONS.md`. Whether a given source page has been
enriched yet is tracked by the presence of the `<!-- ENRICHED SUMMARY` marker in that page itself,
not by this log — check the page, not this file, when deciding whether a source still needs one.

**How it's preserved across regeneration**: `1_build_wiki_subset.py` was updated to detect the
`<!-- ENRICHED SUMMARY: ... -->` marker in an existing source page and re-append everything from
that marker onward when it rewrites a page, instead of overwriting it. In practice this rarely
triggers anyway — once a page's article URL is logged in `PROCESSED.csv`, the script skips it on
future runs — but the safeguard is there in case a page ever needs to be regenerated.

**Ordering used so far**: sources taken in ascending date order from `wiki/sources/index.md`
("oldest first"), 10 at a time. Continue from the next unprocessed row in that table.

**Note on summary depth**: several early (2011-2017) sources are press releases/letters whose
scraped fulltext is only 500-2,500 characters (often just the article page's own text, sometimes
missing entirely — see the VAT consultation entry below). For these, a genuinely supportable
summary is a handful of bullets, not 1-2 pages — padding them further would mean inventing content
not in the source. Only sources with substantial fulltext (reports/briefings) get the fuller
treatment.

## Batch 1 (done 2026-07-20) — first 10 sources by date

| Source | Date | Status |
|---|---|---|
| [T&E response to the VAT consultation](t-e-response-to-the-vat-consultation.md) | 2011-06-09 | Done — fulltext capture failed (only PDF filename + boilerplate), noted as such |
| [Allocating aviation CO2 emissions – the airspace-based approach](allocating-aviation-co2-emissions-the-airspace-based-approach-and-its-alternativ.md) | 2013-01-21 | Done |
| [The Billion Euro Aviation Bonanza](the-billion-euro-aviation-bonanza-aviation-s-participation-in-the-eu-ets.md) | 2013-01-22 | Done — exact windfall-profit € figure not present in scraped fulltext, noted as gap |
| [Does aviation pay its way?](does-aviation-pay-its-way.md) | 2013-07-24 | Done |
| [Letter to the Commission on ICAO Assembly](letter-to-the-commission-on-icao-assembly.md) | 2013-09-23 | Done |
| [Open letter to the German government on ETS enforcement](open-letter-to-the-german-government-to-provide-public-proof-of-german-enforceme.md) | 2014-04-29 | Done |
| [How to incentivise renewable aviation fuels through the Renewable Energy Directive](how-to-incentivise-renewable-aviation-fuels-through-the-renewable-energy-directi.md) | 2017-09-05 | Done — full treatment, richest source in this batch |
| [Countries reject plan for aviation biofuels targets](countries-reject-plan-for-aviation-biofuels-targets.md) | 2017-10-14 | Done |
| [Aviation biofuels target rejected](aviation-biofuels-target-rejected.md) | 2017-10-30 | Done |
| [EU Commission surrenders to United Nations' ICAO on aviation biofuels](eu-commission-surrenders-to-united-nations-icao-on-aviation-biofuels.md) | 2017-11-10 | Done |

## Batch 2 (done 2026-07-20) — next 10 sources by date

| Source | Date | Status |
|---|---|---|
| [Aviation carbon offsetting scheme: ICAO circulates draft rules](aviation-carbon-offsetting-scheme-icao-circulates-draft-rules.md) | 2018-01-09 | Done — scraped fulltext is the ICAO draft SARP document itself, not T&E commentary, noted as such |
| [Timmermans must make concrete proposals to deliver a European Green Deal](timmermans-must-make-concrete-proposals-to-deliver-a-european-green-deal.md) | 2019-10-08 | Done — short press-release quote, no figures |
| [Understanding the indirect land use change analysis for Corsia](understanding-the-indirect-land-use-change-analysis-for-corsia.md) | 2020-02-03 | Done — full treatment |
| [EU strategy for Smart Sector Integration](eu-strategy-for-smart-sector-integration.md) | 2020-06-02 | Done — full treatment |
| [How EU legislation can drive an uptake of sustainable advanced fuels in aviation](how-eu-legislation-can-drive-an-uptake-of-sustainable-advanced-fuels-in-aviation.md) | 2020-07-16 | Done — full treatment |
| [Revision of the EU ETS for aviation](revision-of-the-eu-ets-for-aviation.md) | 2020-09-04 | Done — full treatment |
| [Which renewable transport fuels deliver substantial carbon reductions?](which-renewable-transport-fuels-deliver-substantial-carbon-reductions.md) | 2020-09-22 | Done — full treatment |
| [The costs of EU ETS and Corsia for European aviation](the-costs-of-eu-ets-and-corsia-for-european-aviation.md) | 2020-09-23 | Done — full treatment |
| [T&E's response to roadmap consultation on the inception impact assessment for RED revision](t-e-s-response-to-roadmap-consultation-on-the-inception-impact-assessment-for-th.md) | 2020-09-25 | Done — full treatment |
| [Making the aviation ETS fit for purpose](making-the-aviation-ets-fit-for-purpose.md) | 2020-11-29 | Done — full treatment |

## Batches 3-7 (done 2026-07-20) — next 50 sources by date (2020-11-30 through 2021-12-15)

Five batches of 10, processed in one pass. All full treatments except where noted (short
press-releases/news items with little or no quantitative content: airline-beggars-can-t-be-choosers,
only-a-third-of-business-flyers-expect-to-return-to-normal, easyjet-s-new-domestic-routes,
the-uk-s-green-jet-fuel-mandate-needs-robust-sustainability-criteria, the-road-to-a-road-ets).

| Source | Date |
|---|---|
| [Response to the Emissions Trading System (ETS) inception impact assessment](response-to-the-emissions-trading-system-ets-inception-impact-assessment.md) | 2020-11-30 |
| [Airline beggars can't be choosers](airline-beggars-can-t-be-choosers.md) | 2020-12-03 |
| [E-fuel would be wasted on cars while it's badly needed to decarbonise planes and ships – study](e-fuel-would-be-wasted-on-cars-while-it-s-badly-needed-to-decarbonise-planes-and.md) | 2020-12-07 |
| [EU transport plan a big step but risks rerun of biofuels fiasco](eu-transport-plan-a-big-step-but-risks-rerun-of-biofuels-fiasco.md) | 2020-12-09 |
| [Making aviation fuel mandates sustainable](making-aviation-fuel-mandates-sustainable.md) | 2020-12-16 |
| [Plans for 'green' jet fuels threaten to repeat biofuels mistakes – analysis](plans-for-green-jet-fuels-threaten-to-repeat-biofuels-mistakes-analysis.md) | 2020-12-16 |
| [The return of the Climate Chancellor?](the-return-of-the-climate-chancellor.md) | 2020-12-19 |
| [Four positives for sustainable aviation in this annus horribilis](four-positives-for-sustainable-aviation-in-this-annus-horribilis.md) | 2020-12-21 |
| [How to ensure the sustainability of electrofuels](how-to-ensure-the-sustainability-of-electrofuels.md) | 2021-01-19 |
| [Green jet fuel plans risk history repeating itself](green-jet-fuel-plans-risk-history-repeating-itself.md) | 2021-01-21 |
| [FAQ: the what and how of e-kerosene](faq-the-what-and-how-of-e-kerosene.md) | 2021-02-05 |
| [Aviation industry's net zero plan over-reliant on future technologies](aviation-industry-s-net-zero-plan-over-reliant-on-future-technologies.md) | 2021-02-25 |
| [First passenger flight performed using clean fuels. Sort of.](first-passenger-flight-performed-using-clean-fuels-sort-of.md) | 2021-02-25 |
| [NGOs and aviation sector call for long-haul emissions to be covered by EU's SAF mandate](ngos-and-aviation-sector-call-for-long-haul-emissions-to-be-covered-by-eu-s-sust.md) | 2021-03-11 |
| [The EU's assessment of the Corsia airline CO2 deal](the-eu-s-assessment-of-the-corsia-airline-co2-deal.md) | 2021-03-17 |
| [One year of airline bailouts: what have we learned?](one-year-of-airline-bailouts-what-have-we-learned.md) | 2021-03-29 |
| [Advanced renewable fuels in EU transport](advanced-renewable-fuels-in-eu-transport.md) | 2021-03-31 |
| [Decarbonising long-haul trucking in Germany](die-dekarbonisierung-des-lkw-fernverkehrs-in-deutschland.md) | 2021-04-06 |
| [Europe's surging demand for used cooking oil could fuel deforestation](europe-s-surging-demand-for-used-cooking-oil-could-fuel-deforestation.md) | 2021-04-19 |
| [Unlocking electric trucking in the EU: recharging along highways](unlocking-electric-trucking-in-the-eu-recharging-along-highways.md) | 2021-04-21 |
| [Can Airbus deliver guilt-free flying?](can-airbus-deliver-guilt-free-flying.md) | 2021-04-29 |
| [Only a third of business flyers expect to return to normal](only-a-third-of-business-flyers-expect-to-return-to-normal.md) | 2021-04-29 |
| [How regulation is failing to electrify Europe's van market](how-regulation-is-failing-to-electrify-europe-s-van-market.md) | 2021-05-10 |
| [E-kerosene mandate: key steps for ReFuelEU success](e-kerosene-mandate-key-steps-for-refueleu-success.md) | 2021-05-11 |
| [How to make Europe's green fuels law truly green](how-to-make-europe-s-green-fuels-law-truly-green.md) | 2021-05-27 |
| [Private jets: can the super-rich supercharge zero-emission aviation?](private-jets-can-the-super-rich-supercharge-zero-emission-aviation.md) | 2021-05-27 |
| [Rising use of private jets sends CO2 emissions soaring](rising-use-of-private-jets-sends-co2-emissions-soaring.md) | 2021-05-27 |
| [Germany raises climate target following 'epoch-making' supreme court decision](germany-raises-climate-target-following-epoch-making-supreme-court-decision.md) | 2021-05-28 |
| [The UK's green jet fuel mandate needs robust sustainability criteria](the-uk-s-green-jet-fuel-mandate-needs-robust-sustainability-criteria-to-set-avia.md) | 2021-06-15 |
| [Next steps for the UK's Air Passenger Duty](next-steps-for-the-uk-s-air-passenger-duty.md) | 2021-06-24 |
| [Easyjet's new domestic routes fly in the face of environmental spin](easyjet-s-new-domestic-routes-fly-in-the-face-of-environmental-spin.md) | 2021-06-29 |
| [The five tests awaiting the EU's big 'Fit for 55' climate push](the-five-tests-awaiting-the-eu-s-big-fit-for-55-climate-push.md) | 2021-06-29 |
| [Now is the time for an ambitious European e-kerosene target](now-is-the-time-for-an-ambitious-european-e-kerosene-target.md) | 2021-07-02 |
| [Why direct air capture holds one of the keys to sustainable aviation](why-direct-air-capture-holds-one-of-the-keys-to-sustainable-aviation.md) | 2021-07-06 |
| [EU axes airlines' fuel tax exemption in drive for greener fuels](eu-axes-airlines-fuel-tax-exemption-in-drive-for-greener-fuels.md) | 2021-07-14 |
| [Decades of inaction on flying's climate impact are being replaced by action. But does it go far enough?](decades-of-inaction-on-flying-s-climate-impact-are-being-replaced-by-action-but-.md) | 2021-07-15 |
| [What the EU's climate plan means for Europe](what-the-eu-s-climate-plan-means-for-europe.md) | 2021-07-15 |
| [Aviation's CO2: use it or bury it?](aviation-s-co2-use-it-or-bury-it.md) | 2021-08-06 |
| [Jet Zero: our strategy for net zero aviation in the UK](jet-zero-our-strategy-for-net-zero-aviation-in-the-uk.md) | 2021-09-20 |
| [LNG trucks: a dead-end bridge](lng-trucks-a-dead-end-bridge.md) | 2021-09-27 |
| [Why airline net zero commitments aren't green at all](why-airline-net-zero-commitments-aren-t-green-at-all.md) | 2021-10-28 |
| [Aviation's climate pledges contradicted by huge growth forecasts](aviation-s-climate-pledges-contradicted-by-huge-growth-forecasts.md) | 2021-11-26 |
| [Germany confirms end of combustion engine era – but doesn't say how](germany-confirms-end-of-combustion-engine-era-but-doesn-t-say-how.md) | 2021-11-26 |
| [EU truck targets too weak to incentivise transition to zero-emission vehicles](eu-truck-targets-too-weak-to-incentivise-transition-to-zero-emission-vehicles.md) | 2021-10-10 |
| [Transport target pathways: a study by T&E Germany and Prognos](zielpfade-verkehr-eine-studie-von-t-e-deutschland-und-prognos-ber-sozial-gerecht.md) | 2021-10-26 |
| [Lift off for e-kerosene at first commercial factory](lift-off-for-e-kerosene-at-first-commercial-factory.md) | 2021-10-28 |
| [The EU's green fuels law: A clean shift for EU transport fuels?](the-eu-s-green-fuels-law-a-clean-shift-for-eu-transport-fuels.md) | 2021-11-26 |
| [EU's hydrogen plan would heap additional pressure on energy prices](eu-s-hydrogen-plan-would-heap-additional-pressure-on-energy-prices.md) | 2021-12-01 |
| [Magic green fuels: Why synthetic fuels in cars will not solve Europe's pollution problems](magic-green-fuels-why-synthetic-fuels-in-cars-will-not-solve-europe-s-pollution-.md) | 2021-12-06 |
| [The road to a road ETS](the-road-to-a-road-ets-how-to-design-a-socially-fair-and-environmentally-effecti.md) | 2021-12-15 |

## Next batch

Continue from the next unprocessed row of `wiki/sources/index.md` after 2021-12-15 — check that
table for the current row order, since it's regenerated by `2_refresh_wiki_index.py` and may
reflow as new sources are added.
