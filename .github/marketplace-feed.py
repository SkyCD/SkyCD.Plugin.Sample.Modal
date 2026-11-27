import io
import json
import os
from pathlib import Path
import re
import subprocess
import urllib.request
import xml.etree.ElementTree as ET
from zipfile import ZipFile

repository = os.environ["GITHUB_REPOSITORY"]
package_id = repository.split("/")[1]
base = os.environ["PAGES_URL"].rstrip("/")
project_url = f"https://github.com/{repository}"
registration = f"{base}/registration/{package_id.lower()}/index.json"
root = Path("_site")

def write(path, content):
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(content, indent=2) + "\n", encoding="utf-8")

def dependency_groups(metadata):
    groups = []
    dependencies = metadata.find("dependencies")
    if dependencies is None:
        return groups
    for group in dependencies.findall("group") or [dependencies]:
        entry = {"dependencies": [
            {"id": dependency.attrib["id"], "range": dependency.attrib.get("version") or "(,)"}
            for dependency in group.findall("dependency")
        ]}
        if "targetFramework" in group.attrib:
            entry["targetFramework"] = group.attrib["targetFramework"]
        groups.append(entry)
    return groups

pages = json.loads(subprocess.check_output([
    "gh", "api", "--paginate", "--slurp", f"repos/{repository}/releases?per_page=100"
], text=True))
releases = []
entries = []
for page in pages:
    for release in page:
        tag = release["tag_name"]
        if release["draft"] or not re.fullmatch(r"v\d+\.\d+\.\d+(?:\.\d+)?(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?", tag):
            continue
        version = tag[1:]
        asset_name = f"{package_id}.{version}.nupkg"
        asset = next((asset["browser_download_url"] for asset in release["assets"]
                      if asset["name"] == asset_name and asset["state"] == "uploaded"), None)
        if asset is None:
            continue
        if asset != f"{project_url}/releases/download/{tag}/{asset_name}":
            raise ValueError(f"Unexpected asset URL for {tag}")
        with urllib.request.urlopen(asset, timeout=30) as response:
            content = response.read(64 * 1024 * 1024 + 1)
        if len(content) > 64 * 1024 * 1024:
            raise ValueError(f"Package exceeds the marketplace size limit for {tag}")
        with ZipFile(io.BytesIO(content)) as package:
            with package.open(f"{package_id}.nuspec") as nuspec:
                document = ET.fromstring(nuspec.read(256 * 1024 + 1))
        for element in document.iter():
            element.tag = element.tag.split("}")[-1]
        metadata = document.find("metadata")
        if metadata is None or metadata.findtext("id") != package_id or metadata.findtext("version") != version:
            raise ValueError(f"Package identity does not match {tag}")

        details = {"id": package_id, "version": version, "listed": True,
                   "dependencyGroups": dependency_groups(metadata)}
        entry = {"catalogEntry": details, "packageContent": asset}
        releases.append({"version": version, **json.loads(os.environ["HOST_RANGE"])})
        entries.append(entry)

if not entries:
    raise ValueError("No published plugin packages found")

entries.sort(key=lambda entry: entry["catalogEntry"]["version"].lower())
items = []
for entry in entries:
    version = entry["catalogEntry"]["version"].lower()
    leaf_url = f"{base}/registration/{package_id.lower()}/{version}.json"
    detail_url = f"{base}/registration/{package_id.lower()}/{version}.metadata.json"
    entry["@id"] = leaf_url
    entry["registration"] = registration
    entry["catalogEntry"]["@id"] = detail_url
    write(f"registration/{package_id.lower()}/{version}.json", {
        "@id": leaf_url, "catalogEntry": detail_url, "packageContent": entry["packageContent"],
        "registration": registration, "listed": True,
    })
    write(f"registration/{package_id.lower()}/{version}.metadata.json", entry["catalogEntry"])
    items.append({"@id": leaf_url, "lower": version, "upper": version, "count": 1, "items": [entry]})

write("registration/" + package_id.lower() + "/index.json", {"@id": registration, "count": len(items), "items": items})
write("index.json", {"version": "3.0.0", "resources": [
    {"@id": f"{base}/registration/", "@type": "RegistrationsBaseUrl/3.6.0"}
]})
project = ET.parse(f"{package_id}.csproj")
write("plugins.json", {"schemaVersion": 1, "publisher": "SkyCD", "projectUrl": project_url,
                       "feed": f"{base}/index.json", "packages": [{"id": package_id, "projectUrl": project_url,
                       "displayName": project.findtext(".//AssemblyTitle"), "summary": project.findtext(".//Description"),
                       "license": "BSD-2-Clause", "releases": releases}]})
