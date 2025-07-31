import importlib
import yaml
from typing import Dict

class ConfigManager:
    """Loads configuration (rules, magic signatures) from config.py or external YAML."""

    def __init__(self, module_name: str = "ocracle.config.config", rule_file: str = None):
        self.module_name = module_name
        self.rule_file = rule_file
        self._config = None
        self._rules = None
        self._load_config()

    def _load_config(self):
        self._config = importlib.import_module(self.module_name)

        # Se è stato passato un file YAML, carica da lì
        if self.rule_file:
            with open(self.rule_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            # struttura interna: dict {name: pattern}
            self._rules = {
                rule["name"]: {
                    "description": rule.get("description", ""),
                    "pattern": rule["pattern"],
                }
                for rule in data.get("rules", [])
            }

    @property
    def rules(self) -> Dict[str, str]:
        if self._rules:
            return {name: r["pattern"] for name, r in self._rules.items()}
        return getattr(self._config, "RULES", {})

    @property
    def rules_full(self) -> Dict[str, Dict[str, str]]:
        """Ritorna regole complete (nome -> {description, pattern})"""
        if self._rules:
            return self._rules
        # genera struttura base anche da config.py
        return {name: {"description": "", "pattern": pat}
                for name, pat in getattr(self._config, "RULES", {}).items()}

    @property
    def magic_signatures(self) -> Dict[bytes, str]:
        return getattr(self._config, "MAGIC_SIGNATURES", {})

    def reload(self):
        importlib.reload(self._config)
