"""
Ejercicio: Encontrar el primer número repetido en una lista.

Restricciones:
- No usar collections.Counter
- Solución óptima en O(n)

Este tipo de ejercicio es frecuente en entrevistas técnicas.
"""

nums = [4, 1, 7, 3, 9, 2, 8, 3, 1]


# --- Solución O(n) con set() ---

def primer_duplicado_set(nums):
    """
    Usa set() para búsquedas en O(1) → complejidad total O(n).

    Nota: solo tipos hashables pueden ir en un set.
        - Válidos: int, float, str, tuple
        - No válidos: list, dict
    """
    vistos = set()
    for i in nums:
        if i in vistos:
            return i
        vistos.add(i)
    return None


# --- Solución O(n²) con lista (menos eficiente) ---

def primer_duplicado_lista(nums):
    """
    Usa una lista normal → búsquedas O(n) → complejidad total O(n²).
    Funciona, pero escala mal para listas grandes.
    """
    vistos = []
    for i in nums:
        if i in vistos:
            return i
        vistos.append(i)
    return None


if __name__ == "__main__":
    print("Lista:", nums)
    print("Primer duplicado (set, O(n)):", primer_duplicado_set(nums))
    print("Primer duplicado (lista, O(n²)):", primer_duplicado_lista(nums))
