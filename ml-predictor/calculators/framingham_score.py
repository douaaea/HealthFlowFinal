import math

class FraminghamCalculator:
    """Calculateur du score de Framingham (risque à 10 ans) - Version optimisée"""
    
    # Tables de lookup pour les points
    AGE_POINTS_MALE = {
        range(0, 35): -9,
        range(35, 40): -4,
        range(40, 45): 0,
        range(45, 50): 3,
        range(50, 55): 6,
        range(55, 60): 8,
        range(60, 65): 10,
        range(65, 70): 11,
        range(70, 75): 12,
        range(75, 150): 13
    }
    
    AGE_POINTS_FEMALE = {
        range(0, 35): -7,
        range(35, 40): -3,
        range(40, 45): 0,
        range(45, 50): 3,
        range(50, 55): 6,
        range(55, 60): 8,
        range(60, 65): 10,
        range(65, 70): 12,
        range(70, 75): 14,
        range(75, 150): 16
    }
    
    CHOL_POINTS_MALE = {
        range(0, 160): 0,
        range(160, 200): 4,
        range(200, 240): 7,
        range(240, 280): 9,
        range(280, 500): 11
    }
    
    CHOL_POINTS_FEMALE = {
        range(0, 160): 0,
        range(160, 200): 4,
        range(200, 240): 8,
        range(240, 280): 11,
        range(280, 500): 13
    }
    
    HDL_POINTS = {
        range(60, 200): -1,
        range(50, 60): 0,
        range(40, 50): 1,
        range(0, 40): 2
    }
    
    BP_POINTS_UNTREATED = {
        range(0, 120): 0,
        range(120, 130): 1,
        range(130, 140): 2,
        range(140, 160): 3,
        range(160, 300): 4
    }
    
    BP_POINTS_TREATED = {
        range(0, 120): 1,
        range(120, 130): 2,
        range(130, 140): 3,
        range(140, 160): 4,
        range(160, 300): 5
    }
    
    # Tables de risque selon le total de points
    RISK_TABLE_MALE = {
        **{i: 1 for i in range(-10, 5)},  # Points < 5 = 1%
        5: 2, 6: 2, 7: 3, 8: 4, 9: 5, 10: 6,
        11: 8, 12: 10, 13: 12, 14: 16, 15: 20, 16: 25
    }
    
    RISK_TABLE_FEMALE = {
        **{i: 1 for i in range(-10, 13)},  # Points < 13 = 1%
        13: 2, 14: 2, 15: 3, 16: 4, 17: 5, 18: 6,
        19: 8, 20: 11, 21: 14, 22: 17, 23: 22, 24: 27
    }
    
    @staticmethod
    def _get_points_from_range_dict(value, range_dict):
        """Récupère les points depuis un dictionnaire avec des ranges"""
        for value_range, points in range_dict.items():
            if value in value_range:
                return points
        return 0
    
    @classmethod
    def calculate(cls, age, gender, total_cholesterol, hdl, systolic_bp, 
                  on_bp_medication=False, smoker=False, diabetic=False):
        """
        Calcule le score de Framingham
        
        Retourne: Risque à 10 ans en pourcentage
        """
        
        points = 0
        
        # Points pour l'âge
        age_points = cls.AGE_POINTS_MALE if gender == 'male' else cls.AGE_POINTS_FEMALE
        points += cls._get_points_from_range_dict(age, age_points)
        
        # Points pour le cholestérol
        chol_points = cls.CHOL_POINTS_MALE if gender == 'male' else cls.CHOL_POINTS_FEMALE
        points += cls._get_points_from_range_dict(total_cholesterol, chol_points)
        
        # Points pour le HDL
        points += cls._get_points_from_range_dict(hdl, cls.HDL_POINTS)
        
        # Points pour la pression artérielle
        bp_points = cls.BP_POINTS_TREATED if on_bp_medication else cls.BP_POINTS_UNTREATED
        points += cls._get_points_from_range_dict(systolic_bp, bp_points)
        
        # Points pour fumeur
        points += (4 if gender == 'male' else 3) if smoker else 0
        
        # Points pour diabète
        points += (2 if gender == 'male' else 4) if diabetic else 0
        
        # Calculer le risque depuis la table
        risk_table = cls.RISK_TABLE_MALE if gender == 'male' else cls.RISK_TABLE_FEMALE
        risk = risk_table.get(points, 30)  # 30% si points > max
        
        return risk
