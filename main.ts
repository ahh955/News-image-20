// Entry point for the make.fun news-image-20261120 entry.
// Copies the pre-built entry.png into the output directory and validates it.
// Node 22 standard library only; no network access.
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const SRC = new URL("./entry.png", import.meta.url).pathname;
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const DEST = join(OUT_DIR, "entry.png");

const buf = readFileSync(SRC);
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!buf.subarray(0, 8).equals(PNG_SIG)) {
  throw new Error("entry.png: bad PNG signature");
}
if (buf.subarray(12, 16).toString("ascii") !== "IHDR") {
  throw new Error("entry.png: first chunk is not IHDR");
}
if (buf.length > 1024 * 1024) {
  throw new Error(`entry.png: ${buf.length} bytes exceeds 1 MiB`);
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`entry.png: ${width}x${height} exceeds 1024x1024`);
}
mkdirSync(OUT_DIR, { recursive: true });
copyFileSync(SRC, DEST);
console.log(`entry.png copied to ${DEST} (${width}x${height}, ${statSync(DEST).size} bytes)`);
