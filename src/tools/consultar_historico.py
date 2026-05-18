def consultar_historico_paciente(paciente_id: str):
    return {
        "paciente_id": paciente_id,
        "historico": [
            "Baixa vitamina D",
            "Sono irregular",
            "Uso de suplemento de ferro"
        ]
    }