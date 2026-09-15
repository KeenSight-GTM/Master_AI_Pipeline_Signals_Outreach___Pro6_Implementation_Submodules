# Full metric catalog — 89 definitions

Metric definitions dispatch MeasurementValue. Dimensions below are required schema keys; extra dimensions are rejected unless registered. The reporting period and timezone also remain part of identity.

| Metric | Unit | Aggregation | Required dimensions | Denominator required | Allowed nature |
|---|---|---|---|---|---|
| `traffic.visits` | count | ESTIMATE | country, device, granularity | False | PROVIDER_ESTIMATE |
| `traffic.unique_visitors` | count | ESTIMATE | country, device, granularity | False | PROVIDER_ESTIMATE |
| `traffic.pageviews` | count | ESTIMATE | country, device, granularity | False | PROVIDER_ESTIMATE |
| `traffic.pages_per_visit` | pages_per_visit | ESTIMATE | country, device, granularity | False | PROVIDER_ESTIMATE |
| `traffic.visit_duration` | seconds | ESTIMATE | country, device, granularity | False | PROVIDER_ESTIMATE |
| `traffic.bounce_rate` | proportion | ESTIMATE | country, device, granularity | False | PROVIDER_ESTIMATE |
| `traffic.growth` | proportion_change | ESTIMATE | country, device, granularity | False | PROVIDER_ESTIMATE |
| `traffic.global_rank` | rank | RANK | country, device, granularity | False | PROVIDER_ESTIMATE |
| `traffic.country_rank` | rank | RANK | country, device, granularity | False | PROVIDER_ESTIMATE |
| `traffic.category_rank` | rank | RANK | country, device, granularity | False | PROVIDER_ESTIMATE |
| `traffic.channel_share` | proportion | ESTIMATE | country, device, granularity, channel | False | PROVIDER_ESTIMATE |
| `traffic.geography_share` | proportion | ESTIMATE | country, device, granularity, visitor_country | False | PROVIDER_ESTIMATE |
| `traffic.popular_page_share` | proportion | ESTIMATE | country, device, granularity, page_url | False | PROVIDER_ESTIMATE |
| `traffic.referral_share` | proportion | ESTIMATE | country, device, granularity, referring_domain | False | PROVIDER_ESTIMATE |
| `traffic.outgoing_share` | proportion | ESTIMATE | country, device, granularity, outgoing_domain | False | PROVIDER_ESTIMATE |
| `traffic.paid_referral_concentration` | proportion | ESTIMATE | country, device, granularity, top_n | False | PROVIDER_ESTIMATE |
| `traffic.audience_overlap` | proportion | ESTIMATE | country, device, granularity, peer_domain, basis | False | PROVIDER_ESTIMATE |
| `traffic.social_source_share` | proportion | ESTIMATE | country, device, granularity, social_network | False | PROVIDER_ESTIMATE |
| `traffic.device_share` | proportion | ESTIMATE | country, device, granularity, device_segment | False | PROVIDER_ESTIMATE |
| `traffic.organic_visits` | count | ESTIMATE | country, device, granularity | False | PROVIDER_ESTIMATE |
| `traffic.paid_visits` | count | ESTIMATE | country, device, granularity | False | PROVIDER_ESTIMATE |
| `traffic.referral_visits` | count | ESTIMATE | country, device, granularity | False | PROVIDER_ESTIMATE |
| `traffic.social_visits` | count | ESTIMATE | country, device, granularity | False | PROVIDER_ESTIMATE |
| `traffic.direct_visits` | count | ESTIMATE | country, device, granularity | False | PROVIDER_ESTIMATE |
| `traffic.search_visits` | count | ESTIMATE | country, device, granularity | False | PROVIDER_ESTIMATE |
| `hiring.open_postings` | count | COUNT | department, country | False | DERIVED_MEASUREMENT |
| `hiring.new_postings` | count | COUNT | department, country | False | DERIVED_MEASUREMENT |
| `hiring.closed_postings` | count | COUNT | department, country | False | DERIVED_MEASUREMENT |
| `hiring.workflow_mention_count` | count | COUNT | department, country | False | DERIVED_MEASUREMENT |
| `hiring.spreadsheet_mention_count` | count | COUNT | department, country | False | DERIVED_MEASUREMENT |
| `hiring.document_mention_count` | count | COUNT | department, country | False | DERIVED_MEASUREMENT |
| `review.count` | count | COUNT | platform, profile_id | False | THIRD_PARTY_REPORT, DERIVED_MEASUREMENT |
| `review.new_reviews` | count | COUNT | platform, profile_id | False | THIRD_PARTY_REPORT, DERIVED_MEASUREMENT |
| `review.owner_responses` | count | COUNT | platform, profile_id | False | THIRD_PARTY_REPORT, DERIVED_MEASUREMENT |
| `review.negative_reviews` | count | COUNT | platform, profile_id | False | THIRD_PARTY_REPORT, DERIVED_MEASUREMENT |
| `review.theme_support_count` | count | COUNT | platform, profile_id | False | THIRD_PARTY_REPORT, DERIVED_MEASUREMENT |
| `review.rating` | rating | MEAN | platform, profile_id, scale_maximum | False | THIRD_PARTY_REPORT, DERIVED_MEASUREMENT |
| `review.response_ratio` | proportion | RATE | platform, profile_id | True | DERIVED_MEASUREMENT |
| `review.negative_share` | proportion | RATE | platform, profile_id | True | DERIVED_MEASUREMENT |
| `review.theme_share` | proportion | RATE | platform, profile_id | True | DERIVED_MEASUREMENT |
| `seo.keyword_count` | count | COUNT | country, engine, device | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT |
| `seo.indexed_pages` | count | COUNT | country, engine, device | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT |
| `seo.backlinks` | count | COUNT | country, engine, device | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT |
| `seo.referring_domains` | count | COUNT | country, engine, device | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT |
| `seo.mentions` | count | COUNT | country, engine, device | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT |
| `seo.broken_links` | count | COUNT | country, engine, device | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT |
| `seo.pages_crawled` | count | COUNT | country, engine, device | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT |
| `seo.local_results_count` | count | COUNT | country, engine, device | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT |
| `seo.organic_rank` | rank | RANK | query, country, engine, device | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT |
| `seo.paid_rank` | rank | RANK | query, country, engine, device | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT |
| `seo.local_rank` | rank | RANK | query, country, engine, device | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT |
| `seo.shopping_rank` | rank | RANK | query, country, engine, device | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT |
| `seo.lcp` | milliseconds | DESCRIPTIVE | country, device, scope_level | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT |
| `seo.inp` | milliseconds | DESCRIPTIVE | country, device, scope_level | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT |
| `seo.cls` | score | DESCRIPTIVE | country, device, scope_level | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT |
| `seo.authority` | score | DESCRIPTIVE | country, device, scope_level | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT |
| `seo.search_volume` | count | ESTIMATE | country, query, engine | False | PROVIDER_ESTIMATE |
| `seo.keyword_difficulty` | score | ESTIMATE | country, query, engine | False | PROVIDER_ESTIMATE |
| `seo.estimated_organic_traffic` | count | ESTIMATE | country, query, engine | False | PROVIDER_ESTIMATE |
| `seo.estimated_paid_traffic` | count | ESTIMATE | country, query, engine | False | PROVIDER_ESTIMATE |
| `seo.cpc` | currency_major | ESTIMATE | country, query, currency | False | PROVIDER_ESTIMATE |
| `seo.ai_citation_share` | proportion | RATE | engine, prompt_set_id, locale | True | DERIVED_MEASUREMENT |
| `registry.providers` | count | COUNT | segment | False | REGISTRY_RECORD, DERIVED_MEASUREMENT |
| `registry.advisers` | count | COUNT | segment | False | REGISTRY_RECORD, DERIVED_MEASUREMENT |
| `registry.locations` | count | COUNT | segment | False | REGISTRY_RECORD, DERIVED_MEASUREMENT |
| `registry.licenses` | count | COUNT | segment | False | REGISTRY_RECORD, DERIVED_MEASUREMENT |
| `registry.permits` | count | COUNT | segment | False | REGISTRY_RECORD, DERIVED_MEASUREMENT |
| `phone.inbound_calls` | count | COUNT | segment | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT, DERIVED_MEASUREMENT |
| `phone.answered_calls` | count | COUNT | segment | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT, DERIVED_MEASUREMENT |
| `phone.missed_calls` | count | COUNT | segment | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT, DERIVED_MEASUREMENT |
| `phone.callbacks` | count | COUNT | segment | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT, DERIVED_MEASUREMENT |
| `phone.voicemail_calls` | count | COUNT | segment | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT, DERIVED_MEASUREMENT |
| `app.reviews` | count | COUNT | segment | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT, DERIVED_MEASUREMENT |
| `app.ratings` | count | COUNT | segment | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT, DERIVED_MEASUREMENT |
| `app.downloads_reported` | count | COUNT | segment | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT, DERIVED_MEASUREMENT |
| `shopping.listings` | count | COUNT | segment | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT, DERIVED_MEASUREMENT |
| `shopping.offers` | count | COUNT | segment | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT, DERIVED_MEASUREMENT |
| `shopping.sellers` | count | COUNT | segment | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT, DERIVED_MEASUREMENT |
| `ads.active_ads` | count | COUNT | segment | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT, DERIVED_MEASUREMENT |
| `ads.creatives` | count | COUNT | segment | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT, DERIVED_MEASUREMENT |
| `technology.products_detected` | count | COUNT | segment | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT, DERIVED_MEASUREMENT |
| `technology.domains_observed` | count | COUNT | segment | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT, DERIVED_MEASUREMENT |
| `technology.cooccurrence_support` | count | COUNT | segment | False | DIRECT_OBSERVATION, THIRD_PARTY_REPORT, DERIVED_MEASUREMENT |
| `registry.aum` | currency_major | DESCRIPTIVE | currency, filing_namespace, form_item | False | REGISTRY_RECORD |
| `phone.missed_call_rate` | proportion | RATE | system_id | True | DERIVED_MEASUREMENT |
| `phone.callback_rate` | proportion | RATE | system_id | True | DERIVED_MEASUREMENT |
| `phone.booking_conversion_rate` | proportion | RATE | system_id | True | DERIVED_MEASUREMENT |
| `phone.callback_delay` | seconds | MEAN | system_id | False | DERIVED_MEASUREMENT |
| `research.theme_share` | proportion | RATE | sample_id, theme_id | True | DERIVED_MEASUREMENT |
