// "The Daily World" — front page for Friday, 20 November 2026.
//
// The finished page is checked into this repo as entry.png. Running this
// program copies that exact file into the harness output directory, so
// the result of a second run is byte-for-byte the same as the first.
// A size check after the write makes a truncated copy fail loudly
// instead of slipping through as a broken entry.
import { mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = join(here, "entry.png");
const target = join(outDir, "entry.png");

const image = readFileSync(source);
mkdirSync(outDir, { recursive: true });
writeFileSync(target, image);

const written = statSync(target).size;
if (written !== image.length) {
  throw new Error(
    `entry.png was not copied whole: wrote ${written} bytes, ` +
      `expected ${image.length}`,
  );
}
