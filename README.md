# 🛍️ Django E-commerce

Un progetto e-commerce completo sviluppato con **Django**, che include gestione utenti, carrello, ordini e un'area di amministrazione dedicata ai **manager**.  
Il sito è **deployato su Render** ed è dotato di **Cloudinary** per la gestione delle immagini.

---

## 👥 Accesso demo

**Manager access credentials:**

```
username: professore  
password: ecommerce2025
```
**Admin access credentials:**
```
username: admin  
password: admin

django admin url: website-domain/admin
```
---

## 📌 Obiettivi richiesti rispettati ✅

Queste sono le richieste tecniche imposte per il progetto, tutte soddisfatte:

| Requisito | Implementazione                                                        |
|----------|------------------------------------------------------------------------|
| ✅ Almeno **2 app Django** | `store`, `order`, `accounts`, `cart`,`management`                      |
| ✅ Almeno **2 relazioni tra modelli** | `Product → Category`, `Order → User`, `OrderItem → Product`,`...`      |
| ✅ Almeno **1 CBV (Class-Based View)** | `HomeView` (store/views.py),`ManagerProductView` (management/views.py) |
| ✅ Almeno **2 permessi per gruppi diversi** | Customer e Manager                                                     |
| ✅ Classe `User` **estesa e personalizzata** | `CustomUser` (in `accounts.models`)                                    |

---

## 🧑‍💻 Funzionalità principali

### 👤 Per i **Clienti**
- Navigazione prodotti per categoria o nome
- Filtri per prezzo minimo/massimo
- Visualizzazione dettagli prodotto
- Aggiunta prodotti al carrello
- Checkout con indirizzo e pagamento (demo)
- Cronologia ordini
- Gestione profilo e indirizzi

---

### 🛠️ Per i **Manager**
- Accesso riservato a `/management/`
- Gestione prodotti: crea, modifica, elimina, filtra per categoria o stato (attivo/inattivo)
- Gestione categorie: crea, rinomina, elimina
- Gestione utenti: cambio ruolo da customer a manager
- Gestione ordini: filtro per utente, prodotto, città, stato spedizione
- Modifica stato degli ordini (`In transit`, `Delivered`, ecc.)

> Tutte le funzionalità manageriali sono protette da permessi e visibili solo a chi ha ruolo "Manager".

---

## 🛒 Caratteristiche tecniche

- **Autenticazione completa** (login, logout)
- **Sessione checkout protetta**: ogni step (indirizzo, carta, conferma) richiede quello precedente
- **Carrello persistente** per utente loggato
- **UI responsiva con Bootstrap 5**

---

## ☁️ Gestione media: Cloudinary

Tutte le immagini dei prodotti vengono caricate su **Cloudinary**, evitando la perdita di file nei deploy su Render.

---

## 🚀 Deploy

Il progetto è attualmente deployato su [Render](https://render.com/).  
(NB: inserire link reale al progetto se disponibile)

---

## 🛠️ Setup locale

Segui questi passaggi per eseguire il progetto in locale:

```bash
# 1. Clona il progetto
git clone https://github.com/tuo-utente/tuo-repo.git
cd tuo-repo

# 2. Crea e attiva un ambiente virtuale con conda
conda create -n ecommerce-env python=3.11
conda activate ecommerce-env

# 3. Installa le dipendenze
pip install -r requirements.txt

# 4. Crea un file .env e aggiungi le variabili:
DEBUG=True
CLOUDINARY_CLOUD_NAME=tuo_cloud_name
CLOUDINARY_API_KEY=la_tua_api_key
CLOUDINARY_API_SECRET=la_tua_api_secret

# 5. Applica le migrazioni e avvia il server
python manage.py migrate
python manage.py runserver
```

---

## 📂 Struttura delle app principali

| App | Descrizione |
|-----|-------------|
| `store` | Modelli e visualizzazione prodotti e categorie |
| `accounts` | Login, utenti, gestione indirizzi e permessi |
| `cart` | Logica del carrello |
| `order` | Checkout, ordini, pagamento e storico ordini |
| `management` | Funzionalità di controllo per i manager |

---

## 📄 Licenza

Progetto sviluppato come elaborato per l'esame di "Progettazione e produzione multimediale" della laurea triennale di Ingegneria informatica presso Università degli studi di Firenze.

Tutte le licenze sono fornite a scopo didattico