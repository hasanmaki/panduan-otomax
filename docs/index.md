# Selamat Datang di panduan otomax

For full documentation visit [Orisinil Topup Machine](https://www.otomax-software.com/id).

## Pendahuluan

Otomax adalah perangkat lunak manajemen penjualan pulsa dan paket data yang dirancang untuk memudahkan proses transaksi bagi para agen pulsa. Dengan fitur-fitur canggih dan antarmuka yang user-friendly, Otomax membantu agen dalam mengelola penjualan, stok, dan laporan keuangan dengan lebih efisien.

## Tentang Project
Project documentasi ini tidak terhubung langsung dengan Otomax Software atau perusahaan terkait. Informasi yang disajikan di sini bersifat independen dan dibuat untuk tujuan edukasi serta referensi bagi pengguna Otomax. Untuk informasi resmi, silakan kunjungi situs web resmi Otomax Software.

Saat transaksi pulsa, Otomax mengirim request ke provider, lalu menunggu balasan untuk proses **<otomax:parsing>**.

Jika **<otomax:deposit|deposit>** belum mencukupi, transaksi tidak bisa diproses — meskipun saldo provider masih ada.

Reseller bisa melihat **<otomax:komisi_tunda|komisi tertunda>** di halaman laporan.
