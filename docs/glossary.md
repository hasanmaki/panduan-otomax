---
glossary: otomax
title: Glossarium Otomax
---

## Cara Mendefinisikan Istilah (singkat)

- Gunakan format *definition list*:

  istilah
  :   Definisi singkat. Contoh: `parsing\n:   Proses membaca balasan provider...`

- Untuk definisi panjang, gunakan baris baru dan spasi indentasi:

  istilah_panjang
  :   Paragraf pertama.

      Paragraf kedua (baris kosong di atas).

- Untuk section/namespace, pastikan front-matter ada `glossary: otomax` dan gunakan link `<otomax:istilah>` di konten.

- Contoh referensi di halaman lain: `<otomax:parsing|baca parsing>` atau jika `markdown_links: true`: `[baca parsing](otomax:parsing)`.

---

## Daftar Istilah

{%
  glossary-summary
  section="otomax"
  theme="detailed"
%}

---

## Definisi

*`otomax:parsing`*
:   Proses Otomax membaca balasan dari server provider (misal: `"SUCESS 12345"`) untuk mengubah status transaksi dari *Proses* menjadi *Sukses* atau *Gagal*.

*`otomax:deposit`*
:   Dana yang ditransfer ke rekening BNI Otomax (bukan ke provider). Harus diproses di menu `Deposit` agar masuk ke saldo sistem.

*`otomax:saldo_deposit`*
:   Saldo di dalam Otomax — uang yang siap dipakai untuk beli pulsa/tagihan.

*`otomax:saldo_provider`*
:   Kredit di server provider (Telkomsel/XL/PLN). Diisi otomatis saat transaksi sukses.

*`otomax:komisi_tunda`*
:   Komisi penjualan yang belum diambil reseller. Masih tersimpan di database sampai diklaim.

*`otomax:grup_reseller`*
:   Kelompok reseller dengan harga jual & komisi yang sama. Salah pilih grup = salah harga!

*`otomax:voucher_fisik`*
:   Struk cetak berisi kode isi ulang (nomor seri) — untuk dijual ke agen atau pelanggan langsung.
