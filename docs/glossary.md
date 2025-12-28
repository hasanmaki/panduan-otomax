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

<dl>
  <dt>otomax:parsing</dt>
  <dd>Proses Otomax membaca balasan dari server provider (misal: `"SUCESS 12345"`) untuk mengubah status transaksi dari *Proses* menjadi *Sukses* atau *Gagal*.</dd>
</dl>

<dl>
  <dt>otomax:deposit</dt>
  <dd>Dana yang ditransfer ke rekening BNI Otomax (bukan ke provider). Harus diproses di menu `Deposit` agar masuk ke saldo sistem.</dd>
  <dt>otomax:saldo_deposit</dt>
  <dd>Saldo di dalam Otomax — uang yang siap dipakai untuk beli pulsa/tagihan.</dd>
  <dt>otomax:saldo_provider</dt>
  <dd>Kredit di server provider (Telkomsel/XL/PLN). Diisi otomatis saat transaksi sukses.</dd>
  <dt>otomax:komisi_tunda</dt>
  <dd>Komisi penjualan yang belum diambil reseller. Masih tersimpan di database sampai diklaim.</dd>
  <dt>otomax:grup_reseller</dt>
  <dd>Kelompok reseller dengan harga jual & komisi yang sama. Salah pilih grup = salah harga!</dd>
  <dt>otomax:voucher_fisik</dt>
  <dd>Struk cetak berisi kode isi ulang (nomor seri) — untuk dijual ke agen atau pelanggan langsung.</dd>
</dl>
:::
