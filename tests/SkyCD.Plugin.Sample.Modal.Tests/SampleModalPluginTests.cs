using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using SkyCD.SDK.Capabilities.Modal;
using SkyCD.Testing;
using Xunit;

namespace SkyCD.Plugin.Sample.Modal.Tests;

public sealed class SampleModalPluginTests
{
    [Fact]
    public void AssemblyDeclaresModalCapability()
    {
        var metadata = PluginAssemblyMetadata.Inspect(typeof(SampleModalPlugin).Assembly);

        Assert.Equal("SkyCD.Plugin.Sample.Modal", metadata.Id);
        Assert.Contains(typeof(SampleModalPlugin), metadata.CapabilityTypes);
    }

    [Fact]
    public void DeclaresExportPermissionsAndPayloadContracts()
    {
        var descriptor = new SampleModalPlugin().Modal;

        Assert.Equal("sample.modal.confirm-export", descriptor.ModalId);
        Assert.Equal(new[] { "catalog.read", "catalog.export" }, descriptor.RequiredPermissions);
        Assert.Equal(new ModalPayloadContract("sample.modal.confirm-export.input", IsRequired: true), descriptor.InputContract);
        Assert.Equal(new ModalPayloadContract("sample.modal.confirm-export.output", IsRequired: true), descriptor.OutputContract);
    }

    [Fact]
    public async Task OpenReturnsConfirmationPayload()
    {
        var plugin = new SampleModalPlugin();
        var result = await plugin.OpenModalAsync(new ModalOpenRequest
        {
            ModalId = "sample.modal.confirm-export",
            Input = new ModalPayload("sample.modal.confirm-export.input", new Dictionary<string, object?>
            {
                ["selectedCount"] = 3
            }),
            GrantedPermissions = ["catalog.read", "catalog.export"]
        });

        Assert.True(result.Success, result.Error);
        Assert.Equal("sample.modal.confirm-export.output", result.Output!.TypeId);
        var payload = Assert.IsType<Dictionary<string, object?>>(result.Output.Value);
        Assert.True(Assert.IsType<bool>(payload["confirmed"]));
        Assert.Equal(DateTimeKind.Utc, Assert.IsType<DateTime>(payload["timestampUtc"]).Kind);
    }

    [Fact]
    public async Task OpenRejectsUnknownModal()
    {
        var result = await new SampleModalPlugin().OpenModalAsync(new ModalOpenRequest
        {
            ModalId = "sample.modal.unknown"
        });

        Assert.False(result.Success);
        Assert.Contains("Unsupported modal", result.Error);
    }
}
