"""
Módulo para manejar correos temporales usando la API de Mail.tm (tmp-mail.org)
Requerido: Python 3.11
"""

import requests
import time
import random
import string
from typing import Optional, List, Dict


class CorreoTemporal:
    """
    Clase para manejar correos temporales usando Mail.tm API (tmp-mail.org)
    API gratuita sin necesidad de API key
    """
    
    BASE_URL = "https://api.mail.tm"
    token = None
    
    def __init__(self, email: Optional[str] = None, password: Optional[str] = None):
        """
        Inicializa el correo temporal
        
        Args:
            email: Dirección de correo opcional. Si no se proporciona, se genera una aleatoria
            password: Contraseña opcional para la cuenta (si no se proporciona, se genera una aleatoria)
        """
        if email:
            self.email = email
            self.password = password or self._generar_password()
            self.login, self.domain = email.split('@')
        else:
            self.email, self.password = self._crear_cuenta()
            self.login, self.domain = self.email.split('@')
        
        # Autenticarse para obtener token (con reintentos)
        if not self._autenticar():
            print(f"⚠ Advertencia: No se pudo autenticar, pero el correo {self.email} fue creado")
            print(f"  El bot intentará autenticarse nuevamente cuando sea necesario")
        
        print(f"✓ Correo temporal creado: {self.email}")
    
    def _generar_password(self) -> str:
        """Genera una contraseña aleatoria segura"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    
    def _obtener_dominios(self) -> List[str]:
        """
        Obtiene la lista de dominios disponibles
        
        Returns:
            Lista de dominios disponibles
        """
        try:
            response = requests.get(
                f"{self.BASE_URL}/domains",
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'hydra:member' in data:
                    # Formato Hydra
                    dominios = [item.get('domain', '') for item in data['hydra:member'] if item.get('domain')]
                elif isinstance(data, list):
                    dominios = [item.get('domain', '') for item in data if item.get('domain')]
                else:
                    dominios = []
                
                # Filtrar dominios válidos
                dominios = [d for d in dominios if d and '@' not in d]
                return dominios if dominios else ['mail.tm']  # Fallback
            else:
                return ['mail.tm']  # Fallback
        except Exception as e:
            print(f"⚠ Error al obtener dominios: {e}")
            return ['mail.tm']  # Fallback
    
    def _crear_cuenta(self) -> tuple:
        """
        Crea un email temporal usando Mail.tm API y retorna el correo y contraseña
        
        Returns:
            Tupla (email, password)
        """
        max_intentos = 3
        for intento in range(max_intentos):
            try:
                # Obtener dominios disponibles
                dominios = self._obtener_dominios()
                dominio = random.choice(dominios)
                
                # Generar nombre de usuario aleatorio
                username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
                email = f"{username}@{dominio}"
                password = self._generar_password()
                
                # Crear cuenta
                response = requests.post(
                    f"{self.BASE_URL}/accounts",
                    json={
                        "address": email,
                        "password": password
                    },
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                if response.status_code in [200, 201]:
                    data = response.json()
                    email_creado = data.get('address', email)
                    print(f"  Email creado exitosamente")
                    # Esperar un momento para que la cuenta esté lista
                    time.sleep(0.5)
                    return (email_creado, password)
                elif response.status_code == 422:
                    # Error de validación (email ya existe o formato inválido)
                    error_data = response.json() if response.text else {}
                    error_msg = error_data.get('message', response.text)
                    if intento < max_intentos - 1:
                        print(f"  ⚠ Intento {intento + 1} falló: {error_msg}, reintentando...")
                        time.sleep(1)
                        continue
                    else:
                        raise Exception(f"Error al crear email después de {max_intentos} intentos: {error_msg}")
                else:
                    error_text = response.text[:200]
                    if intento < max_intentos - 1:
                        print(f"  ⚠ Intento {intento + 1} falló (código {response.status_code}), reintentando...")
                        time.sleep(1)
                        continue
                    else:
                        raise Exception(f"Error al crear email: {response.status_code} - {error_text}")
                    
            except Exception as e:
                if intento < max_intentos - 1:
                    print(f"  ⚠ Intento {intento + 1} falló: {e}, reintentando...")
                    time.sleep(1)
                    continue
                else:
                    print(f"❌ Error con Mail.tm API después de {max_intentos} intentos: {e}")
                    import traceback
                    traceback.print_exc()
                    raise  # Re-lanzar la excepción en lugar de crear credenciales falsas
    
    def _autenticar(self) -> bool:
        """
        Autentica la cuenta y obtiene un token de acceso
        
        Returns:
            True si la autenticación fue exitosa
        """
        max_intentos = 3
        for intento in range(max_intentos):
            try:
                response = requests.post(
                    f"{self.BASE_URL}/token",
                    json={
                        "address": self.email,
                        "password": self.password
                    },
                    headers={"Content-Type": "application/json"},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.token = data.get('token')
                    if self.token:
                        return True
                    else:
                        print(f"⚠ No se recibió token en la respuesta")
                        return False
                elif response.status_code == 401:
                    error_data = response.json() if response.text else {}
                    error_msg = error_data.get('message', 'Credenciales inválidas')
                    if intento < max_intentos - 1:
                        print(f"  ⚠ Autenticación falló (401), esperando y reintentando...")
                        time.sleep(1)
                        continue
                    else:
                        print(f"⚠ Error al autenticar: 401 - {error_msg}")
                        print(f"  💡 Verifica que la cuenta se haya creado correctamente")
                        return False
                else:
                    error_text = response.text[:200] if response.text else ''
                    if intento < max_intentos - 1:
                        print(f"  ⚠ Error {response.status_code} al autenticar, reintentando...")
                        time.sleep(1)
                        continue
                    else:
                        print(f"⚠ Error al autenticar: {response.status_code} - {error_text}")
                        return False
            except Exception as e:
                if intento < max_intentos - 1:
                    print(f"  ⚠ Error al autenticar (intento {intento + 1}): {e}, reintentando...")
                    time.sleep(1)
                    continue
                else:
                    print(f"⚠ Error al autenticar después de {max_intentos} intentos: {e}")
                    return False
        return False
    
    def obtener_correos(self) -> List[Dict]:
        """
        Obtiene la lista de mensajes recibidos en el email
        
        Returns:
            Lista de mensajes recibidos
        """
        if not self.email or not self.token:
            # Intentar autenticar de nuevo si no hay token
            if not self.token:
                self._autenticar()
            if not self.token:
                return []
        
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            # Obtener mensajes
            response = requests.get(
                f"{self.BASE_URL}/messages",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                # La API de Mail.tm puede retornar en formato Hydra o directo
                if 'hydra:member' in data:
                    return data['hydra:member']
                elif isinstance(data, list):
                    return data
                elif isinstance(data, dict) and 'messages' in data:
                    return data['messages']
                return []
            elif response.status_code == 401:
                # Token expirado, intentar autenticar de nuevo
                if self._autenticar():
                    return self.obtener_correos()  # Reintentar
                return []
            else:
                return []
        except Exception as e:
            print(f"Error al obtener correos: {e}")
            return []
    
    def leer_correo(self, correo_id: str) -> Optional[Dict]:
        """
        Lee el contenido de un mensaje específico
        
        Args:
            correo_id: ID del mensaje a leer (o el mensaje completo si ya lo tenemos)
            
        Returns:
            Contenido del mensaje o None si hay error
        """
        if not self.token:
            if not self._autenticar():
                return None
        
        # Si correo_id ya es un diccionario (mensaje completo), retornarlo
        if isinstance(correo_id, dict):
            # Si ya tiene el contenido completo, retornarlo
            if 'text' in correo_id or 'html' in correo_id or 'body' in correo_id:
                return correo_id
            # Si no, obtener el ID y leerlo
            correo_id = correo_id.get('id', '')
        
        if not correo_id:
            return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            # Obtener el mensaje específico usando el ID
            response = requests.get(
                f"{self.BASE_URL}/messages/{correo_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                mensaje = response.json()
                # Asegurar que tenga los campos necesarios (normalizar nombres)
                if isinstance(mensaje, dict):
                    # Mail.tm usa 'text' y 'html', asegurar compatibilidad
                    if 'text' not in mensaje and 'body' in mensaje:
                        mensaje['text'] = mensaje['body']
                    if 'htmlBody' not in mensaje and 'html' in mensaje:
                        mensaje['htmlBody'] = mensaje['html']
                    if 'body_text' not in mensaje and 'text' in mensaje:
                        mensaje['body_text'] = mensaje['text']
                    if 'body_html' not in mensaje and 'html' in mensaje:
                        mensaje['body_html'] = mensaje['html']
                    if 'subject' not in mensaje and 'Subject' in mensaje:
                        mensaje['subject'] = mensaje['Subject']
                    # Normalizar 'from'
                    if 'from' in mensaje and isinstance(mensaje['from'], dict):
                        if 'address' not in mensaje['from'] and 'email' in mensaje['from']:
                            mensaje['from'] = {'address': mensaje['from']['email']}
                
                return mensaje
            elif response.status_code == 401:
                # Token expirado, intentar autenticar de nuevo
                if self._autenticar():
                    return self.leer_correo(correo_id)  # Reintentar
                return None
            else:
                return None
        except Exception as e:
            print(f"Error al leer correo: {e}")
            return None
    
    def esperar_correo(self, tiempo_maximo: int = 60, intervalo: int = 3) -> Optional[Dict]:
        """
        Espera a que llegue un mensaje nuevo
        
        Args:
            tiempo_maximo: Tiempo máximo de espera en segundos (default: 60)
            intervalo: Intervalo entre verificaciones en segundos (default: 3)
            
        Returns:
            Primer mensaje recibido o None si no llega ninguno
        """
        print(f"Esperando correo en {self.email} (máximo {tiempo_maximo} segundos)...")
        
        correos_iniciales = self.obtener_correos()
        ids_iniciales = set()
        for correo in correos_iniciales:
            correo_id = str(correo.get('id', '')) or str(correo.get('@id', '')) or str(correo.get('message_id', ''))
            if correo_id:
                ids_iniciales.add(correo_id)
        
        tiempo_transcurrido = 0
        
        while tiempo_transcurrido < tiempo_maximo:
            time.sleep(intervalo)
            tiempo_transcurrido += intervalo
            
            correos_actuales = self.obtener_correos()
            
            # Buscar mensajes nuevos
            for correo in correos_actuales:
                correo_id = str(correo.get('id', '')) or str(correo.get('@id', ''))
                if correo_id and correo_id not in ids_iniciales:
                    subject = correo.get('subject', correo.get('Subject', 'Sin asunto'))
                    from_addr = correo.get('from', {})
                    if isinstance(from_addr, dict):
                        from_addr = from_addr.get('address', from_addr.get('email', 'Desconocido'))
                    else:
                        from_addr = str(from_addr) if from_addr else 'Desconocido'
                    
                    print(f"✓ Correo recibido: {subject} (de: {from_addr})")
                    
                    # Si el correo ya tiene el contenido completo, retornarlo
                    if 'text' in correo or 'body' in correo or 'htmlBody' in correo or 'html' in correo:
                        return correo
                    
                    # Si no, intentar leer el contenido completo
                    correo_completo = self.leer_correo(correo_id)
                    if correo_completo:
                        return correo_completo
                    else:
                        # Si no se puede leer completo, retornar el básico
                        return correo
            
            # Mostrar progreso cada 10 segundos
            if tiempo_transcurrido % 10 == 0:
                print(f"Esperando... ({tiempo_transcurrido}/{tiempo_maximo} segundos)")
        
        print("⏱ Tiempo máximo alcanzado. No se recibió ningún correo.")
        return None
    
    def obtener_ultimo_correo(self) -> Optional[Dict]:
        """
        Obtiene el último correo recibido
        
        Returns:
            Último correo recibido o None si no hay correos
        """
        correos = self.obtener_correos()
        
        if not correos:
            return None
        
        # Ordenar por fecha (el más reciente primero)
        # Mail.tm usa 'createdAt' o '@id' para ordenar
        correos_ordenados = sorted(
            correos, 
            key=lambda x: x.get('createdAt', x.get('created_at', '')), 
            reverse=True
        )
        ultimo_correo = correos_ordenados[0]
        
        # Leer el contenido completo
        correo_id = ultimo_correo.get('id', '') or ultimo_correo.get('@id', '')
        if correo_id:
            return self.leer_correo(correo_id)
        else:
            return ultimo_correo
    
    def extraer_enlaces(self, correo: Dict) -> List[str]:
        """
        Extrae enlaces del cuerpo del correo
        
        Args:
            correo: Diccionario con el contenido del correo
            
        Returns:
            Lista de enlaces encontrados
        """
        import re
        
        enlaces = []
        texto = correo.get('text', '') + correo.get('htmlBody', '')
        
        # Buscar URLs
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        enlaces = re.findall(url_pattern, texto)
        
        return enlaces
    
    def extraer_codigo_verificacion(self, correo: Dict) -> Optional[str]:
        """
        Intenta extraer un código de verificación del correo
        Prioriza códigos de 6 dígitos
        
        Args:
            correo: Diccionario con el contenido del correo
            
        Returns:
            Código de verificación encontrado o None
        """
        import re
        
        # Obtener texto del correo de diferentes campos posibles
        texto = ""
        # Priorizar texto plano
        if 'text' in correo:
            texto += str(correo['text'])
        if 'body_text' in correo:
            texto += str(correo['body_text'])
        if 'body' in correo:
            texto += str(correo['body'])
        # Si no hay texto plano, usar HTML
        if not texto:
            if 'htmlBody' in correo:
                texto += str(correo['htmlBody'])
            if 'body_html' in correo:
                texto += str(correo['body_html'])
            if 'html' in correo:
                texto += str(correo['html'])
        if 'content' in correo:
            texto += str(correo['content'])
        
        # Limpiar HTML básico si existe
        texto = re.sub(r'<[^>]+>', ' ', texto)
        texto = re.sub(r'&nbsp;', ' ', texto)
        texto = re.sub(r'\s+', ' ', texto)
        
        print(f"  🔍 Buscando código en texto (longitud: {len(texto)} caracteres)")
        
        # PRIORIDAD 1: Buscar patrón "security code: XXXXXX" o "código de seguridad: XXXXXX"
        patrones_security_code = [
            r'security code:\s*(\d{6})',
            r'security code is:\s*(\d{6})',
            r'código de seguridad:\s*(\d{6})',
            r'código de verificación:\s*(\d{6})',
            r'verification code:\s*(\d{6})',
            r'verification code is:\s*(\d{6})',
            r'code:\s*(\d{6})',
            r'código:\s*(\d{6})',
            r'use this security code:\s*(\d{6})',
            r'use this code:\s*(\d{6})',
        ]
        
        for patron in patrones_security_code:
            match = re.search(patron, texto, re.IGNORECASE)
            if match:
                codigo = match.group(1)
                print(f"  ✓ Código encontrado con patrón '{patron}': {codigo}")
                return codigo
        
        # PRIORIDAD 2: Buscar códigos de 6 dígitos (más común para verificación)
        codigos_6 = re.findall(r'\b\d{6}\b', texto)
        if codigos_6:
            # Si hay múltiples, tomar el primero (generalmente es el código)
            codigo = codigos_6[0]
            print(f"  ✓ Código de 6 dígitos encontrado: {codigo}")
            return codigo
        
        # PRIORIDAD 2: Buscar códigos de 6 dígitos con espacios o guiones (ej: 123 456 o 123-456)
        codigo_formateado = re.search(r'\b\d{3}[\s-]?\d{3}\b', texto)
        if codigo_formateado:
            codigo = codigo_formateado.group().replace(' ', '').replace('-', '')
            print(f"  ✓ Código de 6 dígitos encontrado (formateado): {codigo}")
            return codigo
        
        # PRIORIDAD 3: Buscar códigos de 6 dígitos dentro de texto (menos estricto)
        codigo_6_flexible = re.search(r'\d{6}', texto)
        if codigo_6_flexible:
            codigo = codigo_6_flexible.group()
            print(f"  ✓ Código de 6 dígitos encontrado (flexible): {codigo}")
            return codigo
        
        # PRIORIDAD 4: Buscar códigos de 4 dígitos
        codigo_4 = re.search(r'\b\d{4}\b', texto)
        if codigo_4:
            codigo = codigo_4.group()
            print(f"  ✓ Código de 4 dígitos encontrado: {codigo}")
            return codigo
        
        # PRIORIDAD 5: Buscar códigos alfanuméricos de 6-8 caracteres
        codigo_alfa = re.search(r'\b[A-Z0-9]{6,8}\b', texto)
        if codigo_alfa:
            codigo = codigo_alfa.group()
            print(f"  ✓ Código alfanumérico encontrado: {codigo}")
            return codigo
        
        # Debug: mostrar parte del texto para ver qué hay
        print(f"  ⚠ No se encontró código. Primeros 200 caracteres del texto:")
        print(f"     {texto[:200]}")
        return None


if __name__ == "__main__":
    # Prueba del módulo
    print("Creando correo temporal...")
    correo = CorreoTemporal()
    
    print(f"\nCorreo: {correo.email}")
    print("\nEsperando correos (presiona Ctrl+C para cancelar)...")
    
    try:
        correo_recibido = correo.esperar_correo(tiempo_maximo=120)
        if correo_recibido:
            print("\n=== CONTENIDO DEL CORREO ===")
            print(f"Asunto: {correo_recibido.get('subject', 'N/A')}")
            from_addr = correo_recibido.get('from', {})
            if isinstance(from_addr, dict):
                print(f"De: {from_addr.get('address', 'N/A')}")
            else:
                print(f"De: {from_addr}")
            print(f"\nTexto:\n{correo_recibido.get('text', 'N/A')}")
            
            enlaces = correo.extraer_enlaces(correo_recibido)
            if enlaces:
                print(f"\nEnlaces encontrados: {len(enlaces)}")
                for enlace in enlaces[:5]:  # Mostrar solo los primeros 5
                    print(f"  - {enlace}")
            
            codigo = correo.extraer_codigo_verificacion(correo_recibido)
            if codigo:
                print(f"\nCódigo de verificación: {codigo}")
    except KeyboardInterrupt:
        print("\nCancelado por el usuario.")

