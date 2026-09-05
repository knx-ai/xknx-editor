"""Resolving a GitHub release *page* URL to its downloadable asset for "Load OpenKNX from URL"."""

from __future__ import annotations

import pytest

from editor_gui.main import _github_release_api_url, _pick_release_asset


def test_release_tag_url_maps_to_tags_api():
    assert (
        _github_release_api_url(
            "https://github.com/OpenKNX/OAM-PresenceModule/releases/tag/3.6.2-Release"
        )
        == "https://api.github.com/repos/OpenKNX/OAM-PresenceModule/releases/tags/3.6.2-Release"
    )


def test_latest_and_repo_and_releases_map_to_latest_api():
    latest = "https://api.github.com/repos/OpenKNX/OAM-PresenceModule/releases/latest"
    assert (
        _github_release_api_url("https://github.com/OpenKNX/OAM-PresenceModule")
        == latest
    )
    assert (
        _github_release_api_url(
            "https://github.com/OpenKNX/OAM-PresenceModule/releases"
        )
        == latest
    )
    assert (
        _github_release_api_url(
            "https://github.com/OpenKNX/OAM-PresenceModule/releases/latest"
        )
        == latest
    )


def test_direct_asset_and_non_github_pass_through():
    # A direct asset download URL is not a release page -> None (caller downloads it as-is).
    assert (
        _github_release_api_url(
            "https://github.com/OpenKNX/OAM-PresenceModule/releases/download/3.6.2-Release/PresenceModule-Big-3.6.2.zip"
        )
        is None
    )
    assert _github_release_api_url("https://example.com/foo.knxprod") is None


def test_pick_asset_prefers_knxprod_then_zip():
    assets = [
        {"name": "notes.txt", "browser_download_url": "u-txt"},
        {"name": "App.zip", "browser_download_url": "u-zip"},
        {"name": "App.knxprod", "browser_download_url": "u-knxprod"},
    ]
    assert _pick_release_asset(assets) == "u-knxprod"
    assert _pick_release_asset(assets[:2]) == "u-zip"


def test_pick_asset_single_zip():
    assets = [{"name": "PresenceModule-Big-3.6.2.zip", "browser_download_url": "u"}]
    assert _pick_release_asset(assets) == "u"


def test_pick_asset_errors_on_none_and_ambiguous():
    with pytest.raises(ValueError, match=r"no \.knxprod or \.zip"):
        _pick_release_asset([{"name": "readme.md", "browser_download_url": "u"}])
    with pytest.raises(ValueError, match="several assets"):
        _pick_release_asset(
            [
                {"name": "a.zip", "browser_download_url": "ua"},
                {"name": "b.zip", "browser_download_url": "ub"},
            ]
        )
