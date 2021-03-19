from .wrapper import CasinoClass


class CasinoService:
    @staticmethod
    def get_casino(merch_id, merch_key):
        casino = CasinoClass(merch_id, merch_key)
        return casino

