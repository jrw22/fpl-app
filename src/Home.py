import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Local imports
from utils import get_data as fpl

# Title of the app
st.title("FPL Analysis")

# Initialise session state variables
st.session_state.team_id = ""
st.session_state.last_gameweek = ""

# Get data - user input
st.session_state.team_id = st.text_input(label="Enter your team ID")
st.markdown("Your team ID is the number found in the url on the Points page of the FPL website, e.g. fantasy.premierleague.com/entry/**2368852**/event/7")
st.session_state.last_gameweek = st.text_input(label="What was the most recent gameweek? e.g. 7", max_chars=2)

if st.session_state.team_id and st.session_state.last_gameweek:
    st.session_state.last_gameweek = int(st.session_state.last_gameweek)
    ###  Display headline stats -------------------
    st.session_state.team_info = fpl.get_team_general_info(team_id=st.session_state.team_id)
    # Team name
    st.title(st.session_state.team_info['name'])
    # First row: Team Manager and Years Active
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Team Manager", value=f"{st.session_state.team_info['player_first_name']} {st.session_state.team_info['player_last_name']}")
    with col2:
        st.metric(label="Years Active", value=st.session_state.team_info['years_active'])

    # Second row: Overall Points and Overall Rank
    col3, col4 = st.columns(2)
    with col3:
        st.metric(label="Overall Points", value=st.session_state.team_info['summary_overall_points'])
    with col4:
        st.metric(label="Overall Rank", value=st.session_state.team_info['summary_overall_rank'])

    # Third row: Gameweek Points and Rank
    col5, col6 = st.columns(2)
    with col5:
        st.metric(label=f"GW{st.session_state.last_gameweek} Points", value=st.session_state.team_info['summary_event_points'])
    with col6:
        st.metric(label=f"GW{st.session_state.last_gameweek} Rank", value=st.session_state.team_info['summary_event_rank'])

    team_name, points, average_points, highest_points, gameweek_rank, overall_rank, team_value, transfers, transfers_cost, captain, captain_points, total_points_per_line_season = fpl.get_data(team_id = st.session_state.team_id, last_gameweek = st.session_state.last_gameweek)

    ###  Display plots -------------------

    ## GAMEWEEK POINTS
    gameweek = np.arange(1, st.session_state.last_gameweek+1)
    fig = go.Figure()
    # Team FPL points
    fig.add_trace(go.Scatter(
        x=gameweek, 
        y=points, 
        mode='lines+markers',
        name='Team FPL points',
        line=dict(color='blue'),
        marker=dict(size=8)
    ))
    # Average FPL points
    fig.add_trace(go.Scatter(
        x=gameweek, 
        y=average_points, 
        mode='lines+markers',
        name='Average FPL points',
        line=dict(color='black'),
        marker=dict(size=8)
    ))
    # Highest FPL points
    fig.add_trace(go.Scatter(
        x=gameweek, 
        y=highest_points, 
        mode='lines+markers',
        name='Highest FPL points',
        line=dict(color='red'),
        marker=dict(size=8)
    ))
    # Update layout
    fig.update_layout(
        title=f"Team Performance",
        xaxis_title="Gameweek",
        yaxis_title="FPL Points",
        legend_title="Metrics",
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        width=800,  # Adjust width if needed
        height=500  # Adjust height if needed
    )
    st.plotly_chart(fig)

    ## GAMEWEEK RANK
    gameweekRank = np.array(gameweek_rank)
    fig_rank = go.Figure()
    # GW Rank (Bar chart)
    fig_rank.add_trace(go.Bar(
        x=gameweek,
        y=gameweekRank,
        name="GW Rank",
        marker_color='blue'
    ))
    # Overall Rank (Line chart)
    fig_rank.add_trace(go.Scatter(
        x=gameweek,
        y=overall_rank,
        mode='lines+markers',
        name="Overall Rank",
        line=dict(color='red'),
        marker=dict(size=8)
    ))
    # Update layout
    fig_rank.update_layout(
        title="Team Rank",
        xaxis_title="Gameweek",
        yaxis_title="Rank",
        yaxis_range=[0, max(gameweekRank) + 400000],  # Adjust range based on data
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        barmode='overlay',  # To overlay bar and line
    )
    st.plotly_chart(fig_rank)

    ## TEAM VALUE
    team_value_normalised = list(map(lambda x: x / 10, team_value))
    fig_value = go.Figure()
    # Team Value (Bar chart)
    fig_value.add_trace(go.Bar(
        x=gameweek,
        y=team_value_normalised,
        name="Team Value",
        marker_color='blue'
    ))
    # Update layout
    fig_value.update_layout(
        title="Team Value (incl. bank)",
        xaxis_title="Gameweek",
        yaxis_title="Team Value (in million)",
        yaxis_range=[min(team_value_normalised) - 0.5, max(team_value_normalised) + 0.5],
        showlegend=False
    )
    st.plotly_chart(fig_value)

    ## TEAM TRANSFERS
    fig_transfers = go.Figure()
    # Number of Transfers (Bar chart)
    fig_transfers.add_trace(go.Bar(
        x=gameweek,
        y=transfers,
        name="Number of Transfers",
        marker_color='blue'
    ))
    # Transfers Cost (Line chart)
    fig_transfers.add_trace(go.Scatter(
        x=gameweek,
        y=transfers_cost,
        mode='lines+markers',
        name="Transfers Cost",
        line=dict(color='red'),
        marker=dict(size=8)
    ))
    # Update layout
    fig_transfers.update_layout(
        title="Transfers and Transfer Cost",
        xaxis_title="Gameweek",
        yaxis_title="Number of Transfers",
        yaxis2=dict(
            title="Transfer Cost",
            overlaying="y",  # Overlay the second y-axis
            side="right",
            range=[0, max(transfers_cost) + 1]
        ),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        barmode='overlay'  # Overlay bars and lines
    )
    st.plotly_chart(fig_transfers)

    ## CAPTAIN POINTS
    captain_points = np.array(captain_points)
    # Create captain display labels
    captain_display = [f"{n+1} - {captain[n]}" for n in range(st.session_state.last_gameweek)]
    # Mask for Captain Points > 3
    mask1 = captain_points > 3
    # Mask for Captain Points <= 3
    mask2 = captain_points <= 3
    # Masks for colouring
    captain_points_filtered_mask1 = [captain_points[i] * 2 for i in range(len(captain_points)) if mask1[i]]
    captain_points_filtered_mask2 = [captain_points[i] * 2 for i in range(len(captain_points)) if mask2[i]]
    fig_captain = go.Figure()
    # Bar chart for Captain Points > 3 (Green)
    fig_captain.add_trace(go.Bar(
        x=gameweek[mask1],
        y=captain_points_filtered_mask1,
        name="Captain Points > 3",
        marker_color='green'
    ))
    # Bar chart for Captain Points <= 3 (Red)
    fig_captain.add_trace(go.Bar(
        x=gameweek[mask2],
        y=captain_points_filtered_mask2,
        name="Captain Points <= 3",
        marker_color='firebrick'
    ))
    # Update layout
    fig_captain.update_layout(
        title="Captain FPL Points",
        xaxis_title="Gameweek",
        yaxis_title="Captain Points",
        yaxis_range=[0, max(captain_points) * 2 + 5],
        xaxis=dict(
            tickvals=gameweek,
            ticktext=captain_display,
            tickangle=90
        ),
        showlegend=True
    )

else:
    st.info("⚽ Enter your team ID and the most recent GW to get started!")
