// "The Daily World" — front page for Friday, 20 November 2026.
//
// The finished page is checked into this repo as entry.png. Running this
// program copies that exact file into the harness output directory, so
// the result of a second run is byte-for-byte the same as the first.
// A size check after the write makes a truncated copy fail loudly
// instead of slipping through as a broken entry. Before copying, the
// file is validated as a real PNG within the competition's limits:
// correct magic signature, at most 1 MiB, and at most 1024×1024 px.
import { mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const source = join(here, "entry.png");
const target = join(outDir, "entry.png");

const image = readFileSync(source);

// Validate the source before copying: it must be a real PNG within
// the competition's limits (≤ 1 MiB, ≤ 1024×1024 px).
const PNG_SIGNATURE = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
if (image.length > 1_048_576) {
  throw new Error(
    `entry.png is too large: ${image.length} bytes, ` +
      `limit is 1048576 bytes`,
  );
}
if (
  image.length < PNG_SIGNATURE.length ||
  !image.subarray(0, PNG_SIGNATURE.length).equals(PNG_SIGNATURE)
) {
  throw new Error("entry.png is not a valid PNG: bad magic signature");
}
if (image.length < 24 || image.toString("ascii", 12, 16) !== "IHDR") {
  throw new Error("entry.png is not a valid PNG: missing IHDR chunk");
}
const width = image.readUInt32BE(16);
const height = image.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(
    `entry.png is too large: ${width}x${height}px, ` +
      `limit is 1024x1024px`,
  );
}

mkdirSync(outDir, { recursive: true });
writeFileSync(target, image);

const written = statSync(target).size;
if (written !== image.length) {
  throw new Error(
    `entry.png was not copied whole: wrote ${written} bytes, ` +
      `expected ${image.length}`,
  );
}
