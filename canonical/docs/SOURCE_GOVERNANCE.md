# Source governance and semantic cautions

Primary references checked September 14, 2026. These notes specify engineering gates; they are not source licenses or a legal opinion. Applicability depends on the actual endpoint, account agreement, geography, intended use and data categories. Real source blueprints remain unimplemented and unapproved.

| Source family | Relevant primary documentation | Required contract consequence |
|---|---|---|
| Google Places | https://developers.google.com/maps/documentation/places/web-service/policies | The policy restricts storage/caching beyond allowed exceptions and requires attribution. Do not assign a generic indefinite retention permission or assume that all analysis/model uses are authorized. |
| Reddit | https://redditinc.com/policies/data-api-terms | Commercial or otherwise unpermitted use needs a separate agreement; retention is tied to the approved use. Unapproved research processing is disabled. |
| Similarweb visits | https://developers.similarweb.com/reference/visits | Visits are documented as estimates. Preserve provider-estimate nature, period, dimensions and method rather than relabeling them as direct analytics. |
| DataForSEO technologies | https://docs.dataforseo.com/v3/domain_analytics-technologies-overview/ | Domain technologies are a provider data family. Preserve provider-report provenance; they are not the local scanner's own observations. |
| DataForSEO business data | https://docs.dataforseo.com/v3/business_data-overview/ | Map endpoint-specific business/review payloads into typed families. An API provider name does not collapse all content into one fact or authorize every downstream use. |
| CMS/NPPES | https://download.cms.gov/nppes/NPI_Files.html | NPI issuance is not validation of licensure or credentialing. Keep registration and license facts distinct. |
| SEC/IAPD | https://www.investor.gov/introduction-investing/investing-basics/glossary/investment-adviser-public-disclosure-iapd | Preserve the firm/individual distinction, issuer and filing/registration context. Do not conflate professional registration, assets and employee counts. |

G2, Capterra, Similarweb, third-party review/traffic feeds, bar/licensing boards, permit registries and every jurisdiction-specific dataset still require an actual access and use review. A source's existence or a public page is not a blanket permission to scrape, retain, redistribute or submit content to a model.

## Policy contract

DataAccessPolicy carries an explicit tenant allowlist, approval evidence, version, validity period, permitted purposes, raw/derived retention limits, attribution, personal/sensitive-data flags and deletion behavior. SourceDefinition references that policy and separately declares source version, acquisition method, supported natures, freshness and emitted predicates.

The fixture policy is deliberately synthetic. The validator refuses production mode. ProviderBlueprint is planning metadata only; it cannot produce a fact until an implemented SourceDefinition and applicable policy are supplied.

## Privacy defaults

Research concerns businesses, products and aggregate industry themes. Do not infer sensitive personal characteristics or de-anonymize forum users. Public professional person records require an approved purpose and appropriate source-level permissions. Review content can contain health, legal or financial details; personal/sensitive content is denied by the default policy and must be excluded or redacted under an approved processing path before admission.

Authorized phone metadata does not authorize audio recording or transcription. Consent/recording requirements and restricted-data storage are separate enablement gates. The example contains synthetic, non-sensitive call metadata only.

## Retention and loss of support

When retention expires, the artifact can become REFERENCE_ONLY/DELETED, retaining only permitted metadata. Derived facts and packages must lose current-use eligibility when required evidence is no longer inspectable or permitted. Preserve historical explanations only to the extent allowed. A content hash is not a substitute for evidence or for permission to retain the underlying content.

Production deletion, revocation propagation and attribution presentation are specified requirements, not implemented services in this archive.
