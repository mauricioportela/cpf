"""Demonstra diferentes formas de uso da classe CPF."""

from pprint import pprint

from cpf import CPF


EXEMPLOS = [
    ("CPF válido sem máscara", CPF("52998224725")),
    ("CPF válido com máscara", CPF("529.982.247-25")),
    ("CPF válido com espaços", CPF(" 529.982.247-25 ")),
    ("CPF inválido (dígito verificador)", CPF("52998224724")),
    ("CPF inválido (todos dígitos iguais)", CPF("111.111.111-11")),
    ("CPF com caracteres inválidos", CPF("529.982.247-2A")),
    ("Modo desenvolvimento", CPF("52998224725", development=True)),
]


def main() -> None:
    print("=" * 72)
    print("Demonstração da classe CPF")
    print("=" * 72)

    for titulo, cpf in EXEMPLOS:
        print(f"\n{titulo}:")
        print(f"  Objeto: {cpf!r}")
        resultado = cpf.validate()
        pprint(resultado, sort_dicts=False)

    print("\nVisualização detalhada do cálculo dos dígitos verificadores:")
    visualizacao = CPF("52998224725").dv_visualization()
    pprint(visualizacao, sort_dicts=False)


if __name__ == "__main__":
    main()
