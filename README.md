# SkyCD.Plugin.Sample.Modal

Demonstrates a blocking confirm-export modal with typed input and output contracts.

Install the sample from **Options → Plugins → Browse** in SkyCD 3.0 or later. Restart SkyCD after staging the installation.

To build from source, install the .NET 10 SDK and configure the SkyCD GitHub Packages source with a credential that has read:packages access. Run dotnet restore --locked-mode, then dotnet pack -c Release --no-restore. The [SkyCD SDK](https://github.com/SkyCD/SkyCD.SDK) defines the plugin contracts.

The marketplace reads plugins.json and the anonymous NuGet v3 package feed under feed/. For each release, build the package with a new version, add the lowercase package file under feed/packages/<id>/<version>/, and update the package version index and publisher manifest together. Keep previously published versions available.

Licensed under BSD-2-Clause. See LICENSE.

After the feed update merges, tag that commit with the package version prefixed by `v`. GitHub Actions verifies the build, publishes the same package to GitHub Packages, and attaches it to a GitHub release. To mirror an existing tagged version, run the **Plugin NuGet** workflow with that version.
