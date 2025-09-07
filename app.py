import streamlit as st
import numpy as np
import plotly.graph_objects as go

# -------------------- Page Config --------------------
st.set_page_config(
    page_title="Digital Twin: Brain Simulation",
    layout="wide",
    page_icon="🧠"
)

# -------------------- Custom Styling --------------------
st.markdown("""
<style>
body {
    background-color: #111111;
    color: #fdfdfd;
    font-family: 'Poppins', sans-serif;
}
h1 {
    text-align: center;
    color: #00FFFF;
    text-shadow: 0px 0px 12px #00FFFF;
    margin-bottom: 30px;
}
.stSlider label, .stSlider div {
    color: #fdfdfd;
    font-weight: 500;
}
.stButton>button {
    background-color: #00FFFF;
    color: #111111;
    border-radius: 12px;
    padding: 8px 18px;
    font-weight: bold;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# -------------------- Title --------------------
st.markdown("<h1>🧠 Digital Twin: Brain Simulation</h1>", unsafe_allow_html=True)

# -------------------- Layout --------------------
col1, col2 = st.columns([1,2])

with col1:
    st.markdown("### Adjust Your Brain State")
    stress = st.slider("Perceived Stress (0-100)", 0, 100, 50)
    sleep = st.slider("Sleep Quality (0-10)", 0, 10, 7)
    activity = st.slider("Lifestyle Activity (0-10)", 0, 10, 5)
    run_btn = st.button("Run Simulation")

with col2:
    plot_placeholder = st.empty()
    explanation_placeholder = st.empty()

# -------------------- Simulation Function --------------------
def simulate_brain(stress, sleep, activity):
    t = np.linspace(0, 10, 150)

    # Neurotransmitter curves (normalized 0-1)
    cortisol = 0.5 + (stress/100)*np.exp(-0.4*t) + 0.02*np.random.randn(len(t))
    dopamine = 0.5 + (activity/10)*0.3 - (stress/100)*0.1 + 0.02*np.random.randn(len(t))
    serotonin = 0.5 + (sleep/10)*0.3 - (stress/100)*0.05 + 0.02*np.random.randn(len(t))

    # Keep values between 0–1
    cortisol = np.clip(cortisol, 0, 1)
    dopamine = np.clip(dopamine, 0, 1)
    serotonin = np.clip(serotonin, 0, 1)

    # -------------------- Plotly Figure --------------------
    fig = go.Figure()

    # Cortisol
    fig.add_trace(go.Scatter(
        x=t, y=cortisol, mode='lines', name='Cortisol',
        line=dict(color='#FF4136', width=6, dash='solid'),
        hovertemplate='Cortisol: %{y:.2f}'
    ))

    # Dopamine
    fig.add_trace(go.Scatter(
        x=t, y=dopamine, mode='lines', name='Dopamine',
        line=dict(color='#2ECC40', width=6, dash='dash'),
        hovertemplate='Dopamine: %{y:.2f}'
    ))

    # Serotonin
    fig.add_trace(go.Scatter(
        x=t, y=serotonin, mode='lines', name='Serotonin',
        line=dict(color='#0074D9', width=6, dash='dot'),
        hovertemplate='Serotonin: %{y:.2f}'
    ))

    fig.update_layout(
        title="Neurotransmitter Response Over Time",
        xaxis_title="Time (s)",
        yaxis_title="Normalized Level",
        plot_bgcolor="#111111",
        paper_bgcolor="#111111",
        font=dict(color="#fdfdfd", family="Poppins"),
        legend=dict(x=0.75, y=1.15, bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=20,r=20,t=60,b=20),
        hovermode="x unified"
    )

    # -------------------- Explanation --------------------
    explanation = f"""
### 🧾 Simulation Results

- **Stress Level:** {stress}/100  
- **Sleep Quality:** {sleep}/10  
- **Lifestyle Activity:** {activity}/10  

**Cortisol (Stress Hormone):**  
Rises when stress is high. Too much long-term cortisol may cause fatigue and anxiety.  

**Dopamine (Motivation & Reward):**  
Increases with activity. It fuels drive, focus, and positive mood.  

**Serotonin (Mood Stabilizer):**  
Improves with better sleep and balance. It’s linked to calmness and emotional stability.  

🧠 *This simulation is a simplified digital twin of your brain chemistry.  
It shows how lifestyle and stress interact with biology in real-time.*  
"""
    return fig, explanation

# -------------------- Run Simulation --------------------
if run_btn:
    fig, explanation = simulate_brain(stress, sleep, activity)
    plot_placeholder.plotly_chart(fig, use_container_width=True)
    explanation_placeholder.markdown(explanation)
