def transform_pvcalc_data(raw: dict) -> dict:
    monthly_raw = raw.get("outputs", {}).get("monthly", {}).get("fixed", [])
    totals_raw = raw.get("outputs", {}).get("totals", {}).get("fixed", {})

    monthly = []
    for month_data in monthly_raw:
        monthly.append(
            {
                "month": month_data.get("month"),
                "E_d": month_data.get("E_d"),
                "E_m": month_data.get("E_m"),
                "H(i)_d": month_data.get("H(i)_d"),
                "H(i)_m": month_data.get("H(i)_m"),
                "SD_m": month_data.get("SD_m"),
            }
        )

    yearly = {
        "E_d": totals_raw.get("E_d"),
        "E_m": totals_raw.get("E_m"),
        "E_y": totals_raw.get("E_y"),
        "H(i)_d": totals_raw.get("H(i)_d"),
        "H(i)_m": totals_raw.get("H(i)_m"),
        "H(i)_y": totals_raw.get("H(i)_y"),
        "SD_m": totals_raw.get("SD_m"),
        "SD_y": totals_raw.get("SD_y"),
        "l_aoi": totals_raw.get("l_aoi"),
        "l_spec": totals_raw.get("l_spec"),
        "l_tg": totals_raw.get("l_tg"),
        "l_total": totals_raw.get("l_total"),
    }

    return {"monthly": monthly, "yearly": yearly}
