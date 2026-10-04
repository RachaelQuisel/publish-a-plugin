## Trigger

- The user asks to prepare a Claude Code plugin, fix a validation finding, or work on a directory submission.

## Inputs

- The plugin folder or repository supplies the package.
- The requested stage defines inspection, fixes, or submission work.
- A validation report identifies the finding when one is available.
- Available account access and authorization determine whether GitHub or directory actions can be completed.

## What happens

1. The plugin asks up to three questions about the target, requested stage, and current problem. It waits for missing answers and preserves supplied details.
2. It inspects the package and reads the reference that matches the issue. For a new package, it resolves the purpose and audience first.
3. It validates the manifest and runs the local preflight script. The script reads the package and reports findings.
4. When fixes are requested, it changes supported issues. It preserves required syntax, listing fields, licenses, and attribution. It does not invent a credential configuration to clear a false finding.
5. For an oversized icon, it can run the compression script. The script writes only after verifying that decoded pixels are identical.
6. It repeats the affected local checks. It reports unresolved findings and distinguishes observed scanner behavior from confirmed requirements.
7. When pushing or submitting is authorized, it verifies the repository state and completes the requested action through available tools. Missing access stops the dependent action.
8. After a pushed fix to an existing submission, the portal must revalidate the new commit. A policy hold means review is pending. It does not establish rejection or approval.

## Outputs

- Local validation results and requested package fixes.
- A GitHub push or directory submission only when authorized and completed.
- A clear statement of whether the result is local validation, a submission, a hold, or a visible listing.
