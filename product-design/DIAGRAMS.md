# Full product dataflow and UML

Editable Mermaid sources. These diagrams are proposed associations and workflows, not rendered screenshots or runtime tests. The lifecycle flow can contain operational feedback; concrete same-run computations still require an acyclic dependency plan.

## Full product lifecycle

```mermaid
flowchart TD
  A[Program, audience and offer policy] --> B[Account discovery and selection]
  B --> C[Bounded acquisition and Scrapling]
  C --> D[Fingerprints, evidence and attributable facts]
  D --> E[Resolved claims and pinned evaluation inputs]
  E --> K[Searchable knowledge result]
  E --> F[Research context, comparisons and signals]
  F --> G[Opportunity selection]
  G --> H[Contacts, role and endpoint assessment]
  H --> I[Grounded content and exact-revision review]
  I --> J[Approved campaign and enrollment]
  J --> L[Fresh use gate and reconciled dispatch]
  L --> M[Verified inbound events]
  M --> N[Immediate stop or hold controls]
  N --> J
  M --> O[Conversations and human response tasks]
  O --> P[CRM handoff and sales lifecycle]
  P --> Q[Attributable outcomes and quality]
  Q -. reviewed future version .-> A
  D --> R[Fingerprint candidate research]
  R --> S[Fixtures, calibration and authorized release]
  S -. next scan or replay .-> C
  T[Product and industry corpus] --> F
```

## Campaign, dispatch, reply and CRM sequence

```mermaid
sequenceDiagram
    participant CP as Campaign policy
    participant EN as Enrollment owner
    participant UG as Current-use gate
    participant DS as Dispatcher
    participant PR as Provider
    participant IN as Verified event ingress
    participant GV as Governance restrictions
    participant CV as Conversation handler
    participant CR as CRM adapter
    CP->>EN: Approved route and exactly one schedule owner
    EN->>UG: Due step, assessed recipient, reviewed message
    UG-->>EN: ALLOW or BLOCK with current state versions
    EN->>DS: Stable delivery intent and eligible gate
    DS->>DS: Recheck local state and preserve prepared intent
    DS->>PR: Dispatch exact authorized message
    alt acceptance confirmed
        PR-->>DS: Provider message identity
    else response ambiguous
        PR-->>DS: Timeout or ambiguous result
        DS->>PR: Reconcile existing effect, not blind resend
    end
    PR-->>IN: Reply or opt-out event
    IN->>IN: Verify source and deduplicate
    IN->>CV: Routed event, before optional classification
    CV->>GV: Restriction request when opt-out is established
    CV->>EN: Pause or stop future steps
    CV->>CV: Optional classification and human follow-up task
    CV->>CR: Evidence-linked sales handoff
    alt CRM unavailable
        CR->>CR: Retry sync intent only
    end
```

## High-level product class associations

```mermaid
classDiagram
  class ProgramDefinition
  class AudienceDefinition
  class OfferDefinition
  class AccountSeed
  class Subject
  class SubjectBinding
  class Fact
  class ClaimResolution
  class InputSnapshot
  class ContextAssessment
  class SignalEvaluation
  class OpportunitySelection
  class ContactProfile
  class ContactAssessment
  class OutreachPackage
  class MessageArtifact
  class ReviewDecision
  class CampaignDefinition
  class CampaignApproval
  class Enrollment
  class DeliveryIntent
  class SendGateDecision
  class DeliveryAttempt
  class Exposure
  class OutcomeEvent
  class Conversation
  class ReplyAssessment
  class SalesHandoff
  class CRMSyncReceipt
  class QualityAssessment
  class PromotionProposal
  ProgramDefinition --> AudienceDefinition : selects
  ProgramDefinition --> OfferDefinition : offers
  AudienceDefinition --> AccountSeed : discovery policy
  AccountSeed --> Subject : accepted resolution
  SubjectBinding --> Subject : binds with evidence
  Fact --> Subject : concerns
  ClaimResolution --> Fact : complete evidence group
  InputSnapshot --> ClaimResolution : pins
  ContextAssessment --> InputSnapshot : explicit allowed join
  SignalEvaluation --> InputSnapshot : evaluates
  SignalEvaluation --> ContextAssessment : internal context
  OpportunitySelection --> SignalEvaluation : considers
  OpportunitySelection --> OfferDefinition : compatible offer
  ContactProfile --> SubjectBinding : person account link
  ContactAssessment --> ContactProfile : separately assesses
  OutreachPackage --> OpportunitySelection : supported path
  OutreachPackage --> MessageArtifact : exact visible revision
  ReviewDecision --> OutreachPackage : binds revision hash
  CampaignDefinition --> ProgramDefinition : program
  CampaignApproval --> CampaignDefinition : approves exact policy
  Enrollment --> CampaignDefinition : one schedule owner
  Enrollment --> ContactAssessment : audience eligibility
  DeliveryIntent --> Enrollment : one step
  DeliveryIntent --> MessageArtifact : approved payload
  SendGateDecision --> DeliveryIntent : current permission
  SendGateDecision --> ReviewDecision : exact review
  SendGateDecision --> CampaignApproval : campaign authority
  DeliveryAttempt --> DeliveryIntent : stable effect identity
  Exposure --> DeliveryAttempt : accepted or reconciled effect
  OutcomeEvent --> Exposure : nullable until attributed
  Conversation --> OutcomeEvent : verified inbound
  ReplyAssessment --> Conversation : assessment not observed truth
  SalesHandoff --> Conversation : qualified handoff
  CRMSyncReceipt --> SalesHandoff : external sync result
  QualityAssessment --> OutcomeEvent : eligible measurement
  PromotionProposal --> QualityAssessment : later authorized release
```

