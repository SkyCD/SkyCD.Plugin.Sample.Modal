# SkyCD.Plugin.Sample.Modal

Demonstrates a blocking confirm-export modal with typed input and output contracts.

Install the sample from **Options → Plugins → Browse** in SkyCD 3.0 or later. Restart SkyCD after staging the installation.

To build from source, install the .NET 10 SDK and configure the SkyCD GitHub Packages source with a credential that has `read:packages` access. The [SkyCD SDK](https://github.com/SkyCD/SkyCD.SDK) defines the plugin contracts.

The project and its assets live under `src/SkyCD.Plugin.Sample.Modal/`.

```sh
dotnet restore src/SkyCD.Plugin.Sample.Modal/SkyCD.Plugin.Sample.Modal.csproj --locked-mode
dotnet pack src/SkyCD.Plugin.Sample.Modal/SkyCD.Plugin.Sample.Modal.csproj -c Release --no-restore
```

Licensed under BSD-2-Clause. See LICENSE.

## Host integration tests

The **SkyCD host integration** workflow runs on pull requests and can also be started from the Actions tab. It builds this checkout and runs the corresponding SkyCD host tests.

To run locally, check out SkyCD beside this repository at the revision pinned in `.github/workflows/host-integration.yml`. From this repository:

```sh
pwsh -File ../SkyCD/tools/scripts/ci/test-standalone-plugin.ps1 -PluginProject src/SkyCD.Plugin.Sample.Modal/SkyCD.Plugin.Sample.Modal.csproj
```

## Releases

After a version bump merges, tag the commit with the package version prefixed by `v`. GitHub Actions builds the package, publishes it to GitHub Packages, and attaches it to the GitHub Release. The Pages workflow regenerates the marketplace manifest and the NuGet registration feed from published releases.

To mirror an existing tagged version, run **Plugin NuGet** with that version. To regenerate metadata for all published releases, run **Publish marketplace feed**.
[Marketplace manifest](https://skycd.github.io/SkyCD.Plugin.Sample.Modal/plugins.json) · [NuGet service index](https://skycd.github.io/SkyCD.Plugin.Sample.Modal/index.json)
