#!/usr/bin/env python3
"""PLNE global par bibliotheque de tournees candidates.

Ce script implemente l'option 2 de `modele_global_tournees.md`.

Il ne choisit pas entre S1/S2/S3/S4. Il choisit directement combien de fois
effectuer chaque tournee candidate par annee, tout en dimensionnant la flotte.

Dependance:
    python3 -m pip install pulp

Execution:
    python3 scripts/optimisation_tournees_pulp.py
"""

from __future__ import annotations

from dataclasses import dataclass


try:
    import pulp
except ModuleNotFoundError as exc:  # pragma: no cover - message utilisateur
    raise SystemExit(
        "PuLP n'est pas installe. Installez-le avec:\n"
        "  python3 -m pip install pulp\n"
        "puis relancez:\n"
        "  python3 scripts/optimisation_tournees_pulp.py"
    ) from exc


YEARS = [1, 2, 3, 4, 5]
TRUCK_TYPES = [1, 2]
ACID_CITIES = ["AN", "CH", "GA", "BR", "HA"]

DAYS_PER_YEAR = 250
HOURS_PER_DAY = 9
SPEED_KMH = 70

BUY_COST = {1: 140_000, 2: 200_000}
INITIAL_FLEET = {1: 4, 2: 6}
MAINTENANCE_PER_TRUCK = 5_000
DRIVER_YEAR_COST = 35 * HOURS_PER_DAY * DAYS_PER_YEAR
KM_COST = 0.60
ALPHA = 0.20
MIN_DELIVERY_T = 5.0
MAX_TRUCKS_BY_TYPE = 20
MAX_ROTATIONS_PER_ROUTE_YEAR = 3_000
SOLVER_TIME_LIMIT_S = 20

BASE_DEMAND = {year: 30_000 for year in YEARS}
ACID_DEMAND = {
    1: {"AN": 9_000, "CH": 12_000, "GA": 2_000, "BR": 6_200, "HA": 350},
    2: {"AN": 9_000, "CH": 12_000, "GA": 2_000, "BR": 6_200, "HA": 825},
    3: {"AN": 9_000, "CH": 12_000, "GA": 2_000, "BR": 6_200, "HA": 1_300},
    4: {"AN": 9_000, "CH": 12_000, "GA": 2_000, "BR": 6_200, "HA": 1_300},
    5: {"AN": 9_000, "CH": 12_000, "GA": 2_000, "BR": 6_200, "HA": 1_300},
}


@dataclass(frozen=True)
class Route:
    name: str
    truck_type: int
    distance_km: float
    time_h: float
    acid_capacity_t: float
    base_capacity_t: float
    acid_cities: tuple[str, ...]


def t(distance_km: float, acid_stops: int = 0, load_base: bool = False, unload_base: bool = False) -> float:
    """Temps d'une rotation selon les conventions de test_annuel.md."""
    return (
        distance_km / SPEED_KMH
        + acid_stops * 1.0
        + (0.5 if load_base else 0.0)
        + (1.0 if unload_base else 0.0)
    )


ROUTES = [
    # Type 1, acide seul.
    Route("T1_acid_AN", 1, 210, t(210, acid_stops=1), 16.5, 0.0, ("AN",)),
    Route("T1_acid_CH", 1, 200, t(200, acid_stops=1), 16.5, 0.0, ("CH",)),
    Route("T1_acid_GA", 1, 280, t(280, acid_stops=1), 16.5, 0.0, ("GA",)),
    Route("T1_acid_BR", 1, 200, t(200, acid_stops=1), 16.5, 0.0, ("BR",)),
    Route("T1_acid_HA", 1, 120, t(120, acid_stops=1), 16.5, 0.0, ("HA",)),
    Route("T1_acid_CH_BR", 1, 260, t(260, acid_stops=2), 16.5, 0.0, ("CH", "BR")),
    Route("T1_acid_GA_BR", 1, 280, t(280, acid_stops=2), 16.5, 0.0, ("GA", "BR")),
    Route("T1_acid_AN_HA", 1, 215, t(215, acid_stops=2), 16.5, 0.0, ("AN", "HA")),
    # Type 1, base directe. Un camion peut faire deux rotations par jour,
    # mais le modele annuel gere cela via la contrainte de temps.
    Route("T1_base_direct", 1, 210, t(210, load_base=True, unload_base=True), 0.0, 16.5, ()),
    # Type 2, couplage acide/base par Anvers.
    # Variante avec grand compartiment base et petit compartiment acide.
    Route("T2_AN_small_acid_big_base", 2, 210, t(210, acid_stops=1, load_base=True, unload_base=True), 5.5, 16.5, ("AN",)),
    # Variante avec grand compartiment acide et petit compartiment base.
    Route("T2_AN_big_acid_small_base", 2, 210, t(210, acid_stops=1, load_base=True, unload_base=True), 16.5, 5.5, ("AN",)),
    Route("T2_AN_HA_big_acid_small_base", 2, 215, t(215, acid_stops=2, load_base=True, unload_base=True), 16.5, 5.5, ("AN", "HA")),
]


def sale_value(truck_type: int, year: int) -> float:
    """Valeur de revente simplifiee en fonction de l'annee de vente."""
    return BUY_COST[truck_type] / ((1 + ALPHA) ** year)


def build_model() -> tuple[pulp.LpProblem, dict]:
    model = pulp.LpProblem("transport_chimique_tournees", pulp.LpMinimize)

    x = pulp.LpVariable.dicts(
        "rotations",
        ((r.name, year) for r in ROUTES for year in YEARS),
        lowBound=0,
        upBound=MAX_ROTATIONS_PER_ROUTE_YEAR,
        cat=pulp.LpInteger,
    )
    q_acid = pulp.LpVariable.dicts(
        "acid",
        ((r.name, city, year) for r in ROUTES for city in ACID_CITIES for year in YEARS),
        lowBound=0,
        cat=pulp.LpContinuous,
    )
    q_base = pulp.LpVariable.dicts(
        "base",
        ((r.name, year) for r in ROUTES for year in YEARS),
        lowBound=0,
        cat=pulp.LpContinuous,
    )
    fleet = pulp.LpVariable.dicts(
        "fleet",
        ((truck_type, year) for truck_type in TRUCK_TYPES for year in YEARS),
        lowBound=0,
        upBound=MAX_TRUCKS_BY_TYPE,
        cat=pulp.LpInteger,
    )
    buy = pulp.LpVariable.dicts(
        "buy",
        ((truck_type, year) for truck_type in TRUCK_TYPES for year in YEARS),
        lowBound=0,
        upBound=MAX_TRUCKS_BY_TYPE,
        cat=pulp.LpInteger,
    )
    sell = pulp.LpVariable.dicts(
        "sell",
        ((truck_type, year) for truck_type in TRUCK_TYPES for year in YEARS),
        lowBound=0,
        upBound=MAX_TRUCKS_BY_TYPE,
        cat=pulp.LpInteger,
    )

    route_by_name = {route.name: route for route in ROUTES}

    # Objectif: achat - revente + entretien + chauffeur + cout kilometrique.
    model += (
        pulp.lpSum(BUY_COST[k] * buy[(k, year)] for k in TRUCK_TYPES for year in YEARS)
        - pulp.lpSum(sale_value(k, year) * sell[(k, year)] for k in TRUCK_TYPES for year in YEARS)
        + pulp.lpSum(
            (MAINTENANCE_PER_TRUCK + DRIVER_YEAR_COST) * fleet[(k, year)]
            for k in TRUCK_TYPES
            for year in YEARS
        )
        + pulp.lpSum(KM_COST * route.distance_km * x[(route.name, year)] for route in ROUTES for year in YEARS)
    )

    # Couverture acide.
    for year in YEARS:
        for city in ACID_CITIES:
            model += (
                pulp.lpSum(q_acid[(route.name, city, year)] for route in ROUTES)
                == ACID_DEMAND[year][city],
                f"demand_acid_{city}_{year}",
            )

    # Couverture base.
    for year in YEARS:
        model += (
            pulp.lpSum(q_base[(route.name, year)] for route in ROUTES) == BASE_DEMAND[year],
            f"demand_base_{year}",
        )

    # Capacites des tournees.
    for route in ROUTES:
        allowed = set(route.acid_cities)
        for year in YEARS:
            model += (
                pulp.lpSum(q_acid[(route.name, city, year)] for city in ACID_CITIES)
                <= route.acid_capacity_t * x[(route.name, year)],
                f"acid_capacity_{route.name}_{year}",
            )
            model += (
                q_base[(route.name, year)] <= route.base_capacity_t * x[(route.name, year)],
                f"base_capacity_{route.name}_{year}",
            )
            for city in ACID_CITIES:
                if city not in allowed:
                    model += (
                        q_acid[(route.name, city, year)] == 0,
                        f"city_forbidden_{route.name}_{city}_{year}",
                    )
                else:
                    model += (
                        q_acid[(route.name, city, year)] <= route.acid_capacity_t * x[(route.name, year)],
                        f"city_capacity_{route.name}_{city}_{year}",
                    )
                    model += (
                        q_acid[(route.name, city, year)] >= MIN_DELIVERY_T * x[(route.name, year)],
                        f"city_min_delivery_{route.name}_{city}_{year}",
                    )

    # Temps disponible par type de camion.
    for year in YEARS:
        for truck_type in TRUCK_TYPES:
            model += (
                pulp.lpSum(
                    route_by_name[route.name].time_h * x[(route.name, year)]
                    for route in ROUTES
                    if route.truck_type == truck_type
                )
                <= HOURS_PER_DAY * DAYS_PER_YEAR * fleet[(truck_type, year)],
                f"time_capacity_T{truck_type}_{year}",
            )

    # Evolution de flotte.
    for truck_type in TRUCK_TYPES:
        model += (
            fleet[(truck_type, 1)] == INITIAL_FLEET[truck_type] + buy[(truck_type, 1)] - sell[(truck_type, 1)],
            f"fleet_initial_T{truck_type}",
        )
        model += (
            sell[(truck_type, 1)] <= INITIAL_FLEET[truck_type],
            f"sell_initial_limit_T{truck_type}",
        )
        for year in YEARS[1:]:
            model += (
                fleet[(truck_type, year)]
                == fleet[(truck_type, year - 1)] + buy[(truck_type, year)] - sell[(truck_type, year)],
                f"fleet_balance_T{truck_type}_{year}",
            )
            model += (
                sell[(truck_type, year)] <= fleet[(truck_type, year - 1)],
                f"sell_limit_T{truck_type}_{year}",
            )

    return model, {
        "x": x,
        "q_acid": q_acid,
        "q_base": q_base,
        "fleet": fleet,
        "buy": buy,
        "sell": sell,
    }


def solve() -> None:
    model, var = build_model()
    solver = pulp.PULP_CBC_CMD(msg=False, timeLimit=SOLVER_TIME_LIMIT_S, gapRel=0.01)
    model.solve(solver)

    status = pulp.LpStatus[model.status]
    print(f"Status: {status}")
    if status != "Optimal":
        return

    print(f"Cout total: {pulp.value(model.objective):,.2f} euros")
    print()

    print("Flotte / achats / ventes")
    for year in YEARS:
        row = [f"Annee {year}"]
        for truck_type in TRUCK_TYPES:
            n = var["fleet"][(truck_type, year)].value()
            a = var["buy"][(truck_type, year)].value()
            v = var["sell"][(truck_type, year)].value()
            row.append(f"T{truck_type}: N={n:.0f}, achat={a:.0f}, vente={v:.0f}")
        print(" | ".join(row))

    print()
    print("Rotations retenues")
    for year in YEARS:
        print(f"Annee {year}")
        for route in ROUTES:
            rotations = var["x"][(route.name, year)].value()
            if rotations and rotations > 1e-6:
                base = var["q_base"][(route.name, year)].value()
                acid_parts = []
                for city in ACID_CITIES:
                    qty = var["q_acid"][(route.name, city, year)].value()
                    if qty and qty > 1e-6:
                        acid_parts.append(f"{city}={qty:.1f}t")
                acid_text = ", ".join(acid_parts) if acid_parts else "-"
                print(
                    f"  {route.name}: {rotations:.0f} rotations, "
                    f"acide [{acid_text}], base={base:.1f}t"
                )


if __name__ == "__main__":
    solve()
