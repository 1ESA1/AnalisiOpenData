#!/usr/bin/env python3
"""
Launcher per la Suite Unificata di Test AnalisiOpenData
Esegue i test unificati in un unico file per evitare duplicazioni.
Elimina la necessità di eseguire test separati per ogni modulo.
"""

import sys
import subprocess

def run_unified_tests():
    """Esegue la suite unificata di test"""
    print("🚀 AVVIO SUITE UNIFICATA DI TEST")
    print("="*60)
    
    try:
        result = subprocess.run([
            sys.executable, 'test_unified.py'
        ], capture_output=True, text=True, timeout=120)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("❌ TIMEOUT: Suite di test troppo lenta")
        return False
    except Exception as e:
        print(f"❌ ERRORE: {e}")
        return False

def main():
    """Funzione principale"""
    success = run_unified_tests()
    
    print("\n" + "="*60)
    if success:
        print("🎉 SUITE UNIFICATA: TUTTI I TEST SUPERATI")
        print("✅ Progetto completamente validato")
    else:
        print("⚠️  SUITE UNIFICATA: ALCUNI TEST FALLITI")
        print("🔧 Controllare output sopra per dettagli")
    print("="*60)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
