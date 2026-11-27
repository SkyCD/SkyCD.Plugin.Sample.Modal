# SkyCD.Plugin.Sample.Modal

Demonstrates a blocking confirm-export modal with typed input and output contracts.

Install the sample from **Options → Plugins → Browse** in SkyCD 3.0 or later. Restart SkyCD after staging the installation.

To build from source, install the .NET 10 SDK and configure the SkyCD GitHub Packages source with a credential that has read:packages access. Run dotnet restore --locked-mode, then dotnet pack -c Release --no-restore. The [SkyCD SDK](https://github.com/SkyCD/SkyCD.SDK) defines the plugin contracts.


Licensed under BSD-2-Clause. See LICENSE.

## Releases

After a version bump merges, tag the commit with the package version prefixed by `v`. GitHub Actions builds the package, publishes it to GitHub Packages, and attaches it to the GitHub Release. The Pages workflow regenerates the marketplace manifest and the NuGet registration feed from published releases.

To mirror an existing tagged version, run **Plugin NuGet** with that version. To regenerate metadata for all published releases, run **Publish marketplace feed**.
[Marketplace manifest](https://skycd.github.io/SkyCD.Plugin.Sample.Modal/plugins.json) · [NuGet service index](https://skycd.github.io/SkyCD.Plugin.Sample.Modal/index.json)
