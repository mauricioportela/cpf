"""CPF validation utilities."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass(frozen=True)
class CPFAnalysis:
    raw: str
    cleaned: str
    length: int
    has_only_digits: bool
    is_formatted: bool
    has_invalid_chars: bool


class CPF:
    """Representa e valida um CPF."""

    def __init__(self, value: str, development: bool = False) -> None:
        self.raw = value
        self.development = development
        self.cleaned = self._sanitize(value)
        self.analysis = self._analyze_input(value, self.cleaned)

    @staticmethod
    def _sanitize(value: str) -> str:
        return "".join(ch for ch in value if ch.isdigit())

    @staticmethod
    def _analyze_input(raw: str, cleaned: str) -> CPFAnalysis:
        has_only_digits = raw.isdigit()
        is_formatted = any(ch in raw for ch in ".-")
        has_invalid_chars = not has_only_digits and any(
            not ch.isdigit() and ch not in ".-" and not ch.isspace() for ch in raw
        )
        return CPFAnalysis(
            raw=raw,
            cleaned=cleaned,
            length=len(cleaned),
            has_only_digits=has_only_digits,
            is_formatted=is_formatted,
            has_invalid_chars=has_invalid_chars,
        )

    def validate(self) -> Dict[str, Any]:
        """Valida o CPF e retorna detalhes (úteis no modo desenvolvimento)."""
        details: Dict[str, Any] = {"analysis": self.analysis}
        if self.analysis.length != 11:
            details["reason"] = "CPF deve ter 11 dígitos."
            return {"valid": False, **details}

        digits = [int(ch) for ch in self.cleaned]
        if len(set(digits)) == 1:
            details["reason"] = "CPF com todos os dígitos iguais é inválido."
            return {"valid": False, **details}

        dv1_info = self._calculate_digit(digits[:9], factor_start=10)
        dv2_info = self._calculate_digit(digits[:9] + [dv1_info["dv"]], factor_start=11)
        valid = dv1_info["dv"] == digits[9] and dv2_info["dv"] == digits[10]

        if self.development:
            details["dv1"] = dv1_info
            details["dv2"] = dv2_info

        if not valid:
            details["reason"] = "Dígitos verificadores não conferem."

        return {"valid": valid, **details}

    @staticmethod
    def _calculate_digit(digits: List[int], factor_start: int) -> Dict[str, Any]:
        factors = list(range(factor_start, 1, -1))
        products = [digit * factor for digit, factor in zip(digits, factors)]
        total = sum(products)
        remainder = total % 11
        dv = 0 if remainder < 2 else 11 - remainder
        return {
            "digits": digits,
            "factors": factors,
            "products": products,
            "sum": total,
            "remainder": remainder,
            "dv": dv,
        }

    def dv_visualization(self) -> Dict[str, Any]:
        """Retorna a visualização do cálculo dos dígitos verificadores."""
        if self.analysis.length != 11:
            return {"error": "CPF deve ter 11 dígitos para calcular o DV."}

        digits = [int(ch) for ch in self.cleaned]
        dv1_info = self._calculate_digit(digits[:9], factor_start=10)
        dv2_info = self._calculate_digit(digits[:9] + [dv1_info["dv"]], factor_start=11)
        return {"dv1": dv1_info, "dv2": dv2_info}

    def __repr__(self) -> str:
        return f"CPF(value={self.raw!r}, development={self.development!r})"
