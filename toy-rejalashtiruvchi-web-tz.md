# TEXNIK TOPSHIRIQ (TZ)
## "Nikoh/To'y Rejalashtiruvchi" — Veb-sayt (Django + DRF) versiyasi

**Versiya:** 1.0
**Sana:** 2026-yil sentyabr
**Asos:** Telegram bot uchun tuzilgan TZ (v1.0, 2026-yil iyun) — veb-platformaga moslashtirilgan
**Tayyorlovchi:** Yodgor (PDP Academy, Python backend yo'nalishi)

---

## 1. LOYIHA HAQIDA UMUMIY MA'LUMOT

### 1.1. Maqsad
Telegram botdagi bilan bir xil g'oyani — to'y tashkil qilish jarayonini (byudjet, mehmonlar, vendorlar, vazifalar) boshqarishni — veb-sayt orqali taqdim etish. Backend **Django REST Framework** asosida API sifatida quriladi, frontend esa Django shablonlari (HTML/JS) orqali shu API bilan ishlaydi.

### 1.2. Muammo (Pain Point)
Telegram botdagi bilan bir xil:
- To'y rejalashtirish Excel, qog'oz daftar va messenjer guruhlarida tarqoq olib boriladi.
- Byudjet nazoratsiz oshib ketadi.
- Mehmonlar va taom hisobida xatoliklar ko'p.
- Ishonchli vendor (restoran, fotograf, dekorator) topish qiyin.

Veb-sayt qo'shimcha ravishda quyidagilarni yechadi:
- Kompyuterda katta ekranda byudjet jadvali va statistikani qulay ko'rish.
- Bir nechta oila a'zosi bir vaqtda turli qurilmadan kirishi (brauzer orqali, Telegram'ga bog'liq bo'lmagan holda).
- Kelajakda tashqi tizimlar (to'lov, PDF eksport) bilan osonroq integratsiya.

### 1.3. Maqsadli auditoriya
Bot bilan bir xil:
- **Asosiy:** kelin-kuyov yoki ularning ota-onalari (to'y tashkilotchisi).
- **Ikkinchi darajali (B2B):** to'yxonalar, fotograf/videograflar, dekoratorlar.

### 1.4. Platforma tanlovi haqida qaror
| | Telegram bot | Veb-sayt (bu TZ) |
|---|---|---|
| Kirish | Telegram orqali avtomatik | Ro'yxatdan o'tish (username/email + parol) |
| Qurilma | Telefon, Telegram ilovasi | Har qanday brauzer |
| Eslatmalar | Push-xabar (bot orqali) | Email yoki saytga kirganda ko'rsatish (1-bosqichda push yo'q) |
| Auth | telegram_id | Django `User` + `Profile` (OneToOne) |

Ikkala platforma bir xil ma'lumotlar bazasi tuzilmasidan (yoki bir xil backend'dan) foydalanishi mumkin — kelajakda ikkalasini bitta backend'ga ulash rejalashtiriladi (bo'lim 6 ga qarang).

---

## 2. FUNKSIONAL TALABLAR

### 2.1. MVP — 1-bosqich

#### 2.1.1. Ro'yxatdan o'tish va profil
- Ro'yxatdan o'tish: username, email, parol (`/api/users/register/`)
- Kirish: token asosida autentifikatsiya (`/api-token-auth/`)
- Profilda: til (uz_latin / uz_cyrillic / ru), to'y sanasi, premium_status
- To'y sanasi kiritilgach — saytda "to'yga N kun qoldi" avtomatik hisoblanadi va bosh sahifada ko'rsatiladi
- Ixtiyoriy: `telegram_id` maydoni saqlanadi (kelajakda bot bilan bog'lash uchun)

#### 2.1.2. Mehmonlar ro'yxati (Guest List)
- Mehmon qo'shish: ism, telefon, taraf (kelin/kuyov), status (taklif qilindi / tasdiqladi / kelmaydi), guruh (oila/do'stlar/hamkasblar)
- Ro'yxatni jadval (HTML table) ko'rinishida ko'rsatish, qidiruv va filtr (status, taraf bo'yicha)
- Umumiy son, tasdiqlangan son — sahifa tepasida statistik kartochka sifatida
- CRUD: qo'shish, tahrirlash, o'chirish (AJAX/fetch orqali, sahifa qayta yuklanmasdan)

#### 2.1.3. Byudjet kalkulyatori
- Kategoriya qo'shish: nomi, rejalashtirilgan summa, sarflangan summa, izoh
- Har kategoriya uchun progress-bar (rejalashtirilgan vs sarflangan)
- Umumiy byudjet, jami sarflangan, qolgan mablag' — dashboard'da ko'rsatiladi
- Frontendda oddiy diagramma (masalan, Chart.js) orqali kategoriyalar taqsimoti

#### 2.1.4. Vazifalar ro'yxati (Checklist/Timeline)
- To'y sanasiga qarab backend avtomatik taklif qiladigan vazifalar ro'yxati (masalan: 6 oy qoldi → to'yxona, 1 oy qoldi → kelinlik)
- Vazifani "bajarildi" deb belgilash (checkbox, AJAX)
- Muddati yaqinlashgan vazifalar sahifa tepasida ogohlantirish sifatida chiqadi (push-xabar o'rniga)

#### 2.1.5. Vendorlar katalogi
- Kategoriya bo'yicha ro'yxat (to'yxona, fotograf, dekorator, kelinlik salon, musiqachilar)
- Har biri uchun: nomi, manzil, narx diapazoni, kontakt, Instagram havolasi
- Boshida faqat Django admin panel orqali to'ldiriladi
- Frontendda filtrlash (kategoriya, narx diapazoni bo'yicha)

### 2.2. Kengaytirilgan funksiyalar — 2-bosqich
- Ko'p foydalanuvchili rejim: bitta to'y hisobiga kelin va kuyov birga ulanishi (masalan, taklif kodi orqali)
- PDF hisobot generatsiyasi (byudjet, mehmonlar, vazifalar) — `reportlab`/`weasyprint`
- Vendor reyting va sharhlar
- To'lov integratsiyasi (Click/Payme) — premium obuna uchun
- Email orqali eslatma yuborish (Django `send_mail` + Celery)

### 2.3. Kelajakdagi g'oyalar — 3-bosqich
- AI asosida shaxsiylashtirilgan to'y rejasi tavsiyasi
- Vendor bilan saytda to'g'ridan-to'g'ri band qilish (booking)
- Komissiya asosidagi marketpleys
- Veb-sayt va Telegram bot'ni bitta umumiy backend'ga ulash (bo'lim 6)

---

## 3. TEXNIK ARXITEKTURA

### 3.1. Texnologiyalar stack
| Qatlam | Texnologiya |
|---|---|
| Backend | Django + Django REST Framework |
| Frontend | Django shablonlari (HTML) + vanilla JS (`fetch`) — 2-bosqichda React ham ko'rib chiqilishi mumkin |
| Auth | DRF Token Authentication (`rest_framework.authtoken`) |
| Hujjatlar | drf-spectacular (Swagger/OpenAPI) |
| Ma'lumotlar bazasi | SQLite (MVP) → PostgreSQL (production) |
| Eslatmalar | Django signal + (2-bosqichda) Celery + Redis |
| To'lov tizimi | Click.uz / Payme API (2-bosqich) |
| Hosting | Railway/Render (boshlash uchun) → VPS (Timeweb, Hetzner) |
| Admin panel | Django Admin (o'zi tayyor) |
| PDF generatsiya | reportlab yoki weasyprint (2-bosqich) |

### 3.2. Django app tuzilmasi
```
config/                  # loyiha sozlamalari
├── settings.py
├── urls.py
templates/
├── base.html
├── register.html, login.html, profile.html
├── guests.html, budget.html, tasks.html, vendors.html
static/
├── js/, css/
users/                   # Profile, auth
guests/                  # mehmonlar CRUD
budget/                  # byudjet kategoriyalari
tasks/                   # vazifalar/timeline
vendors/                 # vendorlar katalogi
reminders/               # (2-bosqich)
```

### 3.3. Ma'lumotlar bazasi tuzilmasi (asosiy jadvallar)
Bot TZ'dagi bilan deyarli bir xil, faqat `users` jadvali o'rniga Django `User` + `Profile`:

```
Profile (users app)
- id, user (FK → django.contrib.auth.User), telegram_id (null),
  til, toy_sanasi, premium_status, created_at

Guest (guests app)
- id, user (FK), ism, telefon, taraf, status, guruh

BudgetItem (budget app)
- id, user (FK), kategoriya, rejalashtirilgan_summa, sarflangan_summa, izoh

Task (tasks app)
- id, user (FK), nomi, muddat, holati

Vendor (vendors app)
- id, kategoriya, nomi, manzil, narx_diapazoni, kontakt, reyting

Reminder (reminders app, 2-bosqich)
- id, user (FK), task (FK), yuborish_vaqti, holati
```

### 3.4. Sayt sahifalari (bot menyusiga mos)
```
/                       → Bosh sahifa / ro'yxatdan o'tish
/login/                 → Kirish
/dashboard/             → To'ygacha qolgan kun, umumiy statistika
/guests/                → Mehmonlar ro'yxati
/budget/                → Byudjet kategoriyalari
/tasks/                 → Vazifalar/timeline
/vendors/               → Vendorlar katalogi (filtr bilan)
/profile/               → Profil sozlamalari, til, premium
/api/...                → DRF API endpoint'lari (barcha CRUD)
/api/docs/              → Swagger (drf-spectacular)
```

---

## 4. NOFUNKSIONAL TALABLAR
- **Tezlik:** har bir sahifa/so'rov javobi < 2 soniya
- **Til:** boshlang'ich versiyada o'zbek tili (lotin) majburiy, rus va kirill — qo'shimcha
- **Maxfiylik:** foydalanuvchi ma'lumotlari (telefon, byudjet) uchinchi tomonlarga berilmaydi; har bir foydalanuvchi faqat o'z ma'lumotlarini ko'radi (`request.user` orqali filtr)
- **Zaxira nusxa:** ma'lumotlar bazasi muntazam backup qilinadi
- **Responsiv dizayn:** sayt telefon brauzerida ham qulay ochilishi kerak (mobil foydalanuvchilar ko'p bo'ladi)

---

## 5. ISHLAB CHIQISH BOSQICHLARI

| Bosqich | Tavsif | Holat |
|---|---|---|
| 1. Loyihalash | DB sxema, app tuzilmasi, sahifa ro'yxati | ✅ Tugallandi (ushbu TZ) |
| 2. Auth (users) | Ro'yxatdan o'tish, kirish, profil, token auth | 🔄 Boshlangan |
| 3. Frontend asosi | base.html, register/login/profile sahifalari | 🔄 Boshlangan |
| 4. Guests moduli | Model, API, sahifa | Navbatda |
| 5. Budget moduli | Model, API, sahifa, progress-bar | Navbatda |
| 6. Tasks moduli | Model, API, avtomatik taklif logikasi | Navbatda |
| 7. Vendors moduli | Model, admin orqali to'ldirish, filtr sahifasi | Navbatda |
| 8. Testlash | Swagger orqali barcha endpoint'larni sinash | Navbatda |
| 9. 2-bosqich | PDF, ko'p foydalanuvchili rejim, to'lov | MVP dan keyin |

---

## 6. BOT VA VEB-SAYT O'RTASIDAGI BOG'LIQLIK (kelajakdagi reja)
Ikkala loyiha (`toy-qachon-tg-bot` va bu veb-sayt) hozircha alohida kod bazasi sifatida rivojlantiriladi. Kelajakda:
- Umumiy backend (shu DRF API) ikkala platforma uchun ham xizmat qilishi mumkin — bot faqat API'ga so'rov yuboradigan client bo'lib qoladi.
- `telegram_id` maydoni aynan shu maqsadda `Profile` modeliga hozirdanoq qo'shib qo'yilgan.

---

## 7. KEYINGI QADAMLAR
1. `users` app'ini to'liq tugatish (register, login, profile — API + HTML)
2. `guests` app'ini shu naqshda (model → serializer → view → url → template) qurish
3. Har bir app tugagach Swagger orqali sinab ko'rish
4. `budget` va `tasks` app'lariga o'tish
5. MVP tugagach — `vendors` katalogini admin orqali to'ldirish
