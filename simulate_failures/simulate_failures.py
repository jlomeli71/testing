from collections import defaultdict

#############################################################
# This file will simulate the failures on ISP_Tx DWDM Network
#############################################################

# This dictionary is used to map site IDs to their descriptions
# It is used to provide a human-readable description of each site in the network
# Add new sites to this dictionary as needed
site_id = {
    "MSOTOL01": "Toluca",
    "NFO-117": "Maravatio",
    "NFO-006": "Leon LD",
    "NFO-027": "AGS Bestel",
    "NFO-044": "SLP Bestel",
    "NFO-025": "SLP Marcatel",
    "NFO-075": "MTY Marcatel",
    "NFO-076": "MTY Transtelco",
    "NFO-038": "Nuevo Laredo",
    "MSOMTY02": "Buenos Aires",
    "MSOMTY01": "Apodaca",
    "NFO-009": "QRO San Pablo",
    "NFO-040": "QRO Bestel",
    "MSOMEX04": "Ceylan",
    "MSOMEX01": "Megacentro",
    "MSOGDL02": "Canada",
    "MSOGDL01": "Tlaquepaque",
    "TAMREY1273": "Reynosa Iusatel",
    "NFO-022": "Reynosa Marcatel",
    "NFO-053": "Poza Rica Maxcom",
    "MSOPUE01": "Puebla Calera",
    "NFO-010": "Rio Frio",
    "NFO-004": "Jilotepec",
    "NFO-032": "Irapuato Bestel",
    "MSOMTY03": "Gonzalitos",
}

# Each trayectory or lambda in the DWDN network conteings several segments represented by sets of site IDs

laredo_toluca = {
    "name": "Laredo to Toluca",
    "segments": [
        {"NFO-038", "NFO-076"},
        {"NFO-076", "NFO-075"},
        {"NFO-075", "NFO-025"},
        {"NFO-025", "NFO-044"},
        {"NFO-044", "NFO-027"},
        {"NFO-027", "NFO-006"},
        {"NFO-006", "NFO-117"},
        {"NFO-117", "MSOTOL01"},
    ]
}

laredo_apodaca = {
    "name": "Laredo to Apodaca",
    "segments": [
        {"NFO-038", "NFO-076"},
        {"NFO-076", "MSOMTY02"},
        {"MSOMTY02", "MSOMTY01"}
    ]
}

laredo_megacentro = {
    "name": "Laredo to Megacentro",
    "segments": [
        {"NFO-038", "NFO-076"},
        {"NFO-076", "NFO-044"},
        {"NFO-044", "NFO-025"},
        {"NFO-025", "NFO-009"},
        {"NFO-009", "NFO-040"},
        {"NFO-040", "MSOMEX04"},
        {"MSOMEX04", "MSOMEX01", "ruta_2"}
    ]
}

laredo_tlaquepaque = {
    "name": "Laredo to Tlaquepaque",
    "segments": [
        {"NFO-038", "NFO-076"},
        {"NFO-076", "NFO-044"},
        {"NFO-044", "NFO-027"},
        {"NFO-027", "NFO-006"},
        {"NFO-006", "MSOGDL02"},
        {"MSOGDL02", "MSOGDL01", "ruta_1"}
    ]
}

reynosa_toluca = {
    "name": "Reynosa to Toluca",
    "segments": [
        {"TAMREY1273", "NFO-022"},
        {"NFO-022", "NFO-053"},
        {"NFO-053", "MSOPUE01"},
        {"MSOPUE01", "NFO-010"},
        {"NFO-010", "MSOMEX04"},
        {"MSOMEX04", "MSOTOL01"}
    ]
}

reynosa_megacentro = {
    "name": "Reynosa to Megacentro",
    "segments": [
        {"TAMREY1273", "NFO-022"},
        {"NFO-022", "NFO-075"},
        {"NFO-075", "NFO-025"},
        {"NFO-025", "NFO-009"},
        {"NFO-009", "NFO-004"},
        {"NFO-004", "MSOMEX04"},
        {"MSOMEX04", "MSOMEX01", "ruta_1"}
    ]
}

reynosa_tlaquepaque = {
    "name": "Reynosa to Tlaquepaque",
    "segments": [
        {"TAMREY1273", "NFO-022"},
        {"NFO-022", "NFO-075"},
        {"NFO-075", "NFO-025"},
        {"NFO-025", "NFO-009"},
        {"NFO-009", "NFO-040"},
        {"NFO-040", "NFO-032"},
        {"NFO-032", "MSOGDL02"},
        {"MSOGDL02", "MSOGDL01", "ruta_2"}
    ]
}

reynosa_apodaca = {
    "name": "Reynosa to Apodaca",
    "segments": [
        {"TAMREY1273", "NFO-022"},
        {"NFO-022", "NFO-075"},
        {"NFO-075", "MSOMTY02"},
        {"MSOMTY02", "MSOMTY03"},
        {"MSOMTY03", "MSOMTY01"}
    ]
}

megacentro_toluca = {
    "name": "Megacentro to Toluca",
    "segments": [
        {"MSOMEX01", "MSOMEX04", "ruta_1"},
        {"MSOMEX04", "MSOTOL01"}
    ]
}

toluca_tlaquepaque = {
    "name": "Toluca to Tlaquepaque",
    "segments": [
        {"MSOTOL01", "NFO-004"},
        {"NFO-004", "NFO-009"},
        {"NFO-009", "NFO-040"},
        {"NFO-040", "NFO-032"},
        {"NFO-032", "MSOGDL02"},
        {"MSOGDL02", "MSOGDL01", "ruta_2"}
    ]
}

tlaquepaque_apodaca = {
    "name": "Tlaquepaque to Apodaca",
    "segments": [
        {"MSOGDL01", "MSOGDL02", "ruta_1"},
        {"MSOGDL02", "NFO-006"},
        {"NFO-006", "NFO-027"},
        {"NFO-027", "NFO-044"},
        {"NFO-044", "NFO-076"},
        {"NFO-076", "MSOMTY02"},
        {"MSOMTY02", "MSOMTY03"},
        {"MSOMTY03", "MSOMTY01"}
    ]
}

apodaca_megacentro = {
    "name": "Apodaca to Megacentro",
    "segments": [
        {"MSOMTY01", "MSOMTY02"},
        {"MSOMTY02", "NFO-076"},
        {"NFO-076", "NFO-044"},
        {"NFO-044", "NFO-027"},
        {"NFO-027", "NFO-006"},
        {"NFO-006", "NFO-032"},
        {"NFO-032", "NFO-040"},
        {"NFO-040", "MSOMEX04"},
        {"MSOMEX04", "MSOMEX01", "ruta_2"}
    ]
}

# In order to create a unique list of segments, we will use a set to store the segments and then convert it to a list
lambdas = [
    laredo_toluca,
    laredo_apodaca,
    laredo_megacentro,
    laredo_tlaquepaque,
    reynosa_toluca,
    reynosa_megacentro,
    reynosa_tlaquepaque,
    reynosa_apodaca,
    megacentro_toluca,
    toluca_tlaquepaque,
    tlaquepaque_apodaca,
    apodaca_megacentro,
]

# Function to get all unique segments from the lambdas

def get_all_segments(lambdas):
    """Get all unique segments from the given lambdas."""
    all_segments = set()
    for lambda_segments in lambdas:
        for segment in lambda_segments["segments"]:
            # Convert each segment to a sorted tuple for hashability and uniqueness
            all_segments.add(tuple(sorted(segment)))
    return list(all_segments)


print("All unique segments in all the lambdas:")
unique_segments = get_all_segments(lambdas)
print(f"Total unique segments: {len(unique_segments)}")
print(unique_segments)


# Elije uno a uno los segmentos de la lista unique_segments y crea una lista de listas con los segmentos que la incluyen
# Proporciona la impresion de las listas de manera desdcendente, las que tienen listas mas grandes primero

def create_segment_lists(unique_segments):
    """Create a list of lists containing segments that include each unique segment."""
    segment_lists = []
    for segment in unique_segments:
        segment_list = []
        for lambda_segments in lambdas:
            if set(segment).issubset(set().union(*lambda_segments["segments"])):
                segment_list.append(lambda_segments["name"])
        segment_lists.append(segment_list)
    return segment_lists

segment_lists = create_segment_lists(unique_segments)
print("\nSegment lists for each unique segment:")
for i, segment in enumerate(unique_segments):
    print(f"Segment {i + 1}: {segment} -> Lists: {segment_lists[i]}")   

# Crea un diagrama de barras en el que se muestre la cantidad de veces que cada segmento aparece en las listas
# Pon en la columna X el segmento y en la columna Y la cantidad de veces que aparece,
# Ordena que las barras aparescan de manera descendente
import matplotlib.pyplot as plt

# Construir un diccionario que mapea cada segmento a la lista de lambdas donde aparece
segment_to_lambdas = {}
for i, segment in enumerate(unique_segments):
    segment_to_lambdas[segment] = segment_lists[i]

def plot_segment_frequencies(segment_to_lambdas):
    # Ordenar los segmentos por frecuencia descendente
    sorted_items = sorted(segment_to_lambdas.items(), key=lambda x: len(x[1]), reverse=True)
    segments = [str(item[0]) for item in sorted_items]
    frequencies = [len(item[1]) for item in sorted_items]

    plt.figure(figsize=(12, 6))
    plt.barh(segments, frequencies, color='skyblue')
    plt.xlabel('Cantidad de Lambdas')
    plt.title('Frecuencia de Segmentos en Lambdas')
    plt.gca().invert_yaxis()  # Invertir el eje Y para mostrar el más frecuente arriba
    plt.tight_layout()
    plt.show()

plot_segment_frequencies(segment_to_lambdas)

# Agrega otra grafica similar, pero que en lugar de mostrar el Site ID, muestre el nombre del sitio
def plot_segment_frequencies_with_names(segment_to_lambdas):
    # Mapeo de site IDs a nombres
    segment_names = {frozenset(segment): [site_id.get(site, site) for site in segment] for segment in unique_segments}

    # Ordenar los segmentos por frecuencia descendente
    sorted_items = sorted(segment_to_lambdas.items(), key=lambda x: len(x[1]), reverse=True)
    segments = [segment_names[item[0]] for item in sorted_items]
    frequencies = [len(item[1]) for item in sorted_items]

    plt.figure(figsize=(12, 6))
    plt.barh([' & '.join(seg) for seg in segments], frequencies, color='lightgreen')
    plt.xlabel('Cantidad de Lambdas')
    plt.title('Frecuencia de Segmentos en Lambdas (con Nombres)')
    plt.gca().invert_yaxis()  # Invertir el eje Y para mostrar el más frecuente arriba
    plt.tight_layout()
    plt.show()

plot_segment_frequencies_with_names(segment_to_lambdas)

