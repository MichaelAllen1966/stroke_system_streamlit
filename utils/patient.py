class Patient:
    """
    Patient class. 
    The only method is __init__ for creating a patient (with assignment of
    patient id and length of stay).
    """

    def __init__(self, 
        patient_id, hasu_los, asu_los, esd_los, use_asu, use_esd):
        """
        Contructor for new patient.
        """
        self.id = patient_id
        self.los_hasu = hasu_los
        self.los_asu = asu_los
        self.los_esd = esd_los
        self.use_asu = use_asu
        self.use_esd = use_esd

        return