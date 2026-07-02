"""Client for Octopus Energy's public Agile tariff API.

Agile is a half-hourly time-of-use tariff whose unit rate tracks the wholesale
market - exactly the signal this tool exploits. The API is public and needs no
key. Prices come back half-hourly, matching the carbon cadence, so an Agile day
maps straight onto our 48 planning slots. Parsing is separated from I/O for
network-free tests.

Tariff codes are regional, e.g. product ``AGILE-24-04-03`` with tariff
``E-1R-AGILE-24-04-03-C`` for GB region C (South West).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta

from community_energy_flex.data_sources.http import get_json
from community_energy_flex.data_sources.tariffs import (
    MultiBandTariff,
    multiband_from_half_hour_prices,
)
from community_energy_flex.domain.models import SLOTS_PER_DAY

BASE_URL = "https://api.octopus.energy/v1"


def _parse_dt(value: str) -> datetime:
    # e.g. "2026-07-01T00:00:00Z" -> timezone-aware UTC (the API is UTC).
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)


@dataclass(frozen=True)
class AgileRate:
    valid_from: datetime
    valid_to: datetime
    price_p: float


def parse_agile_rates(payload: dict) -> list[AgileRate]:
    """Parse the ``results`` array into rates sorted oldest-first."""
    rates = [
        AgileRate(
            valid_from=_parse_dt(r["valid_from"]),
            valid_to=_parse_dt(r["valid_to"]),
            price_p=float(r["value_inc_vat"]),
        )
        for r in payload.get("results", [])
    ]
    return sorted(rates, key=lambda r: r.valid_from)


def day_price_curve(
    rates: list[AgileRate], day: date, num_slots: int = SLOTS_PER_DAY
) -> list[float]:
    """Half-hourly price array for ``day`` (interpreted as a UTC date, matching
    the UTC carbon data the slots align to). Slots with no matching rate carry
    the previous slot's price forward."""
    by_start = {r.valid_from: r.price_p for r in rates}
    midnight = datetime(day.year, day.month, day.day, tzinfo=UTC)
    curve: list[float] = []
    last: float | None = None
    for i in range(num_slots):
        price = by_start.get(midnight + timedelta(minutes=30 * i))
        if price is None:
            price = last
        if price is None:
            raise ValueError(f"no Agile price for slot {i} on {day} and no earlier price")
        curve.append(price)
        last = price
    return curve


def agile_tariff_for_day(
    rates: list[AgileRate], day: date, standing_charge_p: float = 0.0
) -> MultiBandTariff:
    """Build a slot-aligned tariff for ``day`` from fetched Agile rates."""
    return multiband_from_half_hour_prices(
        day_price_curve(rates, day),
        standing_charge_p=standing_charge_p,
        name=f"Octopus Agile {day.isoformat()}",
        is_manual=False,
    )


class OctopusAgileClient:
    """Thin HTTP client. Inject ``fetch`` to test without a network."""

    def __init__(self, base_url: str = BASE_URL, fetch=None) -> None:
        self.base_url = base_url.rstrip("/")
        self._fetch = fetch or get_json

    def unit_rates(self, product_code: str, tariff_code: str) -> list[AgileRate]:
        url = (
            f"{self.base_url}/products/{product_code}"
            f"/electricity-tariffs/{tariff_code}/standard-unit-rates/"
        )
        return parse_agile_rates(self._fetch(url))
