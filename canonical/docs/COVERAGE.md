# Coverage of all eleven requested areas

Coverage below means typed contracts and explicit modeling, not live adapters. All provider blueprints remain unimplemented. The original aggregate counts total 424 before deduplication; their individual rows were not supplied.

| Section | Area | Representative predicate families | Metric definitions mapped |
|---|---|---|---|
| 1 | Careers / ATS and job-description workflow mining | `careers.page`, `careers.ats`, `job.posting`, `job.status`, `job.salary`, `job.work_arrangement`, `job.workflow_statement`, `job.spreadsheet_statement`, `job.crm_statement`, `job.document_statement`, `job.handoff_statement`, `hiring.change_event`, `hiring.measurement` | 6 |
| 2 | SaaS signatures and technographics | `technology.footprint`, `technology.provider_report`, `technology.script`, `technology.form_action`, `technology.network_request`, `technology.csp`, `technology.cookie`, `technology.header`, `technology.subdomain`, `dns.mx.provider`, `dns.cname.service`, `technology.account_identifier`, `technology.cooccurrence`, `technology.measurement` | 3 |
| 3 | Vertical SaaS | `technology.footprint`, `product.vertical`, `product.category`, `product.capability`, `portal.observed`, `integration.public_marker`, `integration.connection.verified` | 0 |
| 4 | Product-review pain priors | `review.record`, `review.statement`, `review.theme_classification`, `review.measurement`, `product.pain_prior` | 10 |
| 5 | Local review and operational pain reports | `review.record`, `review.owner_response`, `review.statement`, `review.theme_classification`, `review.theme_summary`, `review.measurement` | 9 |
| 6 | Forums and industry/vendor communities | `discussion.record`, `discussion.statement`, `discussion.theme_classification`, `product.pain_prior`, `industry.pain_prior`, `research.measurement` | 1 |
| 7 | Traffic and acquisition estimates | `traffic.measurement` | 25 |
| 8 | Commodity provider data | `search.result`, `business.profile_attribute`, `technology.provider_report`, `backlink.record`, `web.mention`, `web.mention_sentiment`, `app.listing`, `shopping.listing`, `advertisement.record`, `seo.measurement`, `app.measurement`, `shopping.measurement`, `ads.measurement`, `review.measurement` | 39 |
| 9 | Vertical public registries | `registry.registration`, `registry.license`, `registry.permit`, `registry.specialty`, `registry.filing`, `registry.affiliation`, `registry.measurement` | 6 |
| 10 | Phone and inbound economics | `technology.footprint`, `phone.cta`, `phone.routing_observed`, `phone.routing_verified`, `phone.recording_verified`, `phone.call_event`, `phone.measurement`, `phone.economics_hypothesis`, `review.statement` | 9 |
| 11 | Website / workflow extraction and inference | `company.self_claim`, `website.business_model_statement`, `website.customer_type_statement`, `website.lead_channel_statement`, `website.document_type_statement`, `website.handoff_statement`, `website.intent_statement`, `website.manual_process_statement`, `website.knowledge_source_statement`, `document.surface`, `form.surface`, `workflow.hypothesis`, `knowledge_complexity.hypothesis` | 0 |

## Important interpretations

Careers/job facts distinguish employer statements from actual operations; desired skills and future plans cannot be upgraded to verified workflow facts. Salaries have separate optional facts with currency, bounds and period.

An observed product marker, an API technology report and a product capability statement are different things. Product support for a capability does not prove account use of that capability.

Product priors and local-review summaries use the same review-record building blocks but retain different subjects. Industry discussions remain industry evidence until a separate eligible link justifies a contextual association.

Traffic estimates retain provider/method/period/dimensions. Commodity source APIs normalize into multiple measurement and record families. Registry fields preserve issuer meaning. Public phone cues do not establish call economics. Website/LLM statements and inferences are separately typed.

Full predicate and metric definitions are in CATALOG.md and METRICS.md. Extending these lists does not require a new service, graph engine or table per predicate.
