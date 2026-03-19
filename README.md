# fix-steam-launch

> Lightweight utility to resolve Steam launcher issues by clearing corrupted cache files.

---

## Description

`fix-steam-launch` is a small tool designed to fix cases where Steam refuses to launch due to broken or outdated cache data.

It works by removing specific non-essential files inside the Steam directory that are known to cause startup issues.

---

## Important Notice

```
This tool will remove cached login/session data.
You may be logged out after Steam starts successfully.
```

Make sure you have access to:
- your email
- your password
- Steam Guard (if enabled)

For faster login, consider using the Steam Mobile App to scan the QR code on login.

---

## Permissions

```
Administrator privileges may be required
```

Reason:
- Steam is often installed in protected directories (e.g. `Program Files`)
- Elevated access is needed to modify or delete cache files

---

## What the program does

```
Removes:
  - appcache/
  - temporary cache files
  - session-related data
```

```
Does NOT remove:
  - installed games
  - personal files
  - account data stored on Steam servers
```

---

## Usage

```
1. Run the script
2. Let it clean the cache
3. Launch Steam
4. Log in again if required
```

---

## Disclaimer

```
Use at your own risk.
```

This tool only targets cache files, but you are responsible for ensuring you can access your account before using it.

---

## License

MIT License, free to use, modify, and distribute.
