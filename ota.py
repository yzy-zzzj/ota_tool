import argparse, hashlib, json, os, sys, time, random

def checksum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1<<16), b""):
            h.update(chunk)
    return h.hexdigest()

def sign(path, version):
    ck = checksum(path)
    meta = {"version": version, "checksum": ck, "size": os.path.getsize(path), "timestamp": int(time.time())}
    sigpath = path + ".sig.json"
    with open(sigpath, "w") as f:
        json.dump(meta, f, indent=2)
    print(f"Wrote {sigpath}")

def rollout(path, canary, fleet):
    with open(fleet) as f:
        devices = [x.strip() for x in f if x.strip()]
    sample = random.sample(devices, max(1, len(devices)*canary//100))
    report = {"total": len(devices), "canary": canary, "devices": sample, "image": os.path.basename(path)}
    out = "rollout_report.json"
    with open(out, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Created {out}")

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    s1 = sub.add_parser("sign")
    s1.add_argument("path")
    s1.add_argument("version")
    s2 = sub.add_parser("rollout")
    s2.add_argument("path")
    s2.add_argument("--canary", type=int, default=5)
    s2.add_argument("--fleet", required=True)
    args = ap.parse_args()
    if args.cmd == "sign": sign(args.path, args.version)
    else: rollout(args.path, args.canary, args.fleet)

if __name__ == "__main__":
    main()
