"""
Bot que abre la página de registro de Microsoft y genera correos temporales
Requerido: Python 3.11
"""

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.firefox import GeckoDriverManager
from correo_temporal import CorreoTemporal
import time
import sys
import random

# Intentar importar pyperclip para portapapeles
try:
    import pyperclip
    PYPERCLIP_AVAILABLE = True
except ImportError:
    PYPERCLIP_AVAILABLE = False

# Intentar importar bibliotecas para reconocimiento visual
try:
    import pyautogui
    import pytesseract
    RECONOCIMIENTO_VISUAL_AVAILABLE = True
except ImportError:
    RECONOCIMIENTO_VISUAL_AVAILABLE = False
    print("⚠ Bibliotecas de reconocimiento visual no disponibles.")
    print("   Instala: pip install pyautogui pytesseract pillow")
    print("   También necesitas instalar Tesseract OCR")


class BotRegistroMicrosoft:
    """
    Bot para registro de Microsoft con correos temporales
    """
    
    def __init__(self, usar_reconocimiento: bool = True, posicion_x: int = 0, posicion_y: int = 0):
        """
        Inicializa el bot
        
        Args:
            usar_reconocimiento: Si es True, usa reconocimiento visual para encontrar el campo
            posicion_x: Coordeada X donde hacer clic (0 = no usar, solo si usar_reconocimiento=False)
            posicion_y: Coordenada Y donde hacer clic (0 = no usar, solo si usar_reconocimiento=False)
        """
        self.driver = None
        self.correo_temporal = None
        self.usar_reconocimiento = usar_reconocimiento and RECONOCIMIENTO_VISUAL_AVAILABLE
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        self.cuentas_creadas = 0
    
    def inicializar_navegador(self) -> None:
        """Inicializa el navegador Firefox sin mostrar que es automatizado"""
        firefox_options = Options()
        
        # Modo privado (incógnito)
        firefox_options.add_argument("--private")
        
        # TÉCNICAS AVANZADAS PARA OCULTAR AUTOMATIZACIÓN
        # Deshabilitar completamente el indicador de webdriver
        firefox_options.set_preference("dom.webdriver.enabled", False)
        firefox_options.set_preference("useAutomationExtension", False)
        
        # Ocultar marionette (sistema de automatización de Firefox)
        firefox_options.set_preference("marionette.enabled", True)  # Necesario para Selenium, pero lo ocultamos
        
        # Deshabilitar notificaciones de automatización
        firefox_options.set_preference("dom.disable_beforeunload", True)
        firefox_options.set_preference("dom.disable_window_move_resize", True)
        firefox_options.set_preference("dom.disable_window_open_feature.close", True)
        
        # Preferencias para parecer más humano
        firefox_options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0")
        firefox_options.set_preference("dom.webnotifications.enabled", False)
        firefox_options.set_preference("media.navigator.enabled", False)
        firefox_options.set_preference("media.peerconnection.enabled", False)
        firefox_options.set_preference("privacy.trackingprotection.enabled", False)
        firefox_options.set_preference("browser.safebrowsing.malware.enabled", False)
        firefox_options.set_preference("browser.safebrowsing.phishing.enabled", False)
        
        # Deshabilitar logs y señales de automatización
        firefox_options.set_preference("devtools.console.stdout.enabled", False)
        firefox_options.set_preference("devtools.console.stdout.chrome", False)
        firefox_options.log.level = "fatal"
        
        # Ocultar indicadores de automatización en la UI
        firefox_options.set_preference("toolkit.telemetry.enabled", False)
        firefox_options.set_preference("toolkit.telemetry.server", "")
        firefox_options.set_preference("datareporting.policy.dataSubmissionEnabled", False)
        firefox_options.set_preference("datareporting.healthreport.uploadEnabled", False)
        
        try:
            # Configurar el servicio para minimizar señales
            service = FirefoxService(GeckoDriverManager().install())
            
            self.driver = webdriver.Firefox(service=service, options=firefox_options)
            
            # Scripts avanzados para ocultar automatización en Firefox
            stealth_script = '''
                (function() {
                    // TÉCNICA 1: Eliminar webdriver completamente
                    try {
                        delete Object.getPrototypeOf(navigator).webdriver;
                    } catch(e) {}
                    
                    // TÉCNICA 2: Redefinir webdriver como undefined
                    try {
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined,
                            configurable: true,
                            enumerable: false
                        });
                    } catch(e) {
                        try {
                            navigator.webdriver = undefined;
                        } catch(e2) {}
                    }
                    
                    // TÉCNICA 3: Ocultar marionette
                    try {
                        Object.defineProperty(navigator, 'marionette', {
                            get: () => undefined,
                            configurable: true
                        });
                    } catch(e) {}
                    
                    // TÉCNICA 4: Ocultar permisos
                    const originalQuery = window.navigator.permissions.query;
                    if (originalQuery) {
                        window.navigator.permissions.query = (parameters) => (
                            parameters.name === 'notifications' ?
                                Promise.resolve({ state: Notification.permission }) :
                                originalQuery(parameters)
                        );
                    }
                    
                    // TÉCNICA 5: Simular plugins reales
                    try {
                        Object.defineProperty(navigator, 'plugins', {
                            get: () => {
                                const plugins = [];
                                for (let i = 0; i < 5; i++) {
                                    plugins.push({
                                        name: `Plugin ${i}`,
                                        description: `Description ${i}`,
                                        filename: `plugin${i}.dll`
                                    });
                                }
                                return plugins;
                            },
                            configurable: true
                        });
                    } catch(e) {}
                    
                    // TÉCNICA 6: Simular lenguajes
                    try {
                        Object.defineProperty(navigator, 'languages', {
                            get: () => ['en-US', 'en'],
                            configurable: true
                        });
                    } catch(e) {}
                    
                    // TÉCNICA 7: Simular conexión
                    try {
                        Object.defineProperty(navigator, 'connection', {
                            get: () => ({
                                rtt: 50,
                                downlink: 10,
                                effectiveType: '4g',
                                saveData: false
                            }),
                            configurable: true
                        });
                    } catch(e) {}
                    
                    // TÉCNICA 8: Ocultar señales de Selenium en window
                    try {
                        delete window.__selenium_unwrapped;
                        delete window.__selenium_evaluate;
                        delete window.__fxdriver_evaluate;
                        delete window.__driver_evaluate;
                        delete window.__webdriver_evaluate;
                        delete window.__selenium_unwrapped;
                        delete window.__fxdriver_unwrapped;
                        delete window.__driver_unwrapped;
                        delete window.__webdriver_unwrapped;
                    } catch(e) {}
                    
                    // TÉCNICA 9: Ocultar document.$cdc_ y document.$chrome_async
                    try {
                        Object.defineProperty(document, '$cdc_', {
                            get: () => undefined,
                            configurable: true
                        });
                        Object.defineProperty(document, '$chrome_async', {
                            get: () => undefined,
                            configurable: true
                        });
                    } catch(e) {}
                    
                    // TÉCNICA 10: Ocultar en document
                    try {
                        delete document.$cdc_asdjflasutopfhvcZLmcfl_;
                        delete document.$chrome_asyncScriptInfo;
                    } catch(e) {}
                })();
            '''
            
            # Ejecutar script de stealth ANTES de cargar cualquier página
            # También lo ejecutaremos después de cada navegación
            try:
                self.driver.execute_script(stealth_script)
            except:
                pass  # Si falla, continuar
            
            print(f"✓ Navegador Firefox inicializado en modo STEALTH")
        except Exception as e:
            print(f"Error al inicializar el navegador: {e}")
            raise
    
    def _ejecutar_stealth_script(self) -> None:
        """Ejecuta el script de stealth en la página actual (para Firefox)"""
        try:
            stealth_script = '''
                (function() {
                    // TÉCNICA 1: Eliminar webdriver completamente
                    try {
                        delete Object.getPrototypeOf(navigator).webdriver;
                    } catch(e) {}
                    
                    // TÉCNICA 2: Redefinir webdriver como undefined
                    try {
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined,
                            configurable: true,
                            enumerable: false
                        });
                    } catch(e) {
                        try {
                            navigator.webdriver = undefined;
                        } catch(e2) {}
                    }
                    
                    // TÉCNICA 3: Ocultar marionette
                    try {
                        Object.defineProperty(navigator, 'marionette', {
                            get: () => undefined,
                            configurable: true
                        });
                    } catch(e) {}
                    
                    // TÉCNICA 4: Ocultar permisos
                    const originalQuery = window.navigator.permissions.query;
                    if (originalQuery) {
                        window.navigator.permissions.query = (parameters) => (
                            parameters.name === 'notifications' ?
                                Promise.resolve({ state: Notification.permission }) :
                                originalQuery(parameters)
                        );
                    }
                    
                    // TÉCNICA 5: Simular plugins reales
                    try {
                        Object.defineProperty(navigator, 'plugins', {
                            get: () => {
                                const plugins = [];
                                for (let i = 0; i < 5; i++) {
                                    plugins.push({
                                        name: `Plugin ${i}`,
                                        description: `Description ${i}`,
                                        filename: `plugin${i}.dll`
                                    });
                                }
                                return plugins;
                            },
                            configurable: true
                        });
                    } catch(e) {}
                    
                    // TÉCNICA 6: Simular lenguajes
                    try {
                        Object.defineProperty(navigator, 'languages', {
                            get: () => ['en-US', 'en'],
                            configurable: true
                        });
                    } catch(e) {}
                    
                    // TÉCNICA 7: Simular conexión
                    try {
                        Object.defineProperty(navigator, 'connection', {
                            get: () => ({
                                rtt: 50,
                                downlink: 10,
                                effectiveType: '4g',
                                saveData: false
                            }),
                            configurable: true
                        });
                    } catch(e) {}
                    
                    // TÉCNICA 8: Ocultar señales de Selenium en window
                    try {
                        delete window.__selenium_unwrapped;
                        delete window.__selenium_evaluate;
                        delete window.__fxdriver_evaluate;
                        delete window.__driver_evaluate;
                        delete window.__webdriver_evaluate;
                        delete window.__selenium_unwrapped;
                        delete window.__fxdriver_unwrapped;
                        delete window.__driver_unwrapped;
                        delete window.__webdriver_unwrapped;
                    } catch(e) {}
                    
                    // TÉCNICA 9: Ocultar document.$cdc_ y document.$chrome_async
                    try {
                        Object.defineProperty(document, '$cdc_', {
                            get: () => undefined,
                            configurable: true
                        });
                        Object.defineProperty(document, '$chrome_async', {
                            get: () => undefined,
                            configurable: true
                        });
                    } catch(e) {}
                    
                    // TÉCNICA 10: Ocultar en document
                    try {
                        delete document.$cdc_asdjflasutopfhvcZLmcfl_;
                        delete document.$chrome_asyncScriptInfo;
                    } catch(e) {}
                })();
            '''
            self.driver.execute_script(stealth_script)
        except:
            pass  # Si falla, continuar sin el script
    
    def _delay_aleatorio(self, min_sec: float = 0.5, max_sec: float = 2.0) -> None:
        """
        Espera un tiempo aleatorio para simular comportamiento humano
        
        Args:
            min_sec: Tiempo mínimo en segundos
            max_sec: Tiempo máximo en segundos
        """
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)
    
    def _simular_movimiento_mouse(self, elemento) -> None:
        """
        Simula movimiento del mouse hacia un elemento de forma humana
        """
        try:
            # Mover el mouse al elemento de forma suave
            actions = ActionChains(self.driver)
            actions.move_to_element(elemento)
            self._delay_aleatorio(0.1, 0.3)
            actions.perform()
        except:
            pass
    
    def crear_correo_temporal(self) -> str:
        """Crea un correo temporal y lo retorna"""
        self.correo_temporal = CorreoTemporal()
        return self.correo_temporal.email
    
    def abrir_registro_microsoft(self) -> None:
        """Abre la página de registro de Microsoft"""
        if not self.driver:
            self.inicializar_navegador()
        
        self.url_registro = "https://signup.live.com/signup?contextid=D211B384E9EB2FFC&opid=408B0DB90A982CE4&bk=1764613783&sru=https://login.live.com/oauth20_authorize.srf%3fclient_id%3d1f907974-e22b-4810-a9de-d9647380c97e%26client_id%3d1f907974-e22b-4810-a9de-d9647380c97e%26contextid%3dD211B384E9EB2FFC%26opid%3d408B0DB90A982CE4%26mkt%3dEN-US%26lc%3d1033%26bk%3d1764613783%26uaid%3d236c1c5e03ad4d18962ca0f33056a226&uiflavor=web&fluent=2&client_id=000000004C5BC0A9&lic=1&mkt=EN-US&lc=1033&uaid=236c1c5e03ad4d18962ca0f33056a226"
        
        print("Abriendo página de registro de Microsoft...")
        self.driver.get(self.url_registro)
        self._ejecutar_stealth_script()
        
        # Esperar a que la página cargue completamente con delay aleatorio
        self._delay_aleatorio(3, 5)
        print("✓ Página de registro abierta")
    
    def mostrar_correo_temporal(self) -> None:
        """Muestra el correo temporal en la consola"""
        if self.correo_temporal:
            print("\n" + "="*60)
            print(f"CORREO TEMPORAL DISPONIBLE: {self.correo_temporal.email}")
            print("="*60)
            print("\nPuedes usar este correo para el registro de Microsoft.")
            print("El bot está listo para recibir correos.\n")
    
    def encontrar_campo_por_reconocimiento_visual(self) -> tuple | None:
        """
        Encuentra el campo de correo usando reconocimiento visual
        
        Returns:
            Tupla (x, y) con las coordenadas del campo, o None si no se encuentra
        """
        if not RECONOCIMIENTO_VISUAL_AVAILABLE:
            print("⚠ Reconocimiento visual no disponible")
            return None
        
        try:
            print("\n🔍 Buscando campo 'Correo electrónico' usando reconocimiento visual...")
            time.sleep(1)  # Esperar a que la página esté completamente cargada
            
            # Método 1: Buscar el campo usando Selenium (MÁS PRECISO)
            # Buscar primero por label "Correo electrónico" y luego el input asociado
            try:
                print("Buscando por label 'Correo electrónico'...")
                labels = self.driver.find_elements(By.XPATH, "//label[contains(text(), 'Correo electrónico')]")
                
                if not labels:
                    labels = self.driver.find_elements(By.XPATH, "//label[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'correo electrónico')]")
                
                for label in labels:
                    if label.is_displayed():
                        # Buscar input asociado
                        label_for = label.get_attribute('for')
                        if label_for:
                            try:
                                inp = self.driver.find_element(By.ID, label_for)
                                if inp.is_displayed():
                                    location = inp.location
                                    size = inp.size
                                    centro_x = location['x'] + (size['width'] // 2)
                                    centro_y = location['y'] + (size['height'] // 2)
                                    
                                    window_pos = self.driver.get_window_position()
                                    screen_x = window_pos['x'] + centro_x + 8
                                    screen_y = window_pos['y'] + centro_y + 80
                                    
                                    print(f"✓ Campo encontrado por label 'for': ({screen_x}, {screen_y})")
                                    return (screen_x, screen_y)
                            except:
                                pass
                        
                        # Buscar input siguiente
                        try:
                            inp = label.find_element(By.XPATH, "./following-sibling::input[1]")
                            if inp.is_displayed():
                                location = inp.location
                                size = inp.size
                                centro_x = location['x'] + (size['width'] // 2)
                                centro_y = location['y'] + (size['height'] // 2)
                                
                                window_pos = self.driver.get_window_position()
                                screen_x = window_pos['x'] + centro_x + 8
                                screen_y = window_pos['y'] + centro_y + 80
                                
                                print(f"✓ Campo encontrado como siguiente del label: ({screen_x}, {screen_y})")
                                return (screen_x, screen_y)
                        except:
                            pass
            except Exception as e:
                print(f"⚠ Error buscando por label: {e}")
            
            # Método 2: Buscar primer input de tipo email o text visible
            try:
                print("Buscando primer input de tipo email/text...")
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                
                for inp in inputs:
                    if inp.is_displayed() and inp.is_enabled():
                        tipo = inp.get_attribute('type') or 'text'
                        nombre = inp.get_attribute('name') or ''
                        id_attr = inp.get_attribute('id') or ''
                        
                        # Priorizar inputs de tipo email o que parezcan ser de correo
                        if tipo == 'email' or 'email' in nombre.lower() or 'email' in id_attr.lower() or 'member' in nombre.lower():
                            location = inp.location
                            size = inp.size
                            
                            # Calcular centro del campo
                            centro_x = location['x'] + (size['width'] // 2)
                            centro_y = location['y'] + (size['height'] // 2)
                            
                            # Verificar que esté en el viewport visible
                            if location['y'] > 0 and location['y'] < 2000:
                                window_pos = self.driver.get_window_position()
                                screen_x = window_pos['x'] + centro_x + 8
                                screen_y = window_pos['y'] + centro_y + 80
                                
                                print(f"✓ Campo encontrado (tipo {tipo}): ({screen_x}, {screen_y})")
                                return (screen_x, screen_y)
                
                # Si no encontramos uno específico, buscar el primer input text vacío
                for inp in inputs:
                    if inp.is_displayed() and inp.is_enabled():
                        tipo = inp.get_attribute('type') or 'text'
                        valor = inp.get_attribute('value') or ''
                        
                        if tipo == 'text' and not valor:
                            location = inp.location
                            if location['y'] > 0 and location['y'] < 2000:
                                size = inp.size
                                centro_x = location['x'] + (size['width'] // 2)
                                centro_y = location['y'] + (size['height'] // 2)
                                
                                window_pos = self.driver.get_window_position()
                                screen_x = window_pos['x'] + centro_x + 8
                                screen_y = window_pos['y'] + centro_y + 80
                                
                                print(f"✓ Campo encontrado (primer input text vacío): ({screen_x}, {screen_y})")
                                return (screen_x, screen_y)
                                
            except Exception as e:
                print(f"⚠ Error buscando inputs: {e}")
            
        except Exception as e:
            print(f"⚠ Error en reconocimiento visual: {e}")
            import traceback
            traceback.print_exc()
        
        return None
    
    def _pegar_correo_selenium_directo(self, correo: str) -> bool:
        """
        Encuentra el campo usando Selenium y pega el correo directamente (MÁS CONFIABLE)
        
        Args:
            correo: Correo a pegar
            
        Returns:
            True si se pegó exitosamente
        """
        try:
            print("\n🔍 Buscando campo usando Selenium directo...")
            time.sleep(1)  # Esperar a que la página cargue completamente
            
            campo = None
            
            # Método 1: Buscar input de tipo email específicamente
            try:
                inputs_email = self.driver.find_elements(By.CSS_SELECTOR, "input[type='email']")
                for inp in inputs_email:
                    if inp.is_displayed() and inp.is_enabled():
                        # Verificar que esté en el área principal del formulario
                        location = inp.location
                        if location['y'] > 100 and location['y'] < 1000:  # Filtrar campos fuera del área principal
                            campo = inp
                            print("✓ Campo encontrado: input[type='email']")
                            break
            except Exception as e:
                print(f"⚠ Error buscando input[type='email']: {e}")
            
            # Método 2: Buscar por label "Correo electrónico" y encontrar el input asociado
            if not campo:
                try:
                    # Buscar label con texto exacto o similar
                    labels = self.driver.find_elements(By.XPATH, "//label[contains(text(), 'Correo electrónico') or contains(text(), 'correo electrónico')]")
                    
                    for label in labels:
                        if label.is_displayed():
                            # Buscar por atributo 'for'
                            label_for = label.get_attribute('for')
                            if label_for:
                                try:
                                    inp = self.driver.find_element(By.ID, label_for)
                                    if inp.is_displayed() and inp.is_enabled():
                                        location = inp.location
                                        if location['y'] > 100:
                                            campo = inp
                                            print("✓ Campo encontrado por label 'for'")
                                            break
                                except:
                                    pass
                            
                            # Buscar input siguiente al label
                            try:
                                # Buscar en el mismo contenedor padre
                                parent = label.find_element(By.XPATH, "./..")
                                inp = parent.find_element(By.TAG_NAME, "input")
                                if inp.is_displayed() and inp.is_enabled():
                                    location = inp.location
                                    if location['y'] > 100:
                                        campo = inp
                                        print("✓ Campo encontrado en contenedor del label")
                                        break
                            except:
                                pass
                            
                            # Buscar input siguiente hermano
                            try:
                                inp = self.driver.find_element(By.XPATH, f"//label[contains(text(), 'Correo electrónico')]/following::input[1]")
                                if inp.is_displayed() and inp.is_enabled():
                                    location = inp.location
                                    if location['y'] > 100:
                                        campo = inp
                                        print("✓ Campo encontrado como siguiente del label")
                                        break
                            except:
                                pass
                except Exception as e:
                    print(f"⚠ Error buscando por label: {e}")
            
            # Método 3: Buscar input con atributos específicos de Microsoft
            if not campo:
                try:
                    inputs = self.driver.find_elements(By.TAG_NAME, "input")
                    for inp in inputs:
                        if inp.is_displayed() and inp.is_enabled():
                            tipo = inp.get_attribute('type') or 'text'
                            nombre = inp.get_attribute('name') or ''
                            id_attr = inp.get_attribute('id') or ''
                            placeholder = inp.get_attribute('placeholder') or ''
                            
                            location = inp.location
                            
                            # Filtrar solo campos en el área principal y que parezcan ser de email
                            if location['y'] > 100 and location['y'] < 1000:
                                if (tipo == 'email' or 
                                    'email' in nombre.lower() or 
                                    'email' in id_attr.lower() or 
                                    'membername' in nombre.lower() or
                                    'email' in placeholder.lower()):
                                    campo = inp
                                    print(f"✓ Campo encontrado por atributos: type={tipo}, name={nombre}")
                                    break
                except Exception as e:
                    print(f"⚠ Error buscando por atributos: {e}")
            
            # Método 4: Buscar el primer input text vacío en el área principal
            if not campo:
                try:
                    inputs = self.driver.find_elements(By.TAG_NAME, "input")
                    for inp in inputs:
                        if inp.is_displayed() and inp.is_enabled():
                            tipo = inp.get_attribute('type') or 'text'
                            valor = inp.get_attribute('value') or ''
                            location = inp.location
                            
                            # Solo campos text vacíos en el área principal
                            if tipo == 'text' and not valor and location['y'] > 100 and location['y'] < 1000:
                                campo = inp
                                print("✓ Campo encontrado (primer input text vacío en área principal)")
                                break
                except Exception as e:
                    print(f"⚠ Error buscando primer input: {e}")
            
            if campo:
                # Copiar al portapapeles
                if PYPERCLIP_AVAILABLE:
                    pyperclip.copy(correo)
                    print("✓ Correo copiado al portapapeles")
                else:
                    self.driver.execute_script(f"navigator.clipboard.writeText('{correo}');")
                    time.sleep(0.3)
                    print("✓ Correo copiado al portapapeles (JavaScript)")
                
                # Simular movimiento del mouse hacia el campo
                self._simular_movimiento_mouse(campo)
                self._delay_aleatorio(0.2, 0.5)
                
                # Hacer scroll al campo para asegurar que esté visible
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", campo)
                self._delay_aleatorio(0.3, 0.7)
                
                # Enfocar el campo primero
                self.driver.execute_script("arguments[0].focus();", campo)
                self._delay_aleatorio(0.2, 0.4)
                
                # Hacer clic en el campo
                campo.click()
                self._delay_aleatorio(0.3, 0.6)
                
                # Limpiar cualquier contenido existente
                campo.clear()
                self._delay_aleatorio(0.1, 0.3)
                
                # Escribir directamente con velocidad humana (carácter por carácter con delays)
                for char in correo:
                    campo.send_keys(char)
                    # Delay aleatorio entre caracteres para simular escritura humana
                    self._delay_aleatorio(0.05, 0.15)
                
                self._delay_aleatorio(0.3, 0.6)
                
                # Verificar que se escribió correctamente
                valor = campo.get_attribute('value') or ''
                if correo in valor or valor == correo:
                    print(f"✓✓ Correo escrito exitosamente: {correo}")
                    
                    # Presionar Tab una vez y luego Enter con delays humanos
                    print("Presionando Tab y luego Enter...")
                    actions = ActionChains(self.driver)
                    actions.send_keys(Keys.TAB).perform()
                    self._delay_aleatorio(0.2, 0.5)
                    actions.send_keys(Keys.ENTER).perform()
                    self._delay_aleatorio(0.8, 1.5)
                    print("✓✓ Tab y Enter presionados")
                    
                    return True
                else:
                    # Intentar pegar como respaldo
                    print("⚠ Escribir directo falló, intentando pegar...")
                    campo.clear()
                    time.sleep(0.2)
                    actions = ActionChains(self.driver)
                    actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                    time.sleep(0.5)
                    
                    valor = campo.get_attribute('value') or ''
                    if correo in valor or valor == correo:
                        print(f"✓✓ Correo pegado exitosamente: {correo}")
                        
                        # Presionar Tab una vez y luego Enter
                        print("Presionando Tab y luego Enter...")
                        actions = ActionChains(self.driver)
                        actions.send_keys(Keys.TAB).perform()
                        time.sleep(0.3)
                        actions.send_keys(Keys.ENTER).perform()
                        time.sleep(1)
                        print("✓✓ Tab y Enter presionados")
                        
                        return True
            
            print("⚠ No se encontró el campo de correo")
            return False
            
        except Exception as e:
            print(f"⚠ Error en método Selenium directo: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _clic_boton_siguiente(self) -> None:
        """
        Busca y hace clic en el botón "Siguiente" usando múltiples métodos
        """
        try:
            print("\n🔍 Buscando botón 'Siguiente'...")
            time.sleep(2)  # Esperar un momento después de pegar el correo
            
            # Método 0: Buscar botón verde con texto "Next" o "Siguiente"
            try:
                print("Buscando botón verde con texto 'Next'...")
                botones = self.driver.find_elements(By.TAG_NAME, "button")
                boton_verde_next = None
                
                for btn in botones:
                    if btn.is_displayed() and btn.is_enabled():
                        texto = btn.text.strip()
                        texto_lower = texto.lower()
                        
                        # Buscar botones con texto "Next" o "Siguiente"
                        if "next" in texto_lower or "siguiente" in texto_lower:
                            # Obtener el color de fondo del botón
                            color_fondo = btn.value_of_css_property("background-color")
                            clases = btn.get_attribute("class") or ""
                            
                            # Verificar si es verde
                            es_verde = False
                            
                            if color_fondo:
                                # Verificar RGB
                                import re
                                rgb_match = re.search(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', color_fondo)
                                if rgb_match:
                                    r, g, b = int(rgb_match.group(1)), int(rgb_match.group(2)), int(rgb_match.group(3))
                                    # Verde: G debe ser mayor que R y B, y G > 100
                                    if g > r and g > b and g > 100:
                                        es_verde = True
                                        print(f"  Botón encontrado: '{texto}' con color RGB({r}, {g}, {b})")
                                elif "#" in color_fondo.lower() or "green" in color_fondo.lower():
                                    es_verde = True
                                    print(f"  Botón encontrado: '{texto}' con color {color_fondo}")
                            
                            # También buscar por clases
                            if "green" in clases.lower() or "primary" in clases.lower():
                                es_verde = True
                                print(f"  Botón encontrado: '{texto}' con clases {clases}")
                            
                            # Si es verde o si es el único botón con "Next", usarlo
                            if es_verde or boton_verde_next is None:
                                boton_verde_next = btn
                
                if boton_verde_next:
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", boton_verde_next)
                    time.sleep(0.5)
                    boton_verde_next.click()
                    print(f"✓✓ Clic en botón verde '{boton_verde_next.text}'")
                    time.sleep(1)
                    return
            except Exception as e:
                print(f"⚠ Método 0 (botón verde Next) falló: {e}")
                import traceback
                traceback.print_exc()
            
            # Método 0.1: Buscar cualquier botón con texto "Next"
            try:
                print("Buscando botón con texto 'Next'...")
                botones = self.driver.find_elements(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'next')]")
                for boton in botones:
                    if boton.is_displayed() and boton.is_enabled():
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", boton)
                        time.sleep(0.5)
                        boton.click()
                        print(f"✓✓ Clic en botón 'Next': '{boton.text}'")
                        time.sleep(1)
                        return
            except Exception as e:
                print(f"⚠ Método 0.1 (Next) falló: {e}")
            
            # Método 0.5: Buscar el único botón visible en la pantalla
            try:
                print("Buscando único botón visible...")
                botones = self.driver.find_elements(By.TAG_NAME, "button")
                botones_visibles = [btn for btn in botones if btn.is_displayed() and btn.is_enabled()]
                
                if len(botones_visibles) == 1:
                    boton = botones_visibles[0]
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", boton)
                    time.sleep(0.5)
                    boton.click()
                    print("✓✓ Clic en único botón visible")
                    time.sleep(1)
                    return
            except Exception as e:
                print(f"⚠ Método 0.5 (único botón) falló: {e}")
            
            # Método 1: Buscar botón por texto "Siguiente" (más específico)
            try:
                botones = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Siguiente')]")
                for boton in botones:
                    if boton.is_displayed() and boton.is_enabled():
                        # Hacer scroll al botón
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", boton)
                        time.sleep(0.5)
                        boton.click()
                        print("✓✓ Clic en botón 'Siguiente' (por texto)")
                        time.sleep(1)
                        return
            except Exception as e:
                print(f"⚠ Método 1 falló: {e}")
            
            # Método 2: Buscar por texto case-insensitive
            try:
                botones = self.driver.find_elements(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'siguiente')]")
                for boton in botones:
                    if boton.is_displayed() and boton.is_enabled():
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", boton)
                        time.sleep(0.5)
                        boton.click()
                        print("✓✓ Clic en botón 'Siguiente' (case-insensitive)")
                        time.sleep(1)
                        return
            except Exception as e:
                print(f"⚠ Método 2 falló: {e}")
            
            # Método 3: Buscar input de tipo submit
            try:
                botones = self.driver.find_elements(By.CSS_SELECTOR, "input[type='submit']")
                for boton in botones:
                    if boton.is_displayed() and boton.is_enabled():
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", boton)
                        time.sleep(0.5)
                        boton.click()
                        print("✓✓ Clic en botón submit")
                        time.sleep(1)
                        return
            except Exception as e:
                print(f"⚠ Método 3 falló: {e}")
            
            # Método 4: Buscar botones de tipo submit
            try:
                botones = self.driver.find_elements(By.CSS_SELECTOR, "button[type='submit']")
                for btn in botones:
                    if btn.is_displayed() and btn.is_enabled():
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", btn)
                        time.sleep(0.5)
                        btn.click()
                        print("✓✓ Clic en botón submit")
                        time.sleep(1)
                        return
            except Exception as e:
                print(f"⚠ Método 4 falló: {e}")
            
            # Método 5: Buscar todos los botones y filtrar por texto
            try:
                botones = self.driver.find_elements(By.TAG_NAME, "button")
                for btn in botones:
                    if btn.is_displayed() and btn.is_enabled():
                        texto = btn.text.strip().lower()
                        if 'siguiente' in texto or 'next' in texto:
                            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", btn)
                            time.sleep(0.5)
                            btn.click()
                            print(f"✓✓ Clic en botón con texto: '{btn.text}'")
                            time.sleep(1)
                            return
            except Exception as e:
                print(f"⚠ Método 5 falló: {e}")
            
            # Método 6: Usar JavaScript para hacer clic
            try:
                botones = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'Siguiente')]")
                for boton in botones:
                    if boton.is_displayed():
                        self.driver.execute_script("arguments[0].click();", boton)
                        print("✓✓ Clic en botón usando JavaScript")
                        time.sleep(1)
                        return
            except Exception as e:
                print(f"⚠ Método 6 falló: {e}")
            
            # Método 7: Usar reconocimiento visual con pyautogui
            if RECONOCIMIENTO_VISUAL_AVAILABLE:
                try:
                    botones = self.driver.find_elements(By.TAG_NAME, "button")
                    for btn in botones:
                        if btn.is_displayed():
                            texto = btn.text.strip().lower()
                            if 'siguiente' in texto or 'next' in texto or btn.get_attribute('type') == 'submit':
                                location = btn.location
                                size = btn.size
                                centro_x = location['x'] + (size['width'] // 2)
                                centro_y = location['y'] + (size['height'] // 2)
                                
                                window_pos = self.driver.get_window_position()
                                screen_x = window_pos['x'] + centro_x + 8
                                screen_y = window_pos['y'] + centro_y + 80
                                
                                pyautogui.click(screen_x, screen_y)
                                print(f"✓✓ Clic en botón usando pyautogui: ({screen_x}, {screen_y})")
                                time.sleep(1)
                                return
                except Exception as e:
                    print(f"⚠ Método 7 falló: {e}")
            
            # Método 8: Presionar Enter (último recurso)
            try:
                print("Intentando presionar Enter...")
                actions = ActionChains(self.driver)
                actions.send_keys(Keys.ENTER).perform()
                time.sleep(1)
                print("✓✓ Presionado Enter")
                return
            except Exception as e:
                print(f"⚠ Método 8 falló: {e}")
            
            print("⚠ No se encontró el botón 'Siguiente' automáticamente")
            print("💡 Puedes hacer clic manualmente en el botón 'Siguiente'")
            
        except Exception as e:
            print(f"⚠ Error al buscar botón 'Siguiente': {e}")
            import traceback
            traceback.print_exc()
    
    def _esperar_y_pegar_codigo_verificacion(self) -> None:
        """
        Espera a recibir el correo de verificación, extrae el código y lo pega
        """
        if not self.correo_temporal:
            print("⚠ No hay correo temporal configurado")
            return
        
        try:
            print("\n📧 Esperando correo de verificación...")
            print(f"   Correo: {self.correo_temporal.email}")
            correo_recibido = self.correo_temporal.esperar_correo(tiempo_maximo=120, intervalo=3)
            
            if correo_recibido:
                print("✓ Correo recibido")
                
                # Mostrar información del correo recibido
                print("\n" + "="*60)
                print("📧 CORREO RECIBIDO:")
                print("="*60)
                subject = correo_recibido.get('subject', correo_recibido.get('Subject', 'Sin asunto'))
                print(f"Asunto: {subject}")
                
                from_addr = correo_recibido.get('from', {})
                if isinstance(from_addr, dict):
                    from_addr = from_addr.get('address', from_addr.get('email', 'Desconocido'))
                else:
                    from_addr = str(from_addr) if from_addr else 'Desconocido'
                print(f"De: {from_addr}")
                
                # Mostrar parte del contenido
                texto = correo_recibido.get('text', '') or correo_recibido.get('body', '')
                if texto:
                    texto_preview = texto[:300] if len(texto) > 300 else texto
                    print(f"\nContenido (primeros 300 caracteres):")
                    print(f"{texto_preview}")
                    if len(texto) > 300:
                        print("...")
                print("="*60 + "\n")
                
                # Extraer código de verificación (prioriza 6 dígitos)
                print("🔍 Extrayendo código de verificación del correo...")
                codigo = self.correo_temporal.extraer_codigo_verificacion(correo_recibido)
                
                if codigo:
                    print(f"\n{'='*60}")
                    print(f"✓✓ CÓDIGO DE VERIFICACIÓN ENCONTRADO: {codigo}")
                    print(f"{'='*60}\n")
                    
                    # Copiar al portapapeles
                    if PYPERCLIP_AVAILABLE:
                        pyperclip.copy(codigo)
                        print(f"📋 Código copiado al portapapeles: {codigo}")
                    else:
                        self.driver.execute_script(f"navigator.clipboard.writeText('{codigo}');")
                        time.sleep(0.3)
                        print(f"📋 Código copiado al portapapeles (JavaScript): {codigo}")
                    
                    # Buscar campo de código y pegarlo
                    self._pegar_codigo_verificacion(codigo)
                    
                    # Verificar error antes de continuar
                    time.sleep(1)
                    if self._detectar_error_cuenta():
                        print("⚠ Error detectado después de pegar código, abortando...")
                        return
                    
                    # Después de pegar el código, completar los datos personales
                    self._completar_datos_personales()
                    
                    # Verificar error después de completar datos
                    time.sleep(1)
                    if self._detectar_error_cuenta():
                        print("⚠ Error detectado después de completar datos, abortando...")
                        return
                else:
                    print("⚠ No se pudo extraer el código de verificación del correo")
                    print("Intentando buscar enlaces en el correo...")
                    enlaces = self.correo_temporal.extraer_enlaces(correo_recibido)
                    if enlaces:
                        print(f"Enlaces encontrados: {enlaces[:3]}")
            else:
                print("⚠ No se recibió ningún correo en el tiempo esperado")
                
        except Exception as e:
            print(f"⚠ Error al esperar correo: {e}")
            import traceback
            traceback.print_exc()
    
    def _pegar_codigo_verificacion(self, codigo: str) -> None:
        """
        Busca el campo de código de verificación y pega el código
        
        Args:
            codigo: Código de verificación a pegar
        """
        try:
            print(f"\n🔍 Buscando campo para código de verificación...")
            time.sleep(2)  # Esperar a que aparezca el campo
            
            campo = None
            
            # Método 1: Buscar input de tipo text o number
            try:
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                for inp in inputs:
                    if inp.is_displayed() and inp.is_enabled():
                        tipo = inp.get_attribute('type') or 'text'
                        nombre = inp.get_attribute('name') or ''
                        id_attr = inp.get_attribute('id') or ''
                        placeholder = inp.get_attribute('placeholder') or ''
                        
                        # Buscar campos relacionados con código, verificación, OTP
                        if (tipo in ['text', 'number', 'tel'] and 
                            ('code' in nombre.lower() or 'verification' in nombre.lower() or 
                             'otp' in nombre.lower() or 'code' in id_attr.lower() or
                             'code' in placeholder.lower() or 'código' in placeholder.lower())):
                            campo = inp
                            print(f"✓ Campo encontrado por atributos: {nombre or id_attr}")
                            break
            except Exception as e:
                print(f"⚠ Error buscando por atributos: {e}")
            
            # Método 2: Buscar primer input vacío visible
            if not campo:
                try:
                    inputs = self.driver.find_elements(By.TAG_NAME, "input")
                    for inp in inputs:
                        if inp.is_displayed() and inp.is_enabled():
                            tipo = inp.get_attribute('type') or 'text'
                            valor = inp.get_attribute('value') or ''
                            location = inp.location
                            
                            if tipo in ['text', 'number', 'tel'] and not valor and location['y'] > 100:
                                campo = inp
                                print("✓ Campo encontrado (primer input vacío)")
                                break
                except Exception as e:
                    print(f"⚠ Error buscando primer input: {e}")
            
            if campo:
                print(f"✓ Campo encontrado, pegando código: {codigo}")
                
                # Hacer scroll al campo
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", campo)
                time.sleep(0.5)
                
                # Enfocar y hacer clic
                self.driver.execute_script("arguments[0].focus();", campo)
                time.sleep(0.3)
                campo.click()
                time.sleep(0.3)
                
                # Limpiar y escribir el código
                campo.clear()
                time.sleep(0.2)
                campo.send_keys(codigo)
                time.sleep(0.5)
                
                # Verificar
                valor = campo.get_attribute('value') or ''
                if codigo in valor or valor == codigo:
                    print(f"✓✓ Código escrito exitosamente en el campo: {codigo}")
                else:
                    # Intentar pegar con Ctrl+V
                    print("⚠ Escritura directa falló, intentando pegar con Ctrl+V...")
                    campo.clear()
                    time.sleep(0.2)
                    actions = ActionChains(self.driver)
                    actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                    time.sleep(0.5)
                    
                    valor = campo.get_attribute('value') or ''
                    if codigo in valor or valor == codigo:
                        print(f"✓✓ Código pegado exitosamente: {codigo}")
                    else:
                        print(f"⚠ El código no se pegó correctamente. Valor en campo: {valor}")
            else:
                print("⚠ No se encontró el campo de código de verificación")
                
        except Exception as e:
            print(f"⚠ Error al pegar código: {e}")
            import traceback
            traceback.print_exc()
    
    def _completar_datos_personales(self) -> None:
        """
        Completa aleatoriamente los campos de datos personales
        Mes y Día: Tab + Enter 2 veces
        Año: Escribe directamente un año coherente
        """
        try:
            print("\n📝 Completando datos personales...")
            time.sleep(2)  # Esperar a que aparezcan los campos
            
            # Generar fecha de nacimiento aleatoria (entre 18 y 65 años)
            año_actual = 2024
            año_nacimiento = random.randint(año_actual - 65, año_actual - 18)
            mes = random.randint(1, 12)
            # Día aleatorio (considerando que algunos meses tienen 30 o 31 días)
            if mes in [4, 6, 9, 11]:
                dia = random.randint(1, 30)
            elif mes == 2:
                dia = random.randint(1, 28)
            else:
                dia = random.randint(1, 31)
            
            print(f"  Fecha generada: Mes {mes}, Día {dia}, Año {año_nacimiento}")
            
            actions = ActionChains(self.driver)
            
            # Campo 1: Mes - Tab 1 vez, Enter 2 veces
            print("  Completando campo Mes (Tab + Enter 2 veces)...")
            actions.send_keys(Keys.TAB).perform()
            time.sleep(0.3)
            actions.send_keys(Keys.ENTER).perform()
            time.sleep(0.3)
            actions.send_keys(Keys.ENTER).perform()
            time.sleep(0.5)
            print(f"  ✓ Mes completado")
            
            # Campo 2: Día - Tab 1 vez, Enter 2 veces
            print("  Completando campo Día (Tab + Enter 2 veces)...")
            actions.send_keys(Keys.TAB).perform()
            time.sleep(0.3)
            actions.send_keys(Keys.ENTER).perform()
            time.sleep(0.3)
            actions.send_keys(Keys.ENTER).perform()
            time.sleep(0.5)
            print(f"  ✓ Día completado")
            
            # Campo 3: Año - Escribir directamente un año coherente
            print(f"  Completando campo Año (escribiendo directamente: {año_nacimiento})...")
            actions.send_keys(Keys.TAB).perform()
            time.sleep(0.3)
            # Escribir el año directamente
            actions.send_keys(str(año_nacimiento)).perform()
            time.sleep(0.5)
            print(f"  ✓ Año escrito: {año_nacimiento}")
            
            # Botón Next: 2 Tabs y Enter
            print("\n🔍 Navegando al botón 'Next'...")
            time.sleep(0.5)
            actions.send_keys(Keys.TAB).perform()
            time.sleep(0.3)
            actions.send_keys(Keys.TAB).perform()
            time.sleep(0.3)
            actions.send_keys(Keys.ENTER).perform()
            time.sleep(2)
            print("✓✓ Clic en botón 'Next' realizado")
            
            # Completar nombre y apellido
            self._completar_nombre_apellido()
            
        except Exception as e:
            print(f"⚠ Error al completar datos personales: {e}")
            import traceback
            traceback.print_exc()
    
    def _completar_nombre_apellido(self) -> None:
        """
        Completa el nombre y apellido, luego hace clic en Next
        """
        try:
            print("\n📝 Completando nombre y apellido...")
            time.sleep(2)  # Esperar a que aparezcan los campos
            
            # Lista de nombres comunes
            nombres = ['John', 'Michael', 'David', 'James', 'Robert', 'William', 'Richard', 'Joseph',
                      'Thomas', 'Christopher', 'Daniel', 'Matthew', 'Anthony', 'Mark', 'Donald',
                      'Steven', 'Paul', 'Andrew', 'Joshua', 'Kenneth', 'Kevin', 'Brian', 'George',
                      'Maria', 'Jennifer', 'Lisa', 'Patricia', 'Linda', 'Barbara', 'Elizabeth',
                      'Susan', 'Jessica', 'Sarah', 'Karen', 'Nancy', 'Betty', 'Margaret', 'Sandra']
            
            # Lista de apellidos comunes
            apellidos = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
                        'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Wilson', 'Anderson', 'Thomas',
                        'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Thompson', 'White', 'Harris',
                        'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young', 'Allen']
            
            nombre = random.choice(nombres)
            apellido = random.choice(apellidos)
            
            print(f"  Nombre generado: {nombre} {apellido}")
            
            actions = ActionChains(self.driver)
            
            # Escribir nombre (First name)
            print(f"  Escribiendo nombre: {nombre}")
            actions.send_keys(nombre).perform()
            time.sleep(0.5)
            
            # Tab 1 vez
            print("  Presionando Tab...")
            actions.send_keys(Keys.TAB).perform()
            time.sleep(0.3)
            
            # Escribir apellido (Last name)
            print(f"  Escribiendo apellido: {apellido}")
            actions.send_keys(apellido).perform()
            time.sleep(0.5)
            
            # Tab 4 veces
            print("  Presionando Tab 4 veces...")
            for i in range(4):
                actions.send_keys(Keys.TAB).perform()
                time.sleep(0.2)
            
            # Enter
            print("  Presionando Enter...")
            actions.send_keys(Keys.ENTER).perform()
            time.sleep(2)
            print("✓✓ Nombre y apellido completados, clic en 'Next' realizado")
            
            # Verificar error antes del captcha
            time.sleep(1)
            if self._detectar_error_cuenta():
                print("⚠ Error detectado antes del captcha, abortando...")
                return
            
            # Manejar el captcha "Press and hold"
            self._presionar_y_mantener_captcha()
            
            # Verificar error después del captcha
            time.sleep(2)
            if self._detectar_error_cuenta():
                print("⚠ Error detectado después del captcha, abortando...")
                return
            
        except Exception as e:
            print(f"⚠ Error al completar nombre y apellido: {e}")
            import traceback
            traceback.print_exc()
    
    def _detectar_error_cuenta(self) -> bool:
        """
        Detecta si aparece el error "We can't create your account" o "unusual activity"
        
        Returns:
            True si detecta el error, False en caso contrario
        """
        if not self.driver:
            return False
        
        try:
            # Obtener el texto de la página
            page_text = self.driver.page_source.lower()
            page_text_visible = ""
            
            # También obtener texto visible
            try:
                body = self.driver.find_element(By.TAG_NAME, "body")
                page_text_visible = body.text.lower()
            except:
                pass
            
            # Buscar mensajes de error
            mensajes_error = [
                "we can't create your account",
                "can't create your account",
                "unusual activity",
                "we're having trouble creating",
                "having trouble creating",
                "no podemos crear tu cuenta",
                "actividad inusual",
                "estamos teniendo problemas"
            ]
            
            for mensaje in mensajes_error:
                if mensaje in page_text or mensaje in page_text_visible:
                    print(f"\n{'='*60}")
                    print(f"⚠⚠ ERROR DETECTADO: {mensaje.upper()}")
                    print(f"{'='*60}\n")
                    return True
            
            return False
            
        except Exception as e:
            # Si hay error al verificar, asumir que no hay error
            return False
    
    def _reiniciar_navegador(self) -> None:
        """
        Cierra la pestaña/ventana actual y abre una nueva
        """
        try:
            if self.driver:
                print("🔄 Cerrando pestaña actual...")
                # Cerrar todas las pestañas excepto la primera
                if len(self.driver.window_handles) > 1:
                    # Cerrar pestañas adicionales
                    for handle in self.driver.window_handles[1:]:
                        self.driver.switch_to.window(handle)
                        self.driver.close()
                    # Volver a la primera pestaña
                    self.driver.switch_to.window(self.driver.window_handles[0])
                
                # Cerrar la pestaña actual y abrir una nueva
                self.driver.close()
                time.sleep(1)
                
                # Si no quedan ventanas, crear una nueva
                if len(self.driver.window_handles) == 0:
                    self.driver.execute_script("window.open('');")
                    self.driver.switch_to.window(self.driver.window_handles[0])
                else:
                    # Cambiar a la primera pestaña disponible
                    self.driver.switch_to.window(self.driver.window_handles[0])
                
                print("✅ Nueva pestaña abierta")
                time.sleep(2)
        except Exception as e:
            print(f"⚠ Error al reiniciar navegador: {e}")
            # Si falla, cerrar todo y abrir nuevo navegador
            try:
                if self.driver:
                    self.driver.quit()
                self.driver = None
                print("🔄 Abriendo nuevo navegador...")
                self.inicializar_navegador()
            except:
                pass
    
    def _presionar_y_mantener_captcha(self) -> None:
        """
        Espera a que cargue la página, luego presiona Enter 1 vez, Tab, espera 10 segundos y presiona Enter de nuevo
        """
        try:
            print("\n🔐 Manejando captcha 'Press and hold'...")
            
            # Esperar a que la página cargue completamente
            print("  Esperando a que la página cargue completamente...")
            max_espera = 30  # Máximo 30 segundos esperando
            tiempo_esperado = 0
            while tiempo_esperado < max_espera:
                estado = self.driver.execute_script("return document.readyState")
                if estado == "complete":
                    # Esperar un poco más para asegurar que todo esté cargado
                    time.sleep(2)
                    print("  ✓ Página cargada completamente")
                    break
                time.sleep(0.5)
                tiempo_esperado += 0.5
            
            # Esperar adicional para que el captcha aparezca
            time.sleep(2)
            
            actions = ActionChains(self.driver)
            
            # Enter 1 vez
            print("  Presionando Enter 1 vez...")
            actions.send_keys(Keys.ENTER).perform()
            time.sleep(0.5)
            
            # Tab
            print("  Presionando Tab...")
            actions.send_keys(Keys.TAB).perform()
            time.sleep(0.5)
            
            # Esperar 10 segundos
            tiempo_espera = 10.0
            print(f"  Esperando {tiempo_espera} segundos...")
            time.sleep(tiempo_espera)
            
            # Enter de nuevo
            print("  Presionando Enter de nuevo...")
            actions.send_keys(Keys.ENTER).perform()
            time.sleep(1)
            
            print("✓✓ Captcha completado")
            
        except Exception as e:
            print(f"⚠ Error al manejar captcha: {e}")
            import traceback
            traceback.print_exc()
    
    def hacer_clic_y_pegar_por_posicion(self, correo: str) -> bool:
        """
        Hace clic en una posición específica (X, Y) y pega el correo
        
        Args:
            correo: Correo a pegar
            
        Returns:
            True si se pegó exitosamente
        """
        if self.posicion_x == 0 or self.posicion_y == 0:
            print("⚠ No se especificaron coordenadas. Usando modo manual.")
            return False
        
        try:
            print(f"\n🖱️ Haciendo clic en posición ({self.posicion_x}, {self.posicion_y})...")
            
            # Copiar correo al portapapeles
            if PYPERCLIP_AVAILABLE:
                pyperclip.copy(correo)
                print("✓ Correo copiado al portapapeles")
            else:
                # Usar JavaScript para copiar
                self.driver.execute_script(f"""
                    navigator.clipboard.writeText('{correo}');
                """)
                time.sleep(0.3)
                print("✓ Correo copiado al portapapeles (JavaScript)")
            
            # Hacer clic usando pyautogui (coordenadas absolutas de pantalla)
            if RECONOCIMIENTO_VISUAL_AVAILABLE:
                print(f"Haciendo clic en coordenadas de pantalla: ({self.posicion_x}, {self.posicion_y})")
                pyautogui.click(self.posicion_x, self.posicion_y)
                time.sleep(0.5)
                print("✓ Clic realizado")
                
                # Limpiar el campo
                pyautogui.hotkey('ctrl', 'a')
                time.sleep(0.2)
                pyautogui.press('delete')
                time.sleep(0.2)
                
                # Pegar el correo
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.5)
                
                print(f"✓✓ Correo pegado exitosamente: {correo}")
                
                # Hacer clic en el botón "Siguiente"
                self._clic_boton_siguiente()
                
                return True
            else:
                # Método alternativo con Selenium (coordenadas relativas)
                body = self.driver.find_element(By.TAG_NAME, "body")
                actions = ActionChains(self.driver)
                actions.move_to_element_with_offset(body, 0, 0).perform()
                time.sleep(0.2)
                actions.move_by_offset(self.posicion_x, self.posicion_y).click().perform()
                time.sleep(0.5)
                
                actions.send_keys(Keys.CONTROL + 'a').perform()
                time.sleep(0.2)
                actions.send_keys(Keys.DELETE).perform()
                time.sleep(0.2)
                actions.key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
                time.sleep(0.5)
                
                print(f"✓✓ Correo pegado exitosamente: {correo}")
                
                # Hacer clic en el botón "Siguiente"
                self._clic_boton_siguiente()
                
                return True
            
        except Exception as e:
            print(f"⚠ Error al hacer clic y pegar: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def ejecutar(self) -> None:
        """Ejecuta el bot completo"""
        try:
            # Incrementar contador de cuentas
            self.cuentas_creadas += 1
            print(f"\n📊 Cuenta #{self.cuentas_creadas}")
            
            # Crear correo temporal
            correo = self.crear_correo_temporal()
            
            # Bucle para reintentar si detecta error
            max_intentos = 5
            intento = 0
            exito = False
            
            while intento < max_intentos and not exito:
                intento += 1
                if intento > 1:
                    print(f"\n🔄 Reintento #{intento} de {max_intentos}")
                    time.sleep(3)
                
                # Abrir navegador y página de registro
                if intento == 1 or not self.driver:
                    self.abrir_registro_microsoft()
                else:
                    # Si ya hay navegador, solo navegar a la página
                    try:
                        self.driver.get(self.url_registro)
                        self._ejecutar_stealth_script()
                        time.sleep(3)
                    except:
                        self.abrir_registro_microsoft()
                
                # Verificar error antes de continuar
                if self._detectar_error_cuenta():
                    print("⚠ Error detectado antes de empezar, reiniciando...")
                    self._reiniciar_navegador()
                    continue
                
                # Mostrar información del correo
                self.mostrar_correo_temporal()
                
                # Intentar hacer clic y pegar el correo
                correo_pegado = False
                if self.usar_reconocimiento:
                    # Método preferido: Usar Selenium directamente (más confiable)
                    if self._pegar_correo_selenium_directo(correo):
                        print("✅ Correo pegado usando Selenium directo")
                        correo_pegado = True
                    else:
                        # Método alternativo: Usar reconocimiento visual con coordenadas
                        posicion = self.encontrar_campo_por_reconocimiento_visual()
                        if posicion:
                            self.posicion_x, self.posicion_y = posicion
                            if self.hacer_clic_y_pegar_por_posicion(correo):
                                correo_pegado = True
                        else:
                            print("⚠ No se pudo encontrar el campo")
                elif self.posicion_x > 0 and self.posicion_y > 0:
                    # Usar coordenadas manuales
                    if self.hacer_clic_y_pegar_por_posicion(correo):
                        correo_pegado = True
                
                if not correo_pegado:
                    print("⚠ No se pudo pegar el correo, reintentando...")
                    self._reiniciar_navegador()
                    continue
                
                # Verificar error después de pegar correo
                time.sleep(2)
                if self._detectar_error_cuenta():
                    print("⚠ Error detectado después de pegar correo, reiniciando...")
                    self._reiniciar_navegador()
                    continue
                
                # Esperar correo y pegar código
                self._esperar_y_pegar_codigo_verificacion()
                
                # Verificar error después de pegar código
                time.sleep(2)
                if self._detectar_error_cuenta():
                    print("⚠ Error detectado después de verificar código, reiniciando...")
                    self._reiniciar_navegador()
                    continue
                
                # Si llegamos aquí, el proceso fue exitoso
                exito = True
                break
            
            if not exito:
                print(f"\n❌ No se pudo completar después de {max_intentos} intentos")
                print("   El bot continuará intentando en el siguiente ciclo...")
            
            print("El navegador permanecerá abierto.")
            print("Puedes usar el correo temporal mostrado arriba.")
            print("Presiona Ctrl+C para cerrar.\n")
            
            # Mantener el programa en ejecución
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n⏹ Cerrando bot...")
                if self.driver:
                    self.driver.quit()
                print("✓ Bot cerrado correctamente")
                
        except Exception as e:
            print(f"\n❌ Error: {e}")
            if self.driver:
                self.driver.quit()


def abrir_registro_microsoft(usar_reconocimiento: bool = True, posicion_x: int = 0, posicion_y: int = 0) -> None:
    """
    Función principal que abre el registro de Microsoft con correo temporal
    
    Args:
        usar_reconocimiento: Si es True, usa reconocimiento visual (por defecto)
        posicion_x: Coordenada X manual (solo si usar_reconocimiento=False)
        posicion_y: Coordenada Y manual (solo si usar_reconocimiento=False)
    """
    bot = BotRegistroMicrosoft(usar_reconocimiento=usar_reconocimiento, posicion_x=posicion_x, posicion_y=posicion_y)
    bot.ejecutar()


if __name__ == "__main__":
    # Verificar versión de Python
    if sys.version_info < (3, 11):
        print("Error: Este script requiere Python 3.11 o superior.")
        print(f"Versión actual: {sys.version}")
        sys.exit(1)
    
    # Leer argumentos
    usar_reconocimiento = True
    posicion_x = 0
    posicion_y = 0
    
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "manual" and len(sys.argv) >= 4:
            usar_reconocimiento = False
            try:
                posicion_x = int(sys.argv[2])
                posicion_y = int(sys.argv[3])
                print(f"📌 Modo manual: coordenadas ({posicion_x}, {posicion_y})")
            except:
                print("⚠ Error: Las coordenadas deben ser números")
        elif sys.argv[1].lower() == "manual":
            usar_reconocimiento = False
            print("📌 Modo manual sin coordenadas (solo mostrará el correo)")
    
    if usar_reconocimiento:
        print("📌 Modo reconocimiento visual activado")
    
    abrir_registro_microsoft(usar_reconocimiento=usar_reconocimiento, posicion_x=posicion_x, posicion_y=posicion_y)

