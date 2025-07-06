# MCP Mix Server

Server MCP do operacji na plikach CSV i Parquet, zintegrowany z n8n.

## Funkcjonalności

- **Analiza plików CSV**: Podsumowanie liczby wierszy i kolumn
- **Analiza plików Parquet**: Podsumowanie liczby wierszy i kolumn
- **Integracja z n8n**: HTTP API dla łatwej integracji
- **Docker**: Konteneryzacja dla łatwego wdrożenia

## Instalacja

### Lokalna instalacja

```bash
# Zainstaluj zależności
pip install -r requirements.txt
```

### Docker

```bash
# Zbuduj kontener
docker build -t mix-server .

# Uruchom kontener
docker run -d --name mix-server-container -p 8000:8000 --rm mix-server
```

## Użycie

### 1. Standardowy serwer MCP

```bash
python main.py
# lub
python start.py
```

### 2. HTTP serwer dla n8n

```bash
python main.py --http
# lub
python start.py --http
```

Serwer będzie dostępny na `http://localhost:8000`

### 3. Docker

```bash
python start.py --docker
```

## Endpoints API

### Health Check
```
GET /health
```

### Lista dostępnych narzędzi
```
GET /tools
```

### Wywołanie narzędzia
```
POST /call-tool
Content-Type: application/json

{
  "tool_name": "summarize_csv_file",
  "arguments": {
    "filename": "sample.csv"
  }
}
```

## Dostępne narzędzia

### `summarize_csv_file`
Analizuje plik CSV i zwraca informacje o liczbie wierszy i kolumn.

**Parametry:**
- `filename` (string): Nazwa pliku CSV w katalogu `/data`

**Przykład:**
```json
{
  "tool_name": "summarize_csv_file",
  "arguments": {
    "filename": "sample.csv"
  }
}
```

### `summarize_parquet_file`
Analizuje plik Parquet i zwraca informacje o liczbie wierszy i kolumn.

**Parametry:**
- `filename` (string): Nazwa pliku Parquet w katalogu `/data`

**Przykład:**
```json
{
  "tool_name": "summarize_parquet_file",
  "arguments": {
    "filename": "sample.parquet"
  }
}
```

## Integracja z n8n

1. **Uruchom serwer w trybie HTTP:**
   ```bash
   python start.py --http
   ```

2. **W n8n użyj HTTP Request node:**
   - Method: `POST`
   - URL: `http://localhost:8000/call-tool`
   - Headers: `Content-Type: application/json`
   - Body: JSON z parametrami narzędzia

3. **Przykładowy workflow n8n:**
   ```json
   {
     "tool_name": "summarize_csv_file",
     "arguments": {
       "filename": "{{ $json.filename }}"
     }
   }
   ```

## Struktura projektu

```
mix-server/
├── main.py              # Główny plik serwera
├── server.py            # Instancja serwera MCP
├── start.py             # Skrypt uruchamiający
├── requirements.txt     # Zależności Python
├── Dockerfile          # Konfiguracja Docker
├── n8n_config.json     # Konfiguracja dla n8n
├── data/               # Pliki danych
│   ├── sample.csv
│   └── sample.parquet
├── tools/              # Narzędzia MCP
│   ├── csv_tools.py
│   └── parquet_tools.py
└── utils/              # Narzędzia pomocnicze
    └── file_reader.py
```

## Rozszerzanie funkcjonalności

### Dodawanie nowych narzędzi

1. Utwórz nowy plik w katalogu `tools/`
2. Zaimportuj instancję MCP: `from server import mcp`
3. Użyj dekoratora `@mcp.tool()` do rejestracji narzędzia
4. Zaimportuj narzędzie w `main.py`

**Przykład:**
```python
# tools/my_tool.py
from server import mcp

@mcp.tool()
def my_custom_tool(param: str) -> str:
    """
    Opis narzędzia
    """
    return f"Wynik: {param}"
```

## Logowanie

Serwer używa standardowego modułu `logging` Python. Logi są wyświetlane w konsoli z poziomem `INFO`.

## Troubleshooting

### Błąd portu
Jeśli port 8000 jest zajęty, zmień port w `main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Zmień na inny port
```

### Brak modułów
Upewnij się, że zainstalowałeś wszystkie zależności:
```bash
pip install -r requirements.txt
```

### Problemy z Docker
Sprawdź czy Docker jest uruchomiony:
```bash
docker --version
docker ps
```