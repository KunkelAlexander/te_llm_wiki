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

## Batch 8 (done 2026-07-20) — next 10 sources by date (2021-12-16 through 2022-03-14)

All full treatments except assessment-of-carbon-leakage-potential-for-european-aviation, whose
scraped fulltext is only the short intro abstract (the full study text is captured instead under
its companion press-release page, would-airlines-benefit-from-evading-eu-climate-measures — noted
as such on both pages).

| Source | Date |
|---|---|
| [Made-in-Brussels laws will make or break the global climate fight](made-in-brussels-laws-will-make-or-break-the-global-climate-fight.md) | 2021-12-16 |
| [Assessment of carbon leakage potential for European aviation](assessment-of-carbon-leakage-potential-for-european-aviation.md) | 2022-01-06 |
| [Would airlines benefit from evading EU climate measures?](would-airlines-benefit-from-evading-eu-climate-measures.md) | 2022-01-06 |
| [The good, bad and the ugly of SAF mandates](the-good-bad-and-the-ugly-of-saf-mandates.md) | 2022-01-31 |
| [Airlines, NGOs unite behind push for clean jet fuels in Europe](airlines-ngos-unite-behind-push-for-clean-jet-fuels-in-europe.md) | 2022-02-01 |
| [Airlines call for an end to loopholes in carbon market and back European climate measures](airlines-call-for-an-end-to-loopholes-in-carbon-market-and-back-european-climate.md) | 2022-02-04 |
| [How to drive the uptake of sustainable fuels in European shipping](how-to-drive-the-uptake-of-sustainable-fuels-in-european-shipping.md) | 2022-02-16 |
| [How can ReFuelEU enable investment in direct air capture?](how-can-refueleu-enable-investment-in-direct-air-capture.md) | 2022-03-07 |
| [Why 'flying less' offers the best path to sustainable aviation](why-flying-less-offers-the-best-path-to-sustainable-aviation.md) | 2022-03-08 |
| [Can we count on zero-emissions planes and ships?](can-we-count-on-zero-emissions-planes-and-ships.md) | 2022-03-14 |

## Batch 9 (done 2026-07-20) — next 10 sources by date (2022-03-14 through 2022-05-31)

All full treatments. Two pairs of sources (air-france-annonce/lufthansa-wirbt, and the German
"der-wahre-klimaeffekt" report) are FR/DE T&E national-office publications of English-language
T&E work — noted as such and cross-linked rather than treated as fully independent duplicates.
One data-quality note: europe-s-largest-airlines-claim-net-zero-future's primary doc_id has
mismatched scraped fulltext (the industry's own "Destination 2050" report, not T&E's briefing);
the summary was written from the correctly-matched companion doc_id instead — flagged on that page.

| Source | Date |
|---|---|
| [How long will flying less remain the best way to reduce aviation's climate impact?](how-long-will-flying-less-remain-the-best-way-to-reduce-aviation-s-climate-impac.md) | 2022-03-14 |
| [How to decarbonise aviation in Europe by 2050?](comment-d-carboner-l-aviation-en-europe-d-ici-2050.md) | 2022-03-29 |
| [The true climate effect of German air and sea transport](der-wahre-klimaeffekt-des-deutschen-luft-und-seeverkehrs.md) | 2022-03-29 |
| [Air France announces a zero-emission future while lobbying to weaken EU climate laws](air-france-annonce-un-avenir-z-ro-mission-tout-en-att-nuant-les-lois-de-l-ue-sur.md) | 2022-04-07 |
| [Europe's largest airlines claim net zero future whilst lobbying to weaken EU's climate laws](europe-s-largest-airlines-claim-net-zero-future-whilst-lobbying-to-weaken-eu-s-c.md) | 2022-04-07 |
| [Lufthansa advertises a climate-neutral future while working to weaken EU climate rules](lufthansa-wirbt-mit-klimaneutraler-zukunft-bem-ht-sich-aber-gleichzeitig-um-eine.md) | 2022-04-07 |
| [Mitigating aviation's non-CO2 effects in the EU's Fit for 55 package](mitigating-aviation-s-non-co2-effects-in-the-eu-s-fit-for-55-package.md) | 2022-04-19 |
| [Is it possible to fly to New York without emitting CO2?](is-it-possible-to-fly-to-new-york-without-emitting-co2.md) | 2022-04-28 |
| [Europe's chance to say bye to fossil fuels](europe-s-chance-to-say-bye-to-fossil-fuels.md) | 2022-05-05 |
| [What the EU climate plan means for aviation fuel](what-the-eu-climate-plan-means-for-aviation-fuel.md) | 2022-05-31 |

## Batch 10 (done 2026-07-21) — next 10 sources by date (2022-06-02 through 2022-07-06)

All full treatments. One pair (analysis-of-green-jet-fuel-production-in-europe /
green-aviation-fuels-could-save-5-million-tonnes-of-co2-in-2030) are the November-2022-updated vs.
original June-2022 versions of the same e-kerosene tracker briefing — summarised separately since
the figures differ, with cross-links. refueleu-aviation-t-e-s-recommendations-on-the-biofuel-definition
has only a short-abstract scraped fulltext; its full content is captured instead in the companion
joint letter with easyJet (airline-and-green-ngo-urge-meps-to-exclude-palm-oil-by-products...).

| Source | Date |
|---|---|
| [More ambitious European carbon market could slash aviation emissions by an extra 53%](more-ambitious-european-carbon-market-could-slash-aviation-emissions-by-an-extra.md) | 2022-06-02 |
| [A carbon market that works for the climate and industry](a-carbon-market-that-works-for-the-climate-and-industry.md) | 2022-06-03 |
| [Analysis of green jet fuel production in Europe](analysis-of-green-jet-fuel-production-in-europe.md) | 2022-06-09 |
| [Green aviation fuels could save 5 million tonnes of CO2 in 2030](green-aviation-fuels-could-save-5-million-tonnes-of-co2-in-2030.md) | 2022-06-09 |
| [Getting hydrogen right from the start](getting-hydrogen-right-from-the-start.md) | 2022-06-24 |
| [The small price to pay to clean up shipping](the-small-price-to-pay-to-clean-up-shipping.md) | 2022-06-28 |
| [EU governments approve extension of polluter pays principle](eu-governments-approve-extension-of-polluter-pays-principle.md) | 2022-06-29 |
| [EU set for major expansion of carbon market](eu-set-for-major-expansion-of-carbon-market.md) | 2022-06-30 |
| [ReFuelEU Aviation: T&E's recommendations on the biofuel definition](refueleu-aviation-t-e-s-recommendations-on-the-biofuel-definition.md) | 2022-07-01 |
| [Airline and green NGO urge MEPs to exclude palm oil by-products from European aviation](airline-and-green-ngo-urge-meps-to-exclude-palm-oil-by-products-from-european-av.md) | 2022-07-06 |

## Batch 11 (done 2026-07-21) — next 10 sources by date (2022-07-06 through 2022-10-07)

All full treatments. fuels-linked-to-deforestation-and-food-price-increases-risk-flooding... has
only a short-abstract scraped fulltext, cross-linked to its full-content companion (the joint
letter with easyJet from the prior batch). deux-euros-suffisent (T&E France) is the methodology
annex behind un-body-icao-hails-empty-goal's headline figures — summarised as a companion pair.

| Source | Date |
|---|---|
| [Fuels linked to deforestation and food price increases risk flooding the European aviation market](fuels-linked-to-deforestation-and-food-price-increases-risk-flooding-the-europea.md) | 2022-07-06 |
| [EU lawmakers stop controversial biofuels from fuelling planes](eu-lawmakers-stop-controversial-biofuels-from-fuelling-planes.md) | 2022-07-07 |
| [Scaling up Direct Air Capture](scaling-up-direct-air-capture.md) | 2022-07-20 |
| [Europe gets one step closer to a green flight](europe-gets-one-step-closer-to-a-green-flight.md) | 2022-07-25 |
| [Two euros are enough to "green" a flight to New York under the UN's aviation programme](deux-euros-suffisent-verdir-un-vol-pour-new-york-avec-le-programme-de-l-onu-pour.md) | 2022-09-23 |
| [The most important piece of EU climate law you've never heard of](the-most-important-piece-of-eu-climate-law-you-ve-never-heard-of.md) | 2022-09-28 |
| [A football star's Marie Antoinette moment and an uprising against private jets](a-football-star-s-marie-antoinette-moment-and-an-uprising-against-private-jets.md) | 2022-09-30 |
| [Industrial policy is not a relic of the past but key to winning the green energy race](industrial-policy-is-not-a-relic-of-the-past-but-key-to-winning-the-green-energy.md) | 2022-09-30 |
| [A drop of e-fuel in an ocean of oil](a-drop-of-e-fuel-in-an-ocean-of-oil.md) | 2022-10-04 |
| [UN body ICAO hails empty goal and cheap offsetting scheme to 'green' aviation](un-body-icao-hails-empty-goal-and-cheap-offsetting-scheme-to-green-aviation.md) | 2022-10-07 |

## Batch 12 (done 2026-07-21) — next 10 sources by date (2022-10-20 through 2023-01-23)

All full treatments. "Oil companies invest 8 times more in biofuels than in hydrogen" (T&E France)
has a mismatched primary doc_id (its scraped fulltext is the full underlying Ricardo Energy &
Environment refineries study, ~292k chars) — summarised from that study's executive summary rather
than treated as a data-quality gap, since it genuinely is the source report behind the headline claim.

| Source | Date |
|---|---|
| [Third time lucky? RED III trilogue another opportunity to move beyond unsustainable fuels](third-time-lucky-red-iii-trilogue-another-opportunity-to-move-beyond-unsustainab.md) | 2022-10-20 |
| [FAQ: Non-CO2 mitigation measures in ReFuelEU and EU ETS](faq-non-co2-mitigation-measures-in-refueleu-and-eu-ets.md) | 2022-10-24 |
| [Majority of employees expect top executives to set corporate flying reduction targets – new survey](majority-of-employees-expect-top-executives-to-set-corporate-flying-reduction-ta.md) | 2022-11-03 |
| [Running a truck on e-diesel costs 47% more than its battery-electric counterpart](running-a-truck-on-e-diesel-costs-47-more-than-its-battery-electric-counterpart.md) | 2022-11-15 |
| [Tankering in aviation](tankering-in-aviation.md) | 2022-11-22 |
| [Global Powerfuels Alliance and Transport & Environment call for an ambitious e-kerosene target](global-powerfuels-alliance-and-transport-environment-call-for-an-ambitious-e-ker.md) | 2022-11-29 |
| [EU aviation deal will see another lost decade in tackling emissions](eu-aviation-deal-will-see-another-lost-decade-in-tackling-emissions.md) | 2022-12-07 |
| [Aviation's ivory tower may be starting to fall](aviation-s-ivory-tower-may-be-starting-to-fall.md) | 2022-12-16 |
| [Oil companies invest 8 times more in biofuels than in hydrogen](les-groupes-p-troliers-investissent-8-fois-plus-dans-les-biocarburants-que-dans-.md) | 2023-01-11 |
| [Why we need an e-fuel mandate for ships](why-we-need-an-e-fuel-mandate-for-ships.md) | 2023-01-23 |

## Batch 13 (done 2026-07-21) — next 10 sources by date (2023-02-17 through 2023-04-26)

All full treatments. Two FR/DE pairs of near-duplicate national-office publications
(e-fuels-un-plein-d-essence.../over-200-to-fill-up-a-car..., and the two ReFuelEU final-deal
announcements) summarised separately but cross-linked rather than treated as independent sources.

| Source | Date |
|---|---|
| [EU investment rules will greenwash 90% of Airbus' polluting planes](eu-investment-rules-will-greenwash-90-of-airbus-polluting-planes.md) | 2023-02-17 |
| [EU taxonomy for aviation: Will Von der Leyen rubber stamp the biggest act of aviation greenwashing in decades?](eu-taxonomy-for-aviation-will-von-der-leyen-rubber-stamp-the-biggest-act-of-avia.md) | 2023-02-20 |
| [The easy fix to air pollution linked to planes](the-easy-fix-to-air-pollution-linked-to-planes.md) | 2023-02-28 |
| [85% of global companies don't have credible plans to reduce corporate flying emissions](85-of-global-companies-don-t-have-credible-plans-to-reduce-corporate-flying-emis.md) | 2023-03-15 |
| [E-fuels: a full tank of petrol around 50% more expensive if Germany gets its way](e-fuels-un-plein-d-essence-environ-50-plus-cher-si-l-allemagne-obtient-gain-de-c.md) | 2023-03-22 |
| [Over €200 to fill up a car – the cost of Germany's bid to keep combustion engines](over-200-to-fill-up-a-car-the-cost-of-germany-s-bid-to-keep-combustion-engines.md) | 2023-03-23 |
| [Consultation response to the CAA's call for evidence on consumer environmental information](consultation-response-to-the-caa-s-call-for-evidence-on-consumer-environmental-i.md) | 2023-04-03 |
| [Will the aviation sector replicate Big Oil's playbook?](will-the-aviation-sector-replicate-big-oil-s-playbook.md) | 2023-04-04 |
| [Aviation: the EU agrees one of the world's most ambitious mandates for sustainable fuels](aviation-l-ue-s-accorde-sur-l-un-des-mandats-les-plus-ambitieux-au-monde-en-mati.md) | 2023-04-26 |
| [EU adopts world's largest regulation for green fuels in aviation](eu-beschlie-t-weltweit-gr-te-verordnung-f-r-gr-ne-kraftstoffe-in-der-luftfahrt.md) | 2023-04-26 |

## Batch 14 (done 2026-07-21) — next 10 sources by date (2023-04-26 through 2023-06-19)

All full treatments. Four ES/EN/FR/DE national-office near-duplicates of the same underlying
studies (the ReFuelEU final-deal announcement, and the Cerulogy animal-fats report "Pigs do fly")
summarised separately but cross-linked to the fullest version rather than treated as independent.

| Source | Date |
|---|---|
| [La Unión Europea acuerda la adopción del mandato más ambicioso del mundo en materia de combustibles verdes para la aviación](la-uni-n-europea-acuerda-la-adopci-n-del-mandato-m-s-ambicioso-del-mundo-en-mate.md) | 2023-04-26 |
| [How the EU can get its Net Zero Industrial Act right](how-the-eu-can-get-its-net-zero-industrial-act-right.md) | 2023-05-04 |
| [National Energy and Climate Plans: how to deliver zero emission transport](national-energy-and-climate-plans-how-to-deliver-zero-emission-transport.md) | 2023-05-16 |
| [Operating a hydrogen aircraft could be less costly than a conventional aircraft by 2035](exploiter-un-avion-hydrog-ne-pourrait-tre-moins-co-teux-qu-un-avion-traditionnel.md) | 2023-05-22 |
| [The use of animal fats in cars and planes is becoming less and less sustainable](l-utilisation-de-graisses-animales-dans-les-voitures-et-les-avions-est-de-moins-.md) | 2023-05-31 |
| ['Pigs do fly': Growing use of animal fats in cars and planes increasingly unsustainable](pigs-do-fly-growing-use-of-animal-fats-in-cars-and-planes-increasingly-unsustain.md) | 2023-05-31 |
| [Pigs do fly: the rise of animal fats in European transport](pigs-do-fly-the-rise-of-animal-fats-in-european-transport.md) | 2023-05-31 |
| ["Pigs can fly after all": use of animal fats to power cars and planes increasingly unsustainable](schweine-k-nnen-doch-fliegen-einsatz-von-tierfetten-zum-betrieb-von-autos-und-fl.md) | 2023-05-31 |
| [How to improve ESG ratings](how-to-improve-esg-ratings.md) | 2023-06-14 |
| [Ready or not: Who are the frontrunners in the global race to clean up trucks?](ready-or-not-who-are-the-frontrunners-in-the-global-race-to-clean-up-trucks.md) | 2023-06-19 |

## Batch 15 (done 2026-07-21) — next 10 sources by date (2023-07-06 through 2024-02-21)

All full treatments. Note a ~5-month gap in the source index between 2023-07-12 and 2023-12-14
(no sources published/indexed in that window) — not a skipped batch.

| Source | Date |
|---|---|
| [How the EU's car scrapyard law can bring clean steel and aluminium to Europe](how-the-eu-s-car-scrapyard-law-can-bring-clean-steel-and-aluminium-to-europe.md) | 2023-07-06 |
| [Setting 2040 climate ambition](setting-2040-climate-ambition.md) | 2023-07-11 |
| [Tax exemptions for aviation: German government forewent four billion euros in 2022](steuerausnahmen-f-r-den-luftverkehr-bundesregierung-hat-sich-2022-vier-milliarde.md) | 2023-07-12 |
| [Europe's massive dependence on used cooking oil imports raises fears of fraud](la-gigantesque-d-pendance-de-l-europe-aux-importations-d-huile-de-cuisson-usag-e.md) | 2023-12-14 |
| [E-fuels for planes: with 45 projects, is the EU on track to meet its targets?](e-fuels-for-planes-with-45-projects-is-the-eu-on-track-to-meet-its-targets.md) | 2024-01-24 |
| [What Europe needs to learn from the German debt brake fiasco](what-europe-needs-to-learn-from-the-german-debt-brake-fiasco.md) | 2024-02-01 |
| [EU sets historic target to reduce emissions by 2040 but transport sector puts target at risk](eu-sets-historic-target-to-reduce-emissions-by-2040-but-transport-sector-puts-ta.md) | 2024-02-06 |
| [Europe's hydrogen plans reliant on uncertain imports – report](europe-s-hydrogen-plans-reliant-on-uncertain-imports-report.md) | 2024-02-13 |
| [Hydrogen hype: Why the EU should be cautious about uncertain imports from far-flung places](hydrogen-hype-why-the-eu-should-be-cautious-about-uncertain-imports-from-far-flu.md) | 2024-02-13 |
| [On Thin Ice: Norway's Fossil Ambitions and the EU's Green Energy Future](on-thin-ice-norway-s-fossil-ambitions-and-the-eu-s-green-energy-future.md) | 2024-02-21 |

## Batch 16 (done 2026-07-21) — next 10 sources by date (2024-02-22 through 2024-05-02)

All full treatments except leading-environment-and-climate-organisations-score-european-parliament-s-perfor,
a joint five-NGO EU Parliament voting scoreboard whose scraped fulltext is a long country-by-country
data dump — summarised at methodology/top-line level only, per the "if in doubt, leave it out" guidance
on granular content. One companion pair (from-farm-to-fuel-inside-eni-s-african-biofuels-gamble, the
full investigative report, and uncovered-italian-oil-giant-s-african-biofuels-gamble-falls-short, its
press-release announcement) and one pair (making-evs-fit-for-the-future, the full T&E/IMT/BEUC briefing,
and a-streamlined-ev-eco-score-would-encourage-green-made-in-europe-electric-cars, the shorter op-ed
version) summarised separately but cross-linked.

| Source | Date |
|---|---|
| [How is e-kerosene developing in Europe?](how-is-e-kerosene-developing-in-europe.md) | 2024-02-22 |
| [From Farm to Fuel: inside Eni's African biofuels gamble](from-farm-to-fuel-inside-eni-s-african-biofuels-gamble.md) | 2024-02-24 |
| [Uncovered: Italian oil giant's African biofuels gamble falls short](uncovered-italian-oil-giant-s-african-biofuels-gamble-falls-short.md) | 2024-02-24 |
| [Europe's transport sector set to make up almost half of the continent's emissions in 2030](europe-s-transport-sector-set-to-make-up-almost-half-of-the-continent-s-emission.md) | 2024-03-20 |
| [Leading environment and climate organisations score European Parliament's performance on protecting the Green Deal](leading-environment-and-climate-organisations-score-european-parliament-s-perfor.md) | 2024-04-12 |
| [Low cost airlines pollute more than ever, latest emissions data shows](low-cost-airlines-pollute-more-than-ever-latest-emissions-data-shows.md) | 2024-04-19 |
| [Making EVs fit for the future](making-evs-fit-for-the-future.md) | 2024-04-22 |
| [Towards a €1 trillion package for Europe](towards-a-1-trillion-package-for-europe.md) | 2024-04-23 |
| [A streamlined EV 'eco-score' would encourage green, made-in-Europe electric cars](a-streamlined-ev-eco-score-would-encourage-green-made-in-europe-electric-cars.md) | 2024-04-24 |
| [Plane to see](plane-to-see.md) | 2024-05-02 |

## Batch 17 (done 2026-07-21) — next 10 sources by date (2024-05-06 through 2024-06-25)

All full treatments. Two companion pairs: uco-unknown-cooking-oil-high-hopes-on-limited-and-suspicious-materials
(the commissioned Stratas Advisors trade-data study) and l-huile-de-cuisson-usagee (T&E's own briefing built on
that data) summarised separately but cross-linked. what-has-the-eu-done-for-the-planet-and-its-citizens is
another joint 5-NGO pre-election publication (like the Batch 16 EU Parliament scoreboard) covering 10 broad
topics — summarised only for its transport-relevant (electromobility/rail) sections, per "if in doubt, leave
it out." les-particules-ultrafines-...'s scraped fulltext is the underlying English-language T&E briefing
("Can living near an airport make you ill?") rather than France-specific text — noted as such on that page.

| Source | Date |
|---|---|
| [What has the EU done for the planet and its citizens?](what-has-the-eu-done-for-the-planet-and-its-citizens.md) | 2024-05-06 |
| [Europe-Asia Green Corridors](europe-asia-green-corridors.md) | 2024-05-24 |
| [Who could finance e-kerosene production in Germany?](wer-k-nnte-die-e-kerosin-produktion-in-deutschland-finanzieren.md) | 2024-05-29 |
| [Double or quits for climate president Von der Leyen](double-or-quits-for-climate-president-von-der-leyen.md) | 2024-05-31 |
| [E-Fuels observatory for shipping](e-fuels-observatory-for-shipping.md) | 2024-06-03 |
| [Euro 2024: teams could cut their emissions by 60% by avoiding flying](euro-2024-les-quipes-peuvent-r-duire-leurs-missions-de-60-en-vitant-de-prendre-l.md) | 2024-06-04 |
| [Used cooking oil: from miracle fuel to fear of fraud](l-huile-de-cuisson-usag-e-du-carburant-miracle-la-crainte-de-la-fraude.md) | 2024-06-18 |
| [UCO (Unknown Cooking Oil): High hopes on limited and suspicious materials](uco-unknown-cooking-oil-high-hopes-on-limited-and-suspicious-materials.md) | 2024-06-18 |
| [Making the EU single market work for the Green Deal](making-the-eu-single-market-work-for-the-green-deal.md) | 2024-06-24 |
| [Ultrafine particles from aircraft pose a health risk to 11 million French people](les-particules-ultrafines-des-avions-font-peser-un-risque-sur-la-sant-de-11-mill.md) | 2024-06-25 |

## Batch 18 (done 2026-07-21) — next 10 sources by date (2024-07-01 through 2024-10-21)

All full treatments. One companion pair (cleaning-up-steel-in-cars-why-and-how, the full T&E/Ricardo
report, and its German-office press release gr-ner-stahl-...) summarised separately but cross-linked.
e-kerosene-providers-call-upon-the-german-government-... bundles three related documents under one
source page (the open letter, a short T&E news summary, and a 2023 legal opinion by Prof. Pache listed
as its PDF) — all three summarised together, noted as such on that page.

| Source | Date |
|---|---|
| [How sustainable are advanced and waste biofuels?](how-sustainable-are-advanced-and-waste-biofuels.md) | 2024-07-01 |
| [Cleaning up steel in cars: why and how?](cleaning-up-steel-in-cars-why-and-how.md) | 2024-07-10 |
| [Green steel can cut the climate impact of car production for just €57 per car](gr-ner-stahl-kann-die-klimaauswirkungen-der-autoproduktion-f-r-nur-57-euro-pro-a.md) | 2024-07-10 |
| [How EU states can tackle unsustainable biofuels and promote cleaner alternatives?](how-eu-states-can-tackle-unsustainable-biofuels-and-promote-cleaner-alternatives.md) | 2024-09-02 |
| [E-kerosene providers call upon the German government to keep the country's quotas for green jet fuel](e-kerosene-providers-call-upon-the-german-government-to-keep-the-country-s-quota.md) | 2024-09-16 |
| [Joint call for an EU-wide vehicle environmental score to support the industrial transition](joint-call-for-an-eu-wide-vehicle-environmental-score-to-support-the-industrial-.md) | 2024-09-25 |
| [What Draghi didn't say](what-draghi-didn-t-say.md) | 2024-09-30 |
| [Implementing the EU's e-SAF mandate](implementing-the-eu-s-e-saf-mandate.md) | 2024-10-01 |
| [Rail and clean industry players join forces with NGOs to call for the introduction of a fuel tax for planes and ships](rail-and-clean-industry-players-join-forces-with-ngos-to-call-for-the-introducti.md) | 2024-10-18 |
| [T&E response to the public consultation on the Flight Emissions Label](t-e-response-to-the-public-consultation-on-the-flight-emissions-label.md) | 2024-10-21 |

## Batch 19 (done 2026-07-21) — next 10 sources by date (2024-10-24 through 2024-12-03)

All full treatments. Two companion pairs: aviation-r-duire-l-impact-climatique-des-tra-n-es (T&E's
French-office contrail-avoidance briefing) and aviation-international-scientists-warn-... (the follow-up
scientists' open letter citing that briefing's figures); and seulement-10-compagnies-a-riennes (French)
and lkonzerne-und-fluggesellschaften-verschleppen (German) — both national-office pieces covering the
same global airline SAF ranking, cross-linked rather than treated as independent.

| Source | Date |
|---|---|
| [IMO and sustainable fuels criteria](imo-and-sustainable-fuels-criteria.md) | 2024-10-24 |
| [T&E position paper on the End-of-life Vehicles Regulation](t-e-position-paper-on-the-end-of-life-vehicles-regulation.md) | 2024-10-30 |
| [What investments are needed to green Europe's transport sector?](what-investments-are-needed-to-green-europe-s-transport-sector.md) | 2024-11-04 |
| [T&E's take on the EU Transport Commissioner's hearing](t-e-s-take-on-the-eu-transport-commissioner-s-hearing.md) | 2024-11-04 |
| [Aviation: reducing the climate impact of contrails would cost less than 4 euros per flight](aviation-r-duire-l-impact-climatique-des-tra-n-es-de-condensation-co-terait-moin.md) | 2024-11-13 |
| [Aviation: International scientists warn of warming impact of contrails and risks of delaying action](aviation-international-scientists-warn-of-warming-impact-of-contrails-and-risks-.md) | 2024-11-20 |
| [Fuels for cars: a dead end for industry, consumers and the environment](fuels-for-cars-a-dead-end-for-industry-consumers-and-the-environment.md) | 2024-11-27 |
| [Coming soon: Your European train ticket with just one click](coming-soon-your-european-train-ticket-with-just-one-click.md) | 2024-11-28 |
| [Seulement 10 compagnies aériennes, dont Air France-KLM, investissent sérieusement dans les carburants alternatifs](seulement-10-compagnies-a-riennes-dont-air-france-klm-investissent-s-rieusement-.md) | 2024-12-03 |
| [Oil companies and airlines are delaying investments in e-kerosene](lkonzerne-und-fluggesellschaften-verschleppen-investitionen-in-e-kerosin.md) | 2024-12-03 |

## Batch 20 (done 2026-07-21) — next 10 sources by date (2024-12-04 through 2025-01-13)

All full treatments. Two source pages had "no abstract available" placeholders fixed as part of this
batch (used-cooking-oil-the-certified-unknown, green-aviation-s-make-or-break-moment). One companion
pair: down-to-earth (the full "Down to Earth" report — whose own scraped fulltext is only its short
recommendations excerpt) and aviation-industry-plans-for-growth-irreconcilable-with-europe-s-climate-goals
(the press release, whose scraped fulltext happens to contain the full report body) — the rich summary
was written on down-to-earth.md using that press-release page's fulltext, with the press release itself
left as a short pointer. carbon-market-revenues-can-fund-green-fuels-for-shipping-and-aviation bundles
T&E's own briefing together with the underlying commissioned Ricardo technical study under one source
page (three doc_ids) — summarised together.

| Source | Date |
|---|---|
| [Building back better: Ukraine's transport infrastructure](building-back-better-ukraine-s-transport-infrastructure.md) | 2024-12-04 |
| [Trenitalia classée meilleure compagnie ferroviaire d'Europe, Eurostar en dernière position](trenitalia-class-e-meilleure-compagnie-ferroviaire-d-europe-eurostar-en-derni-re.md) | 2024-12-09 |
| [Used Cooking Oil: The Certified Unknown](used-cooking-oil-the-certified-unknown.md) | 2024-12-11 |
| [Carbon market revenues can fund green fuels for shipping and aviation](carbon-market-revenues-can-fund-green-fuels-for-shipping-and-aviation.md) | 2024-12-16 |
| [Reducing emissions from non-road mobile machinery](reducing-emissions-from-non-road-mobile-machinery.md) | 2024-12-19 |
| [Green aviation's make or break moment](green-aviation-s-make-or-break-moment.md) | 2024-12-20 |
| [Make, buy, protect Europe](make-buy-protect-europe.md) | 2024-12-20 |
| [Aviation fuels and emissions trading - T&E consultation response](aviation-fuels-and-emissions-trading-t-e-consultation-response.md) | 2025-01-08 |
| [Aviation industry plans for growth 'irreconcilable' with Europe's climate goals](aviation-industry-plans-for-growth-irreconcilable-with-europe-s-climate-goals.md) | 2025-01-13 |
| [Down to earth](down-to-earth.md) | 2025-01-13 |

## Batch 21 (done 2026-07-21) — next 10 sources by date (2025-01-13 through 2025-02-17)

All full treatments. la-croissance-du-transport-a-rien... is French-office coverage of the same "Down to
Earth" report covered in Batch 20 (title/quote translated per language-handling rules, not previously
done). agenda-klimaneutraler-luftverkehr (German) and quel-avenir-fiscal-pour-le-score-environnemental
(French, whose fulltext is a commissioned WTO/EU-law legal memo) also had their titles/quotes translated
for the first time as part of this batch. Two companion pairs: shipping-companies-call-for-limits-on-
biofuels-in-shipping and un-shipping-body-s-green-fuels-law-could-worsen (same-day industry letter +
Cerulogy study press release); t-e-shipping-and-aviation-industry-jointly-call-for-urgent-action (single
page bundling 2 near-identical doc_ids for the same ECSA/A4E/T&E joint statement).

| Source | Date |
|---|---|
| [Growth in air transport will destroy the sector's climate targets](la-croissance-du-transport-a-rien-an-antira-les-objectifs-climatiques-du-secteur.md) | 2025-01-13 |
| [Agenda for climate-neutral aviation](agenda-klimaneutraler-luftverkehr.md) | 2025-01-16 |
| [What fiscal future for the environmental score (éco-score)?](quel-avenir-fiscal-pour-le-score-environnemental-co-score.md) | 2025-01-27 |
| [How to take the risk out of hydrogen investments](how-to-take-the-risk-out-of-hydrogen-investments.md) | 2025-02-03 |
| [Joint letter for the Clean Industrial Deal to deliver on decarbonisation and competitiveness](joint-letter-for-the-clean-industrial-deal-to-deliver-on-decarbonisation-and-com.md) | 2025-02-05 |
| [T&E, shipping and aviation industry jointly call for urgent action to ramp up clean fuel production](t-e-shipping-and-aviation-industry-jointly-call-for-urgent-action-to-ramp-up-cle.md) | 2025-02-13 |
| [A European Hydrogen Clearing House for green maritime and aviation e-fuels](a-european-hydrogen-clearing-house-for-green-maritime-and-aviation-e-fuels.md) | 2025-02-13 |
| [NGOs, waste managers and recyclers urge policy makers to stick with ambitious targets for recycled plastics in new cars](ngos-waste-managers-and-recyclers-urge-policy-makers-to-stick-with-ambitious-tar.md) | 2025-02-14 |
| [Shipping companies call for limits on biofuels in shipping](shipping-companies-call-for-limits-on-biofuels-in-shipping.md) | 2025-02-17 |
| [UN shipping body's green fuels law could worsen the sector's climate impact - study](un-shipping-body-s-green-fuels-law-could-worsen-the-sector-s-climate-impact-stud.md) | 2025-02-17 |

## Next batch

Continue from the next unprocessed row of `wiki/sources/index.md` after 2025-02-17 — check that
table for the current row order, since it's regenerated by `2_refresh_wiki_index.py` and may
reflow as new sources are added.
