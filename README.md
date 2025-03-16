
<div align="center">

# RAGEMIC <br> 🎤🎙️


<img alt="RageMic Logo" src="https://img.shields.io/badge/RageMic-gerçek zamanlı ses efektleri uygulaması-red">
<img alt="Python" src="https://img.shields.io/badge/python-3.6+-blue">
<img alt="License" src="https://img.shields.io/badge/license-MIT-green">

</div>

RageMic, gerçek zamanlı ses efektleri uygulaması olup, mikrofonunuza gain (ses seviyesi), distorsiyon (bozulma) ve klipleme (ses kesimi) gibi efektler ekleyerek sesinizi “öfke” moduna dönüştürmenizi sağlar.Bu uygulama, [VB AUDIO CABLE](https://vb-audio.com/Cable/index.htm) ile entegre çalışarak, başka uygulamalarda (Discord vb.) “CABLE OUTPUT” üzerinden dönüştürülmüş sesi duyurmanıza imkân tanır.


## ÇALIŞTIRMA ADIMLARI

1. **VB AUDIO CABLE İNDİRİN:**
   - Bu programı kullanmak için [VB AUDIO CABLE](https://vb-audio.com/Cable/index.htm) indirmeniz gerekmektedir.
   - **Önemli:** VB Audio Cable olmadan bu program çalışmaz. (Bana gelip mesaj atarsanız, kafanıza *hidrojen* atarım!)

2. **Programı ÇALIŞTIRMAK İÇİN:**
   - "Mikrofonunuzu Seçin" kısmından kullandığınız mikrofonu seçin.
   - "Çıkış" kısmında **"CABLE INPUT (VB-Audio)"** yazan bileşeni seçin.
   - Programı başlatmak için **F6** tuşuna veya "Efektleri aç/kapa" düğmesine basın. (Sayfaya götürmüyor, merak etmeyin!)
   - Rage modunu kapatmak için tekrar F6'ye basabilirsiniz.
   - Kullandığınız diğer programlarda (Discord, vs.) mikrofon olarak **"CABLE OUTPUT (VB-AUDIO CABLE)"** seçin. **BU ADIMI YAPMAZSANIZ, RAGE OLARAK DUYULAMAZSINIZ!**
   - Program açık kaldığı sürece bu mikrofon çıkışı normal mikrofon olarak çalışır; programı kapatırsanız CABLE OUTPUT'tan ses alamazsınız.

3. **ÖNEMLİ UYARI:**
   - BU PROGRAMI İNDİRİNCE BİLGİSAYARINA BİR ŞEYLER OLURSA SORUMLULUK TAMAMEN SENİNDİR. KULLANMAK İSTEMİYORSAN, SİL GİTSİN!

## NEDEN BU VERSİYON?

Bu versiyon, orijinal projeye göre birçok iyileştirme ve ek özellik sunmaktadır:
- **Modern UI:** ttkbootstrap kullanılarak modern, şık bir arayüz.
- **Preset Ayarları:** Ses efektleri için farklı ön ayarlar eklenmiştir.
- **Global Hotkey Desteği:** F12 tuşuyla kolayca efektleri açıp kapatabilirsiniz.
- **Ses Seviyesi Göstergesi:** Gerçek zamanlı olarak ses seviyesini görsel olarak takip edebilirsiniz.
- **Ayarların Kalıcı Kaydı:** Hem preset ayarları hem de ses aygıtı seçimleri, JSON dosyaları ile aynı klasörde saklanır. Böylece program yeniden açıldığında önceki ayarlar otomatik olarak yüklenir.

## ORİJİNAL VERSİYON ÜZERİNE GELİŞTİRİLMİŞTİR

Bu proje, [orijinal](https://github.com/goblinhanyikan/RAGEMIC) versiyona atıfta bulunarak geliştirilmiştir.  
- **Pull Request:** Orijinal projeye yönelik gönderdiğim pull request ile ek özellikler, hata düzeltmeleri ve modernizasyon sağlanmıştır.
- **Geliştirilmiş Özellikler:** Ek özellikler (modern arayüz, preset desteği, JSON kayıt, vb.) ve hata düzeltmeleri ile kullanıcı deneyimi iyileştirilmiştir.

## YÜKLEME VE ÇALIŞTIRMA

1. **Gerekli Paketler:**
   - [Python 3.x](https://www.python.org/downloads/)
   - [pyaudio](https://pypi.org/project/PyAudio/)
   - [numpy](https://pypi.org/project/numpy/)
   - [ttkbootstrap](https://pypi.org/project/ttkbootstrap/)
   - [keyboard](https://pypi.org/project/keyboard/)

   Tüm paketleri kurmak için:
   ```bash
   pip install pyaudio numpy ttkbootstrap keyboard
   ```

2. **Programı Başlatın:**
   ```bash
   python rage.py
   ```

## BUILD DOSYALARI

- **Build Dosyaları:**  
  - Bu proje herhangi bir resmî lisansa tabii olabilir veya        olmayabilir (orijinal repoya bakınız).
  - VB-Audio Cable gibi üçüncü taraf yazılımlarla ilgili sorunlar için ilgili yazılımın geliştiricilerine başvurunuz.

## OLASI HATALAR VE ÇÖZÜMLERİ
- **Projeye Güven duygusu**  
   - projeye veya benim geliştirdiğim build'e güvenmiyorsanız siz rage.py üzerinden kendinizde buildleyebilirisiniz. bu işlevleri requirements.txt'de bulunan tüm kütüphaneleri indirip daha sonrasında ise 
   ```bash
   pyinstaller --onefile --hidden-import=ttkbootstrap.constants --hidden-import=keyboard --hidden-import=pyaudio rage.py
   ```
   yapmanız yeterli olacaktır.

- **locale.Error: unsupported locale setting**
  - bu sorun 1.0.2 ile çözüldü ancak yinede bazen olabiliyor.
  - Bazı sistemlerde, locale ayarları desteklenmeyebilir.
  - dialogs.py içindeki locale.setlocale satırını try/except ile yakalayın veya 
  ```py
     os.environ["LC_ALL"] = "C"
  ``` 
  - şeklinde ayarlayın.
  - dialogs.py ttkinter'in içinde lib'lerde
- **pyaudio Kurulumu Sırasında Hata:**
  - Windows’ta Visual C++ Build Tools eksikse pip install pyaudio hata verebilir.
  - [Resmi Microsoft Build Tools](https://visualstudio.microsoft.com/downloads/) veya önceden derlenmiş “whl” dosyası yükleyin.
- **Device not found Hatası:**
  - Mikrofon veya sanal cihaz “CABLE INPUT” / “CABLE OUTPUT” algılanmadıysa.
  - Ses aygıtlarını kontrol edin, yeniden takın veya VB-Audio Cable’ın kurulu olduğundan emin olun. Ve tekrar deneyin.

## İLETİŞİM
- Orjinal geliştirici: [RAGEMIC](https://github.com/goblinhanyikan/RAGEMIC)
- Orjinal Sürüm sahibi:[Goblinhanyikan](https://github.com/goblinhanyikan/RAGEMIC)
- Proje Sahibi: [Bay Eggex](https://github.com/bayeggex)
- Geliştirilmiş Sürüm: [Bu repo](https://github.com/bayeggex/RAGEMIC)
- Soru ve öneriler için GitHub Issues üzerinden iletişime geçebilirsiniz.

---

**Keyifli Kulanımlar!:** Bu rehberi izleyerek RageMic’i sorunsuz şekilde kurabilir, kendi öfkeli ses efektlerinizi anında deneyimleyebilirsiniz.