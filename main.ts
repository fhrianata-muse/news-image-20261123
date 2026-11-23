// The World in One Day — Monday 23 November 2026.
// Entry program: copies the front-page image this repository holds
// to the grader's output directory as /output/entry.png, and refuses
// to write anything else: the copied bytes must match the image's
// measured SHA-256, so a swapped or truncated image fails loudly
// instead of entering the heat as a different picture.
// No network, no clock, no randomness: the same bytes every run.
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const EXPECTED_SHA256 =
  "ebd408f6562fb93575b4215339f06c15f158fa248e2853bbf97a32a4934fe146";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const bytes = readFileSync(source);
const actual = createHash("sha256").update(bytes).digest("hex");
if (actual !== EXPECTED_SHA256) {
  throw new Error(
    `entry.png sha256 mismatch: expected ${EXPECTED_SHA256}, got ${actual}`,
  );
}
mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, "entry.png"));
