# 🔒 SSL Pinning Detector

**SSLPinDetect** is a tool for analyzing Android APKs to detect SSL pinning implementations by scanning for known patterns in decompiled smali code. It helps security researchers and penetration testers identify SSL pinning mechanisms used in mobile applications efficiently.

## 🚀 Features

- **Fast Scanning**: Utilizes multi-threading and memory-mapped file reading for efficient and rapid file scanning.
- **Accurate Detection**: Pre-compiled regex patterns for precise SSL pinning detection, with line number and code preview.
- **Real-time Progress**: Interactive progress bars for both scanning and match counting, ensuring better monitoring.
- **Flexible Output**: Supports verbose mode for detailed logs or minimal output for efficiency.

## ⚙️ Requirements

- **Python** 3.8+
- **Java** (Ensure it's in system PATH)
- **Apktool** (Download and specify the path)

## 🛠 Installation

1. Clone the repository:

```bash
git clone https://github.com/aancw/SSLPinDetect
cd SSLPinDetect
```

2. Install required Python packages:

```bash
pip install -r requirements.txt
```

3. Ensure Java and Apktool are installed and accessible.

## 🚦 Usage

```bash
python sslpindetect.py -f <apk_path> -a <apktool_path> -p <pattern_file> [-v]
```

### Arguments:

- `-f`, `--file` (required): Path to the APK file.
- `-a`, `--apktool` (required): Path to the apktool jar file.
- `-p`, `--pattern` (optional): Path to the JSON file containing SSL pinning patterns (default: `patterns.json`).
- `-v`, `--verbose` (optional): Enable detailed logging.

### 🧪 Examples

✅ **1. Basic Usage** (without verbose mode and custom patterns):

```bash
python sslpindetect.py -f app.apk -a apktool.jar
```

🔍 **2. Enable Verbose Mode** (for detailed output):

```bash
python sslpindetect.py -a apktool_2.11.0.jar -f sample/app-release.apk -v
```

```bash
Processing APK...
APK successfully decompiled.
Scanning Smali Files: 100%|█████████████████████| 100/100 [00:05<00:00, 19.76it/s]
Pattern Matched: 5
Total Patterns Matched: 5
Pattern detected: OkHttp Certificate Pinning
  - smali/com/example/app/MainActivity.smali
	[Line 45]: invoke-static {v0}, Lcom/squareup/okhttp/CertificatePinner;->check(Ljava/lang/String;)V
```

🛠️ **3. Use Custom SSL Pinning Patterns**:

```bash
python sslpindetect.py -f app.apk -a apktool.jar -p custom_patterns.json
```

## 📂 Patterns File (`patterns.json`)

> **Download the latest pattern file:** [smali-sslpin-patterns](https://github.dev/aancw/smali-sslpin-patterns)

Example of patterns.json file
```json
{
    "OkHttp Certificate Pinning": [
        "Lcom/squareup/okhttp/CertificatePinner;",
        "Lokhttp3/CertificatePinner;",
        "setCertificatePinner"
    ],
    "TrustManager Override": [
        "Ljavax/net/ssl/X509TrustManager;",
        "checkServerTrusted"
    ]
}
```

## ✅ License

This project is licensed under the MIT License.

## ✅ Contibute

🚀 Ready to take SSLPinDetect to the next level? Contribute your ideas, improvements, or raise issues to make this tool even more powerful! Let's build something amazing together!


## PoC

![SSL Pinning Detector PoC](poc.gif)

