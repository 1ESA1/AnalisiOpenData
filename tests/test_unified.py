#!/usr/bin/env python3
"""
Test Suite Unificata per AnalisiOpenData

Questo script unifica tutti i test in un'unica suite completa:
- Test sintassi (syntax checking)
- Test importazioni (import validation) 
- Test funzionalità (functional testing)
- Test integrazione completa (end-to-end testing)

Elimina le duplicazioni e fornisce un'interfaccia di test semplificata.
"""

import sys
from typing import Dict
from base_test import BaseTest
from test_config import get_available_modules, SAMPLE_JSON_DATA
from test_utils import setup_python_path, temporary_directory, create_sample_dataframe


class UnifiedTestSuite(BaseTest):
    """Suite di test unificata che combina tutti i livelli di testing"""
    
    def __init__(self):
        super().__init__("🎯 Suite Unificata AnalisiOpenData")
        self.modules = get_available_modules()
        
    def run_syntax_tests(self) -> bool:
        """Esegue test di sintassi su tutti i moduli"""
        print("\n" + "="*60)
        print("🔍 FASE 1: TEST SINTASSI")
        print("="*60)
        
        syntax_tests = []
        for module_name, file_path in self.modules.items():
            syntax_tests.append((f"Sintassi {module_name}", 
                               lambda fp=file_path, mn=module_name: self._test_syntax(mn, fp)))
        
        return self.run_tests(syntax_tests)
    
    def _test_syntax(self, module_name: str, file_path: str) -> bool:
        """Test sintassi singolo modulo"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            compile(code, file_path, 'exec')
            return True
        except (SyntaxError, Exception) as e:
            print(f"❌ {module_name}: {e}")
            return False
    
    def run_import_tests(self) -> bool:
        """Esegue test di importazione"""
        print("\n" + "="*60)
        print("📦 FASE 2: TEST IMPORTAZIONI")
        print("="*60)
        
        import_tests = [
            ("Import config", self._test_import_config),
            ("Import services", self._test_import_services),
            ("Import file_manager", self._test_import_file_manager),
            ("Import analyzer", self._test_import_analyzer),
            ("Import ui", self._test_import_ui),
            ("Import main", self._test_import_main),
        ]
        
        return self.run_tests(import_tests)
    
    def _test_import_config(self) -> bool:
        """Test import config"""
        try:
            import config
            # Verifica costanti essenziali
            return hasattr(config, 'CKAN_API_URL') and hasattr(config, 'DATA_DIR')
        except Exception:
            return False
    
    def _test_import_services(self) -> bool:
        """Test import services"""
        try:
            import services
            return hasattr(services, 'CkanApiService') and hasattr(services, 'DataService')
        except Exception:
            return False
    
    def _test_import_file_manager(self) -> bool:
        """Test import file_manager"""
        try:
            import file_manager
            return hasattr(file_manager, 'FileManager')
        except Exception:
            return False
    
    def _test_import_analyzer(self) -> bool:
        """Test import analyzer"""
        try:
            import analyzer
            return hasattr(analyzer, 'IncidentAnalyzer')
        except Exception:
            return False
    
    def _test_import_ui(self) -> bool:
        """Test import ui"""
        try:
            import ui
            return hasattr(ui, 'UserInterface')
        except Exception:
            return False
    
    def _test_import_main(self) -> bool:
        """Test import main"""
        try:
            import main
            return hasattr(main, 'OpenDataAnalyzer')
        except Exception:
            return False
    
    def run_functional_tests(self) -> bool:
        """Esegue test funzionali"""
        print("\n" + "="*60)
        print("⚙️ FASE 3: TEST FUNZIONALITÀ")
        print("="*60)
        
        functional_tests = [
            ("FileManager JSON", self._test_file_manager_json),
            ("FileManager CSV", self._test_file_manager_csv),
            ("DataService Filter", self._test_data_service_filter),
            ("IncidentAnalyzer", self._test_incident_analyzer),
            ("CkanApiService", self._test_ckan_api_service),
        ]
        
        return self.run_tests(functional_tests)
    
    def _test_file_manager_json(self) -> bool:
        """Test FileManager operazioni JSON"""
        try:
            from file_manager import FileManager
            fm = FileManager()
            
            with temporary_directory() as temp_dir:
                # Test save/load JSON
                success = fm.save_json(SAMPLE_JSON_DATA, "test.json", temp_dir)
                if not success:
                    return False
                
                loaded_data = fm.load_json("test.json", temp_dir)
                return loaded_data == SAMPLE_JSON_DATA
        except Exception:
            return False
    
    def _test_file_manager_csv(self) -> bool:
        """Test FileManager operazioni CSV"""
        try:
            from file_manager import FileManager
            fm = FileManager()
            
            with temporary_directory() as temp_dir:
                df = create_sample_dataframe()
                success = fm.save_dataframe_csv(df, "test.csv", temp_dir)
                return success
        except Exception:
            return False
    
    def _test_data_service_filter(self) -> bool:
        """Test DataService filtro pacchetti"""
        try:
            from services import DataService
            ds = DataService()
            
            test_packages = ["incidente-stradale", "traffico-urbano", "meteo-data"]
            filtered = ds.filter_packages_by_keyword(test_packages, "incidente")
            return len(filtered) == 1 and "incidente-stradale" in filtered
        except Exception:
            return False
    
    def _test_incident_analyzer(self) -> bool:
        """Test IncidentAnalyzer"""
        try:
            from analyzer import IncidentAnalyzer
            df = create_sample_dataframe()
            analyzer = IncidentAnalyzer(df)
            summary = analyzer.get_data_summary()
            return isinstance(summary, dict) and len(summary) > 0
        except Exception:
            return False
    
    def _test_ckan_api_service(self) -> bool:
        """Test CkanApiService struttura"""
        try:
            from services import CkanApiService
            service = CkanApiService()
            return hasattr(service, 'get_package_list')
        except Exception:
            return False
    
    def run_integration_tests(self) -> bool:
        """Esegue test di integrazione end-to-end"""
        print("\n" + "="*60)
        print("🚀 FASE 4: TEST INTEGRAZIONE")
        print("="*60)
        
        integration_tests = [
            ("Workflow Completo", self._test_complete_workflow),
            ("Gestione Errori", self._test_error_handling),
            ("Validazione Output", self._test_output_validation),
        ]
        
        return self.run_tests(integration_tests)
    
    def _test_complete_workflow(self) -> bool:
        """Test workflow completo simulato"""
        try:
            # Simula un workflow end-to-end senza chiamate API reali
            from services import DataService, CkanApiService
            from file_manager import FileManager
            from analyzer import IncidentAnalyzer
            from ui import UserInterface
            
            # Test istanziazione componenti
            data_service = DataService()
            api_service = CkanApiService()
            file_manager = FileManager()
            ui = UserInterface()
            
            # Test operazioni base
            df = create_sample_dataframe()
            analyzer = IncidentAnalyzer(df)
            
            with temporary_directory() as temp_dir:
                success = file_manager.save_dataframe_csv(df, "workflow_test.csv", temp_dir)
                return success
        except Exception:
            return False
    
    def _test_error_handling(self) -> bool:
        """Test gestione errori"""
        try:
            from file_manager import FileManager
            fm = FileManager()
            
            # Test con path inesistente
            result = fm.load_json("nonexistent.json", "/path/that/does/not/exist")
            return result is None  # Dovrebbe gestire l'errore gracefully
        except Exception:
            return False
    
    def _test_output_validation(self) -> bool:
        """Test validazione output"""
        try:
            from analyzer import IncidentAnalyzer
            df = create_sample_dataframe()
            analyzer = IncidentAnalyzer(df)
            
            # Test che i metodi restituiscano tipi corretti
            summary = analyzer.get_data_summary()
            return isinstance(summary, dict)
        except Exception:
            return False
    
    def run_all_tests(self) -> bool:
        """Esegue tutti i test in sequenza"""
        print("🎯 AVVIO SUITE UNIFICATA DI TEST")
        print("="*80)
        
        # Setup ambiente
        setup_python_path()
        
        # Esegui tutte le fasi
        phases = [
            ("Sintassi", self.run_syntax_tests),
            ("Importazioni", self.run_import_tests),
            ("Funzionalità", self.run_functional_tests),
            ("Integrazione", self.run_integration_tests),
        ]
        
        all_passed = True
        results = {}
        
        for phase_name, phase_func in phases:
            print(f"\n🔄 Esecuzione fase: {phase_name}")
            result = phase_func()
            results[phase_name] = result
            all_passed = all_passed and result
            
            if result:
                print(f"✅ Fase {phase_name}: SUCCESSO")
            else:
                print(f"❌ Fase {phase_name}: FALLITA")
        
        # Report finale
        self._print_final_report(results, all_passed)
        return all_passed
    
    def _print_final_report(self, results: Dict[str, bool], all_passed: bool):
        """Stampa report finale unificato"""
        print("\n" + "="*80)
        print("📊 REPORT FINALE SUITE UNIFICATA")
        print("="*80)
        
        for phase, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{phase:20} {status}")
        
        print("\n" + "="*80)
        if all_passed:
            print("🎉 SUCCESSO: Tutti i test sono stati superati!")
            print("✨ Il progetto AnalisiOpenData è completamente funzionante")
            print("🚀 Pronto per l'uso in produzione")
        else:
            print("⚠️  ATTENZIONE: Alcuni test sono falliti")
            print("🔧 Rivedere le componenti segnalate")
        
        print("="*80)


def main():
    """Funzione principale per eseguire la suite unificata"""
    suite = UnifiedTestSuite()
    success = suite.run_all_tests()
    
    # Exit con codice appropriato
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
