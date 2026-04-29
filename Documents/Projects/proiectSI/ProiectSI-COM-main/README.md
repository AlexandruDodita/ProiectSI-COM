# Proiect Securitatea Informatiei - Sistem de Comunicare Criptata

## Descriere

Sistem de comunicare securizata intre doua statii folosind:
- Criptare simetrica AES-256 (CBC mode)
- Key agreement Diffie-Hellman pentru schimbul securizat de chei
- Fragmentare si reasamblare mesaje
- Socket communication pentru transmitere

## Structura Proiect

### Module Principale

1. **aes_crypto.py** - Implementare criptare AES
   - Criptare/decriptare AES-256 in modul CBC
   - Padding automat PKCS7
   - Generare chei aleatoare

2. **key_agreement.py** - Protocol Diffie-Hellman
   - Generare perechi de chei publice/private
   - Calculare secret comun
   - Derivare cheie AES din secretul comun

3. **message_splitter.py** - Fragmentare mesaje
   - Impartire mesaje/fisiere in blocuri
   - Reasamblare blocuri in mesaj original
   - Suport pentru date binare

4. **secure_station.py** - Statie de comunicare
   - Server/client socket
   - Schimb automat de chei Diffie-Hellman
   - Trimitere/primire mesaje criptate fragmentate

### Teste

5. **test_vectors.py** - Vectori de test AES
   - Test mesaje simple
   - Test mesaje lungi
   - Test caractere Unicode
   - Test date binare

6. **test_communication.py** - Teste comunicare
   - Test comunicare simpla intre 2 statii
   - Test mesaje lungi (blocuri multiple)
   - Framework pentru teste bidirectionale

7. **demo.py** - Script demonstratie
   - Mod server: asculta pe un port
   - Mod client: trimite mesaj catre server

## Instalare

```bash
pip install -r requirements.txt
```

## Utilizare

### Rulare teste AES:
```bash
python test_vectors.py
```

### Rulare teste comunicare:
```bash
python test_communication.py
```

### Demo comunicare manuala:

Terminal 1 (Server):
```bash
python demo.py server 5000
```

Terminal 2 (Client):
```bash
python demo.py client 5000 "mesajul meu secret"
```

## Cerinte Implementate

✅ Criptare simetrica (AES-256)
✅ Vectori de test pentru algoritm simetric  
✅ Key agreement Diffie-Hellman
✅ Sistem de comunicare client-server
✅ Transmitere mesaje criptate/decriptate
✅ Impartire mesaje in blocuri
✅ Reasamblare blocuri la receptie
✅ Teste pentru comunicare criptata intre 2 statii

## Flux de Comunicare

1. Statia server porneste si asculta pe un port
2. Statia client se conecteaza la server
3. Cele doua statii fac schimb de chei publice Diffie-Hellman
4. Fiecare statie calculeaza secretul comun si deriva cheia AES
5. Clientul cripteaza mesajul cu AES
6. Mesajul criptat este fragmentat in blocuri
7. Blocurile sunt trimise secvential
8. Serverul receptioneaza si reconstruieste mesajul
9. Serverul decripteaza mesajul cu cheia AES

## Detalii Tehnice

- **AES**: 256 biti, modul CBC, padding PKCS7
- **Diffie-Hellman**: Prim 2048 biti (RFC 3526), generator G=2
- **Derivare cheie**: SHA-256 din secretul comun
- **Dimensiune bloc**: 512 bytes (configurabil)
- **Encoding**: Base64 pentru date binare, UTF-8 pentru text
