<div align="center">

# RAGEMIC 🎤🎙️
### Gerçek Zamanlı Ses Efektleri Uygulaması (macOS Uyumlu Sürüm)

<img alt="RageMic Logo" src="https://img.shields.io/badge/RageMic-Ses%20Efektleri-red">
<img alt="Python" src="https://img.shields.io/badge/Python-3.7+-blue">
<img alt="Platform" src="https://img.shields.io/badge/Platform-macOS%20%7C%20Windows*-yellow">
</div>

RageMic, mikrofonunuza gerçek zamanlı olarak gain (ses seviyesi), distorsiyon (bozulma) ve klipleme (ses kesimi) gibi efektler ekleyerek sesinizi "öfke" moduna veya farklı tınılara dönüştürmenizi sağlayan bir uygulamadır. Bu sürüm, özellikle macOS kullanıcıları için uyarlanmıştır ve [BlackHole](https://github.com/ExistentialAudio/BlackHole) gibi sanal ses aygıtlarıyla entegre çalışarak efektli sesi Discord, OBS gibi diğer uygulamalara yönlendirmenize olanak tanır.

## ✨ Temel Özellikler

* **Modern Arayüz:** `ttkbootstrap` ile geliştirilmiş kullanıcı dostu ve şık bir tema.
* **Preset Yönetimi:** Farklı ses efektleri için hazır profiller ve kendi presetlerinizi oluşturup kaydetme imkanı.
* **Gerçek Zamanlı Efektler:** Gain, distorsiyon ve klip seviyelerini anında ayarlayın.
* **Pencere Odaklı Kısayol:** macOS için **⌘⇧R** (Command+Shift+R) kısayolu ile uygulama penceresi odaktayken efektleri kolayca açıp kapatın.
* **Ses Seviyesi Göstergesi:** Mikrofonunuzdan gelen sesin seviyesini gerçek zamanlı olarak izleyin.
* **Kalıcı Ayarlar:** Seçtiğiniz ses aygıtları ve son kullandığınız preset, programın çalıştığı klasördeki JSON dosyalarına kaydedilir ve uygulama yeniden başlatıldığında otomatik olarak yüklenir.
* **macOS Uyumluluğu:** Bu sürüm, macOS üzerinde sorunsuz çalışması için özel olarak gözden geçirilmiş ve ayarlanmıştır.

## 🚀 Başlarken (macOS için)

### Ön Koşullar
1.  **Python:** Python 3.7 veya daha yeni bir sürüm. ([python.org](https://www.python.org/downloads/))
2.  **PortAudio:** `pyaudio` kütüphanesinin çalışabilmesi için gereklidir. [Homebrew](https://brew.sh/index_tr) paket yöneticisi ile kurun:
    ```bash
    brew install portaudio
    ```
3.  **Sanal Ses Aygıtı (Şiddetle Tavsiye Edilir):** Efektli sesi diğer uygulamalara (Discord, OBS vb.) yönlendirmek için [BlackHole (2ch versiyonu genellikle yeterlidir)](https://github.com/ExistentialAudio/BlackHole) gibi bir sanal ses aygıtı kurun.

### Kurulum
1.  Bu repoyu klonlayın veya ZIP olarak indirin:
    ```bash
    git clone [https://github.com/](https://github.com/)[senin-github-kullanıcıadın]/[repo-adın].git
    cd [repo-adın]
    ```
    (Eğer ZIP olarak indirdiyseniz, dosyaları bir klasöre çıkarın ve o klasöre gidin.)

2.  Gerekli Python kütüphanelerini `requirements.txt` dosyasını kullanarak kurun:
    *(Projenizin ana dizininde aşağıdaki içeriğe sahip bir `requirements.txt` dosyası olduğundan emin olun):*
    ```text
    numpy
    pyaudio
    ttkbootstrap
    ```
    Kurulum komutu:
    ```bash
    pip3 install -r requirements.txt
    ```
    Veya kütüphaneleri tek tek kurun:
    ```bash
    pip3 install numpy pyaudio ttkbootstrap
    ```

### Programı Çalıştırma (Kaynak Kodundan)
Proje klasöründeyken terminalde aşağıdaki komutu çalıştırın:
```bash
python3 rage.py
