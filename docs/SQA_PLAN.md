# Software Quality Assurance plan

| Quality attribute | Measure / target | Verification |
|---|---|---|
| Correctness | All critical business-rule tests pass. | pytest and manual test cases |
| Reliability | Stock never becomes negative via sales. | conditional atomic database update and PostgreSQL concurrency test |
| Maintainability | Business logic separated into services and models. | code review |
| Usability | Main tasks accessible from consistent navigation. | staff walkthrough |
| Efficiency | Dashboard and list pages respond promptly on sample data. | measure response time under documented test conditions |
| Security | No production secrets committed; validate numeric input. | configuration review and dependency/security scan |

## Responsible AI checklist
- Forecast is labelled as an estimate.
- Human owner approves every purchasing decision.
- Explain the forecasting method and its limitations.
- Do not put customer personal data or credentials in prompts.
- Keep an AI usage log and verify generated code/tests manually.
