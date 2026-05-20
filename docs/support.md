# Surrogate‑1 Support & Documentation

Welcome to the **Surrogate‑1** orchestration framework! This guide provides all the information you need to get started quickly, troubleshoot common issues, and reach out for help.

---

## 📚 Documentation

- **Getting Started** – [docs/getting_started.md](../docs/getting_started.md)  
  Step‑by‑step instructions to set up your first runner, configure shards, and push results.

- **Architecture Overview** – [docs/architecture.md](../docs/architecture.md)  
  High‑level diagram and component responsibilities.

- **Configuration Reference** – [docs/configuration.md](../docs/configuration.md)  
  All environment variables, CLI flags, and YAML options.

- **FAQ & Troubleshooting** – [docs/faq.md](../docs/faq.md)  
  Answers to the most common questions and error‑handling tips.

- **API Reference** – [docs/api.md](../docs/api.md)  
  Detailed description of the public Python modules and helper scripts.

---

## 🛠️ Support Channels

| Channel | Description | How to Access |
|---------|-------------|---------------|
| **GitHub Issues** | Report bugs, request features, or ask technical questions. | Open an issue in the repository: <https://github.com/axentx/surrogate-1/issues> |
| **Slack Community** | Real‑time chat with the core team and community contributors. | Join the `#surrogate-1` channel on the AxentX Slack workspace. Invite link: <https://axentx.slack.com/invite> |
| **Email Support** | Direct assistance for critical blockers or security concerns. | Send an email to **support@axentx.com** with the subject line `Surrogate‑1 Support`. |
| **Office Hours (Live Q&A)** | Weekly live sessions for deep‑dive walkthroughs and Q&A. | Calendar link: <https://calendar.axentx.com/surrogate-1-office-hours> |
| **Documentation Search** | Quick lookup of topics across all docs. | Use the built‑in search bar at <https://docs.axentx.com/surrogate-1> |

---

## 🚀 Quick Start Checklist

1. **Read the Getting Started guide** – ensures you have the required environment (Python 3.11+, Docker, GitHub token).  
2. **Run the test suite** – `make test` to verify your local setup.  
3. **Configure your runner** – copy `.env.example` to `.env` and adjust `SHARD_ID`, `TOTAL_SHARDS`, and `GH_TOKEN`.  
4. **Launch a runner** – `./bin/run.sh`.  
5. **Monitor logs** – view real‑time output via `docker logs -f surrogate-1-runner`.  
6. **If anything fails**, consult the FAQ or open a GitHub issue.

---

## 📞 When to Reach Out

- **Critical failures** that block dataset ingestion (e.g., authentication errors, persistent crashes).  
- **Security vulnerabilities** discovered in the runner or supporting scripts.  
- **Feature requests** that require changes to the orchestration logic.  
- **Performance bottlenecks** that need architectural guidance.

---

## 🙏 Contributing to Support

We encourage community contributions to improve documentation and support resources:

1. Fork the repository.  
2. Add or update markdown files under `docs/`.  
3. Submit a pull request with a clear description of the changes.  

All contributions are reviewed within 48 hours.

---

*Happy orchestrating! 🎉*  
— The AxentX Surrogate‑1 Team