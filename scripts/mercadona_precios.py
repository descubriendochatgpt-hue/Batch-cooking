#!/usr/bin/env python3
"""Descarga el catálogo de alimentación de la tienda online de Mercadona
para un código postal (por defecto Gijón, 33201) y lo guarda como JSON
listo para cargar en la base de datos de la app (documento precios/mercadona).

Uso:  python3 scripts/mercadona_precios.py [--cp 33201] [--wh ovi1] [--out precios.json]

Formato de salida:
  {"actualizado": "2026-09-24", "cp": "33201", "wh": "...",
   "items": [[nombre, envase, precio envase, precio referencia, unidad referencia, categoría], ...]}
"""
import argparse, datetime, json, sys, time, urllib.request

API = "https://tienda.mercadona.es/api"
HEADERS = {"User-Agent": "Mozilla/5.0 (planificador familiar)", "Accept": "application/json"}
# Categorías que no son comida para casa
EXCLUIR = ("limpieza", "mascota", "cuidado", "maquillaje", "fitoterapia", "bebé", "bebe", "higiene", "hogar")


def get(path, wh):
    sep = "&" if "?" in path else "?"
    req = urllib.request.Request(f"{API}{path}{sep}lang=es&wh={wh}", headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def almacen_para(cp):
    body = json.dumps({"new_postal_code": cp}).encode()
    req = urllib.request.Request(f"{API}/postal-codes/actions/change-pc/", data=body, method="PUT",
                                 headers={**HEADERS, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        wh = r.headers.get("x-customer-wh")
    if not wh:
        sys.exit(f"Mercadona no devolvió almacén para el código postal {cp}; pásalo con --wh")
    return wh


def num(x):
    try:
        return round(float(x), 2)
    except (TypeError, ValueError):
        return 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cp", default="33201")
    ap.add_argument("--wh")
    ap.add_argument("--out", default="precios_mercadona.json")
    a = ap.parse_args()
    wh = a.wh or almacen_para(a.cp)
    items, vistos = [], set()
    for top in get("/categories/", wh)["results"]:
        if any(w in top["name"].lower() for w in EXCLUIR):
            continue
        for sub in top.get("categories", []):
            data = get(f"/categories/{sub['id']}/", wh)
            time.sleep(0.3)
            for grupo in data.get("categories", []):
                for p in grupo.get("products", []):
                    if p["id"] in vistos:
                        continue
                    vistos.add(p["id"])
                    pi = p.get("price_instructions", {})
                    envase = " ".join(str(x) for x in (p.get("packaging"), pi.get("unit_size"), pi.get("size_format")) if x)
                    items.append([p["display_name"], envase, num(pi.get("unit_price")),
                                  num(pi.get("reference_price") or pi.get("bulk_price")),
                                  pi.get("reference_format") or pi.get("size_format") or "ud", top["name"]])
    out = {"actualizado": datetime.date.today().isoformat(), "cp": a.cp, "wh": wh, "items": items}
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
    print(f"{len(items)} productos guardados en {a.out}")


if __name__ == "__main__":
    main()
