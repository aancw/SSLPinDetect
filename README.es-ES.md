

# 🔒 Detector de SSL Pinning

**SSLPinDetect** es una herramienta para analizar APKs de Android y detectar implementaciones de pinning de SSL mediante el escaneo de patrones conocidos en código smali descompilado. Ayuda a investigadores de seguridad y profesionales de pruebas de penetración a identificar eficientemente los mecanismos de pinning de SSL utilizados en aplicaciones móviles.

## 🚀 Características

- **Escaneo rápido**: Utiliza multihilos y lectura de archivos con mapeo de memoria para un escaneo de archivos eficiente y rápido.
- **Detección precisa**: Patrones regex precompilados para una detección precisa de pinning de SSL, con número de línea y vista previa del código.
- **Progreso en tiempo real**: Barras de progreso interactivas tanto para el escaneo como para el conteo de coincidencias, garantizando un mejor monitoreo.
- **Salida flexible**: Soporta modo detallado (verbose) para registros exhaustivos o salida mínima para mayor eficiencia.

## ⚙️ Requisitos

- **Python** 3.8+
- **Java** (Asegúrese de que esté en la PATH del sistema)
- **Apktool** (Descárguelo y especifique la ruta)

## 🛠 Instalación

1. Clona el repositorio:

```bash
git clone https://github.com/aancw/SSLPinDetect
cd SSLPinDetect
```

2. Instala los paquetes de Python requeridos:

```bash
pip install -r requirements.txt
```

3. Asegúrate de que Java y Apktool estén instalados y sean accesibles.

## 🚦 Uso

```bash
python sslpindetect.py -f <apk_path> -a <apktool_path> -p <pattern_file> [-v]
```

### Argumentos:

- `-f`, `--file` (obligatorio): Ruta al archivo APK.
- `-a`, `--apktool` (obligatorio): Ruta al archivo jar de apktool.
- `-p`, `--pattern` (opcional): Ruta al archivo JSON que contiene los patrones de pinning de SSL (predeterminado: `patterns.json`).
- `-v`, `--verbose` (opcional): Habilita registros detallados.

### 🧪 Ejemplos

✅ **1. Uso básico** (sin modo detallado ni patrones personalizados):

```bash
python sslpindetect.py -f app.apk -a apktool.jar
```

🔍 **2. Habilitar modo detallado** (para salida exhaustiva):

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

🛠️ **3. Usar patrones personalizados de SSL Pinning**:

```bash
python sslpindetect.py -f app.apk -a apktool.jar -p custom_patterns.json
```

## 📂 Archivo de patrones (`patterns.json`)

> **Descargar el archivo de patrones más reciente:** [smali-sslpin-patterns](https://github.dev/aancw/smali-sslpin-patterns)

Ejemplo del archivo patterns.json
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

## ✅ Licencia

Este proyecto está licenciado bajo la Licencia MIT.

## ✅ Contribuir

🚀 ¿Listo para llevar SSLPinDetect al siguiente nivel? Contribuye con tus ideas, mejoras o reporta problemas para hacer esta herramienta aún más poderosa. ¡Construyamos algo increíble juntos!


## PoC

![SSL Pinning Detector PoC](poc.gif)
