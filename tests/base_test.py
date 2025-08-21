#!/usr/bin/env python3
"""
Classe base per tutti i test del progetto AnalisiOpenData.
Fornisce funzionalità comuni per eseguire test, gestire risultati e generare report.
Raggruppa il codice che sarebbe ridondante in altri file di test.
"""
import sys
from abc import ABC, abstractmethod # Classi astratte per definire metodi comuni
from typing import List, Tuple, Callable


class BaseTest(ABC):
    """
    Classe base astratta per tutti i test del progetto.
    Fornisce metodi comuni per l'esecuzione e il reporting dei test.
    """
    
    def __init__(self, test_name: str):
        """
        Inizializza la classe base del test.
        
        Args:
            test_name: Nome del test suite (es. "SYNTAX", "IMPORTS", ecc.)
        """
        self.test_name = test_name
        self.results: List[Tuple[str, bool]] = []
    
    def run_tests(self, tests: List[Tuple[str, Callable]]) -> bool:
        """
        Esegue una lista di test e raccoglie i risultati.
        
        Args:
            tests: Lista di tuple (nome_test, funzione_test)
            
        Returns:
            True se tutti i test passano, False altrimenti
        """
        print(f"🚀 AVVIO TEST {self.test_name.upper()}\n")
        
        self.results = []
        
        for test_name, test_func in tests:
            try:
                print(f"🔍 Eseguendo {test_name}...")
                result = test_func()
                self.results.append((test_name, result))
                
                if result:
                    print(f"✅ {test_name} completato con successo\n")
                else:
                    print(f"❌ {test_name} fallito\n")
                    
            except Exception as e:
                print(f"❌ Errore in {test_name}: {e}\n")
                self.results.append((test_name, False))
        
        return self.report_results()
    
    def report_results(self) -> bool:
        """
        Genera un report finale dei risultati dei test.
        
        Returns:
            True se tutti i test passano, False altrimenti
        """
        if not self.results:
            print("⚠️  Nessun test eseguito")
            return False
        
        # Calcola statistiche
        passed = sum(1 for _, result in self.results if result)
        total = len(self.results)
        
        # Stampa separatore e header
        print("\n" + "="*60)
        print(f"RISULTATI TEST {self.test_name.upper()}:")
        print("="*60)
        
        # Stampa risultati individuali
        for test_name, result in self.results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        # Stampa riassunto
        print(f"\nTotale: {passed}/{total} test passati")
        percentage = (passed / total) * 100
        print(f"Percentuale successo: {percentage:.1f}%")
        
        # Messaggio finale
        if passed == total:
            print(f"\n🎉 TUTTI I TEST {self.test_name.upper()} SONO PASSATI!")
            self._success_message()
            return True
        else:
            print(f"\n⚠️  ALCUNI TEST {self.test_name.upper()} SONO FALLITI")
            self._failure_message()
            return False
    
    @abstractmethod
    def _success_message(self) -> None:
        """Messaggio specifico per quando tutti i test passano."""
        pass
    
    @abstractmethod
    def _failure_message(self) -> None:
        """Messaggio specifico per quando alcuni test falliscono."""
        pass
    
    def exit_with_code(self, success: bool) -> None:
        """
        Termina il programma con il codice di uscita appropriato.
        
        Args:
            success: True per exit code 0, False per exit code 1
        """
        sys.exit(0 if success else 1)


class SyntaxTest(BaseTest):
    """Test di sintassi specifico per verificare la correttezza del codice Python."""
    
    def __init__(self):
        super().__init__("SYNTAX")
    
    def _success_message(self) -> None:
        print("Il codice è sintatticamente corretto!")
        print("Procedi con i test di importazione.")
    
    def _failure_message(self) -> None:
        print("Correggi gli errori di sintassi prima di procedere.")


class ImportTest(BaseTest):
    """Test di importazione per verificare dipendenze e strutture."""
    
    def __init__(self):
        super().__init__("IMPORTS")
    
    def _success_message(self) -> None:
        print("Tutte le importazioni e istanziazioni funzionano!")
        print("Il progetto è pronto per i test funzionali.")
    
    def _failure_message(self) -> None:
        print("Risolvi i problemi di importazione prima di procedere.")


class FunctionalTest(BaseTest):
    """Test funzionali per verificare il comportamento delle componenti."""
    
    def __init__(self):
        super().__init__("FUNCTIONAL")
    
    def _success_message(self) -> None:
        print("Tutte le funzionalità principali operano correttamente!")
        print("Il sistema è pronto per i test completi.")
    
    def _failure_message(self) -> None:
        print("Risolvi i problemi funzionali identificati.")


class CompleteTest(BaseTest):
    """Test completi end-to-end per verificare l'integrazione totale."""
    
    def __init__(self):
        super().__init__("COMPLETE")
    
    def _success_message(self) -> None:
        print("✨ L'applicazione è completamente funzionante!")
        print("\n📋 PROSSIMI PASSI:")
        print("1. Esegui: python ../src/main.py")
        print("2. Segui le istruzioni per analizzare i dati")
        print("3. Controlla i file di output nella cartella 'output/'")
    
    def _failure_message(self) -> None:
        print("Risolvi gli errori prima di utilizzare l'applicazione.")
