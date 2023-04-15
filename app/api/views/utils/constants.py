PRODUCTS_MAPPINGS = {
    "ind_cco_fin_ult1": "Current Accounts",
    "ind_cder_fin_ult1": "Derivada Account",
    "ind_cno_fin_ult1": "Payroll Account",
    "ind_ctju_fin_ult1": "Junior Account",
    "ind_ctma_fin_ult1": "Más Particular Account",
    "ind_ctop_fin_ult1": "Particular Account",
    "ind_ctpp_fin_ult1": "Particular Plus Account",
    "ind_deco_fin_ult1": "Short-term deposits",
    "ind_deme_fin_ult1": "Medium-term deposits",
    "ind_dela_fin_ult1": "Long-term deposits",
    "ind_ecue_fin_ult1": "E-Account",
    "ind_fond_fin_ult1": "Funds",
    "ind_hip_fin_ult1": "Mortgage",
    "ind_plan_fin_ult1": "Pensions",
    "ind_pres_fin_ult1": "Loans",
    "ind_reca_fin_ult1": "Taxes",
    "ind_tjcr_fin_ult1": "Credit Card",
    "ind_valo_fin_ult1": "Securities",
    "ind_viv_fin_ult1": "Home Account",
    "ind_nomina_ult1": "Payroll",
    "ind_nom_pens_ult1": "Pensions",
    "ind_recibo_ult1": "Direct Debit",
}


INPUT_MAPPING = {
    "sexo": "gender",
    "pais_residencia": "country_code",
    "nomprov": "city",
    "antiguedad": "seniority",
    "segmento": "segment",
    "tiprel_1mes": "relationship_type",
    "ind_actividad_cliente": "activity_level",
    "renta": "income",
}

USER_ACTIVITY_MAPPING = {
    0: "INACTIVE",
    1: "ACTIVE",
}

USER_RELATIONSHIP_MAPPING = {
    "A": "ACTIVE",
    "I": "INACTIVE",
    "P": "POTENTIAL",
    "R": "POTENTIAL",
}

USER_SEGMENT_MAPPING = {
    "01 - TOP": "VIP",
    "02 - PARTICULARES": "INDIVIDUAL",
    "03 - UNIVERSITARIO": "UNIVERSITY",
}

USER_GENDER_MAPPING = {
    "H": "MALE",
    "V": "FEMALE",
}


BASE_USER_DATA_TEMPLATE = {
    "fecha_dato": "2016-06-28",
    "ncodpers": "15889",
    "ind_empleado": "F",
    "pais_residencia": "ES",
    "sexo": "V",
    "age": "56",
    "fecha_alta": "1995-01-16",
    "ind_nuevo": "0",
    "antiguedad": "256",
    "indrel": "1",
    "ult_fec_cli_1t": "",
    "indrel_1mes": "1",
    "tiprel_1mes": "A",
    "indresi": "S",
    "indext": "N",
    "conyuemp": "N",
    "canal_entrada": "KAT",
    "indfall": "N",
    "tipodom": "1",
    "cod_prov": "28",
    "nomprov": "MADRID",
    "ind_actividad_cliente": "1",
    "renta": "326124.9",
    "segmento": "01 - TOP",
}
