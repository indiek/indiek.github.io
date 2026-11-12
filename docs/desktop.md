---
title: "IndieK Desktop"
description: "Install the IndieK Desktop App on macOS, Windows or Linux, open the first build despite the missing code signature, set up your author key and keep it safe."
---

# IndieK Desktop

The IndieK Desktop App is the easiest way to use IndieK: one installer that
contains the [web UI](/docs/web-ui/), the [local API](/docs/api/) and the
`ik` command line. You don't need Python, Node.js or a terminal. It runs
entirely on your computer and works offline
([how it works](/docs/architecture/)).

> **Status: the first release is coming soon.** Until it is published on
> the [releases page](https://github.com/indiek/indiek-desktop/releases),
> you can run the app from source: see the
> [desktop repository's README](https://github.com/indiek/indiek-desktop#run-from-source-development-mode).

## Download

Download the installer for your system from the
[releases page](https://github.com/indiek/indiek-desktop/releases). In the
file names, `<version>` stands for the version number, for example `0.2.0`.

| System | File | Notes |
| --- | --- | --- |
| macOS, Apple silicon (M1 and later) | `IndieK_<version>_aarch64.dmg` | Intel Macs: not yet; use the [Python package](/docs/intro/) meanwhile |
| Windows 10 and 11 (64-bit) | `IndieK_<version>_x64-setup.exe` or `IndieK_<version>_x64_en-US.msi` | Both install the same app; the `.exe` is the usual choice |
| Linux, 64-bit (Ubuntu 22.04 or newer, Debian 12 or newer) | `IndieK_<version>_amd64.AppImage` or `IndieK_<version>_amd64.deb` | The `.deb` for Debian and Ubuntu; the `.AppImage` runs on most other distributions |

Each release also lists `SHA256SUMS.txt`. To check that your download is
intact, compare its SHA-256 with the line for your file:

```bash
shasum -a 256 IndieK_*.dmg                  # macOS
sha256sum IndieK_*.AppImage                 # Linux
Get-FileHash IndieK_*-setup.exe             # Windows (PowerShell)
```

## Install

### Why your system warns you

The first releases are **not code-signed**. Code signing is a paid
certificate from Apple and Microsoft that lets your system recognise the
publisher, and it will come before IndieK's wider launch. Until then,
macOS and Windows warn you before the first launch and ask you to confirm
that you trust the app. The steps below do exactly that, once. To make sure
the file is the published one, compare its checksum ([Download](#download)).

### macOS

1. Open the `.dmg` and drag **IndieK** onto **Applications**.
2. Open IndieK from Applications. macOS refuses the first time with a message
   like *"IndieK" Not Opened: Apple could not verify "IndieK" is free of
   malware…*. Click **Done**.
3. Open **System Settings → Privacy & Security** and scroll down to
   **Security**. Next to *"IndieK" was blocked to protect your Mac*, click
   **Open Anyway**, then confirm with your password or Touch ID.
4. Open IndieK again and click **Open Anyway** in the last dialog. macOS
   remembers your choice: later launches open directly.

<!-- TODO(owner): screenshots of steps 2, 3 and 4 on macOS 15. -->

On macOS 14 and older, step 2 offers **Open** after a right-click (or
Control-click) on the app → **Open**.

If macOS says *"IndieK" is damaged and can't be opened*, the app is not
damaged: macOS says this about some unsigned apps downloaded from the
internet. Move IndieK to Applications, then run, once, in Terminal:

```bash
xattr -dr com.apple.quarantine /Applications/IndieK.app
```

The first launch after an install or update takes up to about 15 seconds
while macOS checks the new files; later launches take about a second.

### Windows

1. Run `IndieK_<version>_x64-setup.exe` (or the `.msi`).
2. If Windows shows *Windows protected your PC* (Microsoft Defender
   SmartScreen), click **More info**, then **Run anyway**.
3. Follow the installer. IndieK appears in the Start menu.

<!-- TODO(owner): screenshot of the SmartScreen dialog after "More info". -->

The installer downloads Microsoft's WebView2 runtime if your system lacks it
(Windows 10 and 11 normally include it).

### Linux

**Debian, Ubuntu** (`.deb`):

```bash
sudo apt install ./IndieK_<version>_amd64.deb
```

IndieK then appears among your applications.

**AppImage** (no installation): make the file executable and run it.

```bash
chmod +x IndieK_<version>_amd64.AppImage
./IndieK_<version>_amd64.AppImage
```

Some distributions need FUSE 2 for AppImages (on Ubuntu 22.04 and newer:
`sudo apt install libfuse2`).

## First launch

A window opens with *Starting the local IndieK server…*, then shows the
graph explorer's home screen.

### Your author key

To write to an archive, you need an **author key**: the Ed25519 key that
signs everything you add (see
[authors and signatures](/docs/intro/#authors-and-signatures)). Without one,
you can open and read every archive, but not write.

On the first launch, the **Author key** dialog opens by itself. You can
reopen it at any time from the key chip in the header. Choose one of:

- **Create a new key.** The app creates the key, stores it in your system's
  keychain and immediately offers an **encrypted backup**: choose a password
  of at least 12 characters and keep the downloaded `.ikkey` file
  somewhere safe, away from your computer.
- **Import a key**, either from an encrypted backup (`.ikkey` file plus its
  password) or as the 64-character hexadecimal secret, for example the
  `IK_AUTHOR_PRIVATE_KEY` from a `.env` file used with `ik`.

> **Your key is your identity.** Everything you write is signed with it.
> If you lose the key and its backup, you can still read your archives, but
> you can no longer revise or tag what you wrote under that identity.
> Nobody, not even the IndieK developers, can recover it.

The header chip shows where the key comes from: `keychain`, or `env` when
the variable `IK_AUTHOR_PRIVATE_KEY` is set in the app's environment (it
then takes precedence over the keychain).

### Keychain prompts on macOS

The first time the app reads your key, macOS asks whether
*indiek-sidecar* may use the item *indiek* in your keychain. Enter your
password and click **Always Allow**. **Allow** works too, but macOS then
asks again at each launch, sometimes twice.

Because the first releases are unsigned, macOS asks again after each update
of the app.

<!-- TODO(owner): screenshot of the keychain prompt. -->

On Windows the key is kept in the **Credential Manager**, on Linux in the
**Secret Service** keyring (GNOME Keyring, KWallet), usually without
prompts. A Linux system without a Secret Service keyring cannot store the
key: set `IK_AUTHOR_PRIVATE_KEY` in the environment instead.

## Open or create an archive

On the home screen, type the **absolute path** of a folder and click:

- **Open workspace**, for an existing archive. The path may be the archive
  folder itself, or a folder (for example a git repository) that contains
  exactly one archive; if it contains several, the app lists them for you to
  pick.
- **New archive**, to start an archive in a new or empty folder.

The app edits the archive **in place**: no copy, no import. It remembers the
folders you opened (in `~/.indiek/workspaces.json`) and lists them on the
home screen. Removing one from the list never deletes its files.

The archive's files stay readable by every other tool: `ik`, the Python
SDK, `git`, a text editor. If you change an archive outside the app (for
example with `git pull`), the app verifies it again and shows the new state.

From there, the [web UI guide](/docs/web-ui/) explains everything you can do
with the graph.

## The `ik` command line

The app contains the full `ik` command line ([reference](/docs/cli/)). To use
it in a terminal on **macOS or Linux**, choose **Install ik Command…** in the
app menu (on macOS: **IndieK → Install ik Command…**).

- It writes `~/.local/bin/ik`, a two-line launcher for the app's bundled
  `ik`. No administrator password is needed.
- If `~/.local/bin` is not on your `PATH`, the dialog says so; add
  `export PATH="$HOME/.local/bin:$PATH"` to `~/.zshrc` (or your shell's
  profile).
- If an `ik` you installed yourself already exists there (for example with
  `uv tool install indiek`), the app asks before replacing it.
- The bundled `ik` is the same program as the app, so it signs with the same
  keychain key without further keychain prompts.
- After moving the app, choose the menu item again.

Not available on Windows yet: there, install `ik` with
`uv tool install 'indiek[cli]'` ([Get started](/docs/intro/#install)).

## Keep your key safe

### Back up

In the app: **Author key → Back up**. On the command line:

```bash
ik key_backup --out ~/indiek-key.ikkey   # asks for a password (12+ characters)
```

The backup is encrypted with your password (Argon2id). Keep it, and its
password, away from your computer: a USB key, a password manager.

### Where the key is stored

| System | Store | Item |
| --- | --- | --- |
| macOS | Keychain Access, *login* keychain | name `indiek`, account `author-seed` |
| Windows | Credential Manager → Windows Credentials | `author-seed@indiek` |
| Linux | Secret Service (GNOME *Passwords and Keys*, KWallet) | service `indiek`, username `author-seed` |

`ik key_show` prints the public key and where it comes from.

### Revoke the app's access, or delete the key

**Back up first** ([above](#back-up)). Deleting the keychain item deletes
your identity from this computer. Without a backup, it is gone for good.

- **macOS, revoke the app's access**: open *Keychain Access*, search
  `indiek`, double-click the item, open **Access Control** and remove
  *indiek-sidecar* (and *IndieK*). The app asks for permission again at its
  next launch. Some macOS versions delete the whole item when its access
  list is edited, which is one more reason to back up first.
- **macOS, delete**: in *Keychain Access*, right-click the item → **Delete**;
  or in Terminal:
  `security delete-generic-password -s indiek -a author-seed`.
- **Windows, delete**: *Control Panel → Credential Manager → Windows
  Credentials*, expand `author-seed@indiek`, **Remove**.
- **Linux, delete**: in *Passwords and Keys* (Seahorse), search `indiek` and
  delete the item; or `secret-tool clear service indiek username author-seed`.

To put the key back later: `ik key_restore ~/indiek-key.ikkey --keychain`,
or **Author key → Import** in the app.

## Update

Download and install the new release the same way: it replaces the old app
and keeps your workspace list and your key. There is no automatic update
yet. Each release lists its changes in the
[changelog](https://github.com/indiek/indiek-desktop/blob/main/CHANGELOG.md).

On macOS, the unsigned app asks again for keychain access after each update
([above](#keychain-prompts-on-macos)).

## Uninstall

| System | Remove the app |
| --- | --- |
| macOS | Drag IndieK from Applications to the Trash |
| Windows | Settings → Apps → IndieK → Uninstall |
| Linux | `.deb`: remove the package with your package manager. `.AppImage`: delete the file |

The app leaves behind, on purpose:

- **your archives**: they are your data, wherever you put them;
- your **key** in the keychain (delete it [as above](#revoke-the-apps-access-or-delete-the-key)
  only if you no longer need this identity);
- the workspace list `~/.indiek/workspaces.json` and the `ik` launcher
  `~/.local/bin/ik`: delete them by hand if you wish.

## Troubleshooting

| What you see | What to do |
| --- | --- |
| macOS: *"IndieK" Not Opened* / *Apple could not verify…* | Expected for unsigned builds: [Install → macOS](#macos) |
| macOS: *"IndieK" is damaged and can't be opened* | Run the `xattr` command of [Install → macOS](#macos) |
| Windows: *Windows protected your PC* | **More info → Run anyway** |
| The window stays on *Starting the local IndieK server…* for a long time | The first launch after an install or update can take about 15 s on macOS. If it ends with *The IndieK server stopped before it was ready*, see the next row |
| *The IndieK server could not be started* or *stopped before it was ready* | Quit and reopen the app. If it persists, start it from a terminal to see the error (macOS: `/Applications/IndieK.app/Contents/MacOS/IndieK`) and report it |
| Writes fail with *author key missing* | Create or import a key: [Your author key](#your-author-key) |
| The header chip says `env` and ignores the key you created | `IK_AUTHOR_PRIVATE_KEY` is set in the app's environment and takes precedence: remove it |
| Linux: *keychain unavailable* | No Secret Service keyring is running: install and unlock GNOME Keyring or KWallet, or set `IK_AUTHOR_PRIVATE_KEY` |
| *Archive integrity* error when opening an archive | The files on disk are inconsistent (a manual edit, a bad git merge): check with `ik verify` |
| *Archive locked* | Another program (often a long `ik` command) is writing to the same archive: wait and retry |
| `ik: command not found` after **Install ik Command…** | Add `~/.local/bin` to your `PATH` ([The `ik` command line](#the-ik-command-line)) and open a new terminal |

Something else? Report it on the
[desktop repository's issue tracker](https://github.com/indiek/indiek-desktop/issues).
