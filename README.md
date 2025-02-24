# RageMic

**RageMic**, VB-Audio Cable ile çalışan, ses efektlerinizi (gain, distorsiyon, klipleme) anlık olarak uygulayan, modern arayüzlü bir ses işleme uygulamasıdır.  
Bu proje, orijinal versiyona atıfta bulunarak geliştirilmiş, pull request gönderilmiş ve yeni özelliklerle (preset ayarları, global hotkey, ses seviyesi göstergesi, ayarların JSON dosyasıyla saklanması vb.) zenginleştirilmiş bir kopyadır.

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
- **Build Dosyaları:** Benim buildlediğim versiyon, `build/` ve `dist/` klasörlerinde yer almaktadır.

## ORİJİNAL VERSİYON ÜZERİNE GELİŞTİRİLMİŞTİR

Bu proje, [orijinal](https://github.com/goblinhanyikan/RAGEMIC) versiyona atıfta bulunarak geliştirilmiştir.  
- **Pull Request:** Orijinal projeye yönelik gönderdiğim pull request ile ek özellikler, hata düzeltmeleri ve modernizasyon sağlanmıştır.
- **Geliştirilmiş Özellikler:** Yukarıda belirtilen ek özellikler sayesinde, kullanıcı deneyimi ve işlevsellik önemli ölçüde artırılmıştır.

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
  Build ve derleme dosyaları `build/` ve `dist/` klasörlerinde yer almaktadır.  
  Bu klasörler, proje kök dizininde yer alır ve `.gitignore` dosyası ile takip dışı bırakılmıştır.

## SON NOTLAR

RageMic, orijinal projeye göre geliştirilmiş, pull request ile ek özellikler eklenmiş ve tamamen güncellenmiş bir versiyondur.  
Projeye katkıda bulunmak veya geri bildirimde bulunmak isterseniz, lütfen pull request açın ya da issue bildirimi yapın.  
Keyifli kullanımlar!

---

**Uyarı:** Programı kullanırken oluşabilecek herhangi bir sorumluluk tamamen kullanıcıya aittir.