#!/usr/bin/env python3
"""Basit günlük görev takip aracı.

Kullanım:
    python gorev_takip.py ekle "Rapor yaz"
    python gorev_takip.py liste            # bugünün görevleri
    python gorev_takip.py liste --hepsi    # tüm görevler
    python gorev_takip.py bitti 1          # 1 numaralı görevi tamamla
    python gorev_takip.py sil 1            # 1 numaralı görevi sil
    python gorev_takip.py temizle          # tamamlananları sil
"""

import argparse
import json
from datetime import date
from pathlib import Path

DOSYA = Path(__file__).with_name("gorevler.json")


def yukle():
    if DOSYA.exists():
        return json.loads(DOSYA.read_text(encoding="utf-8"))
    return []


def kaydet(gorevler):
    DOSYA.write_text(
        json.dumps(gorevler, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def yeni_id(gorevler):
    return max((g["id"] for g in gorevler), default=0) + 1


def ekle(metin):
    gorevler = yukle()
    gorev = {
        "id": yeni_id(gorevler),
        "metin": metin,
        "tarih": date.today().isoformat(),
        "bitti": False,
    }
    gorevler.append(gorev)
    kaydet(gorevler)
    print(f"Eklendi: [{gorev['id']}] {metin}")


def listele(hepsi=False):
    bugun = date.today().isoformat()
    gorevler = yukle()
    if not hepsi:
        gorevler = [g for g in gorevler if g["tarih"] == bugun]

    if not gorevler:
        print("Gösterilecek görev yok.")
        return

    for g in gorevler:
        isaret = "x" if g["bitti"] else " "
        tarih = f" ({g['tarih']})" if hepsi else ""
        print(f"[{isaret}] {g['id']}. {g['metin']}{tarih}")

    biten = sum(g["bitti"] for g in gorevler)
    print(f"\nTamamlanan: {biten}/{len(gorevler)}")


def bitir(gorev_id):
    gorevler = yukle()
    for g in gorevler:
        if g["id"] == gorev_id:
            g["bitti"] = True
            kaydet(gorevler)
            print(f"Tamamlandı: {g['metin']}")
            return
    print(f"{gorev_id} numaralı görev bulunamadı.")


def sil(gorev_id):
    gorevler = yukle()
    kalan = [g for g in gorevler if g["id"] != gorev_id]
    if len(kalan) == len(gorevler):
        print(f"{gorev_id} numaralı görev bulunamadı.")
        return
    kaydet(kalan)
    print(f"Silindi: {gorev_id}")


def temizle():
    gorevler = yukle()
    kalan = [g for g in gorevler if not g["bitti"]]
    kaydet(kalan)
    print(f"{len(gorevler) - len(kalan)} tamamlanmış görev silindi.")


def main():
    parser = argparse.ArgumentParser(description="Günlük görev takip")
    alt = parser.add_subparsers(dest="komut", required=True)

    p = alt.add_parser("ekle", help="Yeni görev ekle")
    p.add_argument("metin")

    p = alt.add_parser("liste", help="Görevleri listele")
    p.add_argument("--hepsi", action="store_true", help="Tüm günleri göster")

    p = alt.add_parser("bitti", help="Görevi tamamla")
    p.add_argument("id", type=int)

    p = alt.add_parser("sil", help="Görevi sil")
    p.add_argument("id", type=int)

    alt.add_parser("temizle", help="Tamamlananları sil")

    args = parser.parse_args()

    if args.komut == "ekle":
        ekle(args.metin)
    elif args.komut == "liste":
        listele(args.hepsi)
    elif args.komut == "bitti":
        bitir(args.id)
    elif args.komut == "sil":
        sil(args.id)
    elif args.komut == "temizle":
        temizle()


if __name__ == "__main__":
    main()