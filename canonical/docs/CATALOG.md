# v4.1 predicate catalog

213 typed definitions. These are contracts, not live adapter inventory.

| Predicate | Nature(s) | Subject kinds | Copy policy | Meaning |
|---|---|---|---|---|
| `vendor.present` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Vendor/SaaS detected (class + canonical entity) |
| `vendor.mentioned` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Vendor referenced in prose (article, blog, footer text) |
| `booking.present` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Online scheduling system present |
| `crm.present` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | CRM detected |
| `esp.present` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Email marketing platform detected |
| `chat.widget.present` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Live-chat / chatbot widget |
| `payment.processor.present` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Payment stack |
| `automation.platform.present` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Make / Zapier / n8n presence |
| `integration.present` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Public integration marker detected or absent only in the declared public capture scope. Not a statement of private connectivity. |
| `website.platform` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | CMS / site-builder |
| `vendor.certification_badge` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Partner / certification tier badges |
| `dns.mx.provider` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Email hosting provider (Google / Microsoft) |
| `dns.dmarc.policy` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | DMARC policy (none / quarantine / reject) |
| `dns.spf.includes` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | SPF include tokens |
| `dns.txt.verification` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Vendor verification TXT tokens |
| `dns.cname.service` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Service subdomain CNAME mappings |
| `cert.new_subdomain` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | New subdomain certificates (temporal) |
| `api.public.present` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Public API surface (docs / OpenAPI) |
| `app.mobile.present` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Mobile app presence + changelog cadence |
| `status.page.present` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Public status page |
| `schema.jsonld.present` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | JSON-LD blocks on homepage |
| `schema.jsonld.types` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | @type values found |
| `schema.subject_binding` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | JSON-LD org node bound to the account's business |
| `content.page_inventory` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Sitemap URL taxonomy (page count, sections) |
| `content.velocity_band` | DERIVED_MEASUREMENT | ORG, LOCATION, BRAND | INTERNAL_ONLY | New/changed pages per window |
| `content.type.present` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Blog / FAQ / pricing / booking pages present |
| `seo.cwv.field` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Core Web Vitals (real-user field data) |
| `seo.indexation` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Indexed page footprint |
| `seo.keyword.footprint` | PROVIDER_ESTIMATE, FIRST_PARTY_STATEMENT | ORG, LOCATION, BRAND | ESTIMATE_ATTRIBUTED | Ranking keyword set |
| `seo.authority` | PROVIDER_ESTIMATE, FIRST_PARTY_STATEMENT | ORG, LOCATION, BRAND | ESTIMATE_ATTRIBUTED | Domain rating / authority |
| `seo.local.presence` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Local pack presence / GBP linkage |
| `seo.ai_visibility.cited_in` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Completed individual AI-search probe measurement. OBSERVED with cited=false is a valid negative result; failed/unexecuted probes are UNKNOWN. |
| `industry.vertical` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Two-level taxonomy: vertical -> subvertical |
| `industry.subvertical` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Subvertical within taxonomy |
| `company.self_claim` | FIRST_PARTY_STATEMENT | ORG, LOCATION, BRAND | ATTRIBUTED_ONLY | Positioning / service claims in own words |
| `company.locations` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Location list / count |
| `company.geo` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Metro / region |
| `company.age_band` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Domain / company age band |
| `identity.binding_evidence` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | INTERNAL_ONLY | Site <-> account binding evidence |
| `firmo.employee_band` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Employee count band |
| `firmo.revenue_band` | PROVIDER_ESTIMATE, FIRST_PARTY_STATEMENT | ORG, LOCATION, BRAND | ESTIMATE_ATTRIBUTED | Revenue band |
| `firmo.ownership` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Independent / PE-owned / franchisee / subsidiary |
| `firmo.funding` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Funding events |
| `person.contact` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND, PERSON | INTERNAL_ONLY | Contact: name, role, email, LinkedIn |
| `review.metrics` | THIRD_PARTY_REPORT | ORG, LOCATION, BRAND | ATTRIBUTED_ONLY | Review count / average rating |
| `review.response_ratio` | THIRD_PARTY_REPORT | ORG, LOCATION, BRAND | ATTRIBUTED_ONLY | Share of reviews the business responds to |
| `competitor.presence` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Which vendors peers/competitors run |
| `hiring.role` | FIRST_PARTY_STATEMENT | ORG, LOCATION, BRAND | ATTRIBUTED_ONLY | Open roles (title, dept, stack requirements) |
| `hiring.velocity` | DERIVED_MEASUREMENT | ORG, LOCATION, BRAND | INTERNAL_ONLY | Roles posted per quarter |
| `ads.activity` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Active advertising windows + landing pages |
| `news.events` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Press / announcements |
| `headcount.history` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Employee band over time |
| `change.page.delta` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | Pages appeared / removed since last capture |
| `tech.rollback` | DERIVED_MEASUREMENT | ORG, LOCATION, BRAND | INTERNAL_ONLY | Vendor present in earlier capture, absent now |
| `change.velocity` | DERIVED_MEASUREMENT | ORG, LOCATION, BRAND | INTERNAL_ONLY | Site change rate |
| `outreach.outcome` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | INTERNAL_ONLY | Sent / replied / meeting / bounced / unsubscribed |
| `crm.note` | FIRST_PARTY_STATEMENT | ORG, LOCATION, BRAND | ATTRIBUTED_ONLY | Conversation facts from calls/replies |
| `account.stage` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | INTERNAL_ONLY | Pipeline stage |
| `suppression.dnc` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | INTERNAL_ONLY | Do-not-contact / prior rejection / recent outreach |
| `tag.automation_maturity` | INFERENCE | ORG, LOCATION, BRAND | INTERNAL_ONLY | Ladder rung L0-L3 |
| `tag.marketing_maturity` | INFERENCE | ORG, LOCATION, BRAND | INTERNAL_ONLY | NONE / BASIC / ACTIVE / SOPHISTICATED |
| `tag.growth_posture` | INFERENCE | ORG, LOCATION, BRAND | INTERNAL_ONLY | GROWING / STABLE / CONTRACTING / UNKNOWN |
| `tag.platform_camp` | INFERENCE | ORG, LOCATION, BRAND | INTERNAL_ONLY | google_stack / microsoft_stack / mixed |
| `tag.regulated_vertical` | INFERENCE | ORG, LOCATION, BRAND | INTERNAL_ONLY | HIPAA / legal / finance regimes |
| `tag.size_class` | INFERENCE | ORG, LOCATION, BRAND | INTERNAL_ONLY | Banded size |
| `tag.location_model` | INFERENCE | ORG, LOCATION, BRAND | INTERNAL_ONLY | single / chain / franchise / national |
| `tag.industry` | INFERENCE | ORG, LOCATION, BRAND | INTERNAL_ONLY | Preset industry enum (cohort dimension) |
| `tag.business_type` | INFERENCE | ORG, LOCATION, BRAND | INTERNAL_ONLY | Preset business-type enum |
| `tag.ai_surface_readiness` | INFERENCE | ORG, LOCATION, BRAND | INTERNAL_ONLY | Data/API readiness for agentic systems |
| `tag.stack_complexity` | INFERENCE | ORG, LOCATION, BRAND | INTERNAL_ONLY | unified_suite / light_stack / assembled_stack |
| `tag.sales_maturity` | INFERENCE | ORG, LOCATION, BRAND | INTERNAL_ONLY | manual / assisted / automated |
| `tag.seasonality` | INFERENCE | ORG, LOCATION, BRAND | INTERNAL_ONLY | seasonal / steady |
| `tag.icp_fit` | INFERENCE | ORG, LOCATION, BRAND | INTERNAL_ONLY | ICP fit tier |
| `tag.data_quality` | INFERENCE | ORG, LOCATION, BRAND | INTERNAL_ONLY | Scan coverage depth / freshness band |
| `cohort.baseline` | DERIVED_MEASUREMENT | COHORT | CONTEXT_ONLY | Share of peers with predicate X |
| `cohort.percentile` | DERIVED_MEASUREMENT | ORG, LOCATION, BRAND | CONTEXT_ONLY | Account rank vs peers on a metric |
| `cohort.trend` | DERIVED_MEASUREMENT | COHORT | CONTEXT_ONLY | Adoption wave within cohort |
| `cohort.outlier` | DERIVED_MEASUREMENT | ORG, LOCATION, BRAND | CONTEXT_ONLY | Account deviates from cohort norm |
| `angle.performance` | DERIVED_MEASUREMENT | ANGLE | CONTEXT_ONLY | Derived fact type registered via DerivationFlow (see registry/derivations.json). |
| `integration.connection.verified` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | integration connection verified |
| `ops.automation.verified` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | INTERNAL_ONLY | ops automation verified |
| `ops.sales.verified` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | INTERNAL_ONLY | ops sales verified |
| `company.business_model` | FIRST_PARTY_STATEMENT | ORG, LOCATION, BRAND | ATTRIBUTED_ONLY | company business_model |
| `acquisition.coverage` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | INTERNAL_ONLY | acquisition coverage |
| `change.template.stable` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | change template stable |
| `location.data.consistency` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | DIRECT_SCOPED | location data consistency |
| `outreach.exposure` | DIRECT_OBSERVATION | ORG, LOCATION, BRAND | INTERNAL_ONLY | outreach exposure |
| `careers.page` | DIRECT_OBSERVATION | ORG, LOCATION | DIRECT_SCOPED | careers page |
| `careers.ats` | DIRECT_OBSERVATION | ORG, LOCATION | DIRECT_SCOPED | careers ats |
| `job.posting` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | job posting |
| `job.status` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | job status |
| `job.salary` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | job salary |
| `job.work_arrangement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | job work_arrangement |
| `job.location` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | job location |
| `job.skill_requirement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | job skill_requirement |
| `job.department` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | job department |
| `job.workflow_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | job workflow_statement |
| `job.document_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | job document_statement |
| `job.tool_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | job tool_statement |
| `job.handoff_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | job handoff_statement |
| `job.manual_process_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | job manual_process_statement |
| `job.spreadsheet_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | job spreadsheet_statement |
| `job.crm_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | job crm_statement |
| `job.follow_up_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | job follow_up_statement |
| `hiring.change_event` | DERIVED_MEASUREMENT | ORG, LOCATION | INTERNAL_ONLY | hiring change_event |
| `technology.footprint` | DIRECT_OBSERVATION | ORG, LOCATION | DIRECT_SCOPED | technology footprint |
| `technology.provider_report` | THIRD_PARTY_REPORT | ORG, LOCATION | ATTRIBUTED_ONLY | technology provider_report |
| `technology.script` | DIRECT_OBSERVATION | ORG, LOCATION | DIRECT_SCOPED | technology script |
| `technology.form_action` | DIRECT_OBSERVATION | ORG, LOCATION | DIRECT_SCOPED | technology form_action |
| `technology.cookie` | DIRECT_OBSERVATION | ORG, LOCATION | DIRECT_SCOPED | technology cookie |
| `technology.header` | DIRECT_OBSERVATION | ORG, LOCATION | DIRECT_SCOPED | technology header |
| `technology.csp` | DIRECT_OBSERVATION | ORG, LOCATION | DIRECT_SCOPED | technology csp |
| `technology.subdomain` | DIRECT_OBSERVATION | ORG, LOCATION | DIRECT_SCOPED | technology subdomain |
| `technology.network_request` | DIRECT_OBSERVATION | ORG, LOCATION | DIRECT_SCOPED | technology network_request |
| `technology.static_global` | DIRECT_OBSERVATION | ORG, LOCATION | DIRECT_SCOPED | technology static_global |
| `technology.account_identifier` | DIRECT_OBSERVATION | ORG, LOCATION | INTERNAL_ONLY | technology account_identifier |
| `technology.cooccurrence` | DERIVED_MEASUREMENT | ORG, LOCATION | INTERNAL_ONLY | technology cooccurrence |
| `technology.change` | DERIVED_MEASUREMENT | ORG, LOCATION | INTERNAL_ONLY | technology change |
| `product.capability` | FIRST_PARTY_STATEMENT, THIRD_PARTY_REPORT | SOFTWARE_PRODUCT | CONTEXT_ONLY | product capability |
| `product.vertical` | FIRST_PARTY_STATEMENT, THIRD_PARTY_REPORT | SOFTWARE_PRODUCT | CONTEXT_ONLY | product vertical |
| `product.category` | FIRST_PARTY_STATEMENT, THIRD_PARTY_REPORT | SOFTWARE_PRODUCT | CONTEXT_ONLY | product category |
| `product.integration_support` | FIRST_PARTY_STATEMENT, THIRD_PARTY_REPORT | SOFTWARE_PRODUCT | CONTEXT_ONLY | product integration_support |
| `portal.observed` | DIRECT_OBSERVATION | ORG, LOCATION | DIRECT_SCOPED | portal observed |
| `integration.public_marker` | DIRECT_OBSERVATION | ORG, LOCATION | DIRECT_SCOPED | integration public_marker |
| `review.record` | THIRD_PARTY_REPORT | ORG, LOCATION, SOFTWARE_PRODUCT, APPLICATION, LISTING | ATTRIBUTED_ONLY | review record |
| `review.statement` | THIRD_PARTY_REPORT | ORG, LOCATION, SOFTWARE_PRODUCT, APPLICATION | ATTRIBUTED_ONLY | review statement |
| `review.owner_response` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | review owner_response |
| `review.theme_classification` | INFERENCE | ORG, LOCATION, SOFTWARE_PRODUCT, APPLICATION | INTERNAL_ONLY | review theme_classification |
| `discussion.record` | THIRD_PARTY_REPORT | SOFTWARE_PRODUCT, INDUSTRY | CONTEXT_ONLY | discussion record |
| `discussion.statement` | THIRD_PARTY_REPORT | SOFTWARE_PRODUCT, INDUSTRY | CONTEXT_ONLY | discussion statement |
| `discussion.theme_classification` | INFERENCE | SOFTWARE_PRODUCT, INDUSTRY | CONTEXT_ONLY | discussion theme_classification |
| `product.pain_prior` | DERIVED_MEASUREMENT | SOFTWARE_PRODUCT | CONTEXT_ONLY | product pain_prior |
| `industry.pain_prior` | DERIVED_MEASUREMENT | INDUSTRY | CONTEXT_ONLY | industry pain_prior |
| `review.theme_summary` | DERIVED_MEASUREMENT | ORG, LOCATION | INTERNAL_ONLY | review theme_summary |
| `account.industry_membership` | FIRST_PARTY_STATEMENT, REGISTRY_RECORD | ORG, LOCATION | ATTRIBUTED_ONLY | account industry_membership |
| `search.result` | THIRD_PARTY_REPORT | ORG, LOCATION, WEBSITE, APPLICATION, LISTING | ATTRIBUTED_ONLY | search result |
| `business.profile_attribute` | THIRD_PARTY_REPORT | ORG, LOCATION, WEBSITE, APPLICATION, LISTING | ATTRIBUTED_ONLY | business profile_attribute |
| `backlink.record` | THIRD_PARTY_REPORT | ORG, LOCATION, WEBSITE, APPLICATION, LISTING | ATTRIBUTED_ONLY | backlink record |
| `web.mention` | THIRD_PARTY_REPORT | ORG, LOCATION, WEBSITE, APPLICATION, LISTING | ATTRIBUTED_ONLY | web mention |
| `web.mention_sentiment` | INFERENCE | ORG, LOCATION, WEBSITE, APPLICATION, LISTING | INTERNAL_ONLY | web mention_sentiment |
| `app.listing` | THIRD_PARTY_REPORT | ORG, LOCATION, WEBSITE, APPLICATION, LISTING | ATTRIBUTED_ONLY | app listing |
| `shopping.listing` | THIRD_PARTY_REPORT | ORG, LOCATION, WEBSITE, APPLICATION, LISTING | ATTRIBUTED_ONLY | shopping listing |
| `advertisement.record` | THIRD_PARTY_REPORT | ORG, LOCATION, WEBSITE, APPLICATION, LISTING | ATTRIBUTED_ONLY | advertisement record |
| `registry.registration` | REGISTRY_RECORD | ORG, LOCATION, PERSON | REGISTRY_ATTRIBUTED | registry registration |
| `registry.license` | REGISTRY_RECORD | ORG, LOCATION, PERSON | REGISTRY_ATTRIBUTED | registry license |
| `registry.permit` | REGISTRY_RECORD | ORG, LOCATION, PERSON | REGISTRY_ATTRIBUTED | registry permit |
| `registry.specialty` | REGISTRY_RECORD | ORG, LOCATION, PERSON | REGISTRY_ATTRIBUTED | registry specialty |
| `registry.filing` | REGISTRY_RECORD | ORG, LOCATION, PERSON | REGISTRY_ATTRIBUTED | registry filing |
| `registry.affiliation` | REGISTRY_RECORD | ORG, LOCATION, PERSON | REGISTRY_ATTRIBUTED | registry affiliation |
| `phone.cta` | DIRECT_OBSERVATION | ORG, LOCATION | DIRECT_SCOPED | phone cta |
| `phone.routing_observed` | DIRECT_OBSERVATION | ORG, LOCATION | DIRECT_SCOPED | phone routing_observed |
| `phone.routing_verified` | FIRST_PARTY_STATEMENT, DIRECT_OBSERVATION | ORG, LOCATION | ATTRIBUTED_ONLY | phone routing_verified |
| `phone.recording_verified` | FIRST_PARTY_STATEMENT, DIRECT_OBSERVATION | ORG, LOCATION | INTERNAL_ONLY | phone recording_verified |
| `phone.call_event` | DIRECT_OBSERVATION | ORG, LOCATION | INTERNAL_ONLY | phone call_event |
| `phone.economics_hypothesis` | INFERENCE | ORG, LOCATION | INTERNAL_ONLY | phone economics_hypothesis |
| `website.business_model_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | website business_model_statement |
| `website.customer_type_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | website customer_type_statement |
| `website.lead_channel_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | website lead_channel_statement |
| `website.sales_motion_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | website sales_motion_statement |
| `website.document_type_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | website document_type_statement |
| `website.handoff_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | website handoff_statement |
| `website.intent_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | website intent_statement |
| `website.service_offering_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | website service_offering_statement |
| `website.geographic_market_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | website geographic_market_statement |
| `website.workflow_step_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | website workflow_step_statement |
| `website.role_responsibility_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | website role_responsibility_statement |
| `website.knowledge_source_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | website knowledge_source_statement |
| `website.intake_method_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | website intake_method_statement |
| `website.manual_process_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | website manual_process_statement |
| `website.approval_process_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | website approval_process_statement |
| `website.data_reentry_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | website data_reentry_statement |
| `website.reporting_process_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | website reporting_process_statement |
| `website.follow_up_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | website follow_up_statement |
| `website.billing_process_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | website billing_process_statement |
| `website.scheduling_process_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | website scheduling_process_statement |
| `website.compliance_process_statement` | FIRST_PARTY_STATEMENT | ORG, LOCATION | ATTRIBUTED_ONLY | website compliance_process_statement |
| `workflow.hypothesis` | INFERENCE | ORG, LOCATION | INTERNAL_ONLY | workflow hypothesis |
| `business_model.hypothesis` | INFERENCE | ORG, LOCATION | INTERNAL_ONLY | business_model hypothesis |
| `customer_type.hypothesis` | INFERENCE | ORG, LOCATION | INTERNAL_ONLY | customer_type hypothesis |
| `lead_channel.hypothesis` | INFERENCE | ORG, LOCATION | INTERNAL_ONLY | lead_channel hypothesis |
| `knowledge_complexity.hypothesis` | INFERENCE | ORG, LOCATION | INTERNAL_ONLY | knowledge_complexity hypothesis |
| `document_complexity.hypothesis` | INFERENCE | ORG, LOCATION | INTERNAL_ONLY | document_complexity hypothesis |
| `handoff_risk.hypothesis` | INFERENCE | ORG, LOCATION | INTERNAL_ONLY | handoff_risk hypothesis |
| `automation_opportunity.hypothesis` | INFERENCE | ORG, LOCATION | INTERNAL_ONLY | automation_opportunity hypothesis |
| `document.surface` | DIRECT_OBSERVATION | ORG, LOCATION | DIRECT_SCOPED | document surface |
| `form.surface` | DIRECT_OBSERVATION | ORG, LOCATION | DIRECT_SCOPED | form surface |
| `ads.measurement` | DERIVED_MEASUREMENT, DIRECT_OBSERVATION, THIRD_PARTY_REPORT | APPLICATION, LISTING, LOCATION, ORG, SOFTWARE_PRODUCT, WEBSITE | ATTRIBUTED_ONLY | ads measurement |
| `app.measurement` | DERIVED_MEASUREMENT, DIRECT_OBSERVATION, THIRD_PARTY_REPORT | APPLICATION, LISTING, LOCATION, ORG, SOFTWARE_PRODUCT, WEBSITE | ATTRIBUTED_ONLY | app measurement |
| `hiring.measurement` | DERIVED_MEASUREMENT | LOCATION, ORG, WEBSITE | ATTRIBUTED_ONLY | hiring measurement |
| `phone.measurement` | DERIVED_MEASUREMENT, DIRECT_OBSERVATION, THIRD_PARTY_REPORT | APPLICATION, LISTING, LOCATION, ORG, SOFTWARE_PRODUCT, WEBSITE | INTERNAL_ONLY | phone measurement |
| `registry.measurement` | DERIVED_MEASUREMENT, REGISTRY_RECORD | APPLICATION, LISTING, LOCATION, ORG, SOFTWARE_PRODUCT, WEBSITE | ATTRIBUTED_ONLY | registry measurement |
| `research.measurement` | DERIVED_MEASUREMENT | INDUSTRY, SOFTWARE_PRODUCT | INTERNAL_ONLY | research measurement |
| `review.measurement` | DERIVED_MEASUREMENT, THIRD_PARTY_REPORT | APPLICATION, LOCATION, ORG, SOFTWARE_PRODUCT | ATTRIBUTED_ONLY | review measurement |
| `seo.measurement` | DERIVED_MEASUREMENT, DIRECT_OBSERVATION, PROVIDER_ESTIMATE, THIRD_PARTY_REPORT | LOCATION, ORG, WEBSITE | ATTRIBUTED_ONLY | seo measurement |
| `shopping.measurement` | DERIVED_MEASUREMENT, DIRECT_OBSERVATION, THIRD_PARTY_REPORT | APPLICATION, LISTING, LOCATION, ORG, SOFTWARE_PRODUCT, WEBSITE | ATTRIBUTED_ONLY | shopping measurement |
| `technology.measurement` | DERIVED_MEASUREMENT, DIRECT_OBSERVATION, THIRD_PARTY_REPORT | APPLICATION, LISTING, LOCATION, ORG, SOFTWARE_PRODUCT, WEBSITE | ATTRIBUTED_ONLY | technology measurement |
| `traffic.measurement` | PROVIDER_ESTIMATE | LOCATION, ORG, WEBSITE | ESTIMATE_ATTRIBUTED | traffic measurement |
| `publication.record` | FIRST_PARTY_STATEMENT, THIRD_PARTY_REPORT | ORG, LOCATION | ATTRIBUTED_ONLY | Captured press, social, news or case-study publication; publisher claim, not verified execution of a project. |
| `publication.statement` | FIRST_PARTY_STATEMENT, THIRD_PARTY_REPORT | ORG, LOCATION | ATTRIBUTED_ONLY | Attributable exact statement, including transcript speaker and optional timecode. Not a verified account operating condition. |
| `organization.event_report` | FIRST_PARTY_STATEMENT, THIRD_PARTY_REPORT | ORG, LOCATION | ATTRIBUTED_ONLY | Reported corporate event with occurrence and announcement times kept separate. |
| `repository.activity_observed` | DIRECT_OBSERVATION | ORG, LOCATION | ATTRIBUTED_ONLY | Public repository change. A dependency is not evidence of production deployment or organization-wide adoption. |
| `event.public_participation` | THIRD_PARTY_REPORT | ORG, LOCATION | ATTRIBUTED_ONLY | Published organizational participation; not attendance, budget or intent. |
| `event.authorized_attendance` | THIRD_PARTY_REPORT, DIRECT_OBSERVATION | ORG, PERSON | INTERNAL_ONLY | Permissioned registration/attendance record. Registration and interested are not attendance. Requires authorized scope. |
| `trade.shipment_record` | REGISTRY_RECORD, THIRD_PARTY_REPORT | ORG, LOCATION | REGISTRY_ATTRIBUTED | Namespaced reported shipment; not purchase intent or a growth conclusion. |
| `procurement.record` | REGISTRY_RECORD, THIRD_PARTY_REPORT | ORG, LOCATION | REGISTRY_ATTRIBUTED | Procurement stage is explicit. A notice is not a won contract. |
| `legal.filing_record` | REGISTRY_RECORD | ORG, LOCATION | INTERNAL_ONLY | Exact legal filing/procedural record. Allegations and settlement do not establish wrongdoing or failed AI implementation. |
| `award.listing` | THIRD_PARTY_REPORT | ORG, LOCATION | ATTRIBUTED_ONLY | Listing in a named edition; not a current measured growth rate or proof of technical lag. |
| `patent.application_record` | REGISTRY_RECORD | ORG, LOCATION | REGISTRY_ATTRIBUTED | Patent status and date, not deployed capability or available budget. |
| `franchise.disclosure_record` | REGISTRY_RECORD, THIRD_PARTY_REPORT, FIRST_PARTY_STATEMENT | ORG, LOCATION | REGISTRY_ATTRIBUTED | System/edition-bound disclosure, not a franchisee-specific revenue assertion. |
| `registry.financing_filing` | REGISTRY_RECORD | ORG, LOCATION | REGISTRY_ATTRIBUTED | Financing-statement filing. No assumption about cash received, solvency, growth or spending willingness. |
| `registry.loan_record` | REGISTRY_RECORD | ORG, LOCATION | REGISTRY_ATTRIBUTED | Historical program/loan record. Not current company size, budget or propensity to buy. |
| `case_study.report` | THIRD_PARTY_REPORT | ORG, LOCATION | ATTRIBUTED_ONLY | Vendor/customer-reported case about the comparison organization, never a claim that KeenSight delivered it. |
| `case_study.outcome_report` | THIRD_PARTY_REPORT | ORG, LOCATION | ATTRIBUTED_ONLY | Reported outcome with denominator/method gaps preserved. Exact percentage is specificity, not credibility or causal proof. |
