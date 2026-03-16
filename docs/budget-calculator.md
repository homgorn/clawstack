# Budget Calculator

ClawStack should speak in budget bands, not vague "cheap" claims.

## Budget scenarios

| Scenario | Monthly cost | Typical shape |
| --- | --- | --- |
| Free-first | `$0-3` | Free models, low volume, basic experimentation |
| Budget | `$13-20` | Cheap main model, some free fallbacks, self-hosted VPS |
| Recommended | `$28-35` | Budget setup plus stronger research and tool usage |
| Power | `$45-50` | Heavier usage with premium fallback kept under control |

## Main cost levers

- main-agent model choice;
- research model frequency;
- tool-calling frequency;
- whether heartbeat stays cheap;
- whether you add VPS or managed infra.

## Practical rule

Keep expensive models as exception paths, not as the default identity of the system.

That single design choice matters more than almost any micro-optimization.
