import json
import os
import subprocess
import sys

VEO_DIR = r"C:\Users\Owner\Radio-IA-Fala-Brasil\Artistas\13-MC-Foguete\Clipe-Passageiro\Clipes-Veo"
CHUNK_DIR = r"C:\Users\Owner\AppData\Local\Temp\claude\C--Users-Owner\76d66d91-2272-4e59-b55e-241596b8466d\scratchpad\montagem\chunks"
STILL_DIR = r"C:\Users\Owner\AppData\Local\Temp\claude\C--Users-Owner\76d66d91-2272-4e59-b55e-241596b8466d\scratchpad\montagem\still"

W, H, FPS = 1280, 720, 24

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("CMD FAILED:", " ".join(cmd))
        print(r.stderr[-2000:])
        sys.exit(1)

def main():
    with open("chunks.json", encoding="utf-8") as f:
        chunks = json.load(f)

    filelist_path = os.path.join(CHUNK_DIR, "..", "concat_list.txt")
    lines = []

    for idx, c in enumerate(chunks):
        out = os.path.join(CHUNK_DIR, f"{idx:03d}.mp4")
        scene_path = os.path.join(VEO_DIR, f"cena{c['scene']:02d}.mp4")

        if c["kind"] == "clip":
            cmd = [
                "ffmpeg", "-y", "-ss", str(c["offset"]), "-i", scene_path,
                "-t", str(c["length"]),
                "-an", "-r", str(FPS),
                "-vf", f"scale={W}:{H}:force_original_aspect_ratio=decrease,pad={W}:{H}:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p",
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                out,
            ]
        else:  # stillzoom
            still_path = os.path.join(STILL_DIR, f"scene{c['scene']:02d}_last.png")
            if not os.path.exists(still_path):
                run(["ffmpeg", "-y", "-sseof", "-0.15", "-i", scene_path, "-vframes", "1", still_path])
            frames = int(c["length"] * FPS) + 2
            zoom_expr = "min(zoom+0.0006,1.06)"
            cmd = [
                "ffmpeg", "-y", "-loop", "1", "-i", still_path, "-t", str(c["length"]),
                "-vf", (
                    f"scale={W*2}:{H*2},"
                    f"zoompan=z='{zoom_expr}':d={frames}:s={W}x{H}:fps={FPS},"
                    f"format=yuv420p"
                ),
                "-c:v", "libx264", "-preset", "fast", "-crf", "18",
                out,
            ]

        print(f"[{idx:03d}/{len(chunks)}] {c['kind']} cena{c['scene']:02d} off={c['offset']} len={c['length']} -> {out}")
        run(cmd)
        lines.append(f"file '{out}'")

    with open(filelist_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("Wrote concat list:", filelist_path)

if __name__ == "__main__":
    main()
