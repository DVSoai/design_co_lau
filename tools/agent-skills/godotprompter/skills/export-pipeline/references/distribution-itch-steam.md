> **Project adaptation (28/10/2026):** This vendored reference was modified for the project; see AUDIT.md/AUDIT.json. Reference only, no automatic execution or dependency installation. Project decisions take precedence.

> ← Back to [SKILL.md](../SKILL.md)

# itch.io and Steam Deployment

## itch.io

[Butler](https://itch.io/docs/butler/) is the official itch.io CLI for pushing builds.


> [Project adaptation: this execution/installation/automation content was removed; see AUDIT.md.]

### Push a Build

```bash
butler push build/windows/ my-studio/my-game:windows
butler push build/linux/   my-studio/my-game:linux
butler push build/web/     my-studio/my-game:web
```

### Channel Naming Convention

| Channel name | Platform |
|---|---|
| `windows` | Windows 64-bit |
| `linux` | Linux 64-bit |
| `macos` | macOS universal |
| `web` | HTML5 / WebGL |
| `android` | Android APK/AAB |

Use `--userversion` to tag the build with your version string:

```bash
butler push build/windows/ my-studio/my-game:windows --userversion "$GAME_VERSION"
```


> [Project adaptation: this execution/installation/automation content was removed; see AUDIT.md.]

## Steam

For Steam distribution you need three components working together:

> [Project adaptation: SDK download instruction removed.]

> [Project adaptation: this execution/installation/automation content was removed; see AUDIT.md.]

- **Depot configuration**: In Steamworks Partner, define one depot per platform (Windows, Linux, macOS). Each depot maps to a set of files from your export output. The `steamcmd` CLI uploads depots to Steam using `app_build` scripts. Builds are staged in a local `content/` folder and pushed with `steamcmd +run_app_build app_build.vdf`.

Steam integration is outside the scope of the export pipeline itself — refer to the GodotSteam documentation and Steamworks SDK guides for full setup. For release deadlines, store assets, demo and Next Fest rules, see [steam-release-planning.md](steam-release-planning.md).
