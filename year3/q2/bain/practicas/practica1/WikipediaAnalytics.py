from bs4 import BeautifulSoup, Tag
import pandas as pd
import regex as re


class WikipediaAnalytics:
    def __init__(self, list_of_strings: list[str]):
        """
        Constructor: guarda la lista de strings.
        list_of_strings puede ser rutas a HTML, URLs, nombres, etc.
        """
        self.sources: list[str] = list_of_strings
        self.df: pd.DataFrame | None = None

    def __clean_text(self, text: str | None) -> str:
        """
        Limpia el texto de caracteres no deseados y espacios extra.
        """
        if text is None:
            return ""
        return text.replace("\xa0", " ")

    def __find_infobox(self, soup: BeautifulSoup) -> Tag | None:
        """
        Busca la tabla infobox en el HTML. Devuelve el elemento Tag o None si no se encuentra.
        """
        return soup.select_one("table.infobox")

    def __spanish_month_to_number(self, month: str) -> int | None:
        """
        Convierte un nombre de mes en español a su número correspondiente (1-12).
        """
        month = month.lower().strip(". ")
        months = {
            "enero": 1,
            "febrero": 2,
            "marzo": 3,
            "abril": 4,
            "mayo": 5,
            "junio": 6,
            "julio": 7,
            "agosto": 8,
            "septiembre": 9,
            "sept": 9,
            "setiembre": 9,
            "octubre": 10,
            "noviembre": 11,
            "diciembre": 12,
        }
        return months.get(month)

    def __parse_spanish_date(self, text: str) -> pd.Timestamp:
        """
        Intenta extraer una fecha en formato español del texto.
        Devuelve pd.Timestamp o pd.NaT si no se encuentra.
        """
        if not text:
            return pd.NaT

        pattern = re.compile(
            r"(\d{1,2})\s+de\s+([A-Za-záéíóúñ\.]+)\s+de\s+(\d{4})", flags=re.IGNORECASE
        )
        matches = pattern.findall(text)
        if not matches:
            return pd.NaT

        day, month_name, year = matches[-1]
        month = self.__spanish_month_to_number(month_name)
        if month is None:
            return pd.NaT

        return pd.Timestamp(year=int(year), month=month, day=int(day))

    def __extract_last_event_date(self, table: Tag) -> pd.Timestamp:
        """
        Busca en la tabla filas que puedan contener fechas de eventos importantes (fundación, independencia, etc.)
        """
        keywords = ["historia resumida", "fundación", "formación", "independencia"]

        for tr in table.select("tr"):
            txt = self.__clean_text(tr.get_text(" ", strip=True))
            txt_lower = txt.lower()
            if any(key in txt_lower for key in keywords):
                return self.__parse_spanish_date(txt)

        return pd.NaT

    DMS_PATTERN = re.compile(
        r"(\d{1,3})°\s*(\d{1,2})[′']\s*(\d{1,2})[″\"]\s*([NSEWO])", flags=re.IGNORECASE
    )

    def __parse_dms_component(self, part: str) -> float | None:
        """
        Parsea un componente DMS (grados, minutos, segundos y hemisferio) y lo convierte a decimal.
        Devuelve el valor decimal o None si el formato no es correcto.
        """
        m = self.DMS_PATTERN.search(part)
        if not m:
            return None

        deg = float(m.group(1))
        minutes = float(m.group(2))
        seconds = float(m.group(3))
        hemi = m.group(4).upper()

        value = deg + minutes / 60.0 + seconds / 3600.0
        if hemi in {"S", "W", "O"}:
            value *= -1

        return value

    def __extract_coordinates(self, table: Tag) -> tuple[float | None, float | None]:
        """
        Busca en la tabla filas que puedan contener coordenadas en formato DMS y las convierte a decimal.
        Devuelve una tupla (latitud, longitud) o (None, None) si no se encuentran coordenadas válidas.
        """
        for tr in table.select("tr"):
            th = tr.select_one("th")
            td = tr.select_one("td")
            if not th or not td:
                continue

            key = self.__clean_text(th.get_text(" ", strip=True)).lower()
            if "capital" not in key:
                continue

            txt = self.__clean_text(td.get_text(" ", strip=True))

            lat = lon = None
            matches = list(self.DMS_PATTERN.finditer(txt))
            lat = round(self.__parse_dms_component(matches[0].group(0)), 3)
            for match in self.DMS_PATTERN.finditer(txt):
                part = match.group(0)
                hemi = match.group(4).upper()
                value = self.__parse_dms_component(part)

                if value is None:
                    continue

                if hemi in {"N", "S"}:
                    lat = round(value, 3)
                elif hemi in {"E", "W", "O"}:
                    lon = round(value, 3)

            return lat, lon

        return None, None

    def __extract_first_number(self, text: str) -> float | None:
        """
        Extrae el primer número que aparece en el texto, considerando posibles espacios, puntos o comas como separadores.
        Devuelve el número como float o None si no se encuentra ninguno válido.
        """
        if not text:
            return None

        text = self.__clean_text(text)
        m = re.search(r"-?\d[\d\s\.,]*", text)
        if not m:
            return None

        raw = m.group(0).strip()
        raw = raw.replace(" ", "")
        raw = raw.replace(".", "")
        raw = raw.replace(",", ".")

        try:
            return float(raw)
        except ValueError:
            return None

    def __extract_numeric_from_row(
        self, table: Tag, predicate: lambda key, val: bool
    ) -> float | None:
        """
        Busca en la tabla filas que cumplan una condición dada por el predicado (función que recibe key y val) y extrae el primer número de esa fila.
        Devuelve el número como float o None si no se encuentra ninguno válido.
        """
        for tr in table.select("tr"):
            th = tr.select_one("th")
            td = tr.select_one("td")
            if not th or not td:
                continue

            key = self.__clean_text(th.get_text(" ", strip=True)).lower()
            val = self.__clean_text(td.get_text(" ", strip=True))

            if predicate(key, val):
                return self.__extract_first_number(val)

        return None

    def __extract_area(self, table: Tag) -> float | None:
        """
        Busca en la tabla filas que puedan contener el área total en km² y extrae el número.
        """
        return self.__extract_numeric_from_row(
            table,
            lambda key, val: "• total" in key and "km²" in val,
        )

    def __extract_water(self, table: Tag) -> float | None:
        """
        Busca en la tabla filas que puedan contener el porcentaje de agua y extrae el número.
        """
        for tr in table.select("tr"):
            th = tr.select_one("th")
            td = tr.select_one("td")
            if not th or not td:
                continue

            key = self.__clean_text(th.get_text(" ", strip=True)).lower()
            val = self.__clean_text(td.get_text(" ", strip=True))

            if "agua" in key:
                return self.__extract_first_number(val)

        return None

    def __extract_population(self, table: Tag) -> float | None:
        """
        Busca en la tabla filas que puedan contener la población y extrae el número.
        """
        for tr in table.select("tr"):
            th = tr.select_one("th")
            td = tr.select_one("td")
            if not th or not td:
                continue

            key = self.__clean_text(th.get_text(" ", strip=True)).lower()
            val = self.__clean_text(td.get_text(" ", strip=True))

            if (
                "censo" in key or "estimación" in key or "estimacion" in key
            ) and "hab." in val:
                return self.__extract_first_number(val)

        return None

    def __extract_density(self, table: Tag) -> float | None:
        """
        Busca en la tabla filas que puedan contener la densidad de población y extrae el número.
        """
        return self.__extract_numeric_from_row(
            table,
            lambda key, val: "densidad" in key and "hab./km²" in val,
        )

    def __parse_gdp_value(self, text: str) -> float | None:
        """
        Parsea un valor de PIB que puede contener palabras como "billones" o "millones" y lo convierte a un número float.
        """
        text_clean = self.__clean_text(text).lower()
        base = self.__extract_first_number(text_clean)
        if base is None:
            return None

        if "bill" in text_clean:
            return float(base * 1e12)

        if "mill" in text_clean:
            return float(base * 1e6)

        return float(base)

    def __extract_gdp(self, table: Tag) -> float | None:
        """
        Busca en la tabla filas que puedan contener el PIB nominal total y extrae el número.
        """
        rows = table.select("tr")
        in_nominal_block = False

        for tr in rows:
            th = tr.select_one("th")
            td = tr.select_one("td")

            key = self.__clean_text(th.get_text(" ", strip=True)).lower() if th else ""
            val = self.__clean_text(td.get_text(" ", strip=True)) if td else ""

            if "pib (nominal)" in key:
                in_nominal_block = True
                continue

            if in_nominal_block and "• total" in key:
                return self.__parse_gdp_value(val)

        return None

    def __extract_country_name(self, soup: BeautifulSoup) -> str | None:
        """
        Intenta extraer el nombre del país del título de la página o del primer encabezado h1.
        Devuelve el nombre limpio o None si no se encuentra.
        """
        if soup.title:
            title = self.__clean_text(soup.title.get_text())
            return title.split(" - Wikipedia")[0].strip()

        h1 = soup.select_one("h1")
        return self.__clean_text(h1.get_text()) if h1 else None

    def scrap(self) -> None:
        """
        Procesa los ficheros HTML y construye el DataFrame final.
        """
        records = []

        for source in self.sources:
            with open(source, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")

            table = self.__find_infobox(soup)
            if table is None:
                continue

            country_name = self.__extract_country_name(soup)
            latitude, longitude = self.__extract_coordinates(table)
            area = self.__extract_area(table)
            water = self.__extract_water(table)
            population = self.__extract_population(table)
            density = self.__extract_density(table)
            gdp = self.__extract_gdp(table)
            last_event_date = self.__extract_last_event_date(table)

            records.append(
                {
                    "Country Name": country_name,
                    "Area (KM^2)": area,
                    "Water (%)": water,
                    "Population (hab.)": population,
                    "Density (hab./km^2)": density,
                    "GDP ($)": gdp,
                    "Last Event Date": last_event_date,
                    "Latitude (º)": latitude,
                    "Longitude(º)": longitude,
                }
            )

        self.df = pd.DataFrame(
            records,
            columns=[
                "Country Name",
                "Area (KM^2)",
                "Water (%)",
                "Population (hab.)",
                "Density (hab./km^2)",
                "GDP ($)",
                "Last Event Date",
                "Latitude (º)",
                "Longitude(º)",
            ],
        )

        if self.df.empty:
            return

        self.df = self.df.astype(
            {
                "Country Name": "string",
                "Area (KM^2)": "float64",
                "Water (%)": "float64",
                "Population (hab.)": "float64",
                "Density (hab./km^2)": "float64",
                "GDP ($)": "float64",
                "Latitude (º)": "float64",
                "Longitude(º)": "float64",
            }
        )
        self.df["Last Event Date"] = pd.to_datetime(self.df["Last Event Date"])

    def select_row_by_value(self, col_name: str, value):
        """
        Devuelve la fila (o filas) cuyo valor en col_name coincide con value.
        Si no hay coincidencias, devuelve None.
        """
        if self.df is None:
            raise ValueError(
                "El DataFrame no ha sido inicializado. Ejecuta scrap() primero."
            )
        if col_name not in self.df.columns:
            raise ValueError(f"La columna '{col_name}' no existe.")

        result = self.df[self.df[col_name] == value]
        return result if not result.empty else None

    def get_columns(self, col_names):
        """
        Recibe una columna o lista de columnas y devuelve esa parte del DataFrame.
        """
        if self.df is None:
            raise ValueError(
                "El DataFrame no ha sido inicializado. Ejecuta scrap() primero."
            )

        if isinstance(col_names, str):
            col_names = [col_names]

        missing = [col for col in col_names if col not in self.df.columns]
        if missing:
            raise ValueError(f"Las columnas no existen: {missing}")

        return self.df[col_names]

    def aggregate_column(self, col_name: str, operation: str) -> float:
        """
        Agrega una columna numérica según una operación dada:
        - 'max'
        - 'min'
        - 'mean'
        Devuelve el resultado como un float.
        """
        if self.df is None:
            raise ValueError(
                "El DataFrame no ha sido inicializado. Ejecuta scrap() primero."
            )
        if col_name not in self.df.columns:
            raise ValueError(f"La columna '{col_name}' no existe.")

        series = self.df[col_name]
        if not pd.api.types.is_numeric_dtype(series):
            raise ValueError(f"La columna '{col_name}' no es numérica.")

        op = operation.lower()
        if op == "max":
            return float(series.max())
        if op == "min":
            return float(series.min())
        if op == "mean":
            return float(series.mean())

        raise ValueError("La operación debe ser 'max', 'min' o 'mean'.")
