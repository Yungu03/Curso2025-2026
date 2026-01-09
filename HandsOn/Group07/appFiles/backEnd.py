from flask import Flask, jsonify, request, send_from_directory, render_template
from SPARQLWrapper import SPARQLWrapper, JSON
from datetime import datetime, timedelta
import math
import time

app = Flask(__name__, static_folder='static')

# Endpoint SPARQL de GraphDB
SPARQL_ENDPOINT = "http://Fernandos-MacBook-Air.local:7200/repositories/MoveMadrid"
sparql = SPARQLWrapper(SPARQL_ENDPOINT)
sparql.setReturnFormat(JSON)

# Caché global para almacenar los datos
data_cache = {
    'last_update': None,
    'events': [],
    'car_parkings': [],
    'bicycle_parkings': [],
    'barrios': set(),
    'tipos_evento': set()
}

# Cache para notificaciones
notification_cache = {
    'user_sessions': {},
    'last_event_count': 0
}

# --- Funciones de utilidad ---
def calcular_distancia(lat1, lon1, lat2, lon2):
    R = 6371e3  # Radio de la Tierra en metros
    φ1 = math.radians(lat1)
    φ2 = math.radians(lat2)
    Δφ = math.radians(lat2 - lat1)
    Δλ = math.radians(lon2 - lon1)

    a = math.sin(Δφ/2) * math.sin(Δφ/2) + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ/2) * math.sin(Δλ/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c  # Distancia en metros

def filtrar_bicycle_parkings_cercanos(bike_parkings, radio_metros=10):
    parkings_filtrados = []
    
    for parking in bike_parkings:
        es_demasiado_cercano = False
        
        for parking_existente in parkings_filtrados:
            distancia = calcular_distancia(
                float(parking['lat']),
                float(parking['lng']),
                float(parking_existente['lat']),
                float(parking_existente['lng'])
            )
            
            if distancia <= radio_metros:
                es_demasiado_cercano = True
                break
        
        if not es_demasiado_cercano:
            parkings_filtrados.append(parking)
    
    return parkings_filtrados

def formatear_tipo_evento(tipo_completo):
    if not tipo_completo:
        return 'Evento'
    
    partes = tipo_completo.split('/')
    tipo_formateado = partes[-1] if partes else 'Evento'
    tipo_formateado = tipo_formateado.replace('_', ' ').replace('-', ' ')
    return tipo_formateado.title()

def actualizar_cache():
    """Ejecuta la query principal y actualiza la caché"""
    try:
        print("🔄 Actualizando caché desde GraphDB...")
        
        query_principal = """
        PREFIX mm: <http://movemadrid.org/ontology/movilidad#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?event ?eventTitle ?eventDesc ?eventDate
               ?facilityName ?facilityNeighborhoodName ?facilityDistrictName ?facilityLat ?facilityLong
               ?parkingName ?parkingDesc ?parkingLat ?parkingLong ?parkingLink
               ?bicycleLat ?bicycleLong
               ?freeEvent ?eventEndDate ?eventLink ?eventType
        WHERE {
          ?event a mm:Event ;
                 mm:eventTitle ?eventTitle ;
                 mm:eventDescription ?eventDesc ;
                 mm:startsOnDate ?eventDate ;
                 mm:eventFacility ?facility .

          ?facility mm:facilityName ?facilityName ;
                    mm:facilityDistrict ?facilityDistrict ;
                    mm:facilityNeighborhood ?neighResource ;
                    mm:facilityLatitude ?facilityLat ;
                    mm:facilityLongitude ?facilityLong .

          ?neighResource rdfs:label ?facilityNeighborhoodName ;
                         owl:sameAs ?neighURI .
          ?facilityDistrict rdfs:label ?facilityDistrictName ;
                            owl:sameAs ?districtURI .

          OPTIONAL {
            ?parking a mm:CarParking ;
                     mm:carParkingName ?parkingName ;
                     owl:sameAsNeighborhood ?neighURI .
            OPTIONAL { ?parking mm:carParkingDescription ?parkingDesc }
            OPTIONAL { ?parking mm:carParkingLatitude ?parkingLat }
            OPTIONAL { ?parking mm:carParkingLongitude ?parkingLong }
            OPTIONAL { ?parking mm:carParkingLink ?parkingLink }
          }

          OPTIONAL {
            ?bicycle a mm:BicycleParking ;
                     owl:sameAsNeighborhood ?neighURI ;
                     mm:bicycleParkingLatitude ?bicycleLat ;
                     mm:bicycleParkingLongitude ?bicycleLong .
          }

          OPTIONAL { ?event mm:freeEvent ?freeEvent }
          OPTIONAL { ?event mm:endsOnDate ?eventEndDate }
          OPTIONAL { ?event mm:eventLink ?eventLink }
          OPTIONAL { ?event mm:eventType ?eventType }
        }
        """

        sparql.setQuery(query_principal)
        results = sparql.query().convert()

        # Reiniciar caché
        eventos_dict = {}
        car_parkings_set = set()
        bicycle_parkings_set = set()
        barrios_set = set()
        tipos_evento_set = set()

        for r in results["results"]["bindings"]:
            # Procesar evento
            event_id = r["event"]["value"]
            if event_id not in eventos_dict:
                eventos_dict[event_id] = {
                    "evento": r.get("eventTitle", {}).get("value", ""),
                    "descripcion": r.get("eventDesc", {}).get("value", ""),
                    "fecha": r.get("eventDate", {}).get("value", ""),
                    "fin_evento": r.get("eventEndDate", {}).get("value", ""),
                    "evento_gratuito": r.get("freeEvent", {}).get("value", ""),
                    "link_evento": r.get("eventLink", {}).get("value", ""),
                    "tipo_evento": r.get("eventType", {}).get("value", ""),
                    "tipo_evento_formateado": formatear_tipo_evento(r.get("eventType", {}).get("value", "")),
                    "instalacion": r.get("facilityName", {}).get("value", ""),
                    "eventLat": r.get("facilityLat", {}).get("value", ""),
                    "eventLong": r.get("facilityLong", {}).get("value", ""),
                    "barrio": r.get("facilityNeighborhoodName", {}).get("value", ""),
                    "distrito": r.get("facilityDistrictName", {}).get("value", "")
                }
                
                # Agregar barrio y tipo de evento
                barrio = r.get("facilityNeighborhoodName", {}).get("value")
                if barrio:
                    barrios_set.add(barrio)
                
                tipo_evento = formatear_tipo_evento(r.get("eventType", {}).get("value", ""))
                if tipo_evento:
                    tipos_evento_set.add(tipo_evento)

            # Procesar car parking
            parking_name = r.get("parkingName", {}).get("value")
            if parking_name:
                parking_key = f"{parking_name}_{r.get('parkingLat', {}).get('value')}_{r.get('parkingLong', {}).get('value')}"
                if parking_key not in car_parkings_set:
                    car_parkings_set.add(parking_key)
                    data_cache['car_parkings'].append({
                        "nombre": parking_name,
                        "descripcion": r.get("parkingDesc", {}).get("value", ""),
                        "lat": r.get("parkingLat", {}).get("value", ""),
                        "lng": r.get("parkingLong", {}).get("value", ""),
                        "url": r.get("parkingLink", {}).get("value", ""),
                        "barrio": barrio
                    })

            # Procesar bicycle parking
            bicycle_lat = r.get("bicycleLat", {}).get("value")
            bicycle_long = r.get("bicycleLong", {}).get("value")
            if bicycle_lat and bicycle_long:
                bicycle_key = f"{bicycle_lat}_{bicycle_long}"
                if bicycle_key not in bicycle_parkings_set:
                    bicycle_parkings_set.add(bicycle_key)
                    data_cache['bicycle_parkings'].append({
                        "lat": bicycle_lat,
                        "lng": bicycle_long,
                        "barrio": barrio
                    })

        # Actualizar caché principal
        data_cache['events'] = list(eventos_dict.values())
        data_cache['barrios'] = list(barrios_set)
        data_cache['tipos_evento'] = list(tipos_evento_set)
        data_cache['last_update'] = time.time()
        
        # Aplicar filtro de proximidad a bicycle parkings
        data_cache['bicycle_parkings'] = filtrar_bicycle_parkings_cercanos(data_cache['bicycle_parkings'], 10)
        
        print(f"✅ Caché actualizada: {len(data_cache['events'])} eventos, "
              f"{len(data_cache['car_parkings'])} car parkings, "
              f"{len(data_cache['bicycle_parkings'])} bicycle parkings, "
              f"{len(data_cache['barrios'])} barrios")
              
    except Exception as e:
        print(f"❌ Error actualizando caché: {e}")

# --- Funciones para notificaciones ---
def limpiar_notificaciones_expiradas(user_session):
    ahora = datetime.now()
    notificaciones_activas = []
    
    for notif in user_session['notifications']:
        # Si tiene fecha de fin y ya pasó, no incluir
        if notif.get('fecha_fin'):
            try:
                fecha_fin = datetime.fromisoformat(notif['fecha_fin'].replace('Z', '+00:00'))
                if fecha_fin >= ahora:
                    notificaciones_activas.append(notif)
            except:
                # Si hay error en el formato, mantener la notificación
                notificaciones_activas.append(notif)
        else:
            # Si no tiene fecha de fin, mantenerla (evento permanente)
            notificaciones_activas.append(notif)
    
    user_session['notifications'] = notificaciones_activas
    user_session['last_cleanup'] = ahora.isoformat()

# --- Endpoints ---
@app.route("/")
def index():
    return render_template("frontend.html")

# --- Endpoint principal que usa la caché ---
@app.route("/allData")
def get_all_data():
    # Actualizar caché si es necesario (cada 5 minutos)
    if not data_cache['last_update'] or time.time() - data_cache['last_update'] > 300:
        actualizar_cache()
    
    return jsonify({
        'events': data_cache['events'],
        'car_parkings': data_cache['car_parkings'],
        'bicycle_parkings': data_cache['bicycle_parkings'],
        'barrios': data_cache['barrios'],
        'tipos_evento': data_cache['tipos_evento'],
        'last_update': data_cache['last_update']
    })

# --- Endpoints secundarios que filtran desde la caché ---
@app.route("/events")
def get_events():
    if not data_cache['last_update']:
        actualizar_cache()
    
    barrio = request.args.get("barrio", "").strip().lower()
    tipo_evento = request.args.get("tipoEvento", "").strip()
    gratuito = request.args.get("gratuito", "").strip()
    fecha_filtro = request.args.get("fechaFiltro", "").strip()

    eventos_filtrados = []
    
    for evento in data_cache['events']:
        cumple_filtros = True
        
        # Filtro por barrio
        if barrio and barrio not in evento.get('barrio', '').lower():
            cumple_filtros = False
        
        # Filtro por tipo de evento
        if tipo_evento and evento.get('tipo_evento_formateado', '') != tipo_evento:
            cumple_filtros = False
        
        # Filtro por gratuito
        if gratuito and evento.get('evento_gratuito', '') != gratuito:
            cumple_filtros = False
        
        # Filtro por fecha
        if fecha_filtro and evento.get('fecha', ''):
            fecha_evento = evento.get('fin_evento', '') if evento.get('fin_evento') else evento.get('fecha', '')
            if fecha_evento < fecha_filtro:
                cumple_filtros = False
        
        if cumple_filtros:
            eventos_filtrados.append(evento)
    
    print(f"DEBUG: {len(data_cache['events'])} eventos en caché, {len(eventos_filtrados)} después de filtrar")
    return jsonify(eventos_filtrados)

@app.route("/carParkings")
def get_car_parkings():
    if not data_cache['last_update']:
        actualizar_cache()
    
    barrio = request.args.get("barrio", "").strip().lower()
    
    if barrio:
        parkings_filtrados = [p for p in data_cache['car_parkings'] 
                             if barrio in p.get('barrio', '').lower()]
    else:
        parkings_filtrados = data_cache['car_parkings']
    
    return jsonify(parkings_filtrados)

@app.route("/bicycleParkings")
def get_bicycle_parkings():
    if not data_cache['last_update']:
        actualizar_cache()
    
    barrio = request.args.get("barrio", "").strip().lower()
    
    if barrio:
        parkings_filtrados = [p for p in data_cache['bicycle_parkings'] 
                             if barrio in p.get('barrio', '').lower()]
    else:
        parkings_filtrados = data_cache['bicycle_parkings']
    
    return jsonify(parkings_filtrados)

@app.route("/barrios")
def get_barrios():
    if not data_cache['last_update']:
        actualizar_cache()
    
    return jsonify(sorted(data_cache['barrios']))

@app.route("/tiposEvento")
def get_tipos_evento():
    if not data_cache['last_update']:
        actualizar_cache()
    
    return jsonify(sorted(data_cache['tipos_evento']))

# --- Endpoints de Notificaciones ---
@app.route("/nuevosEventos")
def get_nuevos_eventos():
    usuario_id = request.args.get("usuario_id", "default")
    limpiar_antiguas = request.args.get("limpiar", "true") == "true"
    
    # Usar datos de la caché existente en lugar de hacer nueva consulta
    eventos_disponibles = data_cache['events']
    
    # Inicializar sesión de usuario
    if usuario_id not in notification_cache['user_sessions']:
        notification_cache['user_sessions'][usuario_id] = {
            'notifications': [],
            'events_seen': set([evento.get('evento', '') for evento in eventos_disponibles]),
            'last_cleanup': datetime.now().isoformat()
        }
        return jsonify({
            "nuevos_eventos": [],
            "notificaciones_activas": [],
            "total_activas": 0
        })
    
    user_session = notification_cache['user_sessions'][usuario_id]
    
    # Limpiar notificaciones antiguas si se solicita
    if limpiar_antiguas:
        limpiar_notificaciones_expiradas(user_session)
    
    # Identificar eventos nuevos comparando con caché
    eventos_nuevos = []
    ahora = datetime.now()
    
    for evento in eventos_disponibles:
        event_id = evento.get('evento', '')
        event_end_date = evento.get('fin_evento', '')
        
        # Verificar si el evento ya expiró
        if event_end_date:
            try:
                fecha_fin = datetime.fromisoformat(event_end_date.replace('Z', '+00:00'))
                if fecha_fin < ahora:
                    continue  # Saltar eventos expirados
            except:
                pass  # Si hay error en el formato, continuar
        
        # Verificar si es un evento nuevo
        if event_id not in user_session['events_seen']:
            eventos_nuevos.append({
                "event_uri": event_id,
                "evento": evento.get('evento', ''),
                "barrio": evento.get('barrio', ''),
                "fecha_inicio": evento.get('fecha', ''),
                "fecha_fin": event_end_date,
                "timestamp": datetime.now().isoformat(),
                "tipo_evento": evento.get('tipo_evento_formateado', '')
            })
            user_session['events_seen'].add(event_id)
    
    # Agregar nuevos eventos a las notificaciones
    if eventos_nuevos:
        user_session['notifications'].extend(eventos_nuevos)
    
    return jsonify({
        "nuevos_eventos": eventos_nuevos,
        "notificaciones_activas": user_session['notifications'],
        "total_activas": len(user_session['notifications'])
    })

@app.route("/checkNuevosEventos")
def check_nuevos_eventos():
    usuario_id = request.args.get("usuario_id", "default")
    
    # Consulta ultra rápida - usar cache de eventos
    total_actual = len(data_cache['events'])
    
    if usuario_id in notification_cache['user_sessions']:
        user_session = notification_cache['user_sessions'][usuario_id]
        nuevos = total_actual - len(user_session['events_seen'])
        return jsonify({"hay_nuevos": nuevos > 0, "cantidad": nuevos})
    
    return jsonify({"hay_nuevos": False, "cantidad": 0})

@app.route("/limpiarNotificaciones", methods=["POST"])
def limpiar_notificaciones():
    usuario_id = request.args.get("usuario_id", "default")
    
    if usuario_id in notification_cache['user_sessions']:
        notification_cache['user_sessions'][usuario_id]['notifications'] = []
    
    return jsonify({"status": "success", "message": "Notificaciones limpiadas"})

@app.route("/eliminarNotificacion", methods=["POST"])
def eliminar_notificacion():
    usuario_id = request.args.get("usuario_id", "default")
    event_uri = request.json.get("event_uri")
    
    if usuario_id in notification_cache['user_sessions']:
        user_session = notification_cache['user_sessions'][usuario_id]
        user_session['notifications'] = [
            notif for notif in user_session['notifications'] 
            if notif['event_uri'] != event_uri
        ]
    
    return jsonify({"status": "success", "message": "Notificación eliminada"})

@app.route("/refreshCache")
def refresh_cache():
    actualizar_cache()
    return jsonify({"status": "success", "message": "Cache refreshed successfully"})

# --- Servir archivos estáticos ---
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    # Inicializar caché al iniciar la aplicación
    actualizar_cache()
    app.run(debug=True, port=5001)