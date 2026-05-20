
Open the URL in a browser to confirm the files are present.

## 8. Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Docker fails to start | Docker not running | Start Docker Desktop or `sudo systemctl start docker` |
| `python: command not found` | Wrong Docker image | Ensure you use `axentx/surrogate-1:latest` |
| Missing environment variable `SHARD_ID` | Not exported | Export `SHARD_ID` before running or pass via `-e` flag |

## 9. Next Steps

- Watch the **Usage Walkthrough Video** in `docs/usage_walkthrough_video.md` to see the full pipeline in action.
- Explore the `docs/faq.md` for common questions.

Happy ingesting! 🚀