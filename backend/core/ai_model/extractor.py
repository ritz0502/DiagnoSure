# core/ai_model/extractor.py

from core.models import ExtractedMedicine

class MedicineExtractor:
    """
    Dummy extractor that returns hardcoded medicines.
    This avoids OCR dependencies (EasyOCR, fuzzy matching).
    Replace this later if real OCR is needed.
    """

    def __init__(self):
        # Lazy load medicine names - don't query DB at init time
        self._medicine_names = None

    @property
    def medicine_names(self):
        """Lazy load medicine names from DB"""
        if self._medicine_names is None:
            try:
                self._medicine_names = list(
                    ExtractedMedicine.objects.values_list('name', flat=True)
                )
            except:
                # If table doesn't exist yet (during migration), return empty
                self._medicine_names = []
        return self._medicine_names

    def extract_medicines_from_image(self, image_path=None):
        """
        Instead of OCR, return hardcoded or DB-based medicines.
        """
        # Example: pretend the image always contains Paracetamol 500mg
        try:
            med = ExtractedMedicine.objects.get(name__icontains="Paracetamol")
            med.confidence = 1.0  # 100% since it's hardcoded
            return [med]
        except ExtractedMedicine.DoesNotExist:
            return []

    # Keeping API compatibility with old methods
    def extract_potential_medicines(self, text_results):
        return []

    def match_medicines_fuzzy(self, potential_meds):
        return []
