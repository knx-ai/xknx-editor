"""Map version-specific `files.vXX` models onto the unified `intermediate` model.

Most fields copy across by name; only real schema divergences plus a few data rules (such as
synthesized PUIDs for pre-v12 projects) need explicit overrides. The sibling `scripts/` folder
holds the worklist generator and the Mermaid diagram renderer.
"""
