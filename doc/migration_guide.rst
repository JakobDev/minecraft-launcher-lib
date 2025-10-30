Migration Guide
==================================================
minecraft-launcher-lib strives to maintain a backwards-compatible API. However, because it is built around Minecraft and its ecosystem, breaking changes are occasionally necessary to accommodate upstream changes.

In most cases, old functions are deprecated rather than removed, so upgrading to the latest release and performing migrations later is possible.

Always use the latest version of minecraft-launcher-lib to ensure compatibility with newer Minecraft versions and to receive bug fixes.

The :doc:`changelog </changelog>` lists all changes; this page summarizes the actions developers must take when upgrading their code. If an API change is missing from this page, treat it as a bug and report it.

-------------------------
8.0
-------------------------

- The ``forge``, ``fabric`` and ``quilt`` modules have been replaced by the new ``mod_loader`` module.
  The old modules still exist but will no longer receive bug fixes and may be removed in a future release.

