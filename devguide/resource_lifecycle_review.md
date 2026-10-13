# Resource ownership and closeout

ArgDigest's component disposition under `uibcdf/argdigest#33` implements the
accepted `uibcdf/molsyssuite#104` policy. This operation and ownership review
does not certify platforms, engines, scientific workflows or installed packages.

| Operation | Owner and useful lifetime | Success/failure disposition |
| --- | --- | --- |
| Runtime configuration/import/registries | Application session; config files and selected provider are borrowed | Close readers; retain session declarations; never delete caller configuration or environments |
| Agent-doc generation | Caller-selected output, including the CLI's explicit current-directory output | Keep requested output; propagate/write-visible failures; never automatically delete a caller's document |
| Real CLI tests | Private `TemporaryDirectory` fixture for each node | Restore cwd before cleanup; retire outputs after both success and assertion failure; cleanup failures propagate |
| Other file tests | Private pytest fixtures | Retain only through useful failure analysis; task parent retires its owned fixture root |
| Thread/subprocess tests | Function-scoped executors and synchronous child processes/pipes | Context managers join/close; keep useful captured evidence; parent controls bounded fixtures |
| Collective imports | Temporary module/path context | Restore original namespaces in finally; sibling worktrees remain borrowed |
| Release/core/installed verifiers | Read-only source/prefix/archive inputs; caller-owned receipts | Close readers; preserve immutable identity and evidence; no deletion of source/prefix/package inputs |
| Version freezing | Caller supplies disposable build source | Mutate only explicit build inputs; never run on the primary checkout |
| Backlog/report/index tools | Repository-owned maintained output or caller receipt | Close file/network contexts; preserve unrelated output; archive reports rather than delete them |
| Documentation/wheel/Conda qualification | Task-owned disposable source/build/envs; shared caches borrowed | Review/retire after verification; keep original artifact receipts; no uncertain repeat upload/promotion |
| Hosted caller workflows | GitHub/provider-owned runner prefix/scratch and retained artifacts | Local wrappers inspected; external lifecycle implementation and actual cleanup remain provider-owned |

Guard: `tests/test_cli_resource_ownership.py` runs the actual CLI nodes from a
directory with a caller sentinel, on success and a controlled failure after the
real write. The sentinel must remain byte-identical and child scratch must be
empty. No real caller instructions are used as a fixture.

## Dated closeout — 2026-10-13

The original review reproduced caller-file loss and successful-output residue
despite green tests. The corrected nodes use a private managed workspace and
the four custody controls pass. Earlier bounded 2026-10-08 observations retain
their own source/date and are not silently extended.

Eight explicitly identified disposable roots from the completed 0.14.0 task
were retired: `/tmp/argdigest-governance`, `/tmp/argdigest-014-candidate`,
`/tmp/argdigest-windows-provider`, `/tmp/argdigest-014-core-rehearsal`,
`/tmp/argdigest-014-public`, `/tmp/argdigest-014-wheel`,
`/tmp/argdigest-014-wheel-source`, `/tmp/argdigest-014-wheel-target`.
The two Git clones had the original recorded heads and clean worktrees. Every
root was nonsymlink, UID-owned, with no observed owned-process cwd/exe/argv/FD
references, no foreign-owned entries and no unreadable owned process. The venv
was retired before its prefix base. These are current-task removals; no earlier
unattributed absence or reclaimed-byte count is inferred.

Before retirement a private wheel of the current source was checked off-checkout
on the public 0.11.0/0.16.0 dependency floors: core probe, import/CLI, absent
NumPy and `pip check` pass. Its private venv was retired first. The wheel version
is a development identity, not a public package/release claim.

Retained `/tmp/argdigest-014-producer` contains four small original sanitized
producer receipts (5900 logical bytes); exact old release receipts and source
ZIP remain useful for independent provenance after hosted artifact expiry.
ArgDigest maintainers own these records; review at next affected qualification
or 2026-11-03 and retire once an equivalent durable receipt is no longer needed.
The current source-provider checkout/private wheel evidence is task-owned by
#32 while its owner-reviewed PR/qualification remains active; retire disposable
build/venv/source after those checks, preserving the useful normalized receipt.

Primary repositories, shared development environments/caches and an external
prunable worktree registration were preserved. The latter belongs to another
task and requires its owner before any pruning. This review covered explicit
paths rather than a global `/tmp` inventory. The seven known #82 environment conflicts remain
visible; no dependency-closure claim is made for that shared environment.
