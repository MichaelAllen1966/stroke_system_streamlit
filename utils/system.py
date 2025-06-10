import pandas as pd
import matplotlib.pyplot as plt

class System:
    """
    System class holds:
    1) Dictionary of patients present
    2) List of audit times
    3) List of beds occupied at each audit time
    4) Current total beds occupied
    5) Admissions to data

    Methods:

    __init__: Set up system instance

    audit: records number of beds occupied

    build_audit_report: builds audit report at end of run (calculate 5th, 50th
    and 95th percentile bed occupancy.

    chart: plot beds occupied over time (at end of run)
    """

    def __init__(self):
        self.patients = {}
        self.audit_time = []
        self.audit_times = []
        self.hasu_beds_occupied = []
        self.asu_beds_occupied = []
        self.esd_beds_occupied = []
        self.admissions = 0
        self.asu_count = 0
        self.hasu_count = 0
        self.esd_count = 0

    def audit(self, time):
        """
        Audit method. When called appends current simulation time to audit_time
        list, and appends current bed counts to lists.
        """
        
        self.audit_time.append(time)
        self.hasu_beds_occupied.append(self.hasu_count)
        self.asu_beds_occupied.append(self.asu_count)
        self.esd_beds_occupied.append(self.esd_count)


    def build_audit_report(self):
        """
        This method is called at end of run. It creates a pandas DataFrame,
        transfers audit times and bed counts to the DataFrame, and 
        calculates/stores 5th, 50th and 95th percentiles.
        """
        self.audit_report = pd.DataFrame()
        self.audit_report['Time'] = self.audit_time
        
        # Record bed counts at each audit time
        self.audit_report['Occupied_hasu_beds'] = self.hasu_beds_occupied
        self.audit_report['Occupied_asu_beds'] = self.asu_beds_occupied
        self.audit_report['Occupied_esd_beds'] = self.esd_beds_occupied

        # Count 
        self.audit_report_summary = pd.Series(name='Result')
        self.audit_report_summary['hasu_5th_percentile'] = self.audit_report['Occupied_hasu_beds'].quantile(0.05)
        self.audit_report_summary['hasu_median'] = self.audit_report['Occupied_hasu_beds'].quantile(0.5)
        self.audit_report_summary['hasu_95th_percentile'] = self.audit_report['Occupied_hasu_beds'].quantile(0.95)
        self.audit_report_summary['asu_5th_percentile'] = self.audit_report['Occupied_asu_beds'].quantile(0.05)
        self.audit_report_summary['asu_median'] = self.audit_report['Occupied_asu_beds'].quantile(0.5)
        self.audit_report_summary['asu_95th_percentile'] = self.audit_report['Occupied_asu_beds'].quantile(0.95)
        self.audit_report_summary['esd_5th_percentile'] = self.audit_report['Occupied_esd_beds'].quantile(0.05)
        self.audit_report_summary['esd_median'] = self.audit_report['Occupied_esd_beds'].quantile(0.5)
        self.audit_report_summary['esd_95th_percentile'] = self.audit_report['Occupied_esd_beds'].quantile(0.95)
        self.audit_report_summary = self.audit_report_summary.round(1)
   

        

    def chart(self):
        """
        This method is called at end of run. It plots beds occupancy over the
        model run, with 5%, 50% and 95% percentiles.
        """

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        x = self.audit_report['Time']
        y1 = self.audit_report['Occupied_hasu_beds']
        y2 = self.audit_report['Occupied_asu_beds']
        y3 = self.audit_report['Occupied_esd_beds']
        ax.plot(x - 100, y1, color='blue', label='hasu')
        ax.plot(x - 100, y2, color='green', label='asu')
        #ax.plot(x, y3, color='red', label='esd')

        ax.fill_between(x, self.audit_report['Occupied_hasu_beds'].quantile(0.05),
                        self.audit_report['Occupied_hasu_beds'].quantile(0.95),
                        color='blue', alpha=0.2)
        ax.fill_between(x, self.audit_report['Occupied_asu_beds'].quantile(0.05),
                        self.audit_report['Occupied_asu_beds'].quantile(0.95),
                        color='green', alpha=0.2)
        #ax.fill_between(x, self.audit_report['Occupied_esd_beds'].quantile(0.05),
        #                self.audit_report['Occupied_esd_beds'].quantile(0.95),
        #                color='red', alpha=0.2)
        
        ax.set_xlabel('Day')
        ax.set_ylabel('Occupancy (people)')
        txt = "Shaded areas show 5th to 95th percentile occupancy"
        ax.text(0.5, 0.95, txt, ha='center', va='center', transform=ax.transAxes,
            bbox=dict(facecolor='white', alpha=0.5))
        ax.legend()
        self.chart = ax
        # Save
        plt.savefig('./output/bed_occupancy.png', dpi=300, bbox_inches='tight')
        
        return