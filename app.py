import streamlit as st
import os
import shutil
import subprocess
import json

st.set_page_config(page_title="Intelligent Traffic System", layout="centered")
st.title("🚦 Intelligent Traffic System")

st.write("Upload a traffic video below to analyze congestion and traffic statistics.")

uploaded_file = st.file_uploader("Upload a traffic video", type=["mp4", "avi"])

if uploaded_file is not None:
    input_video_path = os.path.join("temp", uploaded_file.name)
    os.makedirs("temp", exist_ok=True)

    with open(input_video_path, "wb") as f:
        f.write(uploaded_file.read())

    st.video(input_video_path)

    if st.button("Analyze Traffic"):
        st.info("Analyzing traffic... please wait.")

        result_path = os.path.join("temp", "output.avi")
        data_path = os.path.join("temp", "analysis_data.json")
        full_data_path = os.path.abspath(data_path)

        try:
            subprocess.run(
                ["python", "main.py", input_video_path, result_path, data_path],
                check=True
            )

            st.success("Analysis complete!")
            st.video(result_path)

            with open(full_data_path, "r") as f:
                analysis_data = json.load(f)

            st.metric("Vehicles Detected", analysis_data.get("vehicle_count", "N/A"))
            st.metric("Congestion Level", analysis_data.get("congestion_level", "N/A"))

            stats = analysis_data.get("detailed_statistics", {})

            if stats:
                st.subheader("📊 Advanced Traffic Analytics")

                st.write(f"**Average Speed (km/h):** {stats.get('average_speed_kmph')}")
                st.write(f"**Traffic Flow Rate (veh/min):** {stats.get('traffic_flow_rate_veh_per_min')}")
                st.write(f"**Speed Variance Index:** {stats.get('speed_variance_index')}")
                st.write(f"**Congestion Severity Score:** {stats.get('congestion_severity_score')}/10")
                st.write(f"**Estimated Average Delay (sec):** {stats.get('estimated_average_delay_sec')}")
                st.write(f"**Traffic Stability Coefficient:** {stats.get('traffic_stability_coefficient')}")
                st.write(f"**CO₂ Emission Impact Index:** {stats.get('co2_emission_impact_index')}")
                st.write(f"**Peak Hour Probability:** {stats.get('peak_hour_probability')}")

                st.markdown("### 🚗 Lane Utilization (%)")
                for lane, value in stats.get("lane_utilization_percent", {}).items():
                    st.progress(int(value))
                    st.caption(f"{lane}: {value}%")

            suggestions = analysis_data.get("suggestions", [])
            if suggestions:
                st.subheader("Optimization Suggestions")
                for suggestion in suggestions:
                    st.markdown(f"- {suggestion}")

        except Exception as e:
            st.error(f"Error during analysis: {e}")

if st.button("Clear Results"):
    shutil.rmtree("temp", ignore_errors=True)
    st.experimental_rerun()
