<div align="center">
  <img src="assets/skulltrace.svg" alt="SKULLTRACE grinning skull and serpent emblem" width="190" />

  <h1>SKULLTRACE</h1>
  <p><strong>Trace the signal. Respect the boundaries.</strong></p>
  <p>A modular Python OSINT and local-analysis workbench with a grinning skull, serpent-inspired terminal UI, and privacy-conscious design.</p>

  <p>
    <img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" />
    <img alt="MIT License" src="https://img.shields.io/badge/License-MIT-14B8A6.svg" />
    <img alt="No runtime dependencies" src="https://img.shields.io/badge/Runtime%20dependencies-None-64748B.svg" />
    <a href="https://github.com/raxwqx/SKULLTRACE/actions/workflows/tests.yml"><img alt="Tests" src="https://github.com/raxwqx/SKULLTRACE/actions/workflows/tests.yml/badge.svg?branch=main" /></a>
  </p>

  <p>
    <a href="#-features">Features</a> •
    <a href="#-installation">Installation</a> •
    <a href="#-usage">Usage</a> •
    <a href="#-privacy--safe-use">Privacy &amp; safety</a> •
    <a href="#-tests">Tests</a> •
    <a href="#turkce">Türkçe</a>
  </p>
</div>

---

## 🐍 What is SKULLTRACE?

**SKULLTRACE** is an original, modular Python project for learning about Open Source Intelligence (OSINT), inspecting public network metadata, and analyzing local files. It combines a colorful terminal interface with small command-line modules that can be tested independently.

The project is inspired by the general idea of an OSINT workbench. Its code, name, visual identity, and implementation are its own.

> [!NOTE]
> SKULLTRACE is an educational and low-impact analysis toolkit. It is not a people-tracking tool, and it does not try to break into accounts, bypass access controls, or secretly collect private information.

## ✨ Features

| Module | What it does | Network activity |
| --- | --- | --- |
| 🧭 **DNS Intelligence** | Resolves a hostname to A/AAAA addresses using the configured system resolver. | Sends a DNS query through your configured resolver. |
| 🌐 **IP Inspector** | Classifies an IPv4 or IPv6 address, including private, global, loopback and reserved ranges. | None; local analysis. |
| 🔎 **URL Risk Hints** | Parses URL structure and flags basic warning signs without opening the link. Sensitive URL components are excluded from the report target. | None; does not fetch pages or follow redirects. |
| ✉️ **Email Syntax** | Checks basic email-address formatting. | None; does not contact a mail server or verify mailbox ownership. |
| 🏷️ **Domain Validator** | Normalizes and checks hostname/domain syntax, including internationalized names. | None; offline validation. |
| #️⃣ **File Fingerprint** | Computes SHA-256, SHA-1 and MD5 hashes for a local file. | None; reads the file locally without modifying or uploading it. MD5 is for legacy comparison only. |
| ✅ **Checksum Verification** | Compares a local file's SHA-256 with a reference digest you supply, using a constant-time comparison. | None; reads the file locally and never uploads it. |
| 🖥️ **Local Info** | Displays local hostname, operating system, architecture, Python version and resolver-provided local addresses. | May ask the system resolver about the local hostname. |
| 🗒️ **Case Notes** | Turns a researcher-written observation into a structured report. | None. |
| 📄 **JSON Reports** | Prints JSON or saves a result atomically to a path you choose. | File output is local. |
| 💀 **Interactive terminal** | Opens a snake-framed, grinning-skull ASCII splash and numbered menu. | Depends on the selected module. |

A result is an **informational hint**, not proof that a domain, URL, address or file is malicious or safe. A matching checksum confirms only that the file matches the reference you supplied; it does not prove that the reference itself is trustworthy.

## 🧰 Requirements

- Kali Linux or another Linux distribution; macOS and Windows are also tested.
- Python **3.10 or newer**.
- Git for the clone-based installation.
- No third-party **runtime** dependencies.

Check your Python version:

```bash
python3 --version
```

## 🚀 Installation

### Option A: Clone with Git (recommended)

Open a terminal and run:

```bash
# 1. Create a place for projects
mkdir -p ~/projeler
cd ~/projeler

# 2. Download the repository
git clone https://github.com/raxwqx/SKULLTRACE.git SKULLTRACE
cd SKULLTRACE

# 3. Create and activate an isolated Python environment
python3 -m venv .venv
source .venv/bin/activate

# 4. Install SKULLTRACE in editable mode
python -m pip install -e .
```

### Option B: Download the ZIP

1. Open the [SKULLTRACE repository](https://github.com/raxwqx/SKULLTRACE).
2. Click **Code → Download ZIP**.
3. Extract the archive and open the extracted project folder in a terminal.
4. From the folder containing `pyproject.toml`, run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

> [!TIP]
> If you do not want to install the package yet, launch it directly from the repository root with `PYTHONPATH=src python3 -m skulltrace`.

## 🎮 Usage

### Launch the interactive terminal

After installation:

```bash
skulltrace
```

Or, from the repository root without installing:

```bash
PYTHONPATH=src python3 -m skulltrace
```

Choose a numbered option from the menu. Enter `0`, `q`, or `quit` to exit. Option **9** verifies a file against a SHA-256 digest; option **10** shows scope and safety notes.

### Command-line examples

The commands below use documentation-safe sample values. Replace them with your own authorized research targets.

```bash
# DNS: resolve a public hostname
skulltrace dns example.com

# Inspect an IP locally
skulltrace ip 8.8.8.8

# Inspect URL syntax only; the page is not visited
skulltrace url 'https://example.com/login?campaign=test'

# Check basic email syntax only
skulltrace email researcher@example.com

# Validate a domain/hostname offline
skulltrace domain example.com

# Hash a file on your own machine
skulltrace hash ./sample.bin

# Verify a local file against a trusted SHA-256 reference
skulltrace verify ./sample.bin --sha256 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef

# Show local system/runtime metadata
skulltrace local-info

# Create a structured observation note
skulltrace case-note lab-01 'Observed the expected test result'

# Display project scope and safety notes
skulltrace about

# Show version and command help
skulltrace --version
skulltrace --help
```

### ✅ Verify a SHA-256 checksum

Use `verify` when a download page, vendor, or evidence record gives you a SHA-256 digest:

```bash
skulltrace verify ./download.bin --sha256 <64_HEX_DIGITS>
```

The command:

- Reads the file locally in fixed-size chunks.
- Accepts uppercase hexadecimal digits and an optional `sha256:` prefix.
- Rejects malformed reference digests instead of silently comparing them.
- Returns status `ok` and exit code `0` when the digest matches.
- Returns status `mismatch` and exit code `1` when the digest does not match.
- Never modifies, executes, or uploads the file.

A match means the file matches the reference **you chose to trust**. Confirm that the reference came from an independent, authentic source before relying on the result.

### 📦 Export JSON reports

Append `--json` to print machine-readable JSON. Use `--output PATH` to save the report to a file. Reports are written atomically, so an interrupted write cannot truncate an existing report.

```bash
# Print JSON to the terminal
skulltrace ip 8.8.8.8 --json

# Create the output folder first if it does not exist
mkdir -p reports

# Save a DNS report
skulltrace dns example.com --output reports/dns-report.json

# Save a URL syntax report and print JSON
skulltrace url 'https://example.com' --json --output reports/url-report.json

# Save a checksum verification report
skulltrace verify ./sample.bin --sha256 <64_HEX_DIGITS> --output reports/verify.json
```

For commands that perform analysis, a non-zero exit status can indicate that the input could not be analyzed successfully or that a verification did not match. Check the printed report and error message.

## 🗂️ Project structure

```text
SKULLTRACE/
├── assets/
│   └── skulltrace.svg         # Original snake + grinning skull emblem
├── docs/
│   ├── methodology.md         # Analysis approach and limitations
│   └── scenarios/
│       └── TEMPLATE.md        # Research scenario template
├── src/skulltrace/
│   ├── core/                  # Shared configuration and JSON reports
│   ├── modules/               # Independent analysis modules
│   ├── ui/                    # ASCII splash and terminal output
│   ├── cli.py                 # CLI commands and interactive menu
│   └── __main__.py            # python -m skulltrace entry point
├── tests/                     # Offline unit tests
├── .github/workflows/         # Automated test workflow
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml
├── README.md
└── SECURITY.md
```

## 🧪 Tests

Run these commands from the repository root:

```bash
PYTHONPATH=src python3 -m compileall -q src tests
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

The test suite is designed to run offline and mocks DNS-related behavior where appropriate. GitHub Actions runs the workflow on Ubuntu, Windows and macOS for Python 3.10 through 3.13.

## 🔐 Privacy & safe use

- Use SKULLTRACE only for lawful learning, systems you own, or targets for which you have explicit authorization.
- DNS lookups use your machine's configured resolver and may be visible to that resolver.
- URL inspection is static: the program does **not** visit the URL, fetch the page or follow redirects. Control characters are rejected so untrusted input cannot inject terminal escape sequences.
- IP classification, domain syntax checks and email syntax checks run locally.
- File hashing and SHA-256 verification read local file contents but do not modify or upload them.
- A checksum match is only as trustworthy as the reference digest. Verify the reference through an independent channel.
- Avoid putting passwords, tokens, private personal data or other secrets into case notes and reports.
- Review JSON reports before sharing them; they may include values you entered.
- Do not treat an automated flag as a definitive security verdict.

Read [SECURITY.md](SECURITY.md) for reporting security concerns and [docs/methodology.md](docs/methodology.md) for the project's analysis principles.

## 🧭 Roadmap

Potential future improvements include richer offline report formatting, signed checksum manifests, more unit tests for edge cases, and additional passive data sources with clear privacy boundaries. Features will be added only when their behavior can be documented and tested.

## 🤝 Contributing

Issues, bug reports, documentation improvements and pull requests are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before contributing. Keep changes modular, testable and respectful of user privacy.

## 📜 License

SKULLTRACE is released under the **MIT License**. See [LICENSE](LICENSE).

---

<a id="turkce"></a>

## 🇹🇷 Türkçe

**SKULLTRACE**, açık kaynak istihbaratı (OSINT) öğrenmek, herkese açık ağ üst verilerini incelemek ve yerel dosyaları analiz etmek için geliştirilmiş modüler bir Python çalışma tezgâhıdır. Renkli bir terminal arayüzünü, bağımsız olarak test edilebilen küçük komut satırı modülleriyle birleştirir.

> [!NOTE]
> SKULLTRACE eğitim ve düşük etkili analiz amaçlıdır. Kişi takip aracı değildir; hesaplara girmeye, erişim kontrollerini atlatmaya veya özel bilgileri gizlice toplamaya çalışmaz.

### Özellikler

| Modül | Ne yapar | Ağ etkinliği |
| --- | --- | --- |
| 🧭 **DNS İstihbaratı** | Bir ana bilgisayar adını sistem çözümleyicisiyle A/AAAA adreslerine çözer. | Yapılandırılmış çözümleyiciye DNS sorgusu gönderir. |
| 🌐 **IP Denetçisi** | IPv4/IPv6 adresini özel, genel, döngüsel ve ayrılmış aralıklara göre sınıflandırır. | Yok; yerel analiz. |
| 🔎 **URL Risk İpuçları** | Bağlantıyı açmadan URL yapısını inceler ve temel uyarı işaretlerini gösterir. | Yok; sayfa getirmez, yönlendirme izlemez. |
| ✉️ **E-posta Sözdizimi** | E-posta adresinin temel biçimini denetler. | Yok; posta sunucusuna bağlanmaz, kutu sahipliğini doğrulamaz. |
| 🏷️ **Alan Adı Doğrulama** | Ana bilgisayar/alan adı sözdizimini ve uluslararası adları normalize eder. | Yok; çevrimdışı doğrulama. |
| #️⃣ **Dosya Parmak İzi** | Yerel bir dosya için SHA-256, SHA-1 ve MD5 hesaplar. | Yok; dosyayı yerelde okur, değiştirmez veya yüklemez. MD5 yalnızca eski uyumluluk içindir. |
| ✅ **Sağlama Doğrulama** | Yerel dosyanın SHA-256 değerini verdiğiniz referansla sabit zamanlı karşılaştırır. | Yok; dosyayı yerelde okur, asla yüklemez. |
| 🖥️ **Yerel Bilgi** | Ana bilgisayar adı, işletim sistemi, mimari, Python sürümü ve yerel adresleri gösterir. | Yerel ana bilgisayar adı için çözümleyiciye sorabilir. |
| 🗒️ **Vaka Notları** | Araştırmacının yazdığı gözlemi yapılandırılmış rapora dönüştürür. | Yok. |
| 📄 **JSON Raporları** | JSON yazdırır veya seçtiğiniz yola atomik olarak kaydeder. | Dosya çıktısı yereldir. |
| 💀 **Etkileşimli terminal** | Yılan çerçeveli, sırıtan kurukafa ASCII açılışı ve numaralı menü sunar. | Seçilen modüle bağlıdır. |

Sonuçlar **bilgilendirici ipuçlarıdır**; bir alan adının, URL'nin, adresin veya dosyanın kötü ya da güvenli olduğunu kanıtlamaz. Eşleşen bir sağlama yalnızca dosyanın sizin verdiğiniz referansla uyumlu olduğunu gösterir; referansın kendisinin güvenilir olduğunu kanıtlamaz.

### Gereksinimler

- Kali Linux veya başka bir Linux dağıtımı; macOS ve Windows da test edilir.
- Python **3.10 veya üzeri**.
- Klonlayarak kurulum için Git.
- Üçüncü taraf **çalışma zamanı** bağımlılığı yoktur.

```bash
python3 --version
```

### Kurulum

```bash
mkdir -p ~/projeler
cd ~/projeler
git clone https://github.com/raxwqx/SKULLTRACE.git SKULLTRACE
cd SKULLTRACE
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Kurulum yapmadan denemek için depo kökünden:

```bash
PYTHONPATH=src python3 -m skulltrace
```

### Kullanım

```bash
# DNS: genel bir ana bilgisayar adını çöz
skulltrace dns example.com

# IP adresini yerelde incele
skulltrace ip 8.8.8.8

# Yalnızca URL sözdizimini incele; sayfa açılmaz
skulltrace url 'https://example.com/login?campaign=test'

# Yalnızca temel e-posta sözdizimini denetle
skulltrace email researcher@example.com

# Alan adını çevrimdışı doğrula
skulltrace domain example.com

# Yerel dosyanın özetlerini hesapla
skulltrace hash ./sample.bin

# Yerel dosyayı güvenilir bir SHA-256 referansıyla doğrula
skulltrace verify ./sample.bin --sha256 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef

# Yerel sistem çalışma zamanı bilgilerini göster
skulltrace local-info

# Yapılandırılmış gözlem notu oluştur
skulltrace case-note lab-01 'Beklenen test sonucu gözlemlendi'

# Proje kapsamını ve güvenlik notlarını göster
skulltrace about
```

Etkileşimli menüde **9** numaralı seçenek SHA-256 doğrulaması yapar, **10** numaralı seçenek kapsam ve güvenlik notlarını gösterir. Çıkmak için `0`, `q` veya `quit` yazın.

### SHA-256 sağlama doğrulama

Bir indirme sayfası, üretici veya delil kaydı size SHA-256 özeti verdiyse:

```bash
skulltrace verify ./indirilen-dosya.bin --sha256 <64_HEX_BASAMAK>
```

- Dosyayı yerelde sabit boyutlu parçalar halinde okur.
- Büyük harfli onaltılık basamakları ve isteğe bağlı `sha256:` önekini kabul eder.
- Hatalı referans özetlerini sessizce karşılaştırmak yerine reddeder.
- Özet eşleşirse `ok` durumu ve `0` çıkış kodu verir.
- Özet eşleşmezse `mismatch` durumu ve `1` çıkış kodu verir.
- Dosyayı değiştirmez, çalıştırmaz veya yüklemez.

Eşleşme, dosyanın **güvenmeyi seçtiğiniz** referansla uyumlu olduğu anlamına gelir. Sonuca güvenmeden önce referansın bağımsız ve gerçek bir kaynaktan geldiğini doğrulayın.

### JSON raporları

`--json` ile makine tarafından okunabilir JSON yazdırılır. `--output YOL` ile rapor dosyaya kaydedilir. Raporlar atomik yazılır; kesilen bir yazma işlemi mevcut raporu bozamaz.

```bash
skulltrace ip 8.8.8.8 --json
skulltrace dns example.com --output reports/dns-report.json
skulltrace verify ./sample.bin --sha256 <64_HEX_BASAMAK> --output reports/verify.json
```

Analiz komutlarında sıfır dışı çıkış kodu, girdinin başarıyla analiz edilemediğini veya doğrulamanın eşleşmediğini gösterebilir. Yazdırılan raporu ve hata mesajını kontrol edin.

### Testler

Depo kökünden:

```bash
PYTHONPATH=src python3 -m compileall -q src tests
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Test paketi çevrimdışı çalışacak şekilde tasarlanmıştır ve DNS davranışını uygun yerlerde taklit eder. GitHub Actions; Ubuntu, Windows ve macOS üzerinde Python 3.10-3.13 sürümleriyle testleri çalıştırır.

### Gizlilik ve güvenli kullanım

- SKULLTRACE'i yalnızca yasal öğrenme, sahip olduğunuz sistemler veya açık yetkiniz olan hedefler için kullanın.
- DNS sorguları makinenizin yapılandırılmış çözümleyicisini kullanır ve bu çözümleyici tarafından görülebilir.
- URL incelemesi statiktir: program URL'yi ziyaret etmez, sayfayı getirmez veya yönlendirmeleri izlemez. Terminal kontrol karakterleri reddedilir.
- IP sınıflandırması, alan adı ve e-posta sözdizimi denetimleri yerelde çalışır.
- Dosya özeti ve SHA-256 doğrulaması yerel dosyayı okur; değiştirmez veya yüklemez.
- Sağlama eşleşmesi yalnızca referans özeti kadar güvenilirdir. Referansı bağımsız bir kanaldan doğrulayın.
- Vaka notlarına ve raporlara parola, belirteç, özel kişisel veri veya sır koymayın.
- JSON raporlarını paylaşmadan önce inceleyin; girdiğiniz değerleri içerebilirler.
- Otomatik bir uyarıyı kesin güvenlik kararı olarak değerlendirmeyin.

Güvenlik bildirimleri için [SECURITY.md](SECURITY.md), analiz ilkeleri için [docs/methodology.md](docs/methodology.md) dosyalarına bakın.

### Katkı ve lisans

Hata bildirimleri, belge iyileştirmeleri ve pull request'ler memnuniyetle karşılanır. Katkıda bulunmadan önce [CONTRIBUTING.md](CONTRIBUTING.md) dosyasını okuyun. SKULLTRACE **MIT Lisansı** ile yayımlanır; ayrıntılar için [LICENSE](LICENSE) dosyasına bakın.

---

<div align="center">
  <p><strong>SKULLTRACE</strong> · Trace responsibly. 🐍</p>
  <sub>Built for learning, transparent analysis, and authorized research.</sub>
</div>
