import numpy as np
import random
import simpy
from utils.system import System
from utils.patient import Patient

"""
    prop_hasu_using_asu,
    prop_hasu_using_esd_only,
    prop_asu_using_esd,
    los_hasu_mu,
    los_hasu_sigma,
    los_asu_no_esd_mu,
    los_asu_no_esd_sigma,
    los_asu_with_esd_mu,
    los_asu_with_esd_sigma,
    los_esd_mu,
    los_esd_sigma,
    inter_arrival_time
"""

def log_normal_params(mean, cv):
    sd = mean * cv
    sigma = np.sqrt(np.log(1 + ((sd**2)/(mean**2))))
    mu = np.log(mean) - ((sigma**2)/2)
    return mu, sigma

class Model:
    """
    The main model class.

    The model class contains the model environment. The modelling environment is
    set up, and patient arrival and audit processes initiated. Patient arrival
    triggers a spell for that patient in hospital. Arrivals and audit continue
    for the duration of the model run. The audit is then summarised and bed
    occupancy (with 5th, 50th and 95th percentiles) plotted.
    """

    def __init__(self, _params):

        """
        Constructor class for new model.
        """
        self.env = simpy.Environment()

        # Default Parameters
        self.admissions_per_year = 1000

        self.prop_hasu_using_asu = 0.7
        self.prop_hasu_using_esd_only = 0.1
        self.prop_asu_using_esd = 0.5
        self.los_hasu_mean = 2.0
        self.los_hasu_cv = 1.0
        self.los_asu_no_esd_mean = 15
        self.los_asu_no_esd_cv = 1.0
        self.los_asu_with_esd_mean = 15
        self.los_asu_with_esd_cv = 1.0
        self.los_esd_mean = 20
        self.los_esd_cv = 1.0


        # update parameters above with _params
        if _params is not None:
            if 'admissions_per_year' in _params:
                self.admissions_per_year = _params['admissions_per_year']
            if 'prop_hasu_using_asu' in _params:
                self.prop_hasu_using_asu = _params['prop_hasu_using_asu']
            if 'prop_hasu_using_esd_only' in _params:
                self.prop_hasu_using_esd_only = _params['prop_hasu_using_esd_only']
            if 'prop_asu_using_esd' in _params:
                self.prop_asu_using_esd = _params['prop_asu_using_esd']
            if 'los_hasu_mean' in _params:
                self.los_hasu_mean = _params['los_hasu_mean']
            if 'los_hasu_cv' in _params:
                self.los_hasu_cv = _params['los_hasu_cv']
            if 'los_asu_no_esd_mean' in _params:
                self.los_asu_no_esd_mean = _params['los_asu_no_esd_mean']
            if 'los_asu_no_esd_cv' in _params:
                self.los_asu_no_esd_cv = _params['los_asu_no_esd_cv']
            if 'los_asu_with_esd_mean' in _params:
                self.los_asu_with_esd_mean = _params['los_asu_with_esd_mean']
            if 'los_asu_with_esd_cv' in _params:
                self.los_asu_with_esd_cv = _params['los_asu_with_esd_cv']
            if 'los_esd_mean' in _params:
                self.los_esd_mean = _params['los_esd_mean']
            if 'los_esd_cv' in _params:
                self.los_esd_cv = _params['los_esd_cv']

        
        # Calculate inter-arrival time
        self.inter_arrival_time = 365.0 / self.admissions_per_year

        # Convert parameters to log normal equivalents
        self.los_hasu_mu, self.los_hasu_sigma = \
            log_normal_params(self.los_hasu_mean, self.los_hasu_cv)
        self.los_asu_no_esd_mu, self.los_asu_no_esd_sigma = \
            log_normal_params(self.los_asu_no_esd_mean, self.los_asu_no_esd_cv)
        self.los_asu_with_esd_mu, self.los_asu_with_esd_sigma = \
            log_normal_params(self.los_asu_with_esd_mean, self.los_asu_with_esd_cv)
        self.los_esd_mu, self.los_esd_sigma = \
            log_normal_params(self.los_esd_mean, self.los_esd_cv)
        
        
    def audit_beds(self, delay):
        """
        Bed audit process. Begins by applying delay, then calls for audit at
        intervals.

        :param delay: delay (days) at start of model run for model warm-up.
        """

        # Delay first audit
        yield self.env.timeout(delay)

        # Continually generate audit requests until end of model run
        while True:
            # Call audit
            self.system.audit(self.env.now)
            # Delay 1 day until next call
            yield self.env.timeout(1)

    def new_admission(self, interarrival_time):
        """
        New admissions to hospital.

        :param interarrival_time: average time (days) between arrivals
        :param los: average length of stay (days)
        """
        while True:
            # Increment hospital admissions count
            self.system.admissions += 1

            # Set patient use of ASU and ESD
            use_asu=random.random() < self.prop_hasu_using_asu
            if use_asu:
                use_esd_after_asu = random.random() < self.prop_asu_using_esd
                use_esd_after_hasu = 0
            else:
                use_esd_after_hasu = random.random() < self.prop_hasu_using_esd_only
                use_esd_after_asu = 0

            # Check any use of ESD
            use_esd = use_esd_after_asu or use_esd_after_hasu
            
            # Set HASU length of stay
            hasu_los = random.lognormvariate(self.los_hasu_mu, self.los_hasu_sigma)
            
            # Set ASU length of stay
            if use_asu:
                if use_esd:
                    asu_los = random.lognormvariate(self.los_asu_with_esd_mu, self.los_asu_with_esd_sigma)
                else:
                    asu_los = random.lognormvariate(self.los_asu_no_esd_mu, self.los_asu_no_esd_sigma)
            else:
                asu_los=0,
            
            # Set ESD length of stay (currently use the same for ESD after HASU or ASU)
            if use_esd_after_asu:
                esd_los = random.lognormvariate(self.los_esd_mu, self.los_esd_sigma)
            elif use_esd_after_hasu:
                esd_los = random.lognormvariate(self.los_esd_mu, self.los_esd_sigma)
            else:
                esd_los=0

            # Generate new patient
            p = Patient(patient_id=self.system.admissions,
                        hasu_los=hasu_los,
                        asu_los=asu_los,
                        esd_los=esd_los,
                        use_asu=use_asu,
                        use_esd=use_esd                        
            )

            # Add patient to hospital patient dictionary
            self.system.patients[p.id] = p

            # Generate a patient spell in hospital (by calling spell method).
            # This triggers a patient admission and allows the next arrival to
            # be set before the paitent spell is finished
            spell = self.spell(p)
            self.env.process(spell)

            # Set and call delay before looping back to new patient admission
            next_admission = random.expovariate(1 / interarrival_time)
            yield self.env.timeout(next_admission)
            

    def run(self, warm_up, sim_duration):
        """
        Controls the main model run. Initialises model and patient arrival and
        audit processes. Instigates the run. At end of run calls for an audit
        summary and bed occupancy plot
        """

        # Set up hospital (calling Hospital class)
        self.system = System()

        # Set up starting processes: new admissions and bed  audit (with delay)
        self.env.process(self.new_admission(self.inter_arrival_time))
        self.env.process(self.audit_beds(delay=warm_up))

        # Start model run
        self.env.run(until=sim_duration + warm_up)

        # At end of run call for bed audit summary and bed occupancy plot
        self.system.build_audit_report()
        self.system.chart()

        
    def spell(self, p):
        """Patient spell in HASU/ASU/ESD"""

        # HASU
        self.system.hasu_count += 1
        # Wait for HASU length of stay
        yield self.env.timeout(p.los_hasu)
        self.system.hasu_count -= 1

        # ASU
        if p.use_asu:
            self.system.asu_count += 1
            # Wait for ASU length of stay
            yield self.env.timeout(p.los_asu)
            self.system.asu_count -= 1

        # ESD
        if p.use_esd:
            self.system.esd_count += 1
            # Wait for ESD length of stay
            yield self.env.timeout(p.los_esd)
            self.system.esd_count -= 1

        # Delete patient from system dictionary
        del self.system.patients[p.id]