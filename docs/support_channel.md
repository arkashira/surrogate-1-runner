# Migration Support Channel

## Support Channels

### Primary Support: Slack
- **Channel Name**: `#surrogate-1-migration-support`
- **Workspace**: `axentx-dev`
- **Access**: Invite link provided to migration team members
- **Response Time**: Within 24 hours during business hours (UTC)

### Secondary Support: Discord
- **Server**: `axentx-support`
- **Channel**: `#surrogate-1-migration`
- **Access**: Join via https://discord.gg/axentx

## How to Join

1. **Request an invitation** by filling out the short form at:  
   https://axentx.com/migration-support-invite
2. You will receive an email with a Slack invitation within a few minutes.
3. Once you join, look for the **#migration-help** channel.

## Support Documentation

All relevant documentation is collected in one place for easy reference:

- **Migration Guide**: https://axentx.com/docs/migration-guide  
- **FAQ**: https://axentx.com/docs/migration-faq  
- **Troubleshooting Checklist**: https://axentx.com/docs/migration-troubleshooting  
- **Internal Resources**:
  - [Dataset Schema Reference](./docs/dataset-schema.md)
  - [Runner Configuration Guide](./docs/runner-config.md)
  - [Error Code Reference](./docs/error-codes.md)

## Escalation Procedure

1. **Level 1**: Submit ticket via Slack/Discord channel
2. **Level 2**: If unresolved in 4 hours, tag `@migration-lead`
3. **Level 3**: Critical blockers require `@platform-engineering` escalation

## Reporting Issues

When reporting an issue, include:
1. Runner ID and shard ID
2. Timestamp of failure
3. Relevant log excerpts
4. Error messages (full stack trace if available)
5. Steps to reproduce

## Response Time SLA

| Priority | Response Time | Resolution Time |
|----------|---------------|-----------------|
| Critical (data loss risk) | 1 hour | 4 hours |
| High (workflow blocked) | 4 hours | 24 hours |
| Medium (minor issues) | 24 hours | 48 hours |
| Low (informational) | 48 hours | 72 hours |

## Support Hours

- **Standard Support**: UTC 08:00 - 20:00 (Mon-Fri)
- **Emergency Support**: 24/7 for critical incidents
- **Weekend Support**: Limited (Level 2 only)

## Contact Information

| Role | Contact | Availability |
|------|---------|--------------|
| Migration Lead | `@migration-lead` | 24/7 Slack |
| Platform Engineer | `@platform-oncall` | 24/7 PagerDuty |
| Documentation | `docs-support@axentx.io` | Business hours |

If you encounter any problems joining the Slack workspace or have urgent issues outside of the support hours, please email **support@axentx.com** and we will get back to you as soon as possible.