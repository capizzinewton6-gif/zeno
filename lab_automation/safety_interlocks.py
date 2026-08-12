"""Safety interlocks — fume hood velocity, thermal runaway, gas leak alarms."""


class SafetyInterlocks:
    """Evaluate lab safety interlock conditions."""

    HOOD_MIN_FACE_VELOCITY_FPM = 100  # OSHA/ANSI minimum

    def check_fume_hood(self, face_velocity_fpm):
        ok = face_velocity_fpm >= self.HOOD_MIN_FACE_VELOCITY_FPM
        return {
            "face_velocity_fpm": face_velocity_fpm,
            "status": "OK" if ok else "ALARM",
            "message": "Adequate face velocity." if ok else
                       f"Low face velocity ({face_velocity_fpm} fpm < {self.HOOD_MIN_FACE_VELOCITY_FPM} fpm). Reduce sash.",
        }

    def thermal_runaway(self, current_T_C, setpoint_C, rate_C_per_min, threshold_rate=2.0):
        over_temp = current_T_C > setpoint_C + 10
        runaway = rate_C_per_min > threshold_rate
        status = "OK"
        if runaway:
            status = "RUNAWAY-ALARM"
        elif over_temp:
            status = "OVER-TEMP"
        return {
            "current_T_C": current_T_C,
            "setpoint_C": setpoint_C,
            "rate_C_per_min": rate_C_per_min,
            "status": status,
            "action": "Kill heat, quench, evacuate." if status == "RUNAWAY-ALARM"
                      else ("Reduce heat input." if status == "OVER-TEMP" else "Normal."),
        }

    def gas_leak(self, sensor_ppm, threshold_ppm=25):
        alarm = sensor_ppm >= threshold_ppm
        return {
            "sensor_ppm": sensor_ppm,
            "threshold_ppm": threshold_ppm,
            "status": "ALARM" if alarm else "OK",
            "action": "Evacuate, ventilate, shut gas supply." if alarm else "Normal.",
        }

    def pressure_interlock(self, pressure_bar, max_bar=10):
        return {
            "pressure_bar": pressure_bar,
            "max_bar": max_bar,
            "status": "ALARM" if pressure_bar >= max_bar else "OK",
            "action": "Vent and reduce pressure." if pressure_bar >= max_bar else "Normal.",
        }
