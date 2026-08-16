# Running Claude Code in the Terminal — Windows Setup

*A slow, one-step-at-a-time guide. On Windows the trick is: you don't use the plain
Command Prompt — you install a small Linux environment inside Windows (called **WSL**)
and run Claude Code from there. This is also the best home for Python projects like the
betting models.*

**The whole journey:** install WSL → install Node → install Claude Code → log in →
clone a repo → run `claude`. Parts 1–4 are one-time. After that, daily use is just Part 6.

---

## Part 1 — Install WSL (one time)

1. Click Start, type **PowerShell**, right-click it, choose **Run as administrator**.
2. In that window, type this and press Enter:
   ```
   wsl --install
   ```
3. Let it finish, then **reboot** when it tells you to.
4. After the reboot, an **Ubuntu** window opens by itself and asks you to create a
   username and password.
   - Pick simple ones you'll remember.
   - **The password looks like nothing is typing — that's normal.** It's hidden. Just
     type it and press Enter.

✅ **Checkpoint:** you end up at a prompt that looks like `alec@DESKTOP:~$`. That blinking
line is the Linux terminal. From here on, use *this* Ubuntu window — not PowerShell.

*If `wsl --install` throws an error:* usually it's virtualization turned off in the BIOS,
or it needs `wsl --install -d Ubuntu`. Copy me the exact error and I'll sort it.

---

## Part 2 — Install Node.js (one time, in the Ubuntu window)

Claude Code runs on Node. Install it with `nvm` (a version manager):

1. Paste this and press Enter:
   ```
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
   ```
2. **Close the Ubuntu window and open it again** (Start → Ubuntu). This matters — it's how
   the terminal notices nvm.
3. Install Node:
   ```
   nvm install --lts
   ```

✅ **Checkpoint:** type `node --version` — you should see something like `v20.x.x`.

---

## Part 3 — Install Claude Code (one time)

```
npm install -g @anthropic-ai/claude-code
```

✅ **Checkpoint:** type `claude --version` — you should see a version number.

---

## Part 4 — Log in (one time)

1. Type `claude` and press Enter.
2. It prints a link and opens your browser. **Log in with the same account you use on the
   web/app** — same subscription, nothing new to buy.
3. The terminal confirms you're signed in.

---

## Part 5 — Get a repo onto your machine

The writing repo is **public**, so it needs no extra login:

```
cd ~
git clone https://github.com/jackiemoon555/Writing-Skills-and-Tools.git
cd Writing-Skills-and-Tools
git pull
```

✅ **Checkpoint:** type `ls` — you should see `docs`, `manuscripts`, `reports`, etc.

Then start Claude in the project:
```
claude
```

*Private repos (nfl-bets, ufc-bets, stocks-, Side-Hustles-) need a GitHub login step first.*
The easiest way is the GitHub CLI (`gh auth login`) — a 2-minute thing. Ping me when you
want to pull one of those down and I'll walk you through just that part.

---

## Part 6 — Daily use (every time after setup)

1. Open the **Ubuntu** window (Start → Ubuntu).
2. Go to the project and grab anything new:
   ```
   cd ~/Writing-Skills-and-Tools
   git pull
   ```
3. Start Claude:
   ```
   claude
   ```
4. When you're done for the day, save your work back to GitHub (or just ask Claude to):
   ```
   git add -A
   git commit -m "today's notes"
   git push
   ```

---

## The two places people trip

1. **Wrong window.** After Part 1, everything happens in the **Ubuntu** window, not
   PowerShell or Command Prompt. If a command "isn't found," check which window you're in.
2. **`node`/`claude` not found right after installing.** Close the Ubuntu window and
   reopen it, then try again — a fresh window reloads the setup.

Stuck on any single step? Copy the exact line that failed and the error text, and I'll
get you past it. No need to figure it out alone — that's what tripped it up last time.
