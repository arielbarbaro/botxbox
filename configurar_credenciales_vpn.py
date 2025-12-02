"""
Script para configurar credenciales de ProtonVPN en los perfiles .ovpn
"""

import os
import sys

def configurar_credenciales():
    """
    Configura las credenciales de ProtonVPN para todos los perfiles .ovpn
    """
    vpn_profiles_dir = "vpn_profiles"
    
    if not os.path.exists(vpn_profiles_dir):
        print(f"❌ No se encontró la carpeta '{vpn_profiles_dir}'")
        print(f"   Asegúrate de que los archivos .ovpn estén en esa carpeta")
        return
    
    # Obtener archivos .ovpn
    ovpn_files = [f for f in os.listdir(vpn_profiles_dir) if f.endswith('.ovpn')]
    
    if not ovpn_files:
        print(f"❌ No se encontraron archivos .ovpn en '{vpn_profiles_dir}'")
        return
    
    print(f"📁 Encontrados {len(ovpn_files)} perfiles .ovpn")
    print("\n" + "="*60)
    print("🔐 CONFIGURACIÓN DE CREDENCIALES PROTONVPN")
    print("="*60)
    print("\n💡 Necesitas tus credenciales de ProtonVPN:")
    print("   - Usuario: Tu nombre de usuario de ProtonVPN")
    print("   - Contraseña: Tu contraseña de ProtonVPN")
    print("\n⚠️  Las credenciales se guardarán en un archivo seguro")
    print("="*60 + "\n")
    
    # Solicitar credenciales
    usuario = input("👤 Usuario de ProtonVPN: ").strip()
    if not usuario:
        print("❌ El usuario no puede estar vacío")
        return
    
    # Intentar usar getpass, si falla usar input normal
    try:
        import getpass
        contraseña = getpass.getpass("🔒 Contraseña de ProtonVPN: ").strip()
    except (ImportError, Exception):
        # Si getpass falla, usar input normal
        print("💡 Nota: La contraseña será visible mientras la escribes")
        contraseña = input("🔒 Contraseña de ProtonVPN: ").strip()
    
    if not contraseña:
        print("❌ La contraseña no puede estar vacía")
        return
    
    # Crear archivo de credenciales
    credenciales_file = os.path.join(vpn_profiles_dir, "credenciales.txt")
    
    try:
        with open(credenciales_file, 'w', encoding='utf-8') as f:
            f.write(f"{usuario}\n")
            f.write(f"{contraseña}\n")
        
        print(f"\n✅ Archivo de credenciales creado: {credenciales_file}")
        
        # Modificar todos los archivos .ovpn para usar el archivo de credenciales
        archivos_modificados = 0
        for ovpn_file in ovpn_files:
            ovpn_path = os.path.join(vpn_profiles_dir, ovpn_file)
            
            try:
                # Leer el contenido del archivo
                with open(ovpn_path, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                # Verificar si ya tiene auth-user-pass configurado
                if 'auth-user-pass' in contenido:
                    # Reemplazar auth-user-pass por auth-user-pass credenciales.txt
                    # Usar ruta relativa desde el directorio del perfil
                    nuevo_contenido = contenido.replace(
                        'auth-user-pass',
                        f'auth-user-pass credenciales.txt'
                    )
                    
                    # Solo escribir si hubo cambio
                    if nuevo_contenido != contenido:
                        with open(ovpn_path, 'w', encoding='utf-8') as f:
                            f.write(nuevo_contenido)
                        archivos_modificados += 1
                        print(f"  ✓ Modificado: {ovpn_file}")
                    else:
                        # Si ya tenía la referencia, verificar que sea correcta
                        if 'auth-user-pass credenciales.txt' in contenido:
                            print(f"  ℹ Ya configurado: {ovpn_file}")
                        else:
                            # Agregar la referencia si no está
                            lineas = contenido.split('\n')
                            nueva_linea = None
                            for i, linea in enumerate(lineas):
                                if 'auth-user-pass' in linea and 'credenciales.txt' not in linea:
                                    lineas[i] = 'auth-user-pass credenciales.txt'
                                    nueva_linea = '\n'.join(lineas)
                                    break
                            
                            if nueva_linea:
                                with open(ovpn_path, 'w', encoding='utf-8') as f:
                                    f.write(nueva_linea)
                                archivos_modificados += 1
                                print(f"  ✓ Actualizado: {ovpn_file}")
                
            except Exception as e:
                print(f"  ⚠ Error al modificar {ovpn_file}: {e}")
        
        print(f"\n✅ Configuración completada!")
        print(f"   - Archivos modificados: {archivos_modificados}/{len(ovpn_files)}")
        print(f"   - Credenciales guardadas en: {credenciales_file}")
        print(f"\n💡 Ahora puedes ejecutar el bot y las VPN deberían conectarse correctamente")
        
    except Exception as e:
        print(f"❌ Error al crear archivo de credenciales: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    configurar_credenciales()

