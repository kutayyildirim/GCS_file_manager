# 📂 GCS File Manager

Google Cloud Storage tabanlı dosya yönetim sistemi.  
Django REST Framework ile geliştirilmiş olup dosya yükleme, indirme (Signed URL), silme, listeleme ve log takibi gibi işlemleri destekler.  
Docker ile container ortamında çalıştırılabilir.

---

## 🚀 Özellikler

- 📤 **Dosya Yükleme** (`upload_file`)
- 📥 **Dosya İndirme / Signed URL Alma** (`download_file_view`)
- 🗑 **Dosya Silme** (`delete_file_view`)
- 📜 **Dosya Listeleme** (`list_files`)
- 📊 **Log Listeleme** (`list_logs`)
- 🐳 **Docker Desteği**
- 🔒 **Güvenli Servis Hesabı ile Yetkilendirme**

---

## 🛠 Kullanılan Teknolojiler

- [Python 3.x](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Google Cloud Storage](https://cloud.google.com/storage)
- [Docker](https://www.docker.com/)
- [docker-compose](https://docs.docker.com/compose/)

---

## 📦 Kurulum

### 1️⃣ Ortam Değişkenleri
Proje kök dizinine `.env` dosyası oluşturun:

```env
SECRET_KEY=django-secret-key
DEBUG=True
ALLOWED_HOSTS=*
GCS_BUCKET_NAME=gcs_file_manager_storage
```

### 2️⃣ Google Cloud Credentials
Google Cloud Console üzerinden bir **Service Account** oluşturun ve `credentials.json` dosyasını indirin.  
Bu dosyayı proje dizinine ekleyin.

Docker ile çalışırken volume olarak mount edilir:
```yaml
volumes:
  - ./credentials.json:/app/credentials.json
```

### 3️⃣ Docker ile Çalıştırma
```bash
docker-compose up --build
```

### 4️⃣ API Endpointleri
| Endpoint | Method | Açıklama |
|----------|--------|----------|
| `/upload/` | POST | Dosya yükleme (`upload_file`) |
| `/files/` | GET | Dosya listeleme (`list_files`) |
| `/logs/` | GET | Log listeleme (`list_logs`) |
| `/files/<file id>/delete/` | DELETE | Dosya silme (`delete_file_view`) |
| `/files/<file id>/download/` | GET | Dosya indirme / Signed URL (`download_file_view`) |

---

## 📂 Proje Yapısı
```
gcs_file_manager/
│── gcs_file_manager/        # Django proje ayarları
│── files/                   # Dosya yönetimi uygulaması
│   ├── models/              # Veritabanı modelleri
│   ├── serializers/         # API veri serileştiricileri
│   ├── services/            # GCS upload ve link servisleri
│   ├── tasks/               # PDF önizleme vb. Celery görevleri
│   ├── views/               # API endpoint view'leri
│── docker-compose.yml
│── Dockerfile
│── credentials.json         # GCS servis hesabı
│── .env                     # Ortam değişkenleri
│── README.md
│── requirements.txt
```

---

## 🛡 Güvenlik Notları
- **credentials.json** ve **.env** dosyaları kesinlikle versiyon kontrolüne eklenmemelidir.
- GCS bucket'ınıza yalnızca gerekli roller atanmalıdır (ör. `Storage Object Admin`).
