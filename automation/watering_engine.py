class WateringEngine:
    def __init__(self):
        self.cooldown_active = False
        self.last_watered_timestamp = 0

    def evaluate_watering(self, soil_moisture: float, threshold: float, water_tank_level: float = 100.0) -> dict:
        """
        Evaluates sensor conditions against thresholds to decide pump action.
        Prevents continuous rapid activation using simple logic gates.
        """
        action_required = False
        reason = "optimal"

        if water_tank_level <= 10.0:
            return {"action": False, "reason": "low_water_tank"}

        if soil_moisture < threshold:
            action_required = True
            reason = "soil_moisture_below_threshold"
        else:
            reason = "moisture_sufficient"

        return {
            "action": action_required,
            "reason": reason,
            "soil_moisture": soil_moisture,
            "threshold": threshold
        }