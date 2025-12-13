import math

class ASCVDCalculator:
    """Calculateur ASCVD (Atherosclerotic Cardiovascular Disease) 10-year risk"""
    
    @staticmethod
    def calculate(age, gender, race, total_cholesterol, hdl, systolic_bp,
                  on_bp_medication=False, diabetic=False, smoker=False):
        """
        Calcule le risque ASCVD à 10 ans
        
        Retourne: Risque en pourcentage
        """
        
        # Coefficients pour l'équation de risque
        if gender == 'male':
            if race == 'white':
                ln_age = 12.344
                ln_total_chol = 11.853
                ln_hdl = -7.990
                ln_sbp_treated = 1.797
                ln_sbp_untreated = 1.764
                ln_smoker = 7.837
                ln_diabetic = 0.658
                ln_age_total_chol = -2.664
                ln_age_smoker = -1.665
            else:  # African American
                ln_age = 2.469
                ln_total_chol = 0.302
                ln_hdl = -0.307
                ln_sbp_treated = 1.916
                ln_sbp_untreated = 1.809
                ln_smoker = 0.549
                ln_diabetic = 0.645
                ln_age_total_chol = 0
                ln_age_smoker = 0
        else:  # female
            if race == 'white':
                ln_age = -29.799
                ln_total_chol = 4.884
                ln_hdl = -13.540
                ln_sbp_treated = 2.019
                ln_sbp_untreated = 2.768
                ln_smoker = 7.574
                ln_diabetic = 0.661
                ln_age_total_chol = -1.665
                ln_age_smoker = -1.665
            else:  # African American
                ln_age = 17.114
                ln_total_chol = 0.940
                ln_hdl = -18.920
                ln_sbp_treated = 29.291
                ln_sbp_untreated = 27.820
                ln_smoker = 0.691
                ln_diabetic = 0.874
                ln_age_total_chol = 0
                ln_age_smoker = 0
        
        # Calcul des termes logarithmiques
        ln_age_val = math.log(age)
        ln_total_chol_val = math.log(total_cholesterol)
        ln_hdl_val = math.log(hdl)
        ln_sbp_val = math.log(systolic_bp)
        
        # Calcul de la somme
        if on_bp_medication:
            individual_sum = (ln_age * ln_age_val +
                            ln_total_chol * ln_total_chol_val +
                            ln_hdl * ln_hdl_val +
                            ln_sbp_treated * ln_sbp_val +
                            (ln_smoker if smoker else 0) +
                            (ln_diabetic if diabetic else 0) +
                            ln_age_total_chol * ln_age_val * ln_total_chol_val +
                            ln_age_smoker * ln_age_val * (1 if smoker else 0))
        else:
            individual_sum = (ln_age * ln_age_val +
                            ln_total_chol * ln_total_chol_val +
                            ln_hdl * ln_hdl_val +
                            ln_sbp_untreated * ln_sbp_val +
                            (ln_smoker if smoker else 0) +
                            (ln_diabetic if diabetic else 0) +
                            ln_age_total_chol * ln_age_val * ln_total_chol_val +
                            ln_age_smoker * ln_age_val * (1 if smoker else 0))
        
        # Baseline survival et calcul final
        if gender == 'male':
            if race == 'white':
                baseline_survival = 0.9144
                mean_coefficient_sum = 61.18
            else:
                baseline_survival = 0.8954
                mean_coefficient_sum = 19.54
        else:
            if race == 'white':
                baseline_survival = 0.9665
                mean_coefficient_sum = -29.18
            else:
                baseline_survival = 0.9533
                mean_coefficient_sum = 86.61
        
        # Calculer le risque
        risk = 1 - math.pow(baseline_survival, math.exp(individual_sum - mean_coefficient_sum))
        risk_percentage = risk * 100
        
        return round(risk_percentage, 2)
 
