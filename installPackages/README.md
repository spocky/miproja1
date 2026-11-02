# Contributing to Projectivy's App Catalog

Projectivy Launcher includes a catalog of third-party apps, wallpaper providers, and icon packs that users can discover and install directly from the launcher.

**Community contributions are welcome!** ❤️

If you've developed an app, plugin, or icon pack compatible with Android TV and Projectivy, or know of something useful that's missing from the catalog, feel free to submit a Pull Request!

The catalog is also used on the [Projectivy website](https://projectivylauncher.com/plugins.html), so please follow the guidelines below.

## How to contribute

1. Find the appropriate category file in this directory:
   - `wallpaper-plugin.json` — Wallpaper providers
   - `icon-pack.json` — Icon packs
   - `file-manager.json` — File managers
   - `misc.json` — Other useful Android TV apps
2. Add your app to the `apps` array, following the existing format.
3. Submit a Pull Request with a brief explanation of what your app does.

Please don't edit `generic.v3.json` directly. It is automatically updated from these category files.

## App fields

| Field | Required | Description |
|---|---|---|
| `name` | Yes | Display name of the application. |
| `package` | Yes | Android application package name (e.g. `com.example.myapp`). |
| `googleplay` | No | Boolean indicating whether the app is available on Google Play. Defaults to `false` when omitted; set to `true` only after checking the Play Store listing for the exact `package`. |
| `url` | Conditional | Direct HTTPS URL to download the APK. Required if the app isn't available on the Play Store and no Downloader code is provided. |
| `downloader` | Conditional | Downloader by AFTVnews code. Can be used instead of a direct APK URL. |
| `description` | Recommended | Short English description, **maximum 2 sentences**. |
| `image` | Recommended | Public HTTPS URL to an image representing the app. |
| `official` | Reserved | Indicates an official Projectivy plugin. Please don't set this field yourself. |

The `category` field is defined at the top of each category file, so you don't need to repeat it for individual apps.

### Installation requirements

Every app must have a valid `name` and `package`.

If the app is available on Google Play, set `googleplay` to `true`; the package name is sufficient as an installation method. Check the listing at `https://play.google.com/store/apps/details?id=<package>`. Availability may vary by country and device.

Otherwise, please provide at least one installation method:

- A direct APK download URL (`url`), preferably pointing to a GitHub release.
- A Downloader code (`downloader`).

Whenever possible, prefer stable download URLs (such as GitHub's `releases/latest/download/...`) over links tied to a specific version.

## Descriptions and images

Descriptions should be in **English, concise, and no longer than two sentences**. Explain what makes the app useful rather than writing promotional text.

Images are displayed on the Projectivy website, where all plugin images may be loaded at once. Please keep them reasonably small:

- Prefer WebP or optimized JPEG/PNG.
- Aim for **under 200 KB**, if possible.
- Use a landscape image that clearly represents the app.
- Avoid unnecessarily large resolutions or multi-megabyte images.
- Use a stable, publicly accessible HTTPS URL.

**Can't host an image yourself?** No problem! You can attach it to your Pull Request or send it to me, and I'll take care of hosting it.

## Example

```json
{
  "name": "My Wallpaper Provider",
  "package": "com.example.wallpaperprovider",
  "googleplay": false,
  "url": "https://github.com/example/my-plugin/releases/latest/download/plugin.apk",
  "description": "Displays beautiful landscape wallpapers from a curated collection. Supports automatic wallpaper rotation.",
  "image": "https://example.com/images/plugin.webp"
}
```

## A few notes

- Please only submit apps that are relevant to Android TV or Projectivy Launcher.
- Make sure the package name and installation links are correct.
- Don't include pirated, modified, or unauthorized APK distributions.
- Existing entries can also be improved! Feel free to submit PRs to update descriptions, images, or outdated download links.
- Submissions may be reviewed, edited, or declined to keep the catalog useful and trustworthy.

Thanks for helping make Projectivy better for everyone! ❤️
