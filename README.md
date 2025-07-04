# Django ecommerce

Un sito di e-commerce realizzato con Django e deployment su Railway.

## 🔧 Funzionalità principali
- Visualizzazione ed interazione dei prodotti
- Acquisto prodotti
- Dettagli prodotto
- Login/Logout utenti
- Gestione account
- Gestione ordini e carrello
- Controllo completo del sito con la "Manager vision", la funzionalità dedicata ai manager dell'e-commerce
- Admin integrato con gestione di prodotti, utenti, categorie e ordini


## 🚀 Deploy

Il progetto è deployato su [Railway](https://railway.app)

## 🖼️ Media Storage

Le immagini dei prodotti e degli utenti sono gestite tramite **Cloudinary**, evitando la perdita di file nei deploy.

## 🛠️ Setup locale

1. Clona il progetto:
   ```bash
   git clone https://github.com/tuo-utente/tuo-repo.git
   cd tua-repo
2. Crea un ambiente conda e attivalo
    ```bash
    conda create -n ecommerce-env python=3.11
    conda activate ecommerce-env
3. Installa le dipendenze presenti in requirements.txt
    ```bash
   pip install -r requirements.txt
4. Crea file .env nella root del progetto e aggiungi
    ```bash
    DEBUG=True
    CLOUDINARY_CLOUD_NAME=tuo_cloud_name
    CLOUDINARY_API_KEY=la_tua_api_key
    CLOUDINARY_API_SECRET=la_tua_api_secret
5. Applica migrazioni e avvia il server
    ```bash
    python manage.py migrate
    python manage.py runserver
