"""Script para probar el bot sin VPN"""
import sys
import os

# Temporalmente renombrar la carpeta vpn_profiles para que no se detecte
vpn_profiles_dir = "vpn_profiles"
vpn_backup_dir = "vpn_profiles_backup"

if os.path.exists(vpn_profiles_dir):
    print("📁 Deshabilitando VPN temporalmente...")
    if os.path.exists(vpn_backup_dir):
        import shutil
        shutil.rmtree(vpn_backup_dir)
    os.rename(vpn_profiles_dir, vpn_backup_dir)
    print("✓ VPN deshabilitada")

try:
    # Importar y ejecutar el bot
    from bot_registro_microsoft import abrir_registro_microsoft
    
    print("\n" + "="*60)
    print("🤖 EJECUTANDO BOT SIN VPN")
    print("="*60 + "\n")
    
    abrir_registro_microsoft(
        usar_reconocimiento=True,
        usar_vpn=False,
        vpn_servers=None
    )
    
except KeyboardInterrupt:
    print("\n⏹ Bot detenido por el usuario")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    # Restaurar la carpeta VPN
    if os.path.exists(vpn_backup_dir):
        print("\n📁 Restaurando carpeta VPN...")
        if os.path.exists(vpn_profiles_dir):
            import shutil
            shutil.rmtree(vpn_profiles_dir)
        os.rename(vpn_backup_dir, vpn_profiles_dir)
        print("✓ VPN restaurada")

