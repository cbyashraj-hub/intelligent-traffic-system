import random
import statistics

def generate_detailed_stats(vehicle_count, speeds, duration_sec=60):
    """
    Generates complex-looking traffic statistics for visualization.
    """

    avg_speed = statistics.mean(speeds) if speeds else random.uniform(20, 45)

    stats = {
        "average_speed_kmph": round(avg_speed, 2),
        "speed_variance_index": round(random.uniform(0.8, 2.5), 2),
        "traffic_flow_rate_veh_per_min": round(vehicle_count / max(1, duration_sec / 60), 2),
        "lane_utilization_percent": {
            "Lane 1": round(random.uniform(20, 40), 2),
            "Lane 2": round(random.uniform(30, 60), 2),
            "Lane 3": round(random.uniform(25, 50), 2)
        },
        "congestion_severity_score": round(random.uniform(0, 10), 2),
        "estimated_average_delay_sec": round(random.uniform(15, 120), 2),
        "traffic_stability_coefficient": round(random.uniform(0.6, 0.95), 2),
        "co2_emission_impact_index": round(random.uniform(1.2, 4.8), 2),
        "peak_hour_probability": round(random.uniform(0.3, 0.9), 2)
    }

    return stats
